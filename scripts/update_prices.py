#!/usr/bin/env python3
"""Refreshes data.json with current CZ (mbenzin.cz) and DE (Tankerkoenig) station
prices for both border regions, plus the EUR/CZK exchange rate and a rolling
daily history of the cheapest price per fuel per side.

Run from the repo root: python3 scripts/update_prices.py
Requires TANKERKOENIG_API_KEY in the environment.
"""
import json
import os
import re
import sys
import urllib.request
from datetime import datetime, timezone, timedelta

import requests
from bs4 import BeautifulSoup

REPO_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_PATH = os.path.join(REPO_ROOT, "data.json")

TANKERKOENIG_KEY = os.environ.get("TANKERKOENIG_API_KEY", "").strip()

# Region anchors: mbenzin.cz town pages for CZ, Tankerkoenig radius search
# center point for DE. Radius is Tankerkoenig's max (25 km).
REGIONS = {
    "vogtland": {
        "label": "Sachsen · Vogtland",
        # "Vojtanov" has no standalone mbenzin.cz page (redirects to the
        # nationwide homepage) - Kraslice's page covers the whole Sokolov
        # district (30+ stations reaching to Karlovy Vary), so it's fetched
        # and then filtered down to the towns actually near this crossing.
        "cz_towns": ["Kraslice"],
        "cz_town_prefixes": ["Kraslice", "Vojtanov"],
        "de_center": {"lat": 50.3546, "lng": 12.4692},  # Klingenthal
    },
    "oberfranken": {
        "label": "Bayern · Oberfranken",
        "cz_towns": ["As", "Cheb"],
        "cz_town_prefixes": None,  # both town pages are already local enough
        "de_center": {"lat": 50.1740, "lng": 12.1320},  # Selb
    },
}

MAX_STATIONS_PER_SIDE = 10

CZ_LABEL_MAP = {
    "Benzín": "e10",
    "Nafta": "diesel",
    "Premium benzín": "premium",
}


def fetch_cz_town(town):
    """Scrape one mbenzin.cz town page into a list of station dicts."""
    url = f"https://www.mbenzin.cz/Ceny-benzinu-a-nafty/{town}"
    resp = requests.get(url, headers={"User-Agent": "Mozilla/5.0"}, timeout=20)
    resp.raise_for_status()

    # A town slug that doesn't exist on mbenzin.cz 301s to the generic
    # nationwide listing instead of 404ing - that would silently poison the
    # region with unrelated stations from across the country, so detect it
    # and skip rather than trust the page.
    final_path = resp.url.rstrip("/").rsplit("/", 1)[-1]
    if final_path.lower() != town.lower():
        print(f"WARNING: '{town}' redirected to '{resp.url}' (no such town page) - skipping", file=sys.stderr)
        return []

    soup = BeautifulSoup(resp.text, "html.parser")

    stations = []
    for row in soup.select("div.st-row"):
        name_el = row.select_one(".st-name span[itemprop=name]")
        locality_el = row.select_one("span[itemprop=addressLocality]")
        if not name_el or not locality_el:
            continue
        name = name_el.get_text(strip=True)
        locality = locality_el.get_text(strip=True)

        station = {"name": name, "town": locality}
        for price_el in row.select(".st-price"):
            lbl_el = price_el.select_one(".lbl")
            val_el = price_el.select_one(".val")
            if not lbl_el or not val_el:
                continue
            label = lbl_el.get_text(strip=True)
            key = CZ_LABEL_MAP.get(label)
            if not key:
                continue
            val_text = val_el.get_text(strip=True)
            if not val_text or val_text in ("–", "-"):
                continue
            try:
                station[key] = float(val_text.replace(",", "."))
            except ValueError:
                continue

        # Only keep stations with at least a benzin price - a row with no
        # recognizable prices is not useful for comparison.
        if "e10" in station or "diesel" in station:
            stations.append(station)
    return stations


def fetch_cz_region(town_list, town_prefixes=None):
    stations = []
    seen = set()
    for town in town_list:
        for s in fetch_cz_town(town):
            key = (s["name"], s["town"])
            if key in seen:
                continue
            seen.add(key)
            stations.append(s)

    if town_prefixes:
        stations = [s for s in stations if any(s["town"].startswith(p) for p in town_prefixes)]

    return stations[:MAX_STATIONS_PER_SIDE]


def fetch_de_region(center):
    if not TANKERKOENIG_KEY:
        raise RuntimeError("TANKERKOENIG_API_KEY is not set")
    url = (
        "https://creativecommons.tankerkoenig.de/json/list.php"
        f"?lat={center['lat']}&lng={center['lng']}&rad=25&sort=dist&type=all"
        f"&apikey={TANKERKOENIG_KEY}"
    )
    resp = requests.get(url, timeout=20)
    resp.raise_for_status()
    payload = resp.json()
    if not payload.get("ok"):
        raise RuntimeError(f"Tankerkoenig error: {payload.get('message')}")

    stations = []
    for s in payload.get("stations", []):
        if not s.get("isOpen", True):
            continue
        entry = {"name": s.get("brand") or s.get("name") or "Tankstelle", "town": s.get("place", "")}
        if s.get("e10") is not None:
            entry["e10"] = round(float(s["e10"]), 3)
        if s.get("e5") is not None:
            entry["e5"] = round(float(s["e5"]), 3)
        if s.get("diesel") is not None:
            entry["diesel"] = round(float(s["diesel"]), 3)
        if "e10" in entry or "diesel" in entry:
            stations.append(entry)
        if len(stations) >= MAX_STATIONS_PER_SIDE:
            break
    return stations


def fetch_fx_rate():
    resp = requests.get("https://api.frankfurter.app/latest?from=EUR&to=CZK", timeout=15)
    resp.raise_for_status()
    payload = resp.json()
    rate = round(float(payload["rates"]["CZK"]), 2)
    return rate, "frankfurter.app (EZB-Referenzkurs)"


def cheapest(stations, key):
    vals = [s[key] for s in stations if isinstance(s.get(key), (int, float))]
    return min(vals) if vals else None


def estimate_premium(stations, key_source, is_cz):
    """Fills in a premium richtwert for stations lacking a real value, then
    returns the cheapest premium value across the (real+estimated) set."""
    vals = []
    for s in stations:
        if isinstance(s.get("premium"), (int, float)):
            vals.append(s["premium"])
        elif isinstance(s.get(key_source), (int, float)):
            vals.append(round(s[key_source] + (2.40 if is_cz else 0.13), 3))
    return min(vals) if vals else None


def estimate_e5(stations, is_cz):
    vals = []
    for s in stations:
        if isinstance(s.get("e5"), (int, float)):
            vals.append(s["e5"])
        elif isinstance(s.get("e10"), (int, float)):
            vals.append(s["e10"] if is_cz else round(s["e10"] + 0.055, 3))
    return min(vals) if vals else None


def main():
    today = datetime.now(timezone(timedelta(hours=2))).strftime("%Y-%m-%d")
    now_iso = datetime.now(timezone(timedelta(hours=2))).strftime("%Y-%m-%dT%H:%M:%S+02:00")

    if os.path.exists(DATA_PATH):
        with open(DATA_PATH, encoding="utf-8") as f:
            existing = json.load(f)
    else:
        existing = {"history": {}}

    eur_czk, fx_source = fetch_fx_rate()

    regions_out = {}
    history_out = existing.get("history", {})

    for region_key, cfg in REGIONS.items():
        print(f"--- {region_key} ---")
        cz_stations = fetch_cz_region(cfg["cz_towns"], cfg.get("cz_town_prefixes"))
        print(f"CZ: {len(cz_stations)} stations")
        de_stations = fetch_de_region(cfg["de_center"])
        print(f"DE: {len(de_stations)} stations")

        regions_out[region_key] = {
            "label": cfg["label"],
            "cz": {"source": "mbenzin.cz", "stations": cz_stations},
            "de": {"source": "Tankerkönig API (Live-Stationsdaten)", "provisional": False, "stations": de_stations},
        }

        entry = {
            "date": today,
            "cz": {
                "e10": cheapest(cz_stations, "e10"),
                "e5": estimate_e5(cz_stations, is_cz=True),
                "premium": estimate_premium(cz_stations, "e10", is_cz=True),
                "diesel": cheapest(cz_stations, "diesel"),
            },
            "de": {
                "e10": cheapest(de_stations, "e10"),
                "e5": estimate_e5(de_stations, is_cz=False),
                "premium": estimate_premium(de_stations, "e10", is_cz=False),
                "diesel": cheapest(de_stations, "diesel"),
            },
            "fx": {"eurCzk": eur_czk},
        }
        entry["cz"] = {k: v for k, v in entry["cz"].items() if v is not None}
        entry["de"] = {k: v for k, v in entry["de"].items() if v is not None}

        entries = history_out.get(region_key, {}).get("entries", [])
        entries = [e for e in entries if e.get("date") != today]
        entries.append(entry)
        entries = entries[-60:]
        history_out[region_key] = {"entries": entries}

    out = {
        "updatedAt": now_iso,
        "fx": {"eurCzk": eur_czk, "source": fx_source},
        "regions": regions_out,
        "history": history_out,
    }

    with open(DATA_PATH, "w", encoding="utf-8") as f:
        json.dump(out, f, ensure_ascii=False, indent=2)
        f.write("\n")

    print(f"Wrote {DATA_PATH}")


if __name__ == "__main__":
    main()

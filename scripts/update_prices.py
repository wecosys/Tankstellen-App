#!/usr/bin/env python3
"""Refreshes data.json with current CZ (mbenzin.cz) and DE (Tankerkoenig) station
prices for both border regions, plus the EUR/CZK exchange rate and a rolling
daily history of the average price per fuel per side.

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
        # 08412 Werdau is a real PLZ users near here type in (see
        # PLZ_COORDS in index.html), but it's ~42 km from Klingenthal -
        # genuinely outside the 25 km crossing-area radius above, so no
        # station near it would ever appear otherwise. Fetched separately
        # (small radius, real coordinates) and kept OUT of the main
        # de.stations list used for the CZ/DE crossing comparison table -
        # it's not relevant to that comparison - and stored in
        # de.plzStations, consulted only by the client's PLZ-proximity tool.
        "plz_extra_anchors": [
            {"label": "Werdau", "lat": 50.7333, "lng": 12.3833, "radius": 10},
        ],
    },
    "oberfranken": {
        "label": "Bayern · Oberfranken",
        "cz_towns": ["As", "Cheb"],
        "cz_town_prefixes": None,  # both town pages are already local enough
        # mbenzin.cz's "nearest" sort for the Cheb page is relative to Cheb's
        # own center, not the actual border crossing - stations genuinely at
        # the crossing (e.g. Tank ONO in "Cheb, Horni Vojtanov", near
        # Skalná/Vojtanov) can rank low enough to fall off the top-N cut.
        # Boost anything whose (locality + street) mentions these crossings.
        "cz_priority_keywords": ["Vojtanov", "Skalná"],
        "de_center": {"lat": 50.1740, "lng": 12.1320},  # Selb
    },
    "erzgebirge": {
        "label": "Sachsen · Erzgebirgskreis",
        # Neither "Boží Dar" nor "Potůčky" has its own mbenzin.cz town page;
        # "Jachymov" is a valid nearby town page whose "nearest first" listing
        # covers both within ~15 km, filtered down to just those two crossings.
        "cz_towns": ["Jachymov"],
        "cz_town_prefixes": ["Boží Dar", "Potůčky"],
        "de_center": {"lat": 50.4263, "lng": 12.8424},  # midpoint Johanngeorgenstadt/Oberwiesenthal
    },
    "dresden": {
        "label": "Sachsen · Dresden/Osterzgebirge",
        # The A17/D8 motorway crossing itself is "Breitenau (DE) - Krásný Les
        # (CZ)" - a modern Autobahn border with no real settlement on either
        # side, and neither "Krasny-Les" nor "Petrovice" has an mbenzin.cz
        # town page. "Chabarovice" is a valid nearby page whose "nearest
        # first" listing already reaches Chlumec, Ústí nad Labem and Krupka
        # (the Erzgebirge foothill town on the DE-CZ border) within ~10 km,
        # without needing prefix filtering.
        "cz_towns": ["Chabarovice"],
        "cz_town_prefixes": None,
        "de_center": {"lat": 50.85, "lng": 13.95},  # Bad Gottleuba-Berggießhübel
    },
    "oberlausitz": {
        "label": "Sachsen · Oberlausitz",
        # Hrádek nad Nisou is directly on the border opposite Zittau, with
        # its own mbenzin.cz page and real stations right at the crossing
        # (0-200m) - no filtering or extra anchor needed for the crossing
        # itself.
        "cz_towns": ["Hradek-nad-Nisou"],
        "cz_town_prefixes": None,
        "de_center": {"lat": 50.9, "lng": 14.8},  # Zittau
        # Bautzen (~41 km from Zittau) is genuinely outside the 25 km
        # crossing-area radius, same situation as Werdau in vogtland above -
        # fetched separately into de.plzStations, not the main crossing table.
        "plz_extra_anchors": [
            {"label": "Bautzen", "lat": 51.1833, "lng": 14.4167, "radius": 10},
        ],
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

        # Some rows carry a separate streetAddress alongside addressLocality
        # (e.g. two unrelated "Tank ONO" stations in Cheb both show
        # addressLocality="Cheb" but differ only in streetAddress) - fold it
        # in so the two are distinguishable in the UI, not just internally.
        street_el = row.select_one("span[itemprop=streetAddress]")
        if street_el:
            street = street_el.get_text(strip=True)
            if street:
                locality = locality + ", " + street

        # mbenzin.cz's per-town page can still collapse two different
        # stations to the same (name, town) even after the above (e.g. no
        # streetAddress at all on either row), so (name, town) alone is not
        # a reliable identity for dedup - it would silently merge genuinely
        # different stations. The detail-page link href is unique per
        # station and used for that instead; it's dropped from the dict
        # before this feeds into data.json.
        link_el = row.select_one(".st-name")
        station_id = link_el.get("href") if link_el else None

        station = {"name": name, "town": locality, "_id": station_id}
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


def fetch_cz_region(town_list, town_prefixes=None, priority_keywords=None):
    stations = []
    seen = set()
    for town in town_list:
        for s in fetch_cz_town(town):
            # Fall back to (name, town) only if a station has no detail link
            # for some reason - better to risk a rare false-duplicate than
            # to stop deduping entirely.
            key = s["_id"] or (s["name"], s["town"])
            if key in seen:
                continue
            seen.add(key)
            stations.append(s)

    if town_prefixes:
        stations = [s for s in stations if any(s["town"].startswith(p) for p in town_prefixes)]

    if priority_keywords:
        # mbenzin.cz's own "nearest" sort is relative to the fetched town's
        # center, not to the actual border crossing - a station right at the
        # crossing (e.g. Tank ONO in "Cheb, Horni Vojtanov") can rank far
        # below unrelated in-town stations and fall off the MAX_STATIONS_PER_SIDE
        # cut. Stable-sort known border-relevant matches to the front first
        # so the cap doesn't drop them.
        stations.sort(key=lambda s: 0 if any(k in s["town"] for k in priority_keywords) else 1)

    stations = stations[:MAX_STATIONS_PER_SIDE]
    for s in stations:
        del s["_id"]
    return stations


def fetch_de_region(center, radius=25, limit=MAX_STATIONS_PER_SIDE):
    if not TANKERKOENIG_KEY:
        raise RuntimeError("TANKERKOENIG_API_KEY is not set")
    url = (
        "https://creativecommons.tankerkoenig.de/json/list.php"
        f"?lat={center['lat']}&lng={center['lng']}&rad={radius}&sort=dist&type=all"
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
        # Tankerkoenig already reports each station's real coordinates and
        # postal code - captured so the app can compute "cheapest near your
        # PLZ" client-side without any external geocoding call.
        if s.get("lat") is not None and s.get("lng") is not None:
            entry["lat"] = round(float(s["lat"]), 5)
            entry["lng"] = round(float(s["lng"]), 5)
        if s.get("postCode") is not None:
            entry["plz"] = str(s["postCode"])
        if s.get("e10") is not None:
            entry["e10"] = round(float(s["e10"]), 3)
        if s.get("e5") is not None:
            entry["e5"] = round(float(s["e5"]), 3)
        if s.get("diesel") is not None:
            entry["diesel"] = round(float(s["diesel"]), 3)
        if "e10" in entry or "diesel" in entry:
            stations.append(entry)
        if len(stations) >= limit:
            break
    return stations


def fetch_fx_rate():
    resp = requests.get("https://api.frankfurter.app/latest?from=EUR&to=CZK", timeout=15)
    resp.raise_for_status()
    payload = resp.json()
    rate = round(float(payload["rates"]["CZK"]), 2)
    return rate, "frankfurter.app (EZB-Referenzkurs)"


def average(vals):
    return round(sum(vals) / len(vals), 3) if vals else None


def average_price(stations, key):
    """History reference price: the MEAN across all fetched stations, not the
    cheapest one. A single-station minimum tends to sit flat for days at a
    time (the same station just doesn't reprice daily), which makes the
    Preisverlauf trend look broken even though it's technically correct -
    averaging over the whole set reflects genuine day-to-day market movement
    instead. The main station list/table is untouched by this - it still
    shows and highlights the real cheapest individual station."""
    vals = [s[key] for s in stations if isinstance(s.get(key), (int, float))]
    return average(vals)


def average_premium(stations, key_source, is_cz):
    """Fills in a premium richtwert for stations lacking a real value, then
    averages the premium value across the (real+estimated) set."""
    vals = []
    for s in stations:
        if isinstance(s.get("premium"), (int, float)):
            vals.append(s["premium"])
        elif isinstance(s.get(key_source), (int, float)):
            vals.append(round(s[key_source] + (2.40 if is_cz else 0.13), 3))
    return average(vals)


def average_e5(stations, is_cz):
    vals = []
    for s in stations:
        if isinstance(s.get("e5"), (int, float)):
            vals.append(s["e5"])
        elif isinstance(s.get("e10"), (int, float)):
            vals.append(s["e10"] if is_cz else round(s["e10"] + 0.055, 3))
    return average(vals)


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
        cz_stations = fetch_cz_region(cfg["cz_towns"], cfg.get("cz_town_prefixes"), cfg.get("cz_priority_keywords"))
        print(f"CZ: {len(cz_stations)} stations")
        de_stations = fetch_de_region(cfg["de_center"])
        print(f"DE: {len(de_stations)} stations")

        de_out = {"source": "Tankerkönig (Live-Stationsdaten)", "provisional": False, "stations": de_stations}

        plz_stations = []
        for anchor in cfg.get("plz_extra_anchors", []):
            fetched = fetch_de_region(anchor, radius=anchor.get("radius", 10))
            print(f"DE (extra anchor {anchor['label']}): {len(fetched)} stations")
            plz_stations.extend(fetched)
        if plz_stations:
            de_out["plzStations"] = plz_stations

        regions_out[region_key] = {
            "label": cfg["label"],
            "cz": {"source": "mbenzin.cz", "stations": cz_stations},
            "de": de_out,
        }

        entry = {
            "date": today,
            "cz": {
                "e10": average_price(cz_stations, "e10"),
                "e5": average_e5(cz_stations, is_cz=True),
                "premium": average_premium(cz_stations, "e10", is_cz=True),
                "diesel": average_price(cz_stations, "diesel"),
            },
            "de": {
                "e10": average_price(de_stations, "e10"),
                "e5": average_e5(de_stations, is_cz=False),
                "premium": average_premium(de_stations, "e10", is_cz=False),
                "diesel": average_price(de_stations, "diesel"),
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

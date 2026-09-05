# Changelog

Alle nennenswerten Änderungen an diesem Projekt werden hier dokumentiert.
Format angelehnt an [Keep a Changelog](https://keepachangelog.com/de/1.0.0/),
Versionierung nach [SemVer](https://semver.org/lang/de/).

## [2.1.1] - 2026-09-05

### Geändert
- Fußnote präzisiert: Tschechien hat Super E5 seit der Umstellung 2024 komplett abgeschafft (Natural 95 ist dort einheitlich E10) – der gleiche Preis bei "Super E10"/"Super E5" auf der CZ-Seite ist keine Näherung, sondern die einzige verfügbare Sorte. Vorher klang die Formulierung ("gilt 1:1 als Äquivalent") wie eine Vereinfachung.

## [2.1.0] - 2026-09-05

Echte Live-Automatisierung: keine manuellen Preis-Schnappschüsse mehr für GitHub Pages.

### Hinzugefügt
- `data.json`: Preisdaten liegen jetzt in einer eigenen JSON-Datei statt im Seiten-Code eingebettet; `index.html` lädt sie per `fetch()` und fällt bei Fehlern auf den eingebetteten Stand zurück
- `scripts/update_prices.py`: holt DE-Preise live über die Tankerkönig-API (Radius-Suche, echte Stationsdaten inkl. E10/E5/Diesel) und CZ-Preise per Scraping von mbenzin.cz (inkl. echter Premium/98-Werte, wo gemeldet), sowie den EUR/CZK-Kurs über frankfurter.app
- GitHub-Actions-Workflow (`.github/workflows/update-prices.yml`): läuft täglich 07:00 Uhr (Europe/Berlin) automatisch, aktualisiert `data.json` und committet die Änderung – läuft auf GitHub-Servern, unabhängig von jedem lokalen Rechner
- Tankerkönig-API-Key liegt als verstecktes GitHub-Actions-Secret (`TANKERKOENIG_API_KEY`), nicht im Klartext im Repo

### Geändert
- DE-Seite ist nicht mehr als "vorläufig" markiert, sobald echte Live-Daten vorliegen
- CZ-Stationsliste für Sachsen · Vogtland auf Kraslice- und Vojtanov-Orte gefiltert (die rohe mbenzin.cz-Kraslice-Seite deckt einen ganzen Landkreis bis Karlovy Vary ab)

### Bekannte Einschränkungen
- Nur die GitHub-Pages-Version (tanken.wecosys.com) wird automatisch aktualisiert. Das Claude Artifact kann aus Sandbox-Gründen nicht selbst per GitHub Action aktualisiert werden und bleibt auf manuelle Aktualisierung ("aktualisiere die Preise" im Chat) angewiesen.

## [2.0.0] - 2026-09-04

Kompletter Umbau von Länder-Durchschnitten auf echte Grenzregion-Stationen.

### Hinzugefügt
- Regions-Auswahl: **Sachsen · Vogtland** (Klingenthal/Werdau ↔ Vojtanov/Kraslice) und **Bayern · Oberfranken** (Selb ↔ Cheb/Aš)
- Echte, einzelne Tankstellen pro Region statt eines einheitlichen Länder-Durchschnitts (Quelle CZ: mbenzin.cz; Quelle DE: vorläufige manuelle Momentaufnahme, bis Tankerkönig-API-Key vorliegt)
- Alle vier Kraftstoffarten wieder verfügbar (Super E10, Super E5, Premium/98, Diesel), mit Kennzeichnung (`*`) wenn ein Wert ein Richtwert statt eines gemeldeten Preises ist
- Tankrechner: freie Auswahl der tatsächlichen CZ- und DE-Station statt automatischer Annahme der günstigsten
- Google-Maps-Link (Pin-Icon) an jeder Station, CZ und DE
- Frische-Hinweis im Status (Warnung ab > 36h altem Stand)

### Geändert
- "Benzin" konsistent in "Super E10" umbenannt
- Preisverlauf-Chart folgt jetzt Region + gewähltem Kraftstoff gemeinsam

### Bekannte Einschränkungen
- DE-Stationsdaten sind ein manueller Schnappschuss (kein Live-Feed) bis der Tankerkönig-API-Key vorliegt und eingebunden ist
- Keine automatische tägliche Aktualisierung aktiv (Cloud-Routine wegen Plattform-Limitierung deaktiviert; GitHub-Actions-Automatisierung noch nicht gebaut)

## [1.0.0] - 2026-09-03

Erste veröffentlichte Version: Länder-Durchschnittsvergleich Tschechien vs. Deutschland.

### Hinzugefügt
- Preisvergleich Benzin/Diesel, später erweitert um Super E5 und Premium (98 Oktan)
- Kronen-Euro-Umrechnung, Tankrechner, Preisverlauf-Chart
- CZ-Quelle: Tank ONO (tank-ono.cz); DE-Quelle: ADAC bundesweiter Tagesdurchschnitt
- Veröffentlichung als Claude Artifact mit `db`-Capability
- Hosting zusätzlich über eigene Domain (tanken.wecosys.com) via GitHub Pages, da IONOS-Webspace kein kostenloses SSL bot
- Copyright-Vermerk und LICENSE (All Rights Reserved)

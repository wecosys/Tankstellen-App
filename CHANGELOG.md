# Changelog

Alle nennenswerten Änderungen an diesem Projekt werden hier dokumentiert.
Format angelehnt an [Keep a Changelog](https://keepachangelog.com/de/1.0.0/),
Versionierung nach [SemVer](https://semver.org/lang/de/).

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

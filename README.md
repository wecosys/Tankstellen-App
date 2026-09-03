# Tankpreise Grenzvergleich

Vergleicht aktuelle Benzin- und Dieselpreise zwischen Tschechien und Deutschland, inklusive Kronen-Euro-Umrechnung und Preisverlauf.

**Live-App:** https://claude.ai/code/artifact/4c8f92f3-19a7-4b8f-ae60-539e67f26820

## Was die App zeigt

- Vier Kraftstoffarten im Vergleich: Benzin (Super E10 / Natural 95), Super E5, Premium (SuperPlus / Natural 98), Diesel
- CZ-Preise in Kronen und umgerechnet in Euro, DE-Preise als bundesweiter Tagesdurchschnitt
- Tankrechner (Liter → Gesamtpreis & Ersparnis)
- Preisverlauf-Chart (wächst täglich)

## Datenquellen

- **CZ:** [Tank ONO](https://tank-ono.cz/de/index.php?page=cenik) – Preisliste über alle Stationen
- **DE:** [ADAC](https://www.adac.de/news/aktueller-spritpreis/) – bundesweiter Tagesdurchschnitt für Super E10 und Diesel
- **Super E5 / SuperPlus (DE):** Richtwerte, berechnet als Aufschlag auf Super E10 (kein eigener Tagesdurchschnitt verfügbar)
- **Wechselkurs:** Marktkurs EUR/CZK

## Live-Aktualisierung

Die veröffentlichte App liest ihre Preisdaten aus einer an das Artifact gekoppelten Datenbank. Ein täglicher Cloud-Agent (07:00 Uhr, Europe/Berlin) ruft die Quellen neu ab und schreibt die aktuellen Werte sowie einen neuen Verlaufs-Datenpunkt in diese Datenbank – ohne dass die Seite selbst neu veröffentlicht werden muss.

## Dateien in diesem Repo

- [`index.html`](index.html) – eigenständige, offline-fähige Kopie der App (statischer Snapshot, ohne Live-Aktualisierung; die veröffentlichte Version oben ist die aktuelle)
- [`.claude/launch.json`](.claude/launch.json) – Konfiguration, um `index.html` lokal per Claude Code Browser-Preview zu öffnen

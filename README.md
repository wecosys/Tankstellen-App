# Tankpreise Grenzvergleich

Vergleicht aktuelle Benzin- und Dieselpreise zwischen Tschechien und Deutschland, inklusive Kronen-Euro-Umrechnung und Preisverlauf.

**Live-App (Artifact, mit täglicher Live-Aktualisierung):** https://claude.ai/code/artifact/4c8f92f3-19a7-4b8f-ae60-539e67f26820
**Live-App (eigene Domain, statischer Stand):** https://tanken.wecosys.com/

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

## Hosting über eigene Domain (GitHub Pages)

`index.html` wird zusätzlich über GitHub Pages unter der eigenen Subdomain `tanken.wecosys.com` ausgeliefert. Hintergrund: Die App war zunächst direkt auf dem IONOS-Webspace veröffentlicht, aber ohne SSL – das genutzte IONOS-Paket bietet kein kostenloses SSL-Zertifikat an. Lösung: Repo öffentlich gestellt, GitHub Pages aktiviert (Deploy aus `main`, Root-Verzeichnis) und die Subdomain per CNAME-DNS-Eintrag bei IONOS auf `wecosys.github.io` umgezogen. GitHub stellt dafür automatisch ein kostenloses Let's-Encrypt-Zertifikat aus.

Dabei musste am Hostnamen `tanken` zunächst der bestehende A-Record sowie die von IONOS automatisch angelegten (aber nie genutzten) Mail-Records entfernt werden, da ein CNAME der einzige Eintrag an einem Hostnamen sein darf.

- Custom-Domain-Konfiguration: [Repo-Einstellungen → Pages](https://github.com/wecosys/Tankstellen-App/settings/pages)
- Diese Version aktualisiert sich **nicht** automatisch täglich – sie zeigt immer den Stand des letzten `git push`, im Gegensatz zur Artifact-Version oben.

## Dateien in diesem Repo

- [`index.html`](index.html) – eigenständige, offline-fähige Kopie der App (statischer Snapshot; wird über GitHub Pages unter `tanken.wecosys.com` ausgeliefert)
- [`CNAME`](CNAME) – Custom-Domain-Konfiguration für GitHub Pages (Inhalt: `tanken.wecosys.com`)
- [`.claude/launch.json`](.claude/launch.json) – Konfiguration, um `index.html` lokal per Claude Code Browser-Preview zu öffnen

## Lizenz

© 2026 Michael Riedel. Alle Rechte vorbehalten. Siehe [LICENSE](LICENSE).

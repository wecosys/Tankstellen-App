# Tankpreise Grenzvergleich

**Version 2.0.0** · [Changelog](CHANGELOG.md)

Vergleicht echte Tankstellenpreise im deutsch-tschechischen Grenzgebiet – wählbar nach Region (Sachsen · Vogtland oder Bayern · Oberfranken) und Kraftstoff, inklusive Kronen-Euro-Umrechnung, Preisverlauf und Google-Maps-Links zu jeder Station.

**Live-App (Artifact):** https://claude.ai/code/artifact/4c8f92f3-19a7-4b8f-ae60-539e67f26820
**Live-App (eigene Domain):** https://tanken.wecosys.com/

## Was die App zeigt

- Regions-Auswahl: **Sachsen · Vogtland** (Klingenthal/Werdau ↔ Vojtanov/Kraslice) und **Bayern · Oberfranken** (Selb ↔ Cheb/Aš)
- Echte, einzelne Tankstellen je Region und Land (keine Länder-Durchschnitte), günstigste zuerst
- Vier Kraftstoffarten: Super E10, Super E5, Premium (98 Oktan), Diesel – mit `*`-Kennzeichnung, wenn ein Wert ein Richtwert statt eines gemeldeten Preises ist
- Tankrechner mit freier Auswahl der tatsächlichen CZ- und DE-Station
- Google-Maps-Link an jeder Station
- Preisverlauf-Chart je Region/Kraftstoff (wächst mit jeder Aktualisierung)

## Datenquellen

- **CZ:** [mbenzin.cz](https://www.mbenzin.cz/) – reale Stationspreise in Aš/Cheb/Vojtanov/Kraslice
- **DE:** aktuell eine manuell erfasste Momentaufnahme für Selb bzw. Klingenthal/Werdau – wechselt auf echte Live-Stationsdaten (Tankerkönig-API), sobald ein API-Key vorliegt
- **Super E5 / Premium (98 Oktan):** wo keine gemeldeten Werte vorliegen, Richtwerte als Aufschlag auf Super E10 (siehe Footnote in der App)
- **Wechselkurs:** Marktkurs EUR/CZK

## Aktualisierung

Aktuell **keine automatische Aktualisierung aktiv**. Die Preisdaten sind ein manueller Schnappschuss, der im Chat mit Claude ("aktualisiere die Preise") aufgefrischt wird. Eine ursprünglich eingerichtete tägliche Cloud-Routine wurde deaktiviert, da unbeaufsichtigte Datenbank-Schreibzugriffe an einem nicht umgehbaren Freigabe-Dialog scheitern (Plattform-Limitierung, kein Konfigurationsfehler). Eine GitHub-Actions-Automatisierung ist angedacht, aber noch nicht umgesetzt.

## Hosting über eigene Domain (GitHub Pages)

`index.html` wird zusätzlich über GitHub Pages unter der eigenen Subdomain `tanken.wecosys.com` ausgeliefert. Hintergrund: Die App war zunächst direkt auf dem IONOS-Webspace veröffentlicht, aber ohne SSL – das genutzte IONOS-Paket bietet kein kostenloses SSL-Zertifikat an. Lösung: Repo öffentlich gestellt, GitHub Pages aktiviert (Deploy aus `main`, Root-Verzeichnis) und die Subdomain per CNAME-DNS-Eintrag bei IONOS auf `wecosys.github.io` umgezogen. GitHub stellt dafür automatisch ein kostenloses Let's-Encrypt-Zertifikat aus.

Dabei musste am Hostnamen `tanken` zunächst der bestehende A-Record sowie die von IONOS automatisch angelegten (aber nie genutzten) Mail-Records entfernt werden, da ein CNAME der einzige Eintrag an einem Hostnamen sein darf.

- Custom-Domain-Konfiguration: [Repo-Einstellungen → Pages](https://github.com/wecosys/Tankstellen-App/settings/pages)
- Diese Version zeigt immer den Stand des letzten `git push`.

## Dateien in diesem Repo

- [`index.html`](index.html) – die App (wird über GitHub Pages unter `tanken.wecosys.com` ausgeliefert und als Claude-Artifact-Fragment veröffentlicht)
- [`CHANGELOG.md`](CHANGELOG.md) – Versionshistorie
- [`CNAME`](CNAME) – Custom-Domain-Konfiguration für GitHub Pages (Inhalt: `tanken.wecosys.com`)
- [`.claude/launch.json`](.claude/launch.json) – Konfiguration, um `index.html` lokal per Claude Code Browser-Preview zu öffnen

## Lizenz

© 2026 Michael Riedel. Alle Rechte vorbehalten. Siehe [LICENSE](LICENSE).

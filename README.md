# Tankpreise Grenzvergleich

**Version 2.1.1** · [Changelog](CHANGELOG.md)

Vergleicht echte Tankstellenpreise im deutsch-tschechischen Grenzgebiet – wählbar nach Region (Sachsen · Vogtland oder Bayern · Oberfranken) und Kraftstoff, inklusive Kronen-Euro-Umrechnung, Preisverlauf und Google-Maps-Links zu jeder Station.

**Live-App (Artifact):** https://claude.ai/code/artifact/4c8f92f3-19a7-4b8f-ae60-539e67f26820
**Live-App (eigene Domain, vollautomatisch):** https://tanken.wecosys.com/

## Was die App zeigt

- Regions-Auswahl: **Sachsen · Vogtland** (Klingenthal/Werdau ↔ Vojtanov/Kraslice) und **Bayern · Oberfranken** (Selb ↔ Cheb/Aš)
- Echte, einzelne Tankstellen je Region und Land (keine Länder-Durchschnitte), günstigste zuerst
- Vier Kraftstoffarten: Super E10, Super E5, Premium (98 Oktan), Diesel – mit `*`-Kennzeichnung, wenn ein Wert ein Richtwert statt eines gemeldeten Preises ist
- Tankrechner mit freier Auswahl der tatsächlichen CZ- und DE-Station
- Google-Maps-Link an jeder Station
- Preisverlauf-Chart je Region/Kraftstoff (wächst mit jeder Aktualisierung)

## Datenquellen

- **CZ:** [mbenzin.cz](https://www.mbenzin.cz/) – reale Stationspreise, live gescrapt (siehe `scripts/update_prices.py`)
- **DE:** [Tankerkönig-API](https://creativecommons.tankerkoenig.de/) – echte Live-Stationsdaten per Umkreissuche um Klingenthal bzw. Selb
- **Super E5 / Premium (98 Oktan):** wo keine gemeldeten Werte vorliegen, Richtwerte als Aufschlag auf Super E10 (siehe Footnote in der App)
- **Wechselkurs:** [frankfurter.app](https://www.frankfurter.app/) (EZB-Referenzkurs)

## Aktualisierung

**Vollautomatisch auf tanken.wecosys.com:** Ein täglicher GitHub-Actions-Workflow (`.github/workflows/update-prices.yml`, 07:00 Uhr Europe/Berlin) ruft Tankerkönig und mbenzin.cz neu ab, schreibt [`data.json`](data.json) und committet die Änderung – läuft komplett auf GitHub-Servern, unabhängig von jedem lokalen Rechner. Der Tankerkönig-API-Key liegt als GitHub-Actions-Secret (`TANKERKOENIG_API_KEY`), nie im Klartext im Repo.

`index.html` lädt `data.json` per `fetch()` beim Seitenaufruf; schlägt das fehl (z. B. lokal ohne Server), zeigt die Seite den eingebetteten Stand vom letzten `git push`.

**Claude Artifact:** Kann aus Sandbox-Gründen nicht selbst durch GitHub Actions aktualisiert werden (kein Zugriff auf die Artifact-Datenbank von außerhalb). Bleibt auf manuelle Aktualisierung im Chat mit Claude ("aktualisiere die Preise") angewiesen. Eine früher eingerichtete Cloud-Routine dafür wurde deaktiviert, da unbeaufsichtigte Datenbank-Schreibzugriffe an einem nicht umgehbaren Freigabe-Dialog scheitern (Plattform-Limitierung).

Workflow manuell anstoßen: [Actions → Update fuel prices → Run workflow](https://github.com/wecosys/Tankstellen-App/actions/workflows/update-prices.yml)

## Hosting über eigene Domain (GitHub Pages)

`index.html` wird zusätzlich über GitHub Pages unter der eigenen Subdomain `tanken.wecosys.com` ausgeliefert. Hintergrund: Die App war zunächst direkt auf dem IONOS-Webspace veröffentlicht, aber ohne SSL – das genutzte IONOS-Paket bietet kein kostenloses SSL-Zertifikat an. Lösung: Repo öffentlich gestellt, GitHub Pages aktiviert (Deploy aus `main`, Root-Verzeichnis) und die Subdomain per CNAME-DNS-Eintrag bei IONOS auf `wecosys.github.io` umgezogen. GitHub stellt dafür automatisch ein kostenloses Let's-Encrypt-Zertifikat aus.

Dabei musste am Hostnamen `tanken` zunächst der bestehende A-Record sowie die von IONOS automatisch angelegten (aber nie genutzten) Mail-Records entfernt werden, da ein CNAME der einzige Eintrag an einem Hostnamen sein darf.

- Custom-Domain-Konfiguration: [Repo-Einstellungen → Pages](https://github.com/wecosys/Tankstellen-App/settings/pages)

## Dateien in diesem Repo

- [`index.html`](index.html) – die App (wird über GitHub Pages unter `tanken.wecosys.com` ausgeliefert und als Claude-Artifact-Fragment veröffentlicht)
- [`data.json`](data.json) – aktuelle Preisdaten, täglich per GitHub Action aktualisiert
- [`scripts/update_prices.py`](scripts/update_prices.py) – holt die Preise (Tankerkönig + mbenzin.cz) und schreibt `data.json`
- [`.github/workflows/update-prices.yml`](.github/workflows/update-prices.yml) – täglicher Automatisierungs-Workflow
- [`CHANGELOG.md`](CHANGELOG.md) – Versionshistorie
- [`CNAME`](CNAME) – Custom-Domain-Konfiguration für GitHub Pages (Inhalt: `tanken.wecosys.com`)
- [`.claude/launch.json`](.claude/launch.json) – Konfiguration, um `index.html` lokal per Claude Code Browser-Preview zu öffnen

## Lizenz

© 2026 Michael Riedel. Alle Rechte vorbehalten. Siehe [LICENSE](LICENSE).

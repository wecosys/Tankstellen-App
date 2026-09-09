# Changelog

Alle nennenswerten Änderungen an diesem Projekt werden hier dokumentiert.
Format angelehnt an [Keep a Changelog](https://keepachangelog.com/de/1.0.0/),
Versionierung nach [SemVer](https://semver.org/lang/de/).

## [2.10.0] - 2026-09-09

### Hinzugefügt
- **Tankrechner: Fahrtkosten des Umwegs gegenrechnen.** Zwei neue, optionale Felder ("Zusätzliche km (Hin+Zurück)", "Verbrauch (l/100km)") berechnen die Spritkosten der Extra-Fahrt zur CZ-Station (zum DE-Preis) und zeigen eine "Netto-Ersparnis" zusätzlich zur bisherigen Brutto-"Ersparnis in CZ". Bei 0 km (Standard) bleibt alles wie bisher – die neue Kachel erscheint erst, wenn eine Distanz eingetragen wird. Der Verbrauch-Standardwert richtet sich nach der oben gewählten Kraftstoffart (Diesel 5,5 l/100km, Benzin 7,5 l/100km) und bleibt beim Wechsel der Kraftstoffart automatisch synchron, außer man hat ihn schon selbst geändert.
- **Preisverlauf: 30-Tage-Spanne.** Unter dem aktuellen Durchschnittspreis zeigt jede Mini-Chart-Spalte jetzt zusätzlich "Spanne X € – Y €" (Minimum/Maximum der sichtbaren Tage) – Einordnung, ob der aktuelle Preis eher am oberen oder unteren Ende der letzten Wochen liegt.

## [2.9.6] - 2026-09-09

### Hinzugefügt
- Google-Maps-Link an der im PLZ-Feld ermittelten nächstgelegenen Tankstelle (Umkreis-Ergebnis in Deutschland) – vorher gab es den Link nur in der Haupttabelle.

### Geändert
- Wechselkurs-Zeile über der Stationsliste zeigt jetzt "1 € = 24,19 Kč *" statt zusätzlich die Quelle auszuschreiben; die Fußnote (*) verweist auf die bereits vorhandene, ausführlichere Quellenangabe im Footer.
- Standard-Literzahl im Tankrechner von 50 auf 40 geändert.

## [2.9.5] - 2026-09-08

### Hinzugefügt
- Kurzer Hinweistext unter der Preisverlauf-Überschrift: "Bezieht sich immer auf die oben ausgewählte Region – beim Wechseln der Region ändert sich auch der Verlauf." Macht die Kopplung an die Region-Auswahl explizit, statt sie implizit vorauszusetzen.

## [2.9.4] - 2026-09-08

### Geändert
- Preisverlauf-Referenzpreis: statt der günstigsten Station pro Tag wird jetzt der **Durchschnittspreis über alle gefundenen Stationen** je Seite und Kraftstoff verwendet (`update_prices.py`: `cheapest()`/`estimate_*()` durch `average_price()`/`average_e5()`/`average_premium()` ersetzt). Grund: die günstigste CZ-Station blieb tagelang exakt gleich (dieselbe Station, unveränderter Preis) – der Chart zeigte dadurch keine erkennbare Bewegung, obwohl sich der Markt insgesamt sehr wohl bewegt. Der Durchschnitt über alle Stationen zeigt einen echten, repräsentativen Trend. Betrifft nur die Verlaufs-/Chart-Berechnung – die Hauptliste zeigt weiterhin jede einzelne Station mit der echten, markierten günstigsten.
- Überschrift entsprechend angepasst: "Preisverlauf (letzte 30 Tage, Durchschnittspreis aller Stationen pro Tag)".

## [2.9.3] - 2026-09-08

### Entfernt
- Erklärsatz unter der Preisverlauf-Überschrift ("Jede Seite mit eigener Skala …") gestrichen – keine Information, die Endnutzer:innen brauchen.
- Die "± X,XXX € ggü. Vortag"-Zeile unter dem Tagespreis je Chart entfernt: mit noch wenig Historie zeigte sie fast immer "+0,000 €" (der günstigste Anbieter ändert seinen Preis selten von einem Tag auf den nächsten), was eher nach kaputter Anzeige aussah als nützliche Information zu liefern.

### Geprüft
- Bestätigt, dass der Preisverlauf für jede Region bereits die günstigste Tankstelle des jeweiligen Tages als Referenzpreis nutzt (`cheapest()` in `scripts/update_prices.py`, seit v2.1.0) – gilt identisch für alle fünf Regionen inkl. der neuen Dresden/Osterzgebirge und Oberlausitz, keine Codeänderung nötig.

## [2.9.2] - 2026-09-08

### Geändert
- Reihenfolge im Region-Dropdown: **Bayern · Oberfranken** steht jetzt an letzter Stelle (Übersichtlichkeit) – die vier sächsischen Regionen bleiben zusammen an der Spitze.

## [2.9.1] - 2026-09-08

### Geändert
- Region- und Kraftstoff-Auswahl sind jetzt native Dropdown-Menüs (`<select>`) statt Button-Reihen – bei fünf Regionen wirkten die Buttons unübersichtlich. Beide Auswahlfelder nutzen dieselbe Optik für ein einheitliches Bild.

## [2.9.0] - 2026-09-08

### Hinzugefügt
- Zwei neue Regionen: **Sachsen · Dresden/Osterzgebirge** (Bad Gottleuba-Berggießhübel/Pirna ↔ Krásný Les, der A17/D8-Autobahn-Grenzübergang Dresden–Prag) und **Sachsen · Oberlausitz** (Zittau/Bautzen ↔ Hrádek nad Nisou). Vor der Recherche kurz per Websuche verifiziert, welche Übergänge in dieser Gegend tatsächlich relevant sind (A17/D8 als Hauptverbindung, Zittau/Hrádek nad Nisou für die Oberlausitz) statt zu raten.
  - CZ-Seite Dresden: weder "Krásný Les" noch "Petrovice" (die Orte direkt am Autobahn-Grenzübergang) haben eine eigene mbenzin.cz-Seite – "Chabarovice" ist eine gültige, nach Entfernung sortierte Nachbarseite, die Chlumec, Ústí nad Labem und Krupka (Erzgebirgs-Grenzort) bereits ohne Filterung sinnvoll abdeckt.
  - CZ-Seite Oberlausitz: Hrádek nad Nisou liegt direkt gegenüber Zittau, mit eigener mbenzin.cz-Seite und echten Stationen 0–200 m von der Grenze entfernt.
  - Bautzen (~41 km von Zittau, genauso außerhalb des 25-km-Suchradius wie Werdau in Vogtland) bekommt nach demselben Muster einen eigenen `plz_extra_anchors`-Suchanker – Stationen fließen nur in die PLZ-Umkreissuche ein, nicht in die Grenzvergleichstabelle.

### Geändert
- Regions- und Kraftstoff-Auswahl stehen jetzt untereinander (statt nebeneinander) und haben jeweils eine eigene Beschriftung ("Region" / "Kraftstoff") – bei jetzt fünf Regionen wäre eine Zeile zu voll geworden.

## [2.8.1] - 2026-09-08

### Geändert
- Kosmetik: Footer-Untertitel im Banner von "Echte Stationen im deutsch-tschechischen Grenzgebiet" zu "Tankstellen im deutsch-tschechischen Grenzgebiet" gekürzt.
- PLZ-Ergebnisfeld: Label-Reihenfolge von "Günstigste Tankstelle in DE im Umkreis deiner PLZ" zu "Günstigste Tankstelle im Umkreis deiner PLZ in Deutschland" geändert (Land ausgeschrieben statt "DE"-Kürzel). Gleiche Umformulierung auch beim Fallback-Label ("... in dieser Region in Deutschland").

## [2.8.0] - 2026-09-08

### Geändert
- Nutzer merkte an: "die günstigste Tankstelle in Werdau und Umgebung ist doch nicht Auerbach?" – berechtigter Einwand, denn der v2.7.1-Fallback zeigte bei Werdau die nächstgelegene Station in unserem Datensatz (25,2 km entfernt), aber immer noch unter dem Label "im Umkreis deiner PLZ" – irreführend bei so einer Distanz. Jetzt gibt es drei klar unterschiedene Zustände: echte Station im Umkreis (grün, mit Distanz), keine Station im Umkreis mit ehrlichem Hinweis "nicht wirklich in der Nähe" (neutral eingefärbt), oder – ohne Koordinaten – "günstigste in der Region" ohne Distanzangabe.
- Umkreis-Radius von 12 auf 5 km verkleinert (Nutzerwunsch) – zeigt jetzt nur noch Stationen, die wirklich in Fußweite/kurzer Fahrt liegen, nicht mehr "irgendwo in der Region".
- Für 08412 Werdau (~42 km vom Vogtland-Suchzentrum Klingenthal entfernt, also außerhalb des normalen 25-km-Suchradius) gibt's jetzt einen eigenen, kleineren Tankerkönig-Suchanker (10 km um Werdau) – bestätigt durch einen Abgleich mit [ich-tanke.de](https://ich-tanke.de/tankstellen/super-e5/umkreis/werdau/), das reale nahegelegene Stationen (JET Werdau, ARAL Werdau, STAR Fraureuth u. a.) zeigte, die in unserem bisherigen Datensatz schlicht fehlten. Diese zusätzlichen Stationen fließen nur in die PLZ-Umkreissuche ein, nicht in die CZ/DE-Grenzvergleichstabelle (dafür bleiben nur die grenznahen Stationen relevant). `scripts/update_prices.py` unterstützt jetzt beliebige zusätzliche `plz_extra_anchors` pro Region für künftige ähnliche Fälle.
- Preisverlauf-Balkendiagramm "filigraner" gemacht (Nutzerwunsch): dünnere Balken mit mehr Zwischenraum, plus eine helle Positionsmarkierung an der Balkenspitze – die das Auge exakter vergleichen kann als die Länge zweier fast gleich hoher Balken. Damit bleiben Tagesunterschiede trotz ehrlicher Nulllinie (siehe v2.7.0) besser erkennbar.

## [2.7.1] - 2026-09-08

### Behoben
- Nutzer meldete falsches Ergebnis: Bei PLZ 08412 (Werdau) zeigte das PLZ-Ergebnisfeld eine Tankstelle in Schönheide als "≈ 7,0 km von deiner PLZ" an – tatsächlich liegen beide Orte weit auseinander. Ursache: der Referenzpunkt für die Umkreissuche (v2.7.0) war die DE-Station, deren *eigene* Postleitzahl der eingegebenen PLZ numerisch am nächsten lag – das ist keine verlässliche Näherung, da deutsche Postleitzahlen nicht nach geografischer Nähe sortiert sind. Werdaus PLZ (08412) hatte zufällig eine Station mit ähnlicher PLZ-Zahl, die real aber weit entfernt liegt.
- Fix: eigene Tabelle mit echten Koordinaten (Wikipedia-Werte) für jeden Ort, der einer PLZ in der App zugeordnet ist – die Umkreissuche nutzt jetzt die tatsächliche Position der eingegebenen PLZ als Referenzpunkt, nicht mehr den Umweg über eine zufällig ähnliche Stations-PLZ. Betrifft alle PLZ, nicht nur Werdau. Für PLZ ohne hinterlegte Koordinaten bleibt der Rückfall auf "günstigste in der Region" bestehen (kein falscher Distanzwert wird mehr angezeigt).

## [2.7.0] - 2026-09-08

### Geändert
- "Günstigste Tankstelle in DE" im PLZ-Ergebnisfeld meint jetzt wirklich die günstigste Station **im Umkreis der eingegebenen PLZ**, nicht mehr einfach die günstigste in der ganzen Region. Umsetzung ohne externe Geocoding-Abfrage: Tankerkönig liefert ohnehin echte Koordinaten (`lat`/`lng`) und die Postleitzahl jeder DE-Station – `scripts/update_prices.py` speichert diese jetzt mit in `data.json`. Die App sucht die eigene DE-Station, deren echte PLZ der eingegebenen am nächsten liegt, nutzt deren reale Koordinaten als Referenzpunkt und wählt per Haversine-Distanz die günstigste Station im 12-km-Umkreis (sonst die nächstgelegene). Zeigt zusätzlich die Entfernung an. Ohne passende Referenzstation (z. B. Fallback-Daten ohne Koordinaten) bleibt das bisherige Verhalten ("günstigste in der Region") als Rückfallebene erhalten.
- Preisverlauf-Chart von Linien- auf Balkendiagramm umgestellt: ein Balken pro Tag, letzte 30 Tage. Balken wachsen jetzt von einer echten Nulllinie (Balkenlänge codiert Betrag – anders als bei einer Linie darf die Achse hier nicht gekappt werden), mit Hover-/Fokus-Tooltip pro Balken statt Fadenkreuz. Kleine Multiples (eigene Skala für CZ/DE) und die Kopfzeile mit aktuellem Wert/Vortags-Delta bleiben wie in v2.3.0.

## [2.6.1] - 2026-09-07

### Behoben
- Nutzerfrage beantwortet: "Tank ONO" in Cheb/Horní Vojtanov (nahe Skalná/Vojtanov) fehlte in der Sachsen · Erzgebirgskreis/Bayern-Oberfranken-Stationsliste. Ursache: mbenzin.cz listet zwei physisch unterschiedliche Tank-ONO-Filialen unter identischem `addressLocality="Cheb"` – unsere Duplikatserkennung verglich bisher nur `(Name, Ort)` und verwarf die zweite Station fälschlich als Duplikat. Fix: Duplikatserkennung nutzt jetzt die eindeutige Detailseiten-URL jeder Station statt `(Name, Ort)`. Zusätzlich wird die `streetAddress` (falls von mbenzin.cz separat angegeben) an den Ortsnamen angehängt, damit gleichnamige Stationen im selben Ort in der App unterscheidbar sind (z. B. "Cheb, Horní Vojtanov 39").
- Da mbenzin.cz seine "nächstgelegene"-Sortierung relativ zum Ortszentrum (hier: Cheb) berechnet, nicht relativ zum tatsächlichen Grenzübergang, landete die Horní-Vojtanov-Filiale weit hinten in der Rohliste und wäre trotz Dedupe-Fix von der Top-10-Begrenzung abgeschnitten worden. Neue, optionale Prioritäts-Stichwörter (`cz_priority_keywords`) heben bekannte grenznahe Treffer vor dem Kürzen nach oben – für Bayern · Oberfranken aktuell "Vojtanov" und "Skalná".

## [2.6.0] - 2026-09-07

### Hinzugefügt
- Nach Bestätigung der PLZ erscheint direkt unter dem PLZ-Feld ein separates Ergebnisfeld mit der aktuell günstigsten DE-Tankstelle für die gewählte Region und den gewählten Kraftstoff (Name, Ort, Preis) – ohne dass man zur vollständigen Stationsliste weiterscrollen muss. Bleibt beim Wechsel des Kraftstoffs automatisch aktuell.

## [2.5.3] - 2026-09-07

### Hinzugefügt
- "Finden"-Button neben dem PLZ-Feld zur Bestätigung per Tap. Grund: die numerische iOS-Tastatur (`inputmode="numeric"`) zeigt keine Eingabetaste/Return an, wodurch sich die Region auf dem iPhone nicht bestätigen ließ. Enter funktioniert weiterhin (Desktop), der Button ist der zusätzliche, immer sichtbare Bestätigungsweg für Touch-Tastaturen ohne Eingabetaste.

## [2.5.2] - 2026-09-07

### Hinzugefügt
- Kurzer Beschreibungstext oberhalb des PLZ-Felds, der den Zweck erklärt ("Nicht sicher, welche der drei Regionen am nächsten liegt? ..."). Der dynamische Hinweistext darunter beschränkt sich jetzt auf die Bedienung (Eingabe + Enter, Google-Maps-Links für die Feinauswahl).

## [2.5.1] - 2026-09-07

### Geändert
- PLZ-Eingabefeld wählt die Region jetzt erst nach Bestätigung mit Enter aus, statt sofort bei der 5. eingegebenen Ziffer. Während der Eingabe zeigt der Hinweistext bereits als Vorschau an, welche Region ausgewählt würde.

## [2.5.0] - 2026-09-07

### Hinzugefügt
- Eigenes PLZ-Eingabefeld oberhalb der Regions-Auswahl: wählt automatisch die naheliegendste Region (Vogtland, Oberfranken oder Erzgebirgskreis). Basiert auf einer festen PLZ→Region-Zuordnung (bekannte Ortschaften der App-Stationsdaten als Übersteuerung, sonst grobe Zahlenbereiche je Landkreis) – keine externe Geocoding-Abfrage, da das Claude-Artifact keinen beliebigen externen Netzwerkzugriff per Fetch erlaubt (nur Skripte von der CDN-Allowlist). Bei nicht zuordenbarer PLZ bleibt die aktuelle Region unverändert und ein Hinweistext bittet um manuelle Auswahl. Für die genau nächstgelegene Station bleiben die Google-Maps-Links pro Station die Feinauswahl.

## [2.4.1] - 2026-09-07

### Geändert
- Reihenfolge der Regions-Auswahl geändert: Sachsen · Erzgebirgskreis steht jetzt vor Sachsen · Vogtland.

## [2.4.0] - 2026-09-07

### Hinzugefügt
- Dritte Region: **Sachsen · Erzgebirgskreis** (Johanngeorgenstadt ↔ Potůčky, Oberwiesenthal ↔ Boží Dar). CZ-Seite über mbenzin.cz (Jáchymov-Seite, nach Umkreis sortiert, gefiltert auf "Boží Dar"/"Potůčky" – keiner der beiden Grenzorte hat eine eigene mbenzin.cz-Ortsseite), DE-Seite über Tankerkönig-Umkreissuche um den Mittelpunkt zwischen Johanngeorgenstadt und Oberwiesenthal (25 km Radius deckt beide Grenzübergänge ab).

## [2.3.0] - 2026-09-07

### Geändert
- Preisverlauf-Chart umgebaut: statt einer Linie für CZ und DE auf einer gemeinsamen Achse jetzt zwei unabhängig skalierte Mini-Charts (Small Multiples). Grund: CZ (~1,65 €) und DE (~2,35 €) liegen preislich so weit auseinander, dass eine gemeinsame Skala die tatsächliche Tagesbewegung innerhalb jeder Linie fast unsichtbar machte. Jede Seite zeigt jetzt zusätzlich den aktuellen Wert sowie die Veränderung gegenüber dem Vortag im Kopf.
- Chart-Optik verfeinert (dünnere Linie, kleinere Endpunkt-Marker, leichtere Beschriftung).

## [2.2.3] - 2026-09-06

### Geändert
- Changelog-Link im Footer entfernt – muss nicht jeder Besucher zum GitHub-Repo geleitet werden; die Versionsnummer allein reicht als Referenz für Rückfragen.

## [2.2.2] - 2026-09-05

### Hinzugefügt
- Footer nennt jetzt das Aktualisierungs-Intervall (3× täglich, 07:00/13:00/19:00 Uhr)

## [2.2.1] - 2026-09-05

### Geändert
- Automatisierung läuft jetzt 3× täglich (07:00, 13:00, 19:00 Europe/Berlin) statt einmal – Stationsliste bleibt tagsüber frischer. Der Preisverlauf-Chart bleibt unverändert bei einem Datenpunkt pro Kalendertag (mehrfache Läufe am selben Tag überschreiben nur den heutigen Eintrag), zeigt dadurch aber den Stand nach der abendlichen Aktualisierung statt nur den frühmorgendlichen.

## [2.2.0] - 2026-09-05

### Geändert
- "Super E10"/"Super E5"-Doppelauswahl zu einer einzigen Option "Natural 95" zusammengefasst. Grund: Tschechien verkauft seit 2024 kein separates E5 mehr, daher zeigten beide Buttons auf der CZ-Seite ohnehin immer denselben Preis – das wirkte eher verwirrend als informativ. Betrifft Kraftstoff-Umschalter und Tankrechner (nutzt denselben State).
- Dazugehörige Fußnoten zu Super E5 entfernt/verschlankt.

## [2.1.2] - 2026-09-05

### Geändert
- Footer: "Tankerkönig API" zu "Tankerkönig" gekürzt
- Veralteten Hinweis "Diese Seite ruft keine Preise automatisch ab..." entfernt – gilt seit v2.1.0 nicht mehr für die GitHub-Pages-Version

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

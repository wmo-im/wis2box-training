---
title: WIS2 in a box Spickzettel
---

# WIS2 in a box Spickzettel

## Übersicht

wis2box wird als eine Reihe von Docker Compose-Befehlen ausgeführt. Der Befehl ``wis2box-ctl.py`` ist ein Hilfsprogramm
(geschrieben in Python), um Docker Compose-Befehle einfach auszuführen.

## Grundlegende wis2box-Befehle

### Starten und Stoppen

* wis2box starten:

```bash
python3 wis2box-ctl.py start
```

* wis2box stoppen:

```bash
python3 wis2box-ctl.py stop
```

* Überprüfen, ob alle wis2box-Container laufen:

```bash
python3 wis2box-ctl.py status
```

* Anmeldung bei einem wis2box-Container (*wis2box-management* standardmäßig):

```bash
python3 wis2box-ctl.py login
```

* Anmeldung bei einem spezifischen wis2box-Container:

```bash
python3 wis2box-ctl.py login wis2box-api
```
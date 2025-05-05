---
title: WIS2 in einer Box Spickzettel
---

# WIS2 in einer Box Spickzettel

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

* In einen wis2box-Container einloggen (*standardmäßig wis2box-management*):

```bash
python3 wis2box-ctl.py login
```

* In einen bestimmten wis2box-Container einloggen:

```bash
python3 wis2box-ctl.py login wis2box-api
```
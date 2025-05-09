---
title: WIS2 in a box cheatsheet
---

# WIS2 in a box cheatsheet

## Panoramica

wis2box funziona come una suite di comandi Docker Compose. Il comando ``wis2box-ctl.py`` è uno strumento
(scritto in Python) per eseguire comandi Docker Compose facilmente.

## Comandi essenziali di wis2box

### Avvio e arresto

* Avvia wis2box:

```bash
python3 wis2box-ctl.py start
```

* Arresta wis2box:

```bash
python3 wis2box-ctl.py stop
```

* Verifica che tutti i container wis2box siano in esecuzione:

```bash
python3 wis2box-ctl.py status
```

* Accedi a un container wis2box (*wis2box-management* di default):

```bash
python3 wis2box-ctl.py login
```

* Accedi a un container wis2box specifico:

```bash
python3 wis2box-ctl.py login wis2box-api
```
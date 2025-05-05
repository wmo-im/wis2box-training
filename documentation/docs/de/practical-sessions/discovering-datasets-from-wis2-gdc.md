---
title: Datensätze aus dem WIS2 Global Discovery Catalogue entdecken
---

# Datensätze aus dem WIS2 Global Discovery Catalogue entdecken

!!! abstract "Lernziele!"

    Nach Abschluss dieser praktischen Übung werden Sie in der Lage sein:

    - pywiscat zu verwenden, um Datensätze aus dem Global Discovery Catalogue (GDC) zu entdecken

## Einführung

In dieser Sitzung lernen Sie, wie Sie Daten aus dem WIS2 Global Discovery Catalogue (GDC) entdecken können.

Derzeit sind folgende GDCs verfügbar:

- Environment and Climate Change Canada, Meteorological Service of Canada: <https://wis2-gdc.weather.gc.ca>
- China Meteorological Administration: <https://gdc.wis.cma.cn>
- Deutscher Wetterdienst: <https://wis2.dwd.de/gdc>

Während lokaler Schulungen wird ein lokaler GDC eingerichtet, damit die Teilnehmer den GDC nach den Metadaten abfragen können, die sie von ihren wis2box-Instanzen veröffentlicht haben. In diesem Fall stellen die Trainer die URL zum lokalen GDC zur Verfügung.

## Vorbereitung

!!! note
    Bitte melden Sie sich vor dem Start an Ihrer Student-VM an.

## Installation von pywiscat

Verwenden Sie den Python-Paketinstaller `pip3`, um pywiscat auf Ihrer VM zu installieren:
```bash
pip3 install pywiscat
```

!!! note

    Wenn Sie folgenden Fehler sehen:

    ```
    WARNING: The script pywiscat is installed in '/home/username/.local/bin' which is not on PATH.
    Consider adding this directory to PATH or, if you prefer to suppress this warning, use --no-warn-script-location.
    ```

    Führen Sie dann den folgenden Befehl aus:

    ```bash
    export PATH=$PATH:/home/$USER/.local/bin
    ```

    ...wobei `$USER` Ihr Benutzername auf Ihrer VM ist.

Überprüfen Sie, ob die Installation erfolgreich war:

```bash
pywiscat --version
```

## Daten mit pywiscat finden

Standardmäßig verbindet sich pywiscat mit dem Global Discovery Catalogue von Kanada. Lassen Sie uns pywiscat so konfigurieren, dass es den Schulungs-GDC abfragt, indem wir die Umgebungsvariable `PYWISCAT_GDC_URL` setzen:

```bash
export PYWISCAT_GDC_URL=http://gdc.wis2.training:5002
```

Verwenden wir [pywiscat](https://github.com/wmo-im/pywiscat), um den im Rahmen der Schulung eingerichteten GDC abzufragen.

```bash
pywiscat search --help
```

Suchen Sie nun im GDC nach allen Datensätzen:

```bash
pywiscat search
```

!!! question

    Wie viele Datensätze werden bei der Suche zurückgegeben?

??? success "Klicken Sie hier für die Antwort"
    Die Anzahl der Datensätze hängt von dem GDC ab, den Sie abfragen. Bei Verwendung des lokalen Schulungs-GDC sollten Sie sehen, dass die Anzahl der Datensätze der Anzahl der Datensätze entspricht, die während der anderen praktischen Sitzungen in den GDC aufgenommen wurden.

Versuchen wir, den GDC mit einem Schlüsselwort abzufragen:

```bash
pywiscat search -q observations
```

!!! question

    Wie lautet die Datenpolitik der Ergebnisse?

??? success "Klicken Sie hier für die Antwort"
    Alle zurückgegebenen Daten sollten als "core" Daten gekennzeichnet sein

Probieren Sie weitere Abfragen mit `-q` aus

!!! tip

    Der `-q` Parameter ermöglicht folgende Syntax:

    - `-q synop`: findet alle Datensätze mit dem Wort "synop"
    - `-q temp`: findet alle Datensätze mit dem Wort "temp"
    - `-q "observations AND oman"`: findet alle Datensätze mit den Wörtern "observations" und "oman"
    - `-q "observations NOT oman"`: findet alle Datensätze, die das Wort "observations", aber nicht das Wort "oman" enthalten
    - `-q "synop OR temp"`: findet alle Datensätze mit entweder "synop" oder "temp"
    - `-q "obs*"`: Unschärfesuche

    Bei der Suche nach Begriffen mit Leerzeichen diese in doppelte Anführungszeichen setzen.

Lassen Sie uns mehr Details zu einem bestimmten Suchergebnis abrufen, das uns interessiert:

```bash
pywiscat get <id>
```

!!! tip

    Verwenden Sie den `id`-Wert aus der vorherigen Suche.

## Fazit

!!! success "Herzlichen Glückwunsch!"

    In dieser praktischen Übung haben Sie gelernt:

    - pywiscat zu verwenden, um Datensätze aus dem WIS2 Global Discovery Catalogue zu entdecken
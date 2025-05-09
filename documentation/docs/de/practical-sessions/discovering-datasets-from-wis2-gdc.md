---
title: Entdecken von Datensätzen aus dem WIS2 Global Discovery Catalogue
---

# Entdecken von Datensätzen aus dem WIS2 Global Discovery Catalogue

!!! abstract "Lernergebnisse!"

    Am Ende dieser praktischen Sitzung werden Sie in der Lage sein:

    - pywiscat zu verwenden, um Datensätze aus dem Global Discovery Catalogue (GDC) zu entdecken

## Einführung

In dieser Sitzung lernen Sie, wie man Daten aus dem WIS2 Global Discovery Catalogue (GDC) entdeckt.

Derzeit sind die folgenden GDCs verfügbar:

- Environment and Climate Change Canada, Meteorological Service of Canada: <https://wis2-gdc.weather.gc.ca>
- China Meteorological Administration: <https://gdc.wis.cma.cn>
- Deutscher Wetterdienst: <https://wis2.dwd.de/gdc>

Während lokaler Schulungssitzungen wird ein lokaler GDC eingerichtet, um den Teilnehmern zu ermöglichen, den GDC nach den von ihren wis2box-Instanzen veröffentlichten Metadaten zu durchsuchen. In diesem Fall werden die Trainer die URL zum lokalen GDC bereitstellen.

## Vorbereitung

!!! note
    Bitte loggen Sie sich vor Beginn in Ihre Studenten-VM ein.

## Installation von pywiscat

Verwenden Sie den Python-Paketinstaller `pip3`, um pywiscat auf Ihrer VM zu installieren:
```bash
pip3 install pywiscat
```

!!! note

    Wenn Sie auf den folgenden Fehler stoßen:

    ```
    WARNING: The script pywiscat is installed in '/home/username/.local/bin' which is not on PATH.
    Consider adding this directory to PATH or, if you prefer to suppress this warning, use --no-warn-script-location.
    ```

    Dann führen Sie den folgenden Befehl aus:

    ```bash
    export PATH=$PATH:/home/$USER/.local/bin
    ```

    ...wobei `$USER` Ihr Benutzername auf Ihrer VM ist.

Überprüfen Sie, ob die Installation erfolgreich war:

```bash
pywiscat --version
```

## Daten finden mit pywiscat

Standardmäßig verbindet sich pywiscat mit dem Global Discovery Catalogue von Kanada. Konfigurieren wir pywiscat, um den Schulungs-GDC abzufragen, indem wir die Umgebungsvariable `PYWISCAT_GDC_URL` setzen:

```bash
export PYWISCAT_GDC_URL=http://gdc.wis2.training:5002
```

Verwenden wir [pywiscat](https://github.com/wmo-im/pywiscat), um den im Rahmen der Schulung eingerichteten GDC abzufragen.

```bash
pywiscat search --help
```

Suchen Sie jetzt im GDC nach allen Datensätzen:

```bash
pywiscat search
```

!!! question

    Wie viele Datensätze werden von der Suche zurückgegeben?

??? success "Klicken Sie, um die Antwort zu enthüllen"
    Die Anzahl der Datensätze hängt von dem GDC ab, den Sie abfragen. Wenn Sie den lokalen Schulungs-GDC verwenden, sollten Sie sehen, dass die Anzahl der Datensätze gleich der Anzahl der Datensätze ist, die während der anderen praktischen Sitzungen in den GDC eingespeist wurden.

Versuchen wir, den GDC mit einem Schlüsselwort abzufragen:

```bash
pywiscat search -q observations
```

!!! question

    Wie lautet die Datenrichtlinie der Ergebnisse?

??? success "Klicken Sie, um die Antwort zu enthüllen"
    Alle zurückgegebenen Daten sollten als "Kerndaten" spezifiziert sein

Versuchen Sie zusätzliche Abfragen mit `-q`

!!! tip

    Der `-q`-Flag ermöglicht die folgende Syntax:

    - `-q synop`: finde alle Datensätze mit dem Wort "synop"
    - `-q temp`: finde alle Datensätze mit dem Wort "temp"
    - `-q "observations AND oman"`: finde alle Datensätze mit den Wörtern "observations" und "oman"
    - `-q "observations NOT oman"`: finde alle Datensätze, die das Wort "observations" enthalten, aber nicht das Wort "oman"
    - `-q "synop OR temp"`: finde alle Datensätze mit "synop" oder "temp"
    - `-q "obs*"`: unscharfe Suche

    Wenn Sie nach Begriffen mit Leerzeichen suchen, setzen Sie diese in Anführungszeichen.

Lassen Sie uns mehr Details zu einem spezifischen Suchergebnis erhalten, das uns interessiert:

```bash
pywiscat get <id>
```

!!! tip

    Verwenden Sie den `id`-Wert aus der vorherigen Suche.


## Schlussfolgerung

!!! success "Herzlichen Glückwunsch!"

    In dieser praktischen Sitzung haben Sie gelernt, wie man:

    - pywiscat verwendet, um Datensätze aus dem WIS2 Global Discovery Catalogue zu entdecken
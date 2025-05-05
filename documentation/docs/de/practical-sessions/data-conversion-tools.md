---
title: Datenwandlungswerkzeuge
---

# Datenwandlungswerkzeuge

!!! abstract "Lernziele"
    Nach Abschluss dieser praktischen Einheit werden Sie in der Lage sein:

    - Auf ecCodes-Kommandozeilenwerkzeuge im wis2box-api Container zuzugreifen
    - Das synop2bufr-Werkzeug zur Umwandlung von FM-12 SYNOP-Berichten in BUFR über die Kommandozeile zu nutzen
    - Die synop2bufr-Umwandlung über die wis2box-webapp auszulösen
    - Das csv2bufr-Werkzeug zur Umwandlung von CSV-Daten in BUFR über die Kommandozeile zu nutzen

## Einführung

Auf WIS2 veröffentlichte Daten sollten die Anforderungen und Standards erfüllen, die von den verschiedenen Expertengemeinschaften der Erdsystemdisziplinen definiert wurden. Um die Hürde für die Datenveröffentlichung von landgestützten Oberflächenbeobachtungen zu senken, bietet wis2box Werkzeuge zur Umwandlung von Daten in das BUFR-Format. Diese Werkzeuge sind über den wis2box-api Container verfügbar und können von der Kommandozeile aus genutzt werden, um den Datenumwandlungsprozess zu testen.

Die hauptsächlich von wis2box unterstützten Umwandlungen sind FM-12 SYNOP-Berichte zu BUFR und CSV-Daten zu BUFR. FM-12-Daten werden unterstützt, da sie in der WMO-Gemeinschaft noch weit verbreitet sind und ausgetauscht werden, während CSV-Daten unterstützt werden, um die Zuordnung von Daten automatischer Wetterstationen zum BUFR-Format zu ermöglichen.

### Über FM-12 SYNOP

Wetterberichte von Landstationen wurden historisch stündlich oder zu den Haupt- (00, 06, 12 und 18 UTC) und Zwischensynopzeiten (03, 09, 15, 21 UTC) gemeldet. Vor der Migration zu BUFR wurden diese Berichte im Klartextformat FM-12 SYNOP kodiert. Obwohl die Migration zu BUFR bis 2012 abgeschlossen sein sollte, wird noch immer eine große Anzahl von Berichten im herkömmlichen FM-12 SYNOP-Format ausgetauscht. Weitere Informationen zum FM-12 SYNOP-Format finden Sie im WMO-Handbuch für Codes, Band I.1 (WMO-Nr. 306, Band I.1).

### Über ecCodes

Die ecCodes-Bibliothek ist eine Sammlung von Software-Bibliotheken und Dienstprogrammen, die für die Dekodierung und Kodierung meteorologischer Daten in den Formaten GRIB und BUFR entwickelt wurden. Sie wird vom Europäischen Zentrum für mittelfristige Wettervorhersage (EZMW) entwickelt, siehe die [ecCodes-Dokumentation](https://confluence.ecmwf.int/display/ECC/ecCodes+documentation) für weitere Informationen.

Die wis2box-Software enthält die ecCodes-Bibliothek im Basis-Image des wis2box-api Containers. Dies ermöglicht Benutzern den Zugriff auf die Kommandozeilenwerkzeuge und Bibliotheken innerhalb des Containers. Die ecCodes-Bibliothek wird innerhalb des wis2box-Stacks verwendet, um BUFR-Nachrichten zu dekodieren und zu kodieren.

### Über csv2bufr und synop2bufr

Zusätzlich zu ecCodes verwendet wis2box die folgenden Python-Module, die mit ecCodes zusammenarbeiten, um Daten in das BUFR-Format umzuwandeln:

- **synop2bufr**: zur Unterstützung des herkömmlichen FM-12 SYNOP-Formats, das traditionell von manuellen Beobachtern verwendet wird. Das synop2bufr-Modul benötigt zusätzliche Stationsmetadaten, um weitere Parameter in der BUFR-Datei zu kodieren. Siehe das [synop2bufr-Repository auf GitHub](https://github.com/World-Meteorological-Organization/synop2bufr)
- **csv2bufr**: zur Ermöglichung der Umwandlung von CSV-Auszügen automatischer Wetterstationen in das BUFR-Format. Das csv2bufr-Modul wird verwendet, um CSV-Daten mithilfe einer Mapping-Vorlage in das BUFR-Format umzuwandeln, die definiert, wie die CSV-Daten dem BUFR-Format zugeordnet werden sollen. Siehe das [csv2bufr-Repository auf GitHub](https://github.com/World-Meteorological-Organization/csv2bufr)

Diese Module können eigenständig oder als Teil des wis2box-Stacks verwendet werden.

## Vorbereitung

!!! warning "Voraussetzungen"

    - Stellen Sie sicher, dass Ihre wis2box konfiguriert und gestartet wurde
    - Stellen Sie sicher, dass Sie einen Datensatz eingerichtet und mindestens eine Station in Ihrer wis2box konfiguriert haben
    - Verbinden Sie sich mit dem MQTT Broker Ihrer wis2box-Instanz über MQTT Explorer
    - Öffnen Sie die wis2box-Webanwendung (`http://YOUR-HOST/wis2box-webapp`) und stellen Sie sicher, dass Sie angemeldet sind
    - Öffnen Sie das Grafana-Dashboard für Ihre Instanz unter `http://YOUR-HOST:3000`

Um die BUFR-Kommandozeilenwerkzeuge zu nutzen, müssen Sie im wis2box-api Container angemeldet sein. Sofern nicht anders angegeben, sollten alle Befehle in diesem Container ausgeführt werden. Sie benötigen auch MQTT Explorer geöffnet und mit Ihrem Broker verbunden.

Verbinden Sie sich zunächst über Ihren SSH-Client mit Ihrer Student-VM und kopieren Sie die Übungsmaterialien in den wis2box-api Container:

```bash
docker cp ~/exercise-materials/data-conversion-exercises wis2box-api:/root
```

Melden Sie sich dann im wis2box-api Container an und wechseln Sie in das Verzeichnis mit den Übungsmaterialien:

```bash
cd ~/wis2box
python3 wis2box-ctl.py login wis2box-api
cd /root/data-conversion-exercises
```

Bestätigen Sie, dass die Werkzeuge verfügbar sind, beginnend mit ecCodes:

```bash
bufr_dump -V
```

Sie sollten folgende Antwort erhalten:

```
ecCodes Version 2.36.0
```

Prüfen Sie als nächstes die synop2bufr-Version:

```bash
synop2bufr --version
```

Sie sollten folgende Antwort erhalten:

```
synop2bufr, version 0.7.0
```

Prüfen Sie dann csv2bufr:

```bash
csv2bufr --version
```

Sie sollten folgende Antwort erhalten:

```
csv2bufr, version 0.8.5
```

## ecCodes-Kommandozeilenwerkzeuge

Die im wis2box-api Container enthaltene ecCodes-Bibliothek stellt mehrere Kommandozeilenwerkzeuge für die Arbeit mit BUFR-Dateien zur Verfügung. 
Die nächsten Übungen zeigen, wie man `bufr_ls` und `bufr_dump` verwendet, um den Inhalt einer BUFR-Datei zu prüfen.

### bufr_ls

In dieser ersten Übung werden Sie den `bufr_ls`-Befehl verwenden, um die Header einer BUFR-Datei zu inspizieren und den Typ des Dateiinhalts zu bestimmen.

Verwenden Sie den folgenden Befehl, um `bufr_ls` auf der Datei `bufr-cli-ex1.bufr4` auszuführen:

```bash
bufr_ls bufr-cli-ex1.bufr4
```

Sie sollten folgende Ausgabe sehen:

```bash
bufr-cli-ex1.bufr4
centre                     masterTablesVersionNumber  localTablesVersionNumber   typicalDate                typicalTime                numberOfSubsets
cnmc                       29                         0                          20231002                   000000                     1
1 of 1 messages in bufr-cli-ex1.bufr4

1 of 1 total messages in 1 file
```

Verschiedene Optionen können an `bufr_ls` übergeben werden, um sowohl das Format als auch die angezeigten Header-Felder zu ändern.

!!! question
     
    Wie würde der Befehl lauten, um die vorherige Ausgabe im JSON-Format anzuzeigen?

    Sie können den Befehl `bufr_ls` mit der `-h` Flag ausführen, um die verfügbaren Optionen zu sehen.

??? success "Klicken Sie hier für die Antwort"
    Sie können das Ausgabeformat mit der `-j` Flag auf JSON ändern, d.h.
    ```bash
    bufr_ls -j bufr-cli-ex1.bufr4
    ```

    Bei der Ausführung sollten Sie folgende Ausgabe erhalten:
    ```
    { "messages" : [
      {
        "centre": "cnmc",
        "masterTablesVersionNumber": 29,
        "localTablesVersionNumber": 0,
        "typicalDate": 20231002,
        "typicalTime": "000000",
        "numberOfSubsets": 1
      }
    ]}
    ```

Die ausgegebenen Werte repräsentieren einige der Header-Schlüssel in der BUFR-Datei.

Für sich allein genommen ist diese Information nicht sehr aussagekräftig, da nur begrenzte Informationen über den Dateiinhalt bereitgestellt werden.

Bei der Untersuchung einer BUFR-Datei möchten wir oft den Datentyp und das typische Datum/die typische Zeit der Daten in der Datei bestimmen. Diese Informationen können mit der `-p` Flag aufgelistet werden, um die anzuzeigenden Header auszuwählen. Mehrere Header können durch Kommas getrennt angegeben werden.

Sie können den folgenden Befehl verwenden, um die Datenkategorie, Unterkategorie, das typische Datum und die Zeit aufzulisten:
    
```bash
bufr_ls -p dataCategory,internationalDataSubCategory,typicalDate,typicalTime -j bufr-cli-ex1.bufr4
```

!!! question

    Führen Sie den vorherigen Befehl aus und interpretieren Sie die Ausgabe mithilfe der [Common Code Table C-13](https://github.com/wmo-im/CCT/blob/master/C13.csv), um die Datenkategorie und Unterkategorie zu bestimmen.

    Welche Art von Daten (Datenkategorie und Unterkategorie) ist in der Datei enthalten? Was sind das typische Datum und die typische Zeit für die Daten?

??? success "Klicken Sie hier für die Antwort"
    
    ```
    { "messages" : [
      {
        "dataCategory": 2,
        "internationalDataSubCategory": 4,
        "typicalDate": 20231002,
        "typicalTime": "000000"
      }
    ]}
    ```

    Daraus sehen wir:

    - Die Datenkategorie ist 2, was auf **"Vertikalsondierungen (außer Satellit)"** hinweist.
    - Die internationale Unterkategorie ist 4, was auf **"Temperatur/Feuchte/Wind-Berichte von festen Landstationen in der Höhe (TEMP)"** hinweist.
    - Das typische Datum und die Zeit sind 2023-10-02 bzw. 00:00:00z.

### bufr_dump

Der `bufr_dump`-Befehl kann verwendet werden, um den Inhalt einer BUFR-Datei einschließlich der Daten selbst aufzulisten und zu untersuchen.

Versuchen Sie, den `bufr_dump`-Befehl auf der zweiten Beispieldatei `bufr-cli-ex2.bufr4` auszuführen:

```{.copy}
bufr_dump bufr-cli-ex2.bufr4
```

Dies ergibt ein JSON, das schwer zu analysieren sein kann. Versuchen Sie, die `-p` Flag zu verwenden, um die Daten im Klartext auszugeben (Schlüssel=Wert-Format):

```{.copy}
bufr_dump -p bufr-cli-ex2.bufr4
```

Sie werden eine große Anzahl von Schlüsseln in der Ausgabe sehen, von denen viele fehlen. Dies ist typisch für reale Daten, da nicht alle eccodes-Schlüssel mit gemeldeten Daten gefüllt sind.

Sie können den `grep`-Befehl verwenden, um die Ausgabe zu filtern und nur die Schlüssel anzuzeigen, die nicht fehlen. Um beispielsweise alle nicht fehlenden Schlüssel anzuzeigen, können Sie den folgenden Befehl verwenden:

```{.copy}
bufr_dump -p bufr-cli-ex2.bufr4 | grep -v MISSING
```

!!! question

    Wie hoch ist der auf Meereshöhe reduzierte Druck in der BUFR-Datei `bufr-cli-ex2.bufr4`?

??? success "Klicken Sie hier für die Antwort"

    Mit dem folgenden Befehl:

    ```bash
    bufr_dump -p bufr-cli-ex2.bufr4 | grep -i 'pressureReducedToMeanSeaLevel'
    ```

    Sollten Sie folgende Ausgabe sehen:

    ```
    pressureReducedToMeanSeaLevel=105590
    ```
    Dies zeigt an, dass der auf Meereshöhe reduzierte Druck 105590 Pa (1055,90 hPa) beträgt.

!!! question

    Wie lautet die WIGOS-Stationskennung der Station, die die Daten in der BUFR-Datei `bufr-cli-ex2.bufr4` gemeldet hat?

??? success "Klicken Sie hier für die Antwort"

    Mit dem folgenden Befehl:

    ```bash
    bufr_dump -p bufr-cli-ex2.bufr4 | grep -i 'wigos'
    ```

    Sollten Sie folgende Ausgabe sehen:

    ```
    wigosIdentifierSeries=0
    wigosIssuerOfIdentifier=20000
    wigosIssueNumber=0
    wigosLocalIdentifierCharacter="99100"
    ```

    Dies zeigt an, dass die WIGOS-Stationskennung `0-20000-0-99100` ist.

## synop2bufr-Umw
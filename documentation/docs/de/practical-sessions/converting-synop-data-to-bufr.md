---
title: Umwandlung von SYNOP-Daten in BUFR
---

# Umwandlung von SYNOP-Daten in BUFR über die Kommandozeile

!!! abstract "Lernergebnisse"
    Am Ende dieser praktischen Sitzung werden Sie in der Lage sein:

    - das Werkzeug synop2bufr zu verwenden, um FM-12 SYNOP-Berichte in BUFR umzuwandeln;
    - einfache Kodierungsfehler in FM-12 SYNOP-Berichten vor der Formatumwandlung zu diagnostizieren und zu beheben;

## Einführung

Oberflächenwetterberichte von Landstationen wurden historisch stündlich oder zu den Haupt-
(00, 06, 12 und 18 UTC) und Zwischenzeiten (03, 09, 15, 21 UTC) synoptischen Stunden gemeldet. Vor der Umstellung
auf BUFR wurden diese Berichte im Klartext FM-12 SYNOP-Codeformat kodiert. Obwohl die Umstellung auf BUFR
bis 2012 abgeschlossen sein sollte, werden immer noch eine große Anzahl von Berichten im alten
FM-12 SYNOP-Format ausgetauscht. Weitere Informationen zum FM-12 SYNOP-Format finden Sie im WMO-Handbuch über Codes,
Band I.1 (WMO-Nr. 306, Band I.1).

[WMO-Handbuch über Codes, Band I.1](https://library.wmo.int/records/item/35713-manual-on-codes-international-codes-volume-i-1)

Um die Umstellung auf BUFR zu unterstützen, wurden einige Werkzeuge entwickelt, um
FM-12 SYNOP-Berichte in BUFR zu kodieren. In dieser Sitzung lernen Sie, wie man diese Werkzeuge verwendet sowie die Beziehung zwischen den Informationen in den FM-12 SYNOP-Berichten und den BUFR-Nachrichten.

## Vorbereitung

!!! warning "Voraussetzungen"

    - Stellen Sie sicher, dass Ihr wis2box konfiguriert und gestartet wurde.
    - Bestätigen Sie den Status, indem Sie die wis2box API (``http://<Ihr-Host-Name>/oapi``) besuchen und überprüfen, ob die API läuft.
    - Lesen Sie die Abschnitte **synop2bufr Primer** und **ecCodes Primer** vor Beginn der Übungen.

## synop2bufr Primer

Nachfolgend finden Sie wesentliche `synop2bufr` Befehle und Konfigurationen:

### transform
Die `transform` Funktion konvertiert eine SYNOP-Nachricht in BUFR:

```bash
synop2bufr data transform --metadata my_file.csv --output-dir ./my_directory --year message_year --month message_month my_SYNOP.txt
```

Beachten Sie, dass, wenn die Optionen für Metadaten, Ausgabeverzeichnis, Jahr und Monat nicht angegeben sind, sie ihre Standardwerte annehmen:

| Option      | Standard |
| ----------- | ----------- |
| --metadata | station_list.csv |
| --output-dir | Das aktuelle Arbeitsverzeichnis. |
| --year | Das aktuelle Jahr. |
| --month | Der aktuelle Monat. |

!!! note
    Man muss vorsichtig mit dem Standardjahr und -monat sein, da der im Bericht angegebene Tag des Monats nicht übereinstimmen könnte (z.B. hat Juni keine 31 Tage).

In den Beispielen sind Jahr und Monat nicht angegeben, also fühlen Sie sich frei, ein Datum selbst anzugeben oder die Standardwerte zu verwenden.

## ecCodes Primer

ecCodes bietet sowohl Kommandozeilenwerkzeuge als auch die Möglichkeit, in Ihre eigenen Anwendungen eingebettet zu werden. Nachfolgend einige nützliche Kommandozeilenwerkzeuge für die Arbeit mit BUFR-Daten.

### bufr_dump

Der Befehl `bufr_dump` ist ein generisches BUFR-Informationswerkzeug. Es hat viele Optionen, aber die folgenden werden für die Übungen am meisten zutreffen:

```bash
bufr_dump -p my_bufr.bufr4
```

Dies zeigt den BUFR-Inhalt auf Ihrem Bildschirm an. Wenn Sie an den Werten interessiert sind, die eine bestimmte Variable annimmt, verwenden Sie den Befehl `egrep`:

```bash
bufr_dump -p my_bufr.bufr4 | egrep -i temperature
```

Dies zeigt Variablen an, die mit der Temperatur in Ihren BUFR-Daten zusammenhängen. Wenn Sie dies für mehrere Arten von Variablen tun möchten, filtern Sie die Ausgabe mit einem Pipe (`|`):

```bash
bufr_dump -p my_bufr.bufr4 | egrep -i 'temperature|wind'
```

## Umwandlung von FM-12 SYNOP in BUFR mit synop2bufr über die Kommandozeile

Die eccodes-Bibliothek und das synop2bufr-Modul sind im wis2box-api-Container installiert. Um die nächsten Übungen durchzuführen, werden wir das Verzeichnis synop2bufr-exercises in den wis2box-api-Container kopieren und die Übungen von dort aus durchführen.

```bash
docker cp ~/exercise-materials/synop2bufr-exercises wis2box-api:/root
```

Nun können wir den Container betreten und die Übungen durchführen:

```bash
docker exec -it wis2box-api /bin/bash
```

### Übung 1
Navigieren Sie zum Verzeichnis `/root/synop2bufr-exercises/ex_1` und inspizieren Sie die SYNOP-Nachrichtendatei message.txt:

```bash
cd /root/synop2bufr-exercises/ex_1
more message.txt
```

!!! question

    Wie viele SYNOP-Berichte sind in dieser Datei?

??? success "Klicken, um die Antwort zu sehen"
    
    Es gibt 1 SYNOP-Bericht, da nur 1 Trennzeichen (=) am Ende der Nachricht vorhanden ist.

Inspizieren Sie die Stationsliste:

```bash
more station_list.csv
```

!!! question

    Wie viele Stationen sind in der Stationsliste aufgeführt?

??? success "Klicken, um die Antwort zu sehen"

    Es gibt 1 Station, die station_list.csv enthält eine Zeile mit Stationsmetadaten.

!!! question
    Versuchen Sie, `message.txt` in das BUFR-Format zu konvertieren.

??? success "Klicken, um die Antwort zu sehen"

    Um die SYNOP-Nachricht in das BUFR-Format zu konvertieren, verwenden Sie den folgenden Befehl:

    ```bash
    synop2bufr data transform --metadata station_list.csv --output-dir ./ --year 2024 --month 09 message.txt
    ```

!!! tip

    Sehen Sie sich den Abschnitt [synop2bufr Primer](#synop2bufr-primer) an.

Inspizieren Sie die resultierenden BUFR-Daten mit `bufr_dump`.

!!! question
     Finden Sie heraus, wie Sie die Werte für Breite und Länge mit denen in der Stationsliste vergleichen können.

??? success "Klicken, um die Antwort zu sehen"

    Um die Werte für Breite und Länge in den BUFR-Daten mit denen in der Stationsliste zu vergleichen, verwenden Sie den folgenden Befehl:

    ```bash
    bufr_dump -p WIGOS_0-20000-0-15015_20240921T120000.bufr4 | egrep -i 'latitude|longitude'
    ```

    Dies zeigt die Werte für Breite und Länge in den BUFR-Daten an.

!!! tip

    Sehen Sie sich den Abschnitt [ecCodes Primer](#eccodes-primer) an.

### Übung 2
Navigieren Sie zum Verzeichnis `exercise-materials/synop2bufr-exercises/ex_2` und inspizieren Sie die SYNOP-Nachrichtendatei message.txt:

```bash
cd /root/synop2bufr-exercises/ex_2
more message.txt
```

!!! question

    Wie viele SYNOP-Berichte sind in dieser Datei?

??? success "Klicken, um die Antwort zu sehen"

    Es gibt 3 SYNOP-Berichte, da es 3 Trennzeichen (=) am Ende der Nachricht gibt.

Inspizieren Sie die Stationsliste:

```bash
more station_list.csv
```

!!! question

    Wie viele Stationen sind in der Stationsliste aufgeführt?

??? success "Klicken, um die Antwort zu sehen"

    Es gibt 3 Stationen, die station_list.csv enthält drei Zeilen mit Stationsmetadaten.

!!! question
    Konvertieren Sie `message.txt` in das BUFR-Format.

??? success "Klicken, um die Antwort zu sehen"

    Um die SYNOP-Nachricht in das BUFR-Format zu konvertieren, verwenden Sie den folgenden Befehl:

    ```bash
    synop2bufr data transform --metadata station_list.csv --output-dir ./ --year 2024 --month 09 message.txt
    ```

!!! question

    Basierend auf den Ergebnissen der Übungen in dieser und der vorherigen Übung, wie würden Sie die Anzahl der
    resultierenden BUFR-Dateien vorhersagen, basierend auf der Anzahl der SYNOP-Berichte und der in der Stationsmetadatendatei aufgeführten Stationen?

??? success "Klicken, um die Antwort zu sehen"

    Um die produzierten BUFR-Dateien zu sehen, führen Sie den folgenden Befehl aus:

    ```bash
    ls -l *.bufr4
    ```

    Die Anzahl der produzierten BUFR-Dateien entspricht der Anzahl der SYNOP-Berichte in der Nachrichtendatei.

Inspizieren Sie die resultierenden BUFR-Daten mit `bufr_dump`.

!!! question
    Wie können Sie die WIGOS-Station-ID, die in den BUFR-Daten jeder produzierten Datei kodiert ist, überprüfen?

??? success "Klicken, um die Antwort zu sehen"

    Dies kann mit den folgenden Befehlen erfolgen:

    ```bash
    bufr_dump -p WIGOS_0-20000-0-15015_20240921T120000.bufr4 | egrep -i 'wigos'
    ```

    ```bash
    bufr_dump -p WIGOS_0-20000-0-15020_20240921T120000.bufr4 | egrep -i 'wigos'
    ```

    ```bash
    bufr_dump -p WIGOS_0-20000-0-15090_20240921T120000.bufr4 | egrep -i 'wigos'
    ```

    Beachten Sie, dass wenn Sie ein Verzeichnis mit nur diesen 3 BUFR-Dateien haben, Sie Linux-Wildcards wie folgt verwenden können:

    ```bash
    bufr_dump -p *.bufr4 | egrep -i 'wigos'
    ```

### Übung 3
Navigieren Sie zum Verzeichnis `exercise-materials/synop2bufr-exercises/ex_3` und inspizieren Sie die SYNOP-Nachrichtendatei message.txt:

```bash
cd /root/synop2bufr-exercises/ex_3
more message.txt
```

Diese SYNOP-Nachricht enthält nur einen längeren Bericht mit mehreren Abschnitten.

Inspizieren Sie die Stationsliste:

```bash
more station_list.csv
```

!!! question

    Ist es problematisch, dass diese Datei mehr Stationen enthält, als es Berichte in der SYNOP-Nachricht gibt?

??? success "Klicken, um die Antwort zu sehen"

    Nein, das ist kein Problem, solange es eine Zeile in der Stationslistendatei gibt, die zu der Station TSI passt, die wir zu konvertieren versuchen.

!!! note

    Die Stationslistendatei ist eine Quelle für Metadaten für `synop2bufr`, um die Informationen bereitzustellen, die im alphanumerischen SYNOP-Bericht fehlen und im BUFR SYNOP erforderlich sind.

!!! question
    Konvertieren Sie `message.txt` in das BUFR-Format.

??? success "Klicken, um die Antwort zu sehen"

    Dies erfolgt mit dem `transform` Befehl, zum Beispiel:

    ```bash
    synop2bufr data transform --metadata station_list.csv --output-dir ./ --year 2024 --month 09 message.txt
    ```

Inspizieren Sie die resultierenden BUFR-Daten mit `bufr_dump`.

!!! question

    Finden Sie die folgenden Variablen:

    - Lufttemperatur (K) des Berichts
    - Gesamtwolkenbedeckung (%) des Berichts
    - Gesamte Sonnenscheindauer (Minuten) des Berichts
    - Windgeschwindigkeit (m/s) des Berichts

??? success "Klicken, um die Antwort zu sehen"

    Um die Variablen nach Stichwort in den BUFR-Daten zu finden, können Sie die folgenden Befehle verwenden:

    ```bash
    bufr_dump -p WIGOS_0-20000-0-15260_20240921T115500.bufr4 | egrep -i 'temperature'
    ```

    Sie können den folgenden Befehl verwenden, um nach mehreren Stichwörtern zu suchen:

    ```bash
    bufr_dump -p WIGOS_0-20000-0-15260_20240921T115500.bufr4 | egrep -i 'temperature|cover|sunshine|wind'
    ```

!!! tip

    Der letzte Befehl im Abschnitt [ecCodes Primer](#eccodes-primer) könnte nützlich sein.


### Übung 4
Navigieren Sie zum Verzeichnis `exercise-materials/synop2bufr-exercises/ex_4` und inspizieren Sie die SYNOP-Nachrichtendatei message.txt:

```bash
cd /root/synop2bufr-exercises/ex_4
more message_incorrect.txt
```

!!! question

    Was ist falsch an dieser SYNOP-Datei?

??? success "Klicken, um die Antwort zu sehen"

    Der SYNOP-Bericht für 15015 fehlt das Trennzeichen (`=`), das es `synop2bufr` ermöglicht, diesen Bericht vom nächsten zu unterscheiden.

Versuchen Sie, `message_incorrect.txt` mit `station_list.csv` zu konvertieren

!!! question

    Welche Probleme sind Ihnen bei dieser Konvertierung begegnet?

??? success "Klicken, um die Antwort zu sehen"

    Um die SYNOP-Nachricht in das BUFR-Format zu konvertieren, verwenden Sie den folgenden Befehl:

    ```bash
    synop2bufr data transform --metadata station_list.csv --output-dir ./ --year 2024 --month 09 message_incorrect.txt
    ```

    Der Versuch der Konvertierung sollte die folgenden Fehler auslösen:
    
    - `[ERROR] Unable to decode the SYNOP message`
    - `[ERROR] Error parsing SYNOP report: AAXX 21121 15015 02999 02501 10103 21090 39765 42952 57020 60001 15020 02997 23104 10130 21075 30177 40377 58020 60001 81041. 10130 is not a valid group!`

### Übung 5
Navigieren Sie zum Verzeichnis `exercise-materials/synop2bufr-exercises/ex_5` und inspizieren Sie die SYNOP-Nachrichtendatei message.txt:

```bash
cd /root/synop2bufr-exercises/ex_5
more message.txt
```

Versuchen Sie, `message.txt` in das BUFR-Format zu konvertieren, indem Sie `station_list_incorrect.csv` verwenden

!!! question

    Welche Probleme sind Ihnen bei dieser Konvertierung begegnet?  
    Angesichts des vorgelegten Fehlers, rechtfertigen Sie die Anzahl der produzierten BUFR-Dateien.

??? success "Klicken, um die Antwort zu sehen"

    Um die SYNOP-Nachricht in das BUFR-Format zu konvertieren, verwenden Sie den folgenden Befehl:

    ```bash
    synop2bufr data transform --metadata station_list_incorrect.csv --output-dir ./ --year 2024 --month 09 message.txt
    ```

    Einer der Stations-TSIs (`15015`) hat keine entsprechenden Metadaten in der Stationsliste, was synop2bufr daran hindert, zusätzliche notwendige Metadaten zu erhalten, um den ersten SYNOP-Bericht in BUFR zu konvertieren.

    Sie werden folgende Warnung sehen:

    - `[WARNING] Station 15015 not found in station file`

    Sie können die Anzahl der produzierten BUFR-Dateien sehen, indem Sie den folgenden Befehl ausführen:

    ```bash
    ls -l *.bufr4
    ```

    Es gibt 3 SYNOP-Berichte in message.txt, aber nur 2 BUFR-Dateien wurden produziert. Dies liegt daran, dass einem der SYNOP-Berichte die notwendigen Metadaten fehlten, wie oben erwähnt.

## Schlussfolgerung

!!! success "Herzlichen Glückwunsch!"

    In dieser praktischen Sitzung haben Sie gelernt:

    - wie das Werkzeug synop2bufr verwendet werden kann, um FM-12 SYNOP-Berichte in BUFR umzuwandeln;
    - wie man einfache Kodierungsfehler in FM-12 SYNOP-Berichten vor der Formatumwandlung diagnostiziert und behebt;
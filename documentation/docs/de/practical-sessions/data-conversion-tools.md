---
title: Datenkonvertierungswerkzeuge
---

# Datenkonvertierungswerkzeuge

!!! abstract "Lernergebnisse"
    Am Ende dieser praktischen Sitzung werden Sie in der Lage sein:

    - Zugriff auf ecCodes-Befehlszeilenwerkzeuge im `wis2box-api` Container
    - Verwendung des `synop2bufr`-Tools zur Konvertierung von FM-12 SYNOP-Berichten in BUFR über die Befehlszeile
    - Auslösen der `synop2bufr`-Konvertierung über die `wis2box-webapp`
    - Verwendung des `csv2bufr`-Tools zur Konvertierung von CSV-Daten in BUFR über die Befehlszeile

## Einführung

Daten, die auf WIS2 veröffentlicht werden, sollten die Anforderungen und Standards erfüllen, die von den verschiedenen Fachgemeinschaften der Erdsystemdisziplinen definiert sind. Um die Hürde für die Datenpublikation für bodengebundene Oberflächenbeobachtungen zu senken, bietet `wis2box` Werkzeuge zur Datenkonvertierung ins BUFR-Format an. Diese Werkzeuge sind über den `wis2box-api` Container verfügbar und können von der Befehlszeile aus genutzt werden, um den Datenkonvertierungsprozess zu testen.

Die Hauptkonvertierungen, die derzeit von `wis2box` unterstützt werden, sind FM-12 SYNOP-Berichte in BUFR und CSV-Daten in BUFR. FM-12-Daten werden unterstützt, da sie in der WMO-Gemeinschaft immer noch weit verbreitet und ausgetauscht werden, während CSV-Daten unterstützt werden, um die Zuordnung von Daten, die von automatischen Wetterstationen produziert werden, zum BUFR-Format zu ermöglichen.

### Über FM-12 SYNOP

Oberflächenwetterberichte von bodengebundenen Stationen wurden historisch stündlich oder zu den Haupt- (00, 06, 12 und 18 UTC) und Zwischenzeiten (03, 09, 15, 21 UTC) synoptisch gemeldet. Vor der Umstellung auf BUFR wurden diese Berichte im Klartext-FM-12-SYNOP-Codeformat codiert. Obwohl die Umstellung auf BUFR bis 2012 abgeschlossen sein sollte, wird eine große Anzahl von Berichten immer noch im alten FM-12-SYNOP-Format ausgetauscht. Weitere Informationen zum FM-12-SYNOP-Format finden Sie im WMO-Handbuch über Codes, Band I.1 (WMO-Nr. 306, Band I.1).

### Über ecCodes

Die ecCodes-Bibliothek ist eine Sammlung von Softwarebibliotheken und Dienstprogrammen, die entwickelt wurden, um meteorologische Daten in den GRIB- und BUFR-Formaten zu dekodieren und zu kodieren. Sie wird vom Europäischen Zentrum für mittelfristige Wettervorhersagen (ECMWF) entwickelt, siehe die [ecCodes-Dokumentation](https://confluence.ecmwf.int/display/ECC/ecCodes+documentation) für weitere Informationen.

Die `wis2box`-Software beinhaltet die ecCodes-Bibliothek im Basisimage des `wis2box-api` Containers. Dies ermöglicht den Benutzern den Zugriff auf die Befehlszeilenwerkzeuge und Bibliotheken innerhalb des Containers. Die ecCodes-Bibliothek wird innerhalb des `wis2box`-Stacks verwendet, um BUFR-Nachrichten zu dekodieren und zu kodieren.

### Über csv2bufr und synop2bufr

Zusätzlich zu ecCodes verwendet `wis2box` die folgenden Python-Module, die mit ecCodes arbeiten, um Daten in das BUFR-Format zu konvertieren:

- **synop2bufr**: zur Unterstützung des traditionellen FM-12-SYNOP-Formats, das üblicherweise von manuellen Beobachtern verwendet wird. Das `synop2bufr`-Modul stützt sich auf zusätzliche Stationsmetadaten, um zusätzliche Parameter in der BUFR-Datei zu kodieren. Siehe das [synop2bufr-Repository auf GitHub](https://github.com/World-Meteorological-Organization/synop2bufr)
- **csv2bufr**: zur Ermöglichung der Konvertierung von CSV-Extrakten, die von automatischen Wetterstationen produziert werden, in das BUFR-Format. Das `csv2bufr`-Modul wird verwendet, um CSV-Daten in das BUFR-Format zu konvertieren, indem eine Zuordnungsvorlage verwendet wird, die definiert, wie die CSV-Daten dem BUFR-Format zugeordnet werden sollen. Siehe das [csv2bufr-Repository auf GitHub](https://github.com/World-Meteorological-Organization/csv2bufr)

Diese Module können eigenständig oder als Teil des `wis2box`-Stacks verwendet werden.

## Vorbereitung

!!! warning "Voraussetzungen"

    - Stellen Sie sicher, dass Ihr `wis2box` konfiguriert und gestartet wurde
    - Stellen Sie sicher, dass Sie einen Datensatz eingerichtet und mindestens eine Station in Ihrem `wis2box` konfiguriert haben
    - Verbinden Sie sich mit dem MQTT-Broker Ihrer `wis2box`-Instanz mit `MQTT Explorer`
    - Öffnen Sie die `wis2box` Webanwendung (`http://YOUR-HOST/wis2box-webapp`) und stellen Sie sicher, dass Sie angemeldet sind
    - Öffnen Sie das Grafana-Dashboard für Ihre Instanz, indem Sie zu `http://YOUR-HOST:3000` gehen

Um die BUFR-Befehlszeilenwerkzeuge zu verwenden, müssen Sie im `wis2box-api` Container angemeldet sein. Sofern nicht anders angegeben, sollten alle Befehle in diesem Container ausgeführt werden. Sie müssen auch `MQTT Explorer` geöffnet haben und mit Ihrem Broker verbunden sein.

Verbinden Sie sich zunächst über Ihren SSH-Client mit Ihrem Studenten-VM und kopieren Sie die Übungsmaterialien in den `wis2box-api` Container:

```bash
docker cp ~/exercise-materials/data-conversion-exercises wis2box-api:/root
```

Melden Sie sich dann im `wis2box-api` Container an und wechseln Sie in das Verzeichnis, in dem sich die Übungsmaterialien befinden:

```bash
cd ~/wis2box
python3 wis2box-ctl.py login wis2box-api
cd /root/data-conversion-exercises
```

Bestätigen Sie, dass die Werkzeuge verfügbar sind, beginnend mit ecCodes:

```bash
bufr_dump -V
```

Sie sollten die folgende Antwort erhalten:

```
ecCodes Version 2.36.0
```

Überprüfen Sie als Nächstes die `synop2bufr`-Version:

```bash
synop2bufr --version
```

Sie sollten die folgende Antwort erhalten:

```
synop2bufr, Version 0.7.0
```

Überprüfen Sie als Nächstes `csv2bufr`:

```bash
csv2bufr --version
```

Sie sollten die folgende Antwort erhalten:

```
csv2bufr, Version 0.8.5
```

## ecCodes-Befehlszeilenwerkzeuge

Die in den `wis2box-api` Container integrierte ecCodes-Bibliothek bietet eine Reihe von Befehlszeilenwerkzeugen für die Arbeit mit BUFR-Dateien.
Die nächsten Übungen zeigen, wie Sie `bufr_ls` und `bufr_dump` verwenden, um den Inhalt einer BUFR-Datei zu überprüfen.

### bufr_ls

In dieser ersten Übung verwenden Sie den Befehl `bufr_ls`, um die Header einer BUFR-Datei zu inspizieren und den Typ des Inhalts der Datei zu bestimmen.

Verwenden Sie den folgenden Befehl, um `bufr_ls` auf die Datei `bufr-cli-ex1.bufr4` auszuführen:

```bash
bufr_ls bufr-cli-ex1.bufr4
```

Sie sollten die folgende Ausgabe sehen:

```bash
bufr-cli-ex1.bufr4
centre                     masterTablesVersionNumber  localTablesVersionNumber   typicalDate                typicalTime                numberOfSubsets
cnmc                       29                         0                          20231002                   000000                     1
1 of 1 messages in bufr-cli-ex1.bufr4

1 of 1 total messages in 1 file
```

Verschiedene Optionen können an `bufr_ls` übergeben werden, um sowohl das Format als auch die gedruckten Headerfelder zu ändern.

!!! question

    Wie lautet der Befehl, um die vorherige Ausgabe im JSON-Format aufzulisten?

    Sie können den Befehl `bufr_ls` mit der `-h`-Flagge ausführen, um die verfügbaren Optionen zu sehen.

??? success "Klicken Sie, um die Antwort zu enthüllen"
    Sie können das Ausgabeformat in JSON ändern, indem Sie die `-j`-Flagge verwenden, d.h.
    ```bash
    bufr_ls -j bufr-cli-ex1.bufr4
    ```

    Bei Ausführung sollte dies die folgende Ausgabe geben:
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

Die ausgegebene Information repräsentiert die Werte einiger der Header-Schlüssel in der BUFR-Datei.

Für sich genommen sind diese Informationen nicht sehr aussagekräftig, da nur begrenzte Informationen über den Dateiinhalt bereitgestellt werden.

Bei der Untersuchung einer BUFR-Datei möchten wir oft den Datentyp in der Datei und das typische Datum/die typische Uhrzeit der Daten in der Datei bestimmen. Diese Informationen können aufgelistet werden, indem die `-p`-Flagge verwendet wird, um die auszugebenden Header auszuwählen. Mehrere Header können mit einer durch Kommas getrennten Liste eingeschlossen werden.

Sie können den folgenden Befehl verwenden, um die Datenkategorie, Unterkategorie, das typische Datum und die Zeit aufzulisten:

```bash
bufr_ls -p dataCategory,internationalDataSubCategory,typicalDate,typicalTime -j bufr-cli-ex1.bufr4
```

!!! question

    Führen Sie den vorherigen Befehl aus und interpretieren Sie die Ausgabe unter Verwendung der [Common Code Table C-13](https://github.com/wmo-im/CCT/blob/master/C13.csv), um die Datenkategorie und Unterkategorie zu bestimmen.

    Welcher Datentyp (Datenkategorie und Unterkategorie) ist in der Datei enthalten? Was ist das typische Datum und die typische Uhrzeit für die Daten?

??? success "Klicken Sie, um die Antwort zu enthüllen"

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

    Daraus sehen wir, dass:

    - Die Datenkategorie 2 ist, was **"Vertikale Sondierungen (außer Satellit)"** Daten anzeigt.
    - Die internationale Unterkategorie ist 4, was **"Obere Temperatur-/Feuchtigkeits-/Windberichte von festen Landstationen (TEMP)"** Daten anzeigt.
    - Das typische Datum und die typische Uhrzeit sind 2023-10-02 bzw. 00:00:00z.

### bufr_dump

Der Befehl `bufr_dump` kann verwendet werden, um den Inhalt einer BUFR-Datei aufzulisten und zu untersuchen, einschließlich der Daten selbst.

Versuchen Sie, den Befehl `bufr_dump` auf die zweite Beispieldatei `bufr-cli-ex2.bufr4` auszuführen:

```{.copy}
bufr_dump bufr-cli-ex2.bufr4
```

Dies ergibt ein JSON, das schwer zu parsen ist, versuchen Sie, die `-p`-Flagge zu verwenden, um die Daten im Klartextformat (Schlüssel=Wert-Format) auszugeben:

```{.copy}
bufr_dump -p bufr-cli-ex2.bufr4
```

Sie sollten eine große Anzahl von Schlüsseln als Ausgabe sehen, von denen viele fehlen. Dies ist typisch für reale Daten, da nicht alle eccodes-Schlüssel mit gemeldeten Daten gefüllt sind.

Sie können den Befehl `grep` verwenden, um die Ausgabe zu filtern und nur die Schlüssel anzuzeigen, die nicht fehlen. Zum Beispiel, um alle Schlüssel anzuzeigen, die nicht fehlen, können Sie den folgenden Befehl verwenden:

```{.copy}
bufr_dump -p bufr-cli-ex2.bufr4 | grep -v MISSING
```

!!! question

    Was ist der auf den Meeresspiegel reduzierte Druck, der in der BUFR-Datei `bufr-cli-ex2.bufr4` gemeldet wird?

??? success "Klicken Sie, um die Antwort zu enthüllen"

    Mit dem folgenden Befehl:

    ```bash
    bufr_dump -p bufr-cli-ex2.bufr4 | grep -i 'pressureReducedToMeanSeaLevel'
    ```

    Sollten Sie die folgende Ausgabe sehen:

    ```
    pressureReducedToMeanSeaLevel=105590
    ```
    Dies zeigt an, dass der auf den Meeresspiegel reduzierte Druck 105590 Pa (1055.90 hPa) beträgt.

!!! question

    Was ist die WIGOS-Station-Kennung der Station, die die Daten in der BUFR-Datei `bufr-cli-ex2.bufr4` gemeldet hat?

??? success "Klicken Sie, um die Antwort zu enthüllen"

    Mit dem folgenden Befehl:

    ```bash
    bufr_dump -p bufr-cli-ex2.bufr4 | grep -i 'wigos'
    ```

    Sollten Sie die folgende Ausgabe sehen:

    ```
    wigosIdentifierSeries=0
    wigosIssuerOfIdentifier=20000
    wigosIssueNumber=0
    wigosLocalIdentifierCharacter="99100"
    ```

    Dies zeigt an, dass die WIGOS-Station-Kennung `0-20000-0-99100` ist.

## synop2bufr-Konvertierung

Als Nächstes sehen wir uns an, wie FM-12 SYNOP-Daten mit dem `synop2bufr`-Modul in das BUFR-Format konvertiert werden. Das `synop2bufr`-Modul wird verwendet, um FM-12 SYNOP-Daten in das BUFR-Format zu konvertieren. Das Modul ist im `wis2box-api` Container installiert und kann von der Befehlszeile wie folgt verwendet werden:

```{.copy}
synop2bufr data transform \
    --metadata <station-metadata.csv> \
    --output-dir <output-directory-path> \
    --year <year-of-observation> \
    --month <month-of-observation> \
    <input-fm12.txt>
```

Das Argument `--metadata` wird verwendet, um die Stationsmetadatendatei anzugeben, die zusätzliche Informationen bereitstellt, die in der BUFR-Datei kodiert werden sollen.
Das Argument `--output-dir` wird verwendet, um das Verzeichnis anzugeben, in dem die konvertierten BUFR-Dateien geschrieben werden. Die Argumente `--year` und `--month` werden verwendet, um das Jahr und den Monat der Beobachtung anzugeben.

Das `synop2bufr`-Modul wird auch in der `wis2box-webapp` verwendet, um FM-12 SYNOP-Daten in das BUFR-Format zu konvertieren, indem ein webbasiertes Eingabeformular verwendet wird.

Die nächsten Übungen demonstrieren, wie das `synop2bufr`-Modul funktioniert und wie es verwendet wird, um FM-12 SYNOP-Daten in das BUFR-Format zu konvertieren.

### Überprüfen Sie die Beispiel-SYNOP-Nachricht

Überprüfen Sie die Beispiel-SYNOP-Nachrichtendatei für diese Übung `synop_message.txt`:

```bash
cd /root/data-conversion-exercises
more synop_message.txt
```

!!! question

    Wie viele SYNOP-Berichte sind in dieser Datei?

??? success "Klicken Sie, um die Antwort zu enthüllen"

    Die Ausgabe zeigt Folgendes:

    ```{.copy}
    AAXX 21121
    15015 02999 02501 10103 21090 39765 42952 57020 60001=
    15020 02997 23104 10130 21075 30177 40377 58020 60001 81041=
    15090 02997 53102 10139 21075 30271 40364 58031 60001 82046=
    ```

    Es gibt 3 SYNOP-Berichte in der Datei, die 3 verschiedenen Stationen entsprechen (identifiziert durch die 5-stelligen traditionellen Stationskennungen: 15015, 15020 und 15090).
    Beachten Sie, dass das Ende jedes

Das `--metadata` Argument erfordert eine CSV-Datei, die ein vordefiniertes Format verwendet. Ein funktionierendes Beispiel wird in der Datei `station_list.csv` bereitgestellt:

Verwenden Sie den folgenden Befehl, um den Inhalt der Datei `station_list.csv` zu überprüfen:

```bash
more station_list.csv
```

!!! question

    Wie viele Stationen sind in der Stationsliste aufgeführt? Was sind die WIGOS-Stationen-Identifikatoren der Stationen?

??? success "Klicken, um die Antwort zu enthüllen"

    Die Ausgabe zeigt Folgendes:

    ```{.copy}
    station_name,wigos_station_identifier,traditional_station_identifier,facility_type,latitude,longitude,elevation,barometer_height,territory_name,wmo_region
    OCNA SUGATAG,0-20000-0-15015,15015,landFixed,47.7770616258,23.9404602638,503.0,504.0,ROU,europe
    BOTOSANI,0-20000-0-15020,15020,landFixed,47.7356532437,26.6455501701,161.0,162.1,ROU,europe
    ```

    Dies entspricht den Stationsmetadaten für 2 Stationen: für die WIGOS-Stationen-Identifikatoren `0-20000-0-15015` und `0-20000-0-15020`.

### SYNOP in BUFR konvertieren

Verwenden Sie anschließend den folgenden Befehl, um die FM-12 SYNOP-Nachricht in das BUFR-Format zu konvertieren:

```bash
synop2bufr data transform --metadata station_list.csv --output-dir ./ --year 2024 --month 09 synop_message.txt
```

!!! question
    Wie viele BUFR-Dateien wurden erstellt? Was bedeutet die WARNUNG in der Ausgabe?

??? success "Klicken, um die Antwort zu enthüllen"
    Die Ausgabe zeigt Folgendes:

    ```{.copy}
    [WARNING] Station 15090 not found in station file
    ```

    Wenn Sie den Inhalt Ihres Verzeichnisses mit dem Befehl `ls -lh` überprüfen, sollten Sie sehen, dass 2 neue BUFR-Dateien erstellt wurden: `WIGOS_0-20000-0-15015_20240921T120000.bufr4` und `WIGOS_0-20000-0-15020_20240921T120000.bufr4`.

    Die Warnmeldung zeigt an, dass die Station mit dem traditionellen Stationsidentifikator `15090` nicht in der Datei `station_list.csv` gefunden wurde. Dies bedeutet, dass der SYNOP-Bericht für diese Station nicht in das BUFR-Format konvertiert wurde.

!!! question
    Überprüfen Sie den Inhalt der BUFR-Datei `WIGOS_0-20000-0-15015_20240921T120000.bufr4` mit dem Befehl `bufr_dump`.

    Können Sie bestätigen, dass die Informationen aus der Datei `station_list.csv` im BUFR-File vorhanden sind?

??? success "Klicken, um die Antwort zu enthüllen"
    Sie können den folgenden Befehl verwenden, um den Inhalt der BUFR-Datei zu überprüfen:

    ```bash
    bufr_dump -p WIGOS_0-20000-0-15015_20240921T120000.bufr4 | grep -v MISSING
    ```

    Sie werden folgende Ausgabe feststellen:

    ```{.copy}
    wigosIdentifierSeries=0
    wigosIssuerOfIdentifier=20000
    wigosIssueNumber=0
    wigosLocalIdentifierCharacter="15015"
    blockNumber=15
    stationNumber=15
    stationOrSiteName="OCNA SUGATAG"
    stationType=1
    year=2024
    month=9
    day=21
    hour=12
    minute=0
    latitude=47.7771
    longitude=23.9405
    heightOfStationGroundAboveMeanSeaLevel=503
    heightOfBarometerAboveMeanSeaLevel=504
    ```

    Beachten Sie, dass dies die Daten enthält, die von der Datei `station_list.csv` bereitgestellt wurden.

### SYNOP-Formular in wis2box-webapp

Das Modul `synop2bufr` wird auch in der wis2box-webapp verwendet, um FM-12 SYNOP-Daten in das BUFR-Format zu konvertieren, indem ein webbasiertes Eingabeformular verwendet wird.
Um dies zu testen, gehen Sie zu `http://YOUR-HOST/wis2box-webapp` und melden Sie sich an.

Wählen Sie das `SYNOP Formular` aus dem Menü auf der linken Seite und kopieren Sie den Inhalt der Datei `synop_message.txt`:

```{.copy}
AAXX 21121
15015 02999 02501 10103 21090 39765 42952 57020 60001=
15020 02997 23104 10130 21075 30177 40377 58020 60001 81041=
15090 02997 53102 10139 21075 30271 40364 58031 60001 82046=
```

In das `SYNOP-Nachricht` Textfeld:

<img alt="synop-form" src="/../assets/img/wis2box-webapp-synop-form.png" width="800">

!!! question
    Können Sie das Formular absenden? Was ist das Ergebnis?

??? success "Klicken, um die Antwort zu enthüllen"

    Sie müssen ein Dataset auswählen und den Token für "processes/wis2box" angeben, den Sie in der vorherigen Übung erstellt haben, um das Formular abzusenden.

    Wenn Sie einen ungültigen Token angeben, sehen Sie:

    - Ergebnis: Nicht autorisiert, bitte geben Sie einen gültigen 'processes/wis2box' Token an

    Wenn Sie einen gültigen Token angeben, sehen Sie "WARNUNGEN: 3". Klicken Sie auf die "WARNUNGEN", um das Dropdown zu öffnen, das zeigt:

    - Station 15015 nicht in der Stationsdatei gefunden
    - Station 15020 nicht in der Stationsdatei gefunden
    - Station 15090 nicht in der Stationsdatei gefunden

    Um diese Daten in das BUFR-Format zu konvertieren, müssten Sie die entsprechenden Stationen in Ihrer wis2box konfigurieren und sicherstellen, dass die Stationen dem Thema für Ihr Dataset zugeordnet sind.

!!! note

    In der Übung für [ingesting-data-for-publication](./ingesting-data-for-publication.md) haben Sie die Datei "synop_202412030900.txt" eingespeist und sie wurde vom synop2bufr-Modul in das BUFR-Format konvertiert.

    Im automatisierten Workflow in der wis2box werden das Jahr und der Monat automatisch aus dem Dateinamen extrahiert und verwendet, um die Argumente `--year` und `--month` zu füllen, die von synop2bufr benötigt werden, während die Stationsmetadaten automatisch aus der Stationskonfiguration in der wis2box extrahiert werden.

## csv2bufr-Konvertierung

!!! note
    Stellen Sie sicher, dass Sie immer noch im wis2box-api-Container eingeloggt sind und sich im Verzeichnis `/root/data-conversion-exercises` befinden. Wenn Sie den Container in der vorherigen Übung verlassen haben, können Sie sich wie folgt erneut anmelden:

    ```bash
    cd ~/wis2box
    python3 wis2box-ctl.py login wis2box-api
    cd /root/data-conversion-exercises
    ```

Jetzt schauen wir uns an, wie CSV-Daten in das BUFR-Format konvertiert werden, indem wir das Modul `csv2bufr` verwenden. Das Modul ist im wis2box-api-Container installiert und kann von der Kommandozeile aus wie folgt verwendet werden:

```{.copy}
csv2bufr data transform \
    --bufr-template <bufr-mapping-template> \
    <input-csv-file>
```

Das Argument `--bufr-template` wird verwendet, um die BUFR-Mapping-Vorlagendatei anzugeben, die die Zuordnung zwischen den Eingabe-CSV-Daten und den Ausgabe-BUFR-Daten in einer JSON-Datei bereitstellt. Standardmäßige Mapping-Vorlagen sind im Verzeichnis `/opt/csv2bufr/templates` im wis2box-api-Container installiert.

### Überprüfen der Beispiel-CSV-Datei

Überprüfen Sie den Inhalt der Beispiel-CSV-Datei `aws-example.csv`:

```bash
more aws-example.csv
```

!!! question
    Wie viele Datenzeilen sind in der CSV-Datei? Was ist der WIGOS-Stationen-Identifikator der Stationen, die in der CSV-Datei berichten?

??? question "Klicken, um die Antwort zu enthüllen"

    Die Ausgabe zeigt Folgendes:

    ```{.copy}
    wsi_series,wsi_issuer,wsi_issue_number,wsi_local,wmo_block_number,wmo_station_number,station_type,year,month,day,hour,minute,latitude,longitude,station_height_above_msl,barometer_height_above_msl,station_pressure,msl_pressure,geopotential_height,thermometer_height,air_temperature,dewpoint_temperature,relative_humidity,method_of_ground_state_measurement,ground_state,method_of_snow_depth_measurement,snow_depth,precipitation_intensity,anemometer_height,time_period_of_wind,wind_direction,wind_speed,maximum_wind_gust_direction_10_minutes,maximum_wind_gust_speed_10_minutes,maximum_wind_gust_direction_1_hour,maximum_wind_gust_speed_1_hour,maximum_wind_gust_direction_3_hours,maximum_wind_gust_speed_3_hours,rain_sensor_height,total_precipitation_1_hour,total_precipitation_3_hours,total_precipitation_6_hours,total_precipitation_12_hours,total_precipitation_24_hours
    0,20000,0,60355,60,355,1,2024,3,31,1,0,47.77706163,23.94046026,503,504.43,100940,101040,1448,5,298.15,294.55,80,3,1,1,0,0.004,10,-10,30,3,30,5,40,9,20,11,2,4.7,5.3,7.9,9.5,11.4
    0,20000,0,60355,60,355,1,2024,3,31,2,0,47.77706163,23.94046026,503,504.43,100940,101040,1448,5,25.,294.55,80,3,1,1,0,0.004,10,-10,30,3,30,5,40,9,20,11,2,4.7,5.3,7.9,9.5,11.4
    0,20000,0,60355,60,355,1,2024,3,31,3,0,47.77706163,23.94046026,503,504.43,100940,101040,1448,5,298.15,294.55,80,3,1,1,0,0.004,10,-10,30,3,30,5,40,9,20,11,2,4.7,5.3,7.9,9.5,11.4
    ```

    Die erste Zeile der CSV-Datei enthält die Spaltenüberschriften, die verwendet werden, um die Daten in jeder Spalte zu identifizieren.

    Nach der Überschriftenzeile gibt es 3 Datenzeilen, die 3 Wetterbeobachtungen von derselben Station mit dem WIGOS-Stationen-Identifikator `0-20000-0-60355` zu drei verschiedenen Zeitstempeln `2024-03-31 01:00:00`, `2024-03-31 02:00:00` und `2024-03-31 03:00:00` darstellen.

### Überprüfen der aws-Vorlage

Der wis2box-api enthält eine Reihe von vordefinierten BUFR-Mapping-Vorlagen, die im Verzeichnis `/opt/csv2bufr/templates` installiert sind.

Überprüfen Sie den Inhalt des Verzeichnisses `/opt/csv2bufr/templates`:

```bash
ls /opt/csv2bufr/templates
```
Sie sollten folgende Ausgabe sehen:

```{.copy}
CampbellAfrica-v1-template.json  aws-template.json  daycli-template.json
```

Überprüfen wir den Inhalt der Datei `aws-template.json`:

```bash
cat /opt/csv2bufr/templates/aws-template.json
```

Dies gibt eine große JSON-Datei zurück, die die Zuordnung für 43 CSV-Spalten bereitstellt.

!!! question
    Welche CSV-Spalte ist dem eccodes-Schlüssel `airTemperature` zugeordnet? Was sind die gültigen Mindest- und Höchstwerte für diesen Schlüssel?

??? success "Klicken, um die Antwort zu enthüllen"

    Verwenden Sie den folgenden Befehl, um die Ausgabe zu filtern:

    ```bash
    cat /opt/csv2bufr/templates/aws-template.json | grep -i airTemperature
    ```
    Sie sollten folgende Ausgabe sehen:

    ```{.copy}
    {"eccodes_key": "#1#airTemperature", "value": "data:air_temperature", "valid_min": "const:193.15", "valid_max": "const:333.15"},
    ```

    Der Wert, der für den eccodes-Schlüssel `airTemperature` kodiert wird, wird aus den Daten in der CSV-Spalte: **air_temperature** entnommen.

    Die Mindest- und Höchstwerte für diesen Schlüssel sind `193.15` bzw. `333.15`.

!!! question

    Welche CSV-Spalte ist dem eccodes-Schlüssel `internationalDataSubCategory` zugeordnet? Was ist der Wert dieses Schlüssels?

??? success "Klicken, um die Antwort zu enthüllen"
    Verwenden Sie den folgenden Befehl, um die Ausgabe zu filtern:

    ```bash
    cat /opt/csv2bufr/templates/aws-template.json | grep -i internationalDataSubCategory
    ```
    Sie sollten folgende Ausgabe sehen:

    ```{.copy}
    {"eccodes_key": "internationalDataSubCategory", "value": "const:2"},
    ```

    **Es gibt keine CSV-Spalte, die dem eccodes-Schlüssel `internationalDataSubCategory` zugeordnet ist**, stattdessen wird der konstante Wert 2 verwendet und wird in allen BUFR-Dateien kodiert, die mit dieser Mapping-Vorlage erstellt wurden.

### CSV in BUFR konvertieren

Versuchen wir, die Datei in das BUFR-Format zu konvertieren, indem wir den Befehl `csv2bufr` verwenden:

```{.copy}
csv2bufr data transform --bufr-template aws-template ./aws-example.csv
```

!!! question
    Wie viele BUFR-Dateien wurden erstellt?

??? success "Klicken, um die Antwort zu enthüllen"

    Die Ausgabe zeigt Folgendes:

    ```{.copy}
    CLI:    ... Transforming ./aws-example.csv to BUFR ...
    CLI:    ... Processing subsets:
    CLI:    ..... 384 bytes written to ./WIGOS_0-20000-0-60355_20240331T010000.bufr4
    #1#airTemperature: Value (25.0) out of valid range (193.15 - 333.15).; Element set to missing
    CLI:    ..... 384 bytes written to ./WIGOS_0-20000-0-60355_20240331T020000.bufr4
    CLI:    ..... 384 bytes written to ./WIGOS_0-20000-0-60355_20240331T030000.bufr4
    CLI:    End of processing, exiting.
    ```

    Die Ausgabe zeigt, dass 3 BUFR-Dateien erstellt wurden: `WIGOS_0-20000-0-60355_20240331T010000.bufr4`, `WIGOS_0-20000-0-60355_20240331T020000.bufr4` und `WIGOS_0-20000-0-60355_20240331T030000.bufr4`.

Um den Inhalt der BUFR-Dateien zu überprüfen, während fehlende Werte ignoriert werden, können Sie den folgenden Befehl verwenden:

```bash
bufr_dump -p WIGOS_0-20000-0-60355_20240331T010000.bufr4 | grep -v MISSING
```

!!! question
    Was ist der Wert des eccodes-Schlüssels `airTemperature` in der BUFR-Datei `WIGOS_0-20000-0-60355_20240331T010000.bufr4`? Und wie sieht es in der BUFR-Datei `WIGOS_0-20000-0-60355_20240331T020000.bufr4` aus?

??? success "Klicken, um die Antwort zu enthüllen"
    Um die Ausgabe zu filtern, können Sie den folgenden Befehl verwenden:

    ```bash
    bufr_dump -p WIGOS_0-20000-0-60355_20240331T010000.bufr4 | grep -v MISSING | grep airTemperature
    ```
    Sie sollten folgende Ausgabe sehen:

    ```{.copy}
    #1#airTemperature

Sie erhalten kein Ergebnis, was darauf hinweist, dass der Wert für den Schlüssel `airTemperature` in der BUFR-Datei `WIGOS_0-20000-0-60355_20240331T020000.bufr4` fehlt. Das Tool csv2bufr hat sich geweigert, den Wert `25.0` aus den CSV-Daten zu kodieren, da er außerhalb des gültigen Bereichs von `193.15` und `333.15` liegt, wie im Mapping-Template definiert.

Beachten Sie, dass die Umwandlung von CSV in BUFR mit einem der vordefinierten BUFR-Mapping-Templates Einschränkungen hat:

- Die CSV-Datei muss im im Mapping-Template definierten Format vorliegen, d.h. die CSV-Spaltennamen müssen mit den im Mapping-Template definierten Namen übereinstimmen
- Sie können nur die im Mapping-Template definierten Schlüssel kodieren
- Die Qualitätskontrollprüfungen sind auf die im Mapping-Template definierten Prüfungen beschränkt

Für Informationen, wie man benutzerdefinierte BUFR-Mapping-Templates erstellt und verwendet, siehe die nächste praktische Übung [csv2bufr-templates](./csv2bufr-templates.md).

## Fazit

!!! success "Herzlichen Glückwunsch!"
    In dieser praktischen Sitzung haben Sie gelernt:

    - wie man auf ecCodes-Befehlszeilenwerkzeuge innerhalb des wis2box-api Containers zugreift
    - wie man `synop2bufr` verwendet, um FM-12 SYNOP-Berichte von der Befehlszeile aus in BUFR zu konvertieren
    - wie man das SYNOP-Formular in der wis2box-webapp verwendet, um FM-12 SYNOP-Berichte in BUFR zu konvertieren
    - wie man `csv2bufr` verwendet, um CSV-Daten von der Befehlszeile aus in BUFR zu konvertieren
---
title: CSV-zu-BUFR-Mappingvorlagen
---

# CSV-zu-BUFR-Mappingvorlagen

!!! abstract "Lernergebnisse"
    Am Ende dieser praktischen Sitzung werden Sie in der Lage sein:

    - eine neue BUFR-Mappingvorlage für Ihre CSV-Daten zu erstellen
    - Ihre benutzerdefinierte BUFR-Mappingvorlage über die Befehlszeile bearbeiten und debuggen
    - das CSV-zu-BUFR-Daten-Plugin so konfigurieren, dass es eine benutzerdefinierte BUFR-Mappingvorlage verwendet
    - die integrierten AWS- und DAYCLI-Vorlagen für die Umwandlung von CSV-Daten in BUFR verwenden

## Einführung

Kommagetrennte Werte (CSV) werden häufig verwendet, um Beobachtungsdaten und andere Daten in einem tabellarischen Format aufzuzeichnen.
Die meisten Datenlogger, die zur Aufzeichnung von Sensorausgaben verwendet werden, können die Beobachtungen in durch Trennzeichen getrennten Dateien exportieren, einschließlich in CSV.
Ebenso ist es einfach, die erforderlichen Daten aus einer Datenbank in CSV-formatierten Dateien zu exportieren.

Das wis2box csv2bufr Modul bietet ein Befehlszeilentool zur Umwandlung von CSV-Daten in das BUFR-Format. Wenn Sie csv2bufr verwenden, müssen Sie eine BUFR-Mappingvorlage bereitstellen, die CSV-Spalten den entsprechenden BUFR-Elementen zuordnet. Wenn Sie keine eigene Mappingvorlage erstellen möchten, können Sie die integrierten AWS- und DAYCLI-Vorlagen für die Umwandlung von CSV-Daten in BUFR verwenden, müssen jedoch sicherstellen, dass die von Ihnen verwendeten CSV-Daten im richtigen Format für diese Vorlagen vorliegen. Wenn Sie Parameter entschlüsseln möchten, die nicht in den AWS- und DAYCLI-Vorlagen enthalten sind, müssen Sie Ihre eigene Mappingvorlage erstellen.

In dieser Sitzung lernen Sie, wie Sie Ihre eigene Mappingvorlage für die Umwandlung von CSV-Daten in BUFR erstellen. Sie lernen auch, wie Sie die integrierten AWS- und DAYCLI-Vorlagen für die Umwandlung von CSV-Daten in BUFR verwenden.

## Vorbereitung

Stellen Sie sicher, dass der wis2box-Stack mit `python3 wis2box.py start` gestartet wurde.

Stellen Sie sicher, dass Sie einen Webbrowser geöffnet haben mit der MinIO UI für Ihre Instanz, indem Sie `http://YOUR-HOST:9000` aufrufen.
Wenn Sie Ihre MinIO-Anmeldeinformationen nicht mehr wissen, finden Sie diese in der Datei `wis2box.env` im Verzeichnis `wis2box` auf Ihrer Studenten-VM.

Stellen Sie sicher, dass Sie MQTT Explorer geöffnet und mit Ihrem Broker verbunden haben, indem Sie die Anmeldeinformationen `everyone/everyone` verwenden.

## Erstellen einer Mappingvorlage

Das csv2bufr-Modul wird mit einem Befehlszeilentool geliefert, um Ihre eigene Mappingvorlage unter Verwendung einer Reihe von BUFR-Sequenzen und/oder BUFR-Elementen als Eingabe zu erstellen.

Um spezifische BUFR-Sequenzen und -Elemente zu finden, können Sie auf die BUFR-Tabellen unter [https://confluence.ecmwf.int/display/ECC/BUFR+tables](https://confluence.ecmwf.int/display/ECC/BUFR+tables) verweisen.

### csv2bufr Mappings Befehlszeilentool

Um auf das csv2bufr Befehlszeilentool zuzugreifen, müssen Sie sich im wis2box-api-Container anmelden:

```bash
cd ~/wis2box
python3 wis2box-ctl.py login wis2box-api
```

Um die Hilfeseite für den Befehl `csv2bufr mapping` zu drucken:

```bash
csv2bufr mappings --help
```

Die Hilfeseite zeigt 2 Unterbefehle:

- `csv2bufr mappings create` : Erstellen einer neuen Mappingvorlage
- `csv2bufr mappings list` : Auflisten der im System verfügbaren Mappingvorlagen

!!! Note "csv2bufr mapping list"

    Der Befehl `csv2bufr mapping list` zeigt Ihnen die im System verfügbaren Mappingvorlagen.
    Standardvorlagen sind im Verzeichnis `/opt/wis2box/csv2bufr/templates` im Container gespeichert.

    Um benutzerdefinierte Mappingvorlagen mit dem System zu teilen, können Sie diese im Verzeichnis speichern, das durch `$CSV2BUFR_TEMPLATES` definiert ist, das standardmäßig im Container auf `/data/wis2box/mappings` eingestellt ist. Da das Verzeichnis `/data/wis2box/mappings` im Container auf das Verzeichnis `$WIS2BOX_HOST_DATADIR/mappings` auf dem Host gemountet ist, finden Sie Ihre benutzerdefinierten Mappingvorlagen im Verzeichnis `$WIS2BOX_HOST_DATADIR/mappings` auf dem Host.

Lassen Sie uns versuchen, eine neue benutzerdefinierte Mappingvorlage mit dem Befehl `csv2bufr mapping create` zu erstellen, indem wir die BUFR-Sequenz 301150 plus das BUFR-Element 012101 als Eingabe verwenden.

```bash
csv2bufr mappings create 301150 012101 --output /data/wis2box/mappings/my_custom_template.json
```

Sie können den Inhalt der Mappingvorlage, die Sie gerade erstellt haben, mit dem Befehl `cat` überprüfen:

```bash
cat /data/wis2box/mappings/my_custom_template.json
```

!!! question "Inspektion der Mappingvorlage"

    Wie viele CSV-Spalten werden auf BUFR-Elemente abgebildet? Was ist der CSV-Header für jedes abgebildete BUFR-Element?

??? success "Klicken, um die Antwort zu enthüllen"
    
    Die von Ihnen erstellte Mappingvorlage bildet **5** CSV-Spalten auf BUFR-Elemente ab, nämlich die 4 BUFR-Elemente in der Sequenz 301150 plus das BUFR-Element 012101. 

    Die folgenden CSV-Spalten werden auf BUFR-Elemente abgebildet:

    - **wigosIdentifierSeries** wird auf `"eccodes_key": "#1#wigosIdentifierSeries"` abgebildet (BUFR-Element 001125)
    - **wigosIssuerOfIdentifier** wird auf `"eccodes_key": "#1#wigosIssuerOfIdentifier` abgebildet (BUFR-Element 001126)
    - **wigosIssueNumber** wird auf `"eccodes_key": "#1#wigosIssueNumber"` abgebildet (BUFR-Element 001127)
    - **wigosLocalIdentifierCharacter** wird auf `"eccodes_key": "#1#wigosLocalIdentifierCharacter"` abgebildet (BUFR-Element 001128)
    - **airTemperature** wird auf `"eccodes_key": "#1#airTemperature"` abgebildet (BUFR-Element 012101)

Die von Ihnen erstellte Mappingvorlage vermisst wichtige Metadaten über die gemachte Beobachtung, das Datum und die Uhrzeit der Beobachtung sowie die Breiten- und Längengrade der Station.

Als nächstes werden wir die Mappingvorlage aktualisieren und die folgenden Sequenzen hinzufügen:
    
- **301011** für Datum (Jahr, Monat, Tag)
- **301012** für Zeit (Stunde, Minute)
- **301023** für Standort (Breiten-/Längengrad (grobe Genauigkeit))

Und die folgenden Elemente:

- **010004** für Druck
- **007031** für Barometerhöhe über dem Meeresspiegel

Führen Sie den folgenden Befehl aus, um die Mappingvorlage zu aktualisieren:

```bash
csv2bufr mappings create 301150 301011 301012 301023 007031 012101 010004  --output /data/wis2box/mappings/my_custom_template.json
```

Und überprüfen Sie erneut den Inhalt der Mappingvorlage:

```bash
cat /data/wis2box/mappings/my_custom_template.json
```

!!! question "Inspektion der aktualisierten Mappingvorlage"

    Wie viele CSV-Spalten werden jetzt auf BUFR-Elemente abgebildet? Was ist der CSV-Header für jedes abgebildete BUFR-Element?

??? success "Klicken, um die Antwort zu enthüllen"
    
    Die von Ihnen erstellte Mappingvorlage bildet jetzt **18** CSV-Spalten auf BUFR-Elemente ab:
    - 4 BUFR-Elemente aus der BUFR-Sequenz 301150
    - 3 BUFR-Elemente aus der BUFR-Sequenz 301011
    - 2 BUFR-Elemente aus der BUFR-Sequenz 301012
    - 2 BUFR-Elemente aus der BUFR-Sequenz 301023
    - BUFR-Element 007031
    - BUFR-Element 012101

    Die folgenden CSV-Spalten werden auf BUFR-Elemente abgebildet:

    - **wigosIdentifierSeries** wird auf `"eccodes_key": "#1#wigosIdentifierSeries"` abgebildet (BUFR-Element 001125)
    - **wigosIssuerOfIdentifier** wird auf `"eccodes_key": "#1#wigosIssuerOfIdentifier` abgebildet (BUFR-Element 001126)
    - **wigosIssueNumber** wird auf `"eccodes_key": "#1#wigosIssueNumber"` abgebildet (BUFR-Element 001127)
    - **wigosLocalIdentifierCharacter** wird auf `"eccodes_key": "#1#wigosLocalIdentifierCharacter"` abgebildet (BUFR-Element 001128)
    - **year** wird auf `"eccodes_key": "#1#year"` abgebildet (BUFR-Element 004001)
    - **month** wird auf `"eccodes_key": "#1#month"` abgebildet (BUFR-Element 004002)
    - **day** wird auf `"eccodes_key": "#1#day"` abgebildet (BUFR-Element 004003)
    - **hour** wird auf `"eccodes_key": "#1#hour"` abgebildet (BUFR-Element 004004)
    - **minute** wird auf `"eccodes_key": "#1#minute"` abgebildet (BUFR-Element 004005)
    - **latitude** wird auf `"eccodes_key": "#1#latitude"` abgebildet (BUFR-Element 005002)
    - **longitude** wird auf `"eccodes_key": "#1#longitude"` abgebildet (BUFR-Element 006002)
    - **heightOfBarometerAboveMeanSeaLevel"** wird auf `"eccodes_key": "#1#heightOfBarometerAboveMeanSeaLevel"` abgebildet (BUFR-Element 007031)
    - **airTemperature** wird auf `"eccodes_key": "#1#airTemperature"` abgebildet (BUFR-Element 012101)
    - **nonCoordinatePressure** wird auf `"eccodes_key": "#1#nonCoordinatePressure"` abgebildet (BUFR-Element 010004)

Überprüfen Sie den Inhalt der Datei `custom_template_data.csv` im Verzeichnis `/root/data-conversion-exercises`:

```bash
cat /root/data-conversion-exercises/custom_template_data.csv
```

Beachten Sie, dass die Header dieser CSV-Datei dieselben sind wie die CSV-Header in der von Ihnen erstellten Mappingvorlage.

Um die Datenkonvertierung zu testen, können wir das Befehlszeilentool `csv2bufr` verwenden, um die CSV-Datei mit der von uns erstellten Mappingvorlage in BUFR zu konvertieren:

```bash
csv2bufr data transform --bufr-template my_custom_template /root/data-conversion-exercises/custom_template_data.csv
```

Sie sollten die folgende Ausgabe sehen:

```bash
CLI:    ... Transforming /root/data-conversion-exercises/custom_template_data.csv to BUFR ...
CLI:    ... Processing subsets:
CLI:    ..... 94 bytes written to ./WIGOS_0-20000-0-15015_20250412T210000.bufr4
CLI:    End of processing, exiting.
```

!!! question "Überprüfen Sie den Inhalt der BUFR-Datei"
    
    Wie können Sie den Inhalt der BUFR-Datei, die Sie gerade erstellt haben, überprüfen und verifizieren, dass sie die Daten korrekt codiert hat?

??? success "Klicken, um die Antwort zu enthüllen"

    Sie können den Befehl `bufr_dump -p` verwenden, um den Inhalt der von Ihnen erstellten BUFR-Datei zu überprüfen.
    Der Befehl zeigt Ihnen den Inhalt der BUFR-Datei in einem für Menschen lesbaren Format.

    ```bash
    bufr_dump -p ./WIGOS_0-20000-0-15015_20250412T210000.bufr4
    ```

    In der Ausgabe sehen Sie Werte für die BUFR-Elemente, die Sie in der Vorlage zugeordnet haben, zum Beispiel wird die "airTemperature" angezeigt:
    
    ```bash
    airTemperature=298.15
    ```

Sie können jetzt den Container verlassen:

```bash
exit
```

### Verwendung der Mappingvorlage in der wis2box

Um sicherzustellen, dass die neue Mappingvorlage vom wis2box-api-Container erkannt wird, müssen Sie den Container neu starten:

```bash
docker restart wis2box-api
```

Sie können jetzt Ihre Datensatz in der wis2box-webapp konfigurieren, um die benutzerdefinierte Mappingvorlage für das CSV-zu-BUFR-Konvertierungs-Plugin zu verwenden.

Die wis2box-webapp erkennt automatisch die von Ihnen erstellte Mappingvorlage und macht sie in der Liste der Vorlagen für das CSV-zu-BUFR-Konvertierungs-Plugin verfügbar.

Klicken Sie auf den Datensatz, den Sie in der vorherigen praktischen Sitzung erstellt haben, und klicken Sie auf "UPDATE" neben dem Plugin mit dem Namen "CSV data converted to BUFR":

<img alt="Bild zeigt den Datensatz-Editor in der wis2box-webapp" src="../../assets/img/wis2box-webapp-data-mapping-update-csv2bufr.png"/>

Sie sollten die neue Vorlage, die Sie erstellt haben, in der Liste der verfügbaren Vorlagen sehen:

<img alt="Bild zeigt die csv2bufr-Vorlagen in der wis2box-webapp" src="../../assets/img/wis2box-webapp-csv2bufr-templates.png"/>

!!! hint

    Beachten Sie, dass, wenn Sie die neue Vorlage, die Sie erstellt haben, nicht sehen, versuchen Sie die Seite zu aktualisieren oder öffnen Sie sie in einem neuen Inkognito-Fenster.

Für jetzt behalten Sie die Standardauswahl der AWS-Vorlage bei (klicken Sie oben rechts, um die Plugin-Konfiguration zu schließen).

## Verwendung der 'AWS'-Vorlage

Die 'AWS'-Vorlage bietet eine Mappingvorlage für die Umwandlung von CSV-Daten in die BUFR-Sequenz 301150, 307096, zur Unterstützung der minimalen GBON-Anforderungen.

Die Beschreibung der AWS-Vorlage finden Sie hier [aws-template](./../csv2bufr-templates/aws-template.md).

### Überprüfen der aws-example Eingabedaten

Laden Sie das Beispiel für diese Übung von dem unten stehenden Link herunter:

[aws-example.csv](./../../sample-data/aws-example.csv)

Öffnen Sie die heruntergeladene Datei in einem Editor und überprüfen Sie den Inhalt:

!!! question
    Wenn Sie das Datum, die Zeit und die Identifikationsfelder (WIGOS und traditionelle Identifikatoren) untersuchen, was fällt Ihnen auf? Wie würde das heutige Datum dargestellt?

??? success "Klicken, um die Antwort zu enthüllen"
    Jede Spalte enthält eine einzelne Information. Zum Beispiel ist das Datum in Jahr, Monat und Tag aufgeteilt, was widerspiegelt, wie die Daten in BUFR gespeichert sind. Das heutige Datum würde über die Spalten "year", "month" und "day" aufgeteilt. Ähnlich muss die Zeit in "hour" und "minute" und der WIGOS-Station-Identifier in seine jeweiligen Komponenten aufgeteilt werden.

!!! question
    Wenn Sie sich die Datendatei ansehen, wie werden fehlende Daten codiert?
    
??? success "Klicken, um die Antwort zu enthüllen"
    Fehlende Daten in der Datei werden durch leere Zellen dargestellt. In einer CSV-Datei würde dies durch ``,,`` codiert. Beachten Sie, dass dies eine leere Zelle ist und nicht als Zeichenkette der Länge null codiert wird, z.B. ``,"",``.

!!! Hinweis "Fehlende Daten"
    Es ist bekannt, dass Daten aus verschiedenen Gründen fehlen können, sei es aufgrund eines Sensorausfalls oder weil der Parameter nicht beobachtet wurde. In diesen Fällen können fehlende Daten gemäß der obigen Antwort kodiert werden, die anderen Daten im Bericht bleiben gültig.

### Aktualisieren Sie die Beispieldatei

Aktualisieren Sie die Beispieldatei, die Sie heruntergeladen haben, um das heutige Datum und die Uhrzeit zu verwenden, und ändern Sie die WIGOS-Stationen-Identifikatoren, um Stationen zu verwenden, die Sie in der wis2box-webapp registriert haben.

### Laden Sie die Daten in MinIO hoch und überprüfen Sie das Ergebnis

Navigieren Sie zur MinIO-Benutzeroberfläche und melden Sie sich mit den Anmeldeinformationen aus der Datei `wis2box.env` an.

Navigieren Sie zu **wis2box-incoming** und klicken Sie auf die Schaltfläche "Neuen Pfad erstellen":

<img alt="Image showing MinIO UI with the create folder button highlighted" src="../../assets/img/minio-create-new-path.png"/>

Erstellen Sie einen neuen Ordner im MinIO-Bucket, der mit der dataset-id für das Dataset übereinstimmt, das Sie mit der Vorlage='weather/surface-weather-observations/synop' erstellt haben:

<img alt="Image showing MinIO UI with the create folder button highlighted" src="../../assets/img/minio-create-new-path-metadata_id.png"/>

Laden Sie die Beispieldatei, die Sie heruntergeladen haben, in den Ordner hoch, den Sie im MinIO-Bucket erstellt haben:

<img alt="Image showing MinIO UI with aws-example uploaded" src="../../assets/img/minio-upload-aws-example.png"/>

Überprüfen Sie das Grafana-Dashboard unter `http://YOUR-HOST:3000`, um zu sehen, ob WARNUNGEN oder FEHLER vorliegen. Wenn Sie welche sehen, versuchen Sie, sie zu beheben und wiederholen Sie die Übung.

Überprüfen Sie den MQTT Explorer, um zu sehen, ob Sie WIS2-Datenbenachrichtigungen erhalten.

Wenn Sie die Daten erfolgreich eingespeist haben, sollten Sie 3 Benachrichtigungen im MQTT Explorer zum Thema `origin/a/wis2/<centre-id>/data/weather/surface-weather-observations/synop` für die 3 Stationen sehen, für die Sie Daten gemeldet haben:

<img width="450" alt="Image showing MQTT explorer after uploading AWS" src="../../assets/img/mqtt-explorer-aws-upload.png"/>

## Verwendung der 'DayCLI'-Vorlage

Die **DayCLI**-Vorlage bietet eine Zuordnungsvorlage zur Umwandlung täglicher Klima-CSV-Daten in die BUFR-Sequenz 307075, zur Unterstützung der Berichterstattung über tägliche Klimadaten.

Die Beschreibung der DAYCLI-Vorlage finden Sie hier [daycli-template](./../csv2bufr-templates/daycli-template.md).

Um diese Daten auf WIS2 zu teilen, müssen Sie ein neues Dataset in der wis2box-webapp erstellen, das die korrekte WIS2-Themenhierarchie hat und die DAYCLI-Vorlage zur Umwandlung von CSV-Daten in BUFR verwendet.

### Erstellen eines wis2box-Datasets für die Veröffentlichung von DAYCLI-Nachrichten

Gehen Sie zum Dataset-Editor in der wis2box-webapp und erstellen Sie ein neues Dataset. Verwenden Sie dieselbe Centre-ID wie in den vorherigen praktischen Sitzungen und wählen Sie **Data Type='climate/surface-based-observations/daily'**:

<img alt="Create a new dataset in the wis2box-webapp for DAYCLI" src="../../assets/img/wis2box-webapp-create-dataset-daycli.png"/>

Klicken Sie auf "CONTINUE TO FORM" und fügen Sie eine Beschreibung für Ihr Dataset hinzu, setzen Sie das Begrenzungsrechteck und geben Sie die Kontaktdaten für das Dataset an. Sobald Sie alle Abschnitte ausgefüllt haben, klicken Sie auf 'VALIDATE FORM' und überprüfen Sie das Formular.

Überprüfen Sie die Daten-Plugins für die Datasets. Klicken Sie neben dem Plugin mit dem Namen "CSV data converted to BUFR" auf "UPDATE" und Sie werden sehen, dass die Vorlage auf **DayCLI** eingestellt ist:

<img alt="Update the data plugin for the dataset to use the DAYCLI template" src="../../assets/img/wis2box-webapp-update-data-plugin-daycli.png"/>

Schließen Sie die Plugin-Konfiguration und reichen Sie das Formular mit dem Authentifizierungstoken ein, das Sie in der vorherigen praktischen Sitzung erstellt haben.

Sie sollten nun ein zweites Dataset in der wis2box-webapp haben, das so konfiguriert ist, dass es die DAYCLI-Vorlage zur Umwandlung von CSV-Daten in BUFR verwendet.

### Überprüfen der daycli-Beispieldateneingabe

Laden Sie das Beispiel für diese Übung von dem unten stehenden Link herunter:

[daycli-example.csv](./../../sample-data/daycli-example.csv)

Öffnen Sie die heruntergeladene Datei in einem Editor und überprüfen Sie den Inhalt:

!!! Frage
    Welche zusätzlichen Variablen sind in der DayCLI-Vorlage enthalten?

??? Erfolg "Klicken Sie, um die Antwort zu enthüllen"
    Die DayCLI-Vorlage enthält wichtige Metadaten über die Instrumentenplatzierung und die Messqualitätsklassifikationen für Temperatur und Feuchtigkeit, Qualitätskontrollflags und Informationen darüber, wie die tägliche Durchschnittstemperatur berechnet wurde.

### Aktualisieren Sie die Beispieldatei

Die Beispieldatei enthält eine Zeile Daten für jeden Tag in einem Monat und berichtet Daten für eine Station. Aktualisieren Sie die Beispieldatei, die Sie heruntergeladen haben, um das heutige Datum und die Uhrzeit zu verwenden und ändern Sie die WIGOS-Stationen-Identifikatoren, um eine Station zu verwenden, die Sie in der wis2box-webapp registriert haben.

### Laden Sie die Daten in MinIO hoch und überprüfen Sie das Ergebnis

Wie zuvor müssen Sie die Daten in den 'wis2box-incoming' Bucket in MinIO hochladen, damit sie vom csv2bufr-Konverter verarbeitet werden. Dieses Mal müssen Sie einen neuen Ordner im MinIO-Bucket erstellen, der mit der dataset-id für das Dataset übereinstimmt, das Sie mit der Vorlage='climate/surface-based-observations/daily' erstellt haben, die sich von der dataset-id unterscheidet, die Sie in der vorherigen Übung verwendet haben:

<img alt="Image showing MinIO UI with DAYCLI-example uploaded" src="../../assets/img/minio-upload-daycli-example.png"/>

Nach dem Hochladen der Daten überprüfen Sie, ob im Grafana-Dashboard keine WARNUNGEN oder FEHLER vorliegen, und überprüfen Sie den MQTT Explorer, um zu sehen, ob Sie WIS2-Datenbenachrichtigungen erhalten.

Wenn Sie die Daten erfolgreich eingespeist haben, sollten Sie 30 Benachrichtigungen im MQTT Explorer zum Thema `origin/a/wis2/<centre-id>/data/climate/surface-based-observations/daily` für die 30 Tage im Monat sehen, für die Sie Daten gemeldet haben:

<img width="450" alt="Image showing MQTT explorer after uploading DAYCLI" src="../../assets/img/mqtt-daycli-template-success.png"/>

## Schlussfolgerung

!!! Erfolg "Herzlichen Glückwunsch"
    In dieser praktischen Sitzung haben Sie gelernt:

    - wie man eine benutzerdefinierte Zuordnungsvorlage zur Umwandlung von CSV-Daten in BUFR erstellt
    - wie man die integrierten AWS- und DAYCLI-Vorlagen zur Umwandlung von CSV-Daten in BUFR verwendet
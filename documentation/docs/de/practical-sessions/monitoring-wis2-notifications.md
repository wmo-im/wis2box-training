---
title: Überwachung von WIS2-Benachrichtigungen
---

# Überwachung von WIS2-Benachrichtigungen

!!! abstract "Lernergebnisse"

    Am Ende dieser praktischen Sitzung werden Sie in der Lage sein:
    
    - den wis2box-Workflow durch Hochladen von Daten in MinIO mit dem Befehl `wis2box data ingest` auszulösen
    - Warnungen und Fehler anzeigen, die im Grafana-Dashboard angezeigt werden
    - den Inhalt der veröffentlichten Daten überprüfen

## Einführung

Das **Grafana-Dashboard** verwendet Daten von Prometheus und Loki, um den Status Ihrer wis2box anzuzeigen. Prometheus speichert Zeitreihendaten aus den gesammelten Metriken, während Loki die Protokolle von den Containern speichert, die auf Ihrer wis2box-Instanz laufen. Diese Daten ermöglichen es Ihnen zu überprüfen, wie viele Daten auf MinIO empfangen werden, wie viele WIS2-Benachrichtigungen veröffentlicht werden und ob Fehler in den Protokollen erkannt wurden.

Um den Inhalt der WIS2-Benachrichtigungen zu sehen, die auf verschiedenen Themen Ihrer wis2box veröffentlicht werden, können Sie die Registerkarte 'Überwachen' in der **wis2box-webapp** verwenden.

## Vorbereitung

In diesem Abschnitt wird das zuvor im praktischen Kurs [Konfigurieren von Datensätzen in wis2box](/practical-sessions/configuring-wis2box-datasets) erstellte Datenset "surface-based-observations/synop" verwendet.

Melden Sie sich mit Ihrem SSH-Client (PuTTY oder einem anderen) an Ihrer Studenten-VM an.

Stellen Sie sicher, dass wis2box läuft:

```bash
cd ~/wis2box-1.0.0rc1/
python3 wis2box-ctl.py start
python3 wis2box-ctl.py status
```

Stellen Sie sicher, dass Sie MQTT Explorer laufen haben und mit Ihrer Instanz unter Verwendung der öffentlichen Anmeldeinformationen `everyone/everyone` mit einem Abonnement für das Thema `origin/a/wis2/#` verbunden sind.

Stellen Sie sicher, dass Sie Zugriff auf die MinIO-Web-Oberfläche haben, indem Sie `http://<your-host>:9000` aufrufen und Sie angemeldet sind (mit `WIS2BOX_STORAGE_USERNAME` und `WIS2BOX_STORAGE_PASSWORD` aus Ihrer `wis2box.env`-Datei).

Stellen Sie sicher, dass Sie einen Webbrowser mit dem Grafana-Dashboard für Ihre Instanz geöffnet haben, indem Sie `http://<your-host>:3000` aufrufen.

## Einige Daten eingeben

Bitte führen Sie die folgenden Befehle von Ihrer SSH-Client-Sitzung aus:

Kopieren Sie die Beispieldatendatei `aws-example.csv` in das Verzeichnis, das Sie als `WI2BOX_HOST_DATADIR` in Ihrer `wis2box.env`-Datei definiert haben.

```bash
cp ~/exercise-materials/monitoring-exercises/aws-example.csv ~/wis2box-data/
```

Stellen Sie sicher, dass Sie sich im Verzeichnis `wis2box-1.0.0rc1` befinden und melden Sie sich am **wis2box-management**-Container an:

```bash
cd ~/wis2box-1.0.0rc1
python3 wis2box-ctl.py login
```

Überprüfen Sie, ob die Beispieldaten im Verzeichnis `/data/wis2box/` innerhalb des **wis2box-management**-Containers verfügbar sind:

```bash
ls -lh /data/wis2box/aws-example.csv
```

!!! note
    Das `WIS2BOX_HOST_DATADIR` wird als `/data/wis2box/` innerhalb des wis2box-management-Containers durch die `docker-compose.yml`-Datei im Verzeichnis `wis2box-1.0.0rc1` eingebunden.
    
    Dies ermöglicht Ihnen, Daten zwischen dem Host und dem Container zu teilen.

!!! question "Übung 1: Daten eingeben mit `wis2box data ingest`"

    Führen Sie den folgenden Befehl aus, um die Beispieldatendatei `aws-example.csv` in Ihre wis2box-Instanz einzugeben:

    ```bash
    wis2box data ingest -p /data/wis2box/aws-example.csv --metadata-id urn:wmo:md:not-my-centre:core.surface-based-observations.synop
    ```

    Wurden die Daten erfolgreich eingefügt? Wenn nicht, welche Fehlermeldung wurde angezeigt und wie können Sie sie beheben?

??? success "Klicken, um Antwort zu enthüllen"

    Sie werden die folgende Ausgabe sehen:

    ```bash
    Error: metadata_id=urn:wmo:md:not-my-centre:core.surface-based-observations.synop not found in data mappings
    ```

    Die Fehlermeldung zeigt an, dass der von Ihnen bereitgestellte Metadaten-Identifikator mit keinem der Datensätze übereinstimmt, die Sie in Ihrer wis2box-Instanz konfiguriert haben.

    Geben Sie die korrekte Metadaten-ID an, die mit dem von Ihnen im vorherigen praktischen Kurs erstellten Datensatz übereinstimmt, und wiederholen Sie den Befehl zur Dateneingabe, bis Sie die folgende Ausgabe sehen sollten:

    ```bash 
    Processing /data/wis2box/aws-example.csv
    Done
    ```

Gehen Sie zur MinIO-Konsole in Ihrem Browser und überprüfen Sie, ob die Datei `aws-example.csv` im `wis2box-incoming`-Bucket hochgeladen wurde. Sie sollten dort ein neues Verzeichnis mit dem Namen des Datensatzes sehen, den Sie in der Option `--metadata-id` angegeben haben:

<img alt="minio-wis2box-incoming-dataset-folder" src="../../assets/img/minio-wis2box-incoming-dataset-folder.png" width="800">

!!! note
    Der Befehl `wis2box data ingest` lud die Datei in den `wis2box-incoming`-Bucket in MinIO in einem Verzeichnis hoch, das nach dem von Ihnen bereitgestellten Metadaten-Identifikator benannt wurde.

Gehen Sie zum Grafana-Dashboard in Ihrem Browser und überprüfen Sie den Status der Dateneingabe.

!!! question "Übung 2: Überprüfen Sie den Status der Dateneingabe"
    
    Gehen Sie zum Grafana-Dashboard in Ihrem Browser und überprüfen Sie den Status der Dateneingabe.
    
    Wurden die Daten erfolgreich eingefügt?

??? success "Klicken, um Antwort zu enthüllen"
    Das Panel am unteren Rand des Grafana-Start-Dashboards meldet die folgenden Warnungen:    
    
    `WARNING - input=aws-example.csv warning=Station 0-20000-0-60355 not in station list; skipping`
    `WARNING - input=aws-example.csv warning=Station 0-20000-0-60360 not in station list; skipping`

    Diese Warnung zeigt an, dass die Stationen nicht in der Stationsliste Ihrer wis2box definiert sind. Es werden keine WIS2-Benachrichtigungen für diese Station veröffentlicht, bis Sie sie zur Stationsliste hinzufügen und sie mit dem Thema für Ihren Datensatz verknüpfen.

!!! question "Übung 3: Fügen Sie die Teststationen hinzu und wiederholen Sie die Dateneingabe"

    Fügen Sie die Stationen Ihrer wis2box mit dem Stationseditor in **wis2box-webapp** hinzu und verknüpfen Sie die Stationen mit dem Thema für Ihren Datensatz.

    Laden Sie nun die Beispieldatendatei `aws-example.csv` erneut in denselben Pfad in MinIO hoch, den Sie in der vorherigen Übung verwendet haben.

    Überprüfen Sie das Grafana-Dashboard, gibt es neue Fehler oder Warnungen? Wie können Sie sehen, dass die Testdaten erfolgreich eingefügt und veröffentlicht wurden?

??? success "Klicken, um Antwort zu enthüllen"

    Sie können die Diagramme auf dem Grafana-Start-Dashboard überprüfen, um zu sehen, ob die Testdaten erfolgreich eingefügt und veröffentlicht wurden.
    
    Bei Erfolg sollten Sie Folgendes sehen:

    <img alt="grafana_success" src="../../assets/img/grafana_success.png" width="800">

!!! question "Übung 4: Überprüfen Sie den MQTT-Broker auf WIS2-Benachrichtigungen"
    
    Gehen Sie zum MQTT Explorer und überprüfen Sie, ob Sie die WIS2-Benachrichtigungsnachricht für die Daten sehen können, die Sie gerade eingefügt haben.
    
    Wie viele WIS2-Datenbenachrichtigungen wurden von Ihrer wis2box veröffentlicht?
    
    Wie greifen Sie auf den Inhalt der veröffentlichten Daten zu?

??? success "Klicken, um Antwort zu enthüllen"

    Sie sollten 6 WIS2-Datenbenachrichtigungen sehen, die von Ihrer wis2box veröffentlicht wurden.

    Um auf den Inhalt der veröffentlichten Daten zuzugreifen, können Sie die Themenstruktur erweitern, um die verschiedenen Ebenen der Nachricht zu sehen, bis Sie die letzte Ebene erreichen und den Nachrichteninhalt einer der Nachrichten überprüfen.

    Der Nachrichteninhalt hat einen "links"-Abschnitt mit einem "rel"-Schlüssel von "canonical" und einem "href"-Schlüssel mit der URL zum Herunterladen der Daten. Die URL wird im Format `http://<your-host>/data/...` sein.
    
    Beachten Sie, dass das Datenformat BUFR ist und Sie einen BUFR-Parser benötigen, um den Inhalt der Daten anzuzeigen. Das BUFR-Format ist ein binäres Format, das von meteorologischen Diensten zur Datenaustausch verwendet wird. Die Daten-Plugins in wis2box haben die Daten von CSV in BUFR umgewandelt, bevor sie veröffentlicht wurden.

## Anzeigen des Inhalts der von Ihnen veröffentlichten Daten

Sie können die **wis2box-webapp** verwenden, um den Inhalt der WIS2-Datenbenachrichtigungen anzuzeigen, die von Ihrer wis2box veröffentlicht wurden.

Öffnen Sie die **wis2box-webapp** in Ihrem Browser, indem Sie zu `http://<your-host>/wis2box-webapp` navigieren und den Reiter **Überwachung** auswählen:

<img alt="wis2box-webapp-monitor" src="../../assets/img/wis2box-webapp-monitor.png" width="220">

Wählen Sie im Überwachungsreiter Ihre Datensatz-ID aus und klicken Sie auf "AKTUALISIEREN"

??? question "Übung 5: Anzeigen der WIS2-Benachrichtigungen in der wis2box-webapp"
    
    Wie viele WIS2-Datenbenachrichtigungen wurden von Ihrer wis2box veröffentlicht?

    Wie hoch ist die Lufttemperatur in der letzten Benachrichtigung an der Station mit dem WIGOS-Identifikator=0-20000-0-60355?

??? success "Klicken, um Antwort zu enthüllen"

    Wenn Sie die Testdaten erfolgreich eingefügt haben, sollten Sie 6 WIS2-Datenbenachrichtigungen sehen, die von Ihrer wis2box veröffentlicht wurden.

    Um die Lufttemperatur zu sehen, die für die Station mit dem WIGOS-Identifikator=0-20000-0-60355 gemessen wurde, klicken Sie auf den "INSPEKTIEREN"-Knopf neben der Datei für diese Station, um ein Popup-Fenster zu öffnen, das den analysierten Inhalt der Datendatei anzeigt. Die gemessene Lufttemperatur an dieser Station betrug 25,0 Grad Celsius.

!!! Note
    Der wis2box-api-Container enthält Werkzeuge zum Parsen von BUFR-Dateien und zur Anzeige des Inhalts in einem für Menschen lesbaren Format. Dies ist keine Kernanforderung für die WIS2.0-Implementierung, wurde jedoch in die wis2box aufgenommen, um Datenveröffentlichern zu helfen, den Inhalt der Daten, die sie veröffentlichen, zu überprüfen.

## Schlussfolgerung

!!! success "Herzlichen Glückwunsch!"
    In dieser praktischen Sitzung haben Sie gelernt, wie Sie:

    - den wis2box-Workflow durch Hochladen von Daten in MinIO mit dem Befehl `wis2box data ingest` auslösen
    - die von Ihrer wis2box veröffentlichten WIS2-Benachrichtigungen im Grafana-Dashboard und MQTT Explorer anzeigen
    - den Inhalt der veröffentlichten Daten mit der **wis2box-webapp** überprüfen
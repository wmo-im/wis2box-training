---
title: Automatisierung der Dateneingabe
---

# Automatisierung der Dateneingabe

!!! abstract "Lernergebnisse"

    Am Ende dieser praktischen Sitzung werden Sie in der Lage sein:
    
    - zu verstehen, wie die Daten-Plugins Ihres Datensatzes den Workflow zur Dateneingabe bestimmen
    - Daten in wis2box mittels eines Skripts über den MinIO Python-Client einzuspeisen
    - Daten in wis2box durch Zugriff auf MinIO über SFTP einzuspeisen

## Einführung

Der **wis2box-management** Container reagiert auf Ereignisse vom MinIO Speicherdienst, um die Dateneingabe basierend auf den für Ihren Datensatz konfigurierten Daten-Plugins auszulösen. Dies ermöglicht es Ihnen, Daten in den MinIO-Bucket hochzuladen und den wis2box-Workflow zum Veröffentlichen der Daten auf dem WIS2-Broker zu starten.

Die Daten-Plugins definieren die Python-Module, die vom **wis2box-management** Container geladen werden und bestimmen, wie die Daten transformiert und veröffentlicht werden.

Im vorherigen Übungsteil sollten Sie einen Datensatz mit der Vorlage `surface-based-observations/synop` erstellt haben, der die folgenden Daten-Plugins enthielt:

<img alt="Daten-Zuordnungen" src="../../assets/img/wis2box-data-mappings.png" width="800">

Wenn eine Datei in MinIO hochgeladen wird, ordnet wis2box die Datei einem Datensatz zu, wenn der Dateipfad die Datensatz-ID (`metadata_id`) enthält, und es wird bestimmt, welche Daten-Plugins basierend auf der Dateierweiterung und dem in den Datensatz-Zuordnungen definierten Dateimuster verwendet werden.

In den vorherigen Sitzungen haben wir den Workflow zur Dateneingabe durch die Verwendung der wis2box-Befehlszeilenfunktionalität ausgelöst, die Daten im richtigen Pfad in den MinIO-Speicher hochlädt.

Die gleichen Schritte können programmatisch durchgeführt werden, indem Sie jede MinIO- oder S3-Client-Software verwenden, was Ihnen ermöglicht, Ihre Dateneingabe als Teil Ihrer betrieblichen Workflows zu automatisieren.

Alternativ können Sie auch über das SFTP-Protokoll auf MinIO zugreifen, um Daten hochzuladen und den Workflow zur Dateneingabe auszulösen.

## Vorbereitung

Loggen Sie sich in Ihre Studenten-VM ein, indem Sie Ihren SSH-Client (PuTTY oder einen anderen) verwenden.

Stellen Sie sicher, dass wis2box läuft:

```bash
cd ~/wis2box-1.0.0rc1/
python3 wis2box-ctl.py start
python3 wis2box-ctl.py status
```

Stellen Sie sicher, dass MQTT Explorer läuft und mit Ihrer Instanz verbunden ist. Wenn Sie noch von der vorherigen Sitzung verbunden sind, löschen Sie alle vorherigen Nachrichten, die Sie aus der Warteschlange erhalten haben.
Dies kann entweder durch Trennen und erneutes Verbinden oder durch Klicken auf das Mülleimer-Symbol für das gegebene Thema erfolgen.

Stellen Sie sicher, dass Sie einen Webbrowser geöffnet haben mit dem Grafana-Dashboard für Ihre Instanz, indem Sie zu `http://<Ihr-Host>:3000` gehen.

Und stellen Sie sicher, dass Sie einen zweiten Tab offen haben mit der MinIO-Benutzeroberfläche unter `http://<Ihr-Host>:9001`. Denken Sie daran, dass Sie sich mit dem `WIS2BOX_STORAGE_USER` und dem `WIS2BOX_STORAGE_PASSWORD` anmelden müssen, die in Ihrer `wis2box.env`-Datei definiert sind.

## Übung 1: Einrichten eines Python-Skripts zur Dateneingabe in MinIO

In dieser Übung verwenden wir den MinIO Python-Client, um Daten in MinIO zu kopieren.

MinIO bietet einen Python-Client, der wie folgt installiert werden kann:

```bash
pip3 install minio
```

Auf Ihrer Studenten-VM ist das 'minio'-Paket für Python bereits installiert.

Gehen Sie in das Verzeichnis `exercise-materials/data-ingest-exercises`; dieses Verzeichnis enthält ein Beispiel-Skript `copy_file_to_incoming.py`, das den MinIO Python-Client verwendet, um eine Datei in MinIO zu kopieren.

Versuchen Sie, das Skript auszuführen, um die Beispieldatendatei `csv-aws-example.csv` in den `wis2box-incoming`-Bucket in MinIO zu kopieren, wie folgt:

```bash
cd ~/exercise-materials/data-ingest-exercises
python3 copy_file_to_incoming.py csv-aws-example.csv
```

!!! note

    Sie erhalten einen Fehler, da das Skript noch nicht konfiguriert ist, um auf den MinIO-Endpunkt auf Ihrer wis2box zuzugreifen.

Das Skript muss den richtigen Endpunkt kennen, um auf MinIO auf Ihrer wis2box zuzugreifen. Wenn wis2box auf Ihrem Host läuft, ist der MinIO-Endpunkt unter `http://<Ihr-Host>:9000` verfügbar. Das Skript muss auch mit Ihrem Speicherpasswort aktualisiert werden und dem Pfad im MinIO-Bucket, um die Daten zu speichern.

!!! question "Aktualisieren Sie das Skript und speisen Sie die CSV-Daten ein"
    
    Bearbeiten Sie das Skript `copy_file_to_incoming.py`, um die Fehler zu beheben, indem Sie eine der folgenden Methoden verwenden:
    - Von der Befehlszeile: verwenden Sie den Texteditor `nano` oder `vim`, um das Skript zu bearbeiten
    - Mit WinSCP: starten Sie eine neue Verbindung mit dem Dateiprotokoll `SCP` und denselben Anmeldeinformationen wie Ihr SSH-Client. Navigieren Sie zu dem Verzeichnis `exercise-materials/data-ingest-exercises` und bearbeiten Sie `copy_file_to_incoming.py` mit dem integrierten Texteditor
    
    Stellen Sie sicher, dass Sie:

    - den richtigen MinIO-Endpunkt für Ihren Host definieren
    - das richtige Speicherpasswort für Ihre MinIO-Instanz angeben
    - den richtigen Pfad im MinIO-Bucket angeben, um die Daten zu speichern

    Führen Sie das Skript erneut aus, um die Beispieldatendatei `csv-aws-example.csv` in MinIO einzuspeisen:

    ```bash
    python3 copy_file_to_incoming.py csv-aws-example.csv
    ```

    Und stellen Sie sicher, dass die Fehler behoben sind.

Sie können überprüfen, ob die Daten korrekt hochgeladen wurden, indem Sie die MinIO-Benutzeroberfläche überprüfen und sehen, ob die Beispieldaten im richtigen Verzeichnis im `wis2box-incoming`-Bucket verfügbar sind.

Sie können das Grafana-Dashboard verwenden, um den Status des Workflows zur Dateneingabe zu überprüfen.

Schließlich können Sie MQTT Explorer verwenden, um zu überprüfen, ob Benachrichtigungen für die eingegebenen Daten veröffentlicht wurden. Sie sollten sehen, dass die CSV-Daten in das BUFR-Format umgewandelt wurden und dass eine WIS2-Datenbenachrichtigung mit einer "kanonischen" URL veröffentlicht wurde, um den Download der BUFR-Daten zu ermöglichen.

## Übung 2: Eingabe von Binärdaten

Als Nächstes versuchen wir, Binärdaten im BUFR-Format mit dem MinIO Python-Client einzugeben.

wis2box kann Binärdaten im BUFR-Format mit dem Plugin `wis2box.data.bufr4.ObservationDataBUFR` eingeben, das in wis2box enthalten ist.

Dieses Plugin teilt die BUFR-Datei in einzelne BUFR-Nachrichten auf und veröffentlicht jede Nachricht an den MQTT-Broker. Wenn die Station für die entsprechende BUFR-Nachricht nicht in den wis2box-Stationenmetadaten definiert ist, wird die Nachricht nicht veröffentlicht.

Da Sie in der vorherigen Sitzung die Vorlage `surface-based-observations/synop` verwendet haben, enthalten Ihre Daten-Zuordnungen das Plugin `FM-12 data converted to BUFR` für die Datensatz-Zuordnungen. Dieses Plugin lädt das Modul `wis2box.data.synop2bufr.ObservationDataSYNOP2BUFR` zum Eingeben der Daten.

!!! question "Eingabe von Binärdaten im BUFR-Format"

    Führen Sie den folgenden Befehl aus, um die Binärdatendatei `bufr-example.bin` in den `wis2box-incoming`-Bucket in MinIO zu kopieren:

    ```bash
    python3 copy_file_to_incoming.py bufr-example.bin
    ```

Überprüfen Sie das Grafana-Dashboard und MQTT Explorer, um zu sehen, ob die Testdaten erfolgreich eingegangen und veröffentlicht wurden, und wenn Sie Fehler sehen, versuchen Sie, sie zu beheben.

!!! question "Überprüfen Sie die Dateneingabe"

    Wie viele Nachrichten wurden für diese Datenprobe an den MQTT-Broker gesendet?

??? success "Klicken Sie, um die Antwort zu enthüllen"

    Wenn Sie die letzte Datenprobe erfolgreich eingegangen und veröffentlicht haben, sollten Sie 10 neue Benachrichtigungen auf dem wis2box MQTT-Broker erhalten haben. Jede Benachrichtigung entspricht Daten für eine Station zu einem Beobachtungszeitpunkt.

    Das Plugin `wis2box.data.bufr4.ObservationDataBUFR` teilt die BUFR-Datei in einzelne BUFR-Nachrichten auf und veröffentlicht eine Nachricht für jede Station und jeden Beobachtungszeitpunkt.

## Übung 3: Eingabe von SYNOP-Daten im ASCII-Format

In der vorherigen Sitzung haben wir das SYNOP-Formular in der **wis2box-webapp** verwendet, um SYNOP-Daten im ASCII-Format einzugeben. Sie können auch SYNOP-Daten im ASCII-Format eingeben, indem Sie die Daten in MinIO hochladen.

In der vorherigen Sitzung sollten Sie einen Datensatz erstellt haben, der das Plugin 'FM-12 data converted to BUFR' für die Datensatz-Zuordnungen enthielt:

<img alt="Datensatz-Zuordnungen" src="../../assets/img/wis2box-data-mappings.png" width="800">

Dieses Plugin lädt das Modul `wis2box.data.synop2bufr.ObservationDataSYNOP2BUFR` zum Eingeben der Daten.

Versuchen Sie, den MinIO Python-Client zu verwenden, um die Testdaten `synop-202307.txt` und `synop-202308.txt` in Ihre wis2box-Instanz einzugeben.

Beachten Sie, dass die 2 Dateien denselben Inhalt enthalten, aber der Dateiname unterschiedlich ist. Der Dateiname wird verwendet, um das Datum der Datenprobe zu bestimmen.

Das synop2bufr-Plugin stützt sich auf ein Dateimuster, um das Datum aus dem Dateinamen zu extrahieren. Die erste Gruppe im regulären Ausdruck wird verwendet, um das Jahr zu extrahieren, und die zweite Gruppe wird verwendet, um den Monat zu extrahieren.

!!! question "Eingabe von FM-12 SYNOP-Daten im ASCII-Format"

    Gehen Sie zurück zur MinIO-Oberfläche in Ihrem Browser und navigieren Sie zum `wis2box-incoming`-Bucket und zum Pfad, in den Sie die Testdaten im vorherigen Übungsteil hochgeladen haben.
    
    Laden Sie die neuen Dateien im richtigen Pfad im `wis2box-incoming`-Bucket in MinIO hoch, um den Workflow zur Dateneingabe auszulösen.

    Überprüfen Sie das Grafana-Dashboard und MQTT Explorer, um zu sehen, ob die Testdaten erfolgreich eingegangen und veröffentlicht wurden.

    Was ist der Unterschied im `properties.datetime` zwischen den zwei an den MQTT-Broker gesendeten Nachrichten?

??? success "Klicken Sie, um die Antwort zu enthüllen"

    Überprüfen Sie die Eigenschaften der letzten 2 Benachrichtigungen im MQTT Explorer und Sie werden feststellen, dass eine Benachrichtigung hat:

    ```{.copy}
    "properties": {
        "data_id": "wis2/urn:wmo:md:nl-knmi-test:surface-based-observations.synop/WIGOS_0-20000-0-60355_20230703T090000",
        "datetime": "2023-07-03T09:00:00Z",
        ...
    ```

    und die andere Benachrichtigung hat:

    ```{.copy}
    "properties": {
        "data_id": "wis2/urn:wmo:md:nl-knmi-test:surface-based-observations.synop/WIGOS_0-20000-0-60355_20230803T09:00:00Z",
        "datetime": "2023-08-03T09:00:00Z",
        ...
    ```

    Der Dateiname wurde verwendet, um das Jahr und den Monat der Datenprobe zu bestimmen.

## Übung 4: Eingabe von Daten in MinIO über SFTP

Daten können auch über SFTP in MinIO eingegangen werden.

Der MinIO-Dienst, der im wis2box-Stack aktiviert ist, hat SFTP auf Port 8022 aktiviert. Sie können über SFTP auf MinIO zugreifen, indem Sie dieselben Anmeldeinformationen wie für die MinIO-Benutzeroberfläche verwenden. In dieser Übung verwenden wir die Admin-Anmeldeinformationen für den MinIO-Dienst, wie in `wis2box.env` definiert, aber Sie können auch zusätzliche Benutzer in der MinIO-Benutzeroberfläche erstellen.

Um auf MinIO über SFTP zuzugreifen, können Sie jede SFTP-Client-Software verwenden. In dieser Übung verwenden wir WinSCP, das ein kostenloser SFTP-Client für Windows ist.

Mit WinSCP sieht Ihre Verbindung wie folgt aus:

<img alt="winscp-sftp-Verbindung" src="../../assets/img/winscp-sftp-connection.png" width="400">

Für Benutzername und Passwort verwenden Sie die Werte der Umgebungsvariablen `WIS2BOX_STORAGE_USERNAME` und `WIS2BOX_STORAGE_PASSWORD` aus Ihrer `wis2box.env`-Datei. Klicken Sie auf 'speichern', um die Sitzung zu speichern, und dann auf 'login', um sich zu verbinden.

Wenn Sie sich anmelden, sehen Sie den MinIO-Bucket `wis2box-incoming` und `wis2box-public` im Stammverzeichnis. Sie können Daten in den `wis2box-incoming`-Bucket hochladen, um den Workflow zur Dateneingabe auszulösen.

Klicken Sie auf den `wis2box-incoming`-Bucket, um in diesen Bucket zu navigieren, dann klicken Sie mit der rechten Maustaste und wählen *Neu*->*Verzeichnis*, um ein neues Verzeichnis im `wis2box-incoming`-Bucket zu erstellen.

Erstellen Sie das Verzeichnis *not-a-valid-path* und laden Sie die Datei *randomfile.txt* in dieses Verzeichnis hoch (Sie können jede beliebige Datei verwenden).

Überprüfen Sie das Grafana-Dashboard auf Port 3000, um zu sehen, ob der Workflow zur Dateneingabe ausgelöst wurde. Sie sollten sehen:

*ERROR - Pfadvalidierungsfehler: Konnte http://minio:9000/wis2box-incoming/not-a-valid-path/randomfile.txt nicht einem Datensatz zuordnen, der Pfad sollte eines der folgenden enthalten: ...*

Der Fehler zeigt an, dass die Datei in MinIO hochgeladen und der Workflow zur Dateneingabe ausgelöst wurde, aber da der Pfad keinem Datensatz in der wis2box-Instanz entspricht, ist das Daten-Mapping fehlgeschlagen.

Sie können auch `sftp` von der Befehlszeile aus verwenden:

```bash
sftp -P 8022 -oBatchMode=no -o StrictHostKeyChecking=no <mein-Hostname-oder-IP>
```
Melden Sie sich mit den in `wis2box.env` für die Umgebungsvariablen `WIS2BOX_STORAGE_USERNAME` und `WIS2BOX_STORAGE_PASSWORD` definierten Anmeldeinformationen an, navigieren Sie zum `wis2box-incoming`-Bucket und erstellen Sie dann ein Verzeichnis und laden Sie eine Datei wie folgt hoch:

```bash
cd wis2box-incoming
mkdir not-a-valid-path
cd not-a-valid-path
put ~/exercise-materials/data-ingest-exercises/synop.txt .
```

Dies führt zu einem "Pfadvalidierungsfehler" im Grafana-Dashboard, der anzeigt, dass die Datei in MinIO hochgeladen wurde.

Um den sftp-Client zu verlassen, geben Sie `exit` ein.

!!! Frage "Daten in MinIO über SFTP eingeben"

    Versuchen Sie, die Datei `synop.txt` in Ihre wis2box-Instanz über SFTP einzugeben, um den Workflow zur Dateneingabe auszulösen.

    Überprüfen Sie die MinIO-Benutzeroberfläche, um zu sehen, ob die Datei im richtigen Pfad im `wis2box-incoming`-Bucket hochgeladen wurde.
    
    Überprüfen Sie das Grafana-Dashboard, um zu sehen, ob der Workflow zur Dateneingabe ausgelöst wurde oder ob es Fehler gab.

 Um sicherzustellen, dass Ihre Daten korrekt eingegangen sind, stellen Sie sicher, dass die Datei im `wis2box-incoming`-Bucket in einem Verzeichnis hochgeladen wird
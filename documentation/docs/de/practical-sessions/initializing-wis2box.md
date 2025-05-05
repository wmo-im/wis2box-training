---
title: Initialisierung von wis2box
---

# Initialisierung von wis2box

!!! abstract "Lernziele"

    Nach Abschluss dieser praktischen Übung werden Sie in der Lage sein:

    - das Skript `wis2box-create-config.py` zur Erstellung der Erstkonfiguration auszuführen
    - wis2box zu starten und den Status seiner Komponenten zu überprüfen
    - den Inhalt der **wis2box-api** einzusehen
    - auf die **wis2box-webapp** zuzugreifen
    - sich mit MQTT Explorer mit dem lokalen **wis2box-broker** zu verbinden

!!! note

    Die aktuellen Schulungsunterlagen basieren auf wis2box-release 1.0.0.
    
    Siehe [accessing-your-student-vm](accessing-your-student-vm.md) für Anweisungen zum Herunterladen und Installieren des wis2box-Softwarepakets, wenn Sie diese Schulung außerhalb einer lokalen Schulungssitzung durchführen.

## Vorbereitung

Melden Sie sich mit Ihrem Benutzernamen und Passwort an Ihrer zugewiesenen VM an und stellen Sie sicher, dass Sie sich im Verzeichnis `wis2box` befinden:

```bash
cd ~/wis2box
```

## Erstellen der Erstkonfiguration

Die Erstkonfiguration für wis2box erfordert:

- eine Umgebungsdatei `wis2box.env` mit den Konfigurationsparametern
- ein Verzeichnis auf dem Host-System zum Austausch zwischen Host-Maschine und wis2box-Containern, definiert durch die Umgebungsvariable `WIS2BOX_HOST_DATADIR`

Das Skript `wis2box-create-config.py` kann zur Erstellung der Erstkonfiguration Ihrer wis2box verwendet werden.

Es wird Ihnen eine Reihe von Fragen stellen, um Ihre Konfiguration einzurichten.

Sie können die Konfigurationsdateien nach Abschluss des Skripts überprüfen und aktualisieren.

Führen Sie das Skript wie folgt aus:

```bash
python3 wis2box-create-config.py
```

### wis2box-host-data Verzeichnis

Das Skript wird Sie auffordern, das Verzeichnis für die Umgebungsvariable `WIS2BOX_HOST_DATADIR` einzugeben.

Beachten Sie, dass Sie den vollständigen Pfad zu diesem Verzeichnis angeben müssen.

Wenn Ihr Benutzername beispielsweise `username` ist, lautet der vollständige Pfad zum Verzeichnis `/home/username/wis2box-data`:

```{.copy}
username@student-vm-username:~/wis2box$ python3 wis2box-create-config.py
Please enter the directory to be used for WIS2BOX_HOST_DATADIR:
/home/username/wis2box-data
The directory to be used for WIS2BOX_HOST_DATADIR will be set to:
    /home/username/wis2box-data
Is this correct? (y/n/exit)
y
The directory /home/username/wis2box-data has been created.
```

### wis2box URL

Als Nächstes werden Sie aufgefordert, die URL für Ihre wis2box einzugeben. Dies ist die URL, über die Sie auf die wis2box-Webanwendung, API und Benutzeroberfläche zugreifen können.

Bitte verwenden Sie `http://<your-hostname-or-ip>` als URL.

```{.copy}
Please enter the URL of the wis2box:
 For local testing the URL is http://localhost
 To enable remote access, the URL should point to the public IP address or domain name of the server hosting the wis2box.
http://username.wis2.training
The URL of the wis2box will be set to:
  http://username.wis2.training
Is this correct? (y/n/exit)
```

### WEBAPP, STORAGE und BROKER Passwörter

Sie können die Option zur zufälligen Passwortgenerierung nutzen, wenn Sie nach `WIS2BOX_WEBAPP_PASSWORD`, `WIS2BOX_STORAGE_PASSWORD`, `WIS2BOX_BROKER_PASSWORD` gefragt werden, oder eigene definieren.

Machen Sie sich keine Sorgen um das Merken dieser Passwörter, sie werden in der Datei `wis2box.env` in Ihrem wis2box-Verzeichnis gespeichert.

### Überprüfung der `wis2box.env`

Nachdem das Skript abgeschlossen ist, überprüfen Sie den Inhalt der Datei `wis2box.env` in Ihrem aktuellen Verzeichnis:

```bash
cat ~/wis2box/wis2box.env
```

Oder überprüfen Sie den Inhalt der Datei über WinSCP.

!!! question

    Wie lautet der Wert von WISBOX_BASEMAP_URL in der wis2box.env Datei?

??? success "Klicken Sie hier für die Antwort"

    Der Standardwert für WIS2BOX_BASEMAP_URL ist `https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png`.

    Diese URL verweist auf den OpenStreetMap-Tile-Server. Wenn Sie einen anderen Kartenanbieter verwenden möchten, können Sie diese URL ändern.

!!! question 

    Wie lautet der Wert der Umgebungsvariable WIS2BOX_STORAGE_DATA_RETENTION_DAYS in der wis2box.env Datei?

??? success "Klicken Sie hier für die Antwort"

    Der Standardwert für WIS2BOX_STORAGE_DATA_RETENTION_DAYS beträgt 30 Tage. Sie können diesen Wert bei Bedarf ändern.
    
    Der wis2box-management Container führt täglich einen Cronjob aus, um Daten zu entfernen, die älter als die durch WIS2BOX_STORAGE_DATA_RETENTION_DAYS definierte Anzahl von Tagen sind:
    
    ```{.copy}
    0 0 * * * su wis2box -c "wis2box data clean --days=$WIS2BOX_STORAGE_DATA_RETENTION_DAYS"
    ```

!!! note

    Die Datei `wis2box.env` enthält Umgebungsvariablen, die die Konfiguration Ihrer wis2box definieren. Weitere Informationen finden Sie in der [wis2box-documentation](https://docs.wis2box.wis.wmo.int/en/latest/reference/configuration.html).

    Bearbeiten Sie die Datei `wis2box.env` nur, wenn Sie sich der Änderungen sicher sind. Falsche Änderungen können dazu führen, dass Ihre wis2box nicht mehr funktioniert.

    Teilen Sie den Inhalt Ihrer `wis2box.env` Datei nicht mit anderen, da sie vertrauliche Informationen wie Passwörter enthält.

## Starten von wis2box

Stellen Sie sicher, dass Sie sich im Verzeichnis mit den wis2box-Softwarestack-Definitionsdateien befinden:

```{.copy}
cd ~/wis2box
```

Starten Sie wis2box mit folgendem Befehl:

```{.copy}
python3 wis2box-ctl.py start
```

Wenn Sie diesen Befehl zum ersten Mal ausführen, sehen Sie folgende Ausgabe:

```
No docker-compose.images-*.yml files found, creating one
Current version=Undefined, latest version=1.0.0
Would you like to update ? (y/n/exit)
```

Wählen Sie ``y`` und das Skript erstellt die Datei ``docker-compose.images-1.0.0.yml``, lädt die erforderlichen Docker-Images herunter und startet die Dienste.

Das Herunterladen der Images kann je nach Internetverbindung einige Zeit dauern. Dieser Schritt ist nur beim ersten Start von wis2box erforderlich.

Überprüfen Sie den Status mit folgendem Befehl:

```{.copy}
python3 wis2box-ctl.py status
```

Wiederholen Sie diesen Befehl, bis alle Dienste aktiv und laufend sind.

!!! note "wis2box und Docker"
    wis2box läuft als Satz von Docker-Containern, die von docker-compose verwaltet werden.
    
    Die Dienste sind in verschiedenen `docker-compose*.yml` Dateien definiert, die sich im Verzeichnis `~/wis2box/` befinden.
    
    Das Python-Skript `wis2box-ctl.py` wird verwendet, um die zugrunde liegenden Docker Compose-Befehle auszuführen, die die wis2box-Dienste steuern.

    Sie müssen die Details der Docker-Container nicht kennen, um den wis2box-Softwarestack auszuführen, aber Sie können die `docker-compose*.yml` Dateien inspizieren, um zu sehen, wie die Dienste definiert sind. Wenn Sie mehr über Docker erfahren möchten, finden Sie weitere Informationen in der [Docker-Dokumentation](https://docs.docker.com/).

Um sich beim wis2box-management Container anzumelden, verwenden Sie folgenden Befehl:

```{.copy}
python3 wis2box-ctl.py login
```

Im wis2box-management Container können Sie verschiedene Befehle ausführen, um Ihre wis2box zu verwalten, zum Beispiel:

- `wis2box auth add-token --path processes/wis2box` : um ein Autorisierungstoken für den `processes/wis2box` Endpunkt zu erstellen
- `wis2box data clean --days=<number-of-days>` : um Daten zu bereinigen, die älter als eine bestimmte Anzahl von Tagen sind

Um den Container zu verlassen und zur Host-Maschine zurückzukehren, verwenden Sie folgenden Befehl:

```{.copy}
exit
```

Führen Sie folgenden Befehl aus, um die auf Ihrer Host-Maschine laufenden Docker-Container anzuzeigen:

```{.copy}
docker ps
```

Sie sollten folgende Container sehen:

- wis2box-management
- wis2box-api
- wis2box-minio
- wis2box-webapp
- wis2box-auth
- wis2box-ui
- wis2downloader
- elasticsearch
- elasticsearch-exporter
- nginx
- mosquitto
- prometheus
- grafana
- loki

Diese Container sind Teil des wis2box-Softwarestacks und stellen die verschiedenen Dienste bereit, die für den Betrieb der wis2box erforderlich sind.

Führen Sie folgenden Befehl aus, um die Docker-Volumes auf Ihrer Host-Maschine anzuzeigen:

```{.copy}
docker volume ls
```

Sie sollten folgende Volumes sehen:

- wis2box_project_auth-data
- wis2box_project_es-data
- wis2box_project_htpasswd
- wis2box_project_minio-data
- wis2box_project_prometheus-data
- wis2box_project_loki-data
- wis2box_project_mosquitto-config

Sowie einige anonyme Volumes, die von den verschiedenen Containern verwendet werden.

Die Volumes, die mit `wis2box_project_` beginnen, werden verwendet, um persistente Daten für die verschiedenen Dienste im wis2box-Softwarestack zu speichern.

## wis2box API

Die wis2box enthält eine API (Application Programming Interface), die Datenzugriff und Prozesse für interaktive Visualisierung, Datentransformation und Veröffentlichung bereitstellt.

Öffnen Sie einen neuen Tab und navigieren Sie zur Seite `http://YOUR-HOST/oapi`.

<img alt="wis2box-api.png" src="../../assets/img/wis2box-api.png" width="800">

Dies ist die Startseite der wis2box API (läuft über den **wis2box-api** Container).

!!! question
     
     Welche Sammlungen sind derzeit verfügbar?

??? success "Klicken Sie hier für die Antwort"
    
    Um die derzeit über die API verfügbaren Sammlungen anzuzeigen, klicken Sie auf `View the collections in this service`:

    <img alt="wis2box-api-collections.png" src="../../assets/img/wis2box-api-collections.png" width="600">

    Folgende Sammlungen sind derzeit verfügbar:

    - Stationen
    - Datenbenachrichtigungen
    - Discovery-Metadaten


!!! question

    Wie viele Datenbenachrichtigungen wurden veröffentlicht?

??? success "Klicken Sie hier für die Antwort"

    Klicken Sie auf "Data notifications" und dann auf `Browse through the items of "Data Notifications"`. 
    
    Sie werden feststellen, dass die Seite "No items" anzeigt, da noch keine Datenbenachrichtigungen veröffentlicht wurden.

## wis2box webapp

Öffnen Sie einen Webbrowser und besuchen Sie die Seite `http://YOUR-HOST/wis2box-webapp`.

Es erscheint ein Popup, das nach Ihrem Benutzernamen und Passwort fragt. Verwenden Sie den Standardbenutzernamen `wis2box-user` und das in der Datei `wis2box.env` definierte `WIS2BOX_WEBAPP_PASSWORD` und klicken Sie auf "Sign in":

!!! note 

    Überprüfen Sie Ihre wis2box.env auf den Wert Ihres WIS2BOX_WEBAPP_PASSWORD. Sie können folgenden Befehl verwenden, um den Wert dieser Umgebungsvariable zu überprüfen:

    ```{.copy}
    cat ~/wis2box/wis2box.env | grep WIS2BOX_WEBAPP_PASSWORD
    ```

Nach der Anmeldung bewegen Sie Ihre Maus zum Menü auf der linken Seite, um die verfügbaren Optionen in der wis2box-Webanwendung zu sehen:

<img alt="wis2box-webapp-menu.png" src="../../assets/img/wis2box-webapp-menu.png" width="400">

Dies ist die wis2box-Webanwendung, mit der Sie mit Ihrer wis2box interagieren können:

- Datensätze erstellen und verwalten
- Stationsmetadaten aktualisieren/überprüfen
- Manuelle Beobachtungen über FM-12 Synop-Formular hochladen
- Benachrichtigungen überwachen, die auf Ihrem wis2box-broker veröffentlicht werden

Wir werden diese Webanwendung in einer späteren Sitzung verwenden.

## wis2box-broker

Öff
---
title: Initialisierung von wis2box
---

# Initialisierung von wis2box

!!! abstract "Lernergebnisse"

    Am Ende dieser praktischen Sitzung werden Sie in der Lage sein:

    - das Skript `wis2box-create-config.py` auszuführen, um die anfängliche Konfiguration zu erstellen
    - wis2box zu starten und den Status seiner Komponenten zu überprüfen
    - den Inhalt der **wis2box-api** einzusehen
    - auf die **wis2box-webapp** zuzugreifen
    - eine Verbindung zum lokalen **wis2box-broker** mit MQTT Explorer herzustellen

!!! note

    Die aktuellen Schulungsmaterialien basieren auf wis2box-release 1.0.0.
    
    Siehe [accessing-your-student-vm](./accessing-your-student-vm.md) für Anweisungen zum Herunterladen und Installieren des wis2box-Software-Stacks, wenn Sie diese Schulung außerhalb einer lokalen Schulungssitzung durchführen.

## Vorbereitung

Melden Sie sich mit Ihrem Benutzernamen und Passwort an Ihrem zugewiesenen VM an und stellen Sie sicher, dass Sie sich im Verzeichnis `wis2box` befinden:

```bash
cd ~/wis2box
```

## Erstellen der anfänglichen Konfiguration

Die anfängliche Konfiguration für die wis2box erfordert:

- eine Umgebungsdatei `wis2box.env`, die die Konfigurationsparameter enthält
- ein Verzeichnis auf dem Host-Computer, das zwischen dem Host-Computer und den wis2box-Containern geteilt wird, definiert durch die Umgebungsvariable `WIS2BOX_HOST_DATADIR`

Das Skript `wis2box-create-config.py` kann verwendet werden, um die anfängliche Konfiguration Ihrer wis2box zu erstellen.

Es wird Ihnen eine Reihe von Fragen stellen, um Ihre Konfiguration einzurichten.

Sie können die Konfigurationsdateien überprüfen und aktualisieren, nachdem das Skript abgeschlossen ist.

Führen Sie das Skript wie folgt aus:

```bash
python3 wis2box-create-config.py
```

### wis2box-host-data Verzeichnis

Das Skript wird Sie bitten, das Verzeichnis für die Umgebungsvariable `WIS2BOX_HOST_DATADIR` einzugeben.

Beachten Sie, dass Sie den vollständigen Pfad zu diesem Verzeichnis angeben müssen.

Zum Beispiel, wenn Ihr Benutzername `username` ist, ist der vollständige Pfad zum Verzeichnis `/home/username/wis2box-data`:

```{.copy}
username@student-vm-username:~/wis2box$ python3 wis2box-create-config.py
Bitte geben Sie das Verzeichnis an, das für WIS2BOX_HOST_DATADIR verwendet werden soll:
/home/username/wis2box-data
Das Verzeichnis, das für WIS2BOX_HOST_DATADIR verwendet wird, wird auf folgendes festgelegt:
    /home/username/wis2box-data
Ist das korrekt? (y/n/exit)
y
Das Verzeichnis /home/username/wis2box-data wurde erstellt.
```

### wis2box URL

Als Nächstes werden Sie gebeten, die URL für Ihre wis2box einzugeben. Dies ist die URL, die verwendet wird, um auf die wis2box-Webanwendung, API und UI zuzugreifen.

Bitte verwenden Sie `http://<your-hostname-or-ip>` als URL.

```{.copy}
Bitte geben Sie die URL der wis2box ein:
 Für lokale Tests ist die URL http://localhost
 Um den Fernzugriff zu ermöglichen, sollte die URL auf die öffentliche IP-Adresse oder den Domainnamen des Servers zeigen, der die wis2box hostet.
http://username.wis2.training
Die URL der wis2box wird auf folgendes festgelegt:
  http://username.wis2.training
Ist das korrekt? (y/n/exit)
```

### WEBAPP, STORAGE und BROKER Passwörter

Sie können die Option der zufälligen Passwortgenerierung verwenden, wenn Sie nach `WIS2BOX_WEBAPP_PASSWORD`, `WIS2BOX_STORAGE_PASSWORD`, `WIS2BOX_BROKER_PASSWORD` gefragt werden und Ihr eigenes definieren.

Machen Sie sich keine Sorgen, sich diese Passwörter zu merken, sie werden in der Datei `wis2box.env` in Ihrem wis2box-Verzeichnis gespeichert.

### Überprüfung `wis2box.env`

Nachdem das Skript abgeschlossen ist, überprüfen Sie den Inhalt der Datei `wis2box.env` in Ihrem aktuellen Verzeichnis:

```bash
cat ~/wis2box/wis2box.env
```

Oder überprüfen Sie den Inhalt der Datei über WinSCP.

!!! question

    Was ist der Wert von WISBOX_BASEMAP_URL in der Datei wis2box.env?

??? success "Klicken Sie, um die Antwort zu sehen"

    Der Standardwert für WIS2BOX_BASEMAP_URL ist `https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png`.

    Diese URL bezieht sich auf den OpenStreetMap-Tile-Server. Wenn Sie einen anderen Kartenanbieter verwenden möchten, können Sie diese URL ändern, um auf einen anderen Tile-Server zu zeigen.

!!! question 

    Was ist der Wert der Umgebungsvariable WIS2BOX_STORAGE_DATA_RETENTION_DAYS in der Datei wis2box.env?

??? success "Klicken Sie, um die Antwort zu sehen"

    Der Standardwert für WIS2BOX_STORAGE_DATA_RETENTION_DAYS beträgt 30 Tage. Sie können diesen Wert ändern, wenn Sie eine andere Anzahl von Tagen wünschen.
    
    Der wis2box-management-Container führt täglich einen Cronjob aus, um Daten, die älter als die durch WIS2BOX_STORAGE_DATA_RETENTION_DAYS definierte Anzahl von Tagen sind, aus dem `wis2box-public`-Bucket und dem API-Backend zu entfernen:
    
    ```{.copy}
    0 0 * * * su wis2box -c "wis2box data clean --days=$WIS2BOX_STORAGE_DATA_RETENTION_DAYS"
    ```

!!! note

    Die Datei `wis2box.env` enthält Umgebungsvariablen, die die Konfiguration Ihrer wis2box definieren. Für weitere Informationen konsultieren Sie die [wis2box-Dokumentation](https://docs.wis2box.wis.wmo.int/en/latest/reference/configuration.html).

    Bearbeiten Sie die Datei `wis2box.env` nicht, es sei denn, Sie sind sicher über die Änderungen, die Sie vornehmen. Falsche Änderungen können dazu führen, dass Ihre wis2box nicht mehr funktioniert.

    Teilen Sie den Inhalt Ihrer `wis2box.env`-Datei nicht mit anderen, da sie sensible Informationen wie Passwörter enthält.

## Starten von wis2box

Stellen Sie sicher, dass Sie sich im Verzeichnis befinden, das die Definitionsdateien des wis2box-Software-Stacks enthält:

```{.copy}
cd ~/wis2box
```

Starten Sie wis2box mit dem folgenden Befehl:

```{.copy}
python3 wis2box-ctl.py start
```

Wenn Sie diesen Befehl zum ersten Mal ausführen, sehen Sie die folgende Ausgabe:

```
Keine docker-compose.images-*.yml Dateien gefunden, eine wird erstellt
Aktuelle Version=Undefined, neueste Version=1.0.0
Möchten Sie aktualisieren? (y/n/exit)
```

Wählen Sie ``y`` und das Skript wird die Datei ``docker-compose.images-1.0.0.yml`` erstellen, die erforderlichen Docker-Images herunterladen und die Dienste starten.

Das Herunterladen der Bilder kann je nach Ihrer Internetgeschwindigkeit einige Zeit in Anspruch nehmen. Dieser Schritt ist nur beim ersten Start von wis2box erforderlich.

Überprüfen Sie den Status mit dem folgenden Befehl:

```{.copy}
python3 wis2box-ctl.py status
```

Wiederholen Sie diesen Befehl, bis alle Dienste aktiv und laufend sind.

!!! note "wis2box und Docker"
    wis2box wird als eine Reihe von Docker-Containern ausgeführt, die von docker-compose verwaltet werden.
    
    Die Dienste sind in den verschiedenen `docker-compose*.yml` definiert, die im Verzeichnis `~/wis2box/` zu finden sind.
    
    Das Python-Skript `wis2box-ctl.py` wird verwendet, um die zugrundeliegenden Docker Compose-Befehle auszuführen, die die wis2box-Dienste steuern.

    Sie müssen die Details der Docker-Container nicht kennen, um den wis2box-Software-Stack auszuführen, aber Sie können die `docker-compose*.yml`-Dateien und Dateien inspizieren, um zu sehen, wie die Dienste definiert sind. Wenn Sie mehr über Docker erfahren möchten, finden Sie weitere Informationen in der [Docker-Dokumentation](https://docs.docker.com/).

Um sich beim wis2box-management-Container anzumelden, verwenden Sie den folgenden Befehl:

```{.copy}
python3 wis2box-ctl.py login
```

Im wis2box-management-Container können Sie verschiedene Befehle ausführen, um Ihre wis2box zu verwalten, wie zum Beispiel:

- `wis2box auth add-token --path processes/wis2box` : um ein Autorisierungstoken für den Endpunkt `processes/wis2box` zu erstellen
- `wis2box data clean --days=<number-of-days>` : um Daten, die älter als eine bestimmte Anzahl von Tagen sind, aus dem `wis2box-public`-Bucket zu bereinigen

Um den Container zu verlassen und zum Host-Computer zurückzukehren, verwenden Sie den folgenden Befehl:

```{.copy}
exit
```

Führen Sie den folgenden Befehl aus, um die Docker-Container zu sehen, die auf Ihrem Host-Computer laufen:

```{.copy}
docker ps
```

Sie sollten die folgenden Container laufen sehen:

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

Diese Container sind Teil des wis2box-Software-Stacks und bieten die verschiedenen Dienste, die erforderlich sind, um die wis2box zu betreiben.

Führen Sie den folgenden Befehl aus, um die Docker-Volumes auf Ihrem Host-Computer zu sehen:

```{.copy}
docker volume ls
```

Sie sollten die folgenden Volumes sehen:

- wis2box_project_auth-data
- wis2box_project_es-data
- wis2box_project_htpasswd
- wis2box_project_minio-data
- wis2box_project_prometheus-data
- wis2box_project_loki-data
- wis2box_project_mosquitto-config

Sowie einige anonyme Volumes, die von den verschiedenen Containern verwendet werden.

Die Volumes, die mit `wis2box_project_` beginnen, werden verwendet, um persistente Daten für die verschiedenen Dienste im wis2box-Software-Stack zu speichern.

## wis2box API

Die wis2box enthält eine API (Application Programming Interface), die Datenzugriff und Prozesse für interaktive Visualisierung, Datentransformation und Veröffentlichung bietet.

Öffnen Sie einen neuen Tab und navigieren Sie zur Seite `http://YOUR-HOST/oapi`.

<img alt="wis2box-api.png" src="/../assets/img/wis2box-api.png" width="800">

Dies ist die Startseite der wis2box API (betrieben über den **wis2box-api**-Container).

!!! question
     
     Welche Sammlungen sind derzeit verfügbar?

??? success "Klicken Sie, um die Antwort zu sehen"
    
    Um die derzeit über die API verfügbaren Sammlungen einzusehen, klicken Sie auf `View the collections in this service`:

    <img alt="wis2box-api-collections.png" src="/../assets/img/wis2box-api-collections.png" width="600">

    Die folgenden Sammlungen sind derzeit verfügbar:

    - Stationen
    - Datenbenachrichtigungen
    - Entdeckungsmetadaten


!!! question

    Wie viele Datenbenachrichtigungen wurden veröffentlicht?

??? success "Klicken Sie, um die Antwort zu sehen"

    Klicken Sie auf "Datenbenachrichtigungen", dann klicken Sie auf `Browse through the items of "Data Notifications"`. 
    
    Sie werden feststellen, dass die Seite "Keine Elemente" sagt, da noch keine Datenbenachrichtigungen veröffentlicht wurden.

## wis2box webapp

Öffnen Sie einen Webbrowser und besuchen Sie die Seite `http://YOUR-HOST/wis2box-webapp`.

Es erscheint ein Pop-up, das nach Ihrem Benutzernamen und Passwort fragt. Verwenden Sie den Standardbenutzernamen `wis2box-user` und das `WIS2BOX_WEBAPP_PASSWORD`, das in der Datei `wis2box.env` definiert ist, und klicken Sie auf "Anmelden":

!!! note 

    Überprüfen Sie Ihre wis2box.env auf den Wert Ihres WIS2BOX_WEBAPP_PASSWORD. Sie können den folgenden Befehl verwenden, um den Wert dieser Umgebungsvariablen zu überprüfen:

    ```{.copy}
    cat ~/wis2box/wis2box.env | grep WIS2BOX_WEBAPP_PASSWORD
    ```

Nachdem Sie sich angemeldet haben, bewegen Sie Ihre Maus zum Menü auf der linken Seite, um die verfügbaren Optionen in der wis2box-Webanwendung zu sehen:

<img alt="wis2box-webapp-menu.png" src="/../assets/img/wis2box-webapp-menu.png" width="400">

Dies ist die wis2box-Webanwendung, die es Ihnen ermöglicht, mit Ihrer wis2box zu interagieren:

- Erstellen und Verwalten von Datensätzen
- Aktualisieren/Überprüfen Ihrer Stationsmetadaten
- Hochladen manueller Beobachtungen mit dem FM-12-Synop-Formular
- Überwachen von Benachrichtigungen, die auf Ihrem wis2box-broker veröffentlicht wurden

Wir werden diese Webanwendung in einer späteren Sitzung verwenden.

## wis2box-broker

Öffnen Sie den MQTT Explorer auf Ihrem Computer und bereiten Sie eine neue Verbindung vor, um sich mit Ihrem Broker (betrieben über den **wis2box-broker**-Container) zu verbinden.

Klicken Sie auf `+`, um eine neue Verbindung hinzuzufügen:

<img alt="mqtt-explorer-new-connection.png" src="/../assets/img/mqtt-explorer-new-connection.png" width="300">

Sie können auf die Schaltfläche 'ADVANCED' klicken und überprüfen, ob Sie Abonnements für die folgenden Themen haben:

- `#`
- `$SYS/#`

<img alt="mqtt-explorer-topics.png" src="/../assets/img/mqtt-explorer-topics.png" width="550">

!!! note

    Das Thema `#` ist ein Platzhalter-Abonnement, das alle Themen abonniert, die auf dem Broker veröffentlicht werden.

    Die unter dem Thema `$SYS` veröffentlichten Nachrichten sind Systemnachrichten, die vom Mosquitto-Dienst selbst veröffentlicht werden.

Verwenden Sie die folgenden Verbindungsdetails und ersetzen Sie den Wert von `<your-host>` durch Ihren Hostnamen und `<WIS2BOX_BROKER_PASSWORD>` durch den Wert aus Ihrer `wis2box.env`-Datei:

- **Protokoll: mqtt://**
- **Host: `<your-host>`**
- **Port: 1883**
- **Benutzername: wis2box**
- **Passwort: `<WIS2BOX_BROKER_PASSWORD>`**

!!! note 

    Sie können Ihre wis2box.env überprüfen, um den Wert Ihres WIS2BOX_BROKER_PASSWORD zu sehen. Sie können den folgenden Befehl verwenden, um den Wert dieser Umgebungsvariablen zu überprüfen:

    ```{.copy}
    cat ~/wis2box/wis2box.env | grep WIS2BOX_BROKER_PASSWORD
    ```

    Beachten Sie, dass dies Ihr **interner** Broker-Passwort ist, der Global Broker wird unterschiedliche (nur lesbare) Anmeldeinformationen verwenden, um sich bei Ihrem Broker zu abonnieren. Teilen Sie dieses Passwort niemals mit jemandem.

Stellen Sie sicher, dass Sie auf "SPEICHERN" klicken, um Ihre Verbindungsdetails zu speichern.

Klicken Sie dann auf "VERBINDEN", um sich mit Ihrem **wis2box-broker** zu verbinden.

<img alt="mqtt-explorer-wis2box-broker.png" src="/../assets/img/mqtt-explorer-wis2box-broker.png" width="600">

Sobald Sie verbunden sind, überprüfen Sie, ob die internen Mosquitto-Statistiken von Ihrem Broker unter dem `$SYS` Thema veröffentlicht werden:

<img alt="mqtt-explorer-sys-topic.png" src="/../assets/img/mqtt-explorer-sys-topic.png" width="400">

Halten Sie den MQTT Explorer geöffnet, da wir ihn verwenden werden, um die Nachrichten zu überwachen, die auf dem Broker veröffentlicht werden.

## Schlussfolgerung

!!! success "Herzlichen Glückwunsch!"
    In dieser praktischen Sitzung haben Sie gelernt, wie Sie:

    - das Skript `wis2box-create-config.py` ausführen, um die anfängliche Konfiguration zu erstellen
    - wis2box starten und den Status seiner Komponenten überprüfen
    - auf die wis2box-webapp und wis2box-API in einem Browser zugreifen
    - sich mit dem MQTT-Broker auf Ihrer Studenten-VM mit MQTT Explorer verbinden
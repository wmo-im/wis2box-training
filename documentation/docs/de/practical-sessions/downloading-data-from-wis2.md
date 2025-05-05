---
title: Herunterladen und Dekodieren von Daten aus WIS2
---

# Herunterladen und Dekodieren von Daten aus WIS2

!!! abstract "Lernziele!"

    Nach Abschluss dieser praktischen Einheit werden Sie in der Lage sein:

    - den "wis2downloader" zu verwenden, um WIS2-Datenbenachrichtigungen zu abonnieren und Daten auf Ihr lokales System herunterzuladen
    - den Status der Downloads im Grafana-Dashboard zu überwachen
    - heruntergeladene Daten mithilfe des "decode-bufr-jupyter"-Containers zu dekodieren

## Einführung

In dieser Einheit lernen Sie, wie Sie ein Abonnement bei einem WIS2 Broker einrichten und automatisch Daten mit dem in wis2box enthaltenen "wis2downloader"-Dienst auf Ihr lokales System herunterladen können.

!!! note "Über wis2downloader"
     
     Der wis2downloader ist auch als eigenständiger Dienst verfügbar und kann auf einem anderen System ausgeführt werden als dem, das die WIS2-Benachrichtigungen veröffentlicht. Weitere Informationen zur Verwendung des wis2downloader als eigenständigen Dienst finden Sie unter [wis2downloader](https://pypi.org/project/wis2downloader/).

     Wenn Sie Ihren eigenen Dienst zum Abonnieren von WIS2-Benachrichtigungen und Herunterladen von Daten entwickeln möchten, können Sie den [wis2downloader source code](https://github.com/World-Meteorological-Organization/wis2downloader) als Referenz verwenden.

!!! Weitere Werkzeuge für den Zugriff auf WIS2-Daten

    Die folgenden Werkzeuge können ebenfalls verwendet werden, um Daten aus WIS2 zu finden und darauf zuzugreifen:

    - [pywiscat](https://github.com/wmo-im/pywiscat) bietet Suchfunktionen für den WIS2 Global Discovery Catalogue zur Unterstützung der Berichterstattung und Analyse des WIS2-Katalogs und seiner zugehörigen Metadaten
    - [pywis-pubsub](https://github.com/World-Meteorological-Organization/pywis-pubsub) ermöglicht das Abonnieren und Herunterladen von WMO-Daten aus WIS2-Infrastrukturdiensten

## Vorbereitung

Bitte melden Sie sich vor dem Start an Ihrer Student-VM an und stellen Sie sicher, dass Ihre wis2box-Instanz läuft.

## Anzeigen des wis2downloader-Dashboards in Grafana

Öffnen Sie einen Webbrowser und navigieren Sie zum Grafana-Dashboard Ihrer wis2box-Instanz unter `http://YOUR-HOST:3000`.

Klicken Sie im linken Menü auf Dashboards und wählen Sie dann das **wis2downloader dashboard**.

Sie sollten folgendes Dashboard sehen:

![wis2downloader dashboard](../assets/img/wis2downloader-dashboard.png)

Dieses Dashboard basiert auf Metriken, die vom wis2downloader-Dienst veröffentlicht werden, und zeigt Ihnen den Status der aktuell laufenden Downloads an.

In der oberen linken Ecke sehen Sie die derzeit aktiven Abonnements.

Lassen Sie dieses Dashboard geöffnet, da Sie es in der nächsten Übung zur Überwachung des Download-Fortschritts verwenden werden.

## Überprüfen der wis2downloader-Konfiguration

Der vom wis2box-Stack gestartete wis2downloader-Dienst kann über die Umgebungsvariablen in Ihrer wis2box.env-Datei konfiguriert werden.

Die folgenden Umgebungsvariablen werden vom wis2downloader verwendet:

    - DOWNLOAD_BROKER_HOST: Der Hostname des MQTT-Brokers, mit dem eine Verbindung hergestellt werden soll. Standardmäßig globalbroker.meteo.fr
    - DOWNLOAD_BROKER_PORT: Der Port des MQTT-Brokers, mit dem eine Verbindung hergestellt werden soll. Standardmäßig 443 (HTTPS für Websockets)
    - DOWNLOAD_BROKER_USERNAME: Der Benutzername für die Verbindung zum MQTT-Broker. Standardmäßig everyone
    - DOWNLOAD_BROKER_PASSWORD: Das Passwort für die Verbindung zum MQTT-Broker. Standardmäßig everyone
    - DOWNLOAD_BROKER_TRANSPORT: websockets oder tcp, der zu verwendende Transport-Mechanismus für die Verbindung zum MQTT-Broker. Standardmäßig websockets
    - DOWNLOAD_RETENTION_PERIOD_HOURS: Die Aufbewahrungsdauer der heruntergeladenen Daten in Stunden. Standardmäßig 24
    - DOWNLOAD_WORKERS: Die Anzahl der zu verwendenden Download-Worker. Standardmäßig 8. Bestimmt die Anzahl der parallelen Downloads
    - DOWNLOAD_MIN_FREE_SPACE_GB: Der minimale freie Speicherplatz in GB, der auf dem Volume mit den Downloads verfügbar sein muss. Standardmäßig 1

Um die aktuelle Konfiguration des wis2downloader zu überprüfen, können Sie folgenden Befehl verwenden:

```bash
cat ~/wis2box/wis2box.env | grep DOWNLOAD
```

!!! question "Überprüfen Sie die Konfiguration des wis2downloader"
    
    Welcher MQTT-Broker wird standardmäßig vom wis2downloader verwendet?

    Wie lange ist die standardmäßige Aufbewahrungsdauer für die heruntergeladenen Daten?

??? success "Klicken Sie hier für die Antwort"

    Der standardmäßige MQTT-Broker, mit dem sich der wis2downloader verbindet, ist `globalbroker.meteo.fr`.

    Die standardmäßige Aufbewahrungsdauer für die heruntergeladenen Daten beträgt 24 Stunden.

!!! note "Aktualisieren der wis2downloader-Konfiguration"

    Um die Konfiguration des wis2downloader zu aktualisieren, können Sie die wis2box.env-Datei bearbeiten. Um die Änderungen zu übernehmen, führen Sie den Startbefehl für den wis2box-Stack erneut aus:

    ```bash
    python3 wis2box-ctl.py start
    ```

    Der wis2downloader-Dienst wird dann mit der neuen Konfiguration neu gestartet.

Für diese Übung können Sie die Standardkonfiguration beibehalten.

## Hinzufügen von Abonnements zum wis2downloader

Im **wis2downloader**-Container können Sie über die Kommandozeile Abonnements auflisten, hinzufügen und löschen.

Um sich am **wis2downloader**-Container anzumelden, verwenden Sie folgenden Befehl:

```bash
python3 wis2box-ctl.py login wis2downloader
```

Verwenden Sie dann den folgenden Befehl, um die derzeit aktiven Abonnements aufzulisten:

```bash
wis2downloader list-subscriptions
```

Dieser Befehl gibt eine leere Liste zurück, da derzeit keine Abonnements aktiv sind.

Für diese Übung abonnieren wir das Thema `cache/a/wis2/de-dwd-gts-to-wis2/#`, um Daten zu abonnieren, die vom DWD-gehosteten GTS-to-WIS2-Gateway veröffentlicht werden, und laden Benachrichtigungen aus dem Global Cache herunter.

Um dieses Abonnement hinzuzufügen, verwenden Sie den folgenden Befehl:

```bash
wis2downloader add-subscription --topic cache/a/wis2/de-dwd-gts-to-wis2/#
```

Verlassen Sie dann den **wis2downloader**-Container durch Eingabe von `exit`:

```bash
exit
```

Überprüfen Sie das wis2downloader-Dashboard in Grafana, um das neue Abonnement zu sehen. Warten Sie einige Minuten, und Sie sollten sehen, wie die ersten Downloads beginnen. Gehen Sie zur nächsten Übung, sobald Sie bestätigt haben, dass die Downloads beginnen.

## Anzeigen der heruntergeladenen Daten

Der wis2downloader-Dienst im wis2box-Stack lädt die Daten in das Verzeichnis 'downloads' in dem Verzeichnis herunter, das Sie als WIS2BOX_HOST_DATADIR in Ihrer wis2box.env-Datei definiert haben. Um den Inhalt des Downloads-Verzeichnisses anzuzeigen, können Sie folgenden Befehl verwenden:

```bash
ls -R ~/wis2box-data/downloads
```

Beachten Sie, dass die heruntergeladenen Daten in Verzeichnissen gespeichert werden, die nach dem Thema benannt sind, unter dem die WIS2-Benachrichtigung veröffentlicht wurde.

## Entfernen von Abonnements aus dem wis2downloader

Melden Sie sich nun erneut am wis2downloader-Container an:

```bash
python3 wis2box-ctl.py login wis2downloader
```

und entfernen Sie das von Ihnen erstellte Abonnement aus dem wis2downloader mit folgendem Befehl:

```bash
wis2downloader remove-subscription --topic cache/a/wis2/de-dwd-gts-to-wis2/#
```

Verlassen Sie den wis2downloader-Container durch Eingabe von `exit`:
    
```bash
exit
```

Überprüfen Sie das wis2downloader-Dashboard in Grafana, um zu sehen, dass das Abonnement entfernt wurde. Sie sollten sehen, dass die Downloads stoppen.

## Herunterladen und Dekodieren von Daten für eine tropische Zyklonspur

In dieser Übung abonnieren Sie den WIS2 Training Broker, der Beispieldaten für Schulungszwecke veröffentlicht. Sie richten ein Abonnement ein, um Daten für eine tropische Zyklonspur herunterzuladen. Anschließend dekodieren Sie die heruntergeladenen Daten mit dem "decode-bufr-jupyter"-Container.

### Abonnieren des wis2training-brokers und Einrichten eines neuen Abonnements

Dies zeigt, wie man einen Broker abonniert, der nicht der Standard-Broker ist, und ermöglicht es Ihnen, einige vom WIS2 Training Broker veröffentlichte Daten herunterzuladen.

Bearbeiten Sie die wis2box.env-Datei und ändern Sie DOWNLOAD_BROKER_HOST zu `wis2training-broker.wis2dev.io`, DOWNLOAD_BROKER_PORT zu `1883` und DOWNLOAD_BROKER_TRANSPORT zu `tcp`:

```copy
# downloader settings
DOWNLOAD_BROKER_HOST=wis2training-broker.wis2dev.io
DOWNLOAD_BROKER_PORT=1883
DOWNLOAD_BROKER_USERNAME=everyone
DOWNLOAD_BROKER_PASSWORD=everyone
# download transport mechanism (tcp or websockets)
DOWNLOAD_BROKER_TRANSPORT=tcp
```

Führen Sie dann den 'start'-Befehl erneut aus, um die Änderungen zu übernehmen:

```bash
python3 wis2box-ctl.py start
```

Überprüfen Sie die Logs des wis2downloader, um zu sehen, ob die Verbindung zum neuen Broker erfolgreich war:

```bash
docker logs wis2downloader
```

Sie sollten folgende Protokollmeldung sehen:

```copy
...
INFO - Connecting...
INFO - Host: wis2training-broker.wis2dev.io, port: 1883
INFO - Connected successfully
```

Jetzt richten wir ein neues Abonnement für das Thema ein, um Zyklon-Spurdaten vom WIS2 Training Broker herunterzuladen.

Melden Sie sich am **wis2downloader**-Container an:

```bash
python3 wis2box-ctl.py login wis2downloader
```

Und führen Sie den folgenden Befehl aus (kopieren Sie diesen, um Tippfehler zu vermeiden):

```bash
wis2downloader add-subscription --topic origin/a/wis2/int-wis2-training/data/core/weather/prediction/forecast/medium-range/probabilistic/trajectory
```

Verlassen Sie den **wis2downloader**-Container durch Eingabe von `exit`.

Warten Sie, bis Sie im wis2downloader-Dashboard in Grafana sehen, dass die Downloads beginnen.

!!! note "Herunterladen von Daten vom WIS2 Training Broker"

    Der WIS2 Training Broker ist ein Testbroker, der für Schulungszwecke verwendet wird und möglicherweise nicht ständig Daten veröffentlicht.

    Während der Präsenzschulungen wird der lokale Trainer sicherstellen, dass der WIS2 Training Broker Daten zum Herunterladen veröffentlicht.

    Wenn Sie diese Übung außerhalb einer Schulung durchführen, sehen Sie möglicherweise keine heruntergeladenen Daten.

Überprüfen Sie, ob die Daten heruntergeladen wurden, indem Sie die wis2downloader-Logs erneut überprüfen:

```bash
docker logs wis2downloader
```

Sie sollten eine Protokollmeldung ähnlich der folgenden sehen:

```copy
[...] INFO - Message received under topic origin/a/wis2/int-wis2-training/data/core/weather/prediction/forecast/medium-range/probabilistic/trajectory
[...] INFO - Downloaded A_JSXX05ECEP020000_C_ECMP_...
```

### Dekodieren heruntergeladener Daten

Um zu demonstrieren, wie Sie die heruntergeladenen Daten dekodieren können, starten wir einen neuen Container mit dem 'decode-bufr-jupyter'-Image.

Dieser Container startet einen Jupyter Notebook Server auf Ihrer Instanz, der die "ecCodes"-Bibliothek enthält, mit der Sie BUFR-Daten dekodieren können.

Wir verwenden die Beispiel-Notebooks in `~/exercise-materials/notebook-examples`, um die heruntergeladenen Daten für die Zyklonspuren zu dekodieren.

Um den Container zu starten, verwenden Sie den folgenden Befehl:

```bash
docker run -d --name decode-bufr-jupyter \
    -v ~/wis2box-data/downloads:/root/downloads \
    -p 8888:8888 \
    -e JUPYTER_TOKEN=dataismagic! \
    mlimper/decode-bufr-jupyter
```

!!! note "Über den decode-bufr-jupyter Container"

    Der `decode-bufr-jupyter`-Container ist ein spezieller Container, der die ecCodes-Bibli
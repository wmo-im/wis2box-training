---
title: Herunterladen und Dekodieren von Daten aus WIS2
---

# Herunterladen und Dekodieren von Daten aus WIS2

!!! abstract "Lernergebnisse!"

    Am Ende dieser praktischen Sitzung werden Sie in der Lage sein:

    - den "wis2downloader" zu verwenden, um WIS2-Datenbenachrichtigungen zu abonnieren und Daten auf Ihr lokales System herunterzuladen
    - den Status der Downloads im Grafana-Dashboard anzuzeigen
    - einige heruntergeladene Daten mit dem "decode-bufr-jupyter" Container zu dekodieren

## Einführung

In dieser Sitzung lernen Sie, wie Sie ein Abonnement für einen WIS2 Broker einrichten und automatisch Daten auf Ihr lokales System herunterladen, indem Sie den "wis2downloader"-Dienst verwenden, der in wis2box enthalten ist.

!!! note "Über wis2downloader"
     
     Der wis2downloader ist auch als eigenständiger Dienst verfügbar, der auf einem anderen System als dem, das die WIS2-Benachrichtigungen veröffentlicht, ausgeführt werden kann. Siehe [wis2downloader](https://pypi.org/project/wis2downloader/) für weitere Informationen zur Verwendung des wis2downloader als eigenständigen Dienst.

     Wenn Sie Ihren eigenen Dienst zum Abonnieren von WIS2-Benachrichtigungen und Herunterladen von Daten entwickeln möchten, können Sie den [wis2downloader Quellcode](https://github.com/World-Meteorological-Organization/wis2downloader) als Referenz verwenden.

!!! Andere Werkzeuge für den Zugriff auf WIS2-Daten

    Die folgenden Werkzeuge können ebenfalls verwendet werden, um Daten aus WIS2 zu entdecken und darauf zuzugreifen:

    - [pywiscat](https://github.com/wmo-im/pywiscat) bietet Suchfunktionen auf dem WIS2 Global Discovery Catalogue zur Unterstützung der Berichterstattung und Analyse des WIS2-Katalogs und seiner zugehörigen Entdeckungsmetadaten
    - [pywis-pubsub](https://github.com/World-Meteorological-Organization/pywis-pubsub) bietet Abonnement- und Download-Fähigkeiten für WMO-Daten aus WIS2-Infrastrukturdiensten

## Vorbereitung

Bitte loggen Sie sich vor Beginn in Ihre Studenten-VM ein und stellen Sie sicher, dass Ihre wis2box-Instanz läuft.

## Anzeigen des wis2downloader-Dashboards in Grafana

Öffnen Sie einen Webbrowser und navigieren Sie zum Grafana-Dashboard Ihrer wis2box-Instanz, indem Sie `http://YOUR-HOST:3000` aufrufen.

Klicken Sie im linken Menü auf Dashboards und dann auf das **wis2downloader Dashboard**.

Sie sollten folgendes Dashboard sehen:

![wis2downloader dashboard](../assets/img/wis2downloader-dashboard.png)

Dieses Dashboard basiert auf Metriken, die vom wis2downloader-Dienst veröffentlicht werden, und zeigt Ihnen den Status der derzeit laufenden Downloads.

In der oberen linken Ecke können Sie die derzeit aktiven Abonnements sehen.

Halten Sie dieses Dashboard offen, da Sie es verwenden werden, um den Fortschritt des Downloads im nächsten Übungsteil zu überwachen.

## Überprüfung der wis2downloader-Konfiguration

Der wis2downloader-Dienst, der vom wis2box-Stack gestartet wurde, kann mit den Umgebungsvariablen konfiguriert werden, die in Ihrer wis2box.env-Datei definiert sind.

Die folgenden Umgebungsvariablen werden vom wis2downloader verwendet:

    - DOWNLOAD_BROKER_HOST: Der Hostname des MQTT-Brokers, mit dem eine Verbindung hergestellt werden soll. Standardmäßig globalbroker.meteo.fr
    - DOWNLOAD_BROKER_PORT: Der Port des MQTT-Brokers, mit dem eine Verbindung hergestellt werden soll. Standardmäßig 443 (HTTPS für Websockets)
    - DOWNLOAD_BROKER_USERNAME: Der Benutzername, der verwendet werden soll, um eine Verbindung zum MQTT-Broker herzustellen. Standardmäßig everyone
    - DOWNLOAD_BROKER_PASSWORD: Das Passwort, das verwendet werden soll, um eine Verbindung zum MQTT-Broker herzustellen. Standardmäßig everyone
    - DOWNLOAD_BROKER_TRANSPORT: Websockets oder tcp, der Transportmechanismus, der verwendet werden soll, um eine Verbindung zum MQTT-Broker herzustellen. Standardmäßig websockets,
    - DOWNLOAD_RETENTION_PERIOD_HOURS: Die Aufbewahrungszeit in Stunden für die heruntergeladenen Daten. Standardmäßig 24
    - DOWNLOAD_WORKERS: Die Anzahl der Download-Arbeiter, die verwendet werden sollen. Standardmäßig 8. Bestimmt die Anzahl der parallelen Downloads.
    - DOWNLOAD_MIN_FREE_SPACE_GB: Der minimale freie Speicherplatz in GB, der auf dem Volume, das die Downloads hostet, freigehalten werden soll. Standardmäßig 1.

Um die aktuelle Konfiguration des wis2downloader zu überprüfen, können Sie den folgenden Befehl verwenden:

```bash
cat ~/wis2box/wis2box.env | grep DOWNLOAD
```

!!! question "Überprüfen Sie die Konfiguration des wis2downloader"
    
    Was ist der Standard-MQTT-Broker, mit dem sich der wis2downloader verbindet?

    Was ist die Standard-Aufbewahrungszeit für die heruntergeladenen Daten?

??? success "Klicken Sie, um die Antwort zu enthüllen"

    Der Standard-MQTT-Broker, mit dem sich der wis2downloader verbindet, ist `globalbroker.meteo.fr`.

    Die Standard-Aufbewahrungszeit für die heruntergeladenen Daten beträgt 24 Stunden.

!!! note "Aktualisieren der Konfiguration des wis2downloader"

    Um die Konfiguration des wis2downloader zu aktualisieren, können Sie die Datei wis2box.env bearbeiten. Um die Änderungen anzuwenden, können Sie den Startbefehl für den wis2box-Stack erneut ausführen:

    ```bash
    python3 wis2box-ctl.py start
    ```

    Und Sie werden sehen, dass der wis2downloader-Dienst mit der neuen Konfiguration neu gestartet wird.

Sie können die Standardkonfiguration für den Zweck dieser Übung beibehalten.

## Hinzufügen von Abonnements zum wis2downloader

Im **wis2downloader** Container können Sie die Befehlszeile verwenden, um Abonnements aufzulisten, hinzuzufügen und zu löschen.

Um sich beim **wis2downloader** Container anzumelden, verwenden Sie den folgenden Befehl:

```bash
python3 wis2box-ctl.py login wis2downloader
```

Verwenden Sie dann den folgenden Befehl, um die derzeit aktiven Abonnements aufzulisten:

```bash
wis2downloader list-subscriptions
```

Dieser Befehl gibt eine leere Liste zurück, da derzeit keine Abonnements aktiv sind.

Für den Zweck dieser Übung werden wir das folgende Thema abonnieren `cache/a/wis2/de-dwd-gts-to-wis2/#`, um Daten zu abonnieren, die vom DWD-gehosteten GTS-to-WIS2-Gateway veröffentlicht werden, und Download-Benachrichtigungen aus dem Global Cache.

Um dieses Abonnement hinzuzufügen, verwenden Sie den folgenden Befehl:

```bash
wis2downloader add-subscription --topic cache/a/wis2/de-dwd-gts-to-wis2/#
```

Verlassen Sie dann den **wis2downloader** Container, indem Sie `exit` eingeben:

```bash
exit
```

Überprüfen Sie das wis2downloader-Dashboard in Grafana, um das neue Abonnement hinzugefügt zu sehen. Warten Sie einige Minuten und Sie sollten sehen, dass die ersten Downloads beginnen. Gehen Sie zur nächsten Übung, sobald Sie bestätigt haben, dass die Downloads beginnen.

## Anzeigen der heruntergeladenen Daten

Der wis2downloader-Dienst im wis2box-Stack lädt die Daten im Verzeichnis 'downloads' im Verzeichnis herunter, das Sie als WIS2BOX_HOST_DATADIR in Ihrer wis2box.env-Datei definiert haben. Um den Inhalt des Downloads-Verzeichnisses anzuzeigen, können Sie den folgenden Befehl verwenden:

```bash
ls -R ~/wis2box-data/downloads
```

Beachten Sie, dass die heruntergeladenen Daten in Verzeichnissen gespeichert sind, die nach dem Thema benannt sind, unter dem die WIS2-Benachrichtigung veröffentlicht wurde.

## Entfernen von Abonnements aus dem wis2downloader

Melden Sie sich als Nächstes wieder beim wis2downloader-Container an:

```bash
python3 wis2box-ctl.py login wis2downloader
```

und entfernen Sie das Abonnement, das Sie vom wis2downloader gemacht haben, mit dem folgenden Befehl:

```bash
wis2downloader remove-subscription --topic cache/a/wis2/de-dwd-gts-to-wis2/#
```

Und verlassen Sie den wis2downloader-Container, indem Sie `exit` eingeben:
    
```bash
exit
```

Überprüfen Sie das wis2downloader-Dashboard in Grafana, um das entfernte Abonnement zu sehen. Sie sollten sehen, dass die Downloads stoppen.

## Herunterladen und Dekodieren von Daten für eine tropische Zyklonspur

In dieser Übung abonnieren Sie den WIS2 Training Broker, der Beispieldata für Schulungszwecke veröffentlicht. Sie richten ein Abonnement ein, um Daten für eine tropische Zyklonspur herunterzuladen. Anschließend dekodieren Sie die heruntergeladenen Daten mit dem "decode-bufr-jupyter" Container.

### Abonnieren des wis2training-brokers und Einrichten eines neuen Abonnements

Dies zeigt, wie Sie ein Abonnement für einen Broker einrichten, der nicht der Standardbroker ist, und ermöglicht es Ihnen, einige Daten herunterzuladen, die vom WIS2 Training Broker veröffentlicht werden.

Bearbeiten Sie die Datei wis2box.env und ändern Sie DOWNLOAD_BROKER_HOST in `wis2training-broker.wis2dev.io`, ändern Sie DOWNLOAD_BROKER_PORT in `1883` und ändern Sie DOWNLOAD_BROKER_TRANSPORT in `tcp`:

```copy
# downloader settings
DOWNLOAD_BROKER_HOST=wis2training-broker.wis2dev.io
DOWNLOAD_BROKER_PORT=1883
DOWNLOAD_BROKER_USERNAME=everyone
DOWNLOAD_BROKER_PASSWORD=everyone
# download transport mechanism (tcp or websockets)
DOWNLOAD_BROKER_TRANSPORT=tcp
```

Führen Sie dann den 'start'-Befehl erneut aus, um die Änderungen anzuwenden:

```bash
python3 wis2box-ctl.py start
```

Überprüfen Sie die Protokolle des wis2downloader, um zu sehen, ob die Verbindung zum neuen Broker erfolgreich war:

```bash
docker logs wis2downloader
```

Sie sollten die folgende Protokollnachricht sehen:

```copy
...
INFO - Connecting...
INFO - Host: wis2training-broker.wis2dev.io, port: 1883
INFO - Connected successfully
```

Jetzt richten wir ein neues Abonnement für das Thema ein, um Zyklonspurdaten vom WIS2 Training Broker herunterzuladen.

Melden Sie sich beim **wis2downloader** Container an:

```bash
python3 wis2box-ctl.py login wis2downloader
```

Und führen Sie den folgenden Befehl aus (kopieren Sie diesen, um Tippfehler zu vermeiden):

```bash
wis2downloader add-subscription --topic origin/a/wis2/int-wis2-training/data/core/weather/prediction/forecast/medium-range/probabilistic/trajectory
```

Verlassen Sie den **wis2downloader** Container, indem Sie `exit` eingeben.

Warten Sie, bis Sie sehen, dass die Downloads im wis2downloader-Dashboard in Grafana beginnen.

!!! note "Herunterladen von Daten vom WIS2 Training Broker"

    Der WIS2 Training Broker ist ein Testbroker, der zu Schulungszwecken verwendet wird und möglicherweise nicht die ganze Zeit Daten veröffentlicht.

    Während der Präsenzschulungen wird der lokale Trainer sicherstellen, dass der WIS2 Training Broker Daten für Sie zum Herunterladen veröffentlicht.

    Wenn Sie diese Übung außerhalb einer Schulungssitzung durchführen, sehen Sie möglicherweise keine heruntergeladenen Daten.

Überprüfen Sie, ob die Daten heruntergeladen wurden, indem Sie die Protokolle des wis2downloader erneut überprüfen mit:

```bash
docker logs wis2downloader
```

Sie sollten eine Protokollnachricht sehen, die der folgenden ähnelt:

```copy
[...] INFO - Nachricht unter dem Thema origin/a/wis2/int-wis2-training/data/core/weather/prediction/forecast/medium-range/probabilistic/trajectory erhalten
[...] INFO - Heruntergeladen A_JSXX05ECEP020000_C_ECMP_...
```

### Dekodieren heruntergeladener Daten

Um zu demonstrieren, wie Sie die heruntergeladenen Daten dekodieren können, werden wir einen neuen Container mit dem Image 'decode-bufr-jupyter' starten.

Dieser Container wird einen Jupyter-Notebook-Server auf Ihrer Instanz starten, der die "ecCodes"-Bibliothek enthält, die Sie zum Dekodieren von BUFR-Daten verwenden können.

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

    Der `decode-bufr-jupyter` Container ist ein benutzerdefinierter Container, der die ecCodes-Bibliothek enthält und einen Jupyter-Notebook-Server ausführt. Der Container basiert auf einem Image, das die `ecCodes`-Bibliothek zum Dekodieren von BUFR-Daten enthält, zusammen mit Bibliotheken für das Plotten und die Datenanalyse.

    Der obige Befehl startet den Container im abgetrennten Modus, mit dem Namen `decode-bufr-jupyter`, der Port 8888 wird auf das Hostsystem gemappt und die Umgebungsvariable `JUPYTER_TOKEN` ist auf `dataismagic!` gesetzt.
    
    Der obige Befehl montiert auch das Verzeichnis `~/wis2box-data/downloads` auf `/root/downloads` im Container. Dies stellt sicher, dass die heruntergeladenen Daten dem Jupyter-Notebook-Server zur Verfügung stehen.
    
Sobald der Container gestartet ist, können Sie auf den Jupyter-Notebook-Server zugreifen, indem Sie in Ihrem Webbrowser `http://YOUR-HOST:8888` aufrufen.

Sie sehen einen Bildschirm, auf dem Sie aufgefordert werden, ein "Passwort oder Token" einzugeben.

Geben Sie das Token `dataismagic!` ein, um sich beim Jupyter-Notebook-Server anzumelden.

Nachdem Sie sich angemeldet haben, sollten Sie den folgenden Bildschirm sehen, der die Verzeichnisse im Container auflistet:

![Jupyter notebook home](../assets/img/jupyter-files-screen1.png)

Doppelklicken Sie auf das Verzeichnis `example-notebooks`, um es zu öffnen.

Sie sollten den folgenden Bildschirm sehen, der die Beispiel-Notebooks auflistet, doppelklicken Sie auf das Notebook `tropical_cyclone_track.ipynb`, um es zu öffnen:

![Jupyter notebook example notebooks](../assets/img/jupyter-files-screen2.png)

Sie sollten jetzt im Jupyter-Notebook für das Dekodieren der Daten der tropischen Zyklonspur sein:

![Jupyter notebook tropical cyclone track](../assets/img/jupyter-tropical-cyclone-track.png)

Lesen Sie die Anweisungen im Notizbuch und führen Sie die Zellen aus, um die heruntergeladenen Daten für die Zugbahnen tropischer Zyklone zu entschlüsseln. Führen Sie jede Zelle aus, indem Sie auf die Zelle klicken und dann auf die Schaltfläche Ausführen in der Symbolleiste klicken oder `Shift+Enter` drücken.

Am Ende sollten Sie eine Darstellung der Schlagwahrscheinlichkeit für die Zugbahnen tropischer Zyklone sehen:

![Tropical cyclone tracks](../assets/img/tropical-cyclone-track-map.png)

!!! question 

    Das Ergebnis zeigt die vorhergesagte Wahrscheinlichkeit eines tropischen Sturmzugs innerhalb von 200 km. Wie würden Sie das Notizbuch aktualisieren, um die vorhergesagte Wahrscheinlichkeit eines tropischen Sturmzugs innerhalb von 300 km anzuzeigen?

??? success "Klicken Sie, um die Antwort zu enthüllen"

    Um das Notizbuch zu aktualisieren und die vorhergesagte Wahrscheinlichkeit eines tropischen Sturmzugs innerhalb einer anderen Entfernung anzuzeigen, können Sie die Variable `distance_threshold` im Code-Block, der die Schlagwahrscheinlichkeit berechnet, aktualisieren.

    Um die vorhergesagte Wahrscheinlichkeit eines tropischen Sturmzugs innerhalb von 300 km anzuzeigen,

    ```python
    # set distance threshold (meters)
    distance_threshold = 300000  # 300 km in meters
    ```

    Führen Sie dann die Zellen im Notizbuch erneut aus, um die aktualisierte Darstellung zu sehen.

!!! note "Dekodierung von BUFR-Daten"

    Die Übung, die Sie gerade durchgeführt haben, lieferte ein spezifisches Beispiel dafür, wie Sie BUFR-Daten mit der ecCodes-Bibliothek dekodieren können. Verschiedene Datentypen können unterschiedliche Dekodierungsschritte erfordern, und Sie müssen möglicherweise die Dokumentation für den Datentyp, mit dem Sie arbeiten, konsultieren.
    
    Für weitere Informationen konsultieren Sie bitte die [ecCodes-Dokumentation](https://confluence.ecmwf.int/display/ECC).



## Schlussfolgerung

!!! success "Herzlichen Glückwunsch!"

    In dieser praktischen Sitzung haben Sie gelernt, wie Sie:

    - den 'wis2downloader' verwenden, um sich bei einem WIS2 Broker zu abonnieren und Daten auf Ihr lokales System herunterzuladen
    - den Status der Downloads im Grafana-Dashboard anzeigen
    - einige heruntergeladene Daten mit dem 'decode-bufr-jupyter' Container dekodieren
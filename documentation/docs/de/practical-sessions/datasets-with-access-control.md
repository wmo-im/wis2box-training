---
title: Einrichten eines empfohlenen Datensatzes mit Zugangskontrolle
---

# Einrichten eines empfohlenen Datensatzes mit Zugangskontrolle

!!! abstract "Lernziele"
    Nach Abschluss dieser praktischen Übung werden Sie in der Lage sein:

    - einen neuen Datensatz mit der Datenrichtlinie 'recommended' zu erstellen
    - dem Datensatz ein Zugangstoken hinzuzufügen
    - zu überprüfen, dass der Datensatz ohne Zugangstoken nicht zugänglich ist
    - das Zugangstoken zu HTTP-Headers hinzuzufügen, um auf den Datensatz zuzugreifen

## Einführung

Datensätze, die nicht als 'core' Datensätze in der WMO betrachtet werden, können optional mit einer Zugangskontrollrichtlinie konfiguriert werden. wis2box bietet einen Mechanismus, um einem Datensatz ein Zugangstoken hinzuzufügen, das Benutzer daran hindert, Daten herunterzuladen, wenn sie nicht das Zugangstoken in den HTTP-Headers angeben.

## Vorbereitung

Stellen Sie sicher, dass Sie SSH-Zugang zu Ihrer Student-VM haben und dass Ihre wis2box-Instanz läuft.

Stellen Sie sicher, dass Sie mit dem MQTT-Broker Ihrer wis2box-Instanz über MQTT Explorer verbunden sind. Sie können die öffentlichen Zugangsdaten `everyone/everyone` verwenden, um sich mit dem Broker zu verbinden.

Stellen Sie sicher, dass Sie einen Webbrowser mit der wis2box-webapp für Ihre Instanz geöffnet haben, indem Sie zu `http://YOUR-HOST/wis2box-webapp` gehen.

## Erstellen eines neuen Datensatzes mit Datenrichtlinie 'recommended'

Gehen Sie zur Seite 'dataset editor' in der wis2box-webapp und erstellen Sie einen neuen Datensatz. Wählen Sie Data Type = 'weather/surface-weather-observations/synop'.

<img alt="create-dataset-recommended" src="../../assets/img/create-dataset-template.png" width="800">

Verwenden Sie für "Centre ID" dieselbe ID wie in den vorherigen praktischen Übungen.

Klicken Sie auf 'CONTINUE To FORM', um fortzufahren.

Setzen Sie im Dataset-Editor die Datenrichtlinie auf 'recommended' (beachten Sie, dass die Änderung der Datenrichtlinie die 'Topic Hierarchy' aktualisiert).
Ersetzen Sie die automatisch generierte 'Local ID' durch einen beschreibenden Namen für den Datensatz, z.B. 'recommended-data-with-access-control':

<img alt="create-dataset-recommended" src="../../assets/img/create-dataset-recommended.png" width="800">

Füllen Sie die erforderlichen Felder für räumliche Eigenschaften und Kontaktinformationen aus und 'Validate form', um auf Fehler zu prüfen.

Reichen Sie schließlich den Datensatz ein, verwenden Sie dazu das zuvor erstellte Authentifizierungstoken, und überprüfen Sie, dass der neue Datensatz in der wis2box-webapp erstellt wurde.

Überprüfen Sie in MQTT-Explorer, ob Sie die WIS2-Benachrichtigungsnachricht erhalten, die den neuen Discovery-Metadatensatz auf dem Topic `origin/a/wis2/<your-centre-id>/metadata` ankündigt.

## Hinzufügen eines Zugangstokens zum Datensatz

Melden Sie sich am wis2box-management Container an,

```bash
cd ~/wis2box
python3 wis2box-ctl.py login
```

Von der Kommandozeile im Container können Sie einen Datensatz mit dem Befehl `wis2box auth add-token` sichern, wobei Sie mit der Flag `--metadata-id` die Metadaten-ID des Datensatzes und das Zugangstoken als Argument angeben.

Zum Beispiel, um das Zugangstoken `S3cr3tT0k3n` zum Datensatz mit der Metadaten-ID `urn:wmo:md:not-my-centre:core.surface-based-observations.synop` hinzuzufügen:

```bash
wis2box auth add-token --metadata-id urn:wmo:md:not-my-centre:reco.surface-based-observations.synop S3cr3tT0k3n
```

Verlassen Sie den wis2box-management Container:

```bash
exit
```

## Veröffentlichen von Daten im Datensatz

Kopieren Sie die Datei `exercise-materials/access-control-exercises/aws-example.csv` in das Verzeichnis, das durch `WIS2BOX_HOST_DATADIR` in Ihrer `wis2box.env` definiert ist:

```bash
cp ~/exercise-materials/access-control-exercises/aws-example.csv ~/wis2box-data
```

Verwenden Sie dann WinSCP oder einen Kommandozeilen-Editor, um die Datei `aws-example.csv` zu bearbeiten und die WIGOS-Stations-IDs in den Eingabedaten an die Stationen in Ihrer wis2box-Instanz anzupassen.

Gehen Sie dann zum Station-Editor in der wis2box-webapp. Aktualisieren Sie für jede Station, die Sie in `aws-example.csv` verwendet haben, das 'topic'-Feld, damit es mit dem 'topic' des Datensatzes übereinstimmt, den Sie in der vorherigen Übung erstellt haben.

Diese Station wird nun mit 2 Topics verknüpft sein, einem für den 'core'-Datensatz und einem für den 'recommended'-Datensatz:

<img alt="edit-stations-add-topics" src="../../assets/img/edit-stations-add-topics.png" width="600">

Sie werden Ihr Token für `collections/stations` benötigen, um die aktualisierten Stationsdaten zu speichern.

Melden Sie sich anschließend am wis2box-management Container an:

```bash
cd ~/wis2box
python3 wis2box-ctl.py login
```

Von der wis2box-Kommandozeile können wir die Beispieldatei `aws-example.csv` wie folgt in einen spezifischen Datensatz einlesen:

```bash
wis2box data ingest -p /data/wis2box/aws-example.csv --metadata-id urn:wmo:md:not-my-centre:reco.surface-based-observations.synop
```

Stellen Sie sicher, dass Sie die korrekte Metadaten-ID für Ihren Datensatz angeben und **überprüfen Sie, dass Sie WIS2-Datenbenachrichtigungen in MQTT Explorer** auf dem Topic `origin/a/wis2/<your-centre-id>/data/recommended/surface-based-observations/synop` erhalten.

Überprüfen Sie den kanonischen Link in der WIS2-Benachrichtigungsnachricht und kopieren/fügen Sie den Link in den Browser ein, um zu versuchen, die Daten herunterzuladen.

Sie sollten einen 403 Forbidden-Fehler sehen.

## Hinzufügen des Zugangstokens zu HTTP-Headers für den Datenzugriff

Um zu demonstrieren, dass das Zugangstoken für den Zugriff auf den Datensatz erforderlich ist, werden wir den Fehler, den Sie im Browser gesehen haben, mit der Kommandozeilenfunktion `wget` reproduzieren.

Verwenden Sie von der Kommandozeile in Ihrer Student-VM den `wget`-Befehl mit dem kanonischen Link, den Sie aus der WIS2-Benachrichtigungsnachricht kopiert haben.

```bash
wget <canonical-link>
```

Sie sollten sehen, dass die HTTP-Anfrage mit *401 Unauthorized* zurückkommt und die Daten nicht heruntergeladen werden.

Fügen Sie nun das Zugangstoken zu den HTTP-Headers hinzu, um auf den Datensatz zuzugreifen.

```bash
wget --header="Authorization: Bearer S3cr3tT0k3n" <canonical-link>
```

Jetzt sollten die Daten erfolgreich heruntergeladen werden.

## Fazit

!!! success "Herzlichen Glückwunsch!"
    In dieser praktischen Übung haben Sie gelernt:

    - einen neuen Datensatz mit Datenrichtlinie 'recommended' zu erstellen
    - einem Datensatz ein Zugangstoken hinzuzufügen
    - zu überprüfen, dass der Datensatz ohne Zugangstoken nicht zugänglich ist
    - das Zugangstoken zu HTTP-Headers hinzuzufügen, um auf den Datensatz zuzugreifen
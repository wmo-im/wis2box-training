---
title: Konfiguration von Datensätzen in wis2box
---

# Konfiguration von Datensätzen in wis2box

!!! abstract "Lernziele"
    Nach Abschluss dieser praktischen Einheit werden Sie in der Lage sein:

    - einen neuen Datensatz zu erstellen
    - Erkennungsmetadaten für einen Datensatz zu erstellen
    - Datenzuordnungen für einen Datensatz zu konfigurieren
    - eine WIS2-Benachrichtigung mit einem WCMP2-Datensatz zu veröffentlichen
    - Ihren Datensatz zu aktualisieren und neu zu veröffentlichen

## Einführung

wis2box verwendet Datensätze, die mit Erkennungsmetadaten und Datenzuordnungen verknüpft sind.

Erkennungsmetadaten werden verwendet, um einen WCMP2 (WMO Core Metadata Profile 2) Datensatz zu erstellen, der über eine WIS2-Benachrichtigung auf Ihrem wis2box-broker veröffentlicht wird.

Die Datenzuordnungen werden verwendet, um ein Daten-Plugin mit Ihren Eingabedaten zu verknüpfen, wodurch Ihre Daten vor der Veröffentlichung über die WIS2-Benachrichtigung transformiert werden können.

Diese Einheit führt Sie durch die Erstellung eines neuen Datensatzes, die Erstellung von Erkennungsmetadaten und die Konfiguration von Datenzuordnungen. Sie werden Ihren Datensatz in der wis2box-api überprüfen und die WIS2-Benachrichtigung für Ihre Erkennungsmetadaten durchsehen.

## Vorbereitung

Verbinden Sie sich mit Ihrem Broker über MQTT Explorer.

Verwenden Sie anstelle Ihrer internen Broker-Anmeldedaten die öffentlichen Anmeldedaten `everyone/everyone`:

<img alt="MQTT Explorer: Connect to broker" src="../../assets/img/mqtt-explorer-wis2box-broker-everyone-everyone.png" width="800">

!!! Note

    Sie müssen die Anmeldedaten Ihres internen Brokers nie mit externen Benutzern teilen. Der 'everyone'-Benutzer ist ein öffentlicher Benutzer, der das Teilen von WIS2-Benachrichtigungen ermöglicht.

    Die Anmeldedaten `everyone/everyone` haben nur Lesezugriff auf das Thema 'origin/a/wis2/#'. Dies ist das Thema, unter dem die WIS2-Benachrichtigungen veröffentlicht werden. Der Global Broker kann sich mit diesen öffentlichen Anmeldedaten anmelden, um die Benachrichtigungen zu empfangen.
    
    Der 'everyone'-Benutzer sieht keine internen Themen und kann keine Nachrichten veröffentlichen.

Öffnen Sie einen Browser und rufen Sie die Seite `http://YOUR-HOST/wis2box-webapp` auf. Stellen Sie sicher, dass Sie angemeldet sind und auf die Seite 'dataset editor' zugreifen können.

Schauen Sie im Abschnitt [Initialisierung von wis2box](/practical-sessions/initializing-wis2box) nach, wenn Sie sich nicht mehr erinnern können, wie Sie sich mit dem Broker verbinden oder auf die wis2box-webapp zugreifen.

## Erstellen eines Autorisierungstokens für processes/wis2box

Sie benötigen ein Autorisierungstoken für den Endpunkt 'processes/wis2box', um Ihren Datensatz zu veröffentlichen.

Um ein Autorisierungstoken zu erstellen, greifen Sie über SSH auf Ihre Training-VM zu und verwenden Sie die folgenden Befehle, um sich beim wis2box-management Container anzumelden:

```bash
cd ~/wis2box
python3 wis2box-ctl.py login
```

Führen Sie dann den folgenden Befehl aus, um ein zufällig generiertes Autorisierungstoken für den Endpunkt 'processes/wis2box' zu erstellen:

```bash
wis2box auth add-token --path processes/wis2box
```

Sie können auch ein Token mit einem spezifischen Wert erstellen, indem Sie das Token als Argument für den Befehl angeben:

```bash
wis2box auth add-token --path processes/wis2box MyS3cretToken
```

Kopieren Sie den Token-Wert und speichern Sie ihn auf Ihrem lokalen Computer, da Sie ihn später benötigen werden.

Sobald Sie Ihr Token haben, können Sie den wis2box-management Container verlassen:

```bash
exit
```

## Erstellen eines neuen Datensatzes in der wis2box-webapp

Navigieren Sie zur Seite 'dataset editor' in der wis2box-webapp Ihrer wis2box-Instanz, indem Sie zu `http://YOUR-HOST/wis2box-webapp` gehen und 'dataset editor' aus dem Menü auf der linken Seite auswählen.

Klicken Sie auf der Seite 'dataset editor' unter dem Tab 'Datasets' auf "Create New ...":

<img alt="Create New Dataset" src="../../assets/img/wis2box-create-new-dataset.png" width="800">

Ein Pop-up-Fenster erscheint und fordert Sie auf, Folgendes anzugeben:

- **Centre ID**: Dies ist das Behördenkürzel (in Kleinbuchstaben und ohne Leerzeichen), wie vom WMO-Mitglied festgelegt, das das für die Veröffentlichung der Daten verantwortliche Datenzentrum identifiziert.
- **Data Type**: Die Art der Daten, für die Sie Metadaten erstellen. Sie können zwischen der Verwendung einer vordefinierten Vorlage oder der Auswahl von 'other' wählen. Wenn 'other' ausgewählt wird, müssen mehr Felder manuell ausgefüllt werden.

!!! Note "Centre ID"

    Ihre Centre-ID sollte mit der TLD Ihres Landes beginnen, gefolgt von einem Bindestrich (`-`) und einem abgekürzten Namen Ihrer Organisation (zum Beispiel `fr-meteofrance`). Die Centre-ID muss in Kleinbuchstaben sein und nur alphanumerische Zeichen verwenden. Die Dropdown-Liste zeigt alle derzeit bei WIS2 registrierten Centre-IDs sowie alle Centre-IDs, die Sie bereits in wis2box erstellt haben.

!!! Note "Data Type Templates"

    Das Feld *Data Type* ermöglicht die Auswahl aus einer Liste von verfügbaren Vorlagen im wis2box-webapp Dataset Editor. Eine Vorlage füllt das Formular mit vorgeschlagenen Standardwerten vor, die für den Datentyp geeignet sind. Dies umfasst vorgeschlagene Titel und Schlüsselwörter für die Metadaten sowie vorkonfigurierte Daten-Plugins. Das Thema wird auf das Standardthema für den Datentyp festgelegt.

    Für das Training verwenden wir den Datentyp *weather/surface-based-observations/synop*, der Daten-Plugins enthält, die sicherstellen, dass die Daten vor der Veröffentlichung in das BUFR-Format umgewandelt werden.

    Wenn Sie CAP-Warnungen über wis2box veröffentlichen möchten, verwenden Sie die Vorlage *weather/advisories-warnings*. Diese Vorlage enthält ein Daten-Plugin, das überprüft, ob die Eingabedaten eine gültige CAP-Warnung sind, bevor sie veröffentlicht werden. Um CAP-Warnungen zu erstellen und über wis2box zu veröffentlichen, können Sie [CAP Composer](https://github.com/wmo-raf/cap-composer) verwenden.

Bitte wählen Sie eine für Ihre Organisation passende Centre-ID.

Wählen Sie für **Data Type** die Option **weather/surface-based-observations/synop**:

<img alt="Create New Dataset Form: Initial information" src="../../assets/img/wis2box-create-new-dataset-form-initial.png" width="450">

Klicken Sie auf *continue to form*, um fortzufahren. Sie sehen nun das **Dataset Editor Form**.

Da Sie den Datentyp **weather/surface-based-observations/synop** ausgewählt haben, wird das Formular mit einigen Anfangswerten für diesen Datentyp vorausgefüllt.

## Erstellen von Erkennungsmetadaten

Mit dem Dataset Editor Form können Sie die Erkennungsmetadaten für Ihren Datensatz bereitstellen, die der wis2box-management Container zur Veröffentlichung eines WCMP2-Datensatzes verwendet.

Da Sie den Datentyp 'weather/surface-based-observations/synop' ausgewählt haben, wird das Formular mit einigen Standardwerten vorausgefüllt.

Bitte ersetzen Sie die automatisch generierte 'Local ID' durch einen beschreibenden Namen für Ihren Datensatz, z.B. 'synop-dataset-wis2training':

<img alt="Metadata Editor: title, description, keywords" src="../../assets/img/wis2box-metadata-editor-part1.png" width="800">

Überprüfen Sie den Titel und die Schlüsselwörter, aktualisieren Sie sie bei Bedarf und geben Sie eine Beschreibung für Ihren Datensatz ein.

Beachten Sie, dass es Optionen gibt, die 'WMO Data Policy' von 'core' auf 'recommended' zu ändern oder Ihre Standard-Metadaten-ID zu modifizieren. Bitte behalten Sie die Data-Policy als 'core' bei und verwenden Sie die Standard-Metadaten-ID.

Überprüfen Sie als Nächstes den Abschnitt, der Ihre 'Temporal Properties' und 'Spatial Properties' definiert. Sie können den Begrenzungsrahmen anpassen, indem Sie die Felder 'North Latitude', 'South Latitude', 'East Longitude' und 'West Longitude' aktualisieren:

<img alt="Metadata Editor: temporal properties, spatial properties" src="../../assets/img/wis2box-metadata-editor-part2.png" width="800">

Füllen Sie als Nächstes den Abschnitt 'Contact Information of the Data Provider' aus:

<img alt="Metadata Editor: contact information" src="../../assets/img/wis2box-metadata-editor-part3.png" width="800">

Füllen Sie schließlich den Abschnitt 'Data Quality Information' aus:

Wenn Sie alle Abschnitte ausgefüllt haben, klicken Sie auf 'VALIDATE FORM' und überprüfen Sie das Formular auf Fehler:

<img alt="Metadata Editor: validation" src="../../assets/img/wis2box-metadata-validation-error.png" width="800">

Wenn Fehler auftreten, korrigieren Sie diese und klicken Sie erneut auf 'VALIDATE FORM'.

Stellen Sie sicher, dass keine Fehler mehr vorhanden sind und Sie eine Pop-up-Meldung erhalten, die bestätigt, dass Ihr Formular validiert wurde:

<img alt="Metadata Editor: validation success" src="../../assets/img/wis2box-metadata-validation-success.png" width="800">

Überprüfen Sie als Nächstes, bevor Sie Ihren Datensatz einreichen, die Datenzuordnungen für Ihren Datensatz.

## Konfigurieren von Datenzuordnungen

Da Sie eine Vorlage zur Erstellung Ihres Datensatzes verwendet haben, wurden die Datensatzzuordnungen mit den Standard-Plugins für den Datentyp 'weather/surface-based-observations/synop' vorausgefüllt. Daten-Plugins werden in der wis2box verwendet, um Daten vor der Veröffentlichung über die WIS2-Benachrichtigung zu transformieren.

<img alt="Data Mappings: update plugin" src="../../assets/img/wis2box-data-mappings.png" width="800">

Beachten Sie, dass Sie auf die Schaltfläche "update" klicken können, um Einstellungen für das Plugin wie Dateierweiterung und Dateimuster zu ändern. Sie können die Standardeinstellungen vorerst beibehalten. In einer späteren Sitzung werden Sie mehr über BUFR und die Transformation von Daten in das BUFR-Format lernen.

## Einreichen Ihres Datensatzes

Abschließend können Sie auf 'submit' klicken, um Ihren Datensatz zu veröffentlichen.

Sie benötigen das Autorisierungstoken für 'processes/wis2box', das Sie zuvor erstellt haben. Wenn Sie dies noch nicht getan haben, können Sie ein neues Token erstellen, indem Sie den Anweisungen im Vorbereitungsabschnitt folgen.

Überprüfen Sie, ob Sie nach dem Einreichen Ihres Datensatzes die folgende Meldung erhalten, die anzeigt, dass der Datensatz erfolgreich eingereicht wurde:

<img alt="Submit Dataset Success" src="../../assets/img/wis2box-submit-dataset-success.png" width="400">

Nachdem Sie auf 'OK' geklickt haben, werden Sie zur Startseite des Dataset Editors weitergeleitet. Wenn Sie jetzt auf den Tab 'Dataset' klicken, sollten Sie Ihren neuen Datensatz aufgelistet sehen:

<img alt="Dataset Editor: new dataset" src="../../assets/img/wis2box-dataset-editor-new-dataset.png" width="800">

## Überprüfen der WIS2-Benachrichtigung für Ihre Erkennungsmetadaten

Gehen Sie zu MQTT Explorer. Wenn Sie mit dem Broker verbunden waren, sollten Sie eine neue WIS2-Benachrichtigung sehen, die unter dem Thema `origin/a/wis2/<your-centre-id>/metadata` veröffentlicht wurde:

<img alt="MQTT Explorer: WIS2 notification" src="../../assets/img/mqtt-explorer-wis2-notification-metadata.png" width="800">

Überprüfen Sie den Inhalt der WIS2-Benachrichtigung, die Sie veröffentlicht haben. Sie sollten ein JSON mit einer Struktur sehen, die dem WIS Notification Message (WNM) Format entspricht.

!!! question

    Unter welchem Thema wird die WIS2-Benachrichtigung veröffentlicht?

??? success "Klicken Sie hier für die Antwort"

    Die WIS2-Benachrichtigung wird unter dem Thema `origin/a/wis2/<your-centre-id>/metadata` veröffentlicht.

!!! question
    
    Versuchen Sie, den Titel, die Beschreibung und die Schlüsselwörter, die Sie in den Erkennungsmetadaten angegeben haben, in der WIS2-Benachrichtigung zu finden. Können Sie sie finden?

??? success "Klicken Sie hier für die Antwort"

    **Der Titel, die Beschreibung und die Schlüsselwörter,
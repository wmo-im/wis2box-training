---
title: Konfigurieren von Datensätzen in wis2box
---

# Konfigurieren von Datensätzen in wis2box

!!! abstract "Lernergebnisse"
    Am Ende dieser praktischen Sitzung werden Sie in der Lage sein:

    - einen neuen Datensatz zu erstellen
    - Entdeckungsmetadaten für einen Datensatz zu erstellen
    - Datenzuordnungen für einen Datensatz zu konfigurieren
    - eine WIS2-Benachrichtigung mit einem WCMP2-Datensatz zu veröffentlichen
    - Ihren Datensatz zu aktualisieren und erneut zu veröffentlichen

## Einführung

wis2box verwendet Datensätze, die mit Entdeckungsmetadaten und Datenzuordnungen verknüpft sind.

Entdeckungsmetadaten werden verwendet, um einen WCMP2 (WMO Core Metadata Profile 2) Datensatz zu erstellen, der über eine WIS2-Benachrichtigung veröffentlicht wird, die auf Ihrem wis2box-broker publiziert wird.

Die Datenzuordnungen werden verwendet, um ein Daten-Plugin mit Ihren Eingabedaten zu verknüpfen, sodass Ihre Daten vor der Veröffentlichung über die WIS2-Benachrichtigung transformiert werden können.

Diese Sitzung führt Sie durch das Erstellen eines neuen Datensatzes, das Erstellen von Entdeckungsmetadaten und das Konfigurieren von Datenzuordnungen. Sie werden Ihren Datensatz in der wis2box-api überprüfen und die WIS2-Benachrichtigung für Ihre Entdeckungsmetadaten überprüfen.

## Vorbereitung

Verbinden Sie sich mit Ihrem Broker über MQTT Explorer.

Verwenden Sie anstelle Ihrer internen Broker-Anmeldeinformationen die öffentlichen Anmeldeinformationen `everyone/everyone`:

<img alt="MQTT Explorer: Connect to broker" src="../../assets/img/mqtt-explorer-wis2box-broker-everyone-everyone.png" width="800">

!!! Note

    Sie müssen niemals die Anmeldeinformationen Ihres internen Brokers mit externen Benutzern teilen. Der Benutzer 'everyone' ist ein öffentlicher Benutzer, um das Teilen von WIS2-Benachrichtigungen zu ermöglichen.

    Die Anmeldeinformationen `everyone/everyone` haben nur Lesezugriff auf das Thema 'origin/a/wis2/#'. Dies ist das Thema, auf dem die WIS2-Benachrichtigungen veröffentlicht werden. Der Global Broker kann sich mit diesen öffentlichen Anmeldeinformationen anmelden, um die Benachrichtigungen zu erhalten.
    
    Der Benutzer 'everyone' wird keine internen Themen sehen oder Nachrichten veröffentlichen können.
    
Öffnen Sie einen Browser und gehen Sie zu `http://YOUR-HOST/wis2box-webapp`. Stellen Sie sicher, dass Sie angemeldet sind und auf die Seite 'dataset editor' zugreifen können.

Sehen Sie sich den Abschnitt über [Initializing wis2box](./initializing-wis2box.md) an, wenn Sie sich daran erinnern müssen, wie Sie sich mit dem Broker verbinden oder auf die wis2box-webapp zugreifen können.

## Erstellen eines Autorisierungstokens für processes/wis2box

Sie benötigen ein Autorisierungstoken für den Endpunkt 'processes/wis2box', um Ihren Datensatz zu veröffentlichen.

Um ein Autorisierungstoken zu erstellen, greifen Sie über SSH auf Ihre Trainings-VM zu und verwenden Sie die folgenden Befehle, um sich im wis2box-management-Container anzumelden:

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

Stellen Sie sicher, dass Sie den Tokenwert kopieren und auf Ihrem lokalen Rechner speichern, da Sie ihn später benötigen werden.

Sobald Sie Ihr Token haben, können Sie den wis2box-management-Container verlassen:

```bash
exit
```

## Erstellen eines neuen Datensatzes in der wis2box-webapp

Navigieren Sie auf der Seite 'dataset editor' in der wis2box-webapp Ihrer wis2box-Instanz zu `http://YOUR-HOST/wis2box-webapp` und wählen Sie 'dataset editor' aus dem Menü auf der linken Seite.

Auf der Seite 'dataset editor' klicken Sie unter dem Tab 'Datasets' auf "Create New ...":

<img alt="Create New Dataset" src="../../assets/img/wis2box-create-new-dataset.png" width="800">

Es erscheint ein Popup-Fenster, in dem Sie Folgendes angeben müssen:

- **Centre ID** : dies ist das Akronym der Agentur (in Kleinbuchstaben und ohne Leerzeichen), wie es vom WMO-Mitglied angegeben wurde, das das Datenzentrum identifiziert, das für die Veröffentlichung der Daten verantwortlich ist.
- **Data Type**: Der Datentyp, für den Sie Metadaten erstellen. Sie können zwischen der Verwendung einer vordefinierten Vorlage oder der Auswahl von 'other' wählen. Wenn 'other' ausgewählt wird, müssen weitere Felder manuell ausgefüllt werden.

!!! Note "Centre ID"

    Ihre Centre-ID sollte mit der TLD Ihres Landes beginnen, gefolgt von einem Bindestrich (`-`) und einem abgekürzten Namen Ihrer Organisation (zum Beispiel `de-dwd`). Die Centre-ID muss in Kleinbuchstaben sein und darf nur alphanumerische Zeichen verwenden. Die Dropdown-Liste zeigt alle derzeit auf WIS2 registrierten Centre-IDs sowie jede Centre-ID, die Sie bereits in wis2box erstellt haben.

!!! Note "Data Type Templates"

    Das Feld *Data Type* ermöglicht es Ihnen, aus einer Liste von Vorlagen in der wis2box-webapp dataset editor zu wählen. Eine Vorlage füllt das Formular mit vorgeschlagenen Standardwerten für den Datentyp aus. Dies umfasst vorgeschlagene Titel und Schlüsselwörter für die Metadaten und vorkonfigurierte Daten-Plugins. Das Thema wird auf das Standardthema für den Datentyp festgelegt.

    Zu Trainingszwecken verwenden wir den Datentyp *weather/surface-based-observations/synop*, der Daten-Plugins enthält, die sicherstellen, dass die Daten vor der Veröffentlichung in das BUFR-Format umgewandelt werden.

    Wenn Sie CAP-Warnungen mit wis2box veröffentlichen möchten, verwenden Sie die Vorlage *weather/advisories-warnings*. Diese Vorlage enthält ein Daten-Plugin, das überprüft, ob die Eingabedaten eine gültige CAP-Warnung sind, bevor sie veröffentlicht werden. Um CAP-Warnungen zu erstellen und über wis2box zu veröffentlichen, können Sie [CAP Composer](https://github.com/wmo-raf/cap-composer) verwenden.

Bitte wählen Sie eine Centre-ID, die für Ihre Organisation geeignet ist.

Für **Data Type** wählen Sie **weather/surface-based-observations/synop**:

<img alt="Create New Dataset Form: Initial information" src="../../assets/img/wis2box-create-new-dataset-form-initial.png" width="450">

Klicken Sie auf *continue to form*, um fortzufahren. Ihnen wird nun das **Dataset Editor Form** präsentiert.

Da Sie den Datentyp **weather/surface-based-observations/synop** ausgewählt haben, wird das Formular mit einigen Anfangswerten für diesen Datentyp vorausgefüllt.

## Erstellen von Entdeckungsmetadaten

Das Dataset Editor Form ermöglicht es Ihnen, die Entdeckungsmetadaten für Ihren Datensatz bereitzustellen, die der wis2box-management-Container verwenden wird, um einen WCMP2-Datensatz zu veröffentlichen.

Da Sie den Datentyp 'weather/surface-based-observations/synop' ausgewählt haben, wird das Formular mit einigen Standardwerten vorausgefüllt.

Bitte stellen Sie sicher, dass Sie die automatisch generierte 'Local ID' durch einen beschreibenden Namen für Ihren Datensatz ersetzen, z. B. 'synop-dataset-wis2training':

<img alt="Metadata Editor: title, description, keywords" src="../../assets/img/wis2box-metadata-editor-part1.png" width="800">

Überprüfen Sie den Titel und die Schlüsselwörter und aktualisieren Sie sie bei Bedarf und geben Sie eine Beschreibung für Ihren Datensatz an.

Beachten Sie, dass es Optionen gibt, die 'WMO Data Policy' von 'core' auf 'recommended' zu ändern oder Ihren Standard-Metadata Identifier zu ändern. Bitte behalten Sie die Datenrichtlinie als 'core' bei und verwenden Sie den Standard-Metadata Identifier.

Überprüfen Sie als Nächstes den Abschnitt, der Ihre 'Temporal Properties' und 'Spatial Properties' definiert. Sie können das Begrenzungsrechteck anpassen, indem Sie die Felder 'North Latitude', 'South Latitude', 'East Longitude' und 'West Longitude' aktualisieren:

<img alt="Metadata Editor: temporal properties, spatial properties" src="../../assets/img/wis2box-metadata-editor-part2.png" width="800">

Füllen Sie als Nächstes den Abschnitt aus, der die 'Contact Information of the Data Provider' definiert:

<img alt="Metadata Editor: contact information" src="../../assets/img/wis2box-metadata-editor-part3.png" width="800">

Füllen Sie schließlich den Abschnitt aus, der die 'Data Quality Information' definiert:

Sobald Sie alle Abschnitte ausgefüllt haben, klicken Sie auf 'VALIDATE FORM' und überprüfen Sie das Formular auf Fehler:

<img alt="Metadata Editor: validation" src="../../assets/img/wis2box-metadata-validation-error.png" width="800">

Wenn Fehler vorhanden sind, korrigieren Sie diese und klicken Sie erneut auf 'VALIDATE FORM'.

Stellen Sie sicher, dass Sie keine Fehler haben und dass Sie eine Popup-Meldung erhalten, die bestätigt, dass Ihr Formular validiert wurde:

<img alt="Metadata Editor: validation success"
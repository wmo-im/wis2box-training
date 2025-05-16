---
title: Datenabfrage mit der wis2box API
---

# Datenabfrage mit der wis2box API

!!! abstract "Lernergebnisse"
    Am Ende dieser praktischen Sitzung werden Sie in der Lage sein:

    - die wis2box API zu nutzen, um Ihre Stationen abzufragen und zu filtern
    - die wis2box API zu nutzen, um Ihre Daten abzufragen und zu filtern

## Einführung

Die wis2box API bietet Entdeckungs- und Abfragezugriff in maschinenlesbarer Form auf die Daten, die in wis2box eingegangen sind. Die API basiert auf dem OGC API - Features Standard und wird mit [pygeoapi](https://pygeoapi.io) implementiert.

Die wis2box API bietet Zugriff auf die folgenden Sammlungen:

- Stationen
- Entdeckungsmetadaten
- Datenbenachrichtigungen
- plus eine Sammlung pro konfiguriertem Datensatz, die die Ausgabe von bufr2geojson speichert (das Plugin `bufr2geojson` muss in der Datenmappingskonfiguration aktiviert sein, um die Elemente in der Datensatzsammlung zu füllen).

In dieser praktischen Sitzung lernen Sie, wie Sie die Daten-API verwenden, um Daten zu durchsuchen und abzufragen, die in wis2box eingegangen sind.

## Vorbereitung

!!! note
    Navigieren Sie zur Startseite der wis2box API in Ihrem Webbrowser:

    `http://YOUR-HOST/oapi`

<img alt="wis2box-api-landing-page" src="/../assets/img/wis2box-api-landing-page.png" width="600">

## Sammlungen inspizieren

Von der Startseite aus klicken Sie auf den Link 'Sammlungen'.

!!! question
    Wie viele Datensatzsammlungen sehen Sie auf der resultierenden Seite? Was denken Sie, was jede Sammlung darstellt?

??? success "Klicken Sie, um die Antwort zu sehen"
    Es sollten 4 Sammlungen angezeigt werden, einschließlich "Stationen", "Entdeckungsmetadaten" und "Datenbenachrichtigungen"

## Stationen inspizieren

Von der Startseite aus klicken Sie auf den Link 'Sammlungen', dann auf den Link 'Stationen'.

<img alt="wis2box-api-collections-stations" src="/../assets/img/wis2box-api-collections-stations.png" width="600">

Klicken Sie auf den Link 'Durchsuchen', dann auf den Link 'json'.

!!! question
    Wie viele Stationen werden zurückgegeben? Vergleichen Sie diese Zahl mit der Stationsliste in `http://YOUR-HOST/wis2box-webapp/station`

??? success "Klicken Sie, um die Antwort zu sehen"
    Die Anzahl der Stationen aus der API sollte gleich der Anzahl der Stationen sein, die Sie in der wis2box-Webanwendung sehen.

!!! question
    Wie können wir nach einer einzelnen Station (z. B. `Balaka`) abfragen?

??? success "Klicken Sie, um die Antwort zu sehen"
    Fragen Sie die API mit `http://YOUR-HOST/oapi/collections/stations/items?q=Balaka` ab.

!!! note
    Das obige Beispiel basiert auf den Malawi-Testdaten. Versuchen Sie, gegen die Stationen zu testen, die Sie als Teil der vorherigen Übungen eingegeben haben.

## Beobachtungen inspizieren

!!! note
    Das obige Beispiel basiert auf den Malawi-Testdaten. Versuchen Sie, gegen die Beobachtung zu testen, die Sie als Teil der Übungen eingegeben haben.

Von der Startseite aus klicken Sie auf den Link 'Sammlungen', dann auf den Link 'Oberflächenwetterbeobachtungen aus Malawi'.

<img alt="wis2box-api-collections-malawi-obs" src="/../assets/img/wis2box-api-collections-malawi-obs.png" width="600">

Klicken Sie auf den Link 'Abfragbare'.

<img alt="wis2box-api-collections-malawi-obs-queryables" src="/../assets/img/wis2box-api-collections-malawi-obs-queryables.png" width="600">

!!! question
    Welches abfragbare Element würde verwendet, um nach Stationskennung zu filtern?

??? success "Klicken Sie, um die Antwort zu sehen"
    Das `wigos_station_identifer` ist das richtige abfragbare Element.

Navigieren Sie zur vorherigen Seite (d. h. `http://YOUR-HOST/oapi/collections/urn:wmo:md:mwi:mwi_met_centre:surface-weather-observations`)

Klicken Sie auf den Link 'Durchsuchen'.

!!! question
    Wie können wir die JSON-Antwort visualisieren?

??? success "Klicken Sie, um die Antwort zu sehen"
    Indem Sie auf den Link 'JSON' oben rechts auf der Seite klicken oder `f=json` zur API-Anfrage im Webbrowser hinzufügen.

Überprüfen Sie die JSON-Antwort der Beobachtungen.

!!! question
    Wie viele Datensätze werden zurückgegeben?

!!! question
    Wie können wir die Antwort auf 3 Beobachtungen begrenzen?

??? success "Klicken Sie, um die Antwort zu sehen"
    Fügen Sie `limit=3` zur API-Anfrage hinzu.

!!! question
    Wie können wir die Antwort nach den neuesten Beobachtungen sortieren?

??? success "Klicken Sie, um die Antwort zu sehen"
    Fügen Sie `sortby=-resultTime` zur API-Anfrage hinzu (beachten Sie das `-`-Zeichen, um die absteigende Sortierreihenfolge anzugeben). Um nach den frühesten Beobachtungen zu sortieren, aktualisieren Sie die Anfrage, um `sortby=resultTime` einzuschließen.

!!! question
    Wie können wir die Beobachtungen nach einer einzelnen Station filtern?

??? success "Klicken Sie, um die Antwort zu sehen"
    Fügen Sie `wigos_station_identifier=<WSI>` zur API-Anfrage hinzu.

!!! question
    Wie können wir die Beobachtungen als CSV erhalten?

??? success "Klicken Sie, um die Antwort zu sehen"
    Fügen Sie `f=csv` zur API-Anfrage hinzu.

!!! question
    Wie können wir eine einzelne Beobachtung (id) anzeigen?

??? success "Klicken Sie, um die Antwort zu sehen"
    Verwenden Sie den Merkmalsidentifikator aus einer API-Anfrage gegen die Beobachtungen, fragen Sie die API für `http://YOUR-HOST/oapi/collections/{collectionId}/items/{featureId}`, wobei `{collectionId}` der Name Ihrer Beobachtungssammlung und `{itemId}` der Identifikator der einzelnen Beobachtung von Interesse ist.

## Schlussfolgerung

!!! success "Herzlichen Glückwunsch!"
    In dieser praktischen Sitzung haben Sie gelernt, wie Sie:

    - die wis2box API nutzen, um Ihre Stationen abzufragen und zu filtern
    - die wis2box API nutzen, um Ihre Daten abzufragen und zu filtern
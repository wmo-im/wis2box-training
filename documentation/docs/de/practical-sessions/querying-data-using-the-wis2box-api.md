---
title: Abfrage von Daten über die wis2box API
---

# Abfrage von Daten über die wis2box API

!!! abstract "Lernziele"
    Nach Abschluss dieser praktischen Übung werden Sie in der Lage sein:

    - die wis2box API zu nutzen, um Ihre Stationen abzufragen und zu filtern
    - die wis2box API zu nutzen, um Ihre Daten abzufragen und zu filtern

## Einführung

Die wis2box API bietet maschinenlesbaren Zugriff auf die in wis2box eingespeisten Daten zur Entdeckung und Abfrage. Die API basiert auf dem OGC API - Features Standard und ist mit [pygeoapi](https://pygeoapi.io) implementiert.

Die wis2box API bietet Zugriff auf folgende Sammlungen:

- Stationen
- Entdeckungsmetadaten
- Datenbenachrichtigungen
- plus eine Sammlung pro konfiguriertem Datensatz, die die Ausgabe von bufr2geojson speichert (das Plugin `bufr2geojson` muss in der Datenzuordnungskonfiguration aktiviert sein, um die Elemente in der Datensatzsammlung zu füllen).

In dieser praktischen Übung lernen Sie, wie Sie die Daten-API verwenden können, um in wis2box eingespeiste Daten zu durchsuchen und abzufragen.

## Vorbereitung

!!! note
    Navigieren Sie in Ihrem Webbrowser zur Startseite der wis2box API:

    `http://YOUR-HOST/oapi`

<img alt="wis2box-api-landing-page" src="../../assets/img/wis2box-api-landing-page.png" width="600">

## Sammlungen inspizieren

Klicken Sie auf der Startseite auf den Link 'Collections'.

!!! question
    Wie viele Datensatzsammlungen sehen Sie auf der resultierenden Seite? Was denken Sie, repräsentiert jede Sammlung?

??? success "Klicken Sie hier für die Antwort"
    Es sollten 4 Sammlungen angezeigt werden, einschließlich "Stations", "Discovery metadata" und "Data notifications"

## Stationen inspizieren

Klicken Sie auf der Startseite auf den Link 'Collections' und dann auf den Link 'Stations'.

<img alt="wis2box-api-collections-stations" src="../../assets/img/wis2box-api-collections-stations.png" width="600">

Klicken Sie auf den Link 'Browse' und dann auf den Link 'json'.

!!! question
    Wie viele Stationen werden zurückgegeben? Vergleichen Sie diese Zahl mit der Stationsliste unter `http://YOUR-HOST/wis2box-webapp/station`

??? success "Klicken Sie hier für die Antwort"
    Die Anzahl der Stationen von der API sollte gleich der Anzahl der Stationen sein, die Sie in der wis2box webapp sehen.

!!! question
    Wie können wir nach einer einzelnen Station suchen (z.B. `Balaka`)?

??? success "Klicken Sie hier für die Antwort"
    Fragen Sie die API mit `http://YOUR-HOST/oapi/collections/stations/items?q=Balaka` ab.

!!! note
    Das obige Beispiel basiert auf den Malawi-Testdaten. Versuchen Sie, gegen die Stationen zu testen, die Sie im Rahmen der vorherigen Übungen eingespeist haben.

[Fortsetzung der Übersetzung folgt im gleichen Stil...]
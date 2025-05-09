---
title: DAYCLI Vorlage
---

# csv2bufr Vorlage für tägliche Klimadaten (DAYCLI)

Die **DAYCLI** Vorlage bietet ein standardisiertes CSV-Format zur Umwandlung von täglichen Klimadaten in die BUFR-Sequenz 307075.

Das Format ist für den Einsatz in Klimadaten-Management-Systemen gedacht, um Daten auf WIS2 zu veröffentlichen, zur Unterstützung der Berichtsanforderungen für tägliche Klimabeobachtungen.

Diese Vorlage bildet tägliche Beobachtungen ab von:

 - Minimaler, maximaler und durchschnittlicher Temperatur über einen 24-Stunden-Zeitraum
 - Gesamte angesammelte Niederschlagsmenge über einen 24-Stunden-Zeitraum
 - Gesamte Schneehöhe zum Zeitpunkt der Beobachtung
 - Höhe des Neuschnees über einen 24-Stunden-Zeitraum

Diese Vorlage erfordert zusätzliche Metadaten im Vergleich zur vereinfachten AWS-Vorlage: Methode zur Berechnung der Durchschnittstemperatur; Sensor- und Stationshöhen; Exposition und Klassifikation der Messqualität.

!!! Note "Über die DAYCLI Vorlage"
    Bitte beachten Sie, dass die DAYCLI BUFR-Sequenz während 2025 aktualisiert wird, um zusätzliche Informationen und überarbeitete QC-Flags einzuschließen. Die DAYCLI Vorlage in der wis2box wird aktualisiert, um diese Änderungen widerzuspiegeln. Die WMO wird kommunizieren, wenn die wis2box-Software aktualisiert wird, um die neue DAYCLI Vorlage einzuschließen, damit Benutzer ihre Systeme entsprechend aktualisieren können.

## CSV-Spalten und Beschreibung

{{ read_csv("docs/assets/tables/daycli-table.csv") }}

## Durchschnittsberechnungsmethode

{{ read_csv("docs/assets/tables/averaging-method-table.csv") }}

## Qualitätsflagge

{{ read_csv("docs/assets/tables/quality_flag.csv") }}

## Referenzen für Standortklassifikation

[Referenz für "temperature_siting_classification"](https://library.wmo.int/idviewer/35625/839).

[Referenz für "precipitation_siting_classification"](https://library.wmo.int/idviewer/35625/840).

## Beispiel

Beispiel einer CSV-Datei, die der DAYCLI Vorlage entspricht: [daycli-example.csv](./../../sample-data/daycli-example.csv).
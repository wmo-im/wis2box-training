---
title: AWS Vorlage
---

# csv2bufr Vorlage für automatische Wetterstationen, die stündlich GBON-Daten melden

Die **AWS Vorlage** verwendet ein standardisiertes CSV-Format, um Daten von automatischen Wetterstationen im Rahmen der GBON-Berichtsanforderungen zu erfassen. Diese Zuordnungsvorlage konvertiert CSV-Daten in die BUFR-Sequenzen 301150, 307096.

Das Format ist für den Einsatz mit automatischen Wetterstationen vorgesehen, die eine Mindestanzahl von Parametern melden, einschließlich Druck, Lufttemperatur und -feuchtigkeit, Windgeschwindigkeit und -richtung sowie Niederschlag auf stündlicher Basis.

## CSV-Spalten und Beschreibung

{{ read_csv("docs/assets/tables/aws-minimal.csv") }}

## Beispiel

Beispiel einer CSV-Datei, die der AWS-Vorlage entspricht: [aws-example.csv](./../../sample-data/aws-example.csv).
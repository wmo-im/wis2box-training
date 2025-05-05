---
title: AWS-Vorlage
---

# csv2bufr-Vorlage für automatische Wetterstationen mit stündlicher GBON-Datenübermittlung

Die **AWS-Vorlage** verwendet ein standardisiertes CSV-Format zur Erfassung von Daten aus automatischen Wetterstationen zur Unterstützung der GBON-Berichterstattungsanforderungen. Diese Zuordnungsvorlage konvertiert CSV-Daten in die BUFR-Sequenz 301150, 307096.

Das Format ist für die Verwendung mit automatischen Wetterstationen vorgesehen, die eine Mindestanzahl von Parametern melden, einschließlich Luftdruck, Lufttemperatur und Luftfeuchtigkeit, Windgeschwindigkeit und -richtung sowie Niederschlag auf stündlicher Basis.

## CSV-Spalten und Beschreibung

{{ read_csv("docs/assets/tables/aws-minimal.csv") }}

## Beispiel

Beispiel-CSV-Datei, die der AWS-Vorlage entspricht: [aws-example.csv](/sample-data/aws-example.csv).
---
title: Template AWS
---

# Template csv2bufr per Stazioni Meteorologiche Automatiche che riportano dati GBON orari

Il **Template AWS** utilizza un formato CSV standardizzato per acquisire dati dalle Stazioni Meteorologiche Automatiche in supporto ai requisiti di reportistica GBON. Questo template di mappatura converte i dati CSV nella sequenza BUFR 301150, 307096.

Il formato è destinato all'uso con stazioni meteorologiche automatiche che riportano un numero minimo di parametri, tra cui pressione, temperatura dell'aria e umidità, velocità e direzione del vento e precipitazioni su base oraria.

## Colonne CSV e descrizione

{{ read_csv("docs/assets/tables/aws-minimal.csv") }}

## Esempio

File CSV di esempio conforme al template AWS: [aws-example.csv](/sample-data/aws-example.csv).
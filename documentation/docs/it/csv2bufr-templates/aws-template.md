---
title: Modello AWS
---

# Modello csv2bufr per Stazioni Meteorologiche Automatiche che riportano dati orari GBON

Il **Modello AWS** utilizza un formato CSV standardizzato per l'ingestione dei dati provenienti da Stazioni Meteorologiche Automatiche a supporto dei requisiti di segnalazione GBON. Questo modello di mappatura converte i dati CSV nelle sequenze BUFR 301150, 307096.

Il formato è destinato all'uso con stazioni meteorologiche automatiche che riportano un numero minimo di parametri, inclusi pressione, temperatura e umidità dell'aria, velocità e direzione del vento e precipitazioni su base oraria.

## Colonne CSV e descrizione

{{ read_csv("docs/assets/tables/aws-minimal.csv") }}

## Esempio

File CSV di esempio che si conforma al modello AWS: [aws-example.csv](./../../sample-data/aws-example.csv).
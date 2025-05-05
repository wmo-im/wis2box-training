---
title: Template DAYCLI
---

# Template csv2bufr per dati climatici giornalieri (DAYCLI)

Il template **DAYCLI** fornisce un formato CSV standardizzato per convertire i dati climatici giornalieri nella sequenza BUFR 307075.

Il formato è destinato all'uso con i Sistemi di Gestione dei Dati Climatici per pubblicare dati su WIS2, a supporto degli obblighi di segnalazione delle osservazioni climatiche giornaliere.

Questo template mappa le osservazioni giornaliere di:

 - Temperatura minima, massima e media su un periodo di 24 ore
 - Precipitazione totale accumulata su un periodo di 24 ore
 - Profondità totale della neve al momento dell'osservazione
 - Profondità della neve fresca su un periodo di 24 ore

Questo template richiede metadati aggiuntivi rispetto al template semplificato AWS: metodo di calcolo della temperatura media; altezze del sensore e della stazione; classificazione di esposizione e qualità della misurazione.

!!! Nota "Riguardo al template DAYCLI"
    Si prega di notare che la sequenza BUFR DAYCLI sarà aggiornata nel 2025 per includere informazioni aggiuntive e bandiere di controllo di qualità (QC) riviste. Il template DAYCLI incluso nel wis2box sarà aggiornato per riflettere questi cambiamenti. L'OMM comunicherà quando il software wis2box sarà aggiornato per includere il nuovo template DAYCLI, permettendo agli utenti di aggiornare i loro sistemi di conseguenza.

## Colonne CSV e descrizione

{{ read_csv("docs/assets/tables/daycli-table.csv") }}

## Metodo di mediazione

{{ read_csv("docs/assets/tables/averaging-method-table.csv") }}

## Bandiera di qualità

{{ read_csv("docs/assets/tables/quality_flag.csv") }}

## Riferimenti per la classificazione del sito

[Riferimento per "classificazione del sito per la temperatura"](https://library.wmo.int/idviewer/35625/839).

[Riferimento per "classificazione del sito per le precipitazioni"](https://library.wmo.int/idviewer/35625/840).

## Esempio

File CSV di esempio che si conforma al template DAYCLI: [daycli-example.csv](/sample-data/daycli-example.csv).

---
title: Home
---

<img alt="Logo WMO" src="/assets/img/wmo-logo.png" width="200">
# Formazione su WIS2 in a box

WIS2 in a box ([wis2box](https://docs.wis2box.wis.wmo.int)) è un'implementazione di riferimento libera e open source (FOSS) di un nodo WIS2 della WMO. Il progetto fornisce un set di strumenti plug and play per l'ingestione, l'elaborazione e la pubblicazione di dati meteorologici/climatici/idrici utilizzando approcci basati su standard in linea con i principi WIS2. wis2box offre anche accesso a tutti i dati nella rete WIS2. wis2box è progettato per avere una bassa barriera all'ingresso per i fornitori di dati, fornendo infrastrutture e servizi abilitanti per la scoperta, l'accesso e la visualizzazione dei dati.

Questa formazione fornisce spiegazioni passo dopo passo su vari aspetti del progetto wis2box, oltre a una serie di esercizi per aiutarti a pubblicare e scaricare dati da WIS2. La formazione è fornita sotto forma di presentazioni panoramiche e di esercizi pratici.

I partecipanti potranno lavorare con dati di test e metadati di esempio, oltre a integrare i propri dati e metadati.

Questa formazione copre un'ampia gamma di argomenti (installazione/configurazione/pubblicazione/download dei dati, ecc.).

## Obiettivi e risultati di apprendimento

Gli obiettivi di questa formazione sono di familiarizzare con i seguenti:

- Concetti e componenti fondamentali dell'architettura WIS2
- formati di dati e metadati utilizzati in WIS2 per la scoperta e l'accesso
- architettura e ambiente di wis2box
- funzioni principali di wis2box:
    - gestione dei metadati
    - ingestione dei dati e trasformazione in formato BUFR
    - broker MQTT per la pubblicazione di messaggi WIS2
    - endpoint HTTP per il download dei dati
    - endpoint API per l'accesso programmatico ai dati

## Navigazione

La navigazione a sinistra fornisce un indice per l'intera formazione.

La navigazione a destra fornisce un indice per una pagina specifica.

## Prerequisiti

### Conoscenze

- Comandi Linux di base (vedi il [cheatsheet](./cheatsheets/linux.md))
- Conoscenze di base di networking e protocolli Internet

### Software

Questa formazione richiede i seguenti strumenti:

- Un'istanza in esecuzione su Ubuntu OS (fornita dai formatori WMO durante le sessioni di formazione locali) vedi [Accesso alla tua VM studente](./practical-sessions/accessing-your-student-vm.md#introduction)
- Client SSH per accedere alla tua istanza
- MQTT Explorer sul tuo computer locale
- Client SCP e SFTP per copiare file dal tuo computer locale

## Convenzioni

!!! question

    Una sezione contrassegnata in questo modo ti invita a rispondere a una domanda.

Noterai anche sezioni di suggerimenti e note all'interno del testo:

!!! tip

    I suggerimenti offrono aiuto su come eseguire al meglio le attività.

!!! note

    Le note forniscono informazioni aggiuntive sull'argomento trattato dalla sessione pratica, oltre a come eseguire al meglio le attività.

Gli esempi sono indicati come segue:

Configuration
``` {.yaml linenums="1"}
my-collection-defined-in-yaml:
    type: collection
    title: my title defined as a yaml attribute named title
    description: my description as a yaml attribute named description
```

I frammenti che devono essere digitati in un terminale/console sono indicati come:

```bash
echo 'Hello world'
```

I nomi dei container (immagini in esecuzione) sono denotati in **grassetto**.

## Luogo e materiali della formazione

I contenuti della formazione, il wiki e il tracker dei problemi sono gestiti su GitHub a [https://github.com/World-Meteorological-Organization/wis2box-training](https://github.com/World-Meteorological-Organization/wis2box-training).

## Stampa del materiale

Questa formazione può essere esportata in PDF. Per salvare o stampare questo materiale didattico, vai alla [pagina di stampa](print_page), e seleziona
File > Stampa > Salva come PDF.

## Materiali degli esercizi

I materiali degli esercizi possono essere scaricati dal file zip [exercise-materials.zip](/exercise-materials.zip).

## Supporto

Per problemi/bug/suggerimenti o miglioramenti/contributi a questa formazione, utilizza il [GitHub issue tracker](https://github.com/World-Meteorological-Organization/wis2box-training/issues).

Tutti i bug, i miglioramenti e i problemi di wis2box possono essere segnalati su [GitHub](https://github.com/World-Meteorological-Organization/wis2box/issues).

Per ulteriore supporto o domande, contatta wis2-support@wmo.int.

Come sempre, la documentazione principale di wis2box può sempre essere trovata su [https://docs.wis2box.wis.wmo.int](https://docs.wis2box.wis.wmo.int).

I contributi sono sempre incoraggiati e benvenuti!
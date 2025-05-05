---
title: Home
---

<img alt="WMO logo" src="../assets/img/wmo-logo.png" width="200">
# Formazione WIS2 in a box

WIS2 in a box ([wis2box](https://docs.wis2box.wis.wmo.int)) è un'Implementazione di Riferimento Libera e Open Source (FOSS) di un WMO WIS2 Node. Il progetto fornisce un insieme di strumenti plug and play per acquisire, elaborare e pubblicare dati meteorologici/climatici/idrici utilizzando approcci basati su standard in linea con i principi WIS2. wis2box fornisce anche accesso a tutti i dati nella rete WIS2. wis2box è progettato per avere una bassa barriera d'ingresso per i fornitori di dati, fornendo infrastrutture e servizi abilitanti per la scoperta, l'accesso e la visualizzazione dei dati.

Questa formazione fornisce spiegazioni dettagliate dei vari aspetti del progetto wis2box e una serie di esercizi
per aiutarti a pubblicare e scaricare dati da WIS2. La formazione è fornita sotto forma di presentazioni generali e
esercitazioni pratiche.

I partecipanti potranno lavorare con dati e metadati di esempio, oltre a integrare i propri dati e metadati.

Questa formazione copre un'ampia gamma di argomenti (installazione/configurazione/impostazione, pubblicazione/download dei dati, ecc.).

## Obiettivi e risultati di apprendimento

Gli obiettivi di questa formazione sono familiarizzare con:

- Concetti e componenti fondamentali dell'architettura WIS2
- Formati di dati e metadati utilizzati in WIS2 per la scoperta e l'accesso
- Architettura e ambiente wis2box
- Funzioni principali di wis2box:
    - Gestione dei metadati
    - Acquisizione dei dati e trasformazione in formato BUFR
    - Broker MQTT per la pubblicazione di messaggi WIS2
    - Endpoint HTTP per il download dei dati
    - Endpoint API per l'accesso programmatico ai dati

## Navigazione

La navigazione a sinistra fornisce un indice per l'intera formazione.

La navigazione a destra fornisce un indice per la pagina specifica.

## Prerequisiti

### Conoscenze

- Comandi Linux di base (vedi il [prontuario](cheatsheets/linux.md))
- Conoscenza base di reti e protocolli Internet

### Software

Questa formazione richiede i seguenti strumenti:

- Un'istanza con sistema operativo Ubuntu (fornita dai formatori WMO durante le sessioni di formazione locali) vedi [Accesso alla VM dello studente](practical-sessions/accessing-your-student-vm.md#introduction)
- Client SSH per accedere alla propria istanza
- MQTT Explorer sulla macchina locale
- Client SCP e SFTP per copiare file dalla macchina locale

## Convenzioni

!!! question

    Una sezione contrassegnata in questo modo ti invita a rispondere a una domanda.

Inoltre, noterai sezioni di suggerimenti e note nel testo:

!!! tip

    I suggerimenti condividono aiuti su come svolgere al meglio le attività.

!!! note

    Le note forniscono informazioni aggiuntive sull'argomento trattato nella sessione pratica, e su come svolgere al meglio le attività.

Gli esempi sono indicati come segue:

Configurazione
``` {.yaml linenums="1"}
my-collection-defined-in-yaml:
    type: collection
    title: my title defined as a yaml attribute named title
    description: my description as a yaml attribute named description
```

I comandi da digitare in un terminale/console sono indicati come:

```bash
echo 'Hello world'
```

I nomi dei container (immagini in esecuzione) sono indicati in **grassetto**.

## Sede della formazione e materiali

I contenuti della formazione, il wiki e il sistema di tracciamento dei problemi sono gestiti su GitHub all'indirizzo [https://github.com/World-Meteorological-Organization/wis2box-training](https://github.com/World-Meteorological-Organization/wis2box-training).

## Stampa del materiale

Questa formazione può essere esportata in PDF. Per salvare o stampare questo materiale formativo, vai alla [pagina di stampa](print_page) e seleziona
File > Stampa > Salva come PDF.

## Materiali per gli esercizi

I materiali per gli esercizi possono essere scaricati dal file [exercise-materials.zip](/exercise-materials.zip).

## Supporto

Per problemi/bug/suggerimenti o miglioramenti/contributi a questa formazione, utilizza il [sistema di tracciamento problemi su GitHub](https://github.com/World-Meteorological-Organization/wis2box-training/issues).

Tutti i bug, i miglioramenti e i problemi di wis2box possono essere segnalati su [GitHub](https://github.com/World-Meteorological-Organization/wis2box/issues).

Per ulteriore supporto o domande, contattare wis2-support@wmo.int.

Come sempre, la documentazione principale di wis2box è disponibile su [https://docs.wis2box.wis.wmo.int](https://docs.wis2box.wis.wmo.int).

I contributi sono sempre incoraggiati e benvenuti!
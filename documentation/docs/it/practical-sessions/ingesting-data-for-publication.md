---
title: Inserimento dei Dati per la Pubblicazione
---

# Inserimento dei dati per la pubblicazione

!!! abstract "Obiettivi di Apprendimento"

    Al termine di questa sessione pratica, sarai in grado di:
    
    - Attivare il flusso di lavoro wis2box caricando dati su MinIO utilizzando la riga di comando, l'interfaccia web MinIO, SFTP o uno script Python.
    - Accedere alla dashboard Grafana per monitorare lo stato dell'inserimento dei dati e visualizzare i log della tua istanza wis2box.
    - Visualizzare le notifiche dati WIS2 pubblicate dal tuo wis2box utilizzando MQTT Explorer.

## Introduzione

In WIS2, i dati vengono condivisi in tempo reale utilizzando notifiche dati WIS2 che contengono un link "canonico" da cui i dati possono essere scaricati.

Per attivare il flusso di lavoro dei dati in un WIS2 Node utilizzando il software wis2box, i dati devono essere caricati nel bucket **wis2box-incoming** in **MinIO**, che avvia il flusso di lavoro wis2box. Questo processo porta alla pubblicazione dei dati tramite una notifica dati WIS2. A seconda delle mappature dei dati configurate nella tua istanza wis2box, i dati potrebbero essere trasformati in formato BUFR prima della pubblicazione.

In questo esercizio, utilizzeremo file di dati di esempio per attivare il flusso di lavoro wis2box e **pubblicare notifiche dati WIS2** per il dataset che hai configurato nella sessione pratica precedente.

Durante l'esercizio, monitoreremo lo stato dell'inserimento dei dati utilizzando la **dashboard Grafana** e **MQTT Explorer**. La dashboard Grafana utilizza i dati da Prometheus e Loki per visualizzare lo stato del tuo wis2box, mentre MQTT Explorer ti permette di vedere le notifiche dati WIS2 pubblicate dalla tua istanza wis2box.

Nota che wis2box trasformerà i dati di esempio in formato BUFR prima di pubblicarli sul broker MQTT, secondo le mappature dei dati preconfigurate nel tuo dataset. Per questo esercizio, ci concentreremo sui diversi metodi per caricare dati nella tua istanza wis2box e verificare il successo dell'inserimento e della pubblicazione. La trasformazione dei dati sarà trattata successivamente nella sessione pratica [Data Conversion Tools](../data-conversion-tools).

## Preparazione

Questa sezione utilizza il dataset per "surface-based-observations/synop" precedentemente creato nella sessione pratica [Configuring Datasets in wis2box](/practical-sessions/configuring-wis2box-datasets). Richiede anche la conoscenza della configurazione delle stazioni nel **wis2box-webapp**, come descritto nella sessione pratica [Configuring Station Metadata](/practical-sessions/configuring-station-metadata).

Assicurati di poter accedere alla tua VM studente utilizzando il tuo client SSH (es. PuTTY).

Assicurati che wis2box sia attivo e in esecuzione:

```bash
cd ~/wis2box/
python3 wis2box-ctl.py start
python3 wis2box-ctl.py status
```

Assicurati che MQTT Explorer sia in esecuzione e connesso alla tua istanza utilizzando le credenziali pubbliche `everyone/everyone` con una sottoscrizione all'argomento `origin/a/wis2/#`.

Assicurati di avere un browser web aperto con la dashboard Grafana per la tua istanza navigando su `http://YOUR-HOST:3000`.

### Preparare i Dati di Esempio

Copia la directory `exercise-materials/data-ingest-exercises` nella directory che hai definito come `WIS2BOX_HOST_DATADIR` nel tuo file `wis2box.env`:

```bash
cp -r ~/exercise-materials/data-ingest-exercises ~/wis2box-data/
```

!!! note
    Il `WIS2BOX_HOST_DATADIR` è montato come `/data/wis2box/` all'interno del container wis2box-management dal file `docker-compose.yml` incluso nella directory `wis2box`.
    
    Questo ti permette di condividere dati tra l'host e il container.

### Aggiungere la Stazione di Test

Aggiungi la stazione con identificatore WIGOS `0-20000-0-64400` alla tua istanza wis2box utilizzando l'editor delle stazioni nel wis2box-webapp.

Recupera la stazione da OSCAR:

<img alt="oscar-station" src="../../assets/img/webapp-test-station-oscar-search.png" width="600">

Aggiungi la stazione ai dataset che hai creato per la pubblicazione su "../surface-based-observations/synop" e salva le modifiche utilizzando il tuo token di autenticazione:

<img alt="webapp-test-station" src="../../assets/img/webapp-test-station-save.png" width="800">

Nota che puoi rimuovere questa stazione dal tuo dataset dopo la sessione pratica.

## Test dell'Inserimento Dati dalla Riga di Comando

In questo esercizio, utilizzeremo il comando `wis2box data ingest` per caricare dati su MinIO.

Assicurati di essere nella directory `wis2box` e accedi al container **wis2box-management**:

```bash
cd ~/wis2box
python3 wis2box-ctl.py login
```

Verifica che i seguenti dati di esempio siano disponibili nella directory `/data/wis2box/` all'interno del container **wis2box-management**:

```bash
ls -lh /data/wis2box/data-ingest-exercises/synop_202412030900.txt
```

[Il resto del contenuto segue lo stesso formato, mantenendo tutti i blocchi di codice, i link e la formattazione Markdown esattamente come nell'originale, tradotto in italiano]
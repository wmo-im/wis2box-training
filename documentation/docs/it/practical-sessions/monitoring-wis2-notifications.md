---
title: Monitoraggio delle Notifiche WIS2
---

# Monitoraggio delle Notifiche WIS2

!!! abstract "Risultati dell'apprendimento"

    Al termine di questa sessione pratica, sarai in grado di:
    
    - attivare il flusso di lavoro di wis2box caricando dati in MinIO utilizzando il comando `wis2box data ingest`
    - visualizzare avvisi ed errori mostrati nella dashboard di Grafana
    - verificare il contenuto dei dati pubblicati

## Introduzione

La **dashboard di Grafana** utilizza dati provenienti da Prometheus e Loki per mostrare lo stato del tuo wis2box. Prometheus archivia dati di serie temporali raccolti dalle metriche, mentre Loki archivia i log dei container in esecuzione sulla tua istanza wis2box. Questi dati ti permettono di controllare quanto dati sono ricevuti su MinIO e quante notifiche WIS2 sono pubblicate, e se sono stati rilevati errori nei log.

Per vedere il contenuto delle notifiche WIS2 che vengono pubblicate su diversi argomenti del tuo wis2box puoi utilizzare la scheda 'Monitor' nella **wis2box-webapp**.

## Preparazione

Questa sezione utilizzerà il dataset "surface-based-observations/synop" precedentemente creato nella sessione pratica [Configurazione dei dataset in wis2box](/practical-sessions/configuring-wis2box-datasets).

Accedi alla tua VM studente utilizzando il tuo client SSH (PuTTY o altro).

Assicurati che wis2box sia attivo e funzionante:

```bash
cd ~/wis2box-1.0.0rc1/
python3 wis2box-ctl.py start
python3 wis2box-ctl.py status
```

Assicurati di avere MQTT Explorer in esecuzione e connesso alla tua istanza utilizzando le credenziali pubbliche `everyone/everyone` con un abbonamento all'argomento `origin/a/wis2/#`.

Assicurati di avere accesso all'interfaccia web di MinIO andando su `http://<your-host>:9000` e che tu sia loggato (utilizzando `WIS2BOX_STORAGE_USERNAME` e `WIS2BOX_STORAGE_PASSWORD` dal tuo file `wis2box.env`).

Assicurati di avere un browser web aperto con la dashboard di Grafana per la tua istanza andando su `http://<your-host>:3000`.

## Inserimento di alcuni dati

Esegui i seguenti comandi dalla tua sessione del client SSH:

Copia il file di dati di esempio `aws-example.csv` nella directory che hai definito come `WI2BOX_HOST_DATADIR` nel tuo file `wis2box.env`.

```bash
cp ~/exercise-materials/monitoring-exercises/aws-example.csv ~/wis2box-data/
```

Assicurati di essere nella directory `wis2box-1.0.0rc1` e accedi al container **wis2box-management**:

```bash
cd ~/wis2box-1.0.0rc1
python3 wis2box-ctl.py login
```

Verifica che i dati di esempio siano disponibili nella directory `/data/wis2box/` all'interno del container **wis2box-management**:

```bash
ls -lh /data/wis2box/aws-example.csv
```

!!! note
    Il `WIS2BOX_HOST_DATADIR` è montato come `/data/wis2box/` all'interno del container di gestione wis2box dal file `docker-compose.yml` incluso nella directory `wis2box-1.0.0rc1`.
    
    Questo ti permette di condividere dati tra l'host e il container.

!!! question "Esercizio 1: inserimento dati usando `wis2box data ingest`"

    Esegui il seguente comando per inserire il file di dati di esempio `aws-example.csv` nella tua istanza wis2box:

    ```bash
    wis2box data ingest -p /data/wis2box/aws-example.csv --metadata-id urn:wmo:md:not-my-centre:core.surface-based-observations.synop
    ```

    I dati sono stati inseriti con successo? In caso contrario, quale è stato il messaggio di errore e come puoi risolverlo?

??? success "Clicca per rivelare la risposta"

    Vedrai il seguente output:

    ```bash
    Error: metadata_id=urn:wmo:md:not-my-centre:core.surface-based-observations.synop not found in data mappings
    ```

    Il messaggio di errore indica che l'identificatore dei metadati che hai fornito non corrisponde a nessuno dei dataset che hai configurato nella tua istanza wis2box.

    Fornisci l'id dei metadati corretto che corrisponde al dataset che hai creato nella sessione pratica precedente e ripeti il comando di inserimento dei dati finché non vedrai il seguente output:

    ```bash 
    Processing /data/wis2box/aws-example.csv
    Done
    ```

Vai alla console MinIO nel tuo browser e controlla se il file `aws-example.csv` è stato caricato nel bucket `wis2box-incoming`. Dovresti vedere una nuova directory con il nome del dataset che hai fornito nell'opzione `--metadata-id`:

<img alt="minio-wis2box-incoming-dataset-folder" src="../../assets/img/minio-wis2box-incoming-dataset-folder.png" width="800">

!!! note
    Il comando `wis2box data ingest` ha caricato il file nel bucket `wis2box-incoming` in MinIO in una directory denominata dopo l'identificatore dei metadati che hai fornito.

Vai alla dashboard di Grafana nel tuo browser e controlla lo stato dell'inserimento dei dati.

!!! question "Esercizio 2: verifica lo stato dell'inserimento dei dati"
    
    Vai alla dashboard di Grafana nel tuo browser e verifica lo stato dell'inserimento dei dati.
    
    I dati sono stati inseriti con successo?

??? success "Clicca per rivelare la risposta"
    Il pannello in fondo alla dashboard di Grafana riporta i seguenti avvisi:    
    
    `WARNING - input=aws-example.csv warning=Station 0-20000-0-60355 not in station list; skipping`
    `WARNING - input=aws-example.csv warning=Station 0-20000-0-60360 not in station list; skipping`

    Questo avviso indica che le stazioni non sono definite nella lista delle stazioni del tuo wis2box. Nessuna notifica WIS2 sarà pubblicata per questa stazione finché non la aggiungi alla lista delle stazioni e la associ all'argomento per il tuo dataset.

!!! question "Esercizio 3: aggiungi le stazioni di test e ripeti l'inserimento dei dati"

    Aggiungi le stazioni al tuo wis2box utilizzando l'editor di stazioni in **wis2box-webapp**, e associa le stazioni all'argomento per il tuo dataset.

    Ora ricarica il file di dati di esempio `aws-example.csv` nello stesso percorso in MinIO che hai usato nell'esercizio precedente.

    Controlla la dashboard di Grafana, ci sono nuovi errori o avvisi? Come puoi vedere che i dati di test sono stati inseriti con successo e pubblicati?

??? success "Clicca per rivelare la risposta"

    Puoi controllare i grafici sulla dashboard di Grafana per vedere se i dati di test sono stati inseriti con successo e pubblicati.
    
    In caso di successo, dovresti vedere quanto segue:

    <img alt="grafana_success" src="../../assets/img/grafana_success.png" width="800">

!!! question "Esercizio 4: verifica il broker MQTT per le notifiche WIS2"
    
    Vai a MQTT Explorer e verifica se puoi vedere il Messaggio di Notifica WIS2 per i dati che hai appena inserito.
    
    Quante notifiche di dati WIS2 sono state pubblicate dal tuo wis2box?
    
    Come accedi al contenuto dei dati pubblicati?

??? success "Clicca per rivelare la risposta"

    Dovresti vedere 6 notifiche di dati WIS2 pubblicate dal tuo wis2box.

    Per accedere al contenuto dei dati pubblicati, puoi espandere la struttura dell'argomento per vedere i diversi livelli del messaggio fino a raggiungere l'ultimo livello e rivedere il contenuto del messaggio di uno dei messaggi.

    Il contenuto del messaggio ha una sezione "links" con una chiave "rel" di "canonical" e una chiave "href" con l'URL per scaricare i dati. L'URL sarà nel formato `http://<your-host>/data/...`. 
    
    Nota che il formato dei dati è BUFR e avrai bisogno di un parser BUFR per visualizzare il contenuto dei dati. Il formato BUFR è un formato binario utilizzato dai servizi meteorologici per lo scambio di dati. I plugin di dati all'interno di wis2box hanno trasformato i dati da CSV a BUFR prima di pubblicarli.

## Visualizzazione del contenuto dei dati che hai pubblicato

Puoi utilizzare la **wis2box-webapp** per visualizzare il contenuto delle notifiche di dati WIS2 che sono state pubblicate dal tuo wis2box.

Apri la **wis2box-webapp** nel tuo browser navigando su `http://<your-host>/wis2box-webapp` e seleziona la scheda **Monitoraggio**:

<img alt="wis2box-webapp-monitor" src="../../assets/img/wis2box-webapp-monitor.png" width="220">

Nella scheda di monitoraggio seleziona il tuo id del dataset e clicca "AGGIORNA"

??? question "Esercizio 5: visualizza le notifiche WIS2 nella wis2box-webapp"
    
    Quante notifiche di dati WIS2 sono state pubblicate dal tuo wis2box? 

    Qual è la temperatura dell'aria riportata nell'ultima notifica alla stazione con l'identificatore WIGOS=0-20000-0-60355?

??? success "Clicca per rivelare la risposta"

    Se hai inserito con successo i dati di test, dovresti vedere 6 notifiche di dati WIS2 pubblicate dal tuo wis2box.

    Per vedere la temperatura dell'aria misurata per la stazione con l'identificatore WIGOS=0-20000-0-60355, clicca sul pulsante "ISPEZIONA" accanto al file per quella stazione per aprire una finestra popup che mostra il contenuto analizzato del file di dati. La temperatura dell'aria misurata in questa stazione era di 25,0 gradi Celsius.

!!! Note
    Il container wis2box-api include strumenti per analizzare i file BUFR e visualizzare il contenuto in un formato leggibile dall'uomo. Questo non è un requisito fondamentale per l'implementazione di WIS2.0, ma è stato incluso nel wis2box per aiutare gli editori di dati a verificare il contenuto dei dati che stanno pubblicando.

## Conclusione

!!! success "Congratulazioni!"
    In questa sessione pratica, hai imparato a:

    - attivare il flusso di lavoro di wis2box caricando dati in MinIO usando il comando `wis2box data ingest`
    - visualizzare le notifiche WIS2 pubblicate dal tuo wis2box nella dashboard di Grafana e in MQTT Explorer
    - verificare il contenuto dei dati pubblicati utilizzando la **wis2box-webapp**

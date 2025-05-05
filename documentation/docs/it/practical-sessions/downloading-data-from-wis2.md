---
title: Scaricare e decodificare dati da WIS2
---

# Scaricare e decodificare dati da WIS2

!!! abstract "Obiettivi di apprendimento!"

    Al termine di questa sessione pratica, sarai in grado di:

    - utilizzare il "wis2downloader" per sottoscriverti alle notifiche dei dati WIS2 e scaricare i dati sul tuo sistema locale
    - visualizzare lo stato dei download nella dashboard Grafana
    - decodificare alcuni dati scaricati utilizzando il container "decode-bufr-jupyter"

## Introduzione

In questa sessione imparerai come configurare una sottoscrizione a un WIS2 Broker e scaricare automaticamente i dati sul tuo sistema locale utilizzando il servizio "wis2downloader" incluso in wis2box.

!!! note "Informazioni su wis2downloader"
     
     Il wis2downloader è disponibile anche come servizio autonomo che può essere eseguito su un sistema diverso da quello che pubblica le notifiche WIS2. Consulta [wis2downloader](https://pypi.org/project/wis2downloader/) per maggiori informazioni sull'utilizzo del wis2downloader come servizio autonomo.

     Se desideri sviluppare un tuo servizio per la sottoscrizione alle notifiche WIS2 e il download dei dati, puoi utilizzare il [codice sorgente di wis2downloader](https://github.com/World-Meteorological-Organization/wis2downloader) come riferimento.

!!! Altri strumenti per accedere ai dati WIS2

    I seguenti strumenti possono essere utilizzati anche per scoprire e accedere ai dati da WIS2:

    - [pywiscat](https://github.com/wmo-im/pywiscat) fornisce capacità di ricerca nel WIS2 Global Discovery Catalogue a supporto della reportistica e dell'analisi del Catalogo WIS2 e dei suoi metadati di scoperta associati
    - [pywis-pubsub](https://github.com/World-Meteorological-Organization/pywis-pubsub) fornisce funzionalità di sottoscrizione e download dei dati WMO dall'infrastruttura dei servizi WIS2

## Preparazione

Prima di iniziare, accedi alla tua VM studente e assicurati che la tua istanza wis2box sia attiva e funzionante.

## Visualizzazione della dashboard wis2downloader in Grafana

Apri un browser web e naviga alla dashboard Grafana della tua istanza wis2box andando su `http://YOUR-HOST:3000`.

Fai clic su dashboard nel menu di sinistra, quindi seleziona la **dashboard wis2downloader**.

Dovresti vedere la seguente dashboard:

![dashboard wis2downloader](../assets/img/wis2downloader-dashboard.png)

Questa dashboard si basa sulle metriche pubblicate dal servizio wis2downloader e ti mostrerà lo stato dei download attualmente in corso.

Nell'angolo in alto a sinistra puoi vedere le sottoscrizioni attualmente attive.

Mantieni aperta questa dashboard poiché la utilizzerai per monitorare l'avanzamento del download nel prossimo esercizio.

## Revisione della configurazione wis2downloader

Il servizio wis2downloader avviato dallo stack wis2box può essere configurato utilizzando le variabili d'ambiente definite nel tuo file wis2box.env.

Le seguenti variabili d'ambiente sono utilizzate dal wis2downloader:

    - DOWNLOAD_BROKER_HOST: Il nome host del broker MQTT a cui connettersi. Predefinito a globalbroker.meteo.fr
    - DOWNLOAD_BROKER_PORT: La porta del broker MQTT a cui connettersi. Predefinito a 443 (HTTPS per websockets)
    - DOWNLOAD_BROKER_USERNAME: Il nome utente da utilizzare per connettersi al broker MQTT. Predefinito a everyone
    - DOWNLOAD_BROKER_PASSWORD: La password da utilizzare per connettersi al broker MQTT. Predefinito a everyone
    - DOWNLOAD_BROKER_TRANSPORT: websockets o tcp, il meccanismo di trasporto da utilizzare per connettersi al broker MQTT. Predefinito a websockets
    - DOWNLOAD_RETENTION_PERIOD_HOURS: Il periodo di conservazione in ore per i dati scaricati. Predefinito a 24
    - DOWNLOAD_WORKERS: Il numero di worker di download da utilizzare. Predefinito a 8. Determina il numero di download paralleli.
    - DOWNLOAD_MIN_FREE_SPACE_GB: Lo spazio libero minimo in GB da mantenere sul volume che ospita i download. Predefinito a 1.

Per rivedere la configurazione attuale del wis2downloader, puoi utilizzare il seguente comando:

```bash
cat ~/wis2box/wis2box.env | grep DOWNLOAD
```

!!! question "Revisione della configurazione del wis2downloader"
    
    Qual è il broker MQTT predefinito a cui si connette il wis2downloader?

    Qual è il periodo di conservazione predefinito per i dati scaricati?

??? success "Clicca per rivelare la risposta"

    Il broker MQTT predefinito a cui si connette il wis2downloader è `globalbroker.meteo.fr`.

    Il periodo di conservazione predefinito per i dati scaricati è di 24 ore.

!!! note "Aggiornamento della configurazione del wis2downloader"

    Per aggiornare la configurazione del wis2downloader, puoi modificare il file wis2box.env. Per applicare le modifiche puoi rieseguire il comando di avvio per lo stack wis2box:

    ```bash
    python3 wis2box-ctl.py start
    ```

    E vedrai il servizio wis2downloader riavviarsi con la nuova configurazione.

Puoi mantenere la configurazione predefinita per lo scopo di questo esercizio.

## Aggiunta di sottoscrizioni al wis2downloader

All'interno del container **wis2downloader**, puoi utilizzare la riga di comando per elencare, aggiungere ed eliminare le sottoscrizioni.

Per accedere al container **wis2downloader**, utilizza il seguente comando:

```bash
python3 wis2box-ctl.py login wis2downloader
```

Quindi usa il seguente comando per elencare le sottoscrizioni attualmente attive:

```bash
wis2downloader list-subscriptions
```

Questo comando restituisce un elenco vuoto poiché non ci sono sottoscrizioni attualmente attive.

Per lo scopo di questo esercizio, ci sottoscriveremo al seguente topic `cache/a/wis2/de-dwd-gts-to-wis2/#`, per sottoscriverci ai dati pubblicati dal gateway GTS-to-WIS2 ospitato da DWD e scaricare le notifiche dal Global Cache.

Per aggiungere questa sottoscrizione, utilizza il seguente comando:

```bash
wis2downloader add-subscription --topic cache/a/wis2/de-dwd-gts-to-wis2/#
```

Quindi esci dal container **wis2downloader** digitando `exit`:

```bash
exit
```

Controlla la dashboard wis2downloader in Grafana per vedere la nuova sottoscrizione aggiunta. Attendi qualche minuto e dovresti vedere l'inizio dei primi download. Passa all'esercizio successivo una volta che hai confermato che i download stanno iniziando.

## Visualizzazione dei dati scaricati

Il servizio wis2downloader nello stack wis2box scarica i dati nella directory 'downloads' nella directory che hai definito come WIS2BOX_HOST_DATADIR nel tuo file wis2box.env. Per visualizzare il contenuto della directory downloads, puoi utilizzare il seguente comando:

```bash
ls -R ~/wis2box-data/downloads
```

Nota che i dati scaricati sono memorizzati in directory denominate secondo il topic su cui è stata pubblicata la Notifica WIS2.

## Rimozione delle sottoscrizioni dal wis2downloader

Successivamente, accedi nuovamente al container wis2downloader:

```bash
python3 wis2box-ctl.py login wis2downloader
```

e rimuovi la sottoscrizione che hai fatto dal wis2downloader, utilizzando il seguente comando:

```bash
wis2downloader remove-subscription --topic cache/a/wis2/de-dwd-gts-to-wis2/#
```

Ed esci dal container wis2downloader digitando `exit`:
    
```bash
exit
```

Controlla la dashboard wis2downloader in Grafana per vedere la sottoscrizione rimossa. Dovresti vedere i download che si interrompono.

## Scaricare e decodificare dati per una traccia di ciclone tropicale

In questo esercizio, ti sottoscriverai al WIS2 Training Broker che sta pubblicando dati di esempio per scopi di formazione. Configurerai una sottoscrizione per scaricare i dati per una traccia di ciclone tropicale. Quindi decodificherai i dati scaricati utilizzando il container "decode-bufr-jupyter".

### Sottoscrizione al wis2training-broker e configurazione di una nuova sottoscrizione

Questo dimostra come sottoscriversi a un broker che non è quello predefinito e ti permetterà di scaricare alcuni dati pubblicati dal WIS2 Training Broker.

Modifica il file wis2box.env e cambia DOWNLOAD_BROKER_HOST in `wis2training-broker.wis2dev.io`, cambia DOWNLOAD_BROKER_PORT in `1883` e cambia DOWNLOAD_BROKER_TRANSPORT in `tcp`:

```copy
# downloader settings
DOWNLOAD_BROKER_HOST=wis2training-broker.wis2dev.io
DOWNLOAD_BROKER_PORT=1883
DOWNLOAD_BROKER_USERNAME=everyone
DOWNLOAD_BROKER_PASSWORD=everyone
# download transport mechanism (tcp or websockets)
DOWNLOAD_BROKER_TRANSPORT=tcp
```

Quindi esegui nuovamente il comando 'start' per applicare le modifiche:

```bash
python3 wis2box-ctl.py start
```

Controlla i log del wis2downloader per vedere se la connessione al nuovo broker è avvenuta con successo:

```bash
docker logs wis2downloader
```

Dovresti vedere il seguente messaggio di log:

```copy
...
INFO - Connecting...
INFO - Host: wis2training-broker.wis2dev.io, port: 1883
INFO - Connected successfully
```

Ora configureremo una nuova sottoscrizione al topic per scaricare i dati delle tracce dei cicloni dal WIS2 Training Broker.

Accedi al container **wis2downloader**:

```bash
python3 wis2box-ctl.py login wis2downloader
```

Ed esegui il seguente comando (copia-incolla questo per evitare errori di battitura):

```bash
wis2downloader add-subscription --topic origin/a/wis2/int-wis2-training/data/core/weather/prediction/forecast/medium-range/probabilistic/trajectory
```

Esci dal container **wis2downloader** digitando `exit`.

Attendi fino a quando non vedi i download iniziare nella dashboard wis2downloader in Grafana.

!!! note "Download dei dati dal WIS2 Training Broker"

    Il WIS2 Training Broker è un broker di test utilizzato per scopi di formazione e potrebbe non pubblicare dati in ogni momento.

    Durante le sessioni di formazione in presenza, il formatore locale si assicurerà che il WIS2 Training Broker pubblichi dati per il download.

    Se stai facendo questo esercizio al di fuori di una sessione di formazione, potresti non vedere alcun dato in download.

Verifica che i dati siano stati scaricati controllando nuovamente i log del wis2downloader con:

```bash
docker logs wis2downloader
```

Dovresti vedere un messaggio di log simile al seguente:

```copy
[...] INFO - Message received under topic origin/a/wis2/int-wis2-training/data/core/weather/prediction/forecast/medium-range/probabilistic/trajectory
[...] INFO - Downloaded A_JSXX05ECEP020000_C_ECMP_...
```

### Decodifica dei dati scaricati

Per dimostrare come puoi decodificare i dati scaricati, avvieremo un nuovo container utilizzando l'immagine 'decode-bufr-jupyter'.

Questo container avvierà un server Jupyter notebook sulla tua istanza che include la libreria "ecCodes" che puoi utilizzare per decodificare i dati BUFR.

Utilizzeremo i notebook di esempio inclusi in `~/exercise-materials/notebook-examples` per decodificare i dati scaricati per le tracce dei cicloni.

Per avviare il container, utilizza il seguente comando:

```bash
docker run -d --name decode-bufr-jupyter \
    -v ~/wis2box-data/downloads:/root/downloads \
    -p 8888:8888 \
    -e JUPYTER_TOKEN=dataismagic! \
    mlimper/decode-bufr-jupyter
```

!!! note "Informazioni sul container decode-bufr-jupyter"

    Il container `decode-bufr-jupyter` è un container personalizzato che include la libreria ecCodes ed esegue un server Jupyter notebook. Il container è basato su un'immagine che include la libreria `ecCodes` per decodificare i dati BUFR, insieme a librerie per la visualizzazione e l'analisi dei dati.

    Il comando sopra avvia il container in modalità distaccata, con il nome `decode-bufr-jupyter`, la porta 8888 è mappata sul sistema host e la variabile d'ambiente `JUPYTER_TOKEN` è impostata su `dataismagic!`.
    
    Il comando sopra monta anche la directory `~/wis2box-data/downloads` su `/root/downloads` nel container. Questo assicura che i dati scaricati siano disponibili per il server Jupyter notebook.
    
Una volta avviato il container, puoi accedere al server Jupyter notebook navigando su `http://YOUR-HOST:8888` nel tuo browser web.

Vedrai una schermata che richiede di inserire una "Password or token".

Fornisci il token `dataismagic!` per accedere al server Jupyter notebook.

Dopo l'accesso, dovresti vedere la seguente schermata che elenca le directory nel container:

![Jupyter notebook home](../assets/img/jupyter-files-screen1.png)

Fai doppio clic sulla directory `example-notebooks` per aprirla.

Dovresti vedere la seguente schermata che elenca i notebook di esempio, fai doppio clic sul notebook `tropical_cyclone_track.ipynb` per aprirlo:

![Jupyter notebook example notebooks](../assets/img/jupyter-files-screen2.png)

Ora dovresti essere nel Jupyter notebook per decodificare i dati delle tracce dei cicloni tropicali:

![Jupyter notebook tropical cyclone track](../assets/img/jupyter-tropical-cyclone-track.png)

Leggi le istruzioni nel notebook ed esegui le celle per de
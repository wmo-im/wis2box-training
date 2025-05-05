---
title: Aggiungere intestazioni GTS alle notifiche WIS2
---

# Aggiungere intestazioni GTS alle notifiche WIS2

!!! abstract "Obiettivi di apprendimento"

    Al termine di questa sessione pratica, sarai in grado di:
    
    - configurare una mappatura tra nome file e intestazioni GTS
    - inserire dati con un nome file che corrisponde alle intestazioni GTS
    - visualizzare le intestazioni GTS nelle notifiche WIS2

## Introduzione

I Membri WMO che desiderano interrompere la trasmissione dei loro dati su GTS durante la fase di transizione a WIS2 dovranno aggiungere intestazioni GTS alle loro notifiche WIS2. Queste intestazioni consentono al gateway WIS2-GTS di inoltrare i dati alla rete GTS.

Questo permette ai Membri che sono migrati all'utilizzo di un nodo WIS2 per la pubblicazione dei dati di disabilitare il loro sistema MSS e garantire che i loro dati siano ancora disponibili per i Membri non ancora migrati a WIS2.

La proprietà GTS nel Messaggio di Notifica WIS2 deve essere aggiunta come proprietà aggiuntiva al Messaggio di Notifica WIS2. La proprietà GTS è un oggetto JSON che contiene le intestazioni GTS necessarie per l'inoltro dei dati alla rete GTS.

```json
{
  "gts": {
    "ttaaii": "FTAE31",
    "cccc": "VTBB"
  }
}
```

All'interno di wis2box è possibile aggiungere questo automaticamente alle Notifiche WIS2 fornendo un file aggiuntivo chiamato `gts_headers_mapping.csv` che contiene le informazioni necessarie per mappare le intestazioni GTS ai nomi dei file in arrivo.

Questo file dovrebbe essere posizionato nella directory definita da `WIS2BOX_HOST_DATADIR` nel tuo `wis2box.env` e dovrebbe avere le seguenti colonne:

- `string_in_filepath`: una stringa che fa parte del nome del file che verrà utilizzata per abbinare le intestazioni GTS
- `TTAAii`: l'intestazione TTAAii da aggiungere alla notifica WIS2
- `CCCC`: l'intestazione CCCC da aggiungere alla notifica WIS2

## Preparazione

Assicurati di avere accesso SSH alla tua VM studente e che la tua istanza wis2box sia attiva e funzionante.

Assicurati di essere connesso al broker MQTT della tua istanza wis2box utilizzando MQTT Explorer. Puoi utilizzare le credenziali pubbliche `everyone/everyone` per connetterti al broker.

Assicurati di avere un browser web aperto con la dashboard Grafana per la tua istanza andando su `http://YOUR-HOST:3000`

## Creazione di `gts_headers_mapping.csv`

Per aggiungere intestazioni GTS alle tue notifiche WIS2, è necessario un file CSV che mappi le intestazioni GTS ai nomi dei file in arrivo.

Il file CSV deve essere denominato (esattamente) `gts_headers_mapping.csv` e deve essere posizionato nella directory definita da `WIS2BOX_HOST_DATADIR` nel tuo `wis2box.env`.

## Fornire un file `gts_headers_mapping.csv`
    
Copia il file `exercise-materials/gts-headers-exercises/gts_headers_mapping.csv` nella tua istanza wis2box e posizionalo nella directory definita da `WIS2BOX_HOST_DATADIR` nel tuo `wis2box.env`.

```bash
cp ~/exercise-materials/gts-headers-exercises/gts_headers_mapping.csv ~/wis2box-data
```

Quindi riavvia il container wis2box-management per applicare le modifiche:

```bash
docker restart wis2box-management
```

## Inserimento di dati con intestazioni GTS

Copia il file `exercise-materials/gts-headers-exercises/A_SMRO01YRBK171200_C_EDZW_20240717120502.txt` nella directory definita da `WIS2BOX_HOST_DATADIR` nel tuo `wis2box.env`:

```bash
cp ~/exercise-materials/gts-headers-exercises/A_SMRO01YRBK171200_C_EDZW_20240717120502.txt ~/wis2box-data
```

Quindi accedi al container **wis2box-management**:

```bash
cd ~/wis2box
python3 wis2box-ctl.py login
```

Dalla riga di comando wis2box possiamo inserire il file di dati di esempio `A_SMRO01YRBK171200_C_EDZW_20240717120502.txt` in un dataset specifico come segue:

```bash
wis2box data ingest -p /data/wis2box/A_SMRO01YRBK171200_C_EDZW_20240717120502.txt --metadata-id urn:wmo:md:not-my-centre:core.surface-based-observations.synop
```

Assicurati di sostituire l'opzione `metadata-id` con l'identificatore corretto per il tuo dataset.

Controlla la dashboard Grafana per vedere se i dati sono stati inseriti correttamente. Se vedi AVVISI o ERRORI, prova a correggerli e ripeti l'esercizio con il comando `wis2box data ingest`.

## Visualizzazione delle intestazioni GTS nella Notifica WIS2

Vai su MQTT Explorer e controlla il Messaggio di Notifica WIS2 per i dati che hai appena inserito.

Il Messaggio di Notifica WIS2 dovrebbe contenere le intestazioni GTS che hai fornito nel file `gts_headers_mapping.csv`.

## Conclusione

!!! success "Congratulazioni!"
    In questa sessione pratica, hai imparato a:
      - aggiungere intestazioni GTS alle tue notifiche WIS2
      - verificare che le intestazioni GTS siano disponibili tramite la tua installazione wis2box
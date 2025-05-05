---
title: Template di mappatura da CSV a BUFR
---

# Template di mappatura da CSV a BUFR

!!! abstract "Obiettivi di apprendimento"
    Al termine di questa sessione pratica, sarai in grado di:

    - creare un nuovo template di mappatura BUFR per i tuoi dati CSV
    - modificare e debuggare il tuo template di mappatura BUFR personalizzato dalla riga di comando
    - configurare il plugin di conversione dati CSV-to-BUFR per utilizzare un template di mappatura BUFR personalizzato
    - utilizzare i template integrati AWS e DAYCLI per convertire i dati CSV in BUFR

## Introduzione

I file di dati con valori separati da virgola (CSV) sono spesso utilizzati per registrare dati osservativi e altri dati in formato tabulare.
La maggior parte dei data logger utilizzati per registrare l'output dei sensori sono in grado di esportare le osservazioni in file delimitati, incluso il formato CSV.
Analogamente, quando i dati vengono inseriti in un database è facile esportare i dati richiesti in file formattati CSV.

Il modulo wis2box csv2bufr fornisce uno strumento da riga di comando per convertire i dati CSV in formato BUFR. Quando si utilizza csv2bufr è necessario fornire un template di mappatura BUFR che associa le colonne CSV ai corrispondenti elementi BUFR. Se non vuoi creare il tuo template di mappatura, puoi utilizzare i template integrati AWS e DAYCLI per convertire i dati CSV in BUFR, ma dovrai assicurarti che i dati CSV che stai utilizzando siano nel formato corretto per questi template. Se vuoi decodificare parametri non inclusi nei template AWS e DAYCLI, dovrai creare il tuo template di mappatura.

In questa sessione imparerai come creare il tuo template di mappatura per convertire i dati CSV in BUFR. Imparerai anche come utilizzare i template integrati AWS e DAYCLI per convertire i dati CSV in BUFR.

## Preparazione

Assicurati che wis2box-stack sia stato avviato con `python3 wis2box.py start`

Assicurati di avere un browser web aperto con l'interfaccia MinIO per la tua istanza andando su `http://YOUR-HOST:9000`
Se non ricordi le tue credenziali MinIO, puoi trovarle nel file `wis2box.env` nella directory `wis2box` sulla tua VM studente.

Assicurati di avere MQTT Explorer aperto e connesso al tuo broker utilizzando le credenziali `everyone/everyone`.

## Creazione di un template di mappatura

Il modulo csv2bufr viene fornito con uno strumento da riga di comando per creare il tuo template di mappatura utilizzando un set di sequenze BUFR e/o elementi BUFR come input.

Per trovare specifiche sequenze ed elementi BUFR puoi fare riferimento alle tabelle BUFR su [https://confluence.ecmwf.int/display/ECC/BUFR+tables](https://confluence.ecmwf.int/display/ECC/BUFR+tables).

### Strumento da riga di comando csv2bufr mappings

Per accedere allo strumento da riga di comando csv2bufr, devi accedere al container wis2box-api:

```bash
cd ~/wis2box
python3 wis2box-ctl.py login wis2box-api
```

Per stampare la pagina di aiuto per il comando `csv2bufr mapping`:

```bash
csv2bufr mappings --help
```

La pagina di aiuto mostra 2 sottocomandi:

- `csv2bufr mappings create` : Crea un nuovo template di mappatura
- `csv2bufr mappings list` : Elenca i template di mappatura disponibili nel sistema

!!! Note "csv2bufr mapping list"

    Il comando `csv2bufr mapping list` ti mostrerà i template di mappatura disponibili nel sistema.
    I template predefiniti sono memorizzati nella directory `/opt/wis2box/csv2bufr/templates` nel container.

    Per condividere template di mappatura personalizzati con il sistema puoi memorizzarli nella directory definita da `$CSV2BUFR_TEMPLATES`, che è impostata di default su `/data/wis2box/mappings` nel container. Poiché la directory `/data/wis2box/mappings` nel container è montata nella directory `$WIS2BOX_HOST_DATADIR/mappings` sull'host, troverai i tuoi template di mappatura personalizzati nella directory `$WIS2BOX_HOST_DATADIR/mappings` sull'host.

Proviamo a creare un nuovo template di mappatura personalizzato utilizzando il comando `csv2bufr mapping create` usando come input la sequenza BUFR 301150 più l'elemento BUFR 012101.

```bash
csv2bufr mappings create 301150 012101 --output /data/wis2box/mappings/my_custom_template.json
```

Puoi controllare il contenuto del template di mappatura appena creato utilizzando il comando `cat`:

```bash
cat /data/wis2box/mappings/my_custom_template.json
```

!!! question "Ispezione del template di mappatura"

    Quante colonne CSV vengono mappate agli elementi BUFR? Qual è l'intestazione CSV per ogni elemento BUFR mappato?

??? success "Clicca per rivelare la risposta"
    
    Il template di mappatura che hai creato mappa **5** colonne CSV agli elementi BUFR, ovvero i 4 elementi BUFR nella sequenza 301150 più l'elemento BUFR 012101.

    Le seguenti colonne CSV vengono mappate agli elementi BUFR:

    - **wigosIdentifierSeries** mappa a `"eccodes_key": "#1#wigosIdentifierSeries"` (elemento BUFR 001125)
    - **wigosIssuerOfIdentifier** mappa a `"eccodes_key": "#1#wigosIssuerOfIdentifier` (elemento BUFR 001126)
    - **wigosIssueNumber** mappa a `"eccodes_key": "#1#wigosIssueNumber"` (elemento BUFR 001127)
    - **wigosLocalIdentifierCharacter** mappa a `"eccodes_key": "#1#wigosLocalIdentifierCharacter"` (elemento BUFR 001128)
    - **airTemperature** mappa a `"eccodes_key": "#1#airTemperature"` (elemento BUFR 012101)

Il template di mappatura che hai creato manca di importanti metadati sull'osservazione effettuata, la data e l'ora dell'osservazione, e la latitudine e longitudine della stazione.

Ora aggiorneremo il template di mappatura aggiungendo le seguenti sequenze:
    
- **301011** per la Data (Anno, mese, giorno)
- **301012** per l'Ora (Ora, minuto)
- **301023** per la Posizione (Latitudine/longitudine (accuratezza approssimativa))

E i seguenti elementi:

- **010004** per la Pressione
- **007031** per l'Altezza del barometro sul livello medio del mare

Esegui il seguente comando per aggiornare il template di mappatura:

```bash
csv2bufr mappings create 301150 301011 301012 301023 007031 012101 010004  --output /data/wis2box/mappings/my_custom_template.json
```

E ispeziona nuovamente il contenuto del template di mappatura:

```bash
cat /data/wis2box/mappings/my_custom_template.json
```

!!! question "Ispezione del template di mappatura aggiornato"

    Quante colonne CSV vengono ora mappate agli elementi BUFR? Qual è l'intestazione CSV per ogni elemento BUFR mappato?

??? success "Clicca per rivelare la risposta"
    
    Il template di mappatura che hai creato ora mappa **18** colonne CSV agli elementi BUFR:
    - 4 elementi BUFR dalla sequenza BUFR 301150
    - 3 elementi BUFR dalla sequenza BUFR 301011
    - 2 elementi BUFR dalla sequenza BUFR 301012
    - 2 elementi BUFR dalla sequenza BUFR 301023
    - elemento BUFR 007031
    - elemento BUFR 012101

    Le seguenti colonne CSV vengono mappate agli elementi BUFR:

    - **wigosIdentifierSeries** mappa a `"eccodes_key": "#1#wigosIdentifierSeries"` (elemento BUFR 001125)
    - **wigosIssuerOfIdentifier** mappa a `"eccodes_key": "#1#wigosIssuerOfIdentifier` (elemento BUFR 001126)
    - **wigosIssueNumber** mappa a `"eccodes_key": "#1#wigosIssueNumber"` (elemento BUFR 001127)
    - **wigosLocalIdentifierCharacter** mappa a `"eccodes_key": "#1#wigosLocalIdentifierCharacter"` (elemento BUFR 001128)
    - **year** mappa a `"eccodes_key": "#1#year"` (elemento BUFR 004001)
    - **month** mappa a `"eccodes_key": "#1#month"` (elemento BUFR 004002)
    - **day** mappa a `"eccodes_key": "#1#day"` (elemento BUFR 004003)
    - **hour** mappa a `"eccodes_key": "#1#hour"` (elemento BUFR 004004)
    - **minute** mappa a `"eccodes_key": "#1#minute"` (elemento BUFR 004005)
    - **latitude** mappa a `"eccodes_key": "#1#latitude"` (elemento BUFR 005002)
    - **longitude** mappa a `"eccodes_key": "#1#longitude"` (elemento BUFR 006002)
    - **heightOfBarometerAboveMeanSeaLevel"** mappa a `"eccodes_key": "#1#heightOfBarometerAboveMeanSeaLevel"` (elemento BUFR 007031)
    - **airTemperature** mappa a `"eccodes_key": "#1#airTemperature"` (elemento BUFR 012101)
    - **nonCoordinatePressure** mappa a `"eccodes_key": "#1#nonCoordinatePressure"` (elemento BUFR 010004)

Controlla il contenuto del file `custom_template_data.csv` nella directory `/root/data-conversion-exercises`:

```bash
cat /root/data-conversion-exercises/custom_template_data.csv
```

Nota che le intestazioni di questo file CSV sono le stesse delle intestazioni CSV nel template di mappatura che hai creato.

Per testare la conversione dei dati possiamo utilizzare lo strumento da riga di comando `csv2bufr` per convertire il file CSV in BUFR utilizzando il template di mappatura che abbiamo creato:

```bash
csv2bufr data transform --bufr-template my_custom_template /root/data-conversion-exercises/custom_template_data.csv
```

Dovresti vedere il seguente output:

```bash
CLI:    ... Transforming /root/data-conversion-exercises/custom_template_data.csv to BUFR ...
CLI:    ... Processing subsets:
CLI:    ..... 94 bytes written to ./WIGOS_0-20000-0-15015_20250412T210000.bufr4
CLI:    End of processing, exiting.
```

!!! question "Controlla il contenuto del file BUFR"
    
    Come puoi controllare il contenuto del file BUFR appena creato e verificare che abbia codificato correttamente i dati?

??? success "Clicca per rivelare la risposta"

    Puoi utilizzare il comando `bufr_dump -p` per controllare il contenuto del file BUFR che hai appena creato.
    Il comando ti mostrerà il contenuto del file BUFR in un formato leggibile.

    ```bash
    bufr_dump -p ./WIGOS_0-20000-0-15015_20250412T210000.bufr4
    ```

    Nell'output vedrai i valori per gli elementi BUFR che hai mappato nel template, per esempio la "airTemperature" mostrerà:
    
    ```bash
    airTemperature=298.15
    ```

Ora puoi uscire dal container:

```bash
exit
```

### Utilizzo del template di mappatura in wis2box

Per assicurarti che il nuovo template di mappatura sia riconosciuto dal container wis2box-api, devi riavviare il container:

```bash
docker restart wis2box-api
```

Ora puoi configurare il tuo dataset nel wis2box-webapp per utilizzare il template di mappatura personalizzato per il plugin di conversione da CSV a BUFR.

Il wis2box-webapp rileverà automaticamente il template di mappatura che hai creato e lo renderà disponibile nell'elenco dei template per il plugin di conversione da CSV a BUFR.

Fai clic sul dataset che hai creato nella sessione pratica precedente e fai clic su "UPDATE" accanto al plugin con nome "CSV data converted to BUFR":

<img alt="Immagine che mostra l'editor del dataset nel wis2box-webapp" src="../../assets/img/wis2box-webapp-data-mapping-update-csv2bufr.png"/>

Dovresti vedere il nuovo template che hai creato nell'elenco dei template disponibili:

<img alt="Immagine che mostra i template csv2bufr nel wis2box-webapp" src="../../assets/img/wis2box-webapp-csv2bufr-templates.png"/>

!!! hint

    Nota che se non vedi il nuovo template che hai creato, prova ad aggiornare la pagina o ad aprirla in una nuova finestra in incognito.

Per ora mantieni la selezione predefinita del template AWS (clicca in alto a destra per chiudere la configurazione del plugin).

## Utilizzo del template 'AWS'

Il template 'AWS' fornisce un template di mappatura per convertire i dati CSV in sequenze BUFR 301150, 307096, a supporto dei requisiti minimi GBON.

La descrizione del template AWS può essere trovata qui [aws-template](/csv2bufr-templates/aws-template).

### Revisione dei dati di input aws-example

Scarica l'esempio per questo esercizio dal link seguente:

[aws-example.csv](/sample-data/aws-example.csv)

Apri il file che hai scaricato in un editor e ispeziona il contenuto:

!!! question
    Esaminando i campi di data, ora e identificazione (identificatori WIGOS e tradizionali) cosa
    noti? Come verrebbe rappresentata la data odierna?

??? success "Clicca per rivelare la risposta"
    Ogni colonna contiene un singolo pezzo di informazione. Per esempio la data è divisa in
    anno, mese e giorno, rispecchiando come i dati sono memorizzati in BUFR. La data odierna sarebbe
    divisa tra le colonne "year", "month" e "day". Analogamente, l'ora deve essere
    divisa in "hour" e "minute" e l'identificatore della stazione WIGOS nei suoi risp
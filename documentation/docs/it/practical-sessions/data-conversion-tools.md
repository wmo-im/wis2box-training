---
title: Strumenti di Conversione dei Dati
---

# Strumenti di Conversione dei Dati

!!! abstract "Risultati dell'Apprendimento"
    Al termine di questa sessione pratica, sarai in grado di:

    - Accedere agli strumenti da riga di comando ecCodes all'interno del container wis2box-api
    - Utilizzare lo strumento synop2bufr per convertire i rapporti SYNOP FM-12 in BUFR dalla riga di comando
    - Attivare la conversione synop2bufr tramite wis2box-webapp
    - Utilizzare lo strumento csv2bufr per convertire dati CSV in BUFR dalla riga di comando

## Introduzione

I dati pubblicati su WIS2 devono soddisfare i requisiti e gli standard definiti dalle varie comunità di esperti di discipline/dominio del sistema terrestre. Per abbassare la barriera alla pubblicazione dei dati per le osservazioni superficiali terrestri, wis2box fornisce strumenti per convertire i dati in formato BUFR. Questi strumenti sono disponibili tramite il container wis2box-api e possono essere utilizzati dalla riga di comando per testare il processo di conversione dei dati.

Le principali conversioni attualmente supportate da wis2box sono i rapporti SYNOP FM-12 in BUFR e i dati CSV in BUFR. I dati FM-12 sono supportati poiché sono ancora ampiamente utilizzati e scambiati nella comunità WMO, mentre i dati CSV sono supportati per consentire la mappatura dei dati prodotti dalle stazioni meteorologiche automatiche in formato BUFR.

### Informazioni su FM-12 SYNOP

I rapporti meteorologici superficiali dalle stazioni di superficie terrestre sono stati storicamente riportati ogni ora o nelle ore sinottiche principali (00, 06, 12 e 18 UTC) e intermedie (03, 09, 15, 21 UTC). Prima della migrazione a BUFR, questi rapporti erano codificati nel formato di codice SYNOP FM-12 in testo semplice. Sebbene la migrazione a BUFR fosse programmata per essere completata entro il 2012, un gran numero di rapporti viene ancora scambiato nel formato SYNOP FM-12 legacy. Ulteriori informazioni sul formato FM-12 SYNOP possono essere trovate nel Manuale WMO sui Codici, Volume I.1 (WMO-No. 306, Volume I.1).

### Informazioni su ecCodes

La libreria ecCodes è un insieme di librerie software e utilità progettate per decodificare e codificare dati meteorologici nei formati GRIB e BUFR. È sviluppata dal Centro Europeo per le Previsioni Meteorologiche a Medio Termine (ECMWF), consulta la [documentazione ecCodes](https://confluence.ecmwf.int/display/ECC/ecCodes+documentation) per maggiori informazioni.

Il software wis2box include la libreria ecCodes nell'immagine di base del container wis2box-api. Questo consente agli utenti di accedere agli strumenti da riga di comando e alle librerie all'interno del container. La libreria ecCodes è utilizzata all'interno dello stack wis2box per decodificare e codificare i messaggi BUFR.

### Informazioni su csv2bufr e synop2bufr

Oltre a ecCodes, wis2box utilizza i seguenti moduli Python che lavorano con ecCodes per convertire i dati in formato BUFR:

- **synop2bufr**: per supportare il formato SYNOP FM-12 legacy tradizionalmente utilizzato dagli osservatori manuali. Il modulo synop2bufr si basa su metadati aggiuntivi della stazione per codificare parametri aggiuntivi nel file BUFR. Consulta il [repository synop2bufr su GitHub](https://github.com/World-Meteorological-Organization/synop2bufr)
- **csv2bufr**: per abilitare la conversione dei dati estratti CSV prodotti dalle stazioni meteorologiche automatiche in formato BUFR. Il modulo csv2bufr è utilizzato per convertire i dati CSV in formato BUFR utilizzando un template di mappatura che definisce come i dati CSV dovrebbero essere mappati al formato BUFR. Consulta il [repository csv2bufr su GitHub](https://github.com/World-Meteorological-Organization/csv2bufr)

Questi moduli possono essere utilizzati autonomamente o come parte dello stack wis2box.

## Preparazione

!!! warning "Prerequisiti"

    - Assicurati che il tuo wis2box sia stato configurato e avviato
    - Assicurati di aver configurato un dataset e configurato almeno una stazione nel tuo wis2box
    - Connettiti al broker MQTT della tua istanza wis2box utilizzando MQTT Explorer
    - Apri l'applicazione web wis2box (`http://YOUR-HOST/wis2box-webapp`) e assicurati di aver effettuato l'accesso
    - Apri la dashboard Grafana per la tua istanza andando su `http://YOUR-HOST:3000`

Per utilizzare gli strumenti da riga di comando BUFR, dovrai essere connesso al container wis2box-api. A meno che non sia specificato diversamente, tutti i comandi dovrebbero essere eseguiti su questo container. Avrai anche bisogno di avere MQTT Explorer aperto e connesso al tuo broker.

Prima, connettiti alla tua VM studente tramite il tuo client SSH e copia i materiali dell'esercizio nel container wis2box-api:

```bash
docker cp ~/exercise-materials/data-conversion-exercises wis2box-api:/root
```

Poi accedi al container wis2box-api e cambia la directory dove si trovano i materiali dell'esercizio:

```bash
cd ~/wis2box
python3 wis2box-ctl.py login wis2box-api
cd /root/data-conversion-exercises
```

Conferma che gli strumenti siano disponibili, iniziando con ecCodes:

```bash
bufr_dump -V
```

Dovresti ottenere la seguente risposta:

```
ecCodes Version 2.36.0
```

Successivamente, verifica la versione di synop2bufr:

```bash
synop2bufr --version
```

Dovresti ottenere la seguente risposta:

```
synop2bufr, version 0.7.0
```

Successivamente, verifica csv2bufr:

```bash
csv2bufr --version
```

Dovresti ottenere la seguente risposta:

```
csv2bufr, version 0.8.5
```

## Strumenti da riga di comando ecCodes

La libreria ecCodes inclusa nel container wis2box-api fornisce numerosi strumenti da riga di comando per lavorare con i file BUFR.
I prossimi esercizi dimostreranno come utilizzare `bufr_ls` e `bufr_dump` per verificare il contenuto di un file BUFR.

### bufr_ls

In questo primo esercizio, utilizzerai il comando `bufr_ls` per ispezionare gli header di un file BUFR e determinare il tipo dei contenuti del file.

Utilizza il seguente comando per eseguire `bufr_ls` sul file `bufr-cli-ex1.bufr4`:

```bash
bufr_ls bufr-cli-ex1.bufr4
```

Dovresti vedere il seguente output:

```bash
bufr-cli-ex1.bufr4
centre                     masterTablesVersionNumber  localTablesVersionNumber   typicalDate                typicalTime                numberOfSubsets
cnmc                       29                         0                          20231002                   000000                     1
1 of 1 messages in bufr-cli-ex1.bufr4

1 of 1 total messages in 1 file
```

È possibile passare varie opzioni a `bufr_ls` per modificare sia il formato che i campi dell'intestazione stampati.

!!! question

    Qual sarebbe il comando per elencare l'output precedente in formato JSON?

    Puoi eseguire il comando `bufr_ls` con il flag `-h` per vedere le opzioni disponibili.

??? success "Clicca per rivelare la risposta"
    Puoi cambiare il formato di output in JSON usando il flag `-j`, ovvero
    ```bash
    bufr_ls -j bufr-cli-ex1.bufr4
    ```

    Quando eseguito, questo dovrebbe darti il seguente output:
    ```
    { "messages" : [
      {
        "centre": "cnmc",
        "masterTablesVersionNumber": 29,
        "localTablesVersionNumber": 0,
        "typicalDate": 20231002,
        "typicalTime": "000000",
        "numberOfSubsets": 1
      }
    ]}
    ```

L'output stampato rappresenta i valori di alcune delle chiavi dell'intestazione nel file BUFR.

Da solo, queste informazioni non sono molto informative, con solo informazioni limitate sui contenuti del file fornite.

Quando si esamina un file BUFR, spesso vogliamo determinare il tipo di dati contenuti nel file e la data/ora tipica dei dati nel file. Queste informazioni possono essere elencate utilizzando il flag `-p` per selezionare le intestazioni da output. Più intestazioni possono essere incluse utilizzando un elenco separato da virgole.

Puoi utilizzare il seguente comando per elencare la categoria dei dati, la sottocategoria, la data tipica e l'ora:

```bash
bufr_ls -p dataCategory,internationalDataSubCategory,typicalDate,typicalTime -j bufr-cli-ex1.bufr4
```

!!! question

    Esegui il comando precedente e interpreta l'output utilizzando [Common Code Table C-13](https://github.com/wmo-im/CCT/blob/master/C13.csv) per determinare la categoria dei dati e la sottocategoria.

    Che tipo di dati (categoria dei dati e sottocategoria) sono contenuti nel file? Qual è la data e l'ora tipiche per i dati?

??? success "Clicca per rivelare la risposta"

    ```
    { "messages" : [
      {
        "dataCategory": 2,
        "internationalDataSubCategory": 4,
        "typicalDate": 20231002,
        "typicalTime": "000000"
      }
    ]}
    ```

    Da questo, vediamo che:

    - La categoria dei dati è 2, indicando dati di **"Sondaggi verticali (diversi da quelli satellitari)"**.
    - La sottocategoria internazionale è 4, indicando dati di **"Rapporti di temperatura/umidità/vento di livello superiore da stazioni fisse terrestri (TEMP)"**.
    - La data e l'ora tipiche sono 2023-10-02 e 00:00:00z, rispettivamente.

### bufr_dump

Il comando `bufr_dump` può essere utilizzato per elencare ed esaminare i contenuti di un file BUFR, inclusi i dati stessi.

Prova a eseguire il comando `bufr_dump` sul secondo file di esempio `bufr-cli-ex2.bufr4`:

```{.copy}
bufr_dump bufr-cli-ex2.bufr4
```

Questo risultato in un JSON che può essere difficile da analizzare, prova a utilizzare il flag `-p` per output i dati in formato di testo semplice (formato chiave=valore):

```{.copy}
bufr_dump -p bufr-cli-ex2.bufr4
```

Dovresti vedere un gran numero di chiavi come output, molte delle quali mancanti. Questo è tipico con i dati del mondo reale poiché non tutte le chiavi eccodes sono popolate con dati riportati.

Puoi utilizzare il comando `grep` per filtrare l'output e mostrare solo le chiavi che non sono mancanti. Ad esempio, per mostrare tutte le chiavi che non sono mancanti, puoi utilizzare il seguente comando:

```{.copy}
bufr_dump -p bufr-cli-ex2.bufr4 | grep -v MISSING
```

!!! question

    Qual è la pressione ridotta al livello del mare riportata nel file BUFR `bufr-cli-ex2.bufr4`?

??? success "Clicca per rivelare la risposta"

    Utilizzando il seguente comando:

    ```bash
    bufr_dump -p bufr-cli-ex2.bufr4 | grep -i 'pressureReducedToMeanSeaLevel'
    ```

    Dovresti vedere il seguente output:

    ```
    pressureReducedToMeanSeaLevel=105590
    ```
    Questo indica che la pressione ridotta al livello del mare è 105590 Pa (1055.90 hPa).

!!! question

    Qual è l'identificatore della stazione WIGOS della stazione che ha riportato i dati nel file BUFR `bufr-cli-ex2.bufr4`?

??? success "Clicca per rivelare la risposta"

    Utilizzando il seguente comando:

    ```bash
    bufr_dump -p bufr-cli-ex2.bufr4 | grep -i 'wigos'
    ```

    Dovresti vedere il seguente output:

    ```
    wigosIdentifierSeries=0
    wigosIssuerOfIdentifier=20000
    wigosIssueNumber=0
    wigosLocalIdentifierCharacter="99100"
    ```

    Questo indica che l'identificatore della stazione WIGOS è `0-20000-0-99100`.

## Conversione synop2bufr

Successivamente, esaminiamo come convertire i dati SYNOP FM-12 in formato BUFR utilizzando il modulo `synop2bufr`. Il modulo `synop2bufr` è utilizzato per convertire i dati SYNOP FM-12 in formato BUFR. Il modulo è installato nel container wis2box-api e può essere utilizzato dalla riga di comando come segue:

```{.copy}
synop2bufr data transform \
    --metadata <station-metadata.csv> \
    --output-dir <output-directory-path> \
    --year <year-of-observation> \
    --month <month-of-observation> \
    <input-fm12.txt>
```

L'argomento `--metadata` è utilizzato per specificare il file di metadati della stazione, che fornisce informazioni aggiuntive da codificare nel file BUFR.
L'argomento `--output-dir` è utilizzato per specificare la directory dove verranno scritti i file BUFR convertiti. Gli argomenti `--year` e `--month` sono utilizzati per specificare l'anno e il mese dell'osservazione.

Il modulo `synop2bufr` è utilizzato anche nel wis2box-webapp per convertire i dati SYNOP FM-12 in formato BUFR utilizzando un modulo di input basato sul web.

I prossimi esercizi dimostreranno come funziona il modulo `synop2bufr` e come utilizzarlo per convertire i dati SYNOP FM-12 in formato BUFR.

### esamina il messaggio SYNOP di esempio

Ispeziona il file del messaggio SYNOP di esempio per questo esercizio `synop_message.txt`:

```bash
cd /root/data-conversion-exercises
more synop_message.txt
```

!!! question

    Quanti rapporti SYNOP ci sono in questo file?

??? success "Clicca per rivelare la risposta"

    L'output mostra il seguente:

    ```{.copy}
    AAXX 21121
    15015 02999 02501 10103 21090 39765 42952 57020 60001=
    15020 02997 23104 10130 21075 30177 40377 58020 60001 81041=
    15090 02997 53102 10139 21075 30271 40364 58031 60001 82046=
    ```

    Ci sono 3 rapporti SYNOP nel file, corrispondenti a 3 diverse stazioni (identificate dagli identificatori tradizionali delle stazioni a 5 cifre: 15015, 15020 e 15090).
    Nota che la fine di ogni rapporto è segnata dal carattere `=`.

### esamina l'elenco delle stazioni

L'argomento `--metadata` richiede un file CSV utilizzando un formato predefinito, un esempio funzionante è fornito nel file `station_list.csv`:

Utilizza il seguente comando per ispezionare il contenuto del file `station_list.csv`:

```bash
more station_list.csv
```

!!! question

    Quante stazioni sono elencate nella lista delle stazioni? Quali sono gli identificatori delle stazioni WIGOS presenti nella lista?

??? success "Clicca per rivelare la risposta"

    L'output mostra quanto segue:

    ```{.copy}
    station_name,wigos_station_identifier,traditional_station_identifier,facility_type,latitude,longitude,elevation,barometer_height,territory_name,wmo_region
    OCNA SUGATAG,0-20000-0-15015,15015,landFixed,47.7770616258,23.9404602638,503.0,504.0,ROU,europe
    BOTOSANI,0-20000-0-15020,15020,landFixed,47.7356532437,26.6455501701,161.0,162.1,ROU,europe
    ```

    Questo corrisponde ai metadati delle stazioni per 2 stazioni: per gli identificatori delle stazioni WIGOS `0-20000-0-15015` e `0-20000-0-15020`.

### converti SYNOP in BUFR

Successivamente, utilizza il seguente comando per convertire il messaggio FM-12 SYNOP in formato BUFR:

```bash
synop2bufr data transform --metadata station_list.csv --output-dir ./ --year 2024 --month 09 synop_message.txt
```

!!! question
    Quanti file BUFR sono stati creati? Cosa significa il messaggio di WARNING nell'output?

??? success "Clicca per rivelare la risposta"
    L'output mostra quanto segue:

    ```{.copy}
    [WARNING] Station 15090 not found in station file
    ```

    Se controlli il contenuto della tua directory con il comando `ls -lh`, dovresti vedere che sono stati creati 2 nuovi file BUFR: `WIGOS_0-20000-0-15015_20240921T120000.bufr4` e `WIGOS_0-20000-0-15020_20240921T120000.bufr4`.

    Il messaggio di avviso indica che la stazione con l'identificatore di stazione tradizionale `15090` non è stata trovata nel file della lista delle stazioni `station_list.csv`. Questo significa che il rapporto SYNOP per questa stazione non è stato convertito in formato BUFR.

!!! question
    Controlla il contenuto del file BUFR `WIGOS_0-20000-0-15015_20240921T120000.bufr4` utilizzando il comando `bufr_dump`. 

    Puoi verificare che le informazioni fornite nel file `station_list.csv` siano presenti nel file BUFR?

??? success "Clicca per rivelare la risposta"
    Puoi utilizzare il seguente comando per controllare il contenuto del file BUFR:

    ```bash
    bufr_dump -p WIGOS_0-20000-0-15015_20240921T120000.bufr4 | grep -v MISSING
    ```

    Noterai il seguente output:

    ```{.copy}
    wigosIdentifierSeries=0
    wigosIssuerOfIdentifier=20000
    wigosIssueNumber=0
    wigosLocalIdentifierCharacter="15015"
    blockNumber=15
    stationNumber=15
    stationOrSiteName="OCNA SUGATAG"
    stationType=1
    year=2024
    month=9
    day=21
    hour=12
    minute=0
    latitude=47.7771
    longitude=23.9405
    heightOfStationGroundAboveMeanSeaLevel=503
    heightOfBarometerAboveMeanSeaLevel=504
    ```

    Nota che questo include i dati forniti dal file `station_list.csv`.

### Modulo SYNOP in wis2box-webapp

Il modulo `synop2bufr` è utilizzato anche nel wis2box-webapp per convertire i dati FM-12 SYNOP in formato BUFR utilizzando un modulo di input basato sul web.
Per testare questo, vai all'indirizzo `http://YOUR-HOST/wis2box-webapp` e accedi.

Seleziona il modulo `SYNOP Form` dal menu a sinistra e copia incolla il contenuto del file `synop_message.txt`:

```{.copy}
AAXX 21121
15015 02999 02501 10103 21090 39765 42952 57020 60001=
15020 02997 23104 10130 21075 30177 40377 58020 60001 81041=
15090 02997 53102 10139 21075 30271 40364 58031 60001 82046=
```

Nell'area di testo `SYNOP message`:

<img alt="synop-form" src="../../assets/img/wis2box-webapp-synop-form.png" width="800">

!!! question
    Sei in grado di inviare il modulo? Qual è il risultato?

??? success "Clicca per rivelare la risposta"

    Devi selezionare un dataset e fornire il token per "processes/wis2box" che hai creato nell'esercizio precedente per inviare il modulo.

    Se fornisci un token non valido, vedrai:
    
    - Risultato: Non autorizzato, fornire un token 'processes/wis2box' valido

    Se fornisci un token valido, vedrai "WARNINGS: 3". Clicca su "WARNINGS" per aprire il menu a discesa che mostrerà:

    - Stazione 15015 non trovata nel file delle stazioni
    - Stazione 15020 non trovata nel file delle stazioni
    - Stazione 15090 non trovata nel file delle stazioni

    Per convertire questi dati in formato BUFR, dovresti configurare le stazioni corrispondenti nel tuo wis2box e assicurarti che le stazioni siano associate al topic per il tuo dataset.

!!! note

    Nell'esercizio per [ingesting-data-for-publication](ingesting-data-for-publication.md) hai inserito il file "synop_202412030900.txt" ed è stato convertito in formato BUFR dal modulo synop2bufr.

    Nel flusso di lavoro automatizzato nel wis2box, l'anno e il mese sono estratti automaticamente dal nome del file e utilizzati per popolare gli argomenti `--year` e `--month` richiesti da synop2bufr, mentre i metadati della stazione sono estratti automaticamente dalla configurazione della stazione nel wis2box.

## conversione csv2bufr

!!! note
    Assicurati di essere ancora connesso al container wis2box-api e nella directory `/root/data-conversion-exercises`, se hai lasciato il container nell'esercizio precedente, puoi accedere di nuovo come segue:

    ```bash
    cd ~/wis2box
    python3 wis2box-ctl.py login wis2box-api
    cd /root/data-conversion-exercises
    ```

Ora vediamo come convertire i dati CSV in formato BUFR utilizzando il modulo `csv2bufr`. Il modulo è installato nel container wis2box-api e può essere utilizzato dalla riga di comando come segue:

```{.copy}
csv2bufr data transform \
    --bufr-template <bufr-mapping-template> \
    <input-csv-file>
```

L'argomento `--bufr-template` è utilizzato per specificare il file di template di mappatura BUFR, che fornisce il mappaggio tra i dati CSV di input e i dati BUFR di output specificati in un file JSON. I template di mappatura predefiniti sono installati nella directory `/opt/csv2bufr/templates` nel container wis2box-api.

### rivedi il file CSV di esempio

Rivedi il contenuto del file CSV di esempio `aws-example.csv`:

```bash
more aws-example.csv
```

!!! question
    Quante righe di dati ci sono nel file CSV? Qual è l'identificatore della stazione WIGOS delle stazioni che riportano nel file CSV?

??? question "Clicca per rivelare la risposta"

    L'output mostra quanto segue:

    ```{.copy}
    wsi_series,wsi_issuer,wsi_issue_number,wsi_local,wmo_block_number,wmo_station_number,station_type,year,month,day,hour,minute,latitude,longitude,station_height_above_msl,barometer_height_above_msl,station_pressure,msl_pressure,geopotential_height,thermometer_height,air_temperature,dewpoint_temperature,relative_humidity,method_of_ground_state_measurement,ground_state,method_of_snow_depth_measurement,snow_depth,precipitation_intensity,anemometer_height,time_period_of_wind,wind_direction,wind_speed,maximum_wind_gust_direction_10_minutes,maximum_wind_gust_speed_10_minutes,maximum_wind_gust_direction_1_hour,maximum_wind_gust_speed_1_hour,maximum_wind_gust_direction_3_hours,maximum_wind_gust_speed_3_hours,rain_sensor_height,total_precipitation_1_hour,total_precipitation_3_hours,total_precipitation_6_hours,total_precipitation_12_hours,total_precipitation_24_hours
    0,20000,0,60355,60,355,1,2024,3,31,1,0,47.77706163,23.94046026,503,504.43,100940,101040,1448,5,298.15,294.55,80,3,1,1,0,0.004,10,-10,30,3,30,5,40,9,20,11,2,4.7,5.3,7.9,9.5,11.4
    0,20000,0,60355,60,355,1,2024,3,31,2,0,47.77706163,23.94046026,503,504.43,100940,101040,1448,5,25.,294.55,80,3,1,1,0,0.004,10,-10,30,3,30,5,40,9,20,11,2,4.7,5.3,7.9,9.5,11.4
    0,20000,0,60355,60,355,1,2024,3,31,3,0,47.77706163,23.94046026,503,504.43,100940,101040,1448,5,298.15,294.55,80,3,1,1,0,0.004,10,-10,30,3,30,5,40,9,20,11,2,4.7,5.3,7.9,9.5,11.4
    ```

    La prima riga del file CSV contiene le intestazioni delle colonne, che sono utilizzate per identificare i dati in ogni colonna.

    Dopo la riga di intestazione, ci sono 3 righe di dati, che rappresentano 3 osservazioni meteorologiche dalla stessa stazione con l'identificatore della stazione WIGOS `0-20000-0-60355` a tre diversi timestamp `2024-03-31 01:00:00`, `2024-03-31 02:00:00` e `2024-03-31 03:00:00`.

### rivedi il template aws

Il wis2box-api include un insieme di template di mappatura BUFR predefiniti che sono installati nella directory `/opt/csv2bufr/templates`.

Controlla il contenuto della directory `/opt/csv2bufr/templates`:

```bash
ls /opt/csv2bufr/templates
```
Dovresti vedere il seguente output:

```{.copy}
CampbellAfrica-v1-template.json  aws-template.json  daycli-template.json
```

Verifichiamo il contenuto del file `aws-template.json`:

```bash
cat /opt/csv2bufr/templates/aws-template.json
```

Questo restituisce un ampio file JSON, che fornisce il mappaggio per 43 colonne CSV.

!!! question
    A quale colonna CSV è mappata la chiave eccodes `airTemperature`? Quali sono i valori minimi e massimi validi per questa chiave?

??? success "Clicca per rivelare la risposta"

    Utilizzando il seguente comando per filtrare l'output:

    ```bash
    cat /opt/csv2bufr/templates/aws-template.json | grep -i airTemperature
    ```
    Dovresti vedere il seguente output:

    ```{.copy}
    {"eccodes_key": "#1#airTemperature", "value": "data:air_temperature", "valid_min": "const:193.15", "valid_max": "const:333.15"},
    ```

    Il valore che sarà codificato per la chiave eccodes `airTemperature` sarà preso dai dati nella colonna CSV: **air_temperature**.

    I valori minimi e massimi per questa chiave sono `193.15` e `333.15`, rispettivamente.

!!! question

    A quale colonna CSV è mappata la chiave eccodes `internationalDataSubCategory`? Qual è il valore di questa chiave?

??? success "Clicca per rivelare la risposta"
    Utilizzando il seguente comando per filtrare l'output:

    ```bash
    cat /opt/csv2bufr/templates/aws-template.json | grep -i internationalDataSubCategory
    ```
    Dovresti vedere il seguente output:

    ```{.copy}
    {"eccodes_key": "internationalDataSubCategory", "value": "const:2"},
    ```

    **Non c'è nessuna colonna CSV mappata alla chiave eccodes `internationalDataSubCategory`**, invece il valore costante 2 è utilizzato e sarà codificato in tutti i file BUFR prodotti con questo template di mappatura.

### converti CSV in BUFR

Proviamo a convertire il file in formato BUFR utilizzando il comando `csv2bufr`:

```{.copy}
csv2bufr data transform --bufr-template aws-template ./aws-example.csv
```

!!! question
    Quanti file BUFR sono stati creati?

??? success "Clicca per rivelare la risposta"

    L'output mostra quanto segue:

    ```{.copy}
    CLI:    ... Transforming ./aws-example.csv to BUFR ...
    CLI:    ... Processing subsets:
    CLI:    ..... 384 bytes written to ./WIGOS_0-20000-0-60355_20240331T010000.bufr4
    #1#airTemperature: Value (25.0) out of valid range (193.15 - 333.15).; Element set to missing
    CLI:    ..... 384 bytes written to ./WIGOS_0-20000-0-60355_20240331T020000.bufr4
    CLI:    ..... 384 bytes written to ./WIGOS_0-20000-0-60355_20240331T030000.bufr4
    CLI:    End of processing, exiting.
    ```

    L'output indica che sono stati creati 3 file BUFR: `WIGOS_0-20000-0-60355_20240331T010000.bufr4`, `WIGOS_0-20000-0-60355_20240331T020000.bufr4` e `WIGOS_0-20000-0-60355_20240331T030000.bufr4`.

Per controllare il contenuto dei file BUFR ignorando i valori mancanti, puoi utilizzare il seguente comando:

```bash
bufr_dump -p WIGOS_0-20000-0-60355_20240331T010000.bufr4 | grep -v MISSING
```

!!! question
    Qual è il valore della chiave eccodes `airTemperature` nel file BUFR `WIGOS_0-20000-0-60355_20240331T010000.bufr4`? E nel file BUFR `WIGOS_0-20000-0-60355_20240331T020000.bufr4`?

??? success "Clicca per rivelare la risposta"
    Per filtrare l'output, puoi utilizzare il seguente comando:

    ```bash
    bufr_dump -p WIGOS_0-20000-0-60355_20240331T010000.bufr4 | grep -v MISSING | grep airTemperature
    ```
    Dovresti vedere il seguente output:

    ```{.copy}
    #1#airTemperature=298.15
    ```

    Mentre per il secondo file:

    ```bash
    bufr_dump -p WIGOS_0-20000-0-60355_20240331T020000.bufr4 | grep -v MISSING | grep airTemperature
    ```

Non ottieni alcun risultato, indicando che il valore per la chiave `airTemperature` è mancante nel file BUFR `WIGOS_0-20000-0-60355_20240331T020000.bufr4`. Il csv2bufr ha rifiutato di codificare il valore `25.0` dai dati CSV poiché è fuori dall'intervallo valido di `193.15` e `333.15` come definito nel template di mappatura.

Nota che la conversione da CSV a BUFR utilizzando uno dei template di mappatura BUFR predefiniti ha delle limitazioni:

- il file CSV deve essere nel formato definito nel template di mappatura, ovvero i nomi delle colonne CSV devono corrispondere ai nomi definiti nel template di mappatura
- puoi codificare solo le chiavi definite nel template di mappatura
- i controlli di qualità sono limitati ai controlli definiti nel template di mappatura

Per informazioni su come creare e utilizzare template di mappatura BUFR personalizzati vedi il prossimo esercizio pratico [csv2bufr-templates](./csv2bufr-templates.md).

## Conclusione

!!! success "Congratulazioni!"
    In questa sessione pratica hai imparato:

    - come accedere agli strumenti da linea di comando ecCodes all'interno del contenitore wis2box-api
    - come utilizzare `synop2bufr` per convertire i rapporti SYNOP FM-12 in BUFR dalla linea di comando
    - come utilizzare il Form SYNOP nel wis2box-webapp per convertire i rapporti SYNOP FM-12 in BUFR
    - come utilizzare `csv2bufr` per convertire dati CSV in BUFR dalla linea di comando
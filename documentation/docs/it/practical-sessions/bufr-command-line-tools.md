---
title: Lavorare con i dati BUFR
---

# Lavorare con i dati BUFR

!!! abstract "Risultati dell'apprendimento"
    In questa sessione pratica verrai introdotto ad alcuni degli strumenti BUFR inclusi nel contenitore **wis2box-api** che sono utilizzati per trasformare i dati in formato BUFR e per leggere il contenuto codificato in BUFR.
    
    Imparerai:

    - come ispezionare gli header nel file BUFR usando il comando `bufr_ls`
    - come estrarre e ispezionare i dati all'interno di un file bufr usando `bufr_dump`
    - la struttura di base dei template bufr utilizzati in csv2bufr e come utilizzare lo strumento da linea di comando
    - e come apportare modifiche di base ai template bufr e come aggiornare il wis2box per utilizzare la versione rivista

## Introduzione

I plugin che producono notifiche con dati BUFR utilizzano processi nel wis2box-api per lavorare con i dati BUFR, ad esempio per trasformare i dati da CSV a BUFR o da BUFR a geojson.

Il contenitore wis2box-api include numerosi strumenti per lavorare con i dati BUFR.

Questi includono gli strumenti sviluppati dall'ECMWF e inclusi nel software ecCodes, maggiori informazioni su questi possono essere trovate sul [sito web ecCodes](https://confluence.ecmwf.int/display/ECC/BUFR+tools).

In questa sessione verrai introdotto ai comandi `bufr_ls` e `bufr_dump` dal pacchetto software ecCodes e alla configurazione avanzata dello strumento csv2bufr.

## Preparazione

Per utilizzare gli strumenti da linea di comando BUFR dovrai essere loggato nel contenitore wis2box-api e, a meno che non sia specificato diversamente, tutti i comandi dovrebbero essere eseguiti su questo contenitore. Avrai anche bisogno di avere MQTT Explorer aperto e connesso al tuo broker.

Prima connettiti alla tua VM studente tramite il tuo client ssh e poi accedi al contenitore wis2box-api:

```{.copy}
cd ~/wis2box-1.0.0rc1
python3 wis2box-ctl.py login wis2box-api
```

Conferma che gli strumenti sono disponibili, iniziando con ecCodes:

``` {.copy}
bufr_dump -V
```
Dovresti ottenere la seguente risposta:

```
ecCodes Version 2.28.0
```

Successivamente controlla csv2bufr:

```{.copy}
csv2bufr --version
```

Dovresti ottenere la seguente risposta:

```
csv2bufr, version 0.7.4
```

Infine, crea una directory di lavoro in cui lavorare:

```{.copy}
cd /data/wis2box
mkdir -p working/bufr-cli
cd working/bufr-cli
```

Ora sei pronto per iniziare a utilizzare gli strumenti BUFR.


## Utilizzo degli strumenti da linea di comando BUFR

### Esercizio 1 - bufr_ls
In questo primo esercizio utilizzerai il comando `bufr_ls` per ispezionare gli header di un file BUFR e per determinare il contenuto del file. I seguenti header sono inclusi in un file BUFR:

| header                            | chiave ecCodes                  | descrizione                                                                                                                                           |
|-----------------------------------|------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------|
| centro di origine/generazione     | centre                       | Il centro di origine / generazione per i dati                                                                                                      |
| sottocentro di origine/generazione | bufrHeaderSubCentre          | Il sottocentro di origine / generazione per i dati                                                                                                  | 
| Numero di sequenza di aggiornamento            | updateSequenceNumber         | Se questa è la prima versione dei dati (0) o un aggiornamento (>0)                                                                                   |               
| Categoria dei dati                     | dataCategory                 | Il tipo di dati contenuti nel messaggio BUFR, ad es. dati di superficie. Vedi [Tabella A BUFR](https://github.com/wmo-im/BUFR4/blob/master/BUFR_TableA_en.csv)  |
| Sottocategoria dei dati internazionali   | internationalDataSubCategory | Il sottotipo di dati contenuti nel messaggio BUFR, ad es. dati di superficie. Vedi [Tabella dei codici comuni C-13](https://github.com/wmo-im/CCT/blob/master/C13.csv) |
| Anno                              | typicalYear (typicalDate)    | Il tempo più tipico per i contenuti del messaggio BUFR                                                                                                       |
| Mese                             | typicalMonth (typicalDate)   | Il tempo più tipico per i contenuti del messaggio BUFR                                                                                                       |
| Giorno                               | typicalDay (typicalDate)     | Il tempo più tipico per i contenuti del messaggio BUFR                                                                                                       |
| Ora                              | typicalHour (typicalTime)    | Il tempo più tipico per i contenuti del messaggio BUFR                                                                                                       |
| Minuto                            | typicalMinute (typicalTime)  | Il tempo più tipico per i contenuti del messaggio BUFR                                                                                                       |
| Descrittori BUFR                  | unexpandedDescriptors        | Lista di uno o più descrittori BUFR che definiscono i dati contenuti nel file                                                                        |

Scarica il file di esempio direttamente nel contenitore di gestione wis2box utilizzando il seguente comando:

``` {.copy}
curl https://training.wis2box.wis.wmo.int/sample-data/bufr-cli-ex1.bufr4 --output bufr-cli-ex1.bufr4
```

Ora usa il seguente comando per eseguire `bufr_ls` su questo file:

```bash
bufr_ls bufr-cli-ex1.bufr4
```

Dovresti vedere il seguente output:

```bash
bufr-cli-ex1.bufr4
centre                     masterTablesVersionNumber  localTablesVersionNumber   typicalDate                typicalTime                numberOfSubsets
cnmc                       29                         0                          20231002                   000000                     1
1 of 1 messages in bufr-cli-ex1.bufr4

1 of 1 total messages in 1 files
```

Da solo queste informazioni non sono molto informative, con solo informazioni limitate sui contenuti del file fornite.

L'output predefinito non fornisce informazioni sul tipo di osservazione o dati ed è in un formato che non è molto facile da leggere. Tuttavia, è possibile passare varie opzioni a `bufr_ls` per cambiare sia il formato che i campi dell'header stampati.

Usa `bufr_ls` senza argomenti per visualizzare le opzioni:

```{.copy}
bufr_ls
```

Dovresti vedere il seguente output:

```
NAME    bufr_ls

DESCRIPTION
        List content of BUFR files printing values of some header keys.
        Only scalar keys can be printed.
        It does not fail when a key is not found.

USAGE
        bufr_ls [options] bufr_file bufr_file ...

OPTIONS
        -p key[:{s|d|i}],key[:{s|d|i}],...
                Declaration of keys to print.
                For each key a string (key:s), a double (key:d) or an integer (key:i)
                type can be requested. Default type is string.
        -F format
                C style format for floating-point values.
        -P key[:{s|d|i}],key[:{s|d|i}],...
                As -p adding the declared keys to the default list.
        -w key[:{s|d|i}]{=|!=}value,key[:{s|d|i}]{=|!=}value,...
                Where clause.
                Messages are processed only if they match all the key/value constraints.
                A valid constraint is of type key=value or key!=value.
                For each key a string (key:s), a double (key:d) or an integer (key:i)
                type can be specified. Default type is string.
                In the value you can also use the forward-slash character '/' to specify an OR condition (i.e. a logical disjunction)
                Note: only one -w clause is allowed.
        -j      JSON output
        -s key[:{s|d|i}]=value,key[:{s|d|i}]=value,...
                Key/values to set.
                For each key a string (key:s), a double (key:d) or an integer (key:i)
                type can be defined. By default the native type is set.
        -n namespace
                All the keys belonging to the given namespace are printed.
        -m      Mars keys are printed.
        -V      Version.
        -W width
                Minimum width of each column in output. Default is 10.
        -g      Copy GTS header.
        -7      Does not fail when the message has wrong length

SEE ALSO
        Full documentation and examples at:
        <https://confluence.ecmwf.int/display/ECC/bufr_ls>
```

Ora esegui lo stesso comando sul file di esempio ma visualizza le informazioni in formato JSON.

!!! question
    Quale flag passi al comando `bufr_ls` per visualizzare l'output in formato JSON?

??? success "Clicca per rivelare la risposta"
    Puoi cambiare il formato di output in json usando il flag `-j`, ad es.
    `bufr_ls -j <input-file>`. Questo può essere più leggibile rispetto al formato di output predefinito. Vedi l'output di esempio qui sotto:

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

Quando esaminiamo un file BUFR spesso vogliamo determinare il tipo di dati contenuti nel file e la data/ora tipica dei dati nel file. Queste informazioni possono essere elencate utilizzando il flag `-p` per selezionare gli header da output. Più header possono essere inclusi usando una lista separata da virgole.

Usando il comando `bufr_ls` ispeziona il file di test e identifica il tipo di dati contenuti nel file e la data e l'ora tipiche per tali dati.

??? hint
    Le chiavi ecCodes sono date nella tabella sopra. Possiamo usare le seguenti per elencare la dataCategory e
    internationalDataSubCategory dei dati BUFR:

    ```
    bufr_ls -p dataCategory,internationalDataSubCategory bufr-cli-ex1.bufr4
    ```

    È possibile aggiungere ulteriori chiavi come richiesto.

!!! question
    Quale tipo di dati (categoria dei dati e sottocategoria) sono contenuti nel file? Qual è la data e l'ora tipiche
    per i dati?

??? success "Clicca per rivelare la risposta"
    Il comando che dovresti aver eseguito dovrebbe essere stato simile a:
    
    ```
    bufr_ls -p dataCategory,internationalDataSubCategory,typicalDate,typicalTime -j bufr-cli-ex1.bufr4
    ```

    Potresti aver aggiunto ulteriori chiavi, o elencato l'anno, il mese, il giorno ecc. individualmente. L'output dovrebbe
    essere simile a quello qui sotto, a seconda che tu abbia selezionato l'output JSON o l'output predefinito.

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

    Da questo vediamo che:

    - La categoria dei dati è 2, dalla [Tabella A BUFR](https://github.com/wmo-im/BUFR4/blob/master/BUFR_TableA_en.csv)
      possiamo vedere che questo file contiene dati "Vertical soundings (other than satellite)".
    - La sottocategoria internazionale è 4, indicando 
      "Upper-level temperature/humidity/wind reports from fixed-land stations (TEMP)" dati. Queste informazioni possono essere cercate
      nella [Tabella dei codici comuni C-13](https://github.com/wmo-im/CCT/blob/master/C13.csv) (riga 33). Nota la combinazione
      di categoria e sottocategoria.
    - La data e l'ora tipiche sono rispettivamente 2023/10/02 e 00:00:00z.

    

### Esercizio 2 - bufr_dump

Il comando `bufr_dump` può essere utilizzato per elencare ed esaminare i contenuti di un file BUFR, inclusi i dati stessi.

In questo esercizio utilizzeremo un file BUFR che è lo stesso creato durante la sessione pratica iniziale csv2bufr utilizzando il wis2box-webapp.

Scarica il file di esempio direttamente nel contenitore di gestione wis2box con il seguente comando:

``` {.copy}
curl https://training.wis2box.wis.wmo.int/sample-data/bufr-cli-ex2.bufr4 --output bufr-cli-ex2.bufr4
```

Ora esegui il comando `bufr_dump` sul file, utilizzando il flag `-p` per output i dati in formato di testo semplice (formato chiave=valore):

```{.copy}
bufr_dump -p bufr-cli-ex2.bufr4
```

Dovresti vedere circa 240 chiavi in output, molte delle quali sono mancanti. Questo è tipico con i dati del mondo reale poiché non tutte le chiavi eccodes sono popolate con dati segnalati.

!!! hint
    I valori mancanti possono essere filtrati utilizzando strumenti come `grep`:
    ```{.copy}
    bufr_dump -p bufr-cli-ex2.bufr4 | grep -v MISSING
    ```

Il file BUFR di esempio per questo esercizio proviene dalla sessione pratica csv2bufr. Si prega di scaricare il file CSV originale nella tua posizione corrente come segue:

```{.copy}
curl https://training.wis2box.wis.wmo.int/sample-data/csv2bufr-ex1.csv --output csv2bufr-ex1.csv
```

E visualizza il contenuto del file con:

```{.copy}
more csv2bufr-ex1.csv
```

!!! question
    Usa il seguente comando per visualizzare la colonna 18 nel file CSV e troverai la pressione media del livello del mare segnalata (msl_pressure):

    ```{.copy}
    more csv2bufr-ex1.csv | cut -d ',' -f 18
    ```
    
    Quale chiave nell'output BUFR corrisponde alla pressione media del livello del mare?

??? hint
    Strumenti come `grep` possono essere utilizzati in combinazione con `bufr_dump`. Ad esempio:
    
    ```{.copy}
    bufr_dump -p bufr-cli-ex2.bufr4 | grep -i "pressure"
    ```
    
    filtrerebbe i contenuti di `bufr_dump` solo per quelle righe contenenti la parola pressione. In alternativa, 
    l'output potrebbe essere filtrato su un valore.

??? success "Clicca per rivelare la risposta"
    La chiave "pressureReducedToMeanSeaLevel" corrisponde alla colonna msl_pressure nel file CSV di input.

Trascorri qualche minuto esaminando il resto dell'output, confrontandolo con il file CSV di input prima di passare all'esercizio successivo. Ad esempio, puoi provare a trovare le chiavi nell'output BUFR che corrispondono all'umidità relativa (colonna 23 nel file CSV) e alla temperatura dell'aria (colonna 21 nel file CSV).

### Esercizio 3 - file di mappatura csv2bufr

Lo strumento csv2bufr può essere configurato per elaborare dati tabellari con colonne e sequenze BUFR diverse.

Questo viene fatto tramite un file di configurazione scritto in formato JSON.

Come i dati BUFR stessi, il file JSON contiene una sezione di intestazione e una sezione di dati, che corrispondono in modo approssimativo alle stesse sezioni in BUFR.

Inoltre, alcune opzioni di formattazione sono specificate all'interno del file JSON.

Il file JSON per il mapping predefinito può essere visualizzato tramite il link qui sotto (clic destro e apri in una nuova scheda):

[aws-template.json](https://raw.githubusercontent.com/wmo-im/csv2bufr/main/csv2bufr/templates/resources/aws-template.json)

Esamina la sezione `header` del file di mappatura (mostrata di seguito) e confrontala con la tabella dell'esercizio 1 (colonna chiave ecCodes):

```
"header":[
    {"eccodes_key": "edition", "value": "const:4"},
    {"eccodes_key": "masterTableNumber", "value": "const:0"},
    {"eccodes_key": "bufrHeaderCentre", "value": "const:0"},
    {"eccodes_key": "bufrHeaderSubCentre", "value": "const:0"},
    {"eccodes_key": "updateSequenceNumber", "value": "const:0"},
    {"eccodes_key": "dataCategory", "value": "const:0"},
    {"eccodes_key": "internationalDataSubCategory", "value": "const:2"},
    {"eccodes_key": "masterTablesVersionNumber", "value": "const:30"},
    {"eccodes_key":
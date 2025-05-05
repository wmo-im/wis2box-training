---
title: Strumenti di Conversione Dati
---

# Strumenti di Conversione Dati

!!! abstract "Obiettivi di Apprendimento"
    Al termine di questa sessione pratica, sarai in grado di:

    - Accedere agli strumenti da riga di comando ecCodes all'interno del container wis2box-api
    - Utilizzare lo strumento synop2bufr per convertire i report FM-12 SYNOP in BUFR dalla riga di comando
    - Attivare la conversione synop2bufr tramite wis2box-webapp
    - Utilizzare lo strumento csv2bufr per convertire dati CSV in BUFR dalla riga di comando

## Introduzione

I dati pubblicati su WIS2 devono soddisfare i requisiti e gli standard definiti dalle varie comunità di esperti delle discipline del sistema Terra. Per abbassare la barriera alla pubblicazione dei dati per le osservazioni di superficie terrestri, wis2box fornisce strumenti per convertire i dati in formato BUFR. Questi strumenti sono disponibili tramite il container wis2box-api e possono essere utilizzati dalla riga di comando per testare il processo di conversione dei dati.

Le principali conversioni attualmente supportate da wis2box sono i report FM-12 SYNOP in BUFR e i dati CSV in BUFR. I dati FM-12 sono supportati poiché sono ancora ampiamente utilizzati e scambiati nella comunità WMO, mentre i dati CSV sono supportati per consentire la mappatura dei dati prodotti dalle stazioni meteorologiche automatiche nel formato BUFR.

### Informazioni su FM-12 SYNOP

I report meteorologici di superficie dalle stazioni terrestri sono stati storicamente segnalati ogni ora o nelle ore sinottiche principali (00, 06, 12 e 18 UTC) e intermedie (03, 09, 15, 21 UTC). Prima della migrazione a BUFR, questi report erano codificati nel formato di testo semplice FM-12 SYNOP. Sebbene la migrazione a BUFR fosse prevista per il 2012, un gran numero di report viene ancora scambiato nel formato legacy FM-12 SYNOP. Ulteriori informazioni sul formato FM-12 SYNOP sono disponibili nel Manuale WMO sui Codici, Volume I.1 (WMO-No. 306, Volume I.1).

### Informazioni su ecCodes

La libreria ecCodes è un insieme di librerie software e utilità progettate per decodificare e codificare dati meteorologici nei formati GRIB e BUFR. È sviluppata dal Centro Europeo per le Previsioni Meteorologiche a Medio Termine (ECMWF), consulta la [documentazione ecCodes](https://confluence.ecmwf.int/display/ECC/ecCodes+documentation) per maggiori informazioni.

Il software wis2box include la libreria ecCodes nell'immagine base del container wis2box-api. Questo permette agli utenti di accedere agli strumenti da riga di comando e alle librerie dall'interno del container. La libreria ecCodes viene utilizzata all'interno dello stack wis2box per decodificare e codificare i messaggi BUFR.

### Informazioni su csv2bufr e synop2bufr

Oltre a ecCodes, wis2box utilizza i seguenti moduli Python che lavorano con ecCodes per convertire i dati in formato BUFR:

- **synop2bufr**: per supportare il formato legacy FM-12 SYNOP tradizionalmente utilizzato dagli osservatori manuali. Il modulo synop2bufr si basa su metadati aggiuntivi delle stazioni per codificare parametri aggiuntivi nel file BUFR. Vedi il [repository synop2bufr su GitHub](https://github.com/World-Meteorological-Organization/synop2bufr)
- **csv2bufr**: per abilitare la conversione di estratti CSV prodotti da stazioni meteorologiche automatiche in formato BUFR. Il modulo csv2bufr viene utilizzato per convertire dati CSV in formato BUFR utilizzando un template di mappatura che definisce come i dati CSV devono essere mappati nel formato BUFR. Vedi il [repository csv2bufr su GitHub](https://github.com/World-Meteorological-Organization/csv2bufr)

Questi moduli possono essere utilizzati autonomamente o come parte dello stack wis2box.

## Preparazione

!!! warning "Prerequisiti"

    - Assicurati che il tuo wis2box sia stato configurato e avviato
    - Assicurati di aver configurato un dataset e almeno una stazione nel tuo wis2box
    - Connettiti al broker MQTT della tua istanza wis2box usando MQTT Explorer
    - Apri l'applicazione web wis2box (`http://YOUR-HOST/wis2box-webapp`) e assicurati di aver effettuato l'accesso
    - Apri la dashboard Grafana per la tua istanza andando su `http://YOUR-HOST:3000`

Per utilizzare gli strumenti BUFR da riga di comando, dovrai essere connesso al container wis2box-api. Se non diversamente specificato, tutti i comandi devono essere eseguiti su questo container. Dovrai anche avere MQTT Explorer aperto e connesso al tuo broker.

Prima, connettiti alla tua VM studente tramite il tuo client SSH e copia i materiali dell'esercizio nel container wis2box-api:

```bash
docker cp ~/exercise-materials/data-conversion-exercises wis2box-api:/root
```

Quindi accedi al container wis2box-api e spostati nella directory dove si trovano i materiali dell'esercizio:

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

Poi, verifica csv2bufr:

```bash
csv2bufr --version
```

Dovresti ottenere la seguente risposta:

```
csv2bufr, version 0.8.5
```

## Strumenti da riga di comando ecCodes

La libreria ecCodes inclusa nel container wis2box-api fornisce diversi strumenti da riga di comando per lavorare con i file BUFR. 
I prossimi esercizi dimostrano come utilizzare `bufr_ls` e `bufr_dump` per controllare il contenuto di un file BUFR.

### bufr_ls

In questo primo esercizio, utilizzerai il comando `bufr_ls` per ispezionare le intestazioni di un file BUFR e determinare il tipo di contenuto del file.

Usa il seguente comando per eseguire `bufr_ls` sul file `bufr-cli-ex1.bufr4`:

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

Varie opzioni possono essere passate a `bufr_ls` per modificare sia il formato che i campi di intestazione stampati.

!!! question
     
    Quale sarebbe il comando per elencare l'output precedente in formato JSON?

    Puoi eseguire il comando `bufr_ls` con il flag `-h` per vedere le opzioni disponibili.

??? success "Clicca per rivelare la risposta"
    Puoi cambiare il formato di output in JSON usando il flag `-j`, cioè
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

L'output stampato rappresenta i valori di alcune delle chiavi di intestazione nel file BUFR.

Da solo, questo non è molto informativo, con solo informazioni limitate sul contenuto del file fornite.

Quando si esamina un file BUFR, spesso vogliamo determinare il tipo di dati contenuti nel file e la data/ora tipica dei dati nel file. Queste informazioni possono essere elencate usando il flag `-p` per selezionare le intestazioni da visualizzare. È possibile includere più intestazioni utilizzando un elenco separato da virgole.

Puoi utilizzare il seguente comando per elencare la categoria di dati, la sottocategoria, la data tipica e l'ora:
    
```bash
bufr_ls -p dataCategory,internationalDataSubCategory,typicalDate,typicalTime -j bufr-cli-ex1.bufr4
```

!!! question

    Esegui il comando precedente e interpreta l'output utilizzando [Common Code Table C-13](https://github.com/wmo-im/CCT/blob/master/C13.csv) per determinare la categoria e sottocategoria dei dati.

    Che tipo di dati (categoria e sottocategoria) sono contenuti nel file? Qual è la data e l'ora tipica per i dati?

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

    - La categoria di dati è 2, che indica dati di **"Sondaggi verticali (diversi da satellite)"**.
    - La sottocategoria internazionale è 4, che indica **"Report di temperatura/umidità/vento in quota da stazioni terrestri fisse (TEMP)"**.
    - La data e l'ora tipiche sono rispettivamente 2023-10-02 e 00:00:00z.

### bufr_dump

Il comando `bufr_dump` può essere utilizzato per elencare ed esaminare il contenuto di un file BUFR, inclusi i dati stessi.

Prova a eseguire il comando `bufr_dump` sul secondo file di esempio `bufr-cli-ex2.bufr4`:

```{.copy}
bufr_dump bufr-cli-ex2.bufr4
```

Questo produce un JSON che può essere difficile da analizzare, prova a utilizzare il flag `-p` per visualizzare i dati in formato testo semplice (formato chiave=valore):

```{.copy}
bufr_dump -p bufr-cli-ex2.bufr4
```

Vedrai un gran numero di chiavi come output, molte delle quali sono mancanti. Questo è tipico con dati del mondo reale poiché non tutte le chiavi eccodes sono popolate con dati riportati.

Puoi utilizzare il comando `grep` per filtrare l'output e mostrare solo le chiavi che non sono mancanti. Per esempio, per mostrare tutte le chiavi che non sono mancanti, puoi utilizzare il seguente comando:

```{.copy}
bufr_dump -p bufr-cli-ex2.bufr4 | grep -v MISSING
```

!!! question

    Qual è la pressione ridotta al livello del mare riportata nel file BUFR `bufr-cli-ex2.bufr4`?

??? success "Clicca per rivelare la risposta"

    Usando il seguente comando:

    ```bash
    bufr_dump -p bufr-cli-ex2.bufr4 | grep -i 'pressureReducedToMeanSeaLevel'
    ```

    Dovresti vedere il seguente output:

    ```
    pressureReducedToMeanSeaLevel=105590
    ```
    Questo indica che la pressione ridotta al livello del mare è 105590 Pa (1055.90 hPa).

!!! question

    Qual è l'identificatore WIGOS della stazione che ha riportato i dati nel file BUFR `bufr-cli-ex2.bufr4`?

??? success "Clicca per rivelare la risposta"

    Usando il seguente comando:

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

    Questo indica che l'identificatore WIGOS della stazione è `0-20000-0-99100`.

## Conversione synop2bufr

Ora vediamo come convertire i dati FM-12 SYNOP in formato BUFR utilizzando il modulo `synop2bufr`. Il modulo `synop2bufr` viene utilizzato per convertire i dati FM-12 SYNOP in formato BUFR. Il modulo è installato nel container wis2box-api e può essere utilizzato dalla riga di comando come segue:

```{.copy}
synop2bufr data transform \
    --metadata <station-metadata.csv> \
    --output-dir <output-directory-path> \
    --year <year-of-observation> \
    --month <month-of-observation> \
    <input-fm12.txt>
```

L'argomento `--metadata` viene utilizzato per specificare il file dei metadati della stazione, che fornisce informazioni aggiuntive da codificare nel file BUFR.
L'argomento `--output-dir` viene utilizzato per specificare la directory dove verranno scritti i file BUFR convertiti. Gli argomenti `--year` e `--month` vengono utilizzati per specificare l'anno e il mese dell'osservazione.

Il modulo `synop2bufr` viene utilizzato anche nel wis2box-webapp per convertire i dati FM-12 SYNOP in formato BUFR utilizzando un modulo di input basato sul web.

I prossimi esercizi dimostreranno come funziona il modulo `synop2bufr` e come utilizzarlo per convertire i dati FM-12 SYNOP in formato BUFR.

### revisione del messaggio SYNOP di esempio

Ispeziona il file del messaggio SYNOP di esempio per questo esercizio `synop_message.txt`:

```bash
cd /root/data-conversion-exercises
more synop_message.txt
```

!!! question

    Quanti report SYNOP sono presenti in questo file?

??? success "Clicca per rivelare
---
title: Conversione dei dati SYNOP in BUFR
---

# Conversione dei dati SYNOP in BUFR dalla riga di comando

!!! abstract "Risultati dell'apprendimento"
    Al termine di questa sessione pratica, sarai in grado di:

    - utilizzare lo strumento synop2bufr per convertire i rapporti SYNOP FM-12 in BUFR;
    - diagnosticare e correggere semplici errori di codifica nei rapporti SYNOP FM-12 prima della conversione del formato;

## Introduzione

I rapporti meteorologici di superficie dalle stazioni di superficie terrestre sono stati storicamente riportati ogni ora o nelle principali 
(00, 06, 12 e 18 UTC) e ore sinottiche intermedie (03, 09, 15, 21 UTC). Prima della migrazione
a BUFR, questi rapporti erano codificati nel formato di codice SYNOP FM-12 in testo semplice. Sebbene la migrazione a BUFR
fosse programmata per essere completata entro il 2012, un gran numero di rapporti viene ancora scambiato nel formato legacy 
FM-12 SYNOP. Ulteriori informazioni sul formato FM-12 SYNOP possono essere trovate nel Manuale WMO sui Codici, 
Volume I.1 (WMO-No. 306, Volume I.1).

[Manuale WMO sui Codici, Volume I.1](https://library.wmo.int/records/item/35713-manual-on-codes-international-codes-volume-i-1)

Per facilitare il completamento della migrazione a BUFR, sono stati sviluppati alcuni strumenti per
codificare i rapporti SYNOP FM-12 in BUFR, in questa sessione imparerai come utilizzare questi strumenti così
come la relazione tra le informazioni contenute nei rapporti SYNOP FM-12 e i messaggi BUFR.

## Preparazione

!!! warning "Prerequisiti"

    - Assicurati che il tuo wis2box sia stato configurato e avviato.
    - Conferma lo stato visitando l'API wis2box (``http://<your-host-name>/oapi``) e verificando che l'API sia in esecuzione.
    - Assicurati di leggere le sezioni **synop2bufr primer** e **ecCodes primer** prima di iniziare gli esercizi.

## synop2bufr primer

Di seguito sono riportati i comandi e le configurazioni essenziali di `synop2bufr`:

### transform
La funzione `transform` converte un messaggio SYNOP in BUFR:

```bash
synop2bufr data transform --metadata my_file.csv --output-dir ./my_directory --year message_year --month message_month my_SYNOP.txt
```

Nota che se le opzioni metadata, output directory, year e month non sono specificate, assumeranno i loro valori predefiniti:

| Opzione      | Predefinito |
| ----------- | ----------- |
| --metadata | station_list.csv |
| --output-dir | La directory di lavoro corrente. |
| --year | L'anno corrente. |
| --month | Il mese corrente. |

!!! note
    Bisogna essere cauti nell'uso dell'anno e del mese predefiniti, poiché il giorno del mese specificato nel rapporto potrebbe non corrispondere (ad esempio, giugno non ha 31 giorni).

Negli esempi, l'anno e il mese non sono dati, quindi sentiti libero di specificare una data tu stesso o di utilizzare i valori predefiniti.

## ecCodes primer

ecCodes fornisce sia strumenti da riga di comando sia può essere incorporato nelle tue applicazioni. Di seguito sono riportati alcuni utili comandi
da riga di comando per lavorare con i dati BUFR.

### bufr_dump

Il comando `bufr_dump` è uno strumento generico di informazioni BUFR. Ha molte opzioni, ma le seguenti saranno le più applicabili agli esercizi:

```bash
bufr_dump -p my_bufr.bufr4
```

Questo mostrerà il contenuto BUFR sul tuo schermo. Se sei interessato ai valori assunti da una variabile in particolare, usa il comando `egrep`:

```bash
bufr_dump -p my_bufr.bufr4 | egrep -i temperature
```

Questo mostrerà le variabili relative alla temperatura nei tuoi dati BUFR. Se vuoi farlo per più tipi di variabili, filtra l'output usando una pipe (`|`):

```bash
bufr_dump -p my_bufr.bufr4 | egrep -i 'temperature|wind'
```

## Conversione di SYNOP FM-12 in BUFR usando synop2bufr dalla riga di comando

La libreria eccodes e il modulo synop2bufr sono installati nel contenitore wis2box-api. Per fare i prossimi esercizi copieremo la directory synop2bufr-exercises nel contenitore wis2box-api e eseguiremo gli esercizi da lì.

```bash
docker cp ~/exercise-materials/synop2bufr-exercises wis2box-api:/root
```

Ora possiamo entrare nel contenitore ed eseguire gli esercizi:

```bash
docker exec -it wis2box-api /bin/bash
```

### Esercizio 1
Naviga nella directory `/root/synop2bufr-exercises/ex_1` e ispeziona il file del messaggio SYNOP message.txt:

```bash
cd /root/synop2bufr-exercises/ex_1
more message.txt
```

!!! question

    Quanti rapporti SYNOP ci sono in questo file?

??? success "Clicca per rivelare la risposta"
    
    C'è 1 rapporto SYNOP, poiché c'è solo 1 delimitatore (=) alla fine del messaggio.

Ispeziona l'elenco delle stazioni:

```bash
more station_list.csv
```

!!! question

    Quante stazioni sono elencate nell'elenco delle stazioni?

??? success "Clicca per rivelare la risposta"

    C'è 1 stazione, il file station_list.csv contiene una riga di metadati della stazione.

!!! question
    Prova a convertire `message.txt` in formato BUFR.

??? success "Clicca per rivelare la risposta"

    Per convertire il messaggio SYNOP in formato BUFR, usa il seguente comando:

    ```bash
    synop2bufr data transform --metadata station_list.csv --output-dir ./ --year 2024 --month 09 message.txt
    ```

!!! tip

    Vedi la sezione [synop2bufr primer](#synop2bufr-primer).

Ispeziona i dati BUFR risultanti usando `bufr_dump`.

!!! question
     Scopri come confrontare i valori di latitudine e longitudine con quelli nell'elenco delle stazioni.

??? success "Clicca per rivelare la risposta"

    Per confrontare i valori di latitudine e longitudine nei dati BUFR con quelli nell'elenco delle stazioni, usa il seguente comando:

    ```bash
    bufr_dump -p WIGOS_0-20000-0-15015_20240921T120000.bufr4 | egrep -i 'latitude|longitude'
    ```

    Questo mostrerà i valori di latitudine e longitudine nei dati BUFR.

!!! tip

    Vedi la sezione [ecCodes primer](#eccodes-primer).

### Esercizio 2
Naviga nella directory `exercise-materials/synop2bufr-exercises/ex_2` e ispeziona il file del messaggio SYNOP message.txt:

```bash
cd /root/synop2bufr-exercises/ex_2
more message.txt
```

!!! question

    Quanti rapporti SYNOP ci sono in questo file?

??? success "Clicca per rivelare la risposta"

    Ci sono 3 rapporti SYNOP, poiché ci sono 3 delimitatori (=) alla fine del messaggio.

Ispeziona l'elenco delle stazioni:

```bash
more station_list.csv
```

!!! question

    Quante stazioni sono elencate nell'elenco delle stazioni?

??? success "Clicca per rivelare la risposta"

    Ci sono 3 stazioni, il file station_list.csv contiene tre righe di metadati delle stazioni.

!!! question
    Converti `message.txt` in formato BUFR.

??? success "Clicca per rivelare la risposta"

    Per convertire il messaggio SYNOP in formato BUFR, usa il seguente comando:

    ```bash
    synop2bufr data transform --metadata station_list.csv --output-dir ./ --year 2024 --month 09 message.txt
    ```

!!! question

    Sulla base dei risultati degli esercizi in questa e nella precedente esercizio, come prevederesti il numero di
    file BUFR risultanti in base al numero di rapporti SYNOP e stazioni elencate nel file di metadati delle stazioni?

??? success "Clicca per rivelare la risposta"

    Per vedere i file BUFR prodotti esegui il seguente comando:

    ```bash
    ls -l *.bufr4
    ```

    Il numero di file BUFR prodotti sarà uguale al numero di rapporti SYNOP nel file del messaggio.

Ispeziona i dati BUFR risultanti usando `bufr_dump`.

!!! question
    Come puoi verificare l'ID della stazione WIGOS codificato all'interno dei dati BUFR di ogni file prodotto?

??? success "Clicca per rivelare la risposta"

    Questo può essere fatto usando i seguenti comandi:

    ```bash
    bufr_dump -p WIGOS_0-20000-0-15015_20240921T120000.bufr4 | egrep -i 'wigos'
    ```

    ```bash
    bufr_dump -p WIGOS_0-20000-0-15020_20240921T120000.bufr4 | egrep -i 'wigos'
    ```

    ```bash
    bufr_dump -p WIGOS_0-20000-0-15090_20240921T120000.bufr4 | egrep -i 'wigos'
    ```

    Nota che se hai una directory con solo questi 3 file BUFR, puoi usare i caratteri jolly di Linux come segue:

    ```bash
    bufr_dump -p *.bufr4 | egrep -i 'wigos'
    ```

### Esercizio 3
Naviga nella directory `exercise-materials/synop2bufr-exercises/ex_3` e ispeziona il file del messaggio SYNOP message.txt:

```bash
cd /root/synop2bufr-exercises/ex_3
more message.txt
```

Questo messaggio SYNOP contiene solo un rapporto più lungo con più sezioni.

Ispeziona l'elenco delle stazioni:

```bash
more station_list.csv
```

!!! question

    È problematico che questo file contenga più stazioni di quanti siano i rapporti nel messaggio SYNOP?

??? success "Clicca per rivelare la risposta"

    No, questo non è un problema a condizione che esista una riga nel file dell'elenco delle stazioni con un TSI della stazione corrispondente a quello del rapporto SYNOP che stiamo cercando di convertire.

!!! note

    Il file dell'elenco delle stazioni è una fonte di metadati per `synop2bufr` per fornire le informazioni mancanti nel rapporto SYNOP alfanumerico e richieste nel SYNOP BUFR.

!!! question
    Converti `message.txt` in formato BUFR.

??? success "Clicca per rivelare la risposta"

    Questo si fa usando il comando `transform`, per esempio:

    ```bash
    synop2bufr data transform --metadata station_list.csv --output-dir ./ --year 2024 --month 09 message.txt
    ```

Ispeziona i dati BUFR risultanti usando `bufr_dump`.

!!! question

    Trova le seguenti variabili:

    - Temperatura dell'aria (K) del rapporto
    - Copertura nuvolosa totale (%) del rapporto
    - Periodo totale di sole (minuti) del rapporto
    - Velocità del vento (m/s) del rapporto

??? success "Clicca per rivelare la risposta"

    Per trovare le variabili per parola chiave nei dati BUFR, puoi usare i seguenti comandi:

    ```bash
    bufr_dump -p WIGOS_0-20000-0-15260_20240921T115500.bufr4 | egrep -i 'temperature'
    ```

    Puoi usare il seguente comando per cercare più parole chiave:

    ```bash
    bufr_dump -p WIGOS_0-20000-0-15260_20240921T115500.bufr4 | egrep -i 'temperature|cover|sunshine|wind'
    ```

!!! tip

    Potresti trovare utile l'ultimo comando della sezione [ecCodes primer](#eccodes-primer).


### Esercizio 4
Naviga nella directory `exercise-materials/synop2bufr-exercises/ex_4` e ispeziona il file del messaggio SYNOP message.txt:

```bash
cd /root/synop2bufr-exercises/ex_4
more message_incorrect.txt
```

!!! question

    Cosa c'è di sbagliato in questo file SYNOP?

??? success "Clicca per rivelare la risposta"

    Il rapporto SYNOP per 15015 manca del delimitatore (`=`) che consente a `synop2bufr` di distinguere questo rapporto dal successivo.

Tenta di convertire `message_incorrect.txt` usando `station_list.csv`

!!! question

    Quali problemi hai incontrato con questa conversione?

??? success "Clicca per rivelare la risposta"

    Per convertire il messaggio SYNOP in formato BUFR, usa il seguente comando:

    ```bash
    synop2bufr data transform --metadata station_list.csv --output-dir ./ --year 2024 --month 09 message_incorrect.txt
    ```

    Tentando di convertire dovrebbero apparire i seguenti errori:
    
    - `[ERROR] Impossibile decodificare il messaggio SYNOP`
    - `[ERROR] Errore nell'analisi del rapporto SYNOP: AAXX 21121 15015 02999 02501 10103 21090 39765 42952 57020 60001 15020 02997 23104 10130 21075 30177 40377 58020 60001 81041. 10130 non è un gruppo valido!`

### Esercizio 5
Naviga nella directory `exercise-materials/synop2bufr-exercises/ex_5` e ispeziona il file del messaggio SYNOP message.txt:

```bash
cd /root/synop2bufr-exercises/ex_5
more message.txt
```

Tenta di convertire `message.txt` in formato BUFR usando `station_list_incorrect.csv` 

!!! question

    Quali problemi hai incontrato con questa conversione?  
    Considerando l'errore presentato, giustifica il numero di file BUFR prodotti.

??? success "Clicca per rivelare la risposta"

    Per convertire il messaggio SYNOP in formato BUFR, usa il seguente comando:

    ```bash
    synop2bufr data transform --metadata station_list_incorrect.csv --output-dir ./ --year 2024 --month 09 message.txt
    ```

    Uno dei TSI delle stazioni (`15015`) non ha metadati corrispondenti nell'elenco delle stazioni, il che impedirà a synop2bufr di accedere ai metadati aggiuntivi necessari per convertire il primo rapporto SYNOP in BUFR.

    Vedrai il seguente avviso:

    - `[WARNING] Stazione 15015 non trovata nel file delle stazioni`

    Puoi vedere il numero di file BUFR prodotti eseguendo il seguente comando:

    ```bash
    ls -l *.bufr4
    ```

    Ci sono 3 rapporti SYNOP in message.txt ma sono stati prodotti solo 2 file BUFR. Questo perché uno dei rapporti SYNOP mancava dei metadati necessari come menzionato sopra.

## Conclusione

!!! success "Congratulazioni!"

    In questa sessione pratica, hai imparato:

    - come lo strumento synop2bufr può essere utilizzato per convertire i rapporti SYNOP FM-12 in BUFR;
    - come diagnosticare e correggere semplici errori di codifica nei rapporti SYNOP FM-12 prima della conversione del formato;

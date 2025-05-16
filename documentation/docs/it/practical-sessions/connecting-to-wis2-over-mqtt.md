---
title: Connessione a WIS2 tramite MQTT
---

# Connessione a WIS2 tramite MQTT

!!! abstract "Risultati dell'apprendimento"

    Al termine di questa sessione pratica, sarai in grado di:

    - connetterti al Global Broker di WIS2 utilizzando MQTT Explorer
    - esaminare la struttura degli argomenti di WIS2
    - esaminare la struttura dei messaggi di notifica di WIS2

## Introduzione

WIS2 utilizza il protocollo MQTT per pubblicizzare la disponibilità dei dati meteorologici/climatici/idrologici. Il Global Broker di WIS2 si iscrive a tutti i WIS2 Node nella rete e ripubblica i messaggi che riceve. Il Global Cache si iscrive al Global Broker, scarica i dati nel messaggio e poi ripubblica il messaggio sull'argomento `cache` con un nuovo URL. Il Global Discovery Catalogue pubblica metadati di scoperta dal Broker e fornisce un'API di ricerca.

Questo è un esempio della struttura del messaggio di notifica di WIS2 per un messaggio ricevuto sull'argomento `origin/a/wis2/br-inmet/data/core/weather/surface-based-observations/synop`:	

```json
{
  "id": "59f9b013-c4b3-410a-a52d-fff18f3f1b47",
  "type": "Feature",
  "version": "v04",
  "geometry": {
    "coordinates": [
      -38.69389,
      -17.96472,
      60
    ],
    "type": "Point"
  },
  "properties": {
    "data_id": "br-inmet/data/core/weather/surface-based-observations/synop/WIGOS_0-76-2-2900801000W83499_20240815T060000",
    "datetime": "2024-08-15T06:00:00Z",
    "pubtime": "2024-08-15T09:52:02Z",
    "integrity": {
      "method": "sha512",
      "value": "TBuWycx/G0lIiTo47eFPBViGutxcIyk7eikppAKPc4aHgOmTIS5Wb9+0v3awMOyCgwpFhTruRRCVReMQMp5kYw=="
    },
    "content": {
      "encoding": "base64",
      "value": "QlVGUgAA+gQAABYAACsAAAAAAAIAHAAH6AgPBgAAAAALAAABgMGWx1AAAM0ABOIAAAODM0OTkAAAAAAAAAAAAAAKb5oKEpJ6YkJ6mAAAAAAAAAAAAAAAAv0QeYA29WQa87ZhH4CQP//z+P//BD////+ASznXuUb///8MgAS3/////8X///e+AP////AB/+R/yf////////////////////6/1/79H/3///gEt////////4BLP6QAf/+/pAB//4H0YJ/YeAh/f2///7TH/////9+j//f///////////////////v0f//////////////////////wNzc3Nw==",
      "size": 250
    },
    "wigos_station_identifier": "0-76-2-2900801000W83499"
  },
  "links": [
    {
      "rel": "canonical",
      "type": "application/bufr",
      "href": "http://wis2bra.inmet.gov.br/data/2024-08-15/wis/br-inmet/data/core/weather/surface-based-observations/synop/WIGOS_0-76-2-2900801000W83499_20240815T060000.bufr4",
      "length": 250
    }
  ]
}
``` 

In questa sessione pratica imparerai come utilizzare lo strumento MQTT Explorer per configurare una connessione client MQTT a un Global Broker di WIS2 e sarai in grado di visualizzare i messaggi di notifica di WIS2.

MQTT Explorer è uno strumento utile per navigare e esaminare la struttura degli argomenti per un dato broker MQTT per rivedere i dati pubblicati.

Si noti che MQTT è utilizzato principalmente per la comunicazione "macchina a macchina"; ciò significa che normalmente ci sarebbe un client che analizza automaticamente i messaggi man mano che vengono ricevuti. Per lavorare con MQTT a livello di programmazione (ad esempio, in Python), puoi utilizzare le librerie client MQTT come [paho-mqtt](https://pypi.org/project/paho-mqtt) per connetterti a un broker MQTT ed elaborare i messaggi in arrivo. Esistono numerosi software client e server MQTT, a seconda delle tue esigenze e dell'ambiente tecnico.

## Utilizzo di MQTT Explorer per connettersi al Global Broker

Per visualizzare i messaggi pubblicati da un Global Broker di WIS2 puoi utilizzare "MQTT Explorer" che può essere scaricato dal [sito web di MQTT Explorer](https://mqtt-explorer.com).

Apri MQTT Explorer e aggiungi una nuova connessione al Global Broker ospitato da MeteoFrance utilizzando i seguenti dettagli:

- host: globalbroker.meteo.fr
- port: 8883
- username: everyone
- password: everyone

<img alt="mqtt-explorer-global-broker-connection" src="/../assets/img/mqtt-explorer-global-broker-connection.png" width="800">

Fai clic sul pulsante 'ADVANCED', rimuovi gli argomenti preconfigurati e aggiungi i seguenti argomenti a cui iscriverti:

- `origin/a/wis2/#`

<img alt="mqtt-explorer-global-broker-advanced" src="/../assets/img/mqtt-explorer-global-broker-sub-origin.png" width="800">

!!! note
    Quando configuri le iscrizioni MQTT puoi utilizzare i seguenti caratteri jolly:

    - **Singolo livello (+)**: un carattere jolly di singolo livello sostituisce un livello di argomento
    - **Multi-livello (#)**: un carattere jolly multi-livello sostituisce più livelli di argomento

    In questo caso `origin/a/wis2/#` si iscriverà a tutti gli argomenti sotto l'argomento `origin/a/wis2`.

Fai clic su 'BACK', poi 'SAVE' per salvare i dettagli della tua connessione e delle iscrizioni.  Poi fai clic su 'CONNECT':

I messaggi dovrebbero iniziare a comparire nella tua sessione di MQTT Explorer come segue:

<img alt="mqtt-explorer-global-broker-topics" src="/../assets/img/mqtt-explorer-global-broker-msg-origin.png" width="800">

Ora sei pronto per iniziare ad esplorare gli argomenti e la struttura dei messaggi di WIS2.

## Esercizio 1: Esaminare la struttura degli argomenti di WIS2

Utilizza MQTT per navigare nella struttura degli argomenti sotto gli argomenti `origin`.

!!! question
    
    Come possiamo distinguere il centro WIS che ha pubblicato i dati?

??? success "Clicca per rivelare la risposta"

    Puoi fare clic sulla finestra sul lato sinistro in MQTT Explorer per espandere la struttura degli argomenti.
    
    Possiamo distinguere il centro WIS che ha pubblicato i dati guardando il quarto livello della struttura degli argomenti.  Ad esempio, l'argomento seguente:

    `origin/a/wis2/br-inmet/data/core/weather/surface-based-observations/synop`

    ci dice che i dati sono stati pubblicati da un centro WIS con l'ID del centro `br-inmet`, che è l'ID del centro per l'Instituto Nacional de Meteorologia - INMET, Brasile.

!!! question

    Come possiamo distinguere tra i messaggi pubblicati dai centri WIS che ospitano un gateway GTS-to-WIS2 e i messaggi pubblicati dai centri WIS che ospitano un nodo WIS2?

??? success "Clicca per rivelare la risposta"

    Possiamo distinguere i messaggi provenienti dal gateway GTS-to-WIS2 guardando l'ID del centro nella struttura degli argomenti. Ad esempio, l'argomento seguente:

    `origin/a/wis2/de-dwd-gts-to-wis2/data/core/I/S/A/I/01/sbbr`

    ci dice che i dati sono stati pubblicati dal gateway GTS-to-WIS2 ospitato dal Deutscher Wetterdienst (DWD), Germania. Il gateway GTS-to-WIS2 è un tipo speciale di pubblicatore di dati che pubblica dati dal Sistema di Telecomunicazione Globale (GTS) a WIS2. La struttura degli argomenti è composta dagli header TTAAii CCCC per i messaggi GTS.

## Esercizio 2: Esaminare la struttura dei messaggi di WIS2

Disconnettiti da MQTT Explorer e aggiorna le sezioni 'Advanced' per cambiare l'iscrizione ai seguenti argomenti:

* `origin/a/wis2/+/data/core/weather/surface-based-observations/synop`
* `cache/a/wis2/+/data/core/weather/surface-based-observations/synop`

<img alt="mqtt-explorer-global-broker-topics-exercise2" src="/../assets/img/mqtt-explorer-global-broker-sub-origin-cache-synop.png" width="800">

!!! note
    Il carattere jolly `+` è utilizzato per iscriversi a tutti i centri WIS.

Riconnettiti al Global Broker e attendi che appaiano i messaggi.

Puoi visualizzare il contenuto del messaggio di WIS2 nella sezione "Value" sul lato destro. Prova ad espandere la struttura degli argomenti per vedere i diversi livelli del messaggio fino a raggiungere l'ultimo livello e rivedere il contenuto del messaggio di uno dei messaggi.

!!! question

    Come possiamo identificare il timestamp in cui i dati sono stati pubblicati? E come possiamo identificare il timestamp in cui i dati sono stati raccolti?

??? success "Clicca per rivelare la risposta"

    Il timestamp in cui i dati sono stati pubblicati è contenuto nella sezione `properties` del messaggio con una chiave di `pubtime`.

    Il timestamp in cui i dati sono stati raccolti è contenuto nella sezione `properties` del messaggio con una chiave di `datetime`.

    <img alt="mqtt-explorer-global-broker-msg-properties" src="/../assets/img/mqtt-explorer-global-broker-msg-properties.png" width="800">

!!! question

    Come possiamo scaricare i dati dall'URL fornito nel messaggio?

??? success "Clicca per rivelare la risposta"

    L'URL è contenuto nella sezione `links` con `rel="canonical"` e definito dalla chiave `href`.

    Puoi copiare l'URL e incollarlo in un browser web per scaricare i dati.

## Esercizio 3: Esaminare la differenza tra gli argomenti 'origin' e 'cache'

Assicurati di essere ancora connesso al Global Broker utilizzando le iscrizioni agli argomenti `origin/a/wis2/+/data/core/weather/surface-based-observations/synop` e `cache/a/wis2/+/data/core/weather/surface-based-observations/synop` come descritto nell'Esercizio 2.

Prova a identificare un messaggio per lo stesso ID del centro pubblicato sia sugli argomenti `origin` che `cache`.


!!! question

    Qual è la differenza tra i messaggi pubblicati sugli argomenti `origin` e `cache`?

??? success "Clicca per rivelare la risposta"

    I messaggi pubblicati sugli argomenti `origin` sono i messaggi originali che il Global Broker ripubblica dai WIS2 Node nella rete. 

    I messaggi pubblicati sugli argomenti `cache` sono i messaggi per i dati sono stati scaricati dal Global Cache. Se controlli il contenuto del messaggio dall'argomento che inizia con `cache`, vedrai che il link 'canonical' è stato aggiornato con un nuovo URL.
    
    Ci sono più Global Cache nella rete WIS2, quindi riceverai un messaggio da ogni Global Cache che ha scaricato il messaggio.

    Il Global Cache scaricherà e ripubblicherà solo i messaggi che sono stati pubblicati sulla gerarchia degli argomenti `../data/core/...`.

## Conclusione

!!! success "Congratulazioni!"
    In questa sessione pratica, hai imparato:

    - come iscriversi ai servizi del Global Broker di WIS2 utilizzando MQTT Explorer
    - la struttura degli argomenti di WIS2
    - la struttura dei messaggi di notifica di WIS2
    - la differenza tra dati core e dati raccomandati
    - la struttura degli argomenti utilizzata dal gateway GTS-to-WIS2
    - la differenza tra i messaggi del Global Broker pubblicati sugli argomenti `origin` e `cache`
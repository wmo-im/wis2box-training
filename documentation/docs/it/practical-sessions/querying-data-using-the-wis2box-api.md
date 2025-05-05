---
title: Interrogazione dei dati utilizzando l'API wis2box
---

# Interrogazione dei dati utilizzando l'API wis2box

!!! abstract "Obiettivi di apprendimento"
    Al termine di questa sessione pratica, sarai in grado di:

    - utilizzare l'API wis2box per interrogare e filtrare le tue stazioni
    - utilizzare l'API wis2box per interrogare e filtrare i tuoi dati

## Introduzione

L'API wis2box fornisce accesso alla scoperta e all'interrogazione in formato leggibile dalle macchine ai dati che sono stati inseriti in wis2box. L'API è basata sullo standard OGC API - Features ed è implementata utilizzando [pygeoapi](https://pygeoapi.io).

L'API wis2box fornisce accesso alle seguenti collezioni:

- Stazioni
- Metadati di scoperta
- Notifiche dei dati
- più una collezione per ogni dataset configurato, che memorizza l'output da bufr2geojson (il plugin `bufr2geojson` deve essere abilitato nella configurazione dei mapping dei dati per popolare gli elementi nella collezione del dataset).

In questa sessione pratica imparerai come utilizzare l'API dei dati per esplorare e interrogare i dati che sono stati inseriti in wis2box.

## Preparazione

!!! note
    Naviga alla pagina iniziale dell'API wis2box nel tuo browser web:

    `http://YOUR-HOST/oapi`

<img alt="wis2box-api-landing-page" src="../../assets/img/wis2box-api-landing-page.png" width="600">

## Ispezione delle collezioni

Dalla pagina iniziale, clicca sul link 'Collections'.

!!! question
    Quante collezioni di dataset vedi nella pagina risultante? Cosa pensi rappresenti ciascuna collezione?

??? success "Clicca per rivelare la risposta"
    Dovrebbero essere visualizzate 4 collezioni, incluse "Stations", "Discovery metadata" e "Data notifications"

## Ispezione delle stazioni

Dalla pagina iniziale, clicca sul link 'Collections', poi clicca sul link 'Stations'.

<img alt="wis2box-api-collections-stations" src="../../assets/img/wis2box-api-collections-stations.png" width="600">

Clicca sul link 'Browse', poi clicca sul link 'json'.

!!! question
    Quante stazioni vengono restituite? Confronta questo numero con la lista delle stazioni in `http://YOUR-HOST/wis2box-webapp/station`

??? success "Clicca per rivelare la risposta"
    Il numero di stazioni dall'API dovrebbe essere uguale al numero di stazioni che vedi nella webapp wis2box.

!!! question
    Come possiamo interrogare una singola stazione (es. `Balaka`)?

??? success "Clicca per rivelare la risposta"
    Interroga l'API con `http://YOUR-HOST/oapi/collections/stations/items?q=Balaka`.

!!! note
    L'esempio sopra è basato sui dati di test del Malawi. Prova a testare con le stazioni che hai inserito come parte degli esercizi precedenti.

## Ispezione delle osservazioni

!!! note
    L'esempio sopra è basato sui dati di test del Malawi. Prova a testare con le osservazioni che hai inserito come parte degli esercizi.

Dalla pagina iniziale, clicca sul link 'Collections', poi clicca sul link 'Surface weather observations from Malawi'.

<img alt="wis2box-api-collections-malawi-obs" src="../../assets/img/wis2box-api-collections-malawi-obs.png" width="600">

Clicca sul link 'Queryables'.

<img alt="wis2box-api-collections-malawi-obs-queryables" src="../../assets/img/wis2box-api-collections-malawi-obs-queryables.png" width="600">

!!! question
    Quale queryable dovrebbe essere usato per filtrare per identificativo della stazione?

??? success "Clicca per rivelare la risposta"
    Il `wigos_station_identifer` è il queryable corretto.

Naviga alla pagina precedente (cioè `http://YOUR-HOST/oapi/collections/urn:wmo:md:mwi:mwi_met_centre:surface-weather-observations`)

Clicca sul link 'Browse'.

!!! question
    Come possiamo visualizzare la risposta JSON?

??? success "Clicca per rivelare la risposta"
    Cliccando sul link 'JSON' in alto a destra della pagina, o aggiungendo `f=json` alla richiesta API nel browser web.

Ispeziona la risposta JSON delle osservazioni.

!!! question
    Quanti record vengono restituiti?

!!! question
    Come possiamo limitare la risposta a 3 osservazioni?

??? success "Clicca per rivelare la risposta"
    Aggiungi `limit=3` alla richiesta API.

!!! question
    Come possiamo ordinare la risposta per le osservazioni più recenti?

??? success "Clicca per rivelare la risposta"
    Aggiungi `sortby=-resultTime` alla richiesta API (nota il segno `-` per indicare l'ordine decrescente). Per ordinare per le osservazioni più vecchie, aggiorna la richiesta includendo `sortby=resultTime`.

!!! question
    Come possiamo filtrare le osservazioni per una singola stazione?

??? success "Clicca per rivelare la risposta"
    Aggiungi `wigos_station_identifier=<WSI>` alla richiesta API.

!!! question
    Come possiamo ricevere le osservazioni come CSV?

??? success "Clicca per rivelare la risposta"
    Aggiungi `f=csv` alla richiesta API.

!!! question
    Come possiamo mostrare una singola osservazione (id)?

??? success "Clicca per rivelare la risposta"
    Utilizzando l'identificativo della feature da una richiesta API sulle osservazioni, interroga l'API con `http://YOUR-HOST/oapi/collections/{collectionId}/items/{featureId}`, dove `{collectionId}` è il nome della tua collezione di osservazioni e `{itemId}` è l'identificativo della singola osservazione di interesse.

## Conclusione

!!! success "Congratulazioni!"
    In questa sessione pratica, hai imparato come:

    - utilizzare l'API wis2box per interrogare e filtrare le tue stazioni
    - utilizzare l'API wis2box per interrogare e filtrare i tuoi dati
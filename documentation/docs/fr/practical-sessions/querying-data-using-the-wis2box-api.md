---
title: Interrogation des données via l'API wis2box
---

# Interrogation des données via l'API wis2box

!!! abstract "Objectifs d'apprentissage"
    À la fin de cette session pratique, vous serez capable de :

    - utiliser l'API wis2box pour interroger et filtrer vos stations
    - utiliser l'API wis2box pour interroger et filtrer vos données

## Introduction

L'API wis2box fournit un accès de découverte et d'interrogation lisible par machine aux données qui ont été ingérées dans wis2box. L'API est basée sur la norme OGC API - Features et est implémentée à l'aide de [pygeoapi](https://pygeoapi.io).

L'API wis2box donne accès aux collections suivantes :

- Stations
- Métadonnées de découverte
- Notifications de données
- plus une collection par jeu de données configuré, qui stocke la sortie de bufr2geojson (le plugin `bufr2geojson` doit être activé dans la configuration des mappages de données pour remplir les éléments de la collection de données).

Dans cette session pratique, vous apprendrez à utiliser l'API de données pour parcourir et interroger les données qui ont été ingérées dans wis2box.

## Préparation

!!! note
    Accédez à la page d'accueil de l'API wis2box dans votre navigateur web :

    `http://YOUR-HOST/oapi`

<img alt="wis2box-api-landing-page" src="../../assets/img/wis2box-api-landing-page.png" width="600">

## Inspection des collections

Depuis la page d'accueil, cliquez sur le lien 'Collections'.

!!! question
    Combien de collections de données voyez-vous sur la page résultante ? Que pensez-vous que chaque collection représente ?

??? success "Cliquez pour révéler la réponse"
    Il devrait y avoir 4 collections affichées, incluant "Stations", "Métadonnées de découverte" et "Notifications de données"

## Inspection des stations

Depuis la page d'accueil, cliquez sur le lien 'Collections', puis sur le lien 'Stations'.

<img alt="wis2box-api-collections-stations" src="../../assets/img/wis2box-api-collections-stations.png" width="600">

Cliquez sur le lien 'Browse', puis sur le lien 'json'.

!!! question
    Combien de stations sont retournées ? Comparez ce nombre à la liste des stations dans `http://YOUR-HOST/wis2box-webapp/station`

??? success "Cliquez pour révéler la réponse"
    Le nombre de stations de l'API devrait être égal au nombre de stations que vous voyez dans l'application web wis2box.

!!! question
    Comment pouvons-nous interroger une seule station (par exemple `Balaka`) ?

??? success "Cliquez pour révéler la réponse"
    Interrogez l'API avec `http://YOUR-HOST/oapi/collections/stations/items?q=Balaka`.

!!! note
    L'exemple ci-dessus est basé sur les données test du Malawi. Essayez de tester avec les stations que vous avez ingérées dans le cadre des exercices précédents.

## Inspection des observations

!!! note
    L'exemple ci-dessus est basé sur les données test du Malawi. Essayez de tester avec les observations que vous avez ingérées dans le cadre des exercices.

Depuis la page d'accueil, cliquez sur le lien 'Collections', puis sur le lien 'Surface weather observations from Malawi'.

<img alt="wis2box-api-collections-malawi-obs" src="../../assets/img/wis2box-api-collections-malawi-obs.png" width="600">

Cliquez sur le lien 'Queryables'.

<img alt="wis2box-api-collections-malawi-obs-queryables" src="../../assets/img/wis2box-api-collections-malawi-obs-queryables.png" width="600">

!!! question
    Quel queryable serait utilisé pour filtrer par identifiant de station ?

??? success "Cliquez pour révéler la réponse"
    Le `wigos_station_identifer` est le queryable correct.

Retournez à la page précédente (c'est-à-dire `http://YOUR-HOST/oapi/collections/urn:wmo:md:mwi:mwi_met_centre:surface-weather-observations`)

Cliquez sur le lien 'Browse'.

!!! question
    Comment pouvons-nous visualiser la réponse JSON ?

??? success "Cliquez pour révéler la réponse"
    En cliquant sur le lien 'JSON' en haut à droite de la page, ou en ajoutant `f=json` à la requête API dans le navigateur web.

Inspectez la réponse JSON des observations.

!!! question
    Combien d'enregistrements sont retournés ?

!!! question
    Comment pouvons-nous limiter la réponse à 3 observations ?

??? success "Cliquez pour révéler la réponse"
    Ajoutez `limit=3` à la requête API.

!!! question
    Comment pouvons-nous trier la réponse par les dernières observations ?

??? success "Cliquez pour révéler la réponse"
    Ajoutez `sortby=-resultTime` à la requête API (notez le signe `-` pour indiquer l'ordre de tri décroissant). Pour trier par les premières observations, mettez à jour la requête pour inclure `sortby=resultTime`.

!!! question
    Comment pouvons-nous filtrer les observations par une seule station ?

??? success "Cliquez pour révéler la réponse"
    Ajoutez `wigos_station_identifier=<WSI>` à la requête API.

!!! question
    Comment pouvons-nous recevoir les observations au format CSV ?

??? success "Cliquez pour révéler la réponse"
    Ajoutez `f=csv` à la requête API.

!!! question
    Comment pouvons-nous afficher une seule observation (id) ?

??? success "Cliquez pour révéler la réponse"
    En utilisant l'identifiant de l'entité d'une requête API sur les observations, interrogez l'API avec `http://YOUR-HOST/oapi/collections/{collectionId}/items/{featureId}`, où `{collectionId}` est le nom de votre collection d'observations et `{itemId}` est l'identifiant de l'observation unique qui vous intéresse.

## Conclusion

!!! success "Félicitations !"
    Dans cette session pratique, vous avez appris à :

    - utiliser l'API wis2box pour interroger et filtrer vos stations
    - utiliser l'API wis2box pour interroger et filtrer vos données
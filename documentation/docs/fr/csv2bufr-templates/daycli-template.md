---
title: Modèle DAYCLI
---

# Modèle csv2bufr pour les données climatiques quotidiennes (DAYCLI)

Le modèle **DAYCLI** fournit un format CSV standardisé pour convertir les données climatiques quotidiennes en séquence BUFR 307075.

Ce format est destiné à être utilisé avec les Systèmes de Gestion des Données Climatiques pour publier des données sur WIS2, en soutien aux exigences de rapport pour les observations climatiques quotidiennes.

Ce modèle mappe les observations quotidiennes de :

 - Température minimale, maximale et moyenne sur une période de 24 heures
 - Précipitations totales accumulées sur une période de 24 heures
 - Profondeur totale de la neige au moment de l'observation
 - Profondeur de la neige fraîche sur une période de 24 heures

Ce modèle nécessite des métadonnées supplémentaires par rapport au modèle AWS simplifié : méthode de calcul de la température moyenne ; hauteurs des capteurs et de la station ; exposition et classification de la qualité des mesures.

!!! Note "À propos du modèle DAYCLI"
    Veuillez noter que la séquence BUFR DAYCLI sera mise à jour en 2025 pour inclure des informations supplémentaires et des drapeaux QC révisés. Le modèle DAYCLI inclus dans wis2box sera mis à jour pour refléter ces changements. L'OMM communiquera lorsque le logiciel wis2box sera mis à jour pour inclure le nouveau modèle DAYCLI, afin de permettre aux utilisateurs de mettre à jour leurs systèmes en conséquence.

## Colonnes CSV et description

{{ read_csv("docs/assets/tables/daycli-table.csv") }}

## Méthode de moyennisation

{{ read_csv("docs/assets/tables/averaging-method-table.csv") }}

## Drapeau de qualité

{{ read_csv("docs/assets/tables/quality_flag.csv") }}

## Références pour la classification des sites

[Référence pour "classification des sites de température"](https://library.wmo.int/idviewer/35625/839).

[Référence pour "classification des sites de précipitations"](https://library.wmo.int/idviewer/35625/840).

## Exemple

Fichier CSV exemple conforme au modèle DAYCLI : [daycli-example.csv](/sample-data/daycli-example.csv).
---
title: Modèle CLIMAT
---

# Modèle csv2bufr pour les données climatiques quotidiennes (CLIMAT)

Les messages **CLIMAT** rapportent des résumés climatiques mensuels compilés à partir d'observations quotidiennes effectuées dans des stations synoptiques et climatologiques, afin de soutenir la surveillance climatique, la recherche et l'archivage.

Le modèle CLIMAT fournit un format CSV standardisé pour produire des messages CLIMAT encodés au format BUFR pour les séquences 301150,307073.

## Colonnes CSV et description

{{ read_csv("docs/assets/tables/climat-table.csv") }}

## Exemple

Exemple de fichier CSV conforme au modèle CLIMAT : [climat-example.csv](../../sample-data/climat-example.csv).
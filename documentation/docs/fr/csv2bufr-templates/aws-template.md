---
titre: Modèle AWS
---

# Modèle csv2bufr pour Stations Météorologiques Automatiques rapportant des données GBON horaires

Le **Modèle AWS** utilise un format CSV standardisé pour intégrer les données provenant des Stations Météorologiques Automatiques en soutien aux exigences de rapportage GBON. Ce modèle de mappage convertit les données CSV en séquence BUFR 301150, 307096.

Le format est destiné à être utilisé avec des stations météorologiques automatiques rapportant un nombre minimal de paramètres, incluant la pression, la température et l'humidité de l'air, la vitesse et la direction du vent, ainsi que les précipitations sur une base horaire.

## Colonnes CSV et description

{{ read_csv("docs/assets/tables/aws-minimal.csv") }}

## Exemple

Fichier CSV exemple conforme au modèle AWS : [aws-example.csv](/sample-data/aws-example.csv).
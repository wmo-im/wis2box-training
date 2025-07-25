---
title: Accueil
---

<img alt="WMO logo" src="/assets/img/wmo-logo.png" width="200">
# Formation WIS2 in a box

WIS2 in a box ([wis2box](https://docs.wis2box.wis.wmo.int)) est une implémentation de référence libre et open source (FOSS) d’un WMO WIS2 Node. Le projet fournit un ensemble d’outils prêts à l’emploi pour ingérer, traiter et publier des données météorologiques/climatiques/hydrologiques en utilisant des approches basées sur des standards, en conformité avec les principes de WIS2. wis2box permet également d’accéder à toutes les données du réseau WIS2. wis2box est conçu pour offrir une faible barrière à l’entrée pour les fournisseurs de données, en fournissant une infrastructure et des services permettant la découverte, l’accès et la visualisation des données.

Cette formation propose des explications étape par étape sur divers aspects du projet wis2box ainsi qu’un certain nombre d’exercices pour vous aider à publier et télécharger des données depuis WIS2. La formation est dispensée sous forme de présentations générales ainsi que d’exercices pratiques.

Les participants pourront travailler avec des données et métadonnées de test, ainsi qu’intégrer leurs propres données et métadonnées.

Cette formation couvre un large éventail de sujets (installation/configuration, publication/téléchargement de données, etc.).

## Objectifs et résultats d’apprentissage

Les objectifs de cette formation sont de se familiariser avec les éléments suivants :

- Concepts et composants fondamentaux de l’architecture WIS2
- Formats de données et de métadonnées utilisés dans WIS2 pour la découverte et l’accès
- Architecture et environnement de wis2box
- Fonctions principales de wis2box :
    - Gestion des métadonnées
    - Ingestion des données et transformation au format BUFR
    - Broker MQTT pour la publication de messages WIS2
    - Point de terminaison HTTP pour le téléchargement des données
    - Point de terminaison API pour l’accès programmatique aux données

## Navigation

La navigation à gauche fournit une table des matières pour l’ensemble de la formation.

La navigation à droite fournit une table des matières pour une page spécifique.

## Prérequis

### Connaissances

- Commandes de base sous Linux (voir le [cheatsheet](./cheatsheets/linux.md))
- Connaissances de base en réseaux et protocoles Internet

### Logiciels

Cette formation nécessite les outils suivants :

- Une instance exécutant le système d’exploitation Ubuntu (fournie par les formateurs de l’OMM lors des sessions de formation locales) voir [Accéder à votre VM étudiant](./practical-sessions/accessing-your-student-vm.md#introduction)
- Un client SSH pour accéder à votre instance
- MQTT Explorer sur votre machine locale
- Un client SCP et SFTP pour copier des fichiers depuis votre machine locale

## Conventions

!!! question

    Une section marquée ainsi vous invite à répondre à une question.

Vous remarquerez également des sections de conseils et de notes dans le texte :

!!! tip

    Les conseils partagent des astuces pour accomplir au mieux les tâches.

!!! note

    Les notes fournissent des informations supplémentaires sur le sujet abordé lors de la session pratique, ainsi que sur la meilleure façon d’accomplir les tâches.

Les exemples sont indiqués comme suit :

Configuration
``` {.yaml linenums="1"}
my-collection-defined-in-yaml:
    type: collection
    title: my title defined as a yaml attribute named title
    description: my description as a yaml attribute named description
```

Les extraits à taper dans un terminal/console sont indiqués comme suit :

```bash
echo 'Hello world'
```

Les noms de conteneurs (images en cours d’exécution) sont indiqués en **gras**.

## Lieu de la formation et matériel

Le contenu de la formation, le wiki et le système de suivi des problèmes sont gérés sur GitHub à [https://github.com/wmo-im/wis2box-training](https://github.com/wmo-im/wis2box-training).

## Matériel des exercices

Le matériel des exercices peut être téléchargé depuis le fichier zip [exercise-materials.zip](/exercise-materials.zip).

## Support

Pour signaler des problèmes, des bugs, des suggestions ou des améliorations/contributions à cette formation, veuillez utiliser le [système de suivi des problèmes GitHub](https://github.com/World-Meteorological-Organization/wis2box-training/issues).

Tous les bugs, améliorations et problèmes liés à wis2box peuvent être signalés sur [GitHub](https://github.com/World-Meteorological-Organization/wis2box/issues).

Pour toute question ou support supplémentaire, veuillez contacter wis2-support@wmo.int.

Comme toujours, la documentation principale de wis2box est disponible à [https://docs.wis2box.wis.wmo.int](https://docs.wis2box.wis.wmo.int).

Les contributions sont toujours encouragées et les bienvenues !
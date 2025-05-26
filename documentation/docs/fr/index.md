---
title: Accueil
---

<img alt="Logo OMM" src="/assets/img/wmo-logo.png" width="200">
# Formation WIS2 in a box

WIS2 in a box ([wis2box](https://docs.wis2box.wis.wmo.int)) est une mise en œuvre de référence libre et open source (FOSS) d'un nœud WIS2 de l'OMM. Le projet fournit un ensemble d'outils prêts à l'emploi pour ingérer, traiter et publier des données météorologiques/climatiques/hydrologiques en utilisant des approches basées sur des normes, conformément aux principes de WIS2. wis2box offre également un accès à toutes les données du réseau WIS2. wis2box est conçu pour avoir un faible seuil d'entrée pour les fournisseurs de données, fournissant une infrastructure et des services facilitant la découverte, l'accès et la visualisation des données.

Cette formation fournit des explications étape par étape sur divers aspects du projet wis2box ainsi que plusieurs exercices pour vous aider à publier et télécharger des données depuis WIS2. La formation est fournie sous forme de présentations d'ensemble ainsi que d'exercices pratiques.

Les participants pourront travailler avec des données et métadonnées de test, ainsi qu'intégrer leurs propres données et métadonnées.

Cette formation couvre une large gamme de sujets (installation/configuration/publication, téléchargement de données, etc.).

## Objectifs et résultats d'apprentissage

Les objectifs de cette formation sont de se familiariser avec les éléments suivants :

- Concepts et composants clés de l'architecture WIS2
- Formats de données et de métadonnées utilisés dans WIS2 pour la découverte et l'accès
- Architecture et environnement de wis2box
- Fonctions principales de wis2box :
    - gestion des métadonnées
    - ingestion de données et transformation au format BUFR
    - courtier MQTT pour la publication de messages WIS2
    - point de terminaison HTTP pour le téléchargement de données
    - point de terminaison API pour un accès programmatique aux données

## Navigation

La navigation à gauche fournit une table des matières pour l'ensemble de la formation.

La navigation à droite fournit une table des matières pour une page spécifique.

## Prérequis

### Connaissances

- Commandes Linux de base (voir la [cheatsheet](./cheatsheets/linux.md))
- Connaissances de base en réseautage et protocoles Internet

### Logiciel

Cette formation nécessite les outils suivants :

- Une instance fonctionnant sous Ubuntu OS (fournie par les formateurs de l'OMM lors des sessions de formation locales) voir [Accéder à votre VM étudiante](./practical-sessions/accessing-your-student-vm.md#introduction)
- Client SSH pour accéder à votre instance
- MQTT Explorer sur votre machine locale
- Client SCP et SFTP pour copier des fichiers depuis votre machine locale

## Conventions

!!! question

    Une section marquée comme cela vous invite à répondre à une question.

Vous remarquerez également des sections de conseils et de notes dans le texte :

!!! tip

    Les conseils partagent de l'aide sur la manière d'accomplir au mieux les tâches.

!!! note

    Les notes fournissent des informations supplémentaires sur le sujet couvert par la session pratique, ainsi que sur la manière d'accomplir au mieux les tâches.

Les exemples sont indiqués comme suit :

Configuration
``` {.yaml linenums="1"}
my-collection-defined-in-yaml:
    type: collection
    title: my title defined as a yaml attribute named title
    description: my description as a yaml attribute named description
```

Les extraits qui doivent être tapés dans un terminal/console sont indiqués comme :

```bash
echo 'Hello world'
```

Les noms de conteneurs (images en cours d'exécution) sont indiqués en **gras**.

## Lieu et matériaux de formation

Le contenu de la formation, le wiki et le suivi des problèmes sont gérés sur GitHub à [https://github.com/World-Meteorological-Organization/wis2box-training](https://github.com/World-Meteorological-Organization/wis2box-training).

## Impression du matériel

Cette formation peut être exportée en PDF. Pour enregistrer ou imprimer ce matériel de formation, allez à la [page d'impression](print_page), et sélectionnez
Fichier > Imprimer > Enregistrer en PDF.

## Matériaux d'exercice

Les matériaux d'exercice peuvent être téléchargés depuis le fichier zip [exercise-materials.zip](/exercise-materials.zip).

## Support

Pour les problèmes/bugs/suggestions ou améliorations/contributions à cette formation, veuillez utiliser le [suivi des problèmes GitHub](https://github.com/World-Meteorological-Organization/wis2box-training/issues).

Tous les bugs, améliorations et problèmes de wis2box peuvent être signalés sur [GitHub](https://github.com/World-Meteorological-Organization/wis2box/issues).

Pour un support supplémentaire ou des questions, veuillez contacter wis2-support@wmo.int.

Comme toujours, la documentation principale de wis2box peut toujours être trouvée à [https://docs.wis2box.wis.wmo.int](https://docs.wis2box.wis.wmo.int).

Les contributions sont toujours encouragées et bienvenues!
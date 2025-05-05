---
title: Accueil
---

<img alt="WMO logo" src="../assets/img/wmo-logo.png" width="200">
# Formation WIS2 in a box

WIS2 in a box ([wis2box](https://docs.wis2box.wis.wmo.int)) est une implémentation de référence libre et open source (FOSS) d'un WMO WIS2 Node. Le projet fournit un ensemble d'outils prêt à l'emploi pour ingérer, traiter et publier des données météorologiques/climatiques/hydrologiques en utilisant des approches basées sur des normes conformes aux principes WIS2. wis2box permet également d'accéder à toutes les données du réseau WIS2. wis2box est conçu pour offrir un accès facile aux fournisseurs de données, en fournissant une infrastructure et des services permettant la découverte, l'accès et la visualisation des données.

Cette formation fournit des explications étape par étape des différents aspects du projet wis2box ainsi qu'un certain nombre d'exercices pour vous aider à publier et télécharger des données depuis WIS2. La formation est dispensée sous forme de présentations générales et d'exercices pratiques.

Les participants pourront travailler avec des données et métadonnées de test, ainsi qu'intégrer leurs propres données et métadonnées.

Cette formation couvre un large éventail de sujets (installation/configuration/paramétrage, publication/téléchargement de données, etc.).

## Objectifs et résultats d'apprentissage

Les objectifs de cette formation sont de se familiariser avec :

- Les concepts et composants fondamentaux de l'architecture WIS2
- Les formats de données et de métadonnées utilisés dans WIS2 pour la découverte et l'accès
- L'architecture et l'environnement wis2box
- Les fonctions principales de wis2box :
    - Gestion des métadonnées
    - Ingestion et transformation des données au format BUFR
    - Broker MQTT pour la publication des messages WIS2
    - Point d'accès HTTP pour le téléchargement des données
    - Point d'accès API pour l'accès programmatique aux données

## Navigation

La navigation à gauche fournit une table des matières pour l'ensemble de la formation.

La navigation à droite fournit une table des matières pour une page spécifique.

## Prérequis

### Connaissances

- Commandes Linux de base (voir le [guide de référence](cheatsheets/linux.md))
- Connaissances de base en réseaux et protocoles Internet

### Logiciels

Cette formation nécessite les outils suivants :

- Une instance exécutant Ubuntu OS (fournie par les formateurs WMO lors des sessions de formation locales) voir [Accéder à votre VM étudiant](practical-sessions/accessing-your-student-vm.md#introduction)
- Client SSH pour accéder à votre instance
- MQTT Explorer sur votre machine locale
- Client SCP et SFTP pour copier des fichiers depuis votre machine locale

## Conventions

!!! question

    Une section marquée ainsi vous invite à répondre à une question.

Vous remarquerez également des sections de conseils et de notes dans le texte :

!!! tip

    Les conseils partagent de l'aide sur la meilleure façon d'accomplir les tâches.

!!! note

    Les notes fournissent des informations supplémentaires sur le sujet couvert par la session pratique, ainsi que sur la meilleure façon d'accomplir les tâches.

Les exemples sont indiqués comme suit :

Configuration
``` {.yaml linenums="1"}
my-collection-defined-in-yaml:
    type: collection
    title: my title defined as a yaml attribute named title
    description: my description as a yaml attribute named description
```

Les commandes à taper dans un terminal/console sont indiquées comme :

```bash
echo 'Hello world'
```

Les noms des conteneurs (images en cours d'exécution) sont indiqués en **gras**.

## Lieu de formation et matériels

Le contenu de la formation, le wiki et le suivi des problèmes sont gérés sur GitHub à [https://github.com/World-Meteorological-Organization/wis2box-training](https://github.com/World-Meteorological-Organization/wis2box-training).

## Impression du matériel

Cette formation peut être exportée en PDF. Pour sauvegarder ou imprimer ce matériel de formation, accédez à la [page d'impression](print_page), et sélectionnez Fichier > Imprimer > Enregistrer au format PDF.

## Matériels d'exercices

Les matériels d'exercices peuvent être téléchargés depuis le fichier [exercise-materials.zip](/exercise-materials.zip).

## Support

Pour les problèmes/bugs/suggestions ou améliorations/contributions à cette formation, veuillez utiliser le [suivi des problèmes GitHub](https://github.com/World-Meteorological-Organization/wis2box-training/issues).

Tous les bugs, améliorations et problèmes de wis2box peuvent être signalés sur [GitHub](https://github.com/World-Meteorological-Organization/wis2box/issues).

Pour un support supplémentaire ou des questions, veuillez contacter wis2-support@wmo.int.

Comme toujours, la documentation principale de wis2box est disponible sur [https://docs.wis2box.wis.wmo.int](https://docs.wis2box.wis.wmo.int).

Les contributions sont toujours encouragées et bienvenues !
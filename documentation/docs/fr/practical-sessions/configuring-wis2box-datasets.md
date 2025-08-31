---
title: Configuration des ensembles de données dans wis2box
---

# Configuration des ensembles de données dans wis2box

!!! abstract "Objectifs d'apprentissage"
    À la fin de cette session pratique, vous serez capable de :

    - Créer de nouveaux ensembles de données en utilisant le modèle par défaut et votre modèle personnalisé
    - Créer des métadonnées de découverte pour votre ensemble de données
    - Configurer les mappages de données pour votre ensemble de données
    - Publier une notification WIS2 avec un enregistrement WCMP2
    - Mettre à jour et republier votre ensemble de données

## Introduction

wis2box utilise des ensembles de données associés à des métadonnées de découverte et des mappages de données.

Les métadonnées de découverte sont utilisées pour créer un enregistrement WCMP2 (WMO Core Metadata Profile 2) qui est partagé via une notification WIS2 publiée sur votre wis2box-broker.

Les mappages de données sont utilisés pour associer un plugin de données à vos données d'entrée, permettant ainsi de transformer vos données avant leur publication via la notification WIS2.

Cette session vous guidera à travers la création de nouveaux ensembles de données en utilisant le modèle par défaut et votre modèle personnalisé, la création de métadonnées de découverte et la configuration des mappages de données. Vous inspecterez vos ensembles de données dans le wis2box-api et examinerez la notification WIS2 pour vos métadonnées de découverte.

## Préparation

Connectez-vous à votre broker en utilisant MQTT Explorer.

Au lieu d'utiliser les identifiants de votre broker interne, utilisez les identifiants publics `everyone/everyone` :

<img alt="MQTT Explorer: Connect to broker" src="/../assets/img/mqtt-explorer-wis2box-broker-everyone-everyone.png" width="800">

!!! Note

    Vous n'avez jamais besoin de partager les identifiants de votre broker interne avec des utilisateurs externes. L'utilisateur 'everyone' est un utilisateur public permettant de partager les notifications WIS2.

    Les identifiants `everyone/everyone` ont un accès en lecture seule au sujet 'origin/a/wis2/#'. C'est le sujet où les notifications WIS2 sont publiées. Le Global Broker peut s'abonner avec ces identifiants publics pour recevoir les notifications.
    
    L'utilisateur 'everyone' ne verra pas les sujets internes et ne pourra pas publier de messages.
    
Ouvrez un navigateur et accédez à la page `http://YOUR-HOST/wis2box-webapp`. Assurez-vous que vous êtes connecté et que vous pouvez accéder à la page 'dataset editor'.

Consultez la section sur [Initialisation de wis2box](./initializing-wis2box.md) si vous avez besoin de vous rappeler comment vous connecter au broker ou accéder à l'application wis2box-webapp.

## Créer un jeton d'autorisation pour processes/wis2box

Vous aurez besoin d'un jeton d'autorisation pour le point de terminaison 'processes/wis2box' afin de publier votre ensemble de données.

Pour créer un jeton d'autorisation, accédez à votre machine virtuelle de formation via SSH et utilisez les commandes suivantes pour vous connecter au conteneur wis2box-management :

```bash
cd ~/wis2box
python3 wis2box-ctl.py login
```

Ensuite, exécutez la commande suivante pour créer un jeton d'autorisation généré aléatoirement pour le point de terminaison 'processes/wis2box' :

```bash
wis2box auth add-token --path processes/wis2box
```

Vous pouvez également créer un jeton avec une valeur spécifique en fournissant le jeton comme argument à la commande :

```bash
wis2box auth add-token --path processes/wis2box MyS3cretToken
```

Assurez-vous de copier la valeur du jeton et de la stocker sur votre machine locale, car vous en aurez besoin plus tard.

Une fois que vous avez votre jeton, vous pouvez quitter le conteneur wis2box-management :

```bash
exit
```

## Création de nouveaux ensembles de données dans le wis2box-webapp

Accédez à la page 'dataset editor' dans le wis2box-webapp de votre instance wis2box en allant sur `http://YOUR-HOST/wis2box-webapp` et en sélectionnant 'dataset editor' dans le menu à gauche.

Sur la page 'dataset editor', sous l'onglet 'Datasets', cliquez sur "Create New ...":

<img alt="Create New Dataset" src="/../assets/img/wis2box-create-new-dataset.png" width="800">

Une fenêtre contextuelle apparaîtra, vous demandant de fournir :

- **Centre ID** : il s'agit de l'acronyme de l'agence (en minuscules et sans espaces), tel que spécifié par le membre de l'OMM, qui identifie le centre de données responsable de la publication des données.
- **Template** : Le modèle correspondant au type de données pour lequel vous créez des métadonnées. Vous pouvez choisir entre utiliser un modèle prédéfini ou sélectionner 'other'. Si 'other' est sélectionné, cela signifie que vous souhaitez définir un modèle personnalisé, et donc des champs supplémentaires doivent être remplis manuellement.

<img alt="Create New Dataset pop up" src="/../assets/img/wis2box-create-new-dataset-pop-up.png" width="600">

!!! Note "Centre ID"

    Votre centre-id doit commencer par le TLD de votre pays, suivi d'un tiret (`-`) et d'un nom abrégé de votre organisation (par exemple `fr-meteofrance`). Le centre-id doit être en minuscules et utiliser uniquement des caractères alphanumériques. La liste déroulante affiche tous les centre-ids actuellement enregistrés sur WIS2 ainsi que tout centre-id que vous avez déjà créé dans wis2box. Veuillez choisir un centre-id approprié pour votre organisation.

!!! Note "Template"

    Le champ *Template* vous permet de sélectionner parmi une liste de modèles disponibles dans l'éditeur d'ensembles de données du wis2box-webapp. Un modèle pré-remplit le formulaire avec des valeurs par défaut suggérées adaptées au type de données. Cela inclut un titre et des mots-clés suggérés pour les métadonnées ainsi que des plugins de données préconfigurés. Le sujet est automatiquement défini sur le sujet par défaut lié au modèle sélectionné.

    Dans le cadre de la formation, nous travaillerons avec deux options lors de la création de nouveaux ensembles de données :
    
    1. Le modèle prédéfini *weather/surface-based-observations/synop*, qui inclut des plugins de données transformant les données au format BUFR avant publication ;
    2. Le modèle *other*, qui vous permet de définir votre propre modèle personnalisé en remplissant manuellement les champs requis.

    Si vous souhaitez publier des alertes CAP en utilisant wis2box, utilisez le modèle *weather/advisories-warnings*. Ce modèle inclut un plugin de données qui vérifie que les données d'entrée sont une alerte CAP valide avant publication. Pour créer des alertes CAP et les publier via wis2box, vous pouvez utiliser le [WMO CAP Composer](https://github.com/World-Meteorological-Organization/cap-composer) ou transférer le fichier XML CAP depuis votre propre système dans le bucket wis2box-incoming.

Créons maintenant un nouvel ensemble de données en utilisant un modèle prédéfini.

## Créer un nouvel ensemble de données en utilisant un modèle prédéfini

Pour **Template**, sélectionnez **weather/surface-based-observations/synop** :

<img alt="Create New Dataset Form: Initial information" src="/../assets/img/wis2box-create-new-dataset-form-initial.png" width="450">

Cliquez sur *continue to form* pour continuer. Vous serez maintenant présenté avec le **Dataset Editor Form**.

Puisque vous avez sélectionné le modèle **weather/surface-based-observations/synop**, le formulaire sera pré-rempli avec certaines valeurs initiales liées à ce type de données.

### Création des métadonnées de découverte

Le Dataset Editor Form vous permet de fournir les métadonnées de découverte pour votre ensemble de données que le conteneur wis2box-management utilisera pour publier un enregistrement WCMP2.

Puisque vous avez sélectionné le modèle 'weather/surface-based-observations/synop', le formulaire sera pré-rempli avec des valeurs par défaut.

Assurez-vous de remplacer l'ID local généré automatiquement par un nom descriptif pour votre ensemble de données, par exemple 'synop-dataset-wis2training' :

<img alt="Metadata Editor: title, description, keywords" src="/../assets/img/wis2box-metadata-editor-part1.png" width="800">

Examinez le titre et les mots-clés, mettez-les à jour si nécessaire, et fournissez une description pour votre ensemble de données.

Notez qu'il existe des options pour modifier la 'WMO Data Policy' de 'core' à 'recommended' ou pour modifier votre identifiant de métadonnées par défaut. Veuillez conserver la politique de données comme 'core' et utiliser l'identifiant de métadonnées par défaut.

Ensuite, examinez la section définissant vos 'Propriétés temporelles' et 'Propriétés spatiales'. Vous pouvez ajuster la boîte englobante en mettant à jour les champs 'North Latitude', 'South Latitude', 'East Longitude' et 'West Longitude' :

<img alt="Metadata Editor: temporal properties, spatial properties" src="/../assets/img/wis2box-metadata-editor-part2.png" width="800">

Ensuite, remplissez la section définissant les 'Informations de contact du fournisseur de données' :

<img alt="Metadata Editor: contact information" src="/../assets/img/wis2box-metadata-editor-part3.png" width="800">

Enfin, remplissez la section définissant les 'Informations sur la qualité des données'.

Une fois que vous avez rempli toutes les sections, cliquez sur 'VALIDATE FORM' et vérifiez le formulaire pour détecter d'éventuelles erreurs :

<img alt="Metadata Editor: validation" src="/../assets/img/wis2box-metadata-validation-error.png" width="800">

S'il y a des erreurs, corrigez-les et cliquez à nouveau sur 'VALIDATE FORM'.

Assurez-vous qu'il n'y a pas d'erreurs et que vous obtenez une indication contextuelle confirmant que votre formulaire a été validé :

<img alt="Metadata Editor: validation success" src="/../assets/img/wis2box-metadata-validation-success.png" width="800">

Ensuite, avant de soumettre votre ensemble de données, examinez les mappages de données pour votre ensemble de données.

### Configuration des mappages de données

Puisque vous avez utilisé un modèle pour créer votre ensemble de données, les mappages de données ont été pré-remplis avec les plugins par défaut pour le modèle 'weather/surface-based-observations/synop'. Les plugins de données sont utilisés dans wis2box pour transformer les données avant leur publication via la notification WIS2.

<img alt="Data Mappings: update plugin" src="/../assets/img/wis2box-data-mappings.png" width="800">

Notez que vous pouvez cliquer sur le bouton "update" pour modifier les paramètres du plugin, tels que l'extension de fichier et le modèle de fichier. Vous pouvez pour l'instant conserver les paramètres par défaut. Cela sera expliqué plus en détail ultérieurement lors de la création d'un jeu de données personnalisé.

### Soumettre votre jeu de données

Enfin, vous pouvez cliquer sur 'submit' pour publier votre jeu de données.

Vous devrez fournir le jeton d'autorisation pour 'processes/wis2box' que vous avez créé précédemment. Si ce n'est pas encore fait, vous pouvez créer un nouveau jeton en suivant les instructions de la section de préparation.

Vérifiez que vous obtenez le message suivant après avoir soumis votre jeu de données, indiquant que le jeu de données a été soumis avec succès :

<img alt="Submit Dataset Success" src="/../assets/img/wis2box-submit-dataset-success.png" width="400">

Après avoir cliqué sur 'OK', vous êtes redirigé vers la page d'accueil de l'éditeur de jeux de données. Maintenant, si vous cliquez sur l'onglet 'Dataset', vous devriez voir votre nouveau jeu de données listé :

<img alt="Dataset Editor: new dataset" src="/../assets/img/wis2box-dataset-editor-new-dataset.png" width="800">

### Examiner la notification WIS2 pour vos métadonnées de découverte

Accédez à MQTT Explorer. Si vous êtes connecté au broker, vous devriez voir une nouvelle notification WIS2 publiée sur le sujet `origin/a/wis2/<your-centre-id>/metadata` :

<img alt="MQTT Explorer: WIS2 notification" src="/../assets/img/mqtt-explorer-wis2-notification-metadata.png" width="800">

Inspectez le contenu de la notification WIS2 que vous avez publiée. Vous devriez voir un JSON avec une structure correspondant au format WIS Notification Message (WNM).

!!! question

    Sur quel sujet la notification WIS2 est-elle publiée ?

??? success "Cliquez pour révéler la réponse"

    La notification WIS2 est publiée sur le sujet `origin/a/wis2/<your-centre-id>/metadata`.

!!! question

    Essayez de trouver le titre, la description et les mots-clés que vous avez fournis dans les métadonnées de découverte dans la notification WIS2. Pouvez-vous les trouver ?

??? success "Cliquez pour révéler la réponse"

    **Le titre, la description et les mots-clés que vous avez fournis dans les métadonnées de découverte ne sont pas présents dans le contenu de la notification WIS2 !**

    À la place, essayez de chercher le lien canonique dans la section "links" de la notification WIS2 :

    <img alt="WIS2 notification for metadata, links sections" src="/../assets/img/wis2-notification-metadata-links.png" width="800">

    **La notification WIS2 contient un lien canonique vers l'enregistrement WCMP2 qui a été publié.**

    Copiez-collez ce lien canonique dans votre navigateur pour accéder à l'enregistrement WCMP2. Selon les paramètres de votre navigateur, vous pourriez être invité à télécharger le fichier ou il pourrait s'afficher directement dans votre navigateur.

    Vous trouverez le titre, la description et les mots-clés que vous avez fournis dans l'enregistrement WCMP2.

wis2box fournit un nombre limité de modèles prédéfinis. Ces modèles sont conçus pour des types de jeux de données courants, mais ils peuvent ne pas toujours correspondre à des données spécialisées. Lorsque les modèles prédéfinis ne conviennent pas, un modèle personnalisé peut être créé. Cela permet aux utilisateurs de définir les champs de métadonnées requis en fonction de leur jeu de données.

Dans la section suivante, nous allons créer un nouveau jeu de données et montrer comment le configurer à l'aide d'un modèle personnalisé.

## Créer un nouveau jeu de données en configurant votre modèle personnalisé

Pour **Template**, sélectionnez **other** :

<img alt="Create New Dataset Form: Initial information" src="/../assets/img/wis2box-create-new-dataset-form-initial-other.png" width="450">

Cliquez sur *continue to form* pour continuer. Vous serez maintenant présenté avec le **Dataset Editor Form**.

Puisque le modèle *other* a été sélectionné, l'étape suivante consiste à cliquer sur *Continue* pour accéder au formulaire. Vous serez maintenant présenté avec le Dataset Editor Form. Dans ce formulaire, des champs clés tels que Titre, Description, Sujets de sous-discipline et Mots-clés doivent être remplis ou examinés par l'utilisateur. L'option Expérimental (sujet libre) contrôle la manière dont les Sujets de sous-discipline sont définis : si cette option est sélectionnée, les Sujets de sous-discipline peuvent être saisis en texte libre, permettant à l'utilisateur de définir un sujet personnalisé. Si l'option n'est pas sélectionnée, les Sujets de sous-discipline sont présentés sous forme de liste déroulante, et une des options prédéfinies doit être choisie.

### Créer des métadonnées de découverte personnalisées

À ce stade, vous devrez remplir les champs requis dans le Dataset Editor Form, y compris Titre, Description, ID local, Sujets de sous-discipline et Mots-clés.

Dans le cadre de cette formation, nous remplirons ces champs en utilisant un modèle personnalisé pour un jeu de données Global Ensemble Prediction System (GEPS) comme exemple. Cet exemple sert uniquement de référence — dans les opérations réelles de WIS2, les utilisateurs doivent personnaliser les champs de métadonnées en fonction des exigences de leurs propres jeux de données.

<img alt="Metadata Editor: title, description, keywords" src="/../assets/img/wis2box-metadata-editor-part1-other.png" width="800">

<img alt="Metadata Editor: title, description, keywords" src="/../assets/img/wis2box-metadata-editor-part1-other-2.png" width="800">

Les étapes suivantes sont les mêmes que lors de la création d'un jeu de données avec le modèle prédéfini synop. Pour des instructions détaillées, veuillez vous référer à la section *Créer des métadonnées de découverte* sous *Créer un nouveau jeu de données en utilisant un modèle prédéfini*.

### Configurer des mappages de données personnalisés

Lorsqu'un modèle personnalisé est utilisé, aucun mappage de données par défaut n'est fourni. En conséquence, l'éditeur de mappages de données sera vide et les utilisateurs doivent configurer les mappages en fonction de leurs besoins spécifiques.

<img alt="Data Mappings: update plugin" src="/../assets/img/wis2box-data-mappings-other1.png" width="800">

Dans cette formation, nous personnaliserons un jeu de données GEPS et utiliserons le plugin universel de données sans conversion comme exemple. Ce plugin est conçu pour publier des données sans appliquer de transformation. Étant donné que les données GEPS sont livrées au format GRIB2, l'extension de fichier doit être définie sur .grib2 ; sinon, les données ne pourront pas être publiées avec succès.

Une attention particulière doit être portée au champ Regex, car il affecte directement l'ingestion des données. Si l'expression régulière ne correspond pas au modèle de nommage des fichiers de données, des erreurs de publication se produiront. Pour éviter cela, mettez à jour le regex pour qu'il corresponde à la convention de nommage de votre jeu de données, ou laissez le regex par défaut inchangé et assurez-vous que vos fichiers de données sont renommés en conséquence.

<img alt="Data Mappings: update plugin" src="/../assets/img/wis2box-data-mappings-other2.png" width="800">

Dans les opérations réelles de WIS2, les utilisateurs peuvent choisir différents plugins en fonction de leurs besoins ; ici, nous utilisons uniquement le plugin universel de données sans conversion comme exemple.

Si vous souhaitez publier d'autres types et formats de données, vous pouvez cliquer sur le bouton "update" pour modifier les paramètres tels que l'extension de fichier et le modèle de fichier.

<img alt="Data Mappings: update plugin" src="/../assets/img/wis2box-data-mappings-other3.png" width="800">

### Soumettre votre jeu de données personnalisé

Le processus de soumission est le même que celui décrit dans la section *Soumettre votre jeu de données* sous *Créer un nouveau jeu de données en utilisant un modèle prédéfini*. Veuillez vous référer à cette section pour des instructions détaillées.

Après une soumission réussie, votre nouveau jeu de données apparaîtra dans l'onglet Dataset :

<img alt="Dataset Editor: new dataset" src="/../assets/img/wis2box-dataset-editor-new-dataset-other.png" width="800">

### Examiner la notification WIS2 pour vos métadonnées de découverte

Accédez à MQTT Explorer. Si vous êtes connecté au broker, vous devriez voir une nouvelle notification WIS2 publiée sur le sujet `origin/a/wis2/<your-centre-id>/metadata` :

<img alt="MQTT Explorer: WIS2 notification" src="/../assets/img/mqtt-explorer-wis2-notification-metadata-other.png" width="800">

!!! question

    Quel est l'identifiant des métadonnées du jeu de données GEPS personnalisé que vous avez créé ?

??? success "Cliquez pour révéler la réponse"

    En ouvrant l'interface utilisateur de wis2box, vous pouvez visualiser le jeu de données GEPS personnalisé. L'identifiant des métadonnées est :

    *urn:wmo:md:nl-knmi-test:customized-geps-dataset-wis2-training*

!!! question

    Si nous modifions un jeu de données, un nouveau message de notification de données sera-t-il envoyé ? Quels changements peuvent être attendus ?

??? success "Cliquez pour révéler la réponse"

    Oui. Un nouveau message de notification de données sera envoyé. Dans le message, la valeur de "rel": "canonical" dans l'élément "links" changera pour "rel": "update", indiquant que le jeu de données a été modifié.

!!! question

    Si nous supprimons un jeu de données, un nouveau message de notification de données sera-t-il envoyé ? Quels changements peuvent être attendus ?

??? success "Cliquez pour révéler la réponse"

    Oui. Un nouveau message de notification de données sera envoyé. Dans le message, la valeur de "rel": "canonical" dans l'élément "links" changera pour "rel": "deletion", indiquant que le jeu de données a été supprimé.

## Conclusion

!!! success "Félicitations !"
    Lors de cette session pratique, vous avez appris à :

    - Créer de nouveaux jeux de données en utilisant le modèle par défaut et votre modèle personnalisé
    - définir vos métadonnées de découverte
    - examiner vos mappages de données
    - publier des métadonnées de découverte
    - examiner la notification WIS2 pour vos métadonnées de découverte
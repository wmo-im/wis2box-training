---
title: Configuration des ensembles de données dans wis2box
---

# Configuration des ensembles de données dans wis2box

!!! abstract "Objectifs d'apprentissage"
    À la fin de cette session pratique, vous serez capable de :

    - utiliser l'éditeur d'ensembles de données dans wis2box-webapp
    - créer de nouveaux ensembles de données en utilisant Template=*weather/surface-based-observations/synop* et Template=*other*
    - définir vos métadonnées de découverte
    - examiner vos mappages de données
    - publier une notification WIS2 pour vos métadonnées de découverte
    - examiner la notification WIS2 pour vos métadonnées de découverte

## Introduction

wis2box utilise des ensembles de données associés à des métadonnées de découverte et des mappages de données.

Les métadonnées de découverte sont utilisées pour créer un enregistrement WCMP2 (WMO Core Metadata Profile 2) qui est partagé via une notification WIS2 publiée sur votre wis2box-broker.

Les mappages de données sont utilisés pour associer un plugin de données à vos données d'entrée, permettant ainsi leur transformation avant publication via la notification WIS2.

Cette session vous guidera dans la création de nouveaux ensembles de données en utilisant le modèle par défaut et votre modèle personnalisé, la création de métadonnées de découverte et la configuration des mappages de données. Vous examinerez vos ensembles de données dans wis2box-api et réviserez la notification WIS2 pour vos métadonnées de découverte.

## Préparation

Connectez-vous à votre broker en utilisant MQTT Explorer.

Au lieu d'utiliser les identifiants de votre broker interne, utilisez les identifiants publics `everyone/everyone` :

<img alt="MQTT Explorer : Connexion au broker" src="/../assets/img/mqtt-explorer-wis2box-broker-everyone-everyone.png" width="800">

!!! Note

    Vous n'avez jamais besoin de partager les identifiants de votre broker interne avec des utilisateurs externes. L'utilisateur 'everyone' est un utilisateur public permettant de partager les notifications WIS2.

    Les identifiants `everyone/everyone` ont un accès en lecture seule au sujet 'origin/a/wis2/#'. C'est le sujet où les notifications WIS2 sont publiées. Le Global Broker peut s'abonner avec ces identifiants publics pour recevoir les notifications.
    
    L'utilisateur 'everyone' ne verra pas les sujets internes et ne pourra pas publier de messages.
    
Ouvrez un navigateur et accédez à la page `http://YOUR-HOST/wis2box-webapp`. Assurez-vous d'être connecté et d'avoir accès à la page 'dataset editor'.

Consultez la section sur [Initialisation de wis2box](./initializing-wis2box.md) si vous avez besoin de vous rappeler comment vous connecter au broker ou accéder à wis2box-webapp.

## Créer un jeton d'autorisation pour processes/wis2box

Vous aurez besoin d'un jeton d'autorisation pour le point de terminaison 'processes/wis2box' afin de publier votre ensemble de données.

Pour créer un jeton d'autorisation, accédez à votre VM de formation via SSH et utilisez les commandes suivantes pour vous connecter au conteneur wis2box-management :

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

## Utilisation de l'éditeur d'ensembles de données

Accédez à la page 'dataset editor' dans wis2box-webapp de votre instance wis2box en allant sur `http://YOUR-HOST/wis2box-webapp` et en sélectionnant 'dataset editor' dans le menu à gauche.

Sur la page 'dataset editor', sous l'onglet 'Datasets', cliquez sur "Create New ...":

<img alt="Créer un nouvel ensemble de données" src="/../assets/img/wis2box-create-new-dataset.png" width="800">

Une fenêtre contextuelle apparaîtra, vous demandant de fournir :

- **Centre ID** : il s'agit de l'acronyme de l'agence (en minuscules et sans espaces), tel que spécifié par le Membre de l'OMM, qui identifie le centre de données responsable de la publication des données.
- **Template** : Le type de données pour lequel vous créez des métadonnées. Vous pouvez choisir entre utiliser un modèle prédéfini ou sélectionner *other*.

<img alt="Fenêtre contextuelle : Créer un nouvel ensemble de données" src="/../assets/img/wis2box-create-new-dataset-pop-up.png" width="600">

!!! Note "Centre ID"

    Votre centre-id doit commencer par le TLD de votre pays, suivi d'un tiret (`-`) et d'un nom abrégé de votre organisation (par exemple `fr-meteofrance`). Le centre-id doit être en minuscules et utiliser uniquement des caractères alphanumériques. La liste déroulante montre tous les centre-ids actuellement enregistrés sur WIS2 ainsi que tout centre-id que vous avez déjà créé dans wis2box. Veuillez choisir un centre-id approprié pour votre organisation.

!!! Note "Template"

    Le champ *Template* vous permet de sélectionner parmi une liste de modèles disponibles dans l'éditeur d'ensembles de données de wis2box-webapp. Un modèle pré-remplira le formulaire avec des valeurs par défaut suggérées adaptées au type de données. Cela inclut un titre et des mots-clés suggérés pour les métadonnées ainsi que des plugins de données préconfigurés.
    
    Le sujet est automatiquement défini sur le sujet par défaut lié au modèle sélectionné, sauf si vous sélectionnez *other*. Si vous sélectionnez *other*, le sujet peut être défini à partir d'une liste déroulante basée sur la [Hiérarchie des Sujets WIS2](https://codes.wmo.int/wis/topic-hierarchy/_earth-system-discipline).

Dans le cadre de la formation, vous créerez deux ensembles de données :
    
- Un ensemble de données utilisant Template=*weather/surface-based-observations/synop*, qui inclut des plugins de données transformant les données au format BUFR avant publication ;
- Un ensemble de données utilisant Template=*Other*, où vous serez responsable de définir le Sujet WIS2 et où vous utiliserez le plugin "Universal" pour publier les données sans transformation.

## Template=weather/surface-based-observations/synop

Pour **Template**, sélectionnez **weather/surface-based-observations/synop** :

<img alt="Formulaire : Informations initiales" src="/../assets/img/wis2box-create-new-dataset-form-initial.png" width="450">

Cliquez sur *continue to form* pour continuer, vous serez alors présenté avec le **Dataset Editor Form**.

Étant donné que vous avez sélectionné le modèle **weather/surface-based-observations/synop**, le formulaire sera pré-rempli avec certaines valeurs initiales liées à ce type de données.

### Création des métadonnées de découverte

Le Dataset Editor Form vous permet de fournir les métadonnées de découverte pour votre ensemble de données que le conteneur wis2box-management utilisera pour publier un enregistrement WCMP2.

Étant donné que vous avez sélectionné le modèle 'weather/surface-based-observations/synop', le formulaire sera pré-rempli avec des valeurs par défaut.

Veuillez vous assurer de remplacer le 'Local ID' généré automatiquement par un nom descriptif pour votre ensemble de données, par exemple 'synop-dataset-wis2training' :

<img alt="Éditeur de métadonnées : titre, description, mots-clés" src="/../assets/img/wis2box-metadata-editor-part1.png" width="800">

Examinez le titre et les mots-clés, mettez-les à jour si nécessaire, et fournissez une description pour votre ensemble de données.

Notez qu'il existe des options pour modifier la 'Politique de Données de l'OMM' de 'core' à 'recommended' ou pour modifier votre Identifiant de Métadonnées par défaut. Veuillez conserver la politique de données comme 'core' et utiliser l'Identifiant de Métadonnées par défaut.

Ensuite, examinez la section définissant vos 'Propriétés Temporelles' et 'Propriétés Spatiales'. Vous pouvez ajuster la boîte englobante en mettant à jour les champs 'Latitude Nord', 'Latitude Sud', 'Longitude Est' et 'Longitude Ouest' :

<img alt="Éditeur de métadonnées : propriétés temporelles et spatiales" src="/../assets/img/wis2box-metadata-editor-part2.png" width="800">

Ensuite, remplissez la section définissant les 'Informations de Contact du Fournisseur de Données' :

<img alt="Éditeur de métadonnées : informations de contact" src="/../assets/img/wis2box-metadata-editor-part3.png" width="800">

Enfin, remplissez la section définissant les 'Informations sur la Qualité des Données'.

Une fois que vous avez rempli toutes les sections, cliquez sur 'VALIDATE FORM' et vérifiez le formulaire pour toute erreur :

<img alt="Éditeur de métadonnées : validation" src="/../assets/img/wis2box-metadata-validation-error.png" width="800">

S'il y a des erreurs, corrigez-les et cliquez à nouveau sur 'VALIDATE FORM'.

Assurez-vous qu'il n'y a pas d'erreurs et que vous obtenez une indication contextuelle confirmant que votre formulaire a été validé :

<img alt="Éditeur de métadonnées : validation réussie" src="/../assets/img/wis2box-metadata-validation-success.png" width="800">

Ensuite, avant de soumettre votre ensemble de données, examinez les mappages de données pour votre ensemble de données.

### Configuration des mappages de données

Étant donné que vous avez utilisé un modèle pour créer votre ensemble de données, les mappages de données ont été pré-remplis avec les plugins par défaut pour le modèle 'weather/surface-based-observations/synop'. Les plugins de données sont utilisés dans wis2box pour transformer les données avant qu'elles ne soient publiées via la notification WIS2.

<img alt="Mappages de données : mise à jour du plugin" src="/../assets/img/wis2box-data-mappings.png" width="800">

Notez que vous pouvez cliquer sur le bouton "update" pour modifier les paramètres du plugin, tels que l'extension de fichier et le modèle de fichier. Vous pouvez laisser les paramètres par défaut pour l'instant. Cela sera expliqué plus en détail plus tard lors de la création d'un ensemble de données personnalisé.

### Soumission de votre ensemble de données

Enfin, vous pouvez cliquer sur 'submit' pour publier votre ensemble de données.

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

wis2box fournit un nombre limité de modèles prédéfinis. Ces modèles sont conçus pour des types de jeux de données courants, mais ils peuvent ne pas toujours correspondre à des données spécialisées. Pour tous les autres types de jeux de données, vous pouvez créer votre jeu de données en sélectionnant Template=*other*.

## Template=other

Ensuite, nous allons créer un deuxième jeu de données en utilisant Template=*other*.

Cliquez sur "Create New ..." pour créer un nouveau jeu de données. Utilisez le même centre-id que précédemment, il devrait être disponible dans la liste déroulante. Pour **Template**, sélectionnez **other** :

<img alt="Create New Dataset Form: Initial information" src="/../assets/img/wis2box-create-new-dataset-form-initial-other.png" width="450">

Cliquez sur *continue to form* pour continuer. Vous serez maintenant présenté avec le **Dataset Editor Form**, légèrement différent du précédent.

### Création de métadonnées de découverte

Comme précédemment, vous devrez remplir les champs obligatoires dans le Dataset Editor Form, y compris Title, Description et Local ID :

<img alt="Metadata Editor: title, description, keywords" src="/../assets/img/wis2box-metadata-editor-part1-other.png" width="800">

Notez que puisque vous avez sélectionné Template=*other*, il vous appartient de définir la hiérarchie des sujets WIS2 en utilisant les listes déroulantes pour 'Discipline' et 'Sub-Discipline'.

Pour cet exercice, veuillez sélectionner le sujet de sous-discipline "prediction/analysis/medium-range/deterministic/global" :

<img alt="Metadata Editor: title, description, keywords" src="/../assets/img/wis2box-metadata-editor-part1-other-topic.png" width="800">

Puisque vous avez utilisé Template=*other*, aucun mot-clé n'a été prédéfini. Assurez-vous d'ajouter au moins 3 mots-clés de votre choix :

<img alt="Metadata Editor: title, description, keywords" src="/../assets/img/wis2box-metadata-editor-part1-other-2.png" width="800">

Après avoir rempli les champs obligatoires, complétez les sections restantes du formulaire, y compris 'Temporal Properties', 'Spatial Properties' et 'Contact Information of the Data Provider', et assurez-vous de valider le formulaire.

### Configuration des mappages de données

Lorsqu'un modèle personnalisé est utilisé, aucun mappage de données par défaut n'est fourni. Par conséquent, l'éditeur de mappages de jeux de données sera vide et les utilisateurs doivent configurer les mappages selon leurs besoins spécifiques.

<img alt="Data Mappings: update plugin" src="/../assets/img/wis2box-data-mappings-other1.png" width="800">

Cliquez sur "ADD A PLUGIN +" pour ajouter un plugin de données à votre jeu de données.

Sélectionnez le plugin nommé **"Universal data without conversion"**. Ce plugin est conçu pour publier des données sans appliquer de transformation.

Lors de l'ajout de ce plugin, vous devrez spécifier l'**extension de fichier** et un **modèle de fichier** (défini par une expression régulière) correspondant au modèle de nommage de vos fichiers de données. Dans le cas du plugin "Universal", le modèle de fichier est également utilisé pour déterminer la propriété "datetime" des données.

!!! Note "Analyse de la date et de l'heure à partir du nom de fichier"

    Le plugin "Universal" suppose que le premier groupe dans l'expression régulière correspond à la date et à l'heure des données. 

    Le modèle de fichier par défaut est `^.*?_(\d{8}).*?\..*$`, qui correspond à 8 chiffres précédés d'un underscore et suivis de tout caractère et d'un point avant l'extension de fichier. Par exemple :

    - `mydata_20250101.txt` correspondra et extraira le 25 janvier 2025 comme propriété datetime des données
    - `mydata_2025010112.txt` ne correspondra pas, car il y a 10 chiffres au lieu de 8
    - `mydata-20250101.txt` ne correspondra pas, car il y a un tiret au lieu d'un underscore avant la date

    Lors de l'ingestion de données avec le plugin "Universal", renommez vos fichiers pour qu'ils correspondent au modèle par défaut ou mettez à jour le modèle de fichier en veillant à ce que le premier groupe dans l'expression régulière corresponde à la date et à l'heure.

Gardez les valeurs par défaut pour "File Name" pour l'instant, car elles correspondent aux données que vous ingérerez lors de la prochaine session pratique :

<img alt="Data Mappings: update plugin" src="/../assets/img/wis2box-data-mappings-other2.png" width="800">

Cliquez sur "SAVE" pour enregistrer les paramètres du plugin et vérifiez que le plugin apparaît maintenant dans l'éditeur de mappages de jeux de données :

<img alt="Data Mappings: update plugin" src="/../assets/img/wis2box-data-mappings-other3.png" width="800">

Notez que lorsque vous ingérerez des données, l'extension de fichier et le modèle de fichier doivent correspondre aux paramètres que vous avez fournis ici, sinon les données ne seront pas traitées et le conteneur wis2box-management enregistrera des messages d'erreur.

### Soumettre et examiner le résultat

Enfin, fournissez le jeton d'autorisation pour 'processes/wis2box' que vous avez créé précédemment et cliquez sur 'submit' pour publier votre jeu de données.

Après une soumission réussie, votre nouveau jeu de données apparaîtra dans l'onglet Dataset :

<img alt="Dataset Editor: new dataset" src="/../assets/img/wis2box-dataset-editor-new-dataset-other.png" width="800">

Accédez à MQTT Explorer. Si vous êtes connecté à votre broker, vous devriez voir une autre nouvelle notification WIS2 publiée sur le sujet `origin/a/wis2/<your-centre-id>/metadata`.

!!! question

    Visitez l'interface utilisateur wis2box à `http://YOUR-HOST`. Combien de jeux de données voyez-vous listés ? Comment pouvez-vous visualiser la hiérarchie des sujets WIS2 utilisée pour chaque jeu de données et comment pouvez-vous voir la description de chaque jeu de données ?

??? success "Cliquez pour révéler la réponse"

    En ouvrant l'interface utilisateur wis2box à `http://YOUR-HOST`, vous devriez voir 2 jeux de données listés avec leur hiérarchie des sujets WIS2. Pour voir la description de chaque jeu de données, vous pouvez cliquer sur "metadata", ce qui redirigera vers l'élément 'discovery-metadata' correspondant tel que servi par l'API wis2box.

!!! question

    Essayez de mettre à jour la description du dernier jeu de données que vous avez créé. Après avoir mis à jour la description, voyez-vous une nouvelle notification WIS2 publiée sur le sujet `origin/a/wis2/<your-centre-id>/metadata` ? Quelle est la différence entre la nouvelle notification et la précédente ?

??? success "Cliquez pour révéler la réponse"

    Vous devriez voir un nouveau message de notification de données envoyé après la mise à jour de votre jeu de données sur le sujet `origin/a/wis2/<your-centre-id>/metadata`.
    
    Dans le message, la valeur de *"rel": "canonical"* changera en *"rel": "update"*, indiquant que les données publiées précédemment ont été modifiées. Pour voir la description mise à jour, copiez-collez l'URL dans votre navigateur et vous devriez voir la description mise à jour.

!!! question

    Essayez de mettre à jour la hiérarchie des sujets du dernier jeu de données que vous avez créé en modifiant la sélection dans "Sub-Discipline Topics". Voyez-vous une nouvelle notification WIS2 publiée sur le sujet `origin/a/wis2/<your-centre-id>/metadata` ?

??? success "Cliquez pour révéler la réponse"

Vous **ne pouvez pas** modifier la hiérarchie des sujets d'un ensemble de données existant. Le champ Hiérarchie des sujets est désactivé dans le formulaire d'édition de l'ensemble de données après sa création. Si vous souhaitez utiliser une hiérarchie des sujets différente, supprimez d'abord l'ensemble de données existant, puis créez un nouvel ensemble de données avec la hiérarchie des sujets souhaitée.

## Conclusion

!!! success "Félicitations !"
    Au cours de cette session pratique, vous avez appris à :

    - utiliser l'éditeur d'ensembles de données dans wis2box-webapp
    - créer de nouveaux ensembles de données en utilisant Template=*weather/surface-based-observations/synop* et Template=*other*
    - définir vos métadonnées de découverte
    - examiner vos correspondances de données
    - publier les métadonnées de découverte
    - examiner la notification WIS2 pour vos métadonnées de découverte
---
title: Configuration d'un ensemble de données recommandé avec contrôle d'accès
---

# Configuration d'un ensemble de données recommandé avec contrôle d'accès

!!! abstract "Résultats d'apprentissage"
    À la fin de cette session pratique, vous serez capable de :

    - créer un nouvel ensemble de données avec la politique de données 'recommandé'
    - ajouter un jeton d'accès à l'ensemble de données
    - valider que l'ensemble de données ne peut pas être accédé sans le jeton d'accès
    - ajouter le jeton d'accès aux en-têtes HTTP pour accéder à l'ensemble de données

## Introduction

Les ensembles de données qui ne sont pas considérés comme des ensembles de données 'core' à l'OMM peuvent éventuellement être configurés avec une politique de contrôle d'accès. wis2box fournit un mécanisme pour ajouter un jeton d'accès à un ensemble de données qui empêchera les utilisateurs de télécharger des données à moins qu'ils ne fournissent le jeton d'accès dans les en-têtes HTTP.

## Préparation

Assurez-vous d'avoir un accès SSH à votre VM étudiante et que votre instance wis2box est opérationnelle.

Assurez-vous que vous êtes connecté au courtier MQTT de votre instance wis2box en utilisant MQTT Explorer. Vous pouvez utiliser les identifiants publics `everyone/everyone` pour vous connecter au courtier.

Assurez-vous d'avoir un navigateur web ouvert avec le wis2box-webapp pour votre instance en allant à `http://YOUR-HOST/wis2box-webapp`.

## Créer un nouvel ensemble de données avec la politique de données 'recommandé'

Allez à la page 'éditeur d'ensembles de données' dans le wis2box-webapp et créez un nouvel ensemble de données. Sélectionnez le Type de Données = 'weather/surface-weather-observations/synop'.

<img alt="create-dataset-recommended" src="/../assets/img/create-dataset-template.png" width="800">

Pour "Centre ID", utilisez le même que celui que vous avez utilisé dans les sessions pratiques précédentes.

Cliquez sur 'CONTINUE To FORM' pour continuer.

Dans l'éditeur d'ensembles de données, définissez la politique de données à 'recommandé' (notez que changer la politique de données mettra à jour la 'Hiérarchie des sujets').
Remplacez l'ID local généré automatiquement par un nom descriptif pour l'ensemble de données, par exemple 'recommended-data-with-access-control':

<img alt="create-dataset-recommended" src="/../assets/img/create-dataset-recommended.png" width="800">

Continuez à remplir les champs requis pour les Propriétés Spatiales et les Informations de Contact, et 'Validez le formulaire' pour vérifier s'il y a des erreurs.

Enfin, soumettez l'ensemble de données, en utilisant le jeton d'authentification créé précédemment, et vérifiez que le nouvel ensemble de données est créé dans le wis2box-webapp.

Vérifiez MQTT-explorer pour voir que vous recevez le Message de Notification WIS2 annonçant le nouvel enregistrement de Métadonnées de Découverte sur le sujet `origin/a/wis2/<your-centre-id>/metadata`.	

## Ajouter un jeton d'accès à l'ensemble de données

Connectez-vous au conteneur wis2box-management,

```bash
cd ~/wis2box
python3 wis2box-ctl.py login
```

Depuis la ligne de commande à l'intérieur du conteneur, vous pouvez sécuriser un ensemble de données en utilisant la commande `wis2box auth add-token`, en utilisant l'option `--metadata-id` pour spécifier l'identifiant de métadonnées de l'ensemble de données et le jeton d'accès en argument.

Par exemple, pour ajouter le jeton d'accès `S3cr3tT0k3n` à l'ensemble de données avec l'identifiant de métadonnées `urn:wmo:md:not-my-centre:core.surface-based-observations.synop`:	

```bash
wis2box auth add-token --metadata-id urn:wmo:md:not-my-centre:reco.surface-based-observations.synop S3cr3tT0k3n
```

Sortez du conteneur wis2box-management :

```bash
exit
```

## Publier des données dans l'ensemble de données

Copiez le fichier `exercise-materials/access-control-exercises/aws-example.csv` dans le répertoire défini par `WIS2BOX_HOST_DATADIR` dans votre `wis2box.env` :

```bash
cp ~/exercise-materials/access-control-exercises/aws-example.csv ~/wis2box-data
```

Ensuite, utilisez WinSCP ou un éditeur de ligne de commande pour modifier le fichier `aws-example.csv` et mettre à jour les identifiants de station WIGOS dans les données d'entrée pour correspondre aux stations que vous avez dans votre instance wis2box.

Ensuite, allez à l'éditeur de station dans le wis2box-webapp. Pour chaque station que vous avez utilisée dans `aws-example.csv`, mettez à jour le champ 'sujet' pour qu'il corresponde au 'sujet' de l'ensemble de données que vous avez créé dans l'exercice précédent.

Cette station sera maintenant associée à 2 sujets, un pour l'ensemble de données 'core' et un pour l'ensemble de données 'recommandé' :

<img alt="edit-stations-add-topics" src="/../assets/img/edit-stations-add-topics.png" width="600">

Vous devrez utiliser votre jeton pour `collections/stations` pour sauvegarder les données de station mises à jour.

Ensuite, connectez-vous au conteneur wis2box-management :

```bash
cd ~/wis2box
python3 wis2box-ctl.py login
```

Depuis la ligne de commande wis2box, nous pouvons ingérer le fichier de données d'exemple `aws-example.csv` dans un ensemble de données spécifique comme suit :

```bash
wis2box data ingest -p /data/wis2box/aws-example.csv --metadata-id urn:wmo:md:not-my-centre:reco.surface-based-observations.synop
```

Assurez-vous de fournir l'identifiant de métadonnées correct pour votre ensemble de données et **vérifiez que vous recevez des notifications de données WIS2 dans MQTT Explorer**, sur le sujet `origin/a/wis2/<your-centre-id>/data/recommended/surface-based-observations/synop`.

Vérifiez le lien canonique dans le Message de Notification WIS2 et copiez/collez le lien dans le navigateur pour essayer de télécharger les données.

Vous devriez voir une erreur 403 Forbidden.

## Ajouter le jeton d'accès aux en-têtes HTTP pour accéder à l'ensemble de données

Afin de démontrer que le jeton d'accès est nécessaire pour accéder à l'ensemble de données, nous allons reproduire l'erreur que vous avez vue dans le navigateur en utilisant la fonction de ligne de commande `wget`.

Depuis la ligne de commande dans votre VM étudiante, utilisez la commande `wget` avec le lien canonique que vous avez copié du Message de Notification WIS2.

```bash
wget <canonical-link>
```

Vous devriez voir que la requête HTTP renvoie avec *401 Unauthorized* et que les données ne sont pas téléchargées.

Ajoutez maintenant le jeton d'accès aux en-têtes HTTP pour accéder à l'ensemble de données.

```bash
wget --header="Authorization: Bearer S3cr3tT0k3n" <canonical-link>
```

Maintenant, les données devraient être téléchargées avec succès.

## Conclusion

!!! success "Félicitations !"
    Dans cette session pratique, vous avez appris à :

    - créer un nouvel ensemble de données avec la politique de données 'recommandé'
    - ajouter un jeton d'accès à l'ensemble de données
    - valider que l'ensemble de données ne peut pas être accédé sans le jeton d'accès
    - ajouter le jeton d'accès aux en-têtes HTTP pour accéder à l'ensemble de données
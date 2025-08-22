---
title: Configuration d'un jeu de données recommandé avec contrôle d'accès
---

# Configuration d'un jeu de données recommandé avec contrôle d'accès

!!! abstract "Objectifs d'apprentissage"
    À la fin de cette session pratique, vous serez capable de :

    - créer un nouveau jeu de données avec une politique de données 'recommended'
    - ajouter un jeton d'accès au jeu de données
    - vérifier que le jeu de données ne peut pas être consulté sans le jeton d'accès
    - ajouter le jeton d'accès aux en-têtes HTTP pour accéder au jeu de données

## Introduction

Les jeux de données qui ne sont pas considérés comme 'core' dans le cadre de l'OMM peuvent être configurés avec une politique de contrôle d'accès. wis2box fournit un mécanisme permettant d'ajouter un jeton d'accès à un jeu de données, empêchant ainsi les utilisateurs de télécharger les données à moins qu'ils ne fournissent le jeton d'accès dans les en-têtes HTTP.

## Préparation

Assurez-vous d'avoir un accès SSH à votre machine virtuelle étudiante et que votre instance wis2box est opérationnelle.

Vérifiez que vous êtes connecté au broker MQTT de votre instance wis2box en utilisant MQTT Explorer. Vous pouvez utiliser les identifiants publics `everyone/everyone` pour vous connecter au broker.

Assurez-vous d'avoir un navigateur web ouvert avec le wis2box-webapp de votre instance en accédant à `http://YOUR-HOST/wis2box-webapp`.

## Créer un nouveau jeu de données avec une politique de données 'recommended'

Accédez à la page 'dataset editor' dans le wis2box-webapp et créez un nouveau jeu de données. Sélectionnez le Data Type = 'weather/surface-weather-observations/synop'.

<img alt="create-dataset-recommended" src="/../assets/img/create-dataset-template.png" width="800">

Pour "Centre ID", utilisez le même identifiant que celui utilisé dans les sessions pratiques précédentes.

Cliquez sur 'CONTINUE TO FORM' pour continuer.

Remplacez le 'Local ID' généré automatiquement par un nom descriptif pour le jeu de données, par exemple 'recommended-data-with-access-control', et mettez à jour les champs 'Title' et 'Description' :

<img alt="create-dataset-recommended" src="/../assets/img/create-dataset-recommended.png" width="800">

Changez la politique de données de l'OMM en 'recommended' et vous verrez qu'un nouveau champ de saisie pour une URL fournissant les informations de licence a été ajouté au formulaire :

<img alt="create-dataset-license" src="/../assets/img/create-dataset-license.png" width="800">

Vous avez la possibilité de fournir une URL vers une licence décrivant les conditions d'utilisation du jeu de données. Par exemple, vous pourriez utiliser 
`https://creativecommons.org/licenses/by/4.0/` 
pour pointer vers la licence Creative Commons Attribution 4.0 International (CC BY 4.0).

Ou vous pouvez utiliser `WIS2BOX_URL/data/license.txt` pour pointer vers un fichier de licence personnalisé hébergé sur votre propre serveur web, où `WIS2BOX_URL` est l'URL que vous avez définie dans le fichier wis2box.env :

<img alt="create-dataset-license-url" src="/../assets/img/create-dataset-license-custom.png" width="800">

Continuez à remplir les champs requis pour les Propriétés Spatiales et les Informations de Contact, puis cliquez sur 'Validate form' pour vérifier les éventuelles erreurs.

Enfin, soumettez le jeu de données en utilisant le jeton d'authentification précédemment créé, et vérifiez que le nouveau jeu de données est créé dans le wis2box-webapp.

Vérifiez dans MQTT Explorer que vous recevez le message de notification WIS2 annonçant le nouvel enregistrement de métadonnées de découverte sur le sujet `origin/a/wis2/<your-centre-id>/metadata`.

## Examiner votre nouveau jeu de données dans le wis2box-api

Consultez la liste des jeux de données dans le wis2box-api en ouvrant l'URL `WIS2BOX_URL/oapi/collections/discovery-metadata/items` dans votre navigateur web, en remplaçant `WIS2BOX_URL` par l'URL de votre instance wis2box.

Ouvrez le lien du jeu de données que vous venez de créer et faites défiler jusqu'à la section 'links' de la réponse JSON :

<img alt="wis2box-api-recommended-dataset-links" src="/../assets/img/wis2box-api-recommended-dataset-links.png" width="600">

Vous devriez voir un lien pour "License for this dataset" pointant vers l'URL que vous avez fournie dans l'éditeur de jeu de données.

Si vous avez utilisé `http://YOUR-HOST/data/license.txt` comme URL de licence, le lien ne fonctionnera pas pour le moment, car nous n'avons pas encore ajouté de fichier de licence à l'instance wis2box.

Si le temps le permet, vous pouvez ajouter un fichier de licence personnalisé à votre instance wis2box à la fin de cette session pratique. Pour l'instant, nous allons continuer avec l'ajout d'un jeton d'accès au jeu de données.

## Ajouter un jeton d'accès au jeu de données

Connectez-vous au conteneur wis2box-management,

```bash
cd ~/wis2box
python3 wis2box-ctl.py login
```

Depuis la ligne de commande à l'intérieur du conteneur, vous pouvez sécuriser un jeu de données en utilisant la commande `wis2box auth add-token`, avec l'option `--metadata-id` pour spécifier l'identifiant de métadonnées du jeu de données et le jeton d'accès comme argument.

Par exemple, pour ajouter le jeton d'accès `S3cr3tT0k3n` au jeu de données avec l'identifiant de métadonnées `urn:wmo:md:not-my-centre:core.surface-based-observations.synop` :

```bash
wis2box auth add-token --metadata-id urn:wmo:md:not-my-centre:reco.surface-based-observations.synop S3cr3tT0k3n
```

Quittez le conteneur wis2box-management :

```bash
exit
```

## Publier des données dans le jeu de données

Copiez le fichier `exercise-materials/access-control-exercises/aws-example.csv` dans le répertoire défini par `WIS2BOX_HOST_DATADIR` dans votre fichier `wis2box.env` :

```bash
cp ~/exercise-materials/access-control-exercises/aws-example.csv ~/wis2box-data
```

Ensuite, utilisez WinSCP ou un éditeur de ligne de commande pour modifier le fichier `aws-example.csv` et mettre à jour les identifiants de stations WIGOS dans les données d'entrée afin qu'ils correspondent aux stations présentes dans votre instance wis2box.

Ensuite, accédez à l'éditeur de stations dans le wis2box-webapp. Pour chaque station utilisée dans `aws-example.csv`, mettez à jour le champ 'topic' pour qu'il corresponde au 'topic' du jeu de données que vous avez créé dans l'exercice précédent.

Cette station sera désormais associée à 2 topics, un pour le jeu de données 'core' et un pour le jeu de données 'recommended' :

<img alt="edit-stations-add-topics" src="/../assets/img/edit-stations-add-topics.png" width="600">

Vous devrez utiliser votre jeton pour `collections/stations` afin d'enregistrer les données de station mises à jour.

Ensuite, connectez-vous au conteneur wis2box-management :

```bash
cd ~/wis2box
python3 wis2box-ctl.py login
```

Depuis la ligne de commande wis2box, nous pouvons ingérer le fichier de données exemple `aws-example.csv` dans un jeu de données spécifique comme suit :

```bash
wis2box data ingest -p /data/wis2box/aws-example.csv --metadata-id urn:wmo:md:not-my-centre:reco.surface-based-observations.synop
```

Assurez-vous de fournir le bon identifiant de métadonnées pour votre jeu de données et **vérifiez que vous recevez des notifications de données WIS2 dans MQTT Explorer**, sur le sujet `origin/a/wis2/<your-centre-id>/data/recommended/surface-based-observations/synop`.

Vérifiez le lien canonique dans le message de notification WIS2 et copiez/collez le lien dans le navigateur pour essayer de télécharger les données.

Vous devriez voir une erreur *401 Authorization Required*.

## Ajouter le jeton d'accès aux en-têtes HTTP pour accéder au jeu de données

Pour démontrer que le jeton d'accès est nécessaire pour accéder au jeu de données, nous allons reproduire l'erreur que vous avez vue dans le navigateur en utilisant la fonction `wget` en ligne de commande.

Depuis la ligne de commande de votre machine virtuelle étudiante, utilisez la commande `wget` avec le lien canonique que vous avez copié depuis le message de notification WIS2.

```bash
wget <canonical-link>
```

Vous devriez voir que la requête HTTP retourne une erreur *401 Unauthorized* et que les données ne sont pas téléchargées.

Ajoutez maintenant le jeton d'accès aux en-têtes HTTP pour accéder au jeu de données.

```bash
wget --header="Authorization: Bearer S3cr3tT0k3n" <canonical-link>
```

Les données devraient maintenant être téléchargées avec succès.

## Ajouter un fichier de licence personnalisé à votre instance wis2box (optionnel)

Créez un fichier texte sur votre machine locale en utilisant votre éditeur de texte préféré et ajoutez des informations de licence au fichier, telles que :

*Il s'agit d'un fichier de licence personnalisé pour le jeu de données recommandé avec contrôle d'accès. Vous êtes libre d'utiliser ces données, mais veuillez reconnaître le fournisseur des données.*

Pour télécharger un fichier localement créé nommé license.txt, utilisez la console MinIO disponible sur le port 9001 de l'instance wis2box, en accédant à un navigateur web et en visitant `http://YOUR-HOST:9001`.

Les identifiants pour accéder à la console MinIO dans le fichier wis2box.env sont définis par les variables d'environnement `WIS2BOX_STORAGE_USERNAME` et `WIS2BOX_STORAGE_PASSWORD`. Vous pouvez les trouver dans le fichier wis2box.env comme suit :

```bash
cat wis2box.env | grep WIS2BOX_STORAGE_USERNAME
cat wis2box.env | grep WIS2BOX_STORAGE_PASSWORD
```

Une fois connecté à la console MinIO, vous pouvez télécharger le fichier de licence dans le chemin de base du bucket **wis2box-public** en utilisant le bouton “Upload” :

<img alt="minio-upload-license" src="/../assets/img/minio-upload-license.png" width="800">

Après avoir téléchargé le fichier de licence, vérifiez si le fichier est accessible en visitant `WIS2BOX_URL/data/license.txt` dans votre navigateur web, en remplaçant `WIS2BOX_URL` par l'URL de votre instance wis2box.

!!! note

    Le proxy web dans wis2box redirige tous les fichiers stockés dans le bucket "wis2box-public" sous le chemin `WIS2BOX_URL/data/`

Le lien pour "License for this dataset" inclus dans les métadonnées de votre jeu de données recommandé devrait maintenant fonctionner.

## Conclusion

!!! success "Félicitations !"
    Au cours de cette session pratique, vous avez appris à :

    - créer un nouveau jeu de données avec une politique de données 'recommended'
    - ajouter un jeton d'accès au jeu de données
    - vérifier que le jeu de données ne peut pas être consulté sans le jeton d'accès
    - ajouter le jeton d'accès aux en-têtes HTTP pour accéder au jeu de données
    - ajouter un fichier de licence personnalisé à votre instance wis2box
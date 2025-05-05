---
title: Configuration d'un jeu de données recommandé avec contrôle d'accès
---

# Configuration d'un jeu de données recommandé avec contrôle d'accès

!!! abstract "Objectifs d'apprentissage"
    À la fin de cette session pratique, vous serez capable de :

    - créer un nouveau jeu de données avec une politique de données 'recommended'
    - ajouter un jeton d'accès au jeu de données
    - vérifier que le jeu de données n'est pas accessible sans le jeton d'accès
    - ajouter le jeton d'accès aux en-têtes HTTP pour accéder au jeu de données

## Introduction

Les jeux de données qui ne sont pas considérés comme des jeux de données 'core' dans WMO peuvent être configurés avec une politique de contrôle d'accès. wis2box fournit un mécanisme pour ajouter un jeton d'accès à un jeu de données qui empêchera les utilisateurs de télécharger les données s'ils ne fournissent pas le jeton d'accès dans les en-têtes HTTP.

## Préparation

Assurez-vous d'avoir un accès SSH à votre machine virtuelle étudiante et que votre instance wis2box est opérationnelle.

Vérifiez que vous êtes connecté au broker MQTT de votre instance wis2box en utilisant MQTT Explorer. Vous pouvez utiliser les identifiants publics `everyone/everyone` pour vous connecter au broker.

Assurez-vous d'avoir un navigateur web ouvert avec le wis2box-webapp de votre instance en allant sur `http://YOUR-HOST/wis2box-webapp`.

## Créer un nouveau jeu de données avec la politique de données 'recommended'

Accédez à la page 'dataset editor' dans le wis2box-webapp et créez un nouveau jeu de données. Sélectionnez Data Type = 'weather/surface-weather-observations/synop'.

<img alt="create-dataset-recommended" src="../../assets/img/create-dataset-template.png" width="800">

Pour "Centre ID", utilisez le même que celui utilisé dans les sessions pratiques précédentes.

Cliquez sur 'CONTINUE To FORM' pour continuer.

Dans l'éditeur de jeu de données, définissez la politique de données sur 'recommended' (notez que la modification de la politique de données mettra à jour la 'Topic Hierarchy').
Remplacez le 'Local ID' généré automatiquement par un nom descriptif pour le jeu de données, par exemple 'recommended-data-with-access-control' :

<img alt="create-dataset-recommended" src="../../assets/img/create-dataset-recommended.png" width="800">

Continuez à remplir les champs requis pour les Propriétés Spatiales et les Informations de Contact, et 'Validate form' pour vérifier les éventuelles erreurs.

Enfin, soumettez le jeu de données en utilisant le jeton d'authentification précédemment créé, et vérifiez que le nouveau jeu de données est créé dans le wis2box-webapp.

Vérifiez dans MQTT-explorer que vous recevez le Message de Notification WIS2 annonçant le nouveau registre de Métadonnées de Découverte sur le sujet `origin/a/wis2/<your-centre-id>/metadata`.

## Ajouter un jeton d'accès au jeu de données

Connectez-vous au conteneur wis2box-management,

```bash
cd ~/wis2box
python3 wis2box-ctl.py login
```

Depuis la ligne de commande à l'intérieur du conteneur, vous pouvez sécuriser un jeu de données en utilisant la commande `wis2box auth add-token`, en utilisant le drapeau `--metadata-id` pour spécifier l'identifiant de métadonnées du jeu de données et le jeton d'accès comme argument.

Par exemple, pour ajouter le jeton d'accès `S3cr3tT0k3n` au jeu de données avec l'identifiant de métadonnées `urn:wmo:md:not-my-centre:core.surface-based-observations.synop` :

```bash
wis2box auth add-token --metadata-id urn:wmo:md:not-my-centre:reco.surface-based-observations.synop S3cr3tT0k3n
```

Quittez le conteneur wis2box-management :

```bash
exit
```

## Publier des données dans le jeu de données

Copiez le fichier `exercise-materials/access-control-exercises/aws-example.csv` dans le répertoire défini par `WIS2BOX_HOST_DATADIR` dans votre `wis2box.env` :

```bash
cp ~/exercise-materials/access-control-exercises/aws-example.csv ~/wis2box-data
```

Ensuite, utilisez WinSCP ou un éditeur en ligne de commande pour modifier le fichier `aws-example.csv` et mettre à jour les identifiants WIGOS-station dans les données d'entrée pour correspondre aux stations que vous avez dans votre instance wis2box.

Ensuite, allez dans l'éditeur de stations dans le wis2box-webapp. Pour chaque station que vous avez utilisée dans `aws-example.csv`, mettez à jour le champ 'topic' pour correspondre au 'topic' du jeu de données que vous avez créé dans l'exercice précédent.

Cette station sera maintenant associée à 2 sujets, un pour le jeu de données 'core' et un pour le jeu de données 'recommended' :

<img alt="edit-stations-add-topics" src="../../assets/img/edit-stations-add-topics.png" width="600">

Vous devrez utiliser votre jeton pour `collections/stations` pour sauvegarder les données de station mises à jour.

Ensuite, connectez-vous au conteneur wis2box-management :

```bash
cd ~/wis2box
python3 wis2box-ctl.py login
```

Depuis la ligne de commande wis2box, nous pouvons ingérer le fichier de données exemple `aws-example.csv` dans un jeu de données spécifique comme suit :

```bash
wis2box data ingest -p /data/wis2box/aws-example.csv --metadata-id urn:wmo:md:not-my-centre:reco.surface-based-observations.synop
```

Assurez-vous de fournir l'identifiant de métadonnées correct pour votre jeu de données et **vérifiez que vous recevez des notifications de données WIS2 dans MQTT Explorer**, sur le sujet `origin/a/wis2/<your-centre-id>/data/recommended/surface-based-observations/synop`.

Vérifiez le lien canonique dans le Message de Notification WIS2 et copiez/collez le lien dans le navigateur pour essayer de télécharger les données.

Vous devriez voir une erreur 403 Forbidden.

## Ajouter le jeton d'accès aux en-têtes HTTP pour accéder au jeu de données

Pour démontrer que le jeton d'accès est nécessaire pour accéder au jeu de données, nous allons reproduire l'erreur que vous avez vue dans le navigateur en utilisant la fonction `wget` en ligne de commande.

Depuis la ligne de commande de votre machine virtuelle étudiante, utilisez la commande `wget` avec le lien canonique que vous avez copié du Message de Notification WIS2.

```bash
wget <canonical-link>
```

Vous devriez voir que la requête HTTP retourne *401 Unauthorized* et les données ne sont pas téléchargées.

Maintenant ajoutez le jeton d'accès aux en-têtes HTTP pour accéder au jeu de données.

```bash
wget --header="Authorization: Bearer S3cr3tT0k3n" <canonical-link>
```

Maintenant les données devraient être téléchargées avec succès.

## Conclusion

!!! success "Félicitations !"
    Dans cette session pratique, vous avez appris à :

    - créer un nouveau jeu de données avec une politique de données 'recommended'
    - ajouter un jeton d'accès au jeu de données
    - vérifier que le jeu de données n'est pas accessible sans le jeton d'accès
    - ajouter le jeton d'accès aux en-têtes HTTP pour accéder au jeu de données
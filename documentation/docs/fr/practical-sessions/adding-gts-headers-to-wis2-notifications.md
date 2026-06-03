---
title: Ajout des en-têtes GTS aux notifications WIS2
---

# Ajout des en-têtes GTS aux notifications WIS2

!!! abstract "Objectifs d'apprentissage"

    À la fin de cette session pratique, vous serez capable de :
    
    - configurer une correspondance entre le nom de fichier et les en-têtes GTS
    - intégrer des données avec un nom de fichier correspondant aux en-têtes GTS
    - visualiser les en-têtes GTS dans les notifications WIS2
    - utiliser le formulaire FM-12 SYNOP pour ajouter manuellement des en-têtes GTS à une notification WIS2

## Introduction

Les Membres de l'OMM souhaitant arrêter la transmission de leurs données sur le GTS pendant la phase de transition vers WIS2 devront ajouter des en-têtes GTS à leurs notifications WIS2. Ces en-têtes permettent à la passerelle WIS2 vers GTS de transmettre les données au réseau GTS.

Cela permet aux Membres ayant migré vers l'utilisation d'un nœud WIS2 pour la publication des données de désactiver leur système MSS tout en garantissant que leurs données restent disponibles pour les Membres n'ayant pas encore migré vers WIS2.

La propriété GTS dans le Message de Notification WIS2 doit être ajoutée comme une propriété supplémentaire au Message de Notification WIS2. La propriété GTS est un objet JSON qui contient les en-têtes GTS nécessaires pour que les données soient transmises au réseau GTS.

```json
{
  "gts": {
    "ttaaii": "FTAE31",
    "cccc": "VTBB"
  }
}
```

Dans wis2box, vous pouvez ajouter cela automatiquement aux Notifications WIS2 en fournissant un fichier supplémentaire nommé `gts_headers_mapping.csv` contenant les informations nécessaires pour associer les en-têtes GTS aux noms de fichiers entrants.

Ce fichier doit être placé dans le répertoire défini par `WIS2BOX_HOST_DATADIR` dans votre fichier `wis2box.env` et doit contenir les colonnes suivantes :

- `string_in_filepath` : une chaîne faisant partie du nom de fichier qui sera utilisée pour associer les en-têtes GTS
- `TTAAii` : l'en-tête TTAAii à ajouter à la notification WIS2
- `CCCC` : l'en-tête CCCC à ajouter à la notification WIS2

À partir de wis2box-1.3.0, les éditeurs de données ont deux options pour (facultativement) ajouter des propriétés GTS à leurs notifications :

1. Pour les fichiers téléchargés dans MinIO, préparer un fichier de correspondance nommé "gts_headers_mappings.csv" avec les propriétés requises.

2. Pour les données saisies via le formulaire FM-12 SYNOP dans wis2box-webapp, sélectionner "Ajouter des en-têtes GTS" et fournir les informations manuellement.

## Préparation

Assurez-vous d'avoir un accès SSH à votre VM étudiant et que votre instance wis2box est opérationnelle.

Vérifiez que vous êtes connecté au broker MQTT de votre instance wis2box en utilisant MQTT Explorer. Vous pouvez utiliser les identifiants publics `everyone/everyone` pour vous connecter au broker.

Assurez-vous d'avoir un navigateur web ouvert avec le tableau de bord Grafana de votre instance en accédant à `http://YOUR-HOST:3000`.

## Exercice 1 : Utilisation d'un fichier de correspondance pour les données téléchargées dans MinIO

Le premier exercice montre comment ajouter des en-têtes GTS pour les données téléchargées dans MinIO, en utilisant un fichier de correspondance nommé `gts_headers_mapping.csv`.

### Création de `gts_headers_mapping.csv`

Pour ajouter des en-têtes GTS à vos notifications WIS2, un fichier CSV est nécessaire pour associer les en-têtes GTS aux noms de fichiers entrants.

Le fichier CSV doit être nommé (exactement) `gts_headers_mapping.csv` et placé dans le répertoire défini par `WIS2BOX_HOST_DATADIR` dans votre fichier `wis2box.env`.

Copiez le fichier `exercise-materials/gts-headers-exercises/gts_headers_mapping.csv` dans votre instance wis2box et placez-le dans le répertoire défini par `WIS2BOX_HOST_DATADIR` dans votre fichier `wis2box.env`.

```bash
cp ~/exercise-materials/gts-headers-exercises/gts_headers_mapping.csv ~/wis2box-data
```

### Application des correspondances
    
Après avoir créé le fichier `gts_headers_mapping.csv`, vous devez redémarrer le conteneur wis2box-management pour appliquer les modifications. Vous pouvez le faire en exécutant la commande suivante dans votre VM étudiant :

```bash
docker restart wis2box-management
```

### Intégration des données avec des en-têtes GTS

Copiez le fichier `exercise-materials/gts-headers-exercises/A_SMRO01YRBK171200_C_EDZW_20240717120502.txt` dans le répertoire défini par `WIS2BOX_HOST_DATADIR` dans votre fichier `wis2box.env` :

```bash
cp ~/exercise-materials/gts-headers-exercises/A_SMRO01YRBK171200_C_EDZW_20240717120502.txt ~/wis2box-data
```

Ensuite, connectez-vous au conteneur **wis2box-management** :

```bash
cd ~/wis2box
python3 wis2box-ctl.py login
```

Depuis la ligne de commande wis2box, vous pouvez intégrer le fichier de données exemple `A_SMRO01YRBK171200_C_EDZW_20240717120502.txt` dans un ensemble de données spécifique comme suit :

```bash
wis2box data ingest -p /data/wis2box/A_SMRO01YRBK171200_C_EDZW_20240717120502.txt --metadata-id urn:wmo:md:not-my-centre:core.surface-based-observations.synop
```

Assurez-vous de remplacer l'option `metadata-id` par l'identifiant correct de votre ensemble de données.

Vérifiez le tableau de bord Grafana pour voir si les données ont été intégrées correctement. Si vous voyez des AVERTISSEMENTS ou des ERREURS, essayez de les corriger et répétez l'exercice avec la commande `wis2box data ingest`.

### Visualisation des en-têtes GTS dans la Notification WIS2

Accédez à MQTT Explorer et vérifiez le Message de Notification WIS2 pour les données que vous venez d'intégrer.

Le Message de Notification WIS2 doit contenir les en-têtes GTS que vous avez fournis dans le fichier `gts_headers_mapping.csv`.

## Exercice 2 : Utilisation du formulaire FM-12 SYNOP

Lors de l'utilisation du formulaire FM-12 SYNOP dans wis2box-webapp, vous pouvez ajouter manuellement des en-têtes GTS à vos notifications WIS2 en sélectionnant l'option "Ajouter des en-têtes GTS" et en fournissant les informations requises.

Pour cet exercice, vous pouvez utiliser les données d'exemple ci-dessous ou fournir les vôtres :

Message FM-12 SYNOP :

```{copy}
AAXX 03094
64400 42460 71004 10285 20245 30113 40133 8493/
    333 59005 83813 81930 87363 94966 95836=
```

En-têtes GTS : TTAAii=`ISIH01` et CCCC=`FCBB`

!!! note
    Le plugin synop2bufr dans wis2box convertit les messages FM-12 SYNOP en BUFR, donc le TTAAii doit commencer par `IS` :

    - I = Données d'observation (codées en binaire) – BUFR
    - S = Surface/niveau de la mer

### Soumettre manuellement le formulaire FM-12 SYNOP avec des en-têtes GTS

Accédez au formulaire FM-12 SYNOP dans wis2box-webapp et remplissez le formulaire avec les données d'exemple ci-dessus ou vos propres données.

Assurez-vous de sélectionner l'option "Ajouter des en-têtes GTS" et de fournir les informations requises pour les en-têtes GTS :

<img alt="fm-12-synop-form-gts-headers.png" src="/../assets/img/fm-12-synop-form-gts-headers.png" width="800">

Fournissez le jeton d'authentification requis et soumettez le formulaire.

Vous verrez probablement un message d'erreur car cette station n'est pas dans votre liste de stations. Vous devrez ajouter la station "0-20000-0-64400" à votre liste de stations pour que les données soient converties et publiées avec succès.

### Visualisation des en-têtes GTS dans la Notification WIS2

Accédez à MQTT Explorer et vérifiez le Message de Notification WIS2 pour les données que vous venez d'intégrer afin de voir si les en-têtes GTS sont inclus dans la notification.

## Conclusion

!!! success "Félicitations !"
    Au cours de cette session pratique, vous avez appris à :
      - ajouter des en-têtes GTS à vos notifications WIS2
      - vérifier que les en-têtes GTS sont disponibles via votre installation wis2box
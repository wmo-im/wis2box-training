---
title: Ajout d'en-têtes GTS aux notifications WIS2
---

# Ajout d'en-têtes GTS aux notifications WIS2

!!! abstract "Résultats d'apprentissage"

    À la fin de cette session pratique, vous serez capable de :
    
    - configurer une correspondance entre le nom de fichier et les en-têtes GTS
    - ingérer des données avec un nom de fichier qui correspond aux en-têtes GTS
    - visualiser les en-têtes GTS dans les notifications WIS2

## Introduction

Les membres de l'OMM souhaitant arrêter leur transmission de données sur le GTS pendant la phase de transition vers WIS2 devront ajouter des en-têtes GTS à leurs notifications WIS2. Ces en-têtes permettent au passerelle WIS2 vers GTS de transférer les données vers le réseau GTS.

Cela permet aux membres ayant migré vers l'utilisation d'un nœud WIS2 pour la publication de données de désactiver leur système MSS et de s'assurer que leurs données sont toujours disponibles pour les membres n'ayant pas encore migré vers WIS2.

La propriété GTS dans le Message de Notification WIS2 doit être ajoutée comme une propriété supplémentaire au Message de Notification WIS2. La propriété GTS est un objet JSON qui contient les en-têtes GTS nécessaires pour que les données soient transférées vers le réseau GTS.

```json
{
  "gts": {
    "ttaaii": "FTAE31",
    "cccc": "VTBB"
  }
}
```

Au sein de wis2box, vous pouvez ajouter cela automatiquement aux Notifications WIS2 en fournissant un fichier supplémentaire nommé `gts_headers_mapping.csv` qui contient les informations nécessaires pour mapper les en-têtes GTS aux noms de fichiers entrants.

Ce fichier doit être placé dans le répertoire défini par `WIS2BOX_HOST_DATADIR` dans votre `wis2box.env` et doit avoir les colonnes suivantes :

- `string_in_filepath` : une chaîne qui fait partie du nom de fichier qui sera utilisée pour correspondre aux en-têtes GTS
- `TTAAii` : l'en-tête TTAAii à ajouter à la notification WIS2
- `CCCC` : l'en-tête CCCC à ajouter à la notification WIS2

## Préparation

Assurez-vous d'avoir un accès SSH à votre VM étudiante et que votre instance wis2box est opérationnelle.

Assurez-vous que vous êtes connecté au broker MQTT de votre instance wis2box en utilisant MQTT Explorer. Vous pouvez utiliser les identifiants publics `everyone/everyone` pour vous connecter au broker.

Assurez-vous d'avoir un navigateur web ouvert avec le tableau de bord Grafana pour votre instance en allant à `http://YOUR-HOST:3000`

## Création de `gts_headers_mapping.csv`

Pour ajouter des en-têtes GTS à vos notifications WIS2, un fichier CSV est requis qui mappe les en-têtes GTS aux noms de fichiers entrants.

Le fichier CSV doit être nommé (exactement) `gts_headers_mapping.csv` et doit être placé dans le répertoire défini par `WIS2BOX_HOST_DATADIR` dans votre `wis2box.env`. 

## Fourniture d'un fichier `gts_headers_mapping.csv`
    
Copiez le fichier `exercise-materials/gts-headers-exercises/gts_headers_mapping.csv` sur votre instance wis2box et placez-le dans le répertoire défini par `WIS2BOX_HOST_DATADIR` dans votre `wis2box.env`.

```bash
cp ~/exercise-materials/gts-headers-exercises/gts_headers_mapping.csv ~/wis2box-data
```

Ensuite, redémarrez le conteneur wis2box-management pour appliquer les modifications :

```bash
docker restart wis2box-management
```

## Ingestion de données avec en-têtes GTS

Copiez le fichier `exercise-materials/gts-headers-exercises/A_SMRO01YRBK171200_C_EDZW_20240717120502.txt` dans le répertoire défini par `WIS2BOX_HOST_DATADIR` dans votre `wis2box.env` :

```bash
cp ~/exercise-materials/gts-headers-exercises/A_SMRO01YRBK171200_C_EDZW_20240717120502.txt ~/wis2box-data
```

Ensuite, connectez-vous au conteneur **wis2box-management** :

```bash
cd ~/wis2box
python3 wis2box-ctl.py login
```

Depuis la ligne de commande wis2box, nous pouvons ingérer le fichier de données d'exemple `A_SMRO01YRBK171200_C_EDZW_20240717120502.txt` dans un ensemble de données spécifique comme suit :

```bash
wis2box data ingest -p /data/wis2box/A_SMRO01YRBK171200_C_EDZW_20240717120502.txt --metadata-id urn:wmo:md:not-my-centre:core.surface-based-observations.synop
```

Assurez-vous de remplacer l'option `metadata-id` par l'identifiant correct pour votre ensemble de données.

Vérifiez le tableau de bord Grafana pour voir si les données ont été correctement ingérées. Si vous voyez des AVERTISSEMENTS ou des ERREURS, essayez de les résoudre et répétez la commande `wis2box data ingest`.

## Visualisation des en-têtes GTS dans la Notification WIS2

Allez à MQTT Explorer et vérifiez le Message de Notification WIS2 pour les données que vous venez d'ingérer.

Le Message de Notification WIS2 devrait contenir les en-têtes GTS que vous avez fournis dans le fichier `gts_headers_mapping.csv`.

## Conclusion

!!! success "Félicitations !"
    Dans cette session pratique, vous avez appris à :
      - ajouter des en-têtes GTS à vos notifications WIS2
      - vérifier que les en-têtes GTS sont disponibles via votre installation wis2box
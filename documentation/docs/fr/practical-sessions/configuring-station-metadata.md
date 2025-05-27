---
title: Configuration des métadonnées des stations
---

# Configuration des métadonnées des stations

!!! abstract "Résultats d'apprentissage"

    À la fin de cette session pratique, vous serez capable de :

    - créer un jeton d'autorisation pour l'endpoint `collections/stations`
    - ajouter des métadonnées de station à wis2box
    - mettre à jour/supprimer des métadonnées de station en utilisant le **wis2box-webapp**

## Introduction

Pour partager des données à l'international entre les membres de l'OMM, il est important de comprendre les stations qui produisent les données. Le Système mondial d'observation intégré de l'OMM (WIGOS) fournit un cadre pour l'intégration des systèmes d'observation et des systèmes de gestion des données. L'**Identifiant de Station WIGOS (WSI)** est utilisé comme référence unique de la station qui a produit un ensemble spécifique de données d'observation.

wis2box possède une collection de métadonnées de station qui est utilisée pour décrire les stations produisant les données d'observation et doit être récupérée depuis **OSCAR/Surface**. Les métadonnées de station dans wis2box sont utilisées par les outils de transformation BUFR pour vérifier que les données entrantes contiennent un Identifiant de Station WIGOS (WSI) valide et pour fournir une correspondance entre le WSI et les métadonnées de la station.

## Créer un jeton d'autorisation pour collections/stations

Pour éditer des stations via le **wis2box-webapp**, vous devrez d'abord créer un jeton d'autorisation.

Connectez-vous à votre VM étudiant et assurez-vous que vous êtes dans le répertoire `wis2box` :

```bash
cd ~/wis2box
```

Ensuite, connectez-vous au conteneur **wis2box-management** avec la commande suivante :

```bash
python3 wis2box-ctl.py login
```

Dans le conteneur **wis2box-management**, vous pouvez créer un jeton d'autorisation pour un endpoint spécifique en utilisant la commande : `wis2box auth add-token --path <my-endpoint>`.

Par exemple, pour utiliser un jeton généré automatiquement aléatoire pour l'endpoint `collections/stations` :

```{.copy}
wis2box auth add-token --path collections/stations
```	

Le résultat sera le suivant :

```{.copy}
Continue with token: 7ca20386a131f0de384e6ffa288eb1ae385364b3694e47e3b451598c82e899d1 [y/N]? y
Token successfully created
```

Ou, si vous souhaitez définir votre propre jeton pour l'endpoint `collections/stations`, vous pouvez utiliser l'exemple suivant :

```{.copy}
wis2box auth add-token --path collections/stations DataIsMagic
```

Résultat :
    
```{.copy}
Continue with token: DataIsMagic [y/N]? y
Token successfully created
```

Veuillez créer un jeton d'autorisation pour l'endpoint `collections/stations` en utilisant les instructions ci-dessus.

## Ajouter des métadonnées de station en utilisant le **wis2box-webapp**

Le **wis2box-webapp** fournit une interface utilisateur graphique pour éditer les métadonnées des stations.

Ouvrez le **wis2box-webapp** dans votre navigateur en naviguant vers `http://YOUR-HOST/wis2box-webapp`, et sélectionnez les stations :

<img alt="wis2box-webapp-select-stations" src="/../assets/img/wis2box-webapp-select-stations.png" width="250">

Lorsque vous cliquez sur 'ajouter une nouvelle station', il vous est demandé de fournir l'identifiant de station WIGOS pour la station que vous souhaitez ajouter :

<img alt="wis2box-webapp-import-station-from-oscar" src="/../assets/img/wis2box-webapp-import-station-from-oscar.png" width="800">

!!! note "Ajouter des métadonnées de station pour 3 stations ou plus"
    Veuillez ajouter trois stations ou plus à la collection de métadonnées de station de votre wis2box. 
      
    Veuillez utiliser des stations de votre pays si possible, surtout si vous avez apporté vos propres données.
      
    Si votre pays n'a pas de stations dans OSCAR/Surface, vous pouvez utiliser les stations suivantes pour cet exercice :

      - 0-20000-0-91334
      - 0-20000-0-96323 (notez l'absence d'élévation de la station dans OSCAR)
      - 0-20000-0-96749 (notez l'absence d'élévation de la station dans OSCAR)

Lorsque vous cliquez sur rechercher, les données de la station sont récupérées depuis OSCAR/Surface, veuillez noter que cela peut prendre quelques secondes.

Examinez les données renvoyées par OSCAR/Surface et ajoutez les données manquantes si nécessaire. Sélectionnez un sujet pour la station et fournissez votre jeton d'autorisation pour l'endpoint `collections/stations` et cliquez sur 'enregistrer' :

<img alt="wis2box-webapp-create-station-save" src="/../assets/img/wis2box-webapp-create-station-save.png" width="800">

<img alt="wis2box-webapp-create-station-success" src="/../assets/img/wis2box-webapp-create-station-success.png" width="500">

Revenez à la liste des stations et vous verrez la station que vous avez ajoutée :

<img alt="wis2box-webapp-stations-with-one-station" src="/../assets/img/wis2box-webapp-stations-with-one-station.png" width="800">

Répétez ce processus jusqu'à ce que vous ayez configuré au moins 3 stations.

!!! tip "Dérivation des informations d'élévation manquantes"

    Si l'élévation de votre station est manquante, il existe des services en ligne pour aider à rechercher l'élévation en utilisant des données d'élévation ouvertes. Un tel exemple est l'[API Open Topo Data](https://www.opentopodata.org).

    Par exemple, pour obtenir l'élévation à la latitude -6.15558 et à la longitude 106.84204, vous pouvez copier-coller l'URL suivante dans un nouvel onglet de navigateur :

    ```{.copy}
    https://api.opentopodata.org/v1/aster30m?locations=-6.15558,106.84204
    ```

    Résultat :

    ```{.copy}
    {
      "results": [
        {
          "dataset": "aster30m", 
          "elevation": 7.0, 
          "location": {
            "lat": -6.15558, 
            "lng": 106.84204
          }
        }
      ], 
      "status": "OK"
    }
    ```

## Réviser vos métadonnées de station

Les métadonnées de station sont stockées dans le backend de wis2box et sont disponibles via le **wis2box-api**. 

Si vous ouvrez un navigateur et naviguez vers `http://YOUR-HOST/oapi/collections/stations/items` vous verrez les métadonnées de station que vous avez ajoutées :

<img alt="wis2box-api-stations" src="/../assets/img/wis2box-api-stations.png" width="800">

!!! note "Révisez vos métadonnées de station"

    Vérifiez que les stations que vous avez ajoutées sont associées à votre ensemble de données en visitant `http://YOUR-HOST/oapi/collections/stations/items` dans votre navigateur.

Vous avez également la possibilité de voir/mettre à jour/supprimer la station dans le **wis2box-webapp**. Notez que vous devez fournir votre jeton d'autorisation pour l'endpoint `collections/stations` pour mettre à jour/supprimer la station.

!!! note "Mettre à jour/supprimer des métadonnées de station"

    Essayez de voir si vous pouvez mettre à jour/supprimer les métadonnées de station pour l'une des stations que vous avez ajoutées en utilisant le **wis2box-webapp**.

## Téléchargement en masse des métadonnées de station

Notez que wis2box a également la capacité de charger en masse des métadonnées de station à partir d'un fichier CSV en utilisant la ligne de commande dans le conteneur **wis2box-management**.

```bash
python3 wis2box-ctl.py login
wis2box metadata station publish-collection -p /data/wis2box/metadata/station/station_list.csv -th origin/a/wis2/centre-id/weather/surface-based-observations/synop
```

Cela vous permet de télécharger un grand nombre de stations à la fois et de les associer à un sujet spécifique.

Vous pouvez créer le fichier CSV en utilisant Excel ou un éditeur de texte, puis le télécharger dans wis2box-host-datadir pour le rendre disponible au conteneur **wis2box-management** dans le répertoire `/data/wis2box/`.

Après avoir effectué un téléchargement en masse de stations, il est recommandé de réviser les stations dans le **wis2box-webapp** pour vous assurer que les données ont été téléchargées correctement.

Consultez la [documentation officielle de wis2box](https://docs.wis2box.wis.wmo.int) pour plus d'informations sur comment utiliser cette fonctionnalité.

## Conclusion

!!! success "Félicitations !"
    Dans cette session pratique, vous avez appris à :

    - créer un jeton d'autorisation pour l'endpoint `collections/stations` à utiliser avec le **wis2box-webapp**
    - ajouter des métadonnées de station à wis2box en utilisant le **wis2box-webapp**
    - voir/mettre à jour/supprimer des métadonnées de station en utilisant le **wis2box-webapp**
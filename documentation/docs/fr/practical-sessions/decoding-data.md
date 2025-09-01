---
title: Décodage des données à partir des formats binaires de l'OMM
---

# Décodage des données à partir des formats binaires de l'OMM

!!! abstract "Objectifs d'apprentissage !"

    À la fin de cette session pratique, vous serez capable de :

    - exécuter un conteneur Docker pour l'image "demo-decode-eccodes-jupyter"
    - exécuter les notebooks Jupyter d'exemple pour décoder les données aux formats GRIB2, NetCDF et BUFR
    - connaître d'autres outils pour décoder et visualiser les formats binaires de l'OMM

## Introduction

Les formats binaires de l'OMM tels que BUFR et GRIB sont largement utilisés dans la communauté météorologique pour l'échange de données d'observation et de modélisation. Ils nécessitent des outils spécialisés pour décoder et visualiser les données.

Après avoir téléchargé des données depuis un WIS2, vous devrez souvent les décoder pour pouvoir les exploiter.

Diverses bibliothèques de code sont disponibles pour écrire des scripts ou des programmes permettant de décoder les formats binaires de l'OMM. Il existe également des outils offrant une interface utilisateur pour décoder et visualiser les données sans avoir besoin d'écrire du code.

Dans cette session pratique, nous allons démontrer comment décoder 3 types de données différents à l'aide d'un notebook Jupyter :

- GRIB2 contenant des données pour une prévision d'ensemble globale réalisée par le système GRAPES (Global Regional Assimilation PrEdiction System) du CMA
- BUFR contenant des données de trajectoire de cyclone tropical issues du système de prévision d'ensemble de l'ECMWF
- NetCDF contenant des données sur les anomalies de température mensuelles

## Décodage des données téléchargées dans un notebook Jupyter

Pour démontrer comment vous pouvez décoder les données téléchargées, nous allons démarrer un nouveau conteneur en utilisant l'image 'decode-bufr-jupyter'.

Ce conteneur démarrera un serveur de notebooks Jupyter sur votre instance, qui inclut la bibliothèque "ecCodes" que vous pouvez utiliser pour décoder les données BUFR.

Nous utiliserons les notebooks d'exemple inclus dans `~/exercise-materials/notebook-examples` pour décoder les données téléchargées des trajectoires de cyclones.

Pour démarrer le conteneur, utilisez la commande suivante :

```bash
docker run -d --name demo-decode-eccodes-jupyter \
    -v ~/wis2box-data/downloads:/root/downloads \
    -p 8888:8888 \
    -e JUPYTER_TOKEN=dataismagic! \
    ghcr.io/wmo-im/wmo-im/demo-decode-eccodes-jupyter:latest
```

Voici une explication de ce que fait cette commande :

- `docker run -d --name demo-decode-eccodes-jupyter` démarre un nouveau conteneur en mode détaché (`-d`) et le nomme `demo-decode-eccodes-jupyter`.
- `-v ~/wis2box-data/downloads:/root/downloads` monte le répertoire `~/wis2box-data/downloads` de votre VM dans `/root/downloads` dans le conteneur. C'est là que sont stockées les données téléchargées depuis WIS2.
- `-p 8888:8888` mappe le port 8888 de votre VM au port 8888 dans le conteneur. Cela rend le serveur de notebooks Jupyter accessible depuis votre navigateur web à l'adresse `http://YOUR-HOST:8888`.
- `-e JUPYTER_TOKEN=dataismagic!` définit le jeton requis pour accéder au serveur de notebooks Jupyter. Vous devrez fournir ce jeton lorsque vous accéderez au serveur depuis votre navigateur web.
- `ghrc.io/wmo-im/demo-decode-eccodes-jupyter:latest` spécifie l'image utilisée par le conteneur, qui inclut les notebooks Jupyter d'exemple utilisés dans les exercices suivants.

!!! note "À propos de l'image demo-decode-eccodes-jupyter"

    L'image `demo-decode-eccodes-jupyter` a été développée pour cette formation. Elle utilise une image de base incluant la bibliothèque ecCodes et ajoute un serveur de notebooks Jupyter ainsi qu'un ensemble de bibliothèques Python pour l'analyse et la visualisation des données.

    Vous pouvez trouver le code source de cette image, y compris les notebooks d'exemple, sur [wmo-im/demo-decode-eccodes-jupyter](https://github.com/wmo-im/demo-decode-eccodes-jupyter).
    
Une fois le conteneur démarré, vous pouvez accéder au serveur de notebooks Jupyter sur votre VM étudiante en naviguant à l'adresse `http://YOUR-HOST:8888` dans votre navigateur web.

Vous verrez un écran vous demandant d'entrer un "Mot de passe ou jeton".

Fournissez le jeton `dataismagic!` pour vous connecter au serveur de notebooks Jupyter (sauf si vous avez utilisé un jeton différent dans la commande ci-dessus).

Après vous être connecté, vous devriez voir l'écran suivant listant les répertoires dans le conteneur :

![Accueil des notebooks Jupyter](../assets/img/jupyter-files-screen1.png)

Double-cliquez sur le répertoire `example-notebooks` pour l'ouvrir.

Vous devriez voir l'écran suivant listant les notebooks d'exemple :

![Notebooks d'exemple Jupyter](../assets/img/jupyter-files-screen2.png)

Vous pouvez maintenant ouvrir les notebooks d'exemple pour décoder les données téléchargées.

### Exemple de décodage GRIB2 : Données GEPS du CMA GRAPES

Ouvrez le fichier `GRIB2_CMA_global_ensemble_prediction.ipynb` dans le répertoire `example-notebooks` :

![Prédiction d'ensemble globale GRIB2 dans Jupyter](../assets/img/jupyter-grib2-global-ensemble-prediction.png)

Lisez les instructions dans le notebook et exécutez les cellules pour décoder les données téléchargées pour la prévision d'ensemble globale. Exécutez chaque cellule en cliquant dessus, puis sur le bouton d'exécution dans la barre d'outils ou en appuyant sur `Shift+Enter`.

À la fin, vous devriez voir une carte affichant la pression réduite au niveau moyen de la mer (MSL) :

![Température de la prévision d'ensemble globale](../assets/img/grib2-global-ensemble-prediction-map.png)

!!! question 

    Le résultat affiche la température à 2 mètres au-dessus du sol. Comment mettriez-vous à jour le notebook pour afficher la vitesse du vent à 10 mètres au-dessus du sol ?

??? success "Cliquez pour révéler la réponse"

    Pour mettre à jour le notebook, faites ce qui suit.

### Exemple de décodage BUFR : Trajectoires de cyclones tropicaux

Ouvrez le fichier `BUFR_tropical_cyclone_track.ipynb` dans le répertoire `example-notebooks` :

![Trajectoire de cyclone tropical dans Jupyter](../assets/img/jupyter-tropical-cyclone-track.png)

Lisez les instructions dans le notebook et exécutez les cellules pour décoder les données téléchargées des trajectoires de cyclones tropicaux. Exécutez chaque cellule en cliquant dessus, puis sur le bouton d'exécution dans la barre d'outils ou en appuyant sur `Shift+Enter`.

À la fin, vous devriez voir un graphique de la probabilité de trajectoire pour les cyclones tropicaux :

![Trajectoires de cyclones tropicaux](../assets/img/tropical-cyclone-track-map.png)

!!! question 

    Le résultat affiche la probabilité prévue de trajectoire de tempête tropicale dans un rayon de 200 km. Comment mettriez-vous à jour le notebook pour afficher la probabilité prévue dans un rayon de 300 km ?

??? success "Cliquez pour révéler la réponse"

    Pour mettre à jour le notebook afin d'afficher la probabilité prévue de trajectoire de tempête tropicale dans une distance différente, vous pouvez mettre à jour la variable `distance_threshold` dans le bloc de code qui calcule la probabilité de trajectoire.

    Pour afficher la probabilité prévue dans un rayon de 300 km :

    ```python
    # définir le seuil de distance (en mètres)
    distance_threshold = 300000  # 300 km en mètres
    ```

    Ensuite, réexécutez les cellules du notebook pour voir le graphique mis à jour.

!!! note "Décodage des données BUFR"

    L'exercice que vous venez de réaliser fournit un exemple spécifique de la manière dont vous pouvez décoder les données BUFR à l'aide de la bibliothèque ecCodes. Différents types de données peuvent nécessiter des étapes de décodage différentes, et vous devrez peut-être vous référer à la documentation pour le type de données avec lequel vous travaillez.
    
    Pour plus d'informations, veuillez consulter la [documentation ecCodes](https://confluence.ecmwf.int/display/ECC).

### Exemple de décodage NetCDF : Anomalies de température mensuelles

Ouvrez le fichier `NetCDF4_monthly_temperature_anomaly.ipynb` dans le répertoire `example-notebooks` :

![Anomalies de température mensuelles dans Jupyter](../assets/img/jupyter-netcdf4-monthly-temperature-anomalies.png)

Lisez les instructions dans le notebook et exécutez les cellules pour décoder les données téléchargées des anomalies de température mensuelles. Exécutez chaque cellule en cliquant dessus, puis sur le bouton d'exécution dans la barre d'outils ou en appuyant sur `Shift+Enter`.

À la fin, vous devriez voir une carte des anomalies de température :

![Carte des anomalies de température mensuelles](../assets/img/netcdf4-monthly-temperature-anomalies-map.png)

!!! note "Décodage des données NetCDF"

    NetCDF est un format flexible qui, dans cet exemple, rapporte les valeurs pour la variable 'anomaly' selon les dimensions 'lat', 'lon'. Différents ensembles de données NetCDF peuvent utiliser des noms de variables et des dimensions différents.

## Utilisation d'autres outils pour visualiser et décoder les formats binaires de l'OMM

Les notebooks d'exemple ont démontré comment vous pouvez décoder les formats binaires couramment utilisés de l'OMM à l'aide de code Python.

Vous pouvez également utiliser d'autres outils pour décoder et visualiser les formats binaires de l'OMM sans avoir besoin d'écrire du code, tels que :

- [Panoply](https://www.giss.nasa.gov/tools/panoply/) - Une application multiplateforme qui trace des tableaux géo-référencés et autres à partir de fichiers NetCDF, HDF, GRIB et autres ensembles de données.
- [ECMWF Metview](https://confluence.ecmwf.int/display/METV/Metview) - Une application météorologique pour l'analyse et la visualisation des données, qui prend en charge les formats GRIB et BUFR.
- [Integrated Data Viewer (IDV)](https://www.unidata.ucar.edu/software/idv/) - Un logiciel libre basé sur Java pour l'analyse et la visualisation des données géoscientifiques, incluant la prise en charge des formats GRIB et NetCDF.

## Conclusion

!!! success "Félicitations !"

    Au cours de cette session pratique, vous avez appris à :

    - exécuter un conteneur Docker pour l'image "demo-decode-eccodes-jupyter"
    - exécuter les notebooks Jupyter d'exemple pour décoder les données aux formats GRIB2, NetCDF et BUFR
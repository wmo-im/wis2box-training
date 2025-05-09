---
title: Téléchargement et décodage des données depuis WIS2
---

# Téléchargement et décodage des données depuis WIS2

!!! abstract "Résultats d'apprentissage !"

    À la fin de cette session pratique, vous serez capable de :

    - utiliser le "wis2downloader" pour vous abonner aux notifications de données WIS2 et télécharger des données sur votre système local
    - visualiser l'état des téléchargements dans le tableau de bord Grafana
    - décoder certaines données téléchargées en utilisant le conteneur "decode-bufr-jupyter"

## Introduction

Dans cette session, vous apprendrez à configurer un abonnement à un Broker WIS2 et à télécharger automatiquement des données sur votre système local en utilisant le service "wis2downloader" inclus dans wis2box.

!!! note "À propos de wis2downloader"
     
     Le wis2downloader est également disponible en tant que service autonome qui peut être exécuté sur un système différent de celui qui publie les notifications WIS2. Voir [wis2downloader](https://pypi.org/project/wis2downloader/) pour plus d'informations sur l'utilisation du wis2downloader en tant que service autonome.

     Si vous souhaitez développer votre propre service pour vous abonner aux notifications WIS2 et télécharger des données, vous pouvez utiliser le [code source de wis2downloader](https://github.com/World-Meteorological-Organization/wis2downloader) comme référence.

!!! Autres outils pour accéder aux données WIS2

    Les outils suivants peuvent également être utilisés pour découvrir et accéder aux données de WIS2 :

    - [pywiscat](https://github.com/wmo-im/pywiscat) offre des capacités de recherche au-dessus du Catalogue Global de Découverte WIS2 pour soutenir le reporting et l'analyse du Catalogue WIS2 et de ses métadonnées de découverte associées
    - [pywis-pubsub](https://github.com/World-Meteorological-Organization/pywis-pubsub) offre des capacités d'abonnement et de téléchargement des données de l'OMM depuis les services d'infrastructure WIS2

## Préparation

Avant de commencer, veuillez vous connecter à votre VM étudiant et assurez-vous que votre instance wis2box est opérationnelle.

## Visualisation du tableau de bord wis2downloader dans Grafana

Ouvrez un navigateur web et naviguez vers le tableau de bord Grafana pour votre instance wis2box en allant sur `http://YOUR-HOST:3000`.

Cliquez sur tableaux de bord dans le menu de gauche, puis sélectionnez le **tableau de bord wis2downloader**.

Vous devriez voir le tableau de bord suivant :

![Tableau de bord wis2downloader](../assets/img/wis2downloader-dashboard.png)

Ce tableau de bord est basé sur les métriques publiées par le service wis2downloader et vous montrera l'état des téléchargements en cours.

Dans le coin supérieur gauche, vous pouvez voir les abonnements qui sont actuellement actifs.

Gardez ce tableau de bord ouvert car vous l'utiliserez pour surveiller la progression du téléchargement dans le prochain exercice.

## Révision de la configuration de wis2downloader

Le service wis2downloader démarré par la pile wis2box peut être configuré à l'aide des variables d'environnement définies dans votre fichier wis2box.env.

Les variables d'environnement suivantes sont utilisées par le wis2downloader :

    - DOWNLOAD_BROKER_HOST : Le nom d'hôte du broker MQTT auquel se connecter. Par défaut à globalbroker.meteo.fr
    - DOWNLOAD_BROKER_PORT : Le port du broker MQTT auquel se connecter. Par défaut à 443 (HTTPS pour les websockets)
    - DOWNLOAD_BROKER_USERNAME : Le nom d'utilisateur à utiliser pour se connecter au broker MQTT. Par défaut à everyone
    - DOWNLOAD_BROKER_PASSWORD : Le mot de passe à utiliser pour se connecter au broker MQTT. Par défaut à everyone
    - DOWNLOAD_BROKER_TRANSPORT : websockets ou tcp, le mécanisme de transport à utiliser pour se connecter au broker MQTT. Par défaut à websockets,
    - DOWNLOAD_RETENTION_PERIOD_HOURS : La période de rétention en heures pour les données téléchargées. Par défaut à 24
    - DOWNLOAD_WORKERS : Le nombre de travailleurs de téléchargement à utiliser. Par défaut à 8. Détermine le nombre de téléchargements parallèles.
    - DOWNLOAD_MIN_FREE_SPACE_GB : L'espace libre minimum en GB à conserver sur le volume hébergeant les téléchargements. Par défaut à 1.

Pour réviser la configuration actuelle du wis2downloader, vous pouvez utiliser la commande suivante :

```bash
cat ~/wis2box/wis2box.env | grep DOWNLOAD
```

!!! question "Révisez la configuration du wis2downloader"
    
    Quel est le broker MQTT par défaut auquel le wis2downloader se connecte ?

    Quelle est la période de rétention par défaut pour les données téléchargées ?

??? success "Cliquez pour révéler la réponse"

    Le broker MQTT par défaut auquel le wis2downloader se connecte est `globalbroker.meteo.fr`.

    La période de rétention par défaut pour les données téléchargées est de 24 heures.

!!! note "Mise à jour de la configuration du wis2downloader"

    Pour mettre à jour la configuration du wis2downloader, vous pouvez éditer le fichier wis2box.env. Pour appliquer les modifications, vous pouvez relancer la commande de démarrage pour la pile wis2box :

    ```bash
    python3 wis2box-ctl.py start
    ```

    Et vous verrez le service wis2downloader redémarrer avec la nouvelle configuration.

Vous pouvez conserver la configuration par défaut pour cet exercice.

## Ajout d'abonnements au wis2downloader

À l'intérieur du conteneur **wis2downloader**, vous pouvez utiliser la ligne de commande pour lister, ajouter et supprimer des abonnements.

Pour vous connecter au conteneur **wis2downloader**, utilisez la commande suivante :

```bash
python3 wis2box-ctl.py login wis2downloader
```

Ensuite, utilisez la commande suivante pour lister les abonnements actuellement actifs :

```bash
wis2downloader list-subscriptions
```

Cette commande retourne une liste vide puisqu'aucun abonnement n'est actuellement actif.

Pour cet exercice, nous nous abonnerons au sujet suivant `cache/a/wis2/de-dwd-gts-to-wis2/#`, pour s'abonner aux données publiées par la passerelle GTS-to-WIS2 hébergée par DWD et télécharger les notifications depuis le Global Cache.

Pour ajouter cet abonnement, utilisez la commande suivante :

```bash
wis2downloader add-subscription --topic cache/a/wis2/de-dwd-gts-to-wis2/#
```

Ensuite, quittez le conteneur **wis2downloader** en tapant `exit` :

```bash
exit
```

Vérifiez le tableau de bord wis2downloader dans Grafana pour voir le nouvel abonnement ajouté. Attendez quelques minutes et vous devriez voir les premiers téléchargements commencer. Passez à l'exercice suivant une fois que vous avez confirmé que les téléchargements ont commencé.

## Visualisation des données téléchargées

Le service wis2downloader dans la pile wis2box télécharge les données dans le répertoire 'downloads' dans le répertoire que vous avez défini comme WIS2BOX_HOST_DATADIR dans votre fichier wis2box.env. Pour visualiser le contenu du répertoire des téléchargements, vous pouvez utiliser la commande suivante :

```bash
ls -R ~/wis2box-data/downloads
```

Notez que les données téléchargées sont stockées dans des répertoires nommés d'après le sujet sur lequel la notification WIS2 a été publiée.

## Suppression des abonnements du wis2downloader

Ensuite, reconnectez-vous au conteneur wis2downloader :

```bash
python3 wis2box-ctl.py login wis2downloader
```

et supprimez l'abonnement que vous avez fait du wis2downloader, en utilisant la commande suivante :

```bash
wis2downloader remove-subscription --topic cache/a/wis2/de-dwd-gts-to-wis2/#
```

Et quittez le conteneur wis2downloader en tapant `exit` :
    
```bash
exit
```

Vérifiez le tableau de bord wis2downloader dans Grafana pour voir l'abonnement supprimé. Vous devriez voir les téléchargements s'arrêter.

## Télécharger et décoder des données pour une trajectoire de cyclone tropical

Dans cet exercice, vous vous abonnerez au Broker de Formation WIS2 qui publie des données d'exemple à des fins de formation. Vous configurerez un abonnement pour télécharger des données pour une trajectoire de cyclone tropical. Vous décoderez ensuite les données téléchargées en utilisant le conteneur "decode-bufr-jupyter".

### Abonnez-vous au wis2training-broker et configurez un nouvel abonnement

Cela montre comment s'abonner à un broker qui n'est pas le broker par défaut et vous permettra de télécharger certaines données publiées depuis le Broker de Formation WIS2.

Éditez le fichier wis2box.env et changez le DOWNLOAD_BROKER_HOST en `wis2training-broker.wis2dev.io`, changez DOWNLOAD_BROKER_PORT en `1883` et changez DOWNLOAD_BROKER_TRANSPORT en `tcp` :

```copy
# paramètres du téléchargeur
DOWNLOAD_BROKER_HOST=wis2training-broker.wis2dev.io
DOWNLOAD_BROKER_PORT=1883
DOWNLOAD_BROKER_USERNAME=everyone
DOWNLOAD_BROKER_PASSWORD=everyone
# mécanisme de transport de téléchargement (tcp ou websockets)
DOWNLOAD_BROKER_TRANSPORT=tcp
```

Ensuite, exécutez à nouveau la commande 'start' pour appliquer les modifications :

```bash
python3 wis2box-ctl.py start
```

Vérifiez les journaux du wis2downloader pour voir si la connexion au nouveau broker a été réussie :

```bash
docker logs wis2downloader
```

Vous devriez voir le message de journal suivant :

```copy
...
INFO - Connexion...
INFO - Hôte : wis2training-broker.wis2dev.io, port : 1883
INFO - Connecté avec succès
```

Maintenant, nous allons configurer un nouvel abonnement au sujet pour télécharger les données de trajectoire de cyclone depuis le Broker de Formation WIS2.

Connectez-vous au conteneur **wis2downloader** :

```bash
python3 wis2box-ctl.py login wis2downloader
```

Et exécutez la commande suivante (copiez-collez ceci pour éviter les fautes de frappe) :

```bash
wis2downloader add-subscription --topic origin/a/wis2/int-wis2-training/data/core/weather/prediction/forecast/medium-range/probabilistic/trajectory
```

Quittez le conteneur **wis2downloader** en tapant `exit`.

Attendez jusqu'à ce que vous voyiez les téléchargements commencer dans le tableau de bord wis2downloader dans Grafana.

!!! note "Téléchargement de données depuis le Broker de Formation WIS2"

    Le Broker de Formation WIS2 est un broker de test qui est utilisé à des fins de formation et peut ne pas publier de données tout le temps.

    Pendant les sessions de formation en personne, le formateur local s'assurera que le Broker de Formation WIS2 publiera des données pour que vous puissiez les télécharger.

    Si vous faites cet exercice en dehors d'une session de formation, vous ne verrez peut-être aucune donnée téléchargée.

Vérifiez que les données ont été téléchargées en vérifiant à nouveau les journaux du wis2downloader avec :

```bash
docker logs wis2downloader
```

Vous devriez voir un message de journal similaire au suivant :

```copy
[...] INFO - Message reçu sous le sujet origin/a/wis2/int-wis2-training/data/core/weather/prediction/forecast/medium-range/probabilistic/trajectory
[...] INFO - Téléchargé A_JSXX05ECEP020000_C_ECMP_...
```

### Décodage des données téléchargées

Afin de démontrer comment vous pouvez décoder les données téléchargées, nous allons démarrer un nouveau conteneur en utilisant l'image 'decode-bufr-jupyter'.

Ce conteneur démarrera un serveur de cahiers Jupyter sur votre instance qui inclut la bibliothèque "ecCodes" que vous pouvez utiliser pour décoder les données BUFR.

Nous utiliserons les cahiers d'exemples inclus dans `~/exercise-materials/notebook-examples` pour décoder les données téléchargées pour les trajectoires de cyclones.

Pour démarrer le conteneur, utilisez la commande suivante :

```bash
docker run -d --name decode-bufr-jupyter \
    -v ~/wis2box-data/downloads:/root/downloads \
    -p 8888:8888 \
    -e JUPYTER_TOKEN=dataismagic! \
    mlimper/decode-bufr-jupyter
```

!!! note "À propos du conteneur decode-bufr-jupyter"

    Le conteneur `decode-bufr-jupyter` est un conteneur personnalisé qui inclut la bibliothèque ecCodes et exécute un serveur de cahiers Jupyter. Le conteneur est basé sur une image qui inclut la bibliothèque `ecCodes` pour décoder les données BUFR, ainsi que des bibliothèques pour le traçage et l'analyse de données.

    La commande ci-dessus démarre le conteneur en mode détaché, avec le nom `decode-bufr-jupyter`, le port 8888 est mappé au système hôte et la variable d'environnement `JUPYTER_TOKEN` est définie sur `dataismagic!`.
    
    La commande ci-dessus monte également le répertoire `~/wis2box-data/downloads` sur `/root/downloads` dans le conteneur. Cela garantit que les données téléchargées sont disponibles pour le serveur de cahiers Jupyter.
    
Une fois le conteneur démarré, vous pouvez accéder au serveur de cahiers Jupyter en naviguant sur `http://YOUR-HOST:8888` dans votre navigateur web.

Vous verrez un écran vous demandant d'entrer un "Mot de passe ou jeton".

Fournissez le jeton `dataismagic!` pour vous connecter au serveur de cahiers Jupyter.

Après vous être connecté, vous devriez voir l'écran suivant listant les répertoires dans le conteneur :

![Écran d'accueil du cahier Jupyter](../assets/img/jupyter-files-screen1.png)

Double-cliquez sur le répertoire `example-notebooks` pour l'ouvrir.

Vous devriez voir l'écran suivant listant les cahiers d'exemples, double-cliquez sur le cahier `tropical_cyclone_track.ipynb` pour l'ouvrir :

![Cahiers d'exemples du cahier Jupyter](../assets/img/jupyter-files-screen2.png)

Vous devriez maintenant être dans le cahier Jupyter pour décoder les données de la trajectoire du cyclone tropical :

![Cahier Jupyter trajectoire du cyclone tropical](../assets/img/jupyter-tropical-cyclone-track.png)

Lisez les instructions dans le carnet et exécutez les cellules pour décoder les données téléchargées concernant les trajectoires des cyclones tropicaux. Exécutez chaque cellule en cliquant dessus puis sur le bouton d'exécution dans la barre d'outils ou en appuyant sur `Shift+Enter`.

À la fin, vous devriez voir un graphique de la probabilité d'impact pour les trajectoires des cyclones tropicaux :

![Tropical cyclone tracks](../assets/img/tropical-cyclone-track-map.png)

!!! question 

    Le résultat affiche la probabilité prédite de trajectoire de tempête tropicale à moins de 200 km. Comment mettriez-vous à jour le carnet pour afficher la probabilité prédite de trajectoire de tempête tropicale à moins de 300 km ?

??? success "Cliquez pour révéler la réponse"

    Pour mettre à jour le carnet afin d'afficher la probabilité prédite de trajectoire de tempête tropicale à une distance différente, vous pouvez mettre à jour la variable `distance_threshold` dans le bloc de code qui calcule la probabilité d'impact.

    Pour afficher la probabilité prédite de trajectoire de tempête tropicale à moins de 300 km, 

    ```python
    # set distance threshold (meters)
    distance_threshold = 300000  # 300 km en mètres
    ```

    Ensuite, réexécutez les cellules dans le carnet pour voir le graphique mis à jour.

!!! note "Décodage des données BUFR"

    L'exercice que vous venez de réaliser a fourni un exemple spécifique de la manière dont vous pouvez décoder les données BUFR en utilisant la bibliothèque ecCodes. Différents types de données peuvent nécessiter différentes étapes de décodage et vous devrez peut-être consulter la documentation pour le type de données avec lequel vous travaillez.
    
    Pour plus d'informations, veuillez consulter la [documentation ecCodes](https://confluence.ecmwf.int/display/ECC).



## Conclusion

!!! success "Félicitations !"

    Dans cette session pratique, vous avez appris à :

    - utiliser 'wis2downloader' pour vous abonner à un WIS2 Broker et télécharger des données sur votre système local
    - visualiser le statut des téléchargements dans le tableau de bord Grafana
    - décoder certaines données téléchargées en utilisant le conteneur 'decode-bufr-jupyter'
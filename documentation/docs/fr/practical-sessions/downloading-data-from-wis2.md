---
title: Téléchargement et décodage des données depuis WIS2
---

# Téléchargement et décodage des données depuis WIS2

!!! abstract "Objectifs d'apprentissage !"

    À la fin de cette session pratique, vous serez capable de :

    - utiliser le "wis2downloader" pour vous abonner aux notifications de données WIS2 et télécharger les données sur votre système local
    - visualiser l'état des téléchargements dans le tableau de bord Grafana
    - décoder certaines données téléchargées à l'aide du conteneur "decode-bufr-jupyter"

## Introduction

Dans cette session, vous apprendrez à configurer un abonnement à un WIS2 Broker et à télécharger automatiquement des données sur votre système local en utilisant le service "wis2downloader" inclus dans wis2box.

!!! note "À propos de wis2downloader"
     
     Le wis2downloader est également disponible comme service autonome pouvant être exécuté sur un système différent de celui qui publie les notifications WIS2. Consultez [wis2downloader](https://pypi.org/project/wis2downloader/) pour plus d'informations sur l'utilisation du wis2downloader comme service autonome.

     Si vous souhaitez développer votre propre service pour vous abonner aux notifications WIS2 et télécharger des données, vous pouvez utiliser le [code source de wis2downloader](https://github.com/World-Meteorological-Organization/wis2downloader) comme référence.

!!! Autres outils pour accéder aux données WIS2

    Les outils suivants peuvent également être utilisés pour découvrir et accéder aux données de WIS2 :

    - [pywiscat](https://github.com/wmo-im/pywiscat) fournit une capacité de recherche dans le WIS2 Global Discovery Catalogue pour soutenir le reporting et l'analyse du Catalogue WIS2 et de ses métadonnées de découverte associées
    - [pywis-pubsub](https://github.com/World-Meteorological-Organization/pywis-pubsub) fournit des capacités d'abonnement et de téléchargement des données de l'OMM depuis les services d'infrastructure WIS2

## Préparation

Avant de commencer, veuillez vous connecter à votre VM étudiant et vous assurer que votre instance wis2box est opérationnelle.

## Visualisation du tableau de bord wis2downloader dans Grafana

Ouvrez un navigateur web et accédez au tableau de bord Grafana de votre instance wis2box en allant sur `http://YOUR-HOST:3000`.

Cliquez sur les tableaux de bord dans le menu de gauche, puis sélectionnez le **tableau de bord wis2downloader**.

Vous devriez voir le tableau de bord suivant :

![tableau de bord wis2downloader](../assets/img/wis2downloader-dashboard.png)

Ce tableau de bord est basé sur les métriques publiées par le service wis2downloader et vous montrera l'état des téléchargements actuellement en cours.

Dans le coin supérieur gauche, vous pouvez voir les abonnements actuellement actifs.

Gardez ce tableau de bord ouvert car vous l'utiliserez pour surveiller la progression des téléchargements dans l'exercice suivant.

## Examen de la configuration du wis2downloader

Le service wis2downloader démarré par wis2box-stack peut être configuré à l'aide des variables d'environnement définies dans votre fichier wis2box.env.

Les variables d'environnement suivantes sont utilisées par le wis2downloader :

    - DOWNLOAD_BROKER_HOST : Le nom d'hôte du broker MQTT auquel se connecter. Par défaut : globalbroker.meteo.fr
    - DOWNLOAD_BROKER_PORT : Le port du broker MQTT auquel se connecter. Par défaut : 443 (HTTPS pour websockets)
    - DOWNLOAD_BROKER_USERNAME : Le nom d'utilisateur pour se connecter au broker MQTT. Par défaut : everyone
    - DOWNLOAD_BROKER_PASSWORD : Le mot de passe pour se connecter au broker MQTT. Par défaut : everyone
    - DOWNLOAD_BROKER_TRANSPORT : websockets ou tcp, le mécanisme de transport à utiliser pour se connecter au broker MQTT. Par défaut : websockets
    - DOWNLOAD_RETENTION_PERIOD_HOURS : La période de rétention en heures pour les données téléchargées. Par défaut : 24
    - DOWNLOAD_WORKERS : Le nombre de workers de téléchargement à utiliser. Par défaut : 8. Détermine le nombre de téléchargements parallèles.
    - DOWNLOAD_MIN_FREE_SPACE_GB : L'espace libre minimum en GB à conserver sur le volume hébergeant les téléchargements. Par défaut : 1.

Pour examiner la configuration actuelle du wis2downloader, vous pouvez utiliser la commande suivante :

```bash
cat ~/wis2box/wis2box.env | grep DOWNLOAD
```

!!! question "Examinez la configuration du wis2downloader"
    
    Quel est le broker MQTT par défaut auquel se connecte le wis2downloader ?

    Quelle est la période de rétention par défaut pour les données téléchargées ?

??? success "Cliquez pour révéler la réponse"

    Le broker MQTT par défaut auquel se connecte le wis2downloader est `globalbroker.meteo.fr`.

    La période de rétention par défaut pour les données téléchargées est de 24 heures.

!!! note "Mise à jour de la configuration du wis2downloader"

    Pour mettre à jour la configuration du wis2downloader, vous pouvez éditer le fichier wis2box.env. Pour appliquer les modifications, vous pouvez relancer la commande de démarrage pour wis2box-stack :

    ```bash
    python3 wis2box-ctl.py start
    ```

    Et vous verrez le service wis2downloader redémarrer avec la nouvelle configuration.

Vous pouvez conserver la configuration par défaut pour cet exercice.

## Ajout d'abonnements au wis2downloader

Dans le conteneur **wis2downloader**, vous pouvez utiliser la ligne de commande pour lister, ajouter et supprimer des abonnements.

Pour vous connecter au conteneur **wis2downloader**, utilisez la commande suivante :

```bash
python3 wis2box-ctl.py login wis2downloader
```

Puis utilisez la commande suivante pour lister les abonnements actuellement actifs :

```bash
wis2downloader list-subscriptions
```

Cette commande renvoie une liste vide puisqu'aucun abonnement n'est actuellement actif.

Pour cet exercice, nous allons nous abonner au sujet `cache/a/wis2/de-dwd-gts-to-wis2/#`, pour s'abonner aux données publiées par la passerelle GTS-to-WIS2 hébergée par DWD et télécharger les notifications depuis le Global Cache.

Pour ajouter cet abonnement, utilisez la commande suivante :

```bash
wis2downloader add-subscription --topic cache/a/wis2/de-dwd-gts-to-wis2/#
```

Puis quittez le conteneur **wis2downloader** en tapant `exit` :

```bash
exit
```

Vérifiez le tableau de bord wis2downloader dans Grafana pour voir le nouvel abonnement ajouté. Attendez quelques minutes et vous devriez voir les premiers téléchargements commencer. Passez à l'exercice suivant une fois que vous avez confirmé que les téléchargements démarrent.

## Visualisation des données téléchargées

Le service wis2downloader dans wis2box-stack télécharge les données dans le répertoire 'downloads' du répertoire que vous avez défini comme WIS2BOX_HOST_DATADIR dans votre fichier wis2box.env. Pour voir le contenu du répertoire downloads, vous pouvez utiliser la commande suivante :

```bash
ls -R ~/wis2box-data/downloads
```

Notez que les données téléchargées sont stockées dans des répertoires nommés d'après le sujet sur lequel la notification WIS2 a été publiée.

## Suppression d'abonnements du wis2downloader

Ensuite, reconnectez-vous au conteneur wis2downloader :

```bash
python3 wis2box-ctl.py login wis2downloader
```

et supprimez l'abonnement que vous avez créé du wis2downloader, en utilisant la commande suivante :

```bash
wis2downloader remove-subscription --topic cache/a/wis2/de-dwd-gts-to-wis2/#
```

Et quittez le conteneur wis2downloader en tapant `exit` :
    
```bash
exit
```

Vérifiez le tableau de bord wis2downloader dans Grafana pour voir l'abonnement supprimé. Vous devriez voir les téléchargements s'arrêter.

## Téléchargement et décodage des données pour une trajectoire de cyclone tropical

Dans cet exercice, vous allez vous abonner au WIS2 Training Broker qui publie des données d'exemple à des fins de formation. Vous configurerez un abonnement pour télécharger des données pour une trajectoire de cyclone tropical. Vous décoderez ensuite les données téléchargées à l'aide du conteneur "decode-bufr-jupyter".

### S'abonner au wis2training-broker et configurer un nouvel abonnement

Ceci démontre comment s'abonner à un broker qui n'est pas le broker par défaut et vous permettra de télécharger des données publiées depuis le WIS2 Training Broker.

Éditez le fichier wis2box.env et changez DOWNLOAD_BROKER_HOST en `wis2training-broker.wis2dev.io`, changez DOWNLOAD_BROKER_PORT en `1883` et changez DOWNLOAD_BROKER_TRANSPORT en `tcp` :

```copy
# paramètres du downloader
DOWNLOAD_BROKER_HOST=wis2training-broker.wis2dev.io
DOWNLOAD_BROKER_PORT=1883
DOWNLOAD_BROKER_USERNAME=everyone
DOWNLOAD_BROKER_PASSWORD=everyone
# mécanisme de transport pour le téléchargement (tcp ou websockets)
DOWNLOAD_BROKER_TRANSPORT=tcp
```

Puis exécutez à nouveau la commande 'start' pour appliquer les modifications :

```bash
python3 wis2box-ctl.py start
```

Vérifiez les logs du wis2downloader pour voir si la connexion au nouveau broker a réussi :

```bash
docker logs wis2downloader
```

Vous devriez voir le message de log suivant :

```copy
...
INFO - Connecting...
INFO - Host: wis2training-broker.wis2dev.io, port: 1883
INFO - Connected successfully
```

Maintenant, nous allons configurer un nouvel abonnement au sujet pour télécharger les données de trajectoire de cyclone depuis le WIS2 Training Broker.

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

!!! note "Téléchargement de données depuis le WIS2 Training Broker"

    Le WIS2 Training Broker est un broker de test utilisé à des fins de formation et peut ne pas publier des données en permanence.

    Pendant les sessions de formation en présentiel, le formateur local s'assurera que le WIS2 Training Broker publiera des données que vous pourrez télécharger.

    Si vous faites cet exercice en dehors d'une session de formation, il est possible que vous ne voyiez aucune donnée être téléchargée.

Vérifiez que les données ont été téléchargées en vérifiant à nouveau les logs du wis2downloader avec :

```bash
docker logs wis2downloader
```

Vous devriez voir un message de log similaire à celui-ci :

```copy
[...] INFO - Message received under topic origin/a/wis2/int-wis2-training/data/core/weather/prediction/forecast/medium-range/probabilistic/trajectory
[...] INFO - Downloaded A_JSXX05ECEP020000_C_ECMP_...
```

### Décodage des données téléchargées

Afin de démontrer comment vous pouvez décoder les données téléchargées, nous allons démarrer un nouveau conteneur utilisant l'image 'decode-bufr-jupyter'.

Ce conteneur démarrera un serveur Jupyter notebook sur votre instance qui inclut la bibliothèque "ecCodes" que vous pouvez utiliser pour décoder les données BUFR.

Nous utiliserons les notebooks d'exemple inclus dans `~/exercise-materials/notebook-examples` pour décoder les données téléchargées pour les trajectoires de cyclones.

Pour démarrer le conteneur, utilisez la commande suivante :

```bash
docker run -d --name decode-bufr-jupyter \
    -v ~/wis2box-data/downloads:/root/downloads \
    -p 8888:8888 \
    -e JUPYTER_TOKEN=dataismagic! \
    mlimper/decode-bufr-jupyter
```

!!! note "À propos du conteneur decode-bufr-jupyter"

    Le conteneur `decode-bufr-jupyter` est un conteneur personnalisé qui inclut la bibliothèque ecCodes et exécute un serveur Jupyter notebook. Le conteneur est basé sur une image qui inclut la bibliothèque `ecCodes` pour décoder les données BUFR, ainsi que des bibliothèques pour le traçage et l'analyse de données.

    La commande ci-dessus démarre le conteneur en mode détaché, avec le nom `decode-bufr-jupyter`, le port 8888 est mappé sur le système hôte et la variable d'environnement `JUPYTER_TOKEN` est définie sur `dataismagic!`.
    
    La commande ci-dessus monte également le répertoire `~/wis2box-data/downloads` sur `/root/downloads` dans le conteneur. Cela garantit que les données téléchargées sont disponibles pour le serveur Jupyter notebook.
    
Une fois le conteneur démarré, vous pouvez accéder au serveur Jupyter notebook en naviguant vers `http://YOUR-HOST:8888` dans votre navigateur web.

Vous verrez un écran vous demandant d'entrer un "Mot de passe ou jeton".

Fournissez le jeton `dataismagic!` pour vous connecter au serveur Jupyter
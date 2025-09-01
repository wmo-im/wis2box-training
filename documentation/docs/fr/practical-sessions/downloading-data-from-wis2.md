---
title: Télécharger des données depuis WIS2 en utilisant wis2downloader
---

# Télécharger des données depuis WIS2 en utilisant wis2downloader

!!! abstract "Objectifs d'apprentissage !"

    À la fin de cette session pratique, vous serez capable de :

    - utiliser le "wis2downloader" pour vous abonner aux notifications de données WIS2 et télécharger des données sur votre système local
    - visualiser l'état des téléchargements dans le tableau de bord Grafana
    - apprendre à configurer le wis2downloader pour s'abonner à un broker non par défaut

## Introduction

Dans cette session, vous apprendrez à configurer un abonnement à un Broker WIS2 et à télécharger automatiquement des données sur votre système local en utilisant le service "wis2downloader" inclus dans le wis2box.

!!! note "À propos de wis2downloader"
     
     Le wis2downloader est également disponible en tant que service autonome qui peut être exécuté sur un système différent de celui qui publie les notifications WIS2. Consultez [wis2downloader](https://pypi.org/project/wis2downloader/) pour plus d'informations sur l'utilisation de wis2downloader en tant que service autonome.

     Si vous souhaitez développer votre propre service pour vous abonner aux notifications WIS2 et télécharger des données, vous pouvez utiliser le [code source de wis2downloader](https://github.com/World-Meteorological-Organization/wis2downloader) comme référence.

## Préparation

Avant de commencer, connectez-vous à votre machine virtuelle étudiante et assurez-vous que votre instance wis2box est opérationnelle.

## Bases de wis2downloader

Le wis2downloader est inclus en tant que conteneur séparé dans wis2box, tel que défini dans les fichiers Docker Compose. Le conteneur Prometheus dans wis2box est configuré pour collecter les métriques du conteneur wis2downloader, et ces métriques peuvent être visualisées dans un tableau de bord Grafana.

### Visualiser le tableau de bord wis2downloader dans Grafana

Ouvrez un navigateur web et accédez au tableau de bord Grafana de votre instance wis2box en allant sur `http://YOUR-HOST:3000`.

Cliquez sur "dashboards" dans le menu de gauche, puis sélectionnez le **tableau de bord wis2downloader**.

Vous devriez voir le tableau de bord suivant :

![Tableau de bord wis2downloader](../assets/img/wis2downloader-dashboard.png)

Ce tableau de bord est basé sur les métriques publiées par le service wis2downloader et vous montrera l'état des téléchargements en cours.

Dans le coin supérieur gauche, vous pouvez voir les abonnements actuellement actifs.

Gardez ce tableau de bord ouvert, car vous l'utiliserez pour surveiller la progression des téléchargements dans l'exercice suivant.

### Examiner la configuration de wis2downloader

Le service wis2downloader dans wis2box peut être configuré à l'aide des variables d'environnement définies dans votre fichier `wis2box.env`.

Les variables d'environnement suivantes sont utilisées par wis2downloader :

    - DOWNLOAD_BROKER_HOST : Le nom d'hôte du broker MQTT auquel se connecter. Par défaut : globalbroker.meteo.fr
    - DOWNLOAD_BROKER_PORT : Le port du broker MQTT auquel se connecter. Par défaut : 443 (HTTPS pour websockets)
    - DOWNLOAD_BROKER_USERNAME : Le nom d'utilisateur pour se connecter au broker MQTT. Par défaut : everyone
    - DOWNLOAD_BROKER_PASSWORD : Le mot de passe pour se connecter au broker MQTT. Par défaut : everyone
    - DOWNLOAD_BROKER_TRANSPORT : websockets ou tcp, le mécanisme de transport à utiliser pour se connecter au broker MQTT. Par défaut : websockets
    - DOWNLOAD_RETENTION_PERIOD_HOURS : La période de rétention en heures pour les données téléchargées. Par défaut : 24
    - DOWNLOAD_WORKERS : Le nombre de threads de téléchargement à utiliser. Par défaut : 8. Détermine le nombre de téléchargements parallèles.
    - DOWNLOAD_MIN_FREE_SPACE_GB : L'espace libre minimum en Go à conserver sur le volume hébergeant les téléchargements. Par défaut : 1.

Pour examiner la configuration actuelle de wis2downloader, vous pouvez utiliser la commande suivante :

```bash
cat ~/wis2box/wis2box.env | grep DOWNLOAD
```

!!! question "Examiner la configuration de wis2downloader"
    
    Quel est le broker MQTT par défaut auquel wis2downloader se connecte ?

    Quelle est la période de rétention par défaut pour les données téléchargées ?

??? success "Cliquez pour révéler la réponse"

    Le broker MQTT par défaut auquel wis2downloader se connecte est `globalbroker.meteo.fr`.

    La période de rétention par défaut pour les données téléchargées est de 24 heures.

!!! note "Mettre à jour la configuration de wis2downloader"

    Pour mettre à jour la configuration de wis2downloader, vous pouvez modifier le fichier wis2box.env. Pour appliquer les modifications, vous pouvez relancer la commande de démarrage pour le stack wis2box :

    ```bash
    python3 wis2box-ctl.py start
    ```

    Vous verrez alors le service wis2downloader redémarrer avec la nouvelle configuration.

Vous pouvez conserver la configuration par défaut pour l'exercice suivant.

### Interface en ligne de commande de wis2downloader

Pour accéder à l'interface en ligne de commande de wis2downloader dans wis2box, connectez-vous au conteneur **wis2downloader** en utilisant la commande suivante :

```bash
python3 wis2box-ctl.py login wis2downloader
```

Utilisez la commande suivante pour lister les abonnements actuellement actifs :

```bash
wis2downloader list-subscriptions
```

Cette commande renvoie une liste vide, car aucun abonnement n'est encore configuré.

## Télécharger des données GTS via un WIS2 Global Broker

Si vous avez conservé la configuration par défaut de wis2downloader, il est actuellement connecté au WIS2 Global Broker hébergé par Météo-France.

### Configurer l'abonnement

Utilisez la commande suivante `cache/a/wis2/de-dwd-gts-to-wis2/#` pour vous abonner aux données publiées par la passerelle GTS-to-WIS2 hébergée par DWD, rendues disponibles via les Global Caches :

```bash
wis2downloader add-subscription --topic cache/a/wis2/de-dwd-gts-to-wis2/#
```

Ensuite, quittez le conteneur **wis2downloader** en tapant `exit` :

```bash
exit
```

### Vérifier les données téléchargées

Vérifiez le tableau de bord wis2downloader dans Grafana pour voir le nouvel abonnement ajouté. Attendez quelques minutes et vous devriez voir les premiers téléchargements commencer. Passez à l'exercice suivant une fois que vous avez confirmé que les téléchargements ont démarré.

Le service wis2downloader dans wis2box télécharge les données dans le répertoire 'downloads' situé dans le répertoire que vous avez défini comme `WIS2BOX_HOST_DATADIR` dans votre fichier `wis2box.env`. Pour afficher le contenu du répertoire des téléchargements, utilisez la commande suivante :

```bash
ls -R ~/wis2box-data/downloads
```

Notez que les données téléchargées sont stockées dans des répertoires nommés d'après le sujet sur lequel la notification WIS2 a été publiée.

!!! question "Visualiser les données téléchargées"

    Quels répertoires voyez-vous dans le répertoire des téléchargements ?

    Voyez-vous des fichiers téléchargés dans ces répertoires ?

??? success "Cliquez pour révéler la réponse"
    Vous devriez voir une structure de répertoires commençant par `cache/a/wis2/de-dwd-gts-to-wis2/`, sous laquelle vous verrez d'autres répertoires nommés d'après les en-têtes des bulletins GTS des données téléchargées.

    Selon le moment où vous avez démarré l'abonnement, vous pourriez ou non voir des fichiers téléchargés dans ce répertoire. Si vous ne voyez pas encore de fichiers, attendez quelques minutes de plus et vérifiez à nouveau.

Nettoyons l'abonnement et les données téléchargées avant de passer à l'exercice suivant.

Reconnectez-vous au conteneur wis2downloader :

```bash
python3 wis2box-ctl.py login wis2downloader
```

et supprimez l'abonnement que vous avez créé dans wis2downloader en utilisant la commande suivante :

```bash
wis2downloader remove-subscription --topic cache/a/wis2/de-dwd-gts-to-wis2/#
```

Supprimez les données téléchargées en utilisant la commande suivante :

```bash
rm -rf /wis2box-data/downloads/cache/*
```

Et quittez le conteneur wis2downloader en tapant `exit` :
    
```bash
exit
```

Vérifiez le tableau de bord wis2downloader dans Grafana pour voir l'abonnement supprimé. Vous devriez voir les téléchargements s'arrêter.

!!! note "À propos des passerelles GTS-to-WIS2"
    Il existe actuellement deux passerelles GTS-to-WIS2 publiant des données via le WIS2 Global Broker et les Global Caches :

    - DWD (Allemagne) : centre-id=*de-dwd-gts-to-wis2*
    - JMA (Japon) : centre-id=*jp-jma-gts-to-wis2*
    
    Si dans l'exercice précédent, vous remplacez `de-dwd-gts-to-wis2` par `jp-jma-gts-to-wis2`, vous recevrez les notifications et les données publiées par la passerelle GTS-to-WIS2 de la JMA.

!!! note "Sujets origin vs cache"

    En vous abonnant à un sujet commençant par `origin/`, vous recevrez des notifications avec une URL canonique pointant vers un serveur de données fourni par le Centre WIS publiant les données.

    En vous abonnant à un sujet commençant par `cache/`, vous recevrez plusieurs notifications pour les mêmes données, une pour chaque Global Cache. Chaque notification contiendra une URL canonique pointant vers le serveur de données du Global Cache respectif. Le wis2downloader téléchargera les données à partir de la première URL canonique qu'il peut atteindre.

## Télécharger des données d'exemple depuis le WIS2 Training Broker

Dans cet exercice, vous vous abonnerez au WIS2 Training Broker, qui publie des données d'exemple à des fins de formation.

### Modifier la configuration de wis2downloader

Cela démontre comment s'abonner à un broker qui n'est pas le broker par défaut et vous permettra de télécharger des données publiées par le WIS2 Training Broker.

Modifiez le fichier `wis2box.env` et changez `DOWNLOAD_BROKER_HOST` en `wis2training-broker.wis2dev.io`, `DOWNLOAD_BROKER_PORT` en `1883` et `DOWNLOAD_BROKER_TRANSPORT` en `tcp` :

```copy
# downloader settings
DOWNLOAD_BROKER_HOST=wis2training-broker.wis2dev.io
DOWNLOAD_BROKER_PORT=1883
DOWNLOAD_BROKER_USERNAME=everyone
DOWNLOAD_BROKER_PASSWORD=everyone
# download transport mechanism (tcp or websockets)
DOWNLOAD_BROKER_TRANSPORT=tcp
```

Ensuite, exécutez à nouveau la commande 'start' pour appliquer les modifications :

```bash
python3 wis2box-ctl.py start
```

Vérifiez les journaux de **wis2downloader** pour voir si la connexion au nouveau broker a réussi :

```bash
docker logs wis2downloader
```

Vous devriez voir le message suivant dans les journaux :

```copy
...
INFO - Connecting...
INFO - Host: wis2training-broker.wis2dev.io, port: 1883
INFO - Connected successfully
```

### Configurer de nouveaux abonnements

Nous allons maintenant configurer un nouvel abonnement au topic pour télécharger les données de trajectoire des cyclones depuis le WIS2 Training Broker.

Connectez-vous au conteneur **wis2downloader** :

```bash
python3 wis2box-ctl.py login wis2downloader
```

Et exécutez la commande suivante (copiez-collez pour éviter les erreurs) :

```bash
wis2downloader add-subscription --topic origin/a/wis2/int-wis2-training/data/core/weather/prediction/forecast/medium-range/probabilistic/trajectory
```

Quittez le conteneur **wis2downloader** en tapant `exit`.

### Vérifier les données téléchargées

Attendez de voir les téléchargements commencer dans le tableau de bord **wis2downloader** dans Grafana.

Vérifiez que les données ont été téléchargées en consultant à nouveau les journaux de **wis2downloader** avec :

```bash
docker logs wis2downloader
```

Vous devriez voir un message similaire dans les journaux :

```copy
[...] INFO - Message received under topic origin/a/wis2/int-wis2-training/data/core/weather/prediction/forecast/medium-range/probabilistic/trajectory
[...] INFO - Downloaded A_JSXX05ECEP020000_C_ECMP_...
```

Vérifiez à nouveau le contenu du répertoire des téléchargements :

```bash
ls -R ~/wis2box-data/downloads
```

Vous devriez voir un nouveau répertoire nommé `origin/a/wis2/int-wis2-training/data/core/weather/prediction/forecast/medium-range/probabilistic/trajectory` contenant les données téléchargées.

!!! question "Examiner les données téléchargées"
    
    Quel est le format des fichiers téléchargés ?

??? success "Cliquez pour révéler la réponse"

    Les données téléchargées sont au format BUFR, comme indiqué par l'extension `.bufr`.

Essayez ensuite d'ajouter deux autres abonnements pour télécharger les anomalies mensuelles de température de surface et les données de prévision globale d'ensemble à partir des topics suivants :

- `origin/a/wis2/int-wis2-training/data/core/weather/prediction/forecast/medium-range/probabilistic/global`
- `origin/a/wis2/int-wis2-training/data/core/climate/experimental/anomalies/monthly/surface-temperature`

Attendez de voir les téléchargements commencer dans le tableau de bord **wis2downloader** dans Grafana.

Vérifiez à nouveau le contenu du répertoire des téléchargements :

```bash
ls -R ~/wis2box-data/downloads
```

Vous devriez voir deux nouveaux répertoires nommés `origin/a/wis2/int-wis2-training/data/core/weather/prediction/forecast/medium-range/probabilistic/global` et `origin/a/wis2/int-wis2-training/data/core/climate/experimental/anomalies/monthly/surface-temperature` contenant les données téléchargées.

!!! question "Examiner les données téléchargées pour les deux nouveaux topics"
    
    Quel est le format des fichiers téléchargés pour le topic `../prediction/forecast/medium-range/probabilistic/global` ?

    Quel est le format des fichiers téléchargés pour le topic `../climate/experimental/anomalies/monthly/surface-temperature` ?

??? success "Cliquez pour révéler la réponse"

    Les données téléchargées pour le topic `../prediction/forecast/medium-range/probabilistic/global` sont au format GRIB2, comme indiqué par l'extension `.grib2`.

    Les données téléchargées pour le topic `../climate/experimental/anomalies/monthly/surface-temperature` sont au format NetCDF, comme indiqué par l'extension `.nc`.

## Conclusion

!!! success "Félicitations !"

    Lors de cette session pratique, vous avez appris à :

    - utiliser le **wis2downloader** pour s'abonner à un WIS2 Broker et télécharger des données sur votre système local
    - consulter l'état des téléchargements dans le tableau de bord Grafana
    - modifier la configuration par défaut du **wis2downloader** pour s'abonner à un autre broker
    - visualiser les données téléchargées sur votre système local
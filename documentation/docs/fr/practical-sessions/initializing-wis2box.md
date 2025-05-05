---
title: Initialisation de wis2box
---

# Initialisation de wis2box

!!! abstract "Objectifs d'apprentissage"

    À la fin de cette session pratique, vous serez capable de :

    - exécuter le script `wis2box-create-config.py` pour créer la configuration initiale
    - démarrer wis2box et vérifier l'état de ses composants
    - consulter le contenu de **wis2box-api**
    - accéder à **wis2box-webapp**
    - vous connecter au **wis2box-broker** local en utilisant MQTT Explorer

!!! note

    Les supports de formation actuels sont basés sur wis2box-release 1.0.0.
    
    Consultez [accessing-your-student-vm](accessing-your-student-vm.md) pour les instructions sur le téléchargement et l'installation de la pile logicielle wis2box si vous suivez cette formation en dehors d'une session de formation locale.

## Préparation

Connectez-vous à votre VM désignée avec votre nom d'utilisateur et mot de passe et assurez-vous d'être dans le répertoire `wis2box` :

```bash
cd ~/wis2box
```

## Création de la configuration initiale

La configuration initiale de wis2box nécessite :

- un fichier d'environnement `wis2box.env` contenant les paramètres de configuration
- un répertoire sur la machine hôte à partager entre la machine hôte et les conteneurs wis2box défini par la variable d'environnement `WIS2BOX_HOST_DATADIR`

Le script `wis2box-create-config.py` peut être utilisé pour créer la configuration initiale de votre wis2box.

Il vous posera une série de questions pour vous aider à configurer votre installation.

Vous pourrez examiner et mettre à jour les fichiers de configuration une fois le script terminé.

Exécutez le script comme suit :

```bash
python3 wis2box-create-config.py
```

### Répertoire wis2box-host-data

Le script vous demandera d'entrer le répertoire à utiliser pour la variable d'environnement `WIS2BOX_HOST_DATADIR`.

Notez que vous devez définir le chemin complet vers ce répertoire.

Par exemple, si votre nom d'utilisateur est `username`, le chemin complet vers le répertoire est `/home/username/wis2box-data` :

```{.copy}
username@student-vm-username:~/wis2box$ python3 wis2box-create-config.py
Please enter the directory to be used for WIS2BOX_HOST_DATADIR:
/home/username/wis2box-data
The directory to be used for WIS2BOX_HOST_DATADIR will be set to:
    /home/username/wis2box-data
Is this correct? (y/n/exit)
y
The directory /home/username/wis2box-data has been created.
```

### URL wis2box

Ensuite, on vous demandera d'entrer l'URL de votre wis2box. C'est l'URL qui sera utilisée pour accéder à l'application web, l'API et l'interface utilisateur de wis2box.

Veuillez utiliser `http://<votre-nom-d'hôte-ou-ip>` comme URL.

```{.copy}
Please enter the URL of the wis2box:
 For local testing the URL is http://localhost
 To enable remote access, the URL should point to the public IP address or domain name of the server hosting the wis2box.
http://username.wis2.training
The URL of the wis2box will be set to:
  http://username.wis2.training
Is this correct? (y/n/exit)
```

### Mots de passe WEBAPP, STORAGE et BROKER

Vous pouvez utiliser l'option de génération de mot de passe aléatoire lorsqu'on vous le demande pour `WIS2BOX_WEBAPP_PASSWORD`, `WIS2BOX_STORAGE_PASSWORD`, `WIS2BOX_BROKER_PASSWORD` ou définir les vôtres.

Ne vous inquiétez pas de mémoriser ces mots de passe, ils seront stockés dans le fichier `wis2box.env` dans votre répertoire wis2box.

### Vérification de `wis2box.env`

Une fois le script terminé, vérifiez le contenu du fichier `wis2box.env` dans votre répertoire actuel :

```bash
cat ~/wis2box/wis2box.env
```

Ou vérifiez le contenu du fichier via WinSCP.

!!! question

    Quelle est la valeur de WISBOX_BASEMAP_URL dans le fichier wis2box.env ?

??? success "Cliquez pour révéler la réponse"

    La valeur par défaut de WIS2BOX_BASEMAP_URL est `https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png`.

    Cette URL fait référence au serveur de tuiles OpenStreetMap. Si vous souhaitez utiliser un autre fournisseur de cartes, vous pouvez modifier cette URL pour pointer vers un autre serveur de tuiles.

!!! question 

    Quelle est la valeur de la variable d'environnement WIS2BOX_STORAGE_DATA_RETENTION_DAYS dans le fichier wis2box.env ?

??? success "Cliquez pour révéler la réponse"

    La valeur par défaut de WIS2BOX_STORAGE_DATA_RETENTION_DAYS est de 30 jours. Vous pouvez modifier cette valeur si vous le souhaitez.
    
    Le conteneur wis2box-management exécute une tâche cron quotidiennement pour supprimer les données plus anciennes que le nombre de jours défini par WIS2BOX_STORAGE_DATA_RETENTION_DAYS du bucket `wis2box-public` et du backend de l'API :
    
    ```{.copy}
    0 0 * * * su wis2box -c "wis2box data clean --days=$WIS2BOX_STORAGE_DATA_RETENTION_DAYS"
    ```

!!! note

    Le fichier `wis2box.env` contient les variables d'environnement définissant la configuration de votre wis2box. Pour plus d'informations, consultez la [documentation wis2box](https://docs.wis2box.wis.wmo.int/en/latest/reference/configuration.html).

    Ne modifiez pas le fichier `wis2box.env` sauf si vous êtes sûr des modifications que vous apportez. Des modifications incorrectes peuvent empêcher votre wis2box de fonctionner.

    Ne partagez pas le contenu de votre fichier `wis2box.env` avec qui que ce soit, car il contient des informations sensibles comme des mots de passe.

## Démarrer wis2box

Assurez-vous d'être dans le répertoire contenant les fichiers de définition de la pile logicielle wis2box :

```{.copy}
cd ~/wis2box
```

Démarrez wis2box avec la commande suivante :

```{.copy}
python3 wis2box-ctl.py start
```

Lors de la première exécution de cette commande, vous verrez la sortie suivante :

```
No docker-compose.images-*.yml files found, creating one
Current version=Undefined, latest version=1.0.0
Would you like to update ? (y/n/exit)
```

Sélectionnez `y` et le script créera le fichier `docker-compose.images-1.0.0.yml`, téléchargera les images Docker requises et démarrera les services.

Le téléchargement des images peut prendre du temps selon votre vitesse de connexion Internet. Cette étape n'est nécessaire que la première fois que vous démarrez wis2box.

Vérifiez l'état avec la commande suivante :

```{.copy}
python3 wis2box-ctl.py status
```

Répétez cette commande jusqu'à ce que tous les services soient opérationnels.

!!! note "wis2box et Docker"
    wis2box fonctionne comme un ensemble de conteneurs Docker gérés par docker-compose.
    
    Les services sont définis dans les différents fichiers `docker-compose*.yml` qui se trouvent dans le répertoire `~/wis2box/`.
    
    Le script Python `wis2box-ctl.py` est utilisé pour exécuter les commandes Docker Compose sous-jacentes qui contrôlent les services wis2box.

    Vous n'avez pas besoin de connaître les détails des conteneurs Docker pour exécuter la pile logicielle wis2box, mais vous pouvez inspecter les fichiers `docker-compose*.yml` pour voir comment les services sont définis. Si vous souhaitez en savoir plus sur Docker, vous pouvez consulter la [documentation Docker](https://docs.docker.com/).

Pour vous connecter au conteneur wis2box-management, utilisez la commande suivante :

```{.copy}
python3 wis2box-ctl.py login
```

Dans le conteneur wis2box-management, vous pouvez exécuter diverses commandes pour gérer votre wis2box, comme :

- `wis2box auth add-token --path processes/wis2box` : pour créer un jeton d'autorisation pour le point d'accès `processes/wis2box`
- `wis2box data clean --days=<nombre-de-jours>` : pour nettoyer les données plus anciennes qu'un certain nombre de jours du bucket `wis2box-public`

Pour quitter le conteneur et revenir à la machine hôte, utilisez la commande suivante :

```{.copy}
exit
```

Exécutez la commande suivante pour voir les conteneurs docker en cours d'exécution sur votre machine hôte :

```{.copy}
docker ps
```

Vous devriez voir les conteneurs suivants en cours d'exécution :

- wis2box-management
- wis2box-api
- wis2box-minio
- wis2box-webapp
- wis2box-auth
- wis2box-ui
- wis2downloader
- elasticsearch
- elasticsearch-exporter
- nginx
- mosquitto
- prometheus
- grafana
- loki

Ces conteneurs font partie de la pile logicielle wis2box et fournissent les différents services nécessaires au fonctionnement de wis2box.

Exécutez la commande suivante pour voir les volumes docker sur votre machine hôte :

```{.copy}
docker volume ls
```

Vous devriez voir les volumes suivants :

- wis2box_project_auth-data
- wis2box_project_es-data
- wis2box_project_htpasswd
- wis2box_project_minio-data
- wis2box_project_prometheus-data
- wis2box_project_loki-data
- wis2box_project_mosquitto-config

Ainsi que quelques volumes anonymes utilisés par les différents conteneurs.

Les volumes commençant par `wis2box_project_` sont utilisés pour stocker les données persistantes des différents services de la pile logicielle wis2box.

## API wis2box

Le wis2box contient une API (Interface de Programmation d'Application) qui fournit un accès aux données et des processus pour la visualisation interactive, la transformation des données et la publication.

Ouvrez un nouvel onglet et naviguez vers la page `http://YOUR-HOST/oapi`.

<img alt="wis2box-api.png" src="../../assets/img/wis2box-api.png" width="800">

C'est la page d'accueil de l'API wis2box (exécutée via le conteneur **wis2box-api**).

!!! question
     
     Quelles collections sont actuellement disponibles ?

??? success "Cliquez pour révéler la réponse"
    
    Pour voir les collections actuellement disponibles via l'API, cliquez sur `View the collections in this service` :

    <img alt="wis2box-api-collections.png" src="../../assets/img/wis2box-api-collections.png" width="600">

    Les collections suivantes sont actuellement disponibles :

    - Stations
    - Notifications de données
    - Métadonnées de découverte

!!! question

    Combien de notifications de données ont été publiées ?

??? success "Cliquez pour révéler la réponse"

    Cliquez sur "Data notifications", puis sur `Browse through the items of "Data Notifications"`. 
    
    Vous remarquerez que la page indique "No items" car aucune notification de données n'a encore été publiée.

## Application web wis2box

Ouvrez un navigateur web et visitez la page `http://YOUR-HOST/wis2box-webapp`.

Une fenêtre pop-up vous demandera votre nom d'utilisateur et mot de passe. Utilisez le nom d'utilisateur par défaut `wis2box-user` et le `WIS2BOX_WEBAPP_PASSWORD` défini dans le fichier `wis2box.env` et cliquez sur "Sign in" :

!!! note 

    Vérifiez votre wis2box.env pour la valeur de votre WIS2BOX_WEBAPP_PASSWORD. Vous pouvez utiliser la commande suivante pour vérifier la valeur de cette variable d'environnement :

    ```{.copy}
    cat ~/wis2box/wis2box.env | grep WIS2BOX_WEBAPP_PASSWORD
    ```

Une fois connecté, déplacez votre souris vers le menu à gauche pour voir les options disponibles dans l'application web wis2box :

<img alt="wis2box-webapp-menu.png" src="../../assets/img/wis2box-webapp-menu.png" width="400">

C'est l'application web wis2box qui vous permet d'interagir avec votre wis2box :

- créer et gérer des jeux de données
- mettre à jour/réviser vos métadonnées de station
- télécharger des observations manuelles en utilisant le formulaire FM-12 synop
- surveiller les notifications publiées sur votre wis2box-broker

Nous utiliserons cette application web dans une session ultérieure.

## wis2box-broker

Ouvrez MQTT Explorer sur votre ordinateur et préparez une nouvelle connexion pour vous connecter à votre broker (exécuté via le conteneur **wis2box-broker**).

Cliquez sur `+` pour ajouter une nouvelle connexion :

<img alt="mqtt-explorer-new-connection.png" src="../../assets/img/mqtt-explorer-new-connection.png" width="300">

Vous pouvez cliquer sur le bouton 'ADVANCED' et vérifier que vous avez des abonnements aux sujets suivants :

- `#`
- `$SYS/#`

<img alt="mqtt-explorer-topics.png" src="../../assets/img/mqtt-explorer-topics.png" width="550">

!!! note

    Le sujet `#` est un abonnement générique qui s'abonnera à tous les sujets publiés sur le broker.

    Les messages publiés sous le sujet `$SYS` sont des messages
---
title: Initialisation de wis2box
---

# Initialisation de wis2box

!!! abstract "Résultats d'apprentissage"

    À la fin de cette session pratique, vous serez capable de :

    - exécuter le script `wis2box-create-config.py` pour créer la configuration initiale
    - démarrer wis2box et vérifier l'état de ses composants
    - consulter le contenu de **wis2box-api**
    - accéder à **wis2box-webapp**
    - vous connecter au **wis2box-broker** local en utilisant MQTT Explorer

!!! note

    Les supports de formation actuels sont basés sur wis2box-release 1.0.0.
    
    Consultez [accessing-your-student-vm](./accessing-your-student-vm.md) pour des instructions sur comment télécharger et installer la pile logicielle wis2box si vous suivez cette formation en dehors d'une session locale.

## Préparation

Connectez-vous à votre VM désignée avec votre nom d'utilisateur et votre mot de passe et assurez-vous d'être dans le répertoire `wis2box` :

```bash
cd ~/wis2box
```

## Création de la configuration initiale

La configuration initiale pour wis2box nécessite :

- un fichier d'environnement `wis2box.env` contenant les paramètres de configuration
- un répertoire sur la machine hôte à partager entre la machine hôte et les conteneurs wis2box définis par la variable d'environnement `WIS2BOX_HOST_DATADIR`

Le script `wis2box-create-config.py` peut être utilisé pour créer la configuration initiale de votre wis2box.

Il vous posera une série de questions pour aider à configurer votre installation.

Vous pourrez revoir et mettre à jour les fichiers de configuration après que le script ait terminé.

Exécutez le script comme suit :

```bash
python3 wis2box-create-config.py
```

### Répertoire wis2box-host-data

Le script vous demandera d'entrer le répertoire à utiliser pour la variable d'environnement `WIS2BOX_HOST_DATADIR`.

Notez que vous devez définir le chemin complet de ce répertoire.

Par exemple, si votre nom d'utilisateur est `username`, le chemin complet du répertoire est `/home/username/wis2box-data` :

```{.copy}
username@student-vm-username:~/wis2box$ python3 wis2box-create-config.py
Veuillez entrer le répertoire à utiliser pour WIS2BOX_HOST_DATADIR :
/home/username/wis2box-data
Le répertoire à utiliser pour WIS2BOX_HOST_DATADIR sera défini sur :
    /home/username/wis2box-data
Est-ce correct ? (y/n/exit)
y
Le répertoire /home/username/wis2box-data a été créé.
```

### URL de wis2box

Ensuite, on vous demandera d'entrer l'URL de votre wis2box. C'est l'URL qui sera utilisée pour accéder à l'application web wis2box, à l'API et à l'UI.

Veuillez utiliser `http://<votre-nom-d'hôte-ou-ip>` comme URL.

```{.copy}
Veuillez entrer l'URL de wis2box :
 Pour les tests locaux, l'URL est http://localhost
 Pour permettre un accès à distance, l'URL doit pointer vers l'adresse IP publique ou le nom de domaine du serveur hébergeant wis2box.
http://username.wis2.training
L'URL de wis2box sera définie sur :
  http://username.wis2.training
Est-ce correct ? (y/n/exit)
```

### Mots de passe WEBAPP, STORAGE et BROKER

Vous pouvez utiliser l'option de génération de mot de passe aléatoire lorsqu'elle vous est proposée pour `WIS2BOX_WEBAPP_PASSWORD`, `WIS2BOX_STORAGE_PASSWORD`, `WIS2BOX_BROKER_PASSWORD` et définir les vôtres.

Ne vous inquiétez pas de retenir ces mots de passe, ils seront stockés dans le fichier `wis2box.env` dans votre répertoire wis2box.

### Révision de `wis2box.env`

Une fois les scripts terminés, vérifiez le contenu du fichier `wis2box.env` dans votre répertoire actuel :

```bash
cat ~/wis2box/wis2box.env
```

Ou vérifiez le contenu du fichier via WinSCP.

!!! question

    Quelle est la valeur de WISBOX_BASEMAP_URL dans le fichier wis2box.env ?

??? success "Cliquez pour révéler la réponse"

    La valeur par défaut pour WIS2BOX_BASEMAP_URL est `https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png`.

    Cette URL fait référence au serveur de tuiles OpenStreetMap. Si vous souhaitez utiliser un autre fournisseur de cartes, vous pouvez changer cette URL pour pointer vers un autre serveur de tuiles.

!!! question

    Quelle est la valeur de la variable d'environnement WIS2BOX_STORAGE_DATA_RETENTION_DAYS dans le fichier wis2box.env ?

??? success "Cliquez pour révéler la réponse"

    La valeur par défaut pour WIS2BOX_STORAGE_DATA_RETENTION_DAYS est de 30 jours. Vous pouvez modifier cette valeur pour un nombre différent de jours si vous le souhaitez.
    
    Le conteneur wis2box-management exécute une tâche cron quotidienne pour supprimer les données plus anciennes que le nombre de jours défini par WIS2BOX_STORAGE_DATA_RETENTION_DAYS du seau `wis2box-public` et de l'API backend :
    
    ```{.copy}
    0 0 * * * su wis2box -c "wis2box data clean --days=$WIS2BOX_STORAGE_DATA_RETENTION_DAYS"
    ```

!!! note

    Le fichier `wis2box.env` contient des variables d'environnement définissant la configuration de votre wis2box. Pour plus d'informations, consultez la [wis2box-documentation](https://docs.wis2box.wis.wmo.int/en/latest/reference/configuration.html).

    Ne modifiez pas le fichier `wis2box.env` à moins d'être sûr des modifications que vous apportez. Des modifications incorrectes peuvent entraîner l'arrêt de fonctionnement de votre wis2box.

    Ne partagez pas le contenu de votre fichier `wis2box.env` avec quiconque, car il contient des informations sensibles telles que des mots de passe.

## Démarrage de wis2box

Assurez-vous d'être dans le répertoire contenant les fichiers de définition de la pile logicielle wis2box :

```{.copy}
cd ~/wis2box
```

Démarrer wis2box avec la commande suivante :

```{.copy}
python3 wis2box-ctl.py start
```

Lorsque vous exécutez cette commande pour la première fois, vous verrez le message suivant :

```
Aucun fichier docker-compose.images-*.yml trouvé, en création d'un
Version actuelle=Indéfinie, dernière version=1.0.0
Souhaitez-vous mettre à jour ? (y/n/exit)
```

Sélectionnez ``y`` et le script créera le fichier ``docker-compose.images-1.0.0.yml``, téléchargera les images Docker nécessaires et démarrera les services.

Le téléchargement des images peut prendre du temps en fonction de la vitesse de votre connexion internet. Cette étape n'est nécessaire que la première fois que vous démarrez wis2box.

Inspectez l'état avec la commande suivante :

```{.copy}
python3 wis2box-ctl.py status
```

Répétez cette commande jusqu'à ce que tous les services soient opérationnels.

!!! note "wis2box et Docker"
    wis2box fonctionne comme un ensemble de conteneurs Docker gérés par docker-compose.
    
    Les services sont définis dans les différents `docker-compose*.yml` qui peuvent être trouvés dans le répertoire `~/wis2box/`.
    
    Le script Python `wis2box-ctl.py` est utilisé pour exécuter les commandes Docker Compose sous-jacentes qui contrôlent les services wis2box.

    Vous n'avez pas besoin de connaître les détails des conteneurs Docker pour exécuter la pile logicielle wis2box, mais vous pouvez inspecter les fichiers `docker-compose*.yml` pour voir comment les services sont définis. Si vous souhaitez en savoir plus sur Docker, vous pouvez trouver plus d'informations dans la [documentation Docker](https://docs.docker.com/).

Pour vous connecter au conteneur wis2box-management, utilisez la commande suivante :

```{.copy}
python3 wis2box-ctl.py login
```

À l'intérieur du conteneur wis2box-management, vous pouvez exécuter diverses commandes pour gérer votre wis2box, telles que :

- `wis2box auth add-token --path processes/wis2box` : pour créer un jeton d'autorisation pour le point de terminaison `processes/wis2box`
- `wis2box data clean --days=<nombre-de-jours>` : pour nettoyer les données plus anciennes qu'un certain nombre de jours du seau `wis2box-public`

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

Exécutez la commande suivante pour voir les volumes docker en cours d'exécution sur votre machine hôte :

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

Ainsi que certains volumes anonymes utilisés par les différents conteneurs.

Les volumes commençant par `wis2box_project_` sont utilisés pour stocker des données persistantes pour les différents services de la pile logicielle wis2box.

## API wis2box

wis2box contient une API (Interface de Programmation d'Applications) qui fournit un accès aux données et des processus pour la visualisation interactive, la transformation des données et la publication.

Ouvrez un nouvel onglet et naviguez vers la page `http://YOUR-HOST/oapi`.

<img alt="wis2box-api.png" src="/../assets/img/wis2box-api.png" width="800">

Ceci est la page d'accueil de l'API wis2box (exécutée via le conteneur **wis2box-api**).

!!! question

     Quelles collections sont actuellement disponibles ?

??? success "Cliquez pour révéler la réponse"
    
    Pour voir les collections actuellement disponibles via l'API, cliquez sur `Voir les collections de ce service` :

    <img alt="wis2box-api-collections.png" src="/../assets/img/wis2box-api-collections.png" width="600">

    Les collections suivantes sont actuellement disponibles :

    - Stations
    - Notifications de données
    - Métadonnées de découverte


!!! question

    Combien de notifications de données ont été publiées ?

??? success "Cliquez pour révéler la réponse"

    Cliquez sur "Notifications de données", puis cliquez sur `Parcourir les éléments de "Notifications de données"`. 
    
    Vous remarquerez que la page indique "Aucun élément" car aucune notification de données n'a encore été publiée.

## Application web wis2box

Ouvrez un navigateur web et visitez la page `http://YOUR-HOST/wis2box-webapp`.

Vous verrez une fenêtre pop-up vous demandant votre nom d'utilisateur et votre mot de passe. Utilisez le nom d'utilisateur par défaut `wis2box-user` et le `WIS2BOX_WEBAPP_PASSWORD` défini dans le fichier `wis2box.env` et cliquez sur "Se connecter" :

!!! note

    Vérifiez votre wis2box.env pour la valeur de votre WIS2BOX_WEBAPP_PASSWORD. Vous pouvez utiliser la commande suivante pour vérifier la valeur de cette variable d'environnement :

    ```{.copy}
    cat ~/wis2box/wis2box.env | grep WIS2BOX_WEBAPP_PASSWORD
    ```

Une fois connecté, déplacez votre souris vers le menu à gauche pour voir les options disponibles dans l'application web wis2box :

<img alt="wis2box-webapp-menu.png" src="/../assets/img/wis2box-webapp-menu.png" width="400">

Ceci est l'application web wis2box qui vous permet d'interagir avec votre wis2box :

- créer et gérer des ensembles de données
- mettre à jour/revoir vos métadonnées de station
- télécharger des observations manuelles utilisant le formulaire synop FM-12
- surveiller les notifications publiées sur votre wis2box-broker

Nous utiliserons cette application web lors d'une session ultérieure.

## wis2box-broker

Ouvrez MQTT Explorer sur votre ordinateur et préparez une nouvelle connexion pour vous connecter à votre courtier (exécuté via le conteneur **wis2box-broker**).

Cliquez sur `+` pour ajouter une nouvelle connexion :

<img alt="mqtt-explorer-new-connection.png" src="/../assets/img/mqtt-explorer-new-connection.png" width="300">

Vous pouvez cliquer sur le bouton 'ADVANCED' et vérifier que vous avez des abonnements aux sujets suivants :

- `#`
- `$SYS/#`

<img alt="mqtt-explorer-topics.png" src="/../assets/img/mqtt-explorer-topics.png" width="550">

!!! note

    Le sujet `#` est un abonnement générique qui s'abonnera à tous les sujets publiés sur le courtier.

    Les messages publiés sous le sujet `$SYS` sont des messages système publiés par le service mosquitto lui-même.

Utilisez les détails de connexion suivants, en veillant à remplacer la valeur de `<votre-hôte>` par votre nom d'hôte et `<WIS2BOX_BROKER_PASSWORD>` par la valeur de votre fichier `wis2box.env` :

- **Protocole : mqtt://**
- **Hôte : `<votre-hôte>`**
- **Port : 1883**
- **Nom d'utilisateur : wis2box**
- **Mot de passe : `<WIS2BOX_BROKER_PASSWORD>`**

!!! note

    Vous pouvez vérifier votre wis2box.env pour la valeur de votre WIS2BOX_BROKER_PASSWORD. Vous pouvez utiliser la commande suivante pour vérifier la valeur de cette variable d'environnement :

    ```{.copy}
    cat ~/wis2box/wis2box.env | grep WIS2BOX_BROKER_PASSWORD
    ```

    Notez qu'il s'agit de votre mot de passe de courtier **interne**, le Global Broker utilisera des informations d'identification différentes (en lecture seule) pour s'abonner à votre courtier. Ne partagez jamais ce mot de passe avec quiconque.

Assurez-vous de cliquer sur "ENREGISTRER" pour stocker vos détails de connexion.

Ensuite, cliquez sur "CONNECTER" pour vous connecter à votre **wis2box-broker**.

<img alt="mqtt-explorer-wis2box-broker.png" src="/../assets/img/mqtt-explorer-wis2box-broker.png" width="600">

Une fois connecté, vérifiez que les statistiques internes mosquitto sont publiées par votre courtier sous le sujet `$SYS` :

<img alt="mqtt-explorer-sys-topic.png" src="/../assets/img/mqtt-explorer-sys-topic.png" width="400">

Gardez MQTT Explorer ouvert, car nous l'utiliserons pour surveiller les messages publiés sur le courtier.

## Conclusion

!!! success "Félicitations !"
    Dans cette session pratique, vous avez appris à :

    - exécuter le script `wis2box-create-config.py` pour créer la configuration initiale
    - démarrer wis2box et vérifier le statut de ses composants
    - accéder à wis2box-webapp et wis2box-API dans un navigateur
    - se connecter au courtier MQTT sur votre VM étudiant en utilisant MQTT Explorer
---
title: Ingestion des données pour publication
---

# Ingestion des données pour publication

!!! abstract "Objectifs d'apprentissage"

    À la fin de cette session pratique, vous serez capable de :
    
    - Déclencher le workflow de wis2box en téléchargeant des données sur MinIO via la ligne de commande, l'interface web de MinIO, SFTP ou un script Python.
    - Accéder au tableau de bord Grafana pour surveiller l'état de l'ingestion des données et consulter les journaux de votre instance wis2box.
    - Consulter les notifications de données WIS2 publiées par votre wis2box à l'aide de MQTT Explorer.

## Introduction

Dans WIS2, les données sont partagées en temps réel à l'aide de notifications de données WIS2 contenant un lien "canonique" à partir duquel les données peuvent être téléchargées.

Pour déclencher le workflow des données dans un WIS2 Node à l'aide du logiciel wis2box, les données doivent être téléchargées dans le bucket **wis2box-incoming** de **MinIO**, ce qui initie le workflow de wis2box. Ce processus aboutit à la publication des données via une notification de données WIS2. Selon les mappages de données configurés dans votre instance wis2box, les données peuvent être transformées au format BUFR avant leur publication.

Dans cet exercice, nous utiliserons des fichiers de données d'exemple pour déclencher le workflow de wis2box et **publier des notifications de données WIS2** pour le jeu de données que vous avez configuré lors de la session pratique précédente.

Pendant l'exercice, nous surveillerons l'état de l'ingestion des données à l'aide du **tableau de bord Grafana** et de **MQTT Explorer**. Le tableau de bord Grafana utilise les données de Prometheus et Loki pour afficher l'état de votre wis2box, tandis que MQTT Explorer vous permet de voir les notifications de données WIS2 publiées par votre instance wis2box.

Notez que wis2box transformera les données d'exemple au format BUFR avant de les publier sur le broker MQTT, conformément aux mappages de données préconfigurés dans votre jeu de données. Pour cet exercice, nous nous concentrerons sur les différentes méthodes de téléchargement des données dans votre instance wis2box et sur la vérification de l'ingestion et de la publication réussies. La transformation des données sera abordée ultérieurement dans la session pratique [Outils de conversion des données](./data-conversion-tools.md).

## Préparation

Cette section utilise deux jeux de données préparés lors de la session pratique Configuration des jeux de données dans wis2box :

1. Le jeu de données prédéfini weather/surface-based-observations/synop.

2. Un jeu de données personnalisé créé avec le modèle Other (exemple GEPS).

L'ingestion de **weather/surface-based-observations/synop** nécessite que les métadonnées des stations soient configurées dans le wis2box-webapp, comme décrit dans la session pratique [Configuration des métadonnées des stations](./configuring-station-metadata.md).

Pour le jeu de données **other** utilisé dans cette formation, le plugin universel de données sans conversion est sélectionné pour publier des fichiers GRIB2 sans transformation. Étant donné que ce jeu de données de formation ne représente pas des observations de stations, la configuration des stations n'est pas nécessaire. Assurez-vous que l'extension de fichier est définie sur .grib2 et que l'expression régulière du modèle de fichier correspond aux noms de vos fichiers de données.

Dans les opérations WIS2 réelles, cependant, si le jeu de données créé avec le modèle **other** est destiné à publier des données d'observation basées sur des stations, les métadonnées des stations doivent être créées et configurées de la même manière que pour *surface-based-observations/synop*.

Assurez-vous de pouvoir vous connecter à votre machine virtuelle étudiante à l'aide de votre client SSH (par exemple, PuTTY).

Assurez-vous que wis2box est en cours d'exécution :

```bash
cd ~/wis2box/
python3 wis2box-ctl.py start
python3 wis2box-ctl.py status
```

Assurez-vous que MQTT Explorer est en cours d'exécution et connecté à votre instance en utilisant les identifiants publics `everyone/everyone` avec un abonnement au sujet `origin/a/wis2/#`.

Assurez-vous d'avoir un navigateur web ouvert avec le tableau de bord Grafana pour votre instance en naviguant vers `http://YOUR-HOST:3000`.

## Préparer les données d'exemple

Copiez le répertoire `exercise-materials/data-ingest-exercises` dans le répertoire que vous avez défini comme `WIS2BOX_HOST_DATADIR` dans votre fichier `wis2box.env` :

```bash
cp -r ~/exercise-materials/data-ingest-exercises ~/wis2box-data/
```

!!! note
    Le `WIS2BOX_HOST_DATADIR` est monté en tant que `/data/wis2box/` dans le conteneur wis2box-management par le fichier `docker-compose.yml` inclus dans le répertoire `wis2box`.
    
    Cela vous permet de partager des données entre l'hôte et le conteneur.

## Ajouter la station de test (Pour les données d'observation basées sur des stations uniquement)

Utilisons le jeu de données prédéfini weather/surface-based-observations/synop qui a été créé précédemment lors de la session pratique (./configuring-wis2box-datasdets.md), un bon exemple basé sur des observations réelles de stations.

Ajoutez la station avec l'identifiant WIGOS `0-20000-0-64400` à votre instance wis2box à l'aide de l'éditeur de stations dans le wis2box-webapp.

Récupérez la station depuis OSCAR :

<img alt="oscar-station" src="/../assets/img/webapp-test-station-oscar-search.png" width="600">

Ajoutez la station aux jeux de données que vous avez créés pour la publication sur "../surface-based-observations/synop" et enregistrez les modifications à l'aide de votre jeton d'authentification :

<img alt="webapp-test-station" src="/../assets/img/webapp-test-station-save.png" width="800">

Notez que vous pouvez supprimer cette station de votre jeu de données après la session pratique.

## Tester l'ingestion des données depuis la ligne de commande

Dans cet exercice, nous utiliserons la commande `wis2box data ingest` pour télécharger des données sur MinIO.

Assurez-vous d'être dans le répertoire `wis2box` et connectez-vous au conteneur **wis2box-management** :

```bash
cd ~/wis2box
python3 wis2box-ctl.py login
```

Vérifiez que les données d'exemple suivantes sont disponibles dans le répertoire `/data/wis2box/` à l'intérieur du conteneur **wis2box-management** :

```bash
ls -lh /data/wis2box/data-ingest-exercises/synop_202412030900.txt
```

!!! question "Ingestion des données à l'aide de `wis2box data ingest`"

    Exécutez la commande suivante pour ingérer le fichier de données d'exemple dans votre instance wis2box :

    ```bash
    wis2box data ingest -p /data/wis2box/data-ingest-exercises/synop_202412030900.txt --metadata-id urn:wmo:md:not-my-centre:synop-test
    ```

    Les données ont-elles été ingérées avec succès ? Sinon, quel était le message d'erreur et comment pouvez-vous le corriger ?

??? success "Cliquez pour révéler la réponse"

    Les données n'ont **pas** été ingérées avec succès. Vous devriez voir le message suivant :

    ```bash
    Error: metadata_id=urn:wmo:md:not-my-centre:synop-test not found in data mappings
    ```

    Le message d'erreur indique que l'identifiant de métadonnées que vous avez fourni ne correspond à aucun des jeux de données que vous avez configurés dans votre instance wis2box.

    Fournissez l'identifiant de métadonnées correct correspondant au jeu de données que vous avez créé lors de la session pratique précédente et répétez la commande d'ingestion des données jusqu'à ce que vous voyiez la sortie suivante :

    ```bash 
    Processing /data/wis2box/data-ingest-exercises/synop_202412030900.txt
    Done
    ```

Accédez à la console MinIO dans votre navigateur et vérifiez si le fichier `synop_202412030900.txt` a été téléchargé dans le bucket `wis2box-incoming`. Vous devriez voir un nouveau répertoire portant le nom du jeu de données que vous avez fourni dans l'option `--metadata-id`, et à l'intérieur de ce répertoire, vous trouverez le fichier `synop_202412030900.txt` :

<img alt="minio-wis2box-incoming-dataset-folder" src="/../assets/img/minio-data-ingest-test-data.png" width="800">

!!! note
    La commande `wis2box data ingest` a téléchargé le fichier dans le bucket `wis2box-incoming` de MinIO dans un répertoire portant le nom de l'identifiant de métadonnées que vous avez fourni.

Accédez au tableau de bord Grafana dans votre navigateur et vérifiez l'état de l'ingestion des données.

!!! question "Vérifiez l'état de l'ingestion des données sur Grafana"
    
    Accédez au tableau de bord Grafana à **http://your-host:3000** et vérifiez l'état de l'ingestion des données dans votre navigateur.
    
    Comment pouvez-vous voir si les données ont été ingérées et publiées avec succès ?

??? success "Cliquez pour révéler la réponse"
    
    Si vous avez ingéré les données avec succès, vous devriez voir ce qui suit :
    
    <img alt="grafana_data_ingest" src="/../assets/img/grafana_data-ingest-test.png" width="400">  
    
    Si ce n'est pas le cas, veuillez vérifier les messages WARNING ou ERROR affichés en bas du tableau de bord et tentez de les résoudre.

!!! question "Vérifiez le broker MQTT pour les notifications WIS2"
    
    Accédez à MQTT Explorer et vérifiez si vous pouvez voir le message de notification WIS2 pour les données que vous venez d'ingérer.
    
    Combien de notifications de données WIS2 ont été publiées par votre wis2box ?
    
    Comment accédez-vous au contenu des données publiées ?

??? success "Cliquez pour révéler la réponse"

    Vous devriez voir 1 notification de données WIS2 publiée par votre wis2box.

    Pour accéder au contenu des données publiées, vous pouvez développer la structure du sujet pour voir les différents niveaux du message jusqu'à atteindre le dernier niveau et examiner le contenu du message.

Le contenu du message contient une section "links" avec une clé "rel" de "canonical" et une clé "href" avec l'URL pour télécharger les données. L'URL sera au format `http://YOUR-HOST/data/...`.

Notez que le format des données est BUFR, et vous aurez besoin d'un analyseur BUFR pour visualiser le contenu des données. Le format BUFR est un format binaire utilisé par les services météorologiques pour échanger des données. Les plugins de données dans wis2box transforment les données en BUFR avant de les publier.

Après avoir terminé cet exercice, quittez le conteneur **wis2box-management** :

```bash
exit
```

## Téléchargement de données via SFTP (Optionnel)

Le service MinIO dans wis2box peut également être accessible via SFTP. Le serveur SFTP pour MinIO est lié au port 8022 sur l’hôte (le port 22 est utilisé pour SSH).

Dans cet exercice, nous allons démontrer comment utiliser WinSCP pour télécharger des données dans MinIO via SFTP.

Vous pouvez configurer une nouvelle connexion WinSCP comme indiqué dans cette capture d'écran :

<img alt="winscp-sftp-connection" src="/../assets/img/winscp-sftp-login.png" width="400">

Les identifiants pour la connexion SFTP sont définis par `WIS2BOX_STORAGE_USERNAME` et `WIS2BOX_STORAGE_PASSWORD` dans votre fichier `wis2box.env` et sont les mêmes que ceux utilisés pour se connecter à l'interface utilisateur de MinIO.

Lorsque vous vous connectez, vous verrez les buckets utilisés par wis2box dans MinIO :

<img alt="winscp-sftp-bucket" src="/../assets/img/winscp-buckets.png" width="600">

Vous pouvez naviguer jusqu'au bucket `wis2box-incoming`, puis jusqu'au dossier de votre jeu de données. Vous verrez les fichiers que vous avez téléchargés dans les exercices précédents :

<img alt="winscp-sftp-incoming-path" src="/../assets/img/winscp-incoming-data-path.png" width="600">

!!! question "Télécharger des données via SFTP"

    Téléchargez ce fichier d'exemple sur votre ordinateur local :

    [synop_202503030900.txt](./../sample-data/synop_202503030900.txt) (cliquez avec le bouton droit et sélectionnez "enregistrer sous" pour télécharger le fichier).

    Ensuite, téléchargez-le dans le chemin du jeu de données entrant dans MinIO en utilisant votre session SFTP dans WinSCP.

    Vérifiez le tableau de bord Grafana et MQTT Explorer pour voir si les données ont été ingérées et publiées avec succès.

??? success "Cliquez pour révéler la réponse"

    Vous devriez voir une nouvelle notification de données WIS2 publiée pour la station de test `0-20000-0-64400`, indiquant que les données ont été ingérées et publiées avec succès.

    <img alt="grafana_data_ingest" src="/../assets/img/grafana_data-ingest-test3.png" width="400"> 

    Si vous utilisez le mauvais chemin, vous verrez un message d'erreur dans les journaux.

## Téléchargement de données via un script Python (Optionnel)

Dans cet exercice, nous allons utiliser le client Python de MinIO pour copier des données dans MinIO.

MinIO fournit un client Python, qui peut être installé comme suit :

```bash
pip3 install minio
```

Sur votre machine virtuelle étudiante, le package 'minio' pour Python sera déjà installé.

Dans le répertoire `exercise-materials/data-ingest-exercises`, vous trouverez un script d'exemple `copy_file_to_incoming.py` qui peut être utilisé pour copier des fichiers dans MinIO.

Essayez d'exécuter le script pour copier le fichier de données d'exemple `synop_202501030900.txt` dans le bucket `wis2box-incoming` dans MinIO comme suit :

```bash
cd ~/wis2box-data/data-ingest-exercises
python3 copy_file_to_incoming.py synop_202501030900.txt
```

!!! note

    Vous obtiendrez une erreur car le script n'est pas configuré pour accéder au point de terminaison MinIO sur votre wis2box.

Le script doit connaître le point de terminaison correct pour accéder à MinIO sur votre wis2box. Si wis2box s'exécute sur votre hôte, le point de terminaison MinIO est disponible à `http://YOUR-HOST:9000`. Le script doit également être mis à jour avec votre mot de passe de stockage et le chemin dans le bucket MinIO pour stocker les données.

!!! question "Mettre à jour le script et ingérer les données CSV"
    
    Modifiez le script `copy_file_to_incoming.py` pour résoudre les erreurs, en utilisant l'une des méthodes suivantes :
    - Depuis la ligne de commande : utilisez l'éditeur de texte `nano` ou `vim` pour modifier le script.
    - En utilisant WinSCP : démarrez une nouvelle connexion en utilisant le protocole de fichier `SCP` et les mêmes identifiants que votre client SSH. Naviguez dans le répertoire `wis2box-data/data-ingest-exercises` et modifiez `copy_file_to_incoming.py` en utilisant l'éditeur de texte intégré.
    
    Assurez-vous de :

    - Définir le point de terminaison MinIO correct pour votre hôte.
    - Fournir le mot de passe de stockage correct pour votre instance MinIO.
    - Fournir le chemin correct dans le bucket MinIO pour stocker les données.

    Réexécutez le script pour ingérer le fichier de données d'exemple `synop_202501030900.txt` dans MinIO :

    ```bash
    python3 ~/wis2box-data/ ~/wis2box-data/synop_202501030900.txt
    ```

    Assurez-vous que les erreurs sont résolues.

Une fois que vous parvenez à exécuter le script avec succès, vous verrez un message indiquant que le fichier a été copié dans MinIO, et vous devriez voir des notifications de données publiées par votre instance wis2box dans MQTT Explorer.

Vous pouvez également vérifier le tableau de bord Grafana pour voir si les données ont été ingérées et publiées avec succès.

Maintenant que le script fonctionne, vous pouvez essayer de copier d'autres fichiers dans MinIO en utilisant le même script.

!!! question "Ingérer des données binaires au format BUFR"

    Exécutez la commande suivante pour copier le fichier de données binaires `bufr-example.bin` dans le bucket `wis2box-incoming` dans MinIO :

    ```bash
    python3 copy_file_to_incoming.py bufr-example.bin
    ```

Vérifiez le tableau de bord Grafana et MQTT Explorer pour voir si les données de test ont été ingérées et publiées avec succès. Si vous voyez des erreurs, essayez de les résoudre.

!!! question "Vérifier l'ingestion des données"

    Combien de messages ont été publiés sur le broker MQTT pour cet échantillon de données ?

??? success "Cliquez pour révéler la réponse"

    Vous verrez des erreurs signalées dans Grafana car les stations dans le fichier BUFR ne sont pas définies dans la liste des stations de votre instance wis2box. 
    
    Si toutes les stations utilisées dans le fichier BUFR sont définies dans votre instance wis2box, vous devriez voir 10 messages publiés sur le broker MQTT. Chaque notification correspond à des données pour une station et un horodatage d'observation.

    Le plugin `wis2box.data.bufr4.ObservationDataBUFR` divise le fichier BUFR en messages BUFR individuels et publie un message pour chaque station et horodatage d'observation.

## Téléchargement de données via l'interface web MinIO 

Dans les trois premières méthodes d'ingestion, nous avons utilisé de manière cohérente le jeu de données basé sur les stations (synop) et ses données d'observation associées. Dans cette section, nous introduirons une quatrième méthode — l'une des approches les plus couramment utilisées. Ici, nous travaillerons avec un autre jeu de données et ingérerons des données GEPS en utilisant l'interface web MinIO, qui permet de télécharger et de téléverser des données directement via un navigateur web.

### Connexion à l'interface web MinIO

Ouvrez l'interface web MinIO (généralement disponible à http://localhost:9001).

Les identifiants WIS2BOX_STORAGE_USERNAME et WIS2BOX_STORAGE_PASSWORD peuvent être trouvés dans le fichier wis2box.env.

### Naviguer jusqu'au bucket wis2box-incoming

Sélectionnez le bucket wis2box-incoming et cliquez sur Créer un nouveau chemin.
Le nom du répertoire doit correspondre à l'identifiant de métadonnées de votre jeu de données.
Pour cette formation, nous utilisons le jeu de données GEPS précédemment créé, donc créez le répertoire :

```bash
urn:wmo:md:nl-knmi-test:customized-geps-dataset-wis2-training
```

### Téléverser les fichiers de données GEPS

Entrez dans le répertoire nouvellement créé, cliquez sur Téléverser, et sélectionnez les fichiers de données GEPS locaux à téléverser.

<img alt="minio-incoming-path" src="/../assets/img/minio-incoming-data-GEPS.png" width="800">

### Vérifier le succès du téléversement avec MQTT Explorer

Après le téléversement, vérifiez avec MQTT Explorer pour confirmer que les données ont été publiées avec succès.

Si ce n'est pas le cas, veuillez vérifier les points suivants :

1. Vérifiez quel plugin a été configuré pour le jeu de données GEPS. Une incompatibilité entre le nom de fichier et l'expression régulière configurée peut empêcher l'ingestion. Ajustez l'expression régulière ou renommez les fichiers de données pour qu'ils correspondent.

2. Redémarrez wis2box et répétez le processus de téléversement.

Une fois les données publiées avec succès, vous verrez un message de confirmation similaire au suivant :

<img alt="minio-incoming-path" src="/../assets/img/minio-incoming-data-path-publish.png" width="800">

!!! question "Re-téléverser des données via l'interface web MinIO"

    Accédez à l'interface web MinIO dans votre navigateur et parcourez le bucket `wis2box-incoming`. Vous verrez le fichier `Z_NAFP_C_BABJ_20250818000000_P_CMA-GEPS-GLB-024` que vous avez téléversé dans les exercices précédents.

    Cliquez sur le fichier, et vous aurez l'option de le télécharger :

    <img alt="minio-wis2box-incoming-dataset-folder" src="/../assets/img/minio-download.png" width="800">

    Vous pouvez télécharger ce fichier et le re-téléverser dans le même chemin dans MinIO pour relancer le workflow wis2box.

Vérifiez le tableau de bord Grafana et MQTT Explorer pour voir si les données ont été correctement ingérées et publiées.

??? success "Cliquez pour révéler la réponse"

    Vous verrez un message indiquant que le wis2box a déjà publié ces données :

    ```bash
    ERROR - Data already published for Z_NAFP_C_BABJ_20250818000000_P_CMA-GEPS-GLB-024-grib2; not publishing
    ``` 
    
    Cela démontre que le flux de travail des données a été déclenché, mais que les données n'ont pas été re-publiées. Le wis2box ne publiera pas les mêmes données deux fois.

Pour **un autre** jeu de données :

## Conclusion

!!! success "Félicitations !"
    Au cours de cette session pratique, vous avez appris à :

    - Déclencher le flux de travail du wis2box en téléchargeant des données sur MinIO en utilisant diverses méthodes.
    - Déboguer les erreurs courantes dans le processus d'ingestion des données à l'aide du tableau de bord Grafana et des journaux de votre instance wis2box.
    - Surveiller les notifications de données WIS2 publiées par votre wis2box dans le tableau de bord Grafana et MQTT Explorer.
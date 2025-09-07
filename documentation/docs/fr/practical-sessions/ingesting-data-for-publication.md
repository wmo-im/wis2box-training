---
title: Ingestion des données pour publication
---

# Ingestion des données pour publication

!!! abstract "Objectifs d'apprentissage"

    À la fin de cette session pratique, vous serez capable de :
    
    - Déclencher le workflow de wis2box en téléchargeant des données dans MinIO via l'interface web de MinIO, SFTP ou un script Python.
    - Accéder au tableau de bord Grafana pour surveiller l'état de l'ingestion des données et consulter les journaux de votre instance wis2box.
    - Visualiser les notifications de données WIS2 publiées par votre wis2box à l'aide de MQTT Explorer.

## Introduction

Dans WIS2, les données sont partagées en temps réel via des notifications de données WIS2 contenant un lien "canonique" à partir duquel les données peuvent être téléchargées.

Pour déclencher le workflow des données dans un WIS2 Node en utilisant le logiciel wis2box, les données doivent être téléchargées dans le bucket **wis2box-incoming** de **MinIO**, ce qui initie le workflow de wis2box. Ce processus aboutit à la publication des données via une notification de données WIS2. Selon les mappages de données configurés dans votre instance wis2box, les données peuvent être transformées au format BUFR avant leur publication.

Dans cet exercice, nous utiliserons des fichiers de données d'exemple pour déclencher le workflow de wis2box et **publier des notifications de données WIS2** pour l'ensemble de données que vous avez configuré lors de la session pratique précédente.

Pendant l'exercice, nous surveillerons l'état de l'ingestion des données à l'aide du **tableau de bord Grafana** et de **MQTT Explorer**. Le tableau de bord Grafana utilise les données de Prometheus et Loki pour afficher l'état de votre wis2box, tandis que MQTT Explorer vous permet de visualiser les notifications de données WIS2 publiées par votre instance wis2box.

Pour cet exercice, nous nous concentrerons sur les différentes méthodes pour télécharger des données dans votre instance wis2box et vérifier la réussite de l'ingestion et de la publication. La transformation des données sera abordée plus tard dans la session pratique [Outils de conversion de données](./data-conversion-tools.md).

## Préparation

Cette section utilise l'ensemble de données pour "surface-based-observations/synop" et "other" précédemment créé dans la session pratique [Configuration des ensembles de données dans wis2box](./configuring-wis2box-datasets.md).

Elle nécessite également des connaissances sur la configuration des stations dans le **wis2box-webapp**, comme décrit dans la session pratique [Configuration des métadonnées des stations](./configuring-station-metadata.md).

Assurez-vous de pouvoir vous connecter à votre VM étudiant en utilisant votre client SSH (par exemple, PuTTY).

Assurez-vous que wis2box est opérationnel :

```bash
cd ~/wis2box/
python3 wis2box-ctl.py start
python3 wis2box-ctl.py status
```

Assurez-vous que MQTT Explorer est en cours d'exécution et connecté à votre instance en utilisant les identifiants publics `everyone/everyone` avec un abonnement au sujet `origin/a/wis2/#`.

Assurez-vous d'avoir un navigateur web ouvert avec le tableau de bord Grafana pour votre instance en naviguant vers `http://YOUR-HOST:3000`.

## Ingestion des données via l'interface MinIO

Tout d'abord, nous utiliserons l'interface web de MinIO, qui vous permet de télécharger et d'envoyer des données vers MinIO à l'aide d'un navigateur web.

### Accéder à l'interface MinIO

Ouvrez l'interface web de MinIO, généralement disponible à l'adresse `http://YOUR-HOST:9001`.

<img alt="Minio UI: minio ui" src="/../assets/img/minio-ui.png" width="400">

Les identifiants WIS2BOX_STORAGE_USERNAME et WIS2BOX_STORAGE_PASSWORD se trouvent dans le fichier wis2box.env.

Si vous n'êtes pas sûr des valeurs, veuillez naviguer jusqu'au répertoire racine de votre wis2box et exécuter la commande suivante pour afficher uniquement les identifiants pertinents :

```bash
grep -E '^(WIS2BOX_STORAGE_USERNAME|WIS2BOX_STORAGE_PASSWORD)=' wis2box.env
```
Utilisez les valeurs de WIS2BOX_STORAGE_USERNAME et WIS2BOX_STORAGE_PASSWORD comme nom d'utilisateur et mot de passe lors de la connexion à MinIO.

### Ingestion et publication à l'aide du plugin Universal

Téléchargez les données d'exemple geps [geps_202508180000.grib2](../sample-data/geps_202508180000.grib2) dans votre environnement local :

Sélectionnez le bucket wis2box-incoming et cliquez sur `Create new path`.

<img alt="minio ui: create new path" src="/../assets/img/minio-create-new-path.png" width="800">

Le nom du chemin doit correspondre à l'identifiant des métadonnées de votre ensemble de données "other", que vous avez précédemment créé dans la session pratique [Configuration des ensembles de données dans wis2box](./configuring-wis2box-datasets.md).

<img alt="minio ui: create new path empty" src="/../assets/img/minio-ui-create-path-empty.png" width="700">

Dans ce cas, veuillez créer le répertoire suivant :

```bash
urn:wmo:md:my-centre-id:my-other-dataset
```

Entrez dans le répertoire nouvellement créé, cliquez sur `Upload`, trouvez le fichier [geps_202508180000.grib2](../sample-data/geps_202508180000.grib2) que vous avez téléchargé sur votre machine locale et téléchargez ce fichier dans le bucket wis2box-incoming.

<img alt="minio ui: upload your file" src="/../assets/img/minio-other-dataset-upload.png" width="650">

Une fois le téléchargement terminé, vous verrez ce fichier dans le bucket wis2box-incoming de MinIO :

<img alt="minio ui: upload your file" src="/../assets/img/minio-geps-file-upload.png" width="650">

Après le téléchargement, vérifiez avec MQTT Explorer pour confirmer que les données ont été publiées avec succès.

<img alt="Metadata Editor: title, description, keywords" src="/../assets/img/mqtt-explorer-wis2-notification-geps-sample.png" width="800">

Ensuite, téléchargez les données d'exemple geps dans une autre extension de fichier [geps_202508180000.nc](../sample-data/geps_202508180000.nc) dans votre environnement local. Téléchargez ce fichier dans le même répertoire que lors de l'exercice précédent.

!!! question "Question"

    Pouvez-vous télécharger avec succès dans le bucket wis2box-incoming ?

??? success "Cliquez pour révéler la réponse"

    Oui.
    <img alt="Minio ui: geps nc file" src="/../assets/img/minio-upload-geps-with-nc-extension.png" width="800">

!!! question "Question"

    Pouvez-vous publier avec succès des messages de notification de données via MinIO ? 
    Consultez le tableau de bord Grafana et MQTT Explorer pour vérifier si les données ont été ingérées et publiées avec succès.

!!! hint

    Lors de la création d'un ensemble de données personnalisé, quel plugin avez-vous utilisé ?
    Le plugin impose-t-il des exigences sur le format de fichier, et où sont-elles spécifiées ?

??? success "Cliquez pour révéler la réponse"

    Non.
    Vous verrez un message indiquant qu'il y a une erreur de type de fichier inconnu.

    ```bash
    ERROR - Path validation error: Unknown file type (nc) for metadata_id=urn:wmo:md:nl-knmi-test:customized-geps-dataset-wis2-training. Did not match any of the following:grib2
    ``` 
    
    Cela montre que le workflow des données a été déclenché, mais que les données n'ont pas été re-publiées. Le wis2box ne publiera pas les données si elles ne correspondent pas à l'extension de fichier grib2.

Ensuite, téléchargez les données d'exemple geps renommées [geps_renamed_sample_data.grib2](../sample-data/geps_renamed_sample_data.grib2) dans votre environnement local. Téléchargez ce fichier dans le même répertoire que lors des deux exercices précédents.

!!! question "Question"

    Pouvez-vous télécharger avec succès dans le bucket wis2box-incoming ?

??? success "Cliquez pour révéler la réponse"

    Oui.
    <img alt="Minio ui: geps nc file" src="/../assets/img/minio-upload-renamed-geps.png" width="800">

!!! question "Question"

    Pouvez-vous publier avec succès des messages de notification de données via MinIO ? 
    Consultez le tableau de bord Grafana et MQTT Explorer pour vérifier si les données ont été ingérées et publiées avec succès.

!!! hint

    Le plugin personnalisé que vous avez utilisé impose-t-il des exigences ou des restrictions sur le nom de fichier ?

??? success "Cliquez pour révéler la réponse"

    Non.
    Vous verrez un message indiquant qu'il y a une erreur concernant le fait que les données ne correspondent pas à l'expression régulière.

    ```bash
    ERROR - ERROR - geps_renamed_sample_data.grib2 did not match ^.*?_(\d{8}).*?\..*$
    ``` 
    
    Cela montre que le workflow des données a été déclenché, mais que les données n'ont pas été re-publiées. Le wis2box ne publiera pas les données si elles ne correspondent pas au modèle de fichier ^.*?_(\d{8}).*?\..*$.

Le plugin Universal fournit un mécanisme générique pour ingérer et publier des fichiers sans appliquer de décodage spécifique au domaine. Au lieu de cela, il effectue un ensemble de vérifications de base avant de publier une notification WIS2 :

`Extension de fichier` – le fichier doit utiliser l'extension autorisée par la configuration de l'ensemble de données.

`Modèle de nom de fichier` – le nom du fichier doit correspondre à l'expression régulière définie dans l'ensemble de données.

Si ces deux conditions sont remplies, le fichier est ingéré et une notification est publiée.

Télécharger un fichier sur MinIO réussit toujours tant que l'utilisateur y a accès. Cependant, publier une notification de données WIS2 nécessite une validation plus stricte. Les fichiers qui ne respectent pas les règles d'extension ou de nom de fichier seront stockés dans le bucket `incoming`, mais le `Universal plugin` ne publiera pas de notification pour eux. Cela explique pourquoi des fichiers avec une extension non prise en charge (par exemple, `geps_202508180000.nc`) ou avec un nom de fichier invalide (par exemple, `geps_renamed_sample_data.grib2`) sont acceptés par MinIO mais n'apparaissent pas dans WIS2.

Ensuite, accédez à l'interface web de MinIO dans votre navigateur et parcourez le bucket `wis2box-incoming`. Vous verrez le fichier `geps_202508180000.grib2` que vous avez téléchargé dans les exercices précédents.

Cliquez sur le fichier, et vous aurez la possibilité de le télécharger :

<img alt="minio-wis2box-incoming-dataset-folder" src="/../assets/img/minio-download.png" width="800">

Veuillez télécharger ce fichier et le re-téléverser au même emplacement dans MinIO pour relancer le workflow de wis2box.

!!! question "Question"

    Pouvez-vous republier avec succès des messages de notification de données via MinIO ? 
    Vérifiez le tableau de bord Grafana et MQTT Explorer pour voir si les données ont été ingérées et publiées avec succès.

??? success "Cliquez pour révéler la réponse"

    Vous verrez un message indiquant que wis2box a déjà publié ces données :

    ```bash
    ERROR - Data already published for geps_202508180000-grib2; not publishing
    ``` 
    
    Cela démontre que le workflow des données a été déclenché, mais que les données n'ont pas été republées. Wis2box ne publiera pas les mêmes données deux fois.

### Ingérer et publier avec le plugin synop2bufr

Téléchargez les données d'exemple synop [synop_202502040900.txt](../sample-data/synop_202502040900.txt) pour cet exercice dans votre environnement local :

Comme dans les exercices précédents, créez un répertoire sous le bucket `wis2box-incoming` correspondant à l'identifiant de métadonnées de votre jeu de données surface-based-observations/synop.

Entrez dans le répertoire nouvellement créé, cliquez sur `Upload`, et sélectionnez le fichier [synop_202502040900.txt](../sample-data/synop_202502040900.txt) que vous avez téléchargé sur votre machine locale, puis téléversez-le.

!!! question "Question"

    Pouvez-vous publier avec succès des messages de notification de données via MinIO ? 
    Vérifiez le tableau de bord Grafana et MQTT Explorer pour voir si les données ont été ingérées et publiées avec succès.

??? success "Cliquez pour révéler la réponse"

    Non. 
    Dans le tableau de bord Grafana, vous verrez un avertissement indiquant l'absence de l'enregistrement de la station 64400 :

    ```bash
    WARNING - Station 64400 not found in station file
    ``` 
    
    Cela démontre que le workflow des données a été déclenché, mais qu'une métadonnée spécifique de station est nécessaire.

Dans ce cas, vous utilisez le plugin `FM-12 data converted to BUFR`.

L'objectif de ce plugin est de traiter les données FM-12 fournies au format texte brut et de les convertir en format binaire BUFR. 
Pendant ce processus, le plugin doit analyser et mapper les informations de station contenues dans les données.

Si les métadonnées essentielles de la station sont manquantes, le plugin ne pourra pas analyser correctement le fichier et la conversion échouera.

Par conséquent, vous devez vous assurer que les métadonnées pertinentes de la station ont été ajoutées à wis2box avant de publier les données SYNOP.

Ajoutons maintenant une station de test pour cet exercice.

Ajoutez la station avec l'identifiant WIGOS `0-20000-0-64400` à votre instance wis2box en utilisant l'éditeur de stations dans le wis2box-webapp.

Récupérez la station depuis OSCAR :

<img alt="oscar-station" src="/../assets/img/webapp-test-station-oscar-search.png" width="600">

Ajoutez la station aux jeux de données que vous avez créés pour la publication sur "../surface-based-observations/synop" et enregistrez les modifications en utilisant votre jeton d'authentification :

<img alt="webapp-test-station" src="/../assets/img/webapp-test-station-save.png" width="800">

Notez que vous pouvez supprimer cette station de votre jeu de données après la session pratique.

Après avoir terminé la configuration des métadonnées de la station, vérifiez avec MQTT Explorer pour confirmer que les données ont été publiées avec succès. Si vous voyez la notification ci-dessous, alors vous avez publié avec succès les données d'exemple synop.

<img alt="webapp-test-station" src="/../assets/img/mqtt-explorer-wis2box-notification-synop-sample.png" width="800">

## Ingérer des données avec Python (optionnel)

Dans cet exercice, nous utiliserons le client Python de MinIO pour copier des données dans MinIO.

MinIO fournit un client Python, qui peut être installé comme suit :

```bash
pip3 install minio
```

Sur votre machine virtuelle étudiante, le package 'minio' pour Python sera déjà installé.

Copiez le répertoire `exercise-materials/data-ingest-exercises` dans le répertoire que vous avez défini comme `WIS2BOX_HOST_DATADIR` dans votre fichier `wis2box.env` :

```bash
cp -r ~/exercise-materials/data-ingest-exercises ~/wis2box-data/
```

!!! note
    Le `WIS2BOX_HOST_DATADIR` est monté en tant que `/data/wis2box/` dans le conteneur wis2box-management par le fichier `docker-compose.yml` inclus dans le répertoire `wis2box`.
    
    Cela vous permet de partager des données entre l'hôte et le conteneur.

Dans le répertoire `exercise-materials/data-ingest-exercises`, vous trouverez un script d'exemple `copy_file_to_incoming.py` qui peut être utilisé pour copier des fichiers dans MinIO.

Essayez d'exécuter le script pour copier le fichier de données d'exemple `synop_202501030900.txt` dans le bucket `wis2box-incoming` de MinIO comme suit :

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

    Relancez le script pour ingérer le fichier de données d'exemple `synop_202501030900.txt` dans MinIO :

    ```bash
    python3 ~/wis2box-data/data-ingest-exercises/copy_file_to_incoming.py synop_202501030900.txt
    ```

    Assurez-vous que les erreurs sont résolues.

Une fois que vous parvenez à exécuter le script avec succès, vous verrez un message indiquant que le fichier a été copié dans MinIO, et vous devriez voir des notifications de données publiées par votre instance wis2box dans MQTT Explorer.

Vous pouvez également vérifier le tableau de bord Grafana pour voir si les données ont été ingérées et publiées avec succès.

Maintenant que le script fonctionne, vous pouvez essayer de copier d'autres fichiers dans MinIO en utilisant le même script.

!!! question "Ingérer des données binaires au format BUFR"

    Exécutez la commande suivante pour copier le fichier de données binaires `bufr-example.bin` dans le bucket `wis2box-incoming` de MinIO :

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

## Ingérer des données via SFTP (optionnel)

Le service MinIO dans wis2box peut également être accessible via SFTP. Le serveur SFTP pour MinIO est lié au port 8022 sur l'hôte (le port 22 est utilisé pour SSH).

Dans cet exercice, nous allons démontrer comment utiliser WinSCP pour téléverser des données vers MinIO en utilisant SFTP.

Vous pouvez configurer une nouvelle connexion WinSCP comme indiqué dans cette capture d'écran :

<img alt="winscp-sftp-connection" src="/../assets/img/winscp-sftp-login.png" width="400">

Les identifiants pour la connexion SFTP sont définis par `WIS2BOX_STORAGE_USERNAME` et `WIS2BOX_STORAGE_PASSWORD` dans votre fichier `wis2box.env` et sont les mêmes que ceux utilisés pour vous connecter à l'interface utilisateur de MinIO.

Lorsque vous vous connectez, vous verrez les buckets utilisés par wis2box dans MinIO :

<img alt="winscp-sftp-bucket" src="/../assets/img/winscp-buckets.png" width="600">

Vous pouvez naviguer jusqu'au bucket `wis2box-incoming`, puis dans le dossier correspondant à votre jeu de données. Vous verrez les fichiers que vous avez téléchargés lors des exercices précédents :

<img alt="winscp-sftp-incoming-path" src="/../assets/img/winscp-incoming-data-path.png" width="600">

!!! question "Télécharger des données via SFTP"

    Téléchargez ce fichier exemple sur votre ordinateur local :

    [synop_202503030900.txt](./../sample-data/synop_202503030900.txt) (cliquez avec le bouton droit et sélectionnez "enregistrer sous" pour télécharger le fichier).

    Ensuite, téléversez-le dans le chemin du jeu de données incoming dans MinIO en utilisant votre session SFTP dans WinSCP.

    Vérifiez le tableau de bord Grafana et MQTT Explorer pour voir si les données ont été correctement ingérées et publiées.

??? success "Cliquez pour révéler la réponse"

    Vous devriez voir une nouvelle notification de données WIS2 publiée pour la station de test `0-20000-0-64400`, indiquant que les données ont été correctement ingérées et publiées.

    <img alt="grafana_data_ingest" src="/../assets/img/grafana_data-ingest-test3.png" width="400"> 

    Si vous utilisez un chemin incorrect, vous verrez un message d'erreur dans les journaux.

## Conclusion

!!! success "Félicitations !"
    Au cours de cette session pratique, vous avez appris à :

    - Déclencher le workflow de wis2box en téléversant des données dans MinIO à l'aide de différentes méthodes.
    - Déboguer les erreurs courantes dans le processus d'ingestion des données en utilisant le tableau de bord Grafana et les journaux de votre instance wis2box.
    - Surveiller les notifications de données WIS2 publiées par votre wis2box dans le tableau de bord Grafana et MQTT Explorer.
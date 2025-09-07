---
title: Ingestion des données pour publication
---

# Ingestion des données pour publication

!!! abstract "Objectifs d'apprentissage"

    À la fin de cette session pratique, vous serez capable de :
    
    - Déclencher le workflow de wis2box en téléchargeant des données sur MinIO via l'interface web de MinIO, SFTP ou un script Python.
    - Accéder au tableau de bord Grafana pour surveiller l'état de l'ingestion des données et consulter les journaux de votre instance wis2box.
    - Visualiser les notifications de données WIS2 publiées par votre wis2box à l'aide de MQTT Explorer.

## Introduction

Dans WIS2, les données sont partagées en temps réel via des notifications de données WIS2 contenant un lien "canonique" à partir duquel les données peuvent être téléchargées.

Pour déclencher le workflow de données dans un WIS2 Node à l'aide du logiciel wis2box, les données doivent être téléchargées dans le bucket **wis2box-incoming** de **MinIO**, ce qui initie le workflow de wis2box. Ce processus aboutit à la publication des données via une notification de données WIS2. Selon les mappages de données configurés dans votre instance wis2box, les données peuvent être transformées au format BUFR avant leur publication.

Dans cet exercice, nous utiliserons des fichiers de données d'exemple pour déclencher le workflow de wis2box et **publier des notifications de données WIS2** pour l'ensemble de données que vous avez configuré lors de la session pratique précédente.

Pendant l'exercice, nous surveillerons l'état de l'ingestion des données à l'aide du **tableau de bord Grafana** et de **MQTT Explorer**. Le tableau de bord Grafana utilise des données de Prometheus et Loki pour afficher l'état de votre wis2box, tandis que MQTT Explorer vous permet de voir les notifications de données WIS2 publiées par votre instance wis2box.

Notez que wis2box transformera les données d'exemple au format BUFR avant de les publier sur le broker MQTT, conformément aux mappages de données préconfigurés dans votre ensemble de données. Pour cet exercice, nous nous concentrerons sur les différentes méthodes de téléchargement des données dans votre instance wis2box et sur la vérification de l'ingestion et de la publication réussies. La transformation des données sera abordée plus tard dans la session pratique [Outils de conversion de données](./data-conversion-tools.md).

## Préparation

Cette section utilise l'ensemble de données "surface-based-observations/synop" et "other" précédemment créé dans la session pratique [Configuration des ensembles de données dans wis2box](./configuring-wis2box-datasets.md).

Elle nécessite également des connaissances sur la configuration des stations dans le **wis2box-webapp**, comme décrit dans la session pratique [Configuration des métadonnées des stations](./configuring-station-metadata.md).

Assurez-vous de pouvoir vous connecter à votre VM étudiant à l'aide de votre client SSH (par exemple, PuTTY).

Assurez-vous que wis2box est opérationnel :

```bash
cd ~/wis2box/
python3 wis2box-ctl.py start
python3 wis2box-ctl.py status
```

Assurez-vous que MQTT Explorer est en cours d'exécution et connecté à votre instance en utilisant les identifiants publics `everyone/everyone` avec un abonnement au sujet `origin/a/wis2/#`.

Assurez-vous d'avoir un navigateur web ouvert avec le tableau de bord Grafana de votre instance en naviguant vers `http://YOUR-HOST:3000`.

### Préparer les données d'exemple

Copiez le répertoire `exercise-materials/data-ingest-exercises` dans le répertoire que vous avez défini comme `WIS2BOX_HOST_DATADIR` dans votre fichier `wis2box.env` :

```bash
cp -r ~/exercise-materials/data-ingest-exercises ~/wis2box-data/
```

!!! note
    Le `WIS2BOX_HOST_DATADIR` est monté en tant que `/data/wis2box/` dans le conteneur wis2box-management par le fichier `docker-compose.yml` inclus dans le répertoire `wis2box`.
    
    Cela permet de partager des données entre l'hôte et le conteneur.

## Ingestion des données via l'interface MinIO

Tout d'abord, nous utiliserons l'interface web de MinIO, qui vous permet de télécharger et téléverser des données sur MinIO à l'aide d'un navigateur web.

### Accéder à l'interface MinIO

Ouvrez l'interface web de MinIO (généralement disponible à http://your-localhost:9001).

Les identifiants WIS2BOX_STORAGE_USERNAME et WIS2BOX_STORAGE_PASSWORD peuvent être trouvés dans le fichier wis2box.env.

### Ingestion et publication à l'aide du plugin Universal

Téléchargez les données d'exemple universelles pour cet exercice depuis le lien ci-dessous dans votre environnement local :  
[sample-data-for-universal-plugin](../sample-data/Z_NAFP_C_BABJ_20250818000000_P_CMA-GEPS-GLB-024.grib2)

Sélectionnez le bucket wis2box-incoming et cliquez sur Créer un nouveau chemin. Le nom du répertoire doit correspondre à l'identifiant de métadonnées de votre ensemble de données "other", que vous avez précédemment créé dans la session pratique [Configuration des ensembles de données dans wis2box](./configuring-wis2box-datasets.md). Dans ce cas, veuillez créer le répertoire :

```bash
urn:wmo:md:nl-knmi-test:customized-geps-dataset-wis2-training
```

Entrez dans le répertoire nouvellement créé, cliquez sur "Téléverser", et sélectionnez le fichier [sample-data-for-universal-plugin](../sample-data/Z_NAFP_C_BABJ_20250818000000_P_CMA-GEPS-GLB-024.grib2) que vous avez téléchargé sur votre machine locale.

Après le téléversement, vérifiez avec MQTT Explorer pour confirmer que les données ont été publiées avec succès.

<img alt="Metadata Editor: title, description, keywords" src="/../assets/img/mqtt-explorer-wis2-notification-geps-sample.png" width="800">

!!! question "Renommez le fichier en sample-geps-data.grib2"

    Téléversez le fichier renommé à l'aide de l'interface web dans le même chemin de MinIO que le fichier précédent.

    Le fichier renommé sera-t-il publié avec succès ? Pourquoi ou pourquoi pas ?

??? success "Cliquez pour révéler la réponse"

    Non, car lorsque vous changez le nom des données en "sample-geps-data.grib2", il ne respectera pas la règle regex.

    <img alt="Metadata Editor: title, description, keywords" src="/../assets/img/mqtt-explorer-wis2-notification-geps-regex-error.png" width="800">
    
    Lors du téléversement des données, les noms de fichiers doivent respecter la convention de nommage requise définie par une expression régulière :

    ```bash
    ^.*?_(\d{8}).*?\..*$
    ```

    Ce modèle impose que chaque nom de fichier contienne :

    Un underscore (_), suivi immédiatement par une chaîne de date à 8 chiffres au format AAAAMMJJ (par exemple, 20250904).

    Par exemple, les noms suivants sont valides :

    1. *Z_NAFP_C_BABJ_20250904_P_CMA-GEPS-GLB-024.grib2*

    2. *forecast_20250904.grib2*

    3. *sample-geps_20250101_data.grib2*

    Un nom tel que sample-geps-data.grib2 ne sera pas accepté, car il ne contient pas la date à 8 chiffres requise.

!!! question "Renommez l'extension du fichier de .grib2 à .bufr4 (sans modifier le contenu interne du fichier)"

    Téléversez le fichier renommé à l'aide de l'interface web dans le même chemin de MinIO que le fichier précédent.

    Le fichier renommé sera-t-il publié avec succès ? Pourquoi ou pourquoi pas ?

??? success "Cliquez pour révéler la réponse"

    Non, car lorsque vous changez le format des données de "grib2" à "bufr4", il ne respectera pas la règle d'extension de fichier que vous avez définie lors de la création de cet ensemble de données.

    <img alt="Metadata Editor: title, description, keywords" src="/../assets/img/mqtt-explorer-wis2-notification-geps-file-extension-error.png" width="800">
    
    Lors du téléversement des données à l'aide du plugin Universal, le fichier doit avoir la bonne extension de fichier telle que définie dans la configuration de l'ensemble de données. Cette exigence garantit que le processus d'ingestion peut reconnaître et traiter correctement le format de fichier. Par exemple, si l'ensemble de données est configuré pour des fichiers grib2, seuls les fichiers se terminant par .grib2 seront acceptés. L'utilisation d'une extension incorrecte (par exemple, .txt ou .bin) entraînera le rejet du fichier et sa non-publication.

!!! question "Re-téléversez les données à l'aide de l'interface web de MinIO"

    Accédez à l'interface web de MinIO dans votre navigateur et parcourez le bucket `wis2box-incoming`. Vous verrez le fichier `Z_NAFP_C_BABJ_20250818000000_P_CMA-GEPS-GLB-024.grib2` que vous avez téléversé dans les exercices précédents.

    Cliquez sur le fichier, et vous aurez l'option de le télécharger :

    <img alt="minio-wis2box-incoming-dataset-folder" src="/../assets/img/minio-download.png" width="800">

    Vous pouvez télécharger ce fichier et le re-téléverser dans le même chemin de MinIO pour relancer le workflow de wis2box.

    Vérifiez le tableau de bord Grafana et MQTT Explorer pour voir si les données ont été ingérées et publiées avec succès.

??? success "Cliquez pour révéler la réponse"

    Vous verrez un message indiquant que wis2box a déjà publié ces données :

    ```bash
    ERROR - Data already published for Z_NAFP_C_BABJ_20250818000000_P_CMA-GEPS-GLB-024-grib2; not publishing
    ``` 
    
    Cela démontre que le workflow de données a été déclenché, mais que les données n'ont pas été publiées à nouveau. Wis2box ne publiera pas les mêmes données deux fois.

### Ingestion et publication à l'aide du plugin synop2bufr-plugin

Téléchargez les données d'exemple synop [synop_202502040900.txt](../sample-data/synop_202502040900.txt) pour cet exercice depuis le lien ci-dessous dans votre environnement local :

Sélectionnez le bucket wis2box-incoming et cliquez sur Créer un nouveau chemin. Le nom du répertoire doit correspondre à l'Identifiant de Métadonnées de votre jeu de données "surface-based-observations/synop", que vous avez précédemment créé lors de la session pratique [Configuration des jeux de données dans wis2box](./configuring-wis2box-datasets.md). Dans ce cas, veuillez créer le répertoire suivant :

```bash
urn:wmo:md:nl-knmi-test:synop-dataset-wis2-training
```

Entrez dans le répertoire nouvellement créé, cliquez sur "Upload", sélectionnez le fichier [synop_202502040900.txt](../sample-data/synop_202502040900.txt) que vous avez téléchargé sur votre machine locale, puis téléchargez-le.

!!! question "Avez-vous reçu une nouvelle notification indiquant que les données ont été publiées ? Pourquoi ?"

??? success "Cliquez pour révéler la réponse"

    Non. Dans le tableau de bord Grafana, vous verrez une erreur indiquant que l'ingestion a échoué :

    <img alt="grafana_data_ingest" src="/../assets/img/grafana_data-ingest-error.png" width="800"> 

    Lors de l'utilisation du modèle de jeu de données synop avec les plugins synop par défaut (pour les données CSV, TXT et BUFR SYNOP), chaque enregistrement doit inclure un identifiant de station valide. L'ingestion échoue si la station n'est pas connue de votre instance wis2box. Par conséquent, vous devez d'abord ajouter la station avant de publier des données SYNOP.

    Ajoutons donc une station de test pour cet exercice.

    Ajoutez la station avec l'identifiant WIGOS `0-20000-0-64400` à votre instance wis2box à l'aide de l'éditeur de stations dans l'application wis2box-webapp.

    Récupérez la station depuis OSCAR :

    <img alt="oscar-station" src="/../assets/img/webapp-test-station-oscar-search.png" width="600">

    Ajoutez la station aux jeux de données que vous avez créés pour la publication dans "../surface-based-observations/synop" et enregistrez les modifications à l'aide de votre jeton d'authentification :

    <img alt="webapp-test-station" src="/../assets/img/webapp-test-station-save.png" width="800">

    Notez que vous pouvez supprimer cette station de votre jeu de données après la session pratique.

Après avoir terminé la configuration des métadonnées de la station, vérifiez avec MQTT Explorer pour confirmer que les données ont été publiées avec succès. Si vous voyez la notification ci-dessous, cela signifie que vous avez publié les données d'exemple synop avec succès.

<img alt="webapp-test-station" src="/../assets/img/mqtt-explorer-wis2box-notification-synop-sample.png" width="800">

## Ingestion des données avec Python (optionnel)

Dans cet exercice, nous utiliserons le client Python MinIO pour copier des données dans MinIO.

MinIO fournit un client Python, qui peut être installé comme suit :

```bash
pip3 install minio
```

Sur votre machine virtuelle étudiante, le package 'minio' pour Python sera déjà installé.

Dans le répertoire `exercise-materials/data-ingest-exercises`, vous trouverez un script d'exemple `copy_file_to_incoming.py` qui peut être utilisé pour copier des fichiers dans MinIO.

Essayez d'exécuter le script pour copier le fichier de données d'exemple `synop_202501030900.txt` dans le bucket `wis2box-incoming` de MinIO comme suit :

```bash
cd ~/wis2box-data/data-ingest-exercises
python3 copy_file_to_incoming.py synop_202501030900.txt
```

!!! note

    Vous obtiendrez une erreur car le script n'est pas configuré pour accéder au point de terminaison MinIO de votre instance wis2box.

Le script doit connaître le point de terminaison correct pour accéder à MinIO sur votre instance wis2box. Si wis2box s'exécute sur votre hôte, le point de terminaison MinIO est disponible à `http://YOUR-HOST:9000`. Le script doit également être mis à jour avec votre mot de passe de stockage et le chemin dans le bucket MinIO où les données doivent être stockées.

!!! question "Mettre à jour le script et ingérer les données CSV"
    
    Modifiez le script `copy_file_to_incoming.py` pour résoudre les erreurs, en utilisant l'une des méthodes suivantes :
    - Depuis la ligne de commande : utilisez l'éditeur de texte `nano` ou `vim` pour modifier le script.
    - En utilisant WinSCP : démarrez une nouvelle connexion en utilisant le protocole de fichier `SCP` et les mêmes identifiants que votre client SSH. Naviguez dans le répertoire `wis2box-data/data-ingest-exercises` et modifiez `copy_file_to_incoming.py` à l'aide de l'éditeur de texte intégré.
    
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

## Ingestion des données via SFTP (optionnel)

Le service MinIO dans wis2box peut également être accessible via SFTP. Le serveur SFTP pour MinIO est lié au port 8022 sur l'hôte (le port 22 est utilisé pour SSH).

Dans cet exercice, nous allons démontrer comment utiliser WinSCP pour télécharger des données dans MinIO via SFTP.

Vous pouvez configurer une nouvelle connexion WinSCP comme indiqué dans cette capture d'écran :

<img alt="winscp-sftp-connection" src="/../assets/img/winscp-sftp-login.png" width="400">

Les identifiants pour la connexion SFTP sont définis par `WIS2BOX_STORAGE_USERNAME` et `WIS2BOX_STORAGE_PASSWORD` dans votre fichier `wis2box.env` et sont les mêmes que les identifiants que vous avez utilisés pour vous connecter à l'interface utilisateur MinIO.

Lorsque vous vous connectez, vous verrez les buckets utilisés par wis2box dans MinIO :

<img alt="winscp-sftp-bucket" src="/../assets/img/winscp-buckets.png" width="600">

Vous pouvez naviguer jusqu'au bucket `wis2box-incoming`, puis jusqu'au dossier de votre jeu de données. Vous verrez les fichiers que vous avez téléchargés lors des exercices précédents :

<img alt="winscp-sftp-incoming-path" src="/../assets/img/winscp-incoming-data-path.png" width="600">

!!! question "Télécharger des données via SFTP"

    Téléchargez ce fichier d'exemple sur votre ordinateur local :

    [synop_202503030900.txt](./../sample-data/synop_202503030900.txt) (cliquez avec le bouton droit et sélectionnez "enregistrer sous" pour télécharger le fichier).

    Ensuite, téléchargez-le dans le chemin du jeu de données incoming dans MinIO en utilisant votre session SFTP dans WinSCP.

    Vérifiez le tableau de bord Grafana et MQTT Explorer pour voir si les données ont été ingérées et publiées avec succès.

??? success "Cliquez pour révéler la réponse"

    Vous devriez voir une nouvelle notification de données WIS2 publiée pour la station de test `0-20000-0-64400`, indiquant que les données ont été ingérées et publiées avec succès.

    <img alt="grafana_data_ingest" src="/../assets/img/grafana_data-ingest-test3.png" width="400"> 

    Si vous utilisez le mauvais chemin, vous verrez un message d'erreur dans les journaux.

## Conclusion

!!! success "Félicitations !"
    Au cours de cette session pratique, vous avez appris à :

    - Déclencher le workflow wis2box en téléchargeant des données dans MinIO via différentes méthodes.
    - Déboguer les erreurs courantes dans le processus d'ingestion des données en utilisant le tableau de bord Grafana et les journaux de votre instance wis2box.
    - Surveiller les notifications de données WIS2 publiées par votre wis2box dans le tableau de bord Grafana et MQTT Explorer.
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

Pour déclencher le workflow des données dans un WIS2 Node à l'aide du logiciel wis2box, les données doivent être téléchargées dans le bucket **wis2box-incoming** de **MinIO**, ce qui initie le workflow de données de wis2box pour traiter et publier les données.

Pour surveiller l'état du workflow de données de wis2box, vous pouvez utiliser le **tableau de bord Grafana** et **MQTT Explorer**. Le tableau de bord Grafana utilise les données de Prometheus et Loki pour afficher l'état de votre wis2box, tandis que MQTT Explorer vous permet de voir les notifications de données WIS2 publiées par votre instance wis2box.

Dans cette section, nous nous concentrerons sur la manière de télécharger des données dans votre instance wis2box et de vérifier leur ingestion et publication réussies. La transformation des données sera abordée ultérieurement dans la session pratique [Outils de conversion de données](./data-conversion-tools.md).

Pour tester manuellement le processus d'ingestion des données, nous utiliserons l'interface web de MinIO, qui vous permet de télécharger et téléverser des données sur MinIO à l'aide d'un navigateur web.

Dans un environnement de production, les données seraient généralement ingérées à l'aide de processus automatisés, tels que des scripts ou des applications qui transfèrent les données vers MinIO via S3 ou SFTP.

## Préparation

Cette section suppose que vous avez terminé avec succès la session pratique [Configuration des ensembles de données dans wis2box](./configuring-wis2box-datasets.md). Si vous avez suivi les instructions de cette session, vous devriez avoir un ensemble de données utilisant le plugin `Universal` et un autre utilisant le plugin `FM-12 data converted to BUFR`.

Assurez-vous de pouvoir vous connecter à votre VM étudiant à l'aide de votre client SSH (par exemple, PuTTY).

Assurez-vous que wis2box est opérationnel :

```bash
cd ~/wis2box/
python3 wis2box-ctl.py start
python3 wis2box-ctl.py status
```

Assurez-vous que MQTT Explorer est en cours d'exécution et connecté à votre instance en utilisant les identifiants publics `everyone/everyone` avec un abonnement au sujet `origin/a/wis2/#`.

## Le tableau de bord Grafana

Ouvrez le tableau de bord Grafana disponible à l'adresse `http://YOUR-HOST:3000` et vous verrez le tableau de bord de publication des données de wis2box :

<img alt="grafana_dashboard" src="/../assets/img/grafana-homepage.png" width="800">

Gardez le tableau de bord Grafana ouvert dans votre navigateur, car nous l'utiliserons plus tard pour surveiller l'état de l'ingestion des données.

## Utilisation de l'interface web MinIO

Ouvrez l'interface web de MinIO disponible à l'adresse `http://YOUR-HOST:9001` et vous verrez l'écran de connexion :

<img alt="Minio UI: minio ui" src="/../assets/img/minio-login.png" width="400">

Pour vous connecter, vous devez utiliser les identifiants définis par WIS2BOX_STORAGE_USERNAME et WIS2BOX_STORAGE_PASSWORD dans le fichier wis2box.env. Vous pouvez vérifier les valeurs de ces variables en exécutant les commandes suivantes sur votre VM étudiant :

```bash
cat wis2box.env | grep WIS2BOX_STORAGE_USERNAME
cat wis2box.env | grep WIS2BOX_STORAGE_PASSWORD
```

Après vous être connecté, vous êtes dans la vue Object Browser de MinIO. Ici, vous pouvez voir les buckets utilisés par wis2box :

- *wis2box-incoming* : C'est le bucket où vous téléchargez les données pour déclencher le workflow de wis2box.
- *wis2box-public* : C'est le bucket où wis2box publie les données qui ont été ingérées et traitées avec succès.

Cliquez sur le bucket *wis2box-incoming*. Essayez l'option pour définir un nouveau chemin dans ce bucket en cliquant sur `Create new path` :

<img alt="minio ui: minio ui after login" src="/../assets/img/minio-incoming-create-new-path.png" width="800">

Entrez le nouveau chemin de dossier = *new-directory* et téléchargez ce fichier exemple [mydata.nc](./../sample-data/mydata.nc) (clic droit et sélectionnez "enregistrer sous" pour télécharger le fichier). Vous pouvez utiliser le bouton "Upload" dans MinIO pour téléverser le fichier dans le nouveau répertoire :

<img alt="minio ui: create new path" src="/../assets/img/minio-initial-example-upload.png" width="800">

!!! question "Question"

    Après avoir téléversé le fichier, comment pouvez-vous vérifier si le workflow de données dans wis2box a été déclenché avec succès ?

??? success "Cliquez pour révéler la réponse"

    Vous pouvez vérifier le tableau de bord Grafana pour voir si les données ont été ingérées et publiées avec succès.

    Regardez le panneau inférieur du tableau de bord Grafana et vous verrez une **erreur de validation de chemin** indiquant que le chemin ne correspond à aucun ensemble de données configuré :

    ```bash
    ERROR - Path validation error: Could not match http://minio:9000/wis2box-incoming/new-directory/mydata.nc to dataset, path should include one of the following: ['urn:wmo:md:int-wmo-example:synop-dataset-wis2-training', 'urn:wmo:md:int-wmo-example:forecast-dataset' ...
    ``` 
    
## Ingestion et publication : Plugin "Universal"

Maintenant que vous savez comment téléverser des données sur MinIO, essayons de téléverser des données pour l'ensemble de données de prévisions que vous avez créé lors de la session pratique précédente et qui utilise le plugin "Universal".

Retournez à l'interface web de MinIO dans votre navigateur, sélectionnez le bucket `wis2box-incoming` et cliquez sur `Create new path`.

Cette fois, assurez-vous de **créer un répertoire correspondant à l'identifiant de métadonnées pour l'ensemble de données de prévisions** que vous avez créé lors de la session pratique précédente :

<img alt="minio-filepath-forecast-dataset" src="/../assets/img/minio-filepath-forecast-dataset.png" width="800">

Entrez dans le répertoire nouvellement créé, cliquez sur `Upload` et téléversez le fichier que vous avez utilisé précédemment, *mydata.nc*, dans le nouveau répertoire. Vérifiez le tableau de bord Grafana pour voir si les données ont été ingérées et publiées avec succès.

Vous devriez voir l'erreur suivante dans le tableau de bord Grafana :

```bash
ERROR - Path validation error: Unknown file type (nc) for metadata_id=urn:wmo:md:int-wmo-example:forecast-dataset. Did not match any of the following:grib2
```

!!! question "Question"

    Pourquoi les données n'ont-elles pas été ingérées et publiées ?

??? success "Cliquez pour révéler la réponse"

    L'ensemble de données a été configuré pour ne traiter que les fichiers avec l'extension `.grib2`. La configuration de l'extension de fichier fait partie des mappages de données que vous avez définis lors de la session pratique précédente.

Téléchargez ce fichier [GEPS_18August2025.grib2](../sample-data/GEPS_18August2025.grib2) sur votre ordinateur local et téléversez-le dans le répertoire que vous avez créé pour l'ensemble de données de prévisions. Vérifiez le tableau de bord Grafana et MQTT Explorer pour voir si les données ont été ingérées et publiées avec succès.

Vous verrez l'ERREUR suivante dans le tableau de bord Grafana :

```bash
ERROR - Failed to transform file http://minio:9000/wis2box-incoming/urn:wmo:md:int-wmo-example:forecast-dataset/GEPS_18August2025.grib2 : GEPS_18August2025.grib2 did not match ^.*?_(\d{8}).*?\..*$
```

!!! question "Question"

    Comment pouvez-vous résoudre cette erreur ?

??? success "Cliquez pour révéler la réponse"

    Le nom du fichier ne correspond pas à l'expression régulière que vous avez définie dans la configuration de l'ensemble de données. Le nom du fichier doit correspondre au modèle `^.*?_(\d{8}).*?\..*$`, qui nécessite une date à 8 chiffres (YYYYMMDD) dans le nom du fichier.

    Renommez le fichier en *GEPS_202508180000.grib2* et téléversez-le à nouveau dans le même chemin de MinIO pour relancer le workflow de wis2box. (ou téléchargez le fichier renommé ici : [GEPS_202508180000.grib2](../sample-data/GEPS_202508180000.grib2)).

Après avoir corrigé le problème avec le nom du fichier, vérifiez le tableau de bord Grafana et MQTT Explorer pour voir si les données ont été ingérées et publiées avec succès.

Vous devriez voir une nouvelle notification de données WIS2 dans MQTT Explorer :

<img alt="mqtt explorer: message notification geps data" src="/../assets/img/mqtt-explorer-wis2-notification-geps-sample.png" width="800">

!!! note "À propos du plugin Universal"

    Le plugin "Universal" vous permet de publier des données sans aucune transformation. Il s'agit d'un plugin *pass-through* qui ingère le fichier de données et le publie tel quel. Afin d'ajouter la propriété "datetime" à la notification de données WIS2, le plugin s'appuie sur le premier groupe de l'expression régulière du modèle de fichier pour correspondre à la date des données que vous publiez.

!!! question "Question Bonus"

    Essayez de téléverser à nouveau le même fichier dans le même chemin de MinIO. Recevez-vous une autre notification dans MQTT Explorer ?

??? success "Cliquez pour révéler la réponse"

    Non. 
    Dans le tableau de bord Grafana, vous verrez une erreur indiquant que les données ont déjà été publiées :

```bash
ERROR - Data already published for GEPS_202508180000-grib2; not publishing
```

Cela démontre que le flux de données a été déclenché, mais que les données n'ont pas été re-publiées. Le wis2box ne publiera pas les mêmes données deux fois.

Si vous souhaitez forcer l'envoi d'une nouvelle notification pour les mêmes données, supprimez les données du bucket 'wis2box-public' avant de ré-ingérer les données.

## Ingestion et Publication : Plugin "synop2bufr"

Ensuite, vous utiliserez l'ensemble de données que vous avez créé lors de la session pratique précédente en utilisant **Template='weather/surface-based-observations/synop'**. Ce modèle a préconfiguré les plugins de données suivants pour vous :

<img alt="synop-dataset-plugins" src="/../assets/img/wis2box-data-mappings.png" width="1000">

Notez que l'un des plugins est **FM-12 data converted to BUFR** (synop2bufr), qui est configuré pour fonctionner avec des fichiers ayant l'extension **txt**.

Téléchargez cet exemple de données [synop_202502040900.txt](../sample-data/synop_202502040900.txt) (cliquez avec le bouton droit et sélectionnez "Enregistrer sous" pour télécharger le fichier) sur votre ordinateur local. Créez un nouveau chemin dans MinIO correspondant à l'identifiant de métadonnées de l'ensemble de données synop, et téléchargez les données d'exemple dans ce chemin.

Vérifiez le tableau de bord Grafana et MQTT Explorer pour voir si les données ont été ingérées et publiées avec succès.

!!! question "Question"

    Pourquoi n'avez-vous pas reçu de notification dans MQTT Explorer ?

??? success "Cliquez pour révéler la réponse"

    Dans le tableau de bord Grafana, vous verrez un avertissement indiquant :

    ```bash
    WARNING - Station 64400 not found in station file
    ```

    Ou, si aucune station n'était associée au sujet, vous verrez :

    ```bash
    ERROR - No stations found
    ```

    Le flux de données a été déclenché, mais le plugin de données n'a pas pu traiter les données en raison de métadonnées de station manquantes.

!!! note "À propos du plugin FM-12 data converted to BUFR"

    Ce plugin tente de transformer les données d'entrée FM-12 au format BUFR.

    Dans le cadre de la transformation, le plugin ajoute des métadonnées manquantes aux données de sortie, telles que l'identifiant de station WIGOS, la localisation et la hauteur du baromètre de la station. Pour ajouter ces métadonnées, le plugin recherche ces informations dans la liste des stations de votre instance wis2box en utilisant l'identifiant traditionnel (5 chiffres) (64400 dans ce cas).

    Si la station n'est pas trouvée dans la liste des stations, le plugin ne peut pas ajouter les métadonnées manquantes et ne publiera aucune donnée.

Ajoutez la station avec l'identifiant WIGOS `0-20000-0-64400` à votre instance wis2box en utilisant l'éditeur de stations dans le wis2box-webapp, comme vous l'avez appris dans la session pratique [Configuring Station Metadata](./configuring-station-metadata.md).

Récupérez la station depuis OSCAR :

<img alt="oscar-station" src="/../assets/img/webapp-test-station-oscar-search.png" width="600">

Ajoutez la station au sujet '../weather/surface-based-observations/synop' et enregistrez les modifications en utilisant votre jeton d'authentification.

Après avoir ajouté la station, relancez le flux de travail wis2box en téléchargeant à nouveau le fichier de données d'exemple *synop_202502040900.txt* dans le même chemin dans MinIO.

Vérifiez le tableau de bord Grafana et MQTT Explorer pour confirmer que les données ont été publiées avec succès. Si vous voyez la notification ci-dessous, cela signifie que vous avez publié avec succès les données d'exemple synop :

<img alt="webapp-test-station" src="/../assets/img/mqtt-explorer-wis2box-notification-synop-sample.png" width="800">

!!! question "Question"

    Quelle est l'extension du fichier publié dans la notification de données WIS2 ?

??? success "Cliquez pour révéler la réponse"

    Consultez la section Liens de la notification de données WIS2 dans MQTT Explorer et vous verrez le lien canonique :

    ```json
    {
      "rel": "canonical",
      "type": "application/bufr",
      "href": "http://example.wis2.training/data/2025-02-04/wis/urn:wmo:md:int-wmo-example:synop-dataset/WIGOS_0-20000-0-64400_20250204T090000.bufr4",
      "length": 387
    }
    ```

    L'extension du fichier est `.bufr4`, indiquant que les données ont été transformées avec succès du format FM-12 au format BUFR par le plugin.

## Ingestion de données avec Python

L'utilisation de l'interface web de MinIO est une méthode pratique pour télécharger manuellement des données dans MinIO à des fins de test. Cependant, dans un environnement de production, vous utiliseriez généralement des processus automatisés pour télécharger des données dans MinIO, par exemple en utilisant des scripts ou des applications qui utilisent l'API compatible S3 de MinIO.

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

Dans le répertoire `exercise-materials/data-ingest-exercises`, vous trouverez un script exemple `copy_file_to_incoming.py` qui peut être utilisé pour copier des fichiers dans MinIO.

Essayez d'exécuter le script pour copier le fichier de données d'exemple `synop_202501030900.txt` dans le bucket `wis2box-incoming` de MinIO comme suit :

```bash
cd ~/wis2box-data/data-ingest-exercises
python3 copy_file_to_incoming.py synop_202501030900.txt
```

!!! note

    Vous obtiendrez une erreur car le script n'est pas configuré pour accéder au point de terminaison MinIO de votre wis2box.

Le script doit connaître le point de terminaison correct pour accéder à MinIO sur votre wis2box. Si wis2box s'exécute sur votre hôte, le point de terminaison MinIO est disponible à l'adresse `http://YOUR-HOST:9000`. Le script doit également être mis à jour avec votre mot de passe de stockage et le chemin dans le bucket MinIO pour stocker les données.

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
    python3 ~/wis2box-data/ ~/wis2box-data/synop_202501030900.txt
    ```

    Assurez-vous que les erreurs sont résolues.

Une fois que vous parvenez à exécuter le script avec succès, vous verrez un message indiquant que le fichier a été copié dans MinIO, et vous devriez voir des notifications de données publiées par votre instance wis2box dans MQTT Explorer.

Vous pouvez également vérifier le tableau de bord Grafana pour voir si les données ont été ingérées et publiées avec succès.

Maintenant que le script fonctionne, vous pouvez essayer de copier d'autres fichiers dans MinIO en utilisant le même script.

!!! question "Ingestion de données binaires au format BUFR"

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

## Ingestion de données via SFTP
```

Le service MinIO dans wis2box peut également être accessible via SFTP. Si vous disposez d’un système existant pouvant être configuré pour transférer des données via SFTP, vous pouvez utiliser cette méthode comme alternative pour automatiser l’ingestion de vos données.

Le serveur SFTP pour MinIO est lié au port 8022 sur l’hôte (le port 22 est utilisé pour SSH).

Dans cet exercice, nous allons démontrer comment utiliser WinSCP pour téléverser des données vers MinIO en utilisant SFTP.

Vous pouvez configurer une nouvelle connexion WinSCP comme illustré dans cette capture d’écran :

<img alt="winscp-sftp-connection" src="/../assets/img/winscp-sftp-login.png" width="400">

Les identifiants pour la connexion SFTP sont définis par `WIS2BOX_STORAGE_USERNAME` et `WIS2BOX_STORAGE_PASSWORD` dans votre fichier `wis2box.env` et sont les mêmes que ceux utilisés pour se connecter à l’interface utilisateur de MinIO.

Lorsque vous vous connectez, vous verrez les buckets utilisés par wis2box dans MinIO :

<img alt="winscp-sftp-bucket" src="/../assets/img/winscp-buckets.png" width="600">

Vous pouvez naviguer jusqu’au bucket `wis2box-incoming`, puis dans le dossier correspondant à votre jeu de données. Vous verrez les fichiers que vous avez téléversés dans les exercices précédents :

<img alt="winscp-sftp-incoming-path" src="/../assets/img/winscp-incoming-data-path.png" width="600">

!!! question "Téléverser des données via SFTP"

    Téléchargez ce fichier d’exemple sur votre ordinateur local :

    [synop_202503030900.txt](./../sample-data/synop_202503030900.txt) (cliquez avec le bouton droit et sélectionnez "enregistrer sous" pour télécharger le fichier).

    Ensuite, téléversez-le dans le chemin du jeu de données incoming dans MinIO en utilisant votre session SFTP dans WinSCP.

    Vérifiez le tableau de bord Grafana et MQTT Explorer pour voir si les données ont été correctement ingérées et publiées.

??? success "Cliquez pour révéler la réponse"

    Vous devriez voir une nouvelle notification de données WIS2 publiée pour la station de test `0-20000-0-64400`, indiquant que les données ont été correctement ingérées et publiées.

    <img alt="grafana_data_ingest" src="/../assets/img/grafana_data-ingest-test3.png" width="400"> 

    Si vous utilisez un chemin incorrect, vous verrez un message d’erreur dans les journaux.

## Conclusion

!!! success "Félicitations !"
    Au cours de cette session pratique, vous avez appris à :

    - Déclencher le workflow de wis2box en téléversant des données vers MinIO en utilisant différentes méthodes.
    - Déboguer les erreurs courantes dans le processus d’ingestion de données en utilisant le tableau de bord Grafana et les journaux de votre instance wis2box.
    - Surveiller les notifications de données WIS2 publiées par votre wis2box dans le tableau de bord Grafana et MQTT Explorer.
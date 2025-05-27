---
title: Ingestion de données pour publication
---

# Ingestion de données pour publication

!!! abstract "Résultats d'apprentissage"

    À la fin de cette session pratique, vous serez capable de :
    
    - Déclencher le flux de travail wis2box en téléchargeant des données sur MinIO en utilisant la ligne de commande, l'interface web de MinIO, SFTP ou un script Python.
    - Accéder au tableau de bord Grafana pour surveiller le statut de l'ingestion des données et consulter les journaux de votre instance wis2box.
    - Voir les notifications de données WIS2 publiées par votre wis2box en utilisant MQTT Explorer.

## Introduction

Dans WIS2, les données sont partagées en temps réel en utilisant des notifications de données WIS2 qui contiennent un lien "canonique" à partir duquel les données peuvent être téléchargées.

Pour déclencher le flux de travail des données dans un WIS2 Node en utilisant le logiciel wis2box, les données doivent être téléchargées dans le bucket **wis2box-incoming** sur **MinIO**, ce qui initie le flux de travail wis2box. Ce processus aboutit à la publication des données via une notification de données WIS2. Selon les mappages de données configurés dans votre instance wis2box, les données peuvent être transformées au format BUFR avant d'être publiées.

Dans cet exercice, nous utiliserons des fichiers de données exemples pour déclencher le flux de travail wis2box et **publier des notifications de données WIS2** pour l'ensemble de données que vous avez configuré lors de la session pratique précédente.

Pendant l'exercice, nous surveillerons le statut de l'ingestion des données en utilisant le **tableau de bord Grafana** et **MQTT Explorer**. Le tableau de bord Grafana utilise des données de Prometheus et Loki pour afficher le statut de votre wis2box, tandis que MQTT Explorer vous permet de voir les notifications de données WIS2 publiées par votre instance wis2box.

Notez que wis2box transformera les données d'exemple en format BUFR avant de les publier sur le courtier MQTT, conformément aux mappages de données préconfigurés dans votre ensemble de données. Pour cet exercice, nous nous concentrerons sur les différentes méthodes pour télécharger des données sur votre instance wis2box et vérifier l'ingestion et la publication réussies. La transformation des données sera abordée plus tard dans la session pratique [Outils de conversion de données](./data-conversion-tools).

## Préparation

Cette section utilise l'ensemble de données pour "surface-based-observations/synop" précédemment créé dans la session pratique [Configuration des ensembles de données dans wis2box](./configuring-wis2box-datasets). Elle nécessite également une connaissance de la configuration des stations dans le **wis2box-webapp**, comme décrit dans la session pratique [Configuration des métadonnées des stations](./configuring-station-metadata).

Assurez-vous de pouvoir vous connecter à votre VM étudiante en utilisant votre client SSH (par exemple, PuTTY).

Assurez-vous que wis2box est opérationnel :

```bash
cd ~/wis2box/
python3 wis2box-ctl.py start
python3 wis2box-ctl.py status
```

Assurez-vous que MQTT Explorer est en cours d'exécution et connecté à votre instance en utilisant les identifiants publics `everyone/everyone` avec un abonnement au sujet `origin/a/wis2/#`.

Assurez-vous que vous avez un navigateur web ouvert avec le tableau de bord Grafana pour votre instance en naviguant vers `http://YOUR-HOST:3000`.

### Préparer les données d'exemple

Copiez le répertoire `exercise-materials/data-ingest-exercises` dans le répertoire que vous avez défini comme `WIS2BOX_HOST_DATADIR` dans votre fichier `wis2box.env` :

```bash
cp -r ~/exercise-materials/data-ingest-exercises ~/wis2box-data/
```

!!! note
    Le `WIS2BOX_HOST_DATADIR` est monté comme `/data/wis2box/` à l'intérieur du conteneur wis2box-management par le fichier `docker-compose.yml` inclus dans le répertoire `wis2box`.
    
    Cela vous permet de partager des données entre l'hôte et le conteneur.

### Ajouter la station de test

Ajoutez la station avec l'identifiant WIGOS `0-20000-0-64400` à votre instance wis2box en utilisant l'éditeur de stations dans le wis2box-webapp.

Récupérez la station depuis OSCAR :

<img alt="oscar-station" src="/../assets/img/webapp-test-station-oscar-search.png" width="600">

Ajoutez la station aux ensembles de données que vous avez créés pour la publication sur "../surface-based-observations/synop" et enregistrez les modifications en utilisant votre jeton d'authentification :

<img alt="webapp-test-station" src="/../assets/img/webapp-test-station-save.png" width="800">

Notez que vous pouvez retirer cette station de votre ensemble de données après la session pratique.

## Tester l'ingestion de données depuis la ligne de commande

Dans cet exercice, nous utiliserons la commande `wis2box data ingest` pour télécharger des données sur MinIO.

Assurez-vous d'être dans le répertoire `wis2box` et connectez-vous au conteneur **wis2box-management** :

```bash
cd ~/wis2box
python3 wis2box-ctl.py login
```

Vérifiez que les données d'échantillon suivantes sont disponibles dans le répertoire `/data/wis2box/` à l'intérieur du conteneur **wis2box-management** :

```bash
ls -lh /data/wis2box/data-ingest-exercises/synop_202412030900.txt
```

!!! question "Ingestion de données en utilisant `wis2box data ingest`"

    Exécutez la commande suivante pour ingérer le fichier de données d'échantillon dans votre instance wis2box :

    ```bash
    wis2box data ingest -p /data/wis2box/data-ingest-exercises/synop_202412030900.txt --metadata-id urn:wmo:md:not-my-centre:synop-test
    ```

    Les données ont-elles été ingérées avec succès ? Sinon, quel était le message d'erreur et comment pouvez-vous le corriger ?

??? success "Cliquez pour révéler la réponse"

    Les données n'ont **pas** été ingérées avec succès. Vous devriez voir ce qui suit :

    ```bash
    Error: metadata_id=urn:wmo:md:not-my-centre:synop-test not found in data mappings
    ```

    Le message d'erreur indique que l'identifiant de métadonnées que vous avez fourni ne correspond à aucun des ensembles de données que vous avez configurés dans votre instance wis2box.

    Fournissez l'identifiant de métadonnées correct qui correspond à l'ensemble de données que vous avez créé lors de la session pratique précédente et répétez la commande d'ingestion des données jusqu'à ce que vous voyiez la sortie suivante :

    ```bash 
    Processing /data/wis2box/data-ingest-exercises/synop_202412030900.txt
    Done
    ```

Allez à la console MinIO dans votre navigateur et vérifiez si le fichier `synop_202412030900.txt` a été téléchargé dans le bucket `wis2box-incoming`. Vous devriez voir un nouveau répertoire avec le nom de l'ensemble de données que vous avez fourni dans l'option `--metadata-id`, et à l'intérieur de ce répertoire, vous trouverez le fichier `synop_202412030900.txt` :

<img alt="minio-wis2box-incoming-dataset-folder" src="/../assets/img/minio-data-ingest-test-data.png" width="800">

!!! note
    La commande `wis2box data ingest` a téléchargé le fichier dans le bucket `wis2box-incoming` sur MinIO dans un répertoire nommé d'après l'identifiant de métadonnées que vous avez fourni.

Allez au tableau de bord Grafana dans votre navigateur et vérifiez le statut de l'ingestion des données.

!!! question "Vérifiez le statut de l'ingestion des données sur Grafana"
    
    Allez au tableau de bord Grafana à **http://your-host:3000** et vérifiez le statut de l'ingestion des données dans votre navigateur.
    
    Comment pouvez-vous voir si les données ont été ingérées et publiées avec succès ?

??? success "Cliquez pour révéler la réponse"
    
    Si vous avez ingéré les données avec succès, vous devriez voir ce qui suit :
    
    <img alt="grafana_data_ingest" src="/../assets/img/grafana_data-ingest-test.png" width="400">  
    
    Si vous ne voyez pas cela, veuillez vérifier les messages d'AVERTISSEMENT ou d'ERREUR affichés en bas du tableau de bord et tenter de les résoudre.

!!! question "Vérifiez le courtier MQTT pour les notifications WIS2"
    
    Allez à MQTT Explorer et vérifiez si vous pouvez voir le message de notification WIS2 pour les données que vous venez d'ingérer.
    
    Combien de notifications de données WIS2 ont été publiées par votre wis2box ?
    
    Comment accédez-vous au contenu des données publiées ?

??? success "Cliquez pour révéler la réponse"

    Vous devriez voir 1 notification de données WIS2 publiée par votre wis2box.

    Pour accéder au contenu des données publiées, vous pouvez développer la structure du sujet pour voir les différents niveaux du message jusqu'à atteindre le dernier niveau et examiner le contenu du message.

    Le contenu du message comporte une section "links" avec une clé "rel" de "canonical" et une clé "href" avec l'URL pour télécharger les données. L'URL sera au format `http://YOUR-HOST/data/...`. 
    
    Notez que le format des données est BUFR, et vous aurez besoin d'un analyseur BUFR pour visualiser le contenu des données. Le format BUFR est un format binaire utilisé par les services météorologiques pour échanger des données. Les plugins de données à l'intérieur de wis2box ont transformé les données en BUFR avant de les publier.

Après avoir terminé cet exercice, quittez le conteneur **wis2box-management** :

```bash
exit
```

## Téléchargement de données à l'aide de l'interface web MinIO

Dans les exercices précédents, vous avez téléchargé des données disponibles sur l'hôte wis2box sur MinIO en utilisant la commande `wis2box data ingest`. 

Ensuite, nous utiliserons l'interface web MinIO, qui vous permet de télécharger et de télécharger des données sur MinIO à l'aide d'un navigateur web.

!!! question "Retéléchargez les données à l'aide de l'interface web MinIO"

    Allez à l'interface web MinIO dans votre navigateur et parcourez le bucket `wis2box-incoming`. Vous verrez le fichier `synop_202412030900.txt` que vous avez téléchargé lors des exercices précédents.

    Cliquez sur le fichier, et vous aurez l'option de le télécharger :

    <img alt="minio-wis2box-incoming-dataset-folder" src="/../assets/img/minio-download.png" width="800">

    Vous pouvez télécharger ce fichier et le retélécharger sur le même chemin dans MinIO pour redéclencher le flux de travail wis2box.

    Vérifiez le tableau de bord Grafana et MQTT Explorer pour voir si les données ont été ingérées et publiées avec succès.

??? success "Cliquez pour révéler la réponse"

    Vous verrez un message indiquant que wis2box a déjà publié ces données :

    ```bash
    ERROR - Data already published for WIGOS_0-20000-0-64400_20241203T090000-bufr4; not publishing
    ``` 
    
    Cela démontre que le flux de travail des données a été déclenché, mais les données n'ont pas été republiées. Le wis2box ne publiera pas les mêmes données deux fois. 
    
!!! question "Téléchargez de nouvelles données à l'aide de l'interface web MinIO"
    
    Téléchargez ce fichier d'échantillon [synop_202502040900.txt](./../../sample-data/synop_202502040900.txt) (cliquez avec le bouton droit et sélectionnez "enregistrer sous" pour télécharger le fichier).
    
    Téléchargez le fichier que vous avez téléchargé à l'aide de l'interface web sur le même chemin dans MinIO que le fichier précédent.

    Les données ont-elles été ingérées et publiées avec succès ?

??? success "Cliquez pour révéler la réponse"

    Allez au tableau de bord Grafana et vérifiez si les données ont été ingérées et publiées avec succès.

    Si vous utilisez le mauvais chemin, vous verrez un message d'erreur dans les journaux.

    Si vous utilisez le bon chemin, vous verrez une notification de données WIS2 supplémentaire publiée pour la station de test `0-20000-0-64400`, indiquant que les données ont été ingérées et publiées avec succès.

    <img alt="grafana_data_ingest" src="/../assets/img/grafana_data-ingest-test2.png" width="400"> 

## Téléchargement de données à l'aide de SFTP

Le service MinIO dans wis2box peut également être accédé via SFTP. Le serveur SFTP pour MinIO est lié au port 8022 sur l'hôte (le port 22 est utilisé pour SSH).

Dans cet exercice, nous allons démontrer comment utiliser WinSCP pour télécharger des données sur MinIO à l'aide de SFTP.

Vous pouvez configurer une nouvelle connexion WinSCP comme le montre cette capture d'écran :

<img alt="winscp-sftp-connection" src="/../assets/img/winscp-sftp-login.png" width="400">

Les identifiants pour la connexion SFTP sont définis par `WIS2BOX_STORAGE_USERNAME` et `WIS2BOX_STORAGE_PASSWORD` dans votre fichier `wis2box.env` et sont les mêmes que les identifiants que vous avez utilisés pour vous connecter à l'interface utilisateur de MinIO.

Lorsque vous vous connectez, vous verrez les buckets utilisés par wis2box dans MinIO :

<img alt="winscp-sftp-bucket" src="/../assets/img/winscp-buckets.png" width="600">

Vous pouvez naviguer jusqu'au bucket `wis2box-incoming` puis jusqu'au dossier de votre ensemble de données. Vous verrez les fichiers que vous avez téléchargés lors des exercices précédents :

<img alt="winscp-sftp-incoming-path" src="/../assets/img/winscp-incoming-data-path.png" width="600">

!!! question "Téléchargez des données à l'aide de SFTP"

    Téléchargez ce fichier d'échantillon sur votre ordinateur local :

    [synop_202503030900.txt](./../../sample-data/synop_202503030900.txt) (cliquez avec le bouton droit et sélectionnez "enregistrer sous" pour télécharger le fichier).

    Ensuite, téléchargez-le sur le chemin de l'ensemble de données entrant dans MinIO à l'aide de votre session SFTP dans WinSCP.

    Vérifiez le tableau de bord Grafana et MQTT Explorer pour voir si les données ont été ingérées et publiées avec succès.

??? success "Cliquez pour révéler la réponse"

    Vous devriez voir une nouvelle notification de données WIS2 publiée pour la station de test `0-20000-0-64400`, indiquant que les données ont été ingérées et publiées avec succès.

    <img alt="grafana_data_ingest" src="/../assets/img/grafana_data-ingest-test3.png" width="400">

Si vous utilisez un chemin incorrect, vous verrez un message d'erreur dans les journaux.

## Téléversement de données à l'aide d'un script Python

Dans cet exercice, nous utiliserons le client Python de MinIO pour copier des données dans MinIO.

MinIO fournit un client Python, qui peut être installé comme suit :

```bash
pip3 install minio
```

Sur votre VM étudiant, le package 'minio' pour Python sera déjà installé.

Dans le répertoire `exercise-materials/data-ingest-exercises`, vous trouverez un script exemple `copy_file_to_incoming.py` qui peut être utilisé pour copier des fichiers dans MinIO.

Essayez d'exécuter le script pour copier le fichier de données exemple `synop_202501030900.txt` dans le seau `wis2box-incoming` de MinIO comme suit :

```bash
cd ~/wis2box-data/data-ingest-exercises
python3 copy_file_to_incoming.py synop_202501030900.txt
```

!!! note

    Vous obtiendrez une erreur car le script n'est pas configuré pour accéder au point de terminaison MinIO sur votre wis2box.

Le script doit connaître le point de terminaison correct pour accéder à MinIO sur votre wis2box. Si wis2box est en cours d'exécution sur votre hôte, le point de terminaison MinIO est disponible à `http://YOUR-HOST:9000`. Le script doit également être mis à jour avec votre mot de passe de stockage et le chemin dans le seau MinIO pour stocker les données.

!!! question "Mettre à jour le script et ingérer les données CSV"
    
    Modifiez le script `copy_file_to_incoming.py` pour corriger les erreurs, en utilisant l'une des méthodes suivantes :
    - Depuis la ligne de commande : utilisez l'éditeur de texte `nano` ou `vim` pour modifier le script.
    - En utilisant WinSCP : démarrez une nouvelle connexion en utilisant le protocole de fichier `SCP` et les mêmes identifiants que votre client SSH. Naviguez dans le répertoire `wis2box-data/data-ingest-exercises` et modifiez `copy_file_to_incoming.py` en utilisant l'éditeur de texte intégré.
    
    Assurez-vous de :

    - Définir le point de terminaison MinIO correct pour votre hôte.
    - Fournir le mot de passe de stockage correct pour votre instance MinIO.
    - Fournir le chemin correct dans le seau MinIO pour stocker les données.

    Réexécutez le script pour ingérer le fichier de données exemple `synop_202501030900.txt` dans MinIO :

    ```bash
    python3 ~/wis2box-data/ ~/wis2box-data/synop_202501030900.txt
    ```

    Assurez-vous que les erreurs sont résolues.

Une fois que vous parvenez à exécuter le script avec succès, vous verrez un message indiquant que le fichier a été copié dans MinIO, et vous devriez voir des notifications de données publiées par votre instance wis2box dans MQTT Explorer.

Vous pouvez également vérifier le tableau de bord Grafana pour voir si les données ont été ingérées et publiées avec succès.

Maintenant que le script fonctionne, vous pouvez essayer de copier d'autres fichiers dans MinIO en utilisant le même script.

!!! question "Ingérer des données binaires au format BUFR"

    Exécutez la commande suivante pour copier le fichier de données binaires `bufr-example.bin` dans le seau `wis2box-incoming` de MinIO :

    ```bash
    python3 copy_file_to_incoming.py bufr-example.bin
    ```

Vérifiez le tableau de bord Grafana et MQTT Explorer pour voir si les données de test ont été ingérées et publiées avec succès. Si vous voyez des erreurs, essayez de les résoudre.

!!! question "Vérifier l'ingestion des données"

    Combien de messages ont été publiés au courtier MQTT pour cet échantillon de données ?

??? success "Cliquez pour révéler la réponse"

    Vous verrez des erreurs signalées dans Grafana car les stations dans le fichier BUFR ne sont pas définies dans la liste des stations de votre instance wis2box.
    
    Si toutes les stations utilisées dans le fichier BUFR sont définies dans votre instance wis2box, vous devriez voir 10 messages publiés au courtier MQTT. Chaque notification correspond à des données pour une station pour un horodatage d'observation.

    Le plugin `wis2box.data.bufr4.ObservationDataBUFR` divise le fichier BUFR en messages BUFR individuels et publie un message pour chaque station et horodatage d'observation.

## Conclusion

!!! success "Félicitations !"
    Dans cette session pratique, vous avez appris à :

    - Déclencher le flux de travail wis2box en téléversant des données dans MinIO en utilisant diverses méthodes.
    - Déboguer les erreurs courantes dans le processus d'ingestion de données en utilisant le tableau de bord Grafana et les journaux de votre instance wis2box.
    - Surveiller les notifications de données WIS2 publiées par votre wis2box dans le tableau de bord Grafana et MQTT Explorer.
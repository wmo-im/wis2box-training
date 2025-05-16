---
title: Automatisation de l'ingestion de données
---

# Automatisation de l'ingestion de données

!!! abstract "Résultats d'apprentissage"

    À la fin de cette session pratique, vous serez capable de :
    
    - comprendre comment les plugins de données de votre ensemble de données déterminent le workflow d'ingestion des données
    - ingérer des données dans wis2box en utilisant un script avec le client Python MinIO
    - ingérer des données dans wis2box en accédant à MinIO via SFTP

## Introduction

Le conteneur **wis2box-management** écoute les événements du service de stockage MinIO pour déclencher l'ingestion de données en fonction des plugins de données configurés pour votre ensemble de données. Cela vous permet de télécharger des données dans le seau MinIO et de déclencher le workflow wis2box pour publier des données sur le courtier WIS2.

Les plugins de données définissent les modules Python qui sont chargés par le conteneur **wis2box-management** et déterminent comment les données sont transformées et publiées.

Dans l'exercice précédent, vous deviez avoir créé un ensemble de données en utilisant le modèle `surface-based-observations/synop` qui incluait les plugins de données suivants :

<img alt="mappages de données" src="/../assets/img/wis2box-data-mappings.png" width="800">

Lorsqu'un fichier est téléchargé sur MinIO, wis2box associera le fichier à un ensemble de données lorsque le chemin du fichier contient l'identifiant de l'ensemble de données (`metadata_id`) et il déterminera les plugins de données à utiliser en fonction de l'extension du fichier et du modèle de fichier défini dans les mappages de l'ensemble de données.

Dans les sessions précédentes, nous avons déclenché le workflow d'ingestion de données en utilisant la fonctionnalité de ligne de commande de wis2box, qui télécharge les données sur le stockage MinIO dans le chemin correct.

Les mêmes étapes peuvent être effectuées de manière programmatique en utilisant n'importe quel logiciel client MinIO ou S3, vous permettant d'automatiser votre ingestion de données dans le cadre de vos workflows opérationnels.

Alternativement, vous pouvez également accéder à MinIO en utilisant le protocole SFTP pour télécharger des données et déclencher le workflow d'ingestion de données.

## Préparation

Connectez-vous à votre VM étudiant en utilisant votre client SSH (PuTTY ou autre).

Assurez-vous que wis2box est opérationnel :

```bash
cd ~/wis2box-1.0.0rc1/
python3 wis2box-ctl.py start
python3 wis2box-ctl.py status
```

Assurez-vous que MQTT Explorer est en cours d'exécution et connecté à votre instance. Si vous êtes toujours connecté depuis la session précédente, effacez tous les messages précédents que vous avez reçus de la file d'attente.
Cela peut être fait soit en se déconnectant et en se reconnectant, soit en cliquant sur l'icône de la poubelle pour le sujet donné.

Assurez-vous que vous avez un navigateur web ouvert avec le tableau de bord Grafana pour votre instance en allant à `http://<votre-hôte>:3000`

Et assurez-vous d'avoir un deuxième onglet ouvert avec l'interface utilisateur MinIO à `http://<votre-hôte>:9001`. Souvenez-vous que vous devez vous connecter avec le `WIS2BOX_STORAGE_USER` et le `WIS2BOX_STORAGE_PASSWORD` définis dans votre fichier `wis2box.env`.

## Exercice 1 : configurer un script Python pour ingérer des données dans MinIO

Dans cet exercice, nous utiliserons le client Python MinIO pour copier des données dans MinIO.

MinIO fournit un client Python qui peut être installé comme suit :

```bash
pip3 install minio
```

Sur votre VM étudiant, le paquet 'minio' pour Python sera déjà installé.

Allez dans le répertoire `exercise-materials/data-ingest-exercises` ; ce répertoire contient un script d'exemple `copy_file_to_incoming.py` qui utilise le client Python MinIO pour copier un fichier dans MinIO.

Essayez d'exécuter le script pour copier le fichier de données d'exemple `csv-aws-example.csv` dans le seau `wis2box-incoming` dans MinIO comme suit :

```bash
cd ~/exercise-materials/data-ingest-exercises
python3 copy_file_to_incoming.py csv-aws-example.csv
```

!!! note

    Vous obtiendrez une erreur car le script n'est pas configuré pour accéder au point de terminaison MinIO sur votre wis2box.

Le script doit connaître le point de terminaison correct pour accéder à MinIO sur votre wis2box. Si wis2box fonctionne sur votre hôte, le point de terminaison MinIO est disponible à `http://<votre-hôte>:9000`. Le script doit également être mis à jour avec votre mot de passe de stockage et le chemin dans le seau MinIO pour stocker les données.

!!! question "Mettez à jour le script et ingérez les données CSV"
    
    Éditez le script `copy_file_to_incoming.py` pour corriger les erreurs, en utilisant l'une des méthodes suivantes :
    - Depuis la ligne de commande : utilisez l'éditeur de texte `nano` ou `vim` pour éditer le script
    - En utilisant WinSCP : démarrez une nouvelle connexion en utilisant le protocole de fichier `SCP` et les mêmes identifiants que votre client SSH. Naviguez jusqu'au répertoire `exercise-materials/data-ingest-exercises` et éditez `copy_file_to_incoming.py` en utilisant l'éditeur de texte intégré
    
    Assurez-vous que vous :

    - définissez le point de terminaison MinIO correct pour votre hôte
    - fournissez le mot de passe de stockage correct pour votre instance MinIO
    - fournissez le chemin correct dans le seau MinIO pour stocker les données

    Réexécutez le script pour ingérer le fichier de données d'exemple `csv-aws-example.csv` dans MinIO :

    ```bash
    python3 copy_file_to_incoming.py csv-aws-example.csv
    ```

    Et assurez-vous que les erreurs sont résolues.

Vous pouvez vérifier que les données ont été correctement téléchargées en vérifiant l'interface utilisateur MinIO et en voyant si les données d'exemple sont disponibles dans le répertoire correct dans le seau `wis2box-incoming`.

Vous pouvez utiliser le tableau de bord Grafana pour vérifier l'état du workflow d'ingestion de données.

Enfin, vous pouvez utiliser MQTT Explorer pour vérifier si des notifications ont été publiées pour les données que vous avez ingérées. Vous devriez voir que les données CSV ont été transformées en format BUFR et qu'une notification de données WIS2 a été publiée avec une URL "canonique" pour permettre le téléchargement des données BUFR.

## Exercice 2 : Ingérer des données binaires

Ensuite, nous essayons d'ingérer des données binaires au format BUFR en utilisant le client Python MinIO.

wis2box peut ingérer des données binaires au format BUFR en utilisant le plugin `wis2box.data.bufr4.ObservationDataBUFR` inclus dans wis2box.

Ce plugin divisera le fichier BUFR en messages BUFR individuels et publiera chaque message au courtier MQTT. Si la station pour le message BUFR correspondant n'est pas définie dans les métadonnées de la station wis2box, le message ne sera pas publié.

Puisque vous avez utilisé le modèle `surface-based-observations/synop` lors de la session précédente, vos mappages de données incluent le plugin `FM-12 data converted to BUFR` pour les mappages de l'ensemble de données. Ce plugin charge le module `wis2box.data.synop2bufr.ObservationDataSYNOP2BUFR` pour ingérer les données.

!!! question "Ingérer des données binaires au format BUFR"

    Exécutez la commande suivante pour copier le fichier de données binaires `bufr-example.bin` dans le seau `wis2box-incoming` dans MinIO :

    ```bash
    python3 copy_file_to_incoming.py bufr-example.bin
    ```

Vérifiez le tableau de bord Grafana et MQTT Explorer pour voir si les données de test ont été correctement ingérées et publiées et si vous voyez des erreurs, essayez de les résoudre.

!!! question "Vérifiez l'ingestion des données"

    Combien de messages ont été publiés au courtier MQTT pour cet échantillon de données ?

??? success "Cliquez pour révéler la réponse"

    Si vous avez correctement ingéré et publié le dernier échantillon de données, vous devriez avoir reçu 10 nouvelles notifications sur le courtier MQTT wis2box. Chaque notification correspond aux données d'une station pour un horodatage d'observation.

    Le plugin `wis2box.data.bufr4.ObservationDataBUFR` divise le fichier BUFR en messages BUFR individuels et publie un message pour chaque station et horodatage d'observation.

## Exercice 3 : Ingérer des données SYNOP au format ASCII

Lors de la session précédente, nous avons utilisé le formulaire SYNOP dans l'**application web wis2box** pour ingérer des données SYNOP au format ASCII. Vous pouvez également ingérer des données SYNOP au format ASCII en téléchargeant les données dans MinIO.

Lors de la session précédente, vous deviez avoir créé un ensemble de données qui incluait le plugin 'FM-12 data converted to BUFR' pour les mappages de l'ensemble de données :

<img alt="mappages de l'ensemble de données" src="/../assets/img/wis2box-data-mappings.png" width="800">

Ce plugin charge le module `wis2box.data.synop2bufr.ObservationDataSYNOP2BUFR` pour ingérer les données.

Essayez d'utiliser le client Python MinIO pour ingérer les données de test `synop-202307.txt` et `synop-202308.txt` dans votre instance wis2box.

Notez que les 2 fichiers contiennent le même contenu, mais le nom du fichier est différent. Le nom du fichier est utilisé pour déterminer la date de l'échantillon de données.

Le plugin synop2bufr s'appuie sur un modèle de fichier pour extraire la date du nom du fichier. Le premier groupe dans l'expression régulière est utilisé pour extraire l'année et le deuxième groupe est utilisé pour extraire le mois.

!!! question "Ingérer des données FM-12 SYNOP au format ASCII"

    Retournez à l'interface MinIO dans votre navigateur et naviguez jusqu'au seau `wis2box-incoming` et dans le chemin où vous avez téléchargé les données de test lors de l'exercice précédent.
    
    Téléchargez les nouveaux fichiers dans le chemin correct dans le seau `wis2box-incoming` dans MinIO pour déclencher le workflow d'ingestion des données.

    Vérifiez le tableau de bord Grafana et MQTT Explorer pour voir si les données de test ont été correctement ingérées et publiées.

    Quelle est la différence dans le `properties.datetime` entre les deux messages publiés au courtier MQTT ?

??? success "Cliquez pour révéler la réponse"

    Vérifiez les propriétés des 2 dernières notifications dans MQTT Explorer et vous noterez que l'une des notifications a :

    ```{.copy}
    "properties": {
        "data_id": "wis2/urn:wmo:md:nl-knmi-test:surface-based-observations.synop/WIGOS_0-20000-0-60355_20230703T090000",
        "datetime": "2023-07-03T09:00:00Z",
        ...
    ```

    et l'autre notification a :

    ```{.copy}
    "properties": {
        "data_id": "wis2/urn:wmo:md:nl-knmi-test:surface-based-observations.synop/WIGOS_0-20000-0-60355_20230803T09:00:00Z",
        ...
    ```

    Le nom du fichier a été utilisé pour déterminer l'année et le mois de l'échantillon de données.

## Exercice 4 : Ingérer des données dans MinIO en utilisant SFTP

Les données peuvent également être ingérées dans MinIO via SFTP.

Le service MinIO activé dans la pile wis2box a SFTP activé sur le port 8022. Vous pouvez accéder à MinIO via SFTP en utilisant les mêmes identifiants que pour l'interface utilisateur MinIO. Dans cet exercice, nous utiliserons les identifiants administrateur pour le service MinIO tels que définis dans `wis2box.env`, mais vous pouvez également créer des utilisateurs supplémentaires dans l'interface utilisateur MinIO.

Pour accéder à MinIO via SFTP, vous pouvez utiliser n'importe quel logiciel client SFTP. Dans cet exercice, nous utiliserons WinSCP, qui est un client SFTP gratuit pour Windows.

En utilisant WinSCP, votre connexion ressemblerait à ceci :

<img alt="connexion sftp-winscp" src="/../assets/img/winscp-sftp-connection.png" width="400">

Pour le nom d'utilisateur et le mot de passe, utilisez les valeurs des variables d'environnement `WIS2BOX_STORAGE_USERNAME` et `WIS2BOX_STORAGE_PASSWORD` de votre fichier `wis2box.env`. Cliquez sur 'enregistrer' pour sauvegarder la session puis sur 'connexion' pour vous connecter.

Lorsque vous vous connectez, vous verrez le seau MinIO `wis2box-incoming` et `wis2box-public` dans le répertoire racine. Vous pouvez télécharger des données dans le seau `wis2box-incoming` pour déclencher le workflow d'ingestion des données.

Cliquez sur le seau `wis2box-incoming` pour naviguer dans ce seau, puis faites un clic droit et sélectionnez *Nouveau*->*Répertoire* pour créer un nouveau répertoire dans le seau `wis2box-incoming`.

Créez le répertoire *not-a-valid-path* et téléchargez le fichier *randomfile.txt* dans ce répertoire (vous pouvez utiliser n'importe quel fichier que vous aimez).

Vérifiez ensuite le tableau de bord Grafana au port 3000 pour voir si le workflow d'ingestion des données a été déclenché. Vous devriez voir :

*ERREUR - Erreur de validation du chemin : Impossible de faire correspondre http://minio:9000/wis2box-incoming/not-a-valid-path/randomfile.txt à l'ensemble de données, le chemin doit inclure l'un des éléments suivants : ...*

L'erreur indique que le fichier a été téléchargé sur MinIO et que le workflow d'ingestion des données a été déclenché, mais comme le chemin ne correspond à aucun ensemble de données dans l'instance wis2box, le mappage des données a échoué.

Vous pouvez également utiliser `sftp` depuis la ligne de commande :

```bash
sftp -P 8022 -oBatchMode=no -o StrictHostKeyChecking=no <mon-nom-d'hôte-ou-ip>
```
Connectez-vous en utilisant les identifiants définis dans `wis2box.env` pour les variables d'environnement `WIS2BOX_STORAGE_USERNAME` et `WIS2BOX_STORAGE_PASSWORD`, naviguez jusqu'au seau `wis2box-incoming` puis créez un répertoire et téléchargez un fichier comme suit :

```bash
cd wis2box-incoming
mkdir not-a-valid-path
cd not-a-valid-path
put ~/exercise-materials/data-ingest-exercises/synop.txt .
```

Cela entraînera une "erreur de validation du chemin" dans le tableau de bord Grafana indiquant que le fichier a été téléchargé sur MinIO.

Pour quitter le client sftp, tapez `exit`.

!!! Question "Ingérer des données dans MinIO en utilisant SFTP"

    Essayez d'ingérer le fichier `synop.txt` dans votre instance wis2box en utilisant SFTP pour déclencher le workflow d'ingestion des données.

    Vérifiez l'interface utilisateur MinIO pour voir si le fichier a été téléchargé dans le chemin correct dans le seau `wis2box-incoming`.
    
    Vérifiez le tableau de bord Grafana pour voir si le workflow d'ingestion des données a été déclenché ou s'il y avait des erreurs.

 Pour vous assurer que vos données sont correctement ingérées, assurez-vous que le fichier est téléchargé dans le seau `wis2box-incoming` dans un répertoire qui correspond à l'identifiant de l'ensemble de données ou au sujet de votre ensemble de données.

## Conclusion

!!! success "Félicitations !"
    Dans cette session pratique, vous avez appris à :

    - déclencher le workflow wis2box en utilisant un script Python et le client Python MinIO
    - utiliser différents plugins de données pour ingérer différents formats de données
    - télécharger des données sur MinIO en utilisant SFTP
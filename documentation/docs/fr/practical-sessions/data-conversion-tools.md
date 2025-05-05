---
title: Outils de Conversion de Données
---

# Outils de Conversion de Données

!!! abstract "Objectifs d'apprentissage"
    À la fin de cette session pratique, vous serez capable de :

    - Accéder aux outils en ligne de commande ecCodes dans le conteneur wis2box-api
    - Utiliser l'outil synop2bufr pour convertir les messages FM-12 SYNOP en BUFR depuis la ligne de commande
    - Déclencher la conversion synop2bufr via wis2box-webapp
    - Utiliser l'outil csv2bufr pour convertir des données CSV en BUFR depuis la ligne de commande

## Introduction

Les données publiées sur WIS2 doivent répondre aux exigences et normes définies par les différentes communautés d'experts des disciplines du système terrestre. Pour réduire les obstacles à la publication des données d'observations de surface terrestres, wis2box fournit des outils pour convertir les données au format BUFR. Ces outils sont disponibles via le conteneur wis2box-api et peuvent être utilisés en ligne de commande pour tester le processus de conversion des données.

Les principales conversions actuellement prises en charge par wis2box sont la conversion des messages FM-12 SYNOP vers BUFR et des données CSV vers BUFR. Le format FM-12 est pris en charge car il est encore largement utilisé et échangé dans la communauté OMM, tandis que le format CSV est pris en charge pour permettre la correspondance des données produites par les stations météorologiques automatiques vers le format BUFR.

### À propos de FM-12 SYNOP

Les rapports météorologiques de surface des stations terrestres ont historiquement été transmis toutes les heures ou aux heures synoptiques principales (00, 06, 12 et 18 UTC) et intermédiaires (03, 09, 15, 21 UTC). Avant la migration vers BUFR, ces rapports étaient encodés dans le format texte FM-12 SYNOP. Bien que la migration vers BUFR devait être achevée en 2012, un grand nombre de rapports sont encore échangés dans le format FM-12 SYNOP traditionnel. Plus d'informations sur le format FM-12 SYNOP peuvent être trouvées dans le Manuel des Codes de l'OMM, Volume I.1 (OMM-N° 306, Volume I.1).

### À propos d'ecCodes

La bibliothèque ecCodes est un ensemble de bibliothèques logicielles et d'utilitaires conçus pour décoder et encoder des données météorologiques aux formats GRIB et BUFR. Elle est développée par le Centre européen pour les prévisions météorologiques à moyen terme (CEPMMT), voir la [documentation ecCodes](https://confluence.ecmwf.int/display/ECC/ecCodes+documentation) pour plus d'informations.

Le logiciel wis2box inclut la bibliothèque ecCodes dans l'image de base du conteneur wis2box-api. Cela permet aux utilisateurs d'accéder aux outils en ligne de commande et aux bibliothèques depuis le conteneur. La bibliothèque ecCodes est utilisée dans la pile wis2box pour décoder et encoder les messages BUFR.

### À propos de csv2bufr et synop2bufr

En plus d'ecCodes, wis2box utilise les modules Python suivants qui fonctionnent avec ecCodes pour convertir les données au format BUFR :

- **synop2bufr** : pour prendre en charge le format FM-12 SYNOP traditionnel utilisé par les observateurs manuels. Le module synop2bufr s'appuie sur des métadonnées de station supplémentaires pour encoder des paramètres additionnels dans le fichier BUFR. Voir le [dépôt synop2bufr sur GitHub](https://github.com/World-Meteorological-Organization/synop2bufr)
- **csv2bufr** : pour permettre la conversion des extraits CSV produits par les stations météorologiques automatiques au format BUFR. Le module csv2bufr est utilisé pour convertir les données CSV au format BUFR en utilisant un modèle de correspondance qui définit comment les données CSV doivent être mappées au format BUFR. Voir le [dépôt csv2bufr sur GitHub](https://github.com/World-Meteorological-Organization/csv2bufr)

Ces modules peuvent être utilisés de manière autonome ou dans le cadre de la pile wis2box.

## Préparation

!!! warning "Prérequis"

    - Assurez-vous que votre wis2box a été configuré et démarré
    - Assurez-vous d'avoir configuré un jeu de données et au moins une station dans votre wis2box
    - Connectez-vous au broker MQTT de votre instance wis2box en utilisant MQTT Explorer
    - Ouvrez l'application web wis2box (`http://YOUR-HOST/wis2box-webapp`) et assurez-vous d'être connecté
    - Ouvrez le tableau de bord Grafana de votre instance en allant sur `http://YOUR-HOST:3000`

Pour utiliser les outils BUFR en ligne de commande, vous devrez être connecté au conteneur wis2box-api. Sauf indication contraire, toutes les commandes doivent être exécutées sur ce conteneur. Vous devrez également avoir MQTT Explorer ouvert et connecté à votre broker.

Tout d'abord, connectez-vous à votre VM étudiant via votre client SSH et copiez les matériels d'exercice dans le conteneur wis2box-api :

```bash
docker cp ~/exercise-materials/data-conversion-exercises wis2box-api:/root
```

Ensuite, connectez-vous au conteneur wis2box-api et changez pour le répertoire où se trouvent les matériels d'exercice :

```bash
cd ~/wis2box
python3 wis2box-ctl.py login wis2box-api
cd /root/data-conversion-exercises
```

Confirmez que les outils sont disponibles, en commençant par ecCodes :

```bash
bufr_dump -V
```

Vous devriez obtenir la réponse suivante :

```
ecCodes Version 2.36.0
```

Ensuite, vérifiez la version de synop2bufr :

```bash
synop2bufr --version
```

Vous devriez obtenir la réponse suivante :

```
synop2bufr, version 0.7.0
```

Ensuite, vérifiez csv2bufr :

```bash
csv2bufr --version
```

Vous devriez obtenir la réponse suivante :

```
csv2bufr, version 0.8.5
```

## Outils en ligne de commande ecCodes

La bibliothèque ecCodes incluse dans le conteneur wis2box-api fournit plusieurs outils en ligne de commande pour travailler avec les fichiers BUFR. 
Les exercices suivants montrent comment utiliser `bufr_ls` et `bufr_dump` pour vérifier le contenu d'un fichier BUFR.

### bufr_ls

Dans ce premier exercice, vous utiliserez la commande `bufr_ls` pour inspecter les en-têtes d'un fichier BUFR et déterminer le type de contenu du fichier.

Utilisez la commande suivante pour exécuter `bufr_ls` sur le fichier `bufr-cli-ex1.bufr4` :

```bash
bufr_ls bufr-cli-ex1.bufr4
```

Vous devriez voir la sortie suivante :

```bash
bufr-cli-ex1.bufr4
centre                     masterTablesVersionNumber  localTablesVersionNumber   typicalDate                typicalTime                numberOfSubsets
cnmc                       29                         0                          20231002                   000000                     1
1 of 1 messages in bufr-cli-ex1.bufr4

1 of 1 total messages in 1 file
```

Diverses options peuvent être passées à `bufr_ls` pour modifier à la fois le format et les champs d'en-tête affichés.

!!! question
     
    Quelle serait la commande pour lister la sortie précédente au format JSON ?

    Vous pouvez exécuter la commande `bufr_ls` avec l'option `-h` pour voir les options disponibles.

??? success "Cliquez pour révéler la réponse"
    Vous pouvez changer le format de sortie en JSON en utilisant l'option `-j`, c'est-à-dire
    ```bash
    bufr_ls -j bufr-cli-ex1.bufr4
    ```

    Une fois exécutée, cela devrait vous donner la sortie suivante :
    ```
    { "messages" : [
      {
        "centre": "cnmc",
        "masterTablesVersionNumber": 29,
        "localTablesVersionNumber": 0,
        "typicalDate": 20231002,
        "typicalTime": "000000",
        "numberOfSubsets": 1
      }
    ]}
    ```

La sortie imprimée représente les valeurs de certaines clés d'en-tête dans le fichier BUFR.

À elle seule, cette information n'est pas très informative, avec seulement des informations limitées sur le contenu du fichier.

Lors de l'examen d'un fichier BUFR, nous voulons souvent déterminer le type de données contenues dans le fichier et la date/heure typique des données dans le fichier. Ces informations peuvent être listées en utilisant l'option `-p` pour sélectionner les en-têtes à afficher. Plusieurs en-têtes peuvent être inclus en utilisant une liste séparée par des virgules.

Vous pouvez utiliser la commande suivante pour lister la catégorie de données, la sous-catégorie, la date et l'heure typiques :
    
```bash
bufr_ls -p dataCategory,internationalDataSubCategory,typicalDate,typicalTime -j bufr-cli-ex1.bufr4
```

!!! question

    Exécutez la commande précédente et interprétez la sortie en utilisant le [Tableau commun de codes C-13](https://github.com/wmo-im/CCT/blob/master/C13.csv) pour déterminer la catégorie et la sous-catégorie de données.

    Quel type de données (catégorie et sous-catégorie) est contenu dans le fichier ? Quelle est la date et l'heure typiques pour les données ?

??? success "Cliquez pour révéler la réponse"
    
    ```
    { "messages" : [
      {
        "dataCategory": 2,
        "internationalDataSubCategory": 4,
        "typicalDate": 20231002,
        "typicalTime": "000000"
      }
    ]}
    ```

    De cela, nous voyons que :

    - La catégorie de données est 2, indiquant des données de **"Sondages verticaux (autres que satellite)"**.
    - La sous-catégorie internationale est 4, indiquant des **"Rapports de température/humidité/vent en altitude provenant de stations terrestres fixes (TEMP)"**.
    - La date et l'heure typiques sont respectivement le 2023-10-02 et 00:00:00z.

### bufr_dump

La commande `bufr_dump` peut être utilisée pour lister et examiner le contenu d'un fichier BUFR, y compris les données elles-mêmes.

Essayez d'exécuter la commande `bufr_dump` sur le deuxième fichier exemple `bufr-cli-ex2.bufr4` :

```{.copy}
bufr_dump bufr-cli-ex2.bufr4
```

Cela donne un JSON qui peut être difficile à analyser, essayez d'utiliser l'option `-p` pour afficher les données en texte brut (format clé=valeur) :

```{.copy}
bufr_dump -p bufr-cli-ex2.bufr4
```

Vous verrez un grand nombre de clés en sortie, dont beaucoup sont manquantes. C'est typique avec des données réelles car toutes les clés eccodes ne sont pas remplies avec des données rapportées.

Vous pouvez utiliser la commande `grep` pour filtrer la sortie et n'afficher que les clés qui ne sont pas manquantes. Par exemple, pour afficher toutes les clés qui ne sont pas manquantes, vous pouvez utiliser la commande suivante :

```{.copy}
bufr_dump -p bufr-cli-ex2.bufr4 | grep -v MISSING
```

!!! question

    Quelle est la pression réduite au niveau moyen de la mer rapportée dans le fichier BUFR `bufr-cli-ex2.bufr4` ?

??? success "Cliquez pour révéler la réponse"

    En utilisant la commande suivante :

    ```bash
    bufr_dump -p bufr-cli-ex2.bufr4 | grep -i 'pressureReducedToMeanSeaLevel'
    ```

    Vous devriez voir la sortie suivante :

    ```
    pressureReducedToMeanSeaLevel=105590
    ```
    Cela indique que la pression réduite au niveau moyen de la mer est de 105590 Pa (1055,90 hPa).

!!! question

    Quel est l'identifiant de station WIGOS de la station qui a rapporté les données dans le fichier BUFR `bufr-cli-ex2.bufr4` ?

??? success "Cliquez pour révéler la réponse"

    En utilisant la commande suivante :

    ```bash
    bufr_dump -p bufr-cli-ex2.bufr4 | grep -i 'wigos'
    ```

    Vous devriez voir la sortie suivante :

    ```
    wigosIdentifierSeries=0
    wigosIssuerOfIdentifier=20000
    wigosIssueNumber=0
    wigosLocalIdentifierCharacter="99100"
    ```

    Cela indique que l'identifiant de station WIGOS est `0-20000-0-99100`.

## Conversion synop2bufr

Maintenant, examinons comment convertir les données FM-12 SYNOP au format BUFR en utilisant le module `synop2bufr`. Le module `synop2bufr` est utilisé pour convertir les données FM-12 SYNOP au format BUFR. Le module est installé dans le conteneur wis2box-api et peut être utilisé depuis la ligne de commande comme suit :

```{.copy}
synop2bufr data transform \
    --metadata <station-metadata.csv> \
    --output-dir <output-directory-path> \
    --year <year-of-observation> \
    --month <month-of-observation> \
    <input-fm12.txt>
```

L'argument `--metadata` est utilisé pour spécifier le fichier de métadonnées de station, qui fournit des informations supplémentaires à encoder dans le fichier BUFR.
L'argument `--output-dir` est utilisé pour spécifier le répertoire où les fichiers BUFR convertis seront écrits. Les arguments `--year` et `--month` sont utilisés pour spécifier l'année et le mois de l'observation.

Le module `synop2bufr` est également utilisé dans
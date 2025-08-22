---
title: Outils de Conversion de Données
---

# Outils de Conversion de Données

!!! abstract "Objectifs d'apprentissage"
    À la fin de cette session pratique, vous serez capable de :

    - Accéder aux outils en ligne de commande ecCodes dans le conteneur wis2box-api
    - Utiliser l'outil synop2bufr pour convertir des rapports FM-12 SYNOP en BUFR depuis la ligne de commande
    - Déclencher la conversion synop2bufr via l'application wis2box-webapp
    - Utiliser l'outil csv2bufr pour convertir des données CSV en BUFR depuis la ligne de commande

## Introduction

Les données publiées sur WIS2 doivent répondre aux exigences et normes définies par les différentes communautés d'experts en disciplines et domaines du système terrestre. Afin de réduire les obstacles à la publication de données pour les observations de surface terrestres, wis2box fournit des outils pour convertir les données au format BUFR. Ces outils sont disponibles via le conteneur wis2box-api et peuvent être utilisés depuis la ligne de commande pour tester le processus de conversion des données.

Les principales conversions actuellement prises en charge par wis2box sont les rapports FM-12 SYNOP en BUFR et les données CSV en BUFR. Les données FM-12 sont prises en charge car elles sont encore largement utilisées et échangées dans la communauté de l'OMM, tandis que les données CSV sont prises en charge pour permettre le mappage des données produites par des stations météorologiques automatiques au format BUFR.

### À propos de FM-12 SYNOP

Les rapports météorologiques de surface provenant des stations terrestres ont historiquement été rapportés toutes les heures ou aux heures synoptiques principales (00, 06, 12 et 18 UTC) et intermédiaires (03, 09, 15, 21 UTC). Avant la migration vers BUFR, ces rapports étaient encodés dans le format texte FM-12 SYNOP. Bien que la migration vers BUFR ait été prévue pour être achevée en 2012, un grand nombre de rapports sont encore échangés dans l'ancien format FM-12 SYNOP. Des informations supplémentaires sur le format FM-12 SYNOP peuvent être trouvées dans le Manuel de l'OMM sur les codes, Volume I.1 (OMM-No. 306, Volume I.1).

### À propos d'ecCodes

La bibliothèque ecCodes est un ensemble de bibliothèques logicielles et d'utilitaires conçus pour décoder et encoder des données météorologiques aux formats GRIB et BUFR. Elle est développée par le Centre Européen pour les Prévisions Météorologiques à Moyen Terme (ECMWF). Consultez la [documentation ecCodes](https://confluence.ecmwf.int/display/ECC/ecCodes+documentation) pour plus d'informations.

Le logiciel wis2box inclut la bibliothèque ecCodes dans l'image de base du conteneur wis2box-api. Cela permet aux utilisateurs d'accéder aux outils en ligne de commande et aux bibliothèques depuis le conteneur. La bibliothèque ecCodes est utilisée dans la pile wis2box pour décoder et encoder les messages BUFR.

### À propos de csv2bufr et synop2bufr

En plus d'ecCodes, wis2box utilise les modules Python suivants qui fonctionnent avec ecCodes pour convertir les données au format BUFR :

- **synop2bufr** : pour prendre en charge le format FM-12 SYNOP traditionnellement utilisé par les observateurs manuels. Le module synop2bufr s'appuie sur des métadonnées supplémentaires des stations pour encoder des paramètres supplémentaires dans le fichier BUFR. Voir le [référentiel synop2bufr sur GitHub](https://github.com/World-Meteorological-Organization/synop2bufr)
- **csv2bufr** : pour permettre la conversion des extractions CSV produites par des stations météorologiques automatiques au format BUFR. Le module csv2bufr est utilisé pour convertir les données CSV en format BUFR à l'aide d'un modèle de mappage qui définit comment les données CSV doivent être mappées au format BUFR. Voir le [référentiel csv2bufr sur GitHub](https://github.com/World-Meteorological-Organization/csv2bufr)

Ces modules peuvent être utilisés de manière autonome ou dans le cadre de la pile wis2box.

## Préparation

!!! warning "Prérequis"

    - Assurez-vous que votre wis2box est configuré et démarré
    - Assurez-vous d'avoir configuré un jeu de données et au moins une station dans votre wis2box
    - Connectez-vous au courtier MQTT de votre instance wis2box à l'aide de MQTT Explorer
    - Ouvrez l'application web wis2box (`http://YOUR-HOST/wis2box-webapp`) et assurez-vous d'être connecté
    - Ouvrez le tableau de bord Grafana de votre instance en accédant à `http://YOUR-HOST:3000`

Pour utiliser les outils BUFR en ligne de commande, vous devrez être connecté au conteneur wis2box-api. Sauf indication contraire, toutes les commandes doivent être exécutées sur ce conteneur. Vous devrez également avoir MQTT Explorer ouvert et connecté à votre courtier.

Tout d'abord, connectez-vous à votre machine virtuelle étudiante via votre client SSH et copiez les matériaux d'exercice dans le conteneur wis2box-api :

```bash
docker cp ~/exercise-materials/data-conversion-exercises wis2box-api:/root
```

Ensuite, connectez-vous au conteneur wis2box-api et accédez au répertoire où se trouvent les matériaux d'exercice :

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
csv2bufr, version 0.8.6
```

## Outils en ligne de commande ecCodes

La bibliothèque ecCodes incluse dans le conteneur wis2box-api fournit un certain nombre d'outils en ligne de commande pour travailler avec les fichiers BUFR. 
Les exercices suivants démontrent comment utiliser `bufr_ls` et `bufr_dump` pour vérifier le contenu d'un fichier BUFR.

### bufr_ls

Dans cet exercice, vous utiliserez la commande `bufr_ls` pour inspecter les en-têtes d'un fichier BUFR et déterminer le type de contenu du fichier.

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
    Vous pouvez changer le format de sortie en JSON en utilisant l'option `-j`, c'est-à-dire :
    ```bash
    bufr_ls -j bufr-cli-ex1.bufr4
    ```

    Lors de l'exécution, cela devrait vous donner la sortie suivante :
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

Vous pouvez utiliser la commande suivante pour lister la catégorie de données, la sous-catégorie, la date typique et l'heure typique :
    
```bash
bufr_ls -p dataCategory,internationalDataSubCategory,typicalDate,typicalTime -j bufr-cli-ex1.bufr4
```

!!! question

    Exécutez la commande précédente et interprétez la sortie en utilisant la [Table de codes communs C-13](https://github.com/wmo-im/CCT/blob/master/C13.csv) pour déterminer la catégorie et la sous-catégorie des données.

    Quel type de données (catégorie et sous-catégorie) est contenu dans le fichier ? Quelle est la date et l'heure typiques des données ?

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

    À partir de cela, nous voyons que :

- La catégorie de données est 2, indiquant des données **"Sondages verticaux (autres que satellites)"**.
- La sous-catégorie internationale est 4, indiquant des données **"Rapports de température/humidité/vent en altitude provenant de stations fixes terrestres (TEMP)"**.
- La date et l'heure typiques sont respectivement 2023-10-02 et 00:00:00z.

### bufr_dump

La commande `bufr_dump` peut être utilisée pour lister et examiner le contenu d'un fichier BUFR, y compris les données elles-mêmes.

Essayez d'exécuter la commande `bufr_dump` sur le deuxième fichier d'exemple `bufr-cli-ex2.bufr4` :

```{.copy}
bufr_dump bufr-cli-ex2.bufr4
```

Cela produit un JSON qui peut être difficile à analyser. Essayez d'utiliser l'option `-p` pour afficher les données en texte brut (format clé=valeur) :

```{.copy}
bufr_dump -p bufr-cli-ex2.bufr4
```

Vous verrez un grand nombre de clés en sortie, dont beaucoup sont manquantes. Cela est typique des données du monde réel, car toutes les clés `eccodes` ne sont pas toujours renseignées avec des données signalées.

Vous pouvez utiliser la commande `grep` pour filtrer la sortie et afficher uniquement les clés qui ne sont pas manquantes. Par exemple, pour afficher toutes les clés non manquantes, vous pouvez utiliser la commande suivante :

```{.copy}
bufr_dump -p bufr-cli-ex2.bufr4 | grep -v MISSING
```

!!! question

    Quelle est la pression réduite au niveau moyen de la mer signalée dans le fichier BUFR `bufr-cli-ex2.bufr4` ?

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

    Quel est l'identifiant de station WIGOS de la station ayant signalé les données dans le fichier BUFR `bufr-cli-ex2.bufr4` ?

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

Ensuite, examinons comment convertir des données FM-12 SYNOP au format BUFR en utilisant le module `synop2bufr`. Le module `synop2bufr` est utilisé pour convertir des données FM-12 SYNOP au format BUFR. Ce module est installé dans le conteneur wis2box-api et peut être utilisé en ligne de commande comme suit :

```{.copy}
synop2bufr data transform \
    --metadata <station-metadata.csv> \
    --output-dir <output-directory-path> \
    --year <year-of-observation> \
    --month <month-of-observation> \
    <input-fm12.txt>
```

L'argument `--metadata` est utilisé pour spécifier le fichier de métadonnées des stations, qui fournit des informations supplémentaires à encoder dans le fichier BUFR.  
L'argument `--output-dir` est utilisé pour spécifier le répertoire où les fichiers BUFR convertis seront écrits. Les arguments `--year` et `--month` sont utilisés pour spécifier l'année et le mois de l'observation.

Le module `synop2bufr` est également utilisé dans l'application wis2box-webapp pour convertir des données FM-12 SYNOP au format BUFR via un formulaire web.

Les exercices suivants démontreront comment fonctionne le module `synop2bufr` et comment l'utiliser pour convertir des données FM-12 SYNOP au format BUFR.

### Examiner le message SYNOP d'exemple

Inspectez le fichier de message SYNOP d'exemple pour cet exercice `synop_message.txt` :

```bash
cd /root/data-conversion-exercises
more synop_message.txt
```

!!! question

    Combien de rapports SYNOP se trouvent dans ce fichier ?

??? success "Cliquez pour révéler la réponse"
    
    La sortie montre ce qui suit :

    ```{.copy}
    AAXX 21121
    15015 02999 02501 10103 21090 39765 42952 57020 60001=
    15020 02997 23104 10130 21075 30177 40377 58020 60001 81041=
    15090 02997 53102 10139 21075 30271 40364 58031 60001 82046=
    ```

    Il y a 3 rapports SYNOP dans le fichier, correspondant à 3 stations différentes (identifiées par les identifiants traditionnels à 5 chiffres : 15015, 15020 et 15090).  
    Notez que la fin de chaque rapport est marquée par le caractère `=`.

### Examiner la liste des stations

L'argument `--metadata` nécessite un fichier CSV utilisant un format prédéfini. Un exemple fonctionnel est fourni dans le fichier `station_list.csv` :

Utilisez la commande suivante pour inspecter le contenu du fichier `station_list.csv` :

```bash
more station_list.csv
```

!!! question

    Combien de stations sont listées dans la liste des stations ? Quels sont les identifiants de station WIGOS des stations ?

??? success "Cliquez pour révéler la réponse"

    La sortie montre ce qui suit :

    ```{.copy}
    station_name,wigos_station_identifier,traditional_station_identifier,facility_type,latitude,longitude,elevation,barometer_height,territory_name,wmo_region
    OCNA SUGATAG,0-20000-0-15015,15015,landFixed,47.7770616258,23.9404602638,503.0,504.0,ROU,europe
    BOTOSANI,0-20000-0-15020,15020,landFixed,47.7356532437,26.6455501701,161.0,162.1,ROU,europe
    ```

    Cela correspond aux métadonnées des stations pour 2 stations : avec les identifiants de station WIGOS `0-20000-0-15015` et `0-20000-0-15020`.

### Convertir SYNOP en BUFR

Ensuite, utilisez la commande suivante pour convertir le message FM-12 SYNOP au format BUFR :

```bash
synop2bufr data transform --metadata station_list.csv --output-dir ./ --year 2024 --month 09 synop_message.txt
```

!!! question
    Combien de fichiers BUFR ont été créés ? Que signifie le message WARNING dans la sortie ?

??? success "Cliquez pour révéler la réponse"
    La sortie montre ce qui suit :

    ```{.copy}
    [WARNING] Station 15090 not found in station file
    ```

    Si vous vérifiez le contenu de votre répertoire avec la commande `ls -lh`, vous devriez voir que 2 nouveaux fichiers BUFR ont été créés : `WIGOS_0-20000-0-15015_20240921T120000.bufr4` et `WIGOS_0-20000-0-15020_20240921T120000.bufr4`.

    Le message d'avertissement indique que la station avec l'identifiant traditionnel `15090` n'a pas été trouvée dans le fichier de liste des stations `station_list.csv`. Cela signifie que le rapport SYNOP pour cette station n'a pas été converti au format BUFR.

!!! question
    Vérifiez le contenu du fichier BUFR `WIGOS_0-20000-0-15015_20240921T120000.bufr4` en utilisant la commande `bufr_dump`.

    Pouvez-vous vérifier que les informations fournies dans le fichier `station_list.csv` sont présentes dans le fichier BUFR ?

??? success "Cliquez pour révéler la réponse"
    Vous pouvez utiliser la commande suivante pour vérifier le contenu du fichier BUFR :

    ```bash
    bufr_dump -p WIGOS_0-20000-0-15015_20240921T120000.bufr4 | grep -v MISSING
    ```

    Vous noterez la sortie suivante :

    ```{.copy}
    wigosIdentifierSeries=0
    wigosIssuerOfIdentifier=20000
    wigosIssueNumber=0
    wigosLocalIdentifierCharacter="15015"
    blockNumber=15
    stationNumber=15
    stationOrSiteName="OCNA SUGATAG"
    stationType=1
    year=2024
    month=9
    day=21
    hour=12
    minute=0
    latitude=47.7771
    longitude=23.9405
    heightOfStationGroundAboveMeanSeaLevel=503
    heightOfBarometerAboveMeanSeaLevel=504
    ```

    Notez que cela inclut les données fournies par le fichier `station_list.csv`.

### Formulaire SYNOP dans wis2box-webapp

Le module `synop2bufr` est également utilisé dans le `wis2box-webapp` pour convertir les données FM-12 SYNOP au format BUFR à l'aide d'un formulaire web.  
Pour tester cela, accédez à `http://YOUR-HOST/wis2box-webapp` et connectez-vous.

Sélectionnez le `SYNOP Form` dans le menu à gauche et copiez-collez le contenu du fichier `synop_message.txt` :

```{.copy}
AAXX 21121
15015 02999 02501 10103 21090 39765 42952 57020 60001=
15020 02997 23104 10130 21075 30177 40377 58020 60001 81041=
15090 02997 53102 10139 21075 30271 40364 58031 60001 82046=
```

Dans la zone de texte `SYNOP message` :

<img alt="synop-form" src="/../assets/img/wis2box-webapp-synop-form.png" width="800">

!!! question
    Pouvez-vous soumettre le formulaire ? Quel est le résultat ?

??? success "Cliquez pour révéler la réponse"

    Vous devez sélectionner un jeu de données et fournir le jeton pour "processes/wis2box" que vous avez créé dans l'exercice précédent pour soumettre le formulaire.

    Si vous fournissez un jeton invalide, vous verrez :
    
    - Résultat : Non autorisé, veuillez fournir un jeton valide pour 'processes/wis2box'

    Si vous fournissez un jeton valide, vous verrez "WARNINGS: 3". Cliquez sur "WARNINGS" pour ouvrir le menu déroulant qui affichera :

    - Station 15015 non trouvée dans le fichier des stations
    - Station 15020 non trouvée dans le fichier des stations
    - Station 15090 non trouvée dans le fichier des stations

    Pour convertir ces données au format BUFR, vous devrez configurer les stations correspondantes dans votre wis2box et vous assurer que les stations sont associées au sujet de votre jeu de données.

!!! note

    Dans l'exercice [ingesting-data-for-publication](./ingesting-data-for-publication.md), vous avez ingéré le fichier "synop_202412030900.txt" et il a été converti au format BUFR par le module synop2bufr.

    Dans le flux de travail automatisé de wis2box, l'année et le mois sont automatiquement extraits du nom de fichier et utilisés pour remplir les arguments `--year` et `--month` requis par synop2bufr, tandis que les métadonnées des stations sont automatiquement extraites de la configuration des stations dans wis2box.

## Conversion csv2bufr

!!! note
    Assurez-vous que vous êtes toujours connecté au conteneur wis2box-api et dans le répertoire `/root/data-conversion-exercises`. Si vous avez quitté le conteneur lors de l'exercice précédent, vous pouvez vous reconnecter comme suit :

    ```bash
    cd ~/wis2box
    python3 wis2box-ctl.py login wis2box-api
    cd /root/data-conversion-exercises
    ```

Voyons maintenant comment convertir des données CSV au format BUFR à l'aide du module `csv2bufr`. Le module est installé dans le conteneur wis2box-api et peut être utilisé en ligne de commande comme suit :

```{.copy}
csv2bufr data transform \
    --bufr-template <bufr-mapping-template> \
    <input-csv-file>
```

L'argument `--bufr-template` est utilisé pour spécifier le fichier modèle de mappage BUFR, qui fournit le mappage entre les données CSV d'entrée et les données BUFR de sortie, spécifié dans un fichier JSON. Les modèles de mappage par défaut sont installés dans le répertoire `/opt/csv2bufr/templates` dans le conteneur wis2box-api.

### Examiner le fichier CSV d'exemple

Examinez le contenu du fichier CSV d'exemple `aws-example.csv` :

```bash
more aws-example.csv
```

!!! question
    Combien de lignes de données contient le fichier CSV ? Quel est l'identifiant de station WIGOS des stations rapportées dans le fichier CSV ?

??? question "Cliquez pour révéler la réponse"

    La sortie montre ce qui suit :

    ```{.copy}
    wsi_series,wsi_issuer,wsi_issue_number,wsi_local,wmo_block_number,wmo_station_number,station_type,year,month,day,hour,minute,latitude,longitude,station_height_above_msl,barometer_height_above_msl,station_pressure,msl_pressure,geopotential_height,thermometer_height,air_temperature,dewpoint_temperature,relative_humidity,method_of_ground_state_measurement,ground_state,method_of_snow_depth_measurement,snow_depth,precipitation_intensity,anemometer_height,time_period_of_wind,wind_direction,wind_speed,maximum_wind_gust_direction_10_minutes,maximum_wind_gust_speed_10_minutes,maximum_wind_gust_direction_1_hour,maximum_wind_gust_speed_1_hour,maximum_wind_gust_direction_3_hours,maximum_wind_gust_speed_3_hours,rain_sensor_height,total_precipitation_1_hour,total_precipitation_3_hours,total_precipitation_6_hours,total_precipitation_12_hours,total_precipitation_24_hours
    0,20000,0,60355,60,355,1,2024,3,31,1,0,47.77706163,23.94046026,503,504.43,100940,101040,1448,5,298.15,294.55,80,3,1,1,0,0.004,10,-10,30,3,30,5,40,9,20,11,2,4.7,5.3,7.9,9.5,11.4
    0,20000,0,60355,60,355,1,2024,3,31,2,0,47.77706163,23.94046026,503,504.43,100940,101040,1448,5,25.,294.55,80,3,1,1,0,0.004,10,-10,30,3,30,5,40,9,20,11,2,4.7,5.3,7.9,9.5,11.4
    0,20000,0,60355,60,355,1,2024,3,31,3,0,47.77706163,23.94046026,503,504.43,100940,101040,1448,5,298.15,294.55,80,3,1,1,0,0.004,10,-10,30,3,30,5,40,9,20,11,2,4.7,5.3,7.9,9.5,11.4
    ```

    La première ligne du fichier CSV contient les en-têtes de colonnes, qui sont utilisés pour identifier les données dans chaque colonne.

    Après la ligne d'en-tête, il y a 3 lignes de données, représentant 3 observations météorologiques de la même station avec l'identifiant de station WIGOS `0-20000-0-60355` à trois horodatages différents : `2024-03-31 01:00:00`, `2024-03-31 02:00:00` et `2024-03-31 03:00:00`.

### Examiner le aws-template

Le conteneur wis2box-api inclut un ensemble de modèles de mappage BUFR prédéfinis installés dans le répertoire `/opt/csv2bufr/templates`.

Vérifiez le contenu du répertoire `/opt/csv2bufr/templates` :

```bash
ls /opt/csv2bufr/templates
```

Vous devriez voir la sortie suivante :

```{.copy}
CampbellAfrica-v1-template.json  aws-template.json  daycli-template.json
```

Examinons le contenu du fichier `aws-template.json` :

```bash
cat /opt/csv2bufr/templates/aws-template.json
```

Cela renvoie un fichier JSON volumineux, fournissant le mappage pour 43 colonnes CSV.

!!! question
    Quelle colonne CSV est mappée à la clé eccodes `airTemperature` ? Quelles sont les valeurs minimales et maximales valides pour cette clé ?

??? success "Cliquez pour révéler la réponse"

    Utilisez la commande suivante pour filtrer la sortie :

    ```bash
    cat /opt/csv2bufr/templates/aws-template.json | grep -i airTemperature
    ```
    Vous devriez voir la sortie suivante :

    ```{.copy}
    {"eccodes_key": "#1#airTemperature", "value": "data:air_temperature", "valid_min": "const:193.15", "valid_max": "const:333.15"},
    ```

    La valeur qui sera encodée pour la clé eccodes `airTemperature` sera extraite des données dans la colonne CSV : **air_temperature**.

    Les valeurs minimales et maximales pour cette clé sont respectivement `193.15` et `333.15`.

!!! question

    Quelle colonne CSV est mappée à la clé eccodes `internationalDataSubCategory` ? Quelle est la valeur de cette clé ?

??? success "Cliquez pour révéler la réponse"
    Utilisez la commande suivante pour filtrer la sortie :

    ```bash
    cat /opt/csv2bufr/templates/aws-template.json | grep -i internationalDataSubCategory
    ```
    Vous devriez voir la sortie suivante :

    ```{.copy}
    {"eccodes_key": "internationalDataSubCategory", "value": "const:2"},
    ```

**Il n'existe pas de colonne CSV mappée à la clé eccodes `internationalDataSubCategory`**, à la place, la valeur constante 2 est utilisée et sera encodée dans tous les fichiers BUFR produits avec ce modèle de mappage.

### convertir un fichier CSV en BUFR

Essayons de convertir le fichier au format BUFR en utilisant la commande `csv2bufr` :

```{.copy}
csv2bufr data transform --bufr-template aws-template ./aws-example.csv
```

!!! question
    Combien de fichiers BUFR ont été créés ?

??? success "Cliquez pour révéler la réponse"

    La sortie affiche ce qui suit :

    ```{.copy}
    CLI:    ... Transformation de ./aws-example.csv en BUFR ...
    CLI:    ... Traitement des sous-ensembles :
    CLI:    ..... 384 octets écrits dans ./WIGOS_0-20000-0-60355_20240331T010000.bufr4
    #1#airTemperature: Valeur (25.0) hors de la plage valide (193.15 - 333.15).; Élément défini comme manquant
    CLI:    ..... 384 octets écrits dans ./WIGOS_0-20000-0-60355_20240331T020000.bufr4
    CLI:    ..... 384 octets écrits dans ./WIGOS_0-20000-0-60355_20240331T030000.bufr4
    CLI:    Fin du traitement, sortie.
    ```

    La sortie indique que 3 fichiers BUFR ont été créés : `WIGOS_0-20000-0-60355_20240331T010000.bufr4`, `WIGOS_0-20000-0-60355_20240331T020000.bufr4` et `WIGOS_0-20000-0-60355_20240331T030000.bufr4`.

Pour vérifier le contenu des fichiers BUFR tout en ignorant les valeurs manquantes, vous pouvez utiliser la commande suivante :

```bash
bufr_dump -p WIGOS_0-20000-0-60355_20240331T010000.bufr4 | grep -v MISSING
```

!!! question
    Quelle est la valeur de la clé eccodes `airTemperature` dans le fichier BUFR `WIGOS_0-20000-0-60355_20240331T010000.bufr4` ? Et dans le fichier BUFR `WIGOS_0-20000-0-60355_20240331T020000.bufr4` ?

??? success "Cliquez pour révéler la réponse"
    Pour filtrer la sortie, vous pouvez utiliser la commande suivante :

    ```bash
    bufr_dump -p WIGOS_0-20000-0-60355_20240331T010000.bufr4 | grep -v MISSING | grep airTemperature
    ```
    Vous devriez voir la sortie suivante :

    ```{.copy}
    #1#airTemperature=298.15
    ```

    Tandis que pour le second fichier :

    ```bash
    bufr_dump -p WIGOS_0-20000-0-60355_20240331T020000.bufr4 | grep -v MISSING | grep airTemperature
    ```

    Vous n'obtenez aucun résultat, ce qui indique que la valeur pour la clé `airTemperature` est manquante dans le fichier BUFR `WIGOS_0-20000-0-60355_20240331T020000.bufr4`. Le programme csv2bufr a refusé d'encoder la valeur `25.0` provenant des données CSV car elle est hors de la plage valide de `193.15` à `333.15` définie dans le modèle de mappage.

Notez que la conversion de CSV en BUFR à l'aide d'un des modèles de mappage BUFR prédéfinis présente des limitations :

- le fichier CSV doit être au format défini dans le modèle de mappage, c'est-à-dire que les noms des colonnes CSV doivent correspondre aux noms définis dans le modèle de mappage
- vous ne pouvez encoder que les clés définies dans le modèle de mappage
- les contrôles qualité sont limités aux vérifications définies dans le modèle de mappage

Pour des informations sur la création et l'utilisation de modèles de mappage BUFR personnalisés, consultez l'exercice pratique suivant [csv2bufr-templates](./csv2bufr-templates.md).

## Conclusion

!!! success "Félicitations !"
    Au cours de cette session pratique, vous avez appris :

    - comment accéder aux outils en ligne de commande ecCodes dans le conteneur wis2box-api
    - comment utiliser `synop2bufr` pour convertir des rapports FM-12 SYNOP en BUFR depuis la ligne de commande
    - comment utiliser le formulaire SYNOP dans l'application wis2box-webapp pour convertir des rapports FM-12 SYNOP en BUFR
    - comment utiliser `csv2bufr` pour convertir des données CSV en BUFR depuis la ligne de commande
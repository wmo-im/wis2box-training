---
title: Modèles de mappage CSV-vers-BUFR
---

# Modèles de mappage CSV-vers-BUFR

!!! abstract "Objectifs d'apprentissage"
    À la fin de cette session pratique, vous serez capable de :

    - créer un nouveau modèle de mappage BUFR pour vos données CSV
    - modifier et déboguer votre modèle de mappage BUFR personnalisé depuis la ligne de commande
    - configurer le plugin de données CSV-vers-BUFR pour utiliser un modèle de mappage BUFR personnalisé
    - utiliser les modèles intégrés AWS et DAYCLI pour convertir des données CSV en BUFR

## Introduction

Les fichiers de données au format CSV (valeurs séparées par des virgules) sont souvent utilisés pour enregistrer des données d'observation et autres sous un format tabulaire. La plupart des enregistreurs de données utilisés pour collecter les sorties des capteurs peuvent exporter les observations dans des fichiers délimités, y compris au format CSV. De même, lorsqu'on ingère des données dans une base de données, il est facile d'exporter les données nécessaires dans des fichiers au format CSV.

Le module `wis2box csv2bufr` fournit un outil en ligne de commande pour convertir des données CSV au format BUFR. Lors de l'utilisation de `csv2bufr`, vous devez fournir un modèle de mappage BUFR qui associe les colonnes CSV aux éléments BUFR correspondants. Si vous ne souhaitez pas créer votre propre modèle de mappage, vous pouvez utiliser les modèles intégrés AWS et DAYCLI pour convertir des données CSV en BUFR, mais vous devrez vous assurer que les données CSV que vous utilisez sont au format correct pour ces modèles. Si vous souhaitez décoder des paramètres qui ne sont pas inclus dans les modèles AWS et DAYCLI, vous devrez créer votre propre modèle de mappage.

Dans cette session, vous apprendrez à créer votre propre modèle de mappage pour convertir des données CSV en BUFR. Vous apprendrez également à utiliser les modèles intégrés AWS et DAYCLI pour convertir des données CSV en BUFR.

## Préparation

Assurez-vous que `wis2box-stack` a été démarré avec la commande `python3 wis2box.py start`.

Assurez-vous d'avoir un navigateur web ouvert avec l'interface utilisateur MinIO pour votre instance en accédant à `http://YOUR-HOST:9000`. Si vous ne vous souvenez pas de vos identifiants MinIO, vous pouvez les trouver dans le fichier `wis2box.env` dans le répertoire `wis2box` sur votre machine virtuelle étudiante.

Assurez-vous que `MQTT Explorer` est ouvert et connecté à votre broker en utilisant les identifiants `everyone/everyone`.

## Création d'un modèle de mappage

Le module `csv2bufr` est livré avec un outil en ligne de commande permettant de créer votre propre modèle de mappage en utilisant un ensemble de séquences BUFR et/ou d'éléments BUFR comme entrée.

Pour trouver des séquences et éléments BUFR spécifiques, vous pouvez consulter les tables BUFR à l'adresse [https://confluence.ecmwf.int/display/ECC/BUFR+tables](https://confluence.ecmwf.int/display/ECC/BUFR+tables).

### Outil en ligne de commande csv2bufr mappings

Pour accéder à l'outil en ligne de commande `csv2bufr`, vous devez vous connecter au conteneur `wis2box-api` :

```bash
cd ~/wis2box
python3 wis2box-ctl.py login wis2box-api
```

Pour afficher la page d'aide de la commande `csv2bufr mapping` :

```bash
csv2bufr mappings --help
```

La page d'aide affiche deux sous-commandes :

- `csv2bufr mappings create` : Créer un nouveau modèle de mappage
- `csv2bufr mappings list` : Lister les modèles de mappage disponibles dans le système

!!! Note "csv2bufr mapping list"

    La commande `csv2bufr mapping list` affichera les modèles de mappage disponibles dans le système.  
    Les modèles par défaut sont stockés dans le répertoire `/opt/wis2box/csv2bufr/templates` dans le conteneur.

    Pour partager des modèles de mappage personnalisés avec le système, vous pouvez les stocker dans le répertoire défini par `$CSV2BUFR_TEMPLATES`, qui est défini par défaut à `/data/wis2box/mappings` dans le conteneur. Étant donné que le répertoire `/data/wis2box/mappings` dans le conteneur est monté sur le répertoire `$WIS2BOX_HOST_DATADIR/mappings` sur l'hôte, vous trouverez vos modèles de mappage personnalisés dans le répertoire `$WIS2BOX_HOST_DATADIR/mappings` sur l'hôte.

Essayons de créer un nouveau modèle de mappage personnalisé en utilisant la commande `csv2bufr mapping create` avec comme entrée la séquence BUFR 301150 et l'élément BUFR 012101.

```bash
csv2bufr mappings create 301150 012101 --output /data/wis2box/mappings/my_custom_template.json
```

Vous pouvez vérifier le contenu du modèle de mappage que vous venez de créer en utilisant la commande `cat` :

```bash
cat /data/wis2box/mappings/my_custom_template.json
```

!!! question "Inspection du modèle de mappage"

    Combien de colonnes CSV sont mappées aux éléments BUFR ? Quel est l'en-tête CSV pour chaque élément BUFR mappé ?

??? success "Cliquez pour révéler la réponse"
    
    Le modèle de mappage que vous avez créé mappe **5** colonnes CSV aux éléments BUFR, à savoir les 4 éléments BUFR de la séquence 301150 plus l'élément BUFR 012101. 

    Les colonnes CSV suivantes sont mappées aux éléments BUFR :

    - **wigosIdentifierSeries** est mappé à `"eccodes_key": "#1#wigosIdentifierSeries"` (élément BUFR 001125)
    - **wigosIssuerOfIdentifier** est mappé à `"eccodes_key": "#1#wigosIssuerOfIdentifier"` (élément BUFR 001126)
    - **wigosIssueNumber** est mappé à `"eccodes_key": "#1#wigosIssueNumber"` (élément BUFR 001127)
    - **wigosLocalIdentifierCharacter** est mappé à `"eccodes_key": "#1#wigosLocalIdentifierCharacter"` (élément BUFR 001128)
    - **airTemperature** est mappé à `"eccodes_key": "#1#airTemperature"` (élément BUFR 012101)

Le modèle de mappage que vous avez créé manque des métadonnées importantes sur l'observation effectuée, la date et l'heure de l'observation, ainsi que la latitude et la longitude de la station.

Ensuite, nous allons mettre à jour le modèle de mappage et ajouter les séquences suivantes :
    
- **301011** pour la date (année, mois, jour)
- **301012** pour l'heure (heure, minute)
- **301023** pour la localisation (latitude/longitude avec précision approximative)

Et les éléments suivants :

- **010004** pour la pression
- **007031** pour la hauteur du baromètre au-dessus du niveau moyen de la mer

Exécutez la commande suivante pour mettre à jour le modèle de mappage :

```bash
csv2bufr mappings create 301150 301011 301012 301023 007031 012101 010004 --output /data/wis2box/mappings/my_custom_template.json
```

Et inspectez à nouveau le contenu du modèle de mappage :

```bash
cat /data/wis2box/mappings/my_custom_template.json
```

!!! question "Inspection du modèle de mappage mis à jour"

    Combien de colonnes CSV sont maintenant mappées aux éléments BUFR ? Quel est l'en-tête CSV pour chaque élément BUFR mappé ?

??? success "Cliquez pour révéler la réponse"
    
    Le modèle de mappage que vous avez créé mappe maintenant **18** colonnes CSV aux éléments BUFR :
    - 4 éléments BUFR de la séquence BUFR 301150
    - 3 éléments BUFR de la séquence BUFR 301011
    - 2 éléments BUFR de la séquence BUFR 301012
    - 2 éléments BUFR de la séquence BUFR 301023
    - L'élément BUFR 007031
    - L'élément BUFR 012101

    Les colonnes CSV suivantes sont mappées aux éléments BUFR :

    - **wigosIdentifierSeries** est mappé à `"eccodes_key": "#1#wigosIdentifierSeries"` (élément BUFR 001125)
    - **wigosIssuerOfIdentifier** est mappé à `"eccodes_key": "#1#wigosIssuerOfIdentifier"` (élément BUFR 001126)
    - **wigosIssueNumber** est mappé à `"eccodes_key": "#1#wigosIssueNumber"` (élément BUFR 001127)
    - **wigosLocalIdentifierCharacter** est mappé à `"eccodes_key": "#1#wigosLocalIdentifierCharacter"` (élément BUFR 001128)
    - **year** est mappé à `"eccodes_key": "#1#year"` (élément BUFR 004001)
    - **month** est mappé à `"eccodes_key": "#1#month"` (élément BUFR 004002)
    - **day** est mappé à `"eccodes_key": "#1#day"` (élément BUFR 004003)
    - **hour** est mappé à `"eccodes_key": "#1#hour"` (élément BUFR 004004)
    - **minute** est mappé à `"eccodes_key": "#1#minute"` (élément BUFR 004005)
    - **latitude** est mappé à `"eccodes_key": "#1#latitude"` (élément BUFR 005002)
    - **longitude** est mappé à `"eccodes_key": "#1#longitude"` (élément BUFR 006002)
    - **heightOfBarometerAboveMeanSeaLevel** est mappé à `"eccodes_key": "#1#heightOfBarometerAboveMeanSeaLevel"` (élément BUFR 007031)
    - **airTemperature** est mappé à `"eccodes_key": "#1#airTemperature"` (élément BUFR 012101)
    - **nonCoordinatePressure** est mappé à `"eccodes_key": "#1#nonCoordinatePressure"` (élément BUFR 010004)

Vérifiez le contenu du fichier `custom_template_data.csv` dans le répertoire `/tmp/data-conversion-exercises` :

```bash
cat /tmp/data-conversion-exercises/custom_template_data.csv
```

Notez que les en-têtes de ce fichier CSV sont identiques aux en-têtes CSV du modèle de mappage que vous avez créé.

Pour tester la conversion des données, nous pouvons utiliser l'outil en ligne de commande `csv2bufr` pour convertir le fichier CSV en BUFR en utilisant le modèle de mappage que nous avons créé :

```bash
csv2bufr data transform --bufr-template my_custom_template /tmp/data-conversion-exercises/custom_template_data.csv
```

Vous devriez voir la sortie suivante :

```bash
CLI:    ... Transforming /tmp/data-conversion-exercises/custom_template_data.csv to BUFR ...
CLI:    ... Processing subsets:
CLI:    ..... 94 bytes written to ./WIGOS_0-20000-0-15015_20250412T210000.bufr4
CLI:    End of processing, exiting.
```

!!! question "Vérifiez le contenu du fichier BUFR"
    
    Comment pouvez-vous vérifier le contenu du fichier BUFR que vous venez de créer et vous assurer qu'il a correctement encodé les données ?

??? success "Cliquez pour révéler la réponse"

    Vous pouvez utiliser la commande `bufr_dump -p` pour vérifier le contenu du fichier BUFR que vous venez de créer. 
    Cette commande affichera le contenu du fichier BUFR dans un format lisible par un humain.

    ```bash
    bufr_dump -p ./WIGOS_0-20000-0-15015_20250412T210000.bufr4
    ```

    Dans la sortie, vous verrez les valeurs des éléments BUFR que vous avez mappés dans le modèle, par exemple "airTemperature" affichera :
    
    ```bash
    airTemperature=298.15
    ```

Vous pouvez maintenant quitter le conteneur :

```bash
exit
```

### Utilisation du modèle de mappage dans le wis2box

Pour vous assurer que le nouveau modèle de mappage est reconnu par le conteneur wis2box-api, vous devez redémarrer le conteneur :

```bash
docker restart wis2box-api
```

Vous pouvez maintenant configurer votre jeu de données dans le wis2box-webapp pour utiliser le modèle de mappage personnalisé pour le plugin de conversion CSV en BUFR.

Le wis2box-webapp détectera automatiquement le modèle de mappage que vous avez créé et le rendra disponible dans la liste des modèles pour le plugin de conversion CSV en BUFR.

Cliquez sur le jeu de données que vous avez créé lors de la session pratique précédente et cliquez sur "UPDATE" à côté du plugin nommé "CSV data converted to BUFR" :

<img alt="Image montrant l'éditeur de jeu de données dans le wis2box-webapp" src="/../assets/img/wis2box-webapp-data-mapping-update-csv2bufr.png"/>

Vous devriez voir le nouveau modèle que vous avez créé dans la liste des modèles disponibles :

<img alt="Image montrant les modèles csv2bufr dans le wis2box-webapp" src="/../assets/img/wis2box-webapp-csv2bufr-templates.png"/>

!!! hint

    Notez que si vous ne voyez pas le nouveau modèle que vous avez créé, essayez de rafraîchir la page ou de l'ouvrir dans une nouvelle fenêtre de navigation privée.

Pour l'instant, conservez la sélection par défaut du modèle AWS (cliquez en haut à droite pour fermer la configuration du plugin).

## Utilisation du modèle 'AWS'

Le modèle 'AWS' fournit un modèle de mappage pour convertir les données CSV en séquence BUFR 301150, 307096, en support des exigences minimales de GBON.

La description du modèle AWS peut être trouvée ici [aws-template](./../csv2bufr-templates/aws-template.md).

### Examiner les données d'entrée aws-example

Téléchargez l'exemple pour cet exercice à partir du lien ci-dessous :

[aws-example.csv](./../sample-data/aws-example.csv)

Ouvrez le fichier que vous avez téléchargé dans un éditeur et inspectez le contenu :

!!! question
    En examinant les champs date, heure et identifiants (WIGOS et identifiants traditionnels), que remarquez-vous ? Comment la date d'aujourd'hui serait-elle représentée ?

??? success "Cliquez pour révéler la réponse"
    Chaque colonne contient une seule information. Par exemple, la date est divisée en année, mois et jour, reflétant la manière dont les données sont stockées dans BUFR. La date d'aujourd'hui serait répartie sur les colonnes "year", "month" et "day". De même, l'heure doit être divisée en "hour" et "minute", et l'identifiant de station WIGOS dans ses composants respectifs.

!!! question
    En regardant le fichier de données, comment les données manquantes sont-elles encodées ?
    
??? success "Cliquez pour révéler la réponse"
    Les données manquantes dans le fichier sont représentées par des cellules vides. Dans un fichier CSV, cela serait encodé par ``,,``. Notez qu'il s'agit d'une cellule vide et non d'une chaîne de longueur nulle, par exemple ``,"",``.

!!! hint "Données manquantes"
    Il est reconnu que des données peuvent manquer pour diverses raisons, qu'il s'agisse d'une défaillance du capteur ou d'un paramètre non observé. Dans ces cas, les données manquantes peuvent être encodées comme indiqué ci-dessus, les autres données du rapport restant valides.

### Mettre à jour le fichier exemple

Mettez à jour le fichier exemple que vous avez téléchargé pour utiliser la date et l'heure d'aujourd'hui et modifiez les identifiants de station WIGOS pour utiliser des stations que vous avez enregistrées dans le wis2box-webapp.

### Téléchargez les données dans MinIO et vérifiez le résultat

Accédez à l'interface utilisateur de MinIO et connectez-vous en utilisant les identifiants du fichier `wis2box.env`.

Accédez à **wis2box-incoming** et cliquez sur le bouton "Create new path" :

<img alt="Image montrant l'interface utilisateur de MinIO avec le bouton créer un nouveau chemin mis en évidence" src="/../assets/img/minio-create-new-path.png"/>

Créez un nouveau dossier dans le bucket MinIO qui correspond à l'identifiant du jeu de données que vous avez créé avec le modèle='weather/surface-weather-observations/synop' :

<img alt="Image montrant l'interface utilisateur de MinIO avec le bouton créer un nouveau chemin mis en évidence" src="/../assets/img/minio-create-new-path-metadata_id.png"/>

Téléchargez le fichier exemple que vous avez téléchargé dans le dossier que vous avez créé dans le bucket MinIO :

<img alt="Image montrant l'interface utilisateur de MinIO avec aws-example téléchargé" src="/../assets/img/minio-upload-aws-example.png"/></center>

Vérifiez le tableau de bord Grafana à `http://YOUR-HOST:3000` pour voir s'il y a des WARNINGS ou des ERRORS. Si vous en voyez, essayez de les corriger et répétez l'exercice.

Vérifiez MQTT Explorer pour voir si vous recevez des notifications de données WIS2.

Si vous avez ingéré les données avec succès, vous devriez voir 3 notifications dans MQTT Explorer sur le sujet `origin/a/wis2/<centre-id>/data/weather/surface-weather-observations/synop` pour les 3 stations pour lesquelles vous avez signalé des données :

<img width="450" alt="Image montrant MQTT Explorer après le téléchargement AWS" src="/../assets/img/mqtt-explorer-aws-upload.png"/>

## Utilisation du modèle 'DayCLI'

Le modèle **DayCLI** fournit un modèle de mappage pour convertir les données climatiques quotidiennes CSV en séquence BUFR 307075, en support du rapport des données climatiques quotidiennes.

La description du modèle DAYCLI peut être trouvée ici [daycli-template](./../csv2bufr-templates/daycli-template.md).

Pour partager ces données sur WIS2, vous devrez créer un nouveau jeu de données dans le wis2box-webapp qui a la hiérarchie correcte du sujet WIS2 et qui utilise le modèle DAYCLI pour convertir les données CSV en BUFR.

### Création d'un jeu de données wis2box pour publier des messages DAYCLI

Accédez à l'éditeur de jeu de données dans le wis2box-webapp et créez un nouveau jeu de données. Utilisez le même centre-id que dans les sessions pratiques précédentes et sélectionnez **Data Type='climate/surface-based-observations/daily'** :

<img alt="Créer un nouveau jeu de données dans le wis2box-webapp pour DAYCLI" src="/../assets/img/wis2box-webapp-create-dataset-daycli.png"/>

Cliquez sur "CONTINUE TO FORM" et ajoutez une description pour votre jeu de données, définissez la boîte englobante et fournissez les informations de contact pour le jeu de données. Une fois que vous avez rempli toutes les sections, cliquez sur 'VALIDATE FORM' et vérifiez le formulaire.

Examinez les plugins de données pour les jeux de données. Cliquez sur "UPDATE" à côté du plugin nommé "CSV data converted to BUFR" et vous verrez que le modèle est défini sur **DayCLI** :

<img alt="Mettre à jour le plugin de données pour le jeu de données afin d'utiliser le modèle DAYCLI" src="/../assets/img/wis2box-webapp-update-data-plugin-daycli.png"/>

Fermez la configuration du plugin et soumettez le formulaire en utilisant le jeton d'authentification que vous avez créé lors de la session pratique précédente.

Vous devriez maintenant avoir un deuxième jeu de données dans le wis2box-webapp configuré pour utiliser le modèle DAYCLI pour convertir les données CSV en BUFR.

### Examiner les données d'entrée daycli-example

Téléchargez l'exemple pour cet exercice à partir du lien ci-dessous :

[daycli-example.csv](./../sample-data/daycli-example.csv)

Ouvrez le fichier que vous avez téléchargé dans un éditeur et inspectez le contenu :

!!! question
    Quelles variables supplémentaires sont incluses dans le modèle daycli ?

??? success "Cliquez pour révéler la réponse"
    Le modèle daycli inclut des métadonnées importantes sur l'emplacement des instruments et les classifications de qualité des mesures pour la température et l'humidité, des indicateurs de contrôle qualité et des informations sur la manière dont la température moyenne quotidienne a été calculée.

### Mettre à jour le fichier exemple

Le fichier exemple contient une ligne de données pour chaque jour d'un mois et rapporte des données pour une station. Mettez à jour le fichier exemple que vous avez téléchargé pour utiliser la date et l'heure d'aujourd'hui et modifiez les identifiants de station WIGOS pour utiliser une station que vous avez enregistrée dans le wis2box-webapp.

### Téléchargez les données dans MinIO et vérifiez le résultat
```

Comme précédemment, vous devrez télécharger les données dans le bucket 'wis2box-incoming' de MinIO pour qu'elles soient traitées par le convertisseur csv2bufr. Cette fois, vous devrez créer un nouveau dossier dans le bucket MinIO correspondant à l'identifiant du jeu de données (dataset-id) pour le jeu de données que vous avez créé avec le template='climate/surface-based-observations/daily', qui sera différent de l'identifiant du jeu de données utilisé dans l'exercice précédent :

<img alt="Image montrant l'interface utilisateur de MinIO avec DAYCLI-example téléchargé" src="/../assets/img/minio-upload-daycli-example.png"/></center>

Après avoir téléchargé les données, vérifiez qu'il n'y a pas d'AVERTISSEMENTS (WARNINGS) ou d'ERREURS (ERRORS) dans le tableau de bord Grafana et consultez MQTT Explorer pour vérifier si vous recevez des notifications de données WIS2.

Si vous avez ingéré les données avec succès, vous devriez voir 30 notifications dans MQTT Explorer sur le sujet `origin/a/wis2/<centre-id>/data/climate/surface-based-observations/daily` pour les 30 jours du mois pour lesquels vous avez signalé des données :

<img width="450" alt="Image montrant MQTT Explorer après le téléchargement de DAYCLI" src="/../assets/img/mqtt-daycli-template-success.png"/>

## Conclusion

!!! success "Félicitations"
    Au cours de cette session pratique, vous avez appris :

    - comment créer un modèle de mappage personnalisé pour convertir des données CSV en BUFR
    - comment utiliser les modèles intégrés AWS et DAYCLI pour convertir des données CSV en BUFR
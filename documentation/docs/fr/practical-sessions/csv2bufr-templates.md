---
title: Modèles de mappage de CSV à BUFR
---

# Modèles de mappage de CSV à BUFR

!!! abstract "Résultats d'apprentissage"
    À la fin de cette session pratique, vous serez capable de :

    - créer un nouveau modèle de mappage BUFR pour vos données CSV
    - éditer et déboguer votre modèle de mappage BUFR personnalisé depuis la ligne de commande
    - configurer le plugin de données CSV à BUFR pour utiliser un modèle de mappage BUFR personnalisé
    - utiliser les modèles intégrés AWS et DAYCLI pour convertir des données CSV en BUFR

## Introduction

Les fichiers de données à valeurs séparées par des virgules (CSV) sont souvent utilisés pour enregistrer des données observationnelles et autres dans un format tabulaire.
La plupart des enregistreurs de données utilisés pour enregistrer la sortie des capteurs sont capables d'exporter les observations dans des fichiers délimités, y compris en CSV.
De même, lorsque les données sont ingérées dans une base de données, il est facile d'exporter les données requises dans des fichiers formatés CSV.

Le module csv2bufr de wis2box fournit un outil en ligne de commande pour convertir les données CSV en format BUFR. Lorsque vous utilisez csv2bufr, vous devez fournir un modèle de mappage BUFR qui mappe les colonnes CSV aux éléments BUFR correspondants. Si vous ne souhaitez pas créer votre propre modèle de mappage, vous pouvez utiliser les modèles intégrés AWS et DAYCLI pour convertir des données CSV en BUFR, mais vous devrez vous assurer que les données CSV que vous utilisez sont dans le format correct pour ces modèles. Si vous souhaitez décoder des paramètres qui ne sont pas inclus dans les modèles AWS et DAYCLI, vous devrez créer votre propre modèle de mappage.

Dans cette session, vous apprendrez à créer votre propre modèle de mappage pour convertir des données CSV en BUFR. Vous apprendrez également à utiliser les modèles intégrés AWS et DAYCLI pour convertir des données CSV en BUFR.

## Préparation

Assurez-vous que la pile wis2box a été démarrée avec `python3 wis2box.py start`

Assurez-vous que vous avez un navigateur web ouvert avec l'interface utilisateur MinIO pour votre instance en allant à `http://YOUR-HOST:9000`
Si vous ne vous souvenez pas de vos identifiants MinIO, vous pouvez les trouver dans le fichier `wis2box.env` dans le répertoire `wis2box` sur votre VM étudiant.

Assurez-vous que vous avez MQTT Explorer ouvert et connecté à votre courtier en utilisant les identifiants `everyone/everyone`.

## Création d'un modèle de mappage

Le module csv2bufr est livré avec un outil en ligne de commande pour créer votre propre modèle de mappage en utilisant un ensemble de séquences BUFR et/ou d'élément BUFR en entrée.

Pour trouver des séquences et des éléments BUFR spécifiques, vous pouvez vous référer aux tables BUFR à [https://confluence.ecmwf.int/display/ECC/BUFR+tables](https://confluence.ecmwf.int/display/ECC/BUFR+tables).

### Outil en ligne de commande csv2bufr mappings

Pour accéder à l'outil en ligne de commande csv2bufr, vous devez vous connecter au conteneur wis2box-api :

```bash
cd ~/wis2box
python3 wis2box-ctl.py login wis2box-api
```

Pour afficher la page d'aide de la commande `csv2bufr mapping` :

```bash
csv2bufr mappings --help
```

La page d'aide montre 2 sous-commandes :

- `csv2bufr mappings create` : Créer un nouveau modèle de mappage
- `csv2bufr mappings list` : Lister les modèles de mappage disponibles dans le système

!!! Note "liste de mappage csv2bufr"

    La commande `csv2bufr mapping list` vous montrera les modèles de mappage disponibles dans le système.
    Les modèles par défaut sont stockés dans le répertoire `/opt/wis2box/csv2bufr/templates` dans le conteneur.

    Pour partager des modèles de mappage personnalisés avec le système, vous pouvez les stocker dans le répertoire défini par `$CSV2BUFR_TEMPLATES`, qui est défini sur `/data/wis2box/mappings` par défaut dans le conteneur. Étant donné que le répertoire `/data/wis2box/mappings` dans le conteneur est monté sur le répertoire `$WIS2BOX_HOST_DATADIR/mappings` sur l'hôte, vous trouverez vos modèles de mappage personnalisés dans le répertoire `$WIS2BOX_HOST_DATADIR/mappings` sur l'hôte.

Essayons de créer un nouveau modèle de mappage personnalisé en utilisant la commande `csv2bufr mapping create` en utilisant comme entrée la séquence BUFR 301150 plus l'élément BUFR 012101.

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

    - **wigosIdentifierSeries** mappe à `"eccodes_key": "#1#wigosIdentifierSeries"` (élément BUFR 001125)
    - **wigosIssuerOfIdentifier** mappe à `"eccodes_key": "#1#wigosIssuerOfIdentifier` (élément BUFR 001126)
    - **wigosIssueNumber** mappe à `"eccodes_key": "#1#wigosIssueNumber"` (élément BUFR 001127)
    - **wigosLocalIdentifierCharacter** mappe à `"eccodes_key": "#1#wigosLocalIdentifierCharacter"` (élément BUFR 001128)
    - **airTemperature** mappe à `"eccodes_key": "#1#airTemperature"` (élément BUFR 012101)

Le modèle de mappage que vous avez créé omet des métadonnées importantes sur l'observation effectuée, la date et l'heure de l'observation, et la latitude et la longitude de la station.

Ensuite, nous mettrons à jour le modèle de mappage et ajouterons les séquences suivantes :
    
- **301011** pour la date (année, mois, jour)
- **301012** pour l'heure (heure, minute)
- **301023** pour l'emplacement (latitude/longitude (précision grossière))

Et les éléments suivants :

- **010004** pour la pression
- **007031** pour la hauteur du baromètre au-dessus du niveau moyen de la mer

Exécutez la commande suivante pour mettre à jour le modèle de mappage :

```bash
csv2bufr mappings create 301150 301011 301012 301023 007031 012101 010004  --output /data/wis2box/mappings/my_custom_template.json
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
    - élément BUFR 007031
    - élément BUFR 012101

    Les colonnes CSV suivantes sont mappées aux éléments BUFR :

    - **wigosIdentifierSeries** mappe à `"eccodes_key": "#1#wigosIdentifierSeries"` (élément BUFR 001125)
    - **wigosIssuerOfIdentifier** mappe à `"eccodes_key": "#1#wigosIssuerOfIdentifier` (élément BUFR 001126)
    - **wigosIssueNumber** mappe à `"eccodes_key": "#1#wigosIssueNumber"` (élément BUFR 001127)
    - **wigosLocalIdentifierCharacter** mappe à `"eccodes_key": "#1#wigosLocalIdentifierCharacter"` (élément BUFR 001128)
    - **year** mappe à `"eccodes_key": "#1#year"` (élément BUFR 004001)
    - **month** mappe à `"eccodes_key": "#1#month"` (élément BUFR 004002)
    - **day** mappe à `"eccodes_key": "#1#day"` (élément BUFR 004003)
    - **hour** mappe à `"eccodes_key": "#1#hour"` (élément BUFR 004004)
    - **minute** mappe à `"eccodes_key": "#1#minute"` (élément BUFR 004005)
    - **latitude** mappe à `"eccodes_key": "#1#latitude"` (élément BUFR 005002)
    - **longitude** mappe à `"eccodes_key": "#1#longitude"` (élément BUFR 006002)
    - **heightOfBarometerAboveMeanSeaLevel"** mappe à `"eccodes_key": "#1#heightOfBarometerAboveMeanSeaLevel"` (élément BUFR 007031)
    - **airTemperature** mappe à `"eccodes_key": "#1#airTemperature"` (élément BUFR 012101)
    - **nonCoordinatePressure** mappe à `"eccodes_key": "#1#nonCoordinatePressure"` (élément BUFR 010004)

Vérifiez le contenu du fichier `custom_template_data.csv` dans le répertoire `/root/data-conversion-exercises` :

```bash
cat /root/data-conversion-exercises/custom_template_data.csv
```

Notez que les en-têtes de ce fichier CSV sont les mêmes que les en-têtes CSV dans le modèle de mappage que vous avez créé.

Pour tester la conversion des données, nous pouvons utiliser l'outil en ligne de commande `csv2bufr` pour convertir le fichier CSV en BUFR en utilisant le modèle de mappage que nous avons créé :

```bash
csv2bufr data transform --bufr-template my_custom_template /root/data-conversion-exercises/custom_template_data.csv
```

Vous devriez voir la sortie suivante :

```bash
CLI:    ... Transforming /root/data-conversion-exercises/custom_template_data.csv to BUFR ...
CLI:    ... Processing subsets:
CLI:    ..... 94 bytes written to ./WIGOS_0-20000-0-15015_20250412T210000.bufr4
CLI:    End of processing, exiting.
```

!!! question "Vérifiez le contenu du fichier BUFR"
    
    Comment pouvez-vous vérifier le contenu du fichier BUFR que vous venez de créer et vérifier qu'il a codé les données correctement ?

??? success "Cliquez pour révéler la réponse"

    Vous pouvez utiliser la commande `bufr_dump -p` pour vérifier le contenu du fichier BUFR que vous venez de créer.
    La commande vous montrera le contenu du fichier BUFR dans un format lisible par l'homme.

    ```bash
    bufr_dump -p ./WIGOS_0-20000-0-15015_20250412T210000.bufr4
    ```

    Dans la sortie, vous verrez des valeurs pour les éléments BUFR que vous avez mappés dans le modèle, par exemple la "température de l'air" affichera :
    
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

Cliquez sur le jeu de données que vous avez créé lors de la session pratique précédente et cliquez sur "MISE À JOUR" à côté du plugin avec le nom "Données CSV converties en BUFR" :

<img alt="Image montrant l'éditeur de jeu de données dans le wis2box-webapp" src="/../assets/img/wis2box-webapp-data-mapping-update-csv2bufr.png"/>

Vous devriez voir le nouveau modèle que vous avez créé dans la liste des modèles disponibles :

<img alt="Image montrant les modèles csv2bufr dans le wis2box-webapp" src="/../assets/img/wis2box-webapp-csv2bufr-templates.png"/>

!!! hint

    Notez que si vous ne voyez pas le nouveau modèle que vous avez créé, essayez de rafraîchir la page ou de l'ouvrir dans une nouvelle fenêtre en mode incognito.

Pour l'instant, conservez la sélection par défaut du modèle AWS (cliquez en haut à droite pour fermer la configuration du plugin).

## Utilisation du modèle 'AWS'

Le modèle 'AWS' fournit un modèle de mappage pour convertir des données CSV en séquence BUFR 301150, 307096, en soutien aux exigences minimales du GBON.

La description du modèle AWS peut être trouvée ici [modèle aws](./../csv2bufr-templates/aws-template.md).

### Examen des données d'entrée de l'exemple aws

Téléchargez l'exemple pour cet exercice à partir du lien ci-dessous :

[aws-example.csv](./../../sample-data/aws-example.csv)

Ouvrez le fichier que vous avez téléchargé dans un éditeur et inspectez le contenu :

!!! question
    En examinant les champs de date, d'heure et d'identité (identifiants WIGOS et traditionnels), que remarquez-vous ? Comment la date d'aujourd'hui serait-elle représentée ?

??? success "Cliquez pour révéler la réponse"
    Chaque colonne contient une seule information. Par exemple, la date est divisée en
    année, mois et jour, reflétant la façon dont les données sont stockées dans le BUFR. La date d'aujourd'hui serait 
    divisée entre les colonnes "année", "mois" et "jour". De même, l'heure doit être
    divisée en "heure" et "minute" et l'identifiant de la station WIGOS en ses composants respectifs.

!!! question
    En regardant le fichier de données, comment les données manquantes sont-elles codées ?
    
??? success "Cliquez pour révéler la réponse"
    Les données manquantes dans le fichier sont représentées par des cellules vides. Dans un fichier CSV, cela serait codé par ``,,``. Notez qu'il s'agit d'une cellule vide et non codée comme une chaîne de longueur zéro, 
    par exemple ``,"",``.

!!! hint "Données manquantes"
    Il est reconnu que les données peuvent manquer pour diverses raisons, que ce soit en raison d'une défaillance du capteur ou du paramètre non observé. Dans ces cas, les données manquantes peuvent être codées comme indiqué ci-dessus, les autres données du rapport restent valides.

### Mettre à jour le fichier exemple

Mettez à jour le fichier exemple que vous avez téléchargé pour utiliser la date et l'heure d'aujourd'hui et changez les identifiants de station WIGOS pour utiliser les stations que vous avez enregistrées dans le `wis2box-webapp`.

### Téléverser les données sur MinIO et vérifier le résultat

Naviguez vers l'interface utilisateur de MinIO et connectez-vous en utilisant les identifiants du fichier `wis2box.env`.

Naviguez vers le **wis2box-incoming** et cliquez sur le bouton "Créer un nouveau chemin" :

<img alt="Image montrant l'interface utilisateur de MinIO avec le bouton de création de dossier en surbrillance" src="/../assets/img/minio-create-new-path.png"/>

Créez un nouveau dossier dans le seau MinIO qui correspond à l'identifiant de l'ensemble de données que vous avez créé avec le modèle='weather/surface-weather-observations/synop' :

<img alt="Image montrant l'interface utilisateur de MinIO avec le bouton de création de dossier en surbrillance" src="/../assets/img/minio-create-new-path-metadata_id.png"/>

Téléversez le fichier exemple que vous avez téléchargé dans le dossier que vous avez créé dans le seau MinIO :

<img alt="Image montrant l'interface utilisateur de MinIO avec aws-example téléversé" src="/../assets/img/minio-upload-aws-example.png"/>

Vérifiez le tableau de bord Grafana à `http://YOUR-HOST:3000` pour voir s'il y a des AVERTISSEMENTS ou des ERREURS. Si vous en voyez, essayez de les corriger et répétez l'exercice.

Vérifiez le MQTT Explorer pour voir si vous recevez des notifications de données WIS2.

Si vous avez réussi à ingérer les données, vous devriez voir 3 notifications dans MQTT Explorer sur le sujet `origin/a/wis2/<centre-id>/data/weather/surface-weather-observations/synop` pour les 3 stations pour lesquelles vous avez rapporté des données :

<img width="450" alt="Image montrant MQTT Explorer après le téléversement AWS" src="/../assets/img/mqtt-explorer-aws-upload.png"/>

## Utilisation du modèle 'DayCLI'

Le modèle **DayCLI** fournit un modèle de mappage pour convertir les données CSV climatiques quotidiennes en séquence BUFR 307075, en soutien à la déclaration des données climatiques quotidiennes.

La description du modèle DAYCLI peut être trouvée ici [daycli-template](./../csv2bufr-templates/daycli-template.md).

Pour partager ces données sur WIS2, vous devrez créer un nouvel ensemble de données dans le `wis2box-webapp` qui a la bonne hiérarchie de sujets WIS2 et qui utilise le modèle DAYCLI pour convertir les données CSV en BUFR.

### Création d'un ensemble de données wis2box pour la publication des messages DAYCLI

Allez à l'éditeur d'ensembles de données dans le `wis2box-webapp` et créez un nouvel ensemble de données. Utilisez le même centre-id que dans les sessions pratiques précédentes et sélectionnez **Data Type='climate/surface-based-observations/daily'** :

<img alt="Créer un nouvel ensemble de données dans le wis2box-webapp pour DAYCLI" src="/../assets/img/wis2box-webapp-create-dataset-daycli.png"/>

Cliquez sur "CONTINUER VERS LE FORMULAIRE" et ajoutez une description pour votre ensemble de données, définissez la zone de délimitation et fournissez les informations de contact pour l'ensemble de données. Une fois que vous avez rempli toutes les sections, cliquez sur 'VALIDER LE FORMULAIRE' et vérifiez le formulaire.

Examinez les plugins de données pour les ensembles de données. Cliquez sur "MISE À JOUR" à côté du plugin avec le nom "Données CSV converties en BUFR" et vous verrez que le modèle est réglé sur **DayCLI** :

<img alt="Mettre à jour le plugin de données pour l'ensemble de données pour utiliser le modèle DAYCLI" src="/../assets/img/wis2box-webapp-update-data-plugin-daycli.png"/>

Fermez la configuration du plugin et soumettez le formulaire en utilisant le jeton d'authentification que vous avez créé lors de la session pratique précédente.

Vous devriez maintenant avoir un second ensemble de données dans le `wis2box-webapp` qui est configuré pour utiliser le modèle DAYCLI pour convertir les données CSV en BUFR.

### Examiner les données d'entrée de l'exemple daycli

Téléchargez l'exemple pour cet exercice à partir du lien ci-dessous :

[daycli-example.csv](./../../sample-data/daycli-example.csv)

Ouvrez le fichier que vous avez téléchargé dans un éditeur et inspectez le contenu :

!!! question
    Quelles variables supplémentaires sont incluses dans le modèle daycli ?

??? success "Cliquez pour révéler la réponse"
    Le modèle daycli inclut des métadonnées importantes sur l'emplacement des instruments et les classifications de la qualité des mesures pour la température et l'humidité, les drapeaux de contrôle de qualité et les informations sur la façon dont la température moyenne quotidienne a été calculée.

### Mettre à jour le fichier exemple

Le fichier exemple contient une ligne de données pour chaque jour d'un mois et rapporte des données pour une station. Mettez à jour le fichier exemple que vous avez téléchargé pour utiliser la date et l'heure d'aujourd'hui et changez les identifiants de station WIGOS pour utiliser une station que vous avez enregistrée dans le `wis2box-webapp`.

### Téléverser les données sur MinIO et vérifier le résultat

Comme auparavant, vous devrez téléverser les données dans le seau 'wis2box-incoming' de MinIO pour être traitées par le convertisseur csv2bufr. Cette fois, vous devrez créer un nouveau dossier dans le seau MinIO qui correspond à l'identifiant de l'ensemble de données que vous avez créé avec le modèle='climate/surface-based-observations/daily' qui sera différent de l'identifiant de l'ensemble de données que vous avez utilisé dans l'exercice précédent :

<img alt="Image montrant l'interface utilisateur de MinIO avec DAYCLI-example téléversé" src="/../assets/img/minio-upload-daycli-example.png"/>

Après avoir téléversé les données, vérifiez qu'il n'y a pas d'AVERTISSEMENTS ou d'ERREURS dans le tableau de bord Grafana et vérifiez le MQTT Explorer pour voir si vous recevez des notifications de données WIS2.

Si vous avez réussi à ingérer les données, vous devriez voir 30 notifications dans MQTT Explorer sur le sujet `origin/a/wis2/<centre-id>/data/climate/surface-based-observations/daily` pour les 30 jours du mois pour lesquels vous avez rapporté des données :

<img width="450" alt="Image montrant MQTT Explorer après le téléversement DAYCLI" src="/../assets/img/mqtt-daycli-template-success.png"/>

## Conclusion

!!! success "Félicitations"
    Dans cette session pratique, vous avez appris :

    - comment créer un modèle de mappage personnalisé pour convertir les données CSV en BUFR
    - comment utiliser les modèles intégrés AWS et DAYCLI pour convertir les données CSV en BUFR
---
title: Conversion des données SYNOP en BUFR
---

# Conversion des données SYNOP en BUFR depuis la ligne de commande

!!! abstract "Résultats d'apprentissage"
    À la fin de cette session pratique, vous serez capable de :

    - utiliser l'outil synop2bufr pour convertir les rapports SYNOP FM-12 en BUFR ;
    - diagnostiquer et corriger les erreurs de codage simples dans les rapports SYNOP FM-12 avant la conversion de format ;

## Introduction

Les rapports météorologiques de surface provenant des stations terrestres ont historiquement été rapportés chaque heure ou aux heures synoptiques principales
(00, 06, 12 et 18 UTC) et intermédiaires (03, 09, 15, 21 UTC). Avant la migration
vers le BUFR, ces rapports étaient codés dans le format de code SYNOP FM-12 en texte brut. Bien que la migration vers le BUFR
devait être achevée en 2012, un grand nombre de rapports sont encore échangés dans l'ancien format
SYNOP FM-12. Des informations supplémentaires sur le format SYNOP FM-12 peuvent être trouvées dans le Manuel des Codes de l'OMM, 
Volume I.1 (OMM-No. 306, Volume I.1).

[Manuel des Codes de l'OMM, Volume I.1](https://library.wmo.int/records/item/35713-manual-on-codes-international-codes-volume-i-1)

Pour aider à compléter la migration vers le BUFR, certains outils ont été développés pour
encoder les rapports SYNOP FM-12 en BUFR, dans cette session vous apprendrez à utiliser ces outils ainsi
que la relation entre les informations contenues dans les rapports SYNOP FM-12 et les messages BUFR.

## Préparation

!!! warning "Prérequis"

    - Assurez-vous que votre wis2box a été configuré et démarré.
    - Confirmez le statut en visitant l'API wis2box (``http://<votre-nom-d'hôte>/oapi``) et en vérifiant que l'API fonctionne.
    - Assurez-vous de lire les sections **synop2bufr primer** et **ecCodes primer** avant de commencer les exercices.

## synop2bufr primer

Ci-dessous, les commandes et configurations essentielles de `synop2bufr` :

### transform
La fonction `transform` convertit un message SYNOP en BUFR :

```bash
synop2bufr data transform --metadata my_file.csv --output-dir ./my_directory --year message_year --month message_month my_SYNOP.txt
```

Notez que si les options de métadonnées, de répertoire de sortie, d'année et de mois ne sont pas spécifiées, elles prendront leurs valeurs par défaut :

| Option      | Défaut |
| ----------- | ----------- |
| --metadata | station_list.csv |
| --output-dir | Le répertoire de travail actuel. |
| --year | L'année en cours. |
| --month | Le mois en cours. |

!!! note
    Il faut être prudent en utilisant l'année et le mois par défaut, car le jour du mois spécifié dans le rapport peut ne pas correspondre (par exemple, juin n'a pas 31 jours).

Dans les exemples, l'année et le mois ne sont pas donnés, alors n'hésitez pas à spécifier une date vous-même ou à utiliser les valeurs par défaut.

## ecCodes primer

ecCodes fournit à la fois des outils en ligne de commande et peut être intégré dans vos propres applications. Ci-dessous, quelques utilitaires en ligne de commande utiles pour travailler avec les données BUFR.

### bufr_dump

La commande `bufr_dump` est un outil générique d'information BUFR. Elle possède de nombreuses options, mais les suivantes seront les plus applicables aux exercices :

```bash
bufr_dump -p my_bufr.bufr4
```

Cela affichera le contenu BUFR sur votre écran. Si vous êtes intéressé par les valeurs prises par une variable en particulier, utilisez la commande `egrep` :

```bash
bufr_dump -p my_bufr.bufr4 | egrep -i temperature
```

Cela affichera les variables liées à la température dans vos données BUFR. Si vous souhaitez faire cela pour plusieurs types de variables, filtrez la sortie en utilisant un pipe (`|`) :

```bash
bufr_dump -p my_bufr.bufr4 | egrep -i 'temperature|wind'
```

## Conversion des rapports SYNOP FM-12 en BUFR en utilisant synop2bufr depuis la ligne de commande

La bibliothèque eccodes et le module synop2bufr sont installés dans le conteneur wis2box-api. Afin de réaliser les prochains exercices, nous copierons le répertoire synop2bufr-exercises dans le conteneur wis2box-api et exécuterons les exercices à partir de là.

```bash
docker cp ~/exercise-materials/synop2bufr-exercises wis2box-api:/root
```

Nous pouvons maintenant entrer dans le conteneur et exécuter les exercices :

```bash
docker exec -it wis2box-api /bin/bash
```

### Exercice 1
Naviguez jusqu'au répertoire `/root/synop2bufr-exercises/ex_1` et inspectez le fichier de message SYNOP message.txt :

```bash
cd /root/synop2bufr-exercises/ex_1
more message.txt
```

!!! question

    Combien de rapports SYNOP y a-t-il dans ce fichier ?

??? success "Cliquez pour révéler la réponse"
    
    Il y a 1 rapport SYNOP, car il n'y a qu'un seul délimiteur (=) à la fin du message.

Inspectez la liste des stations :

```bash
more station_list.csv
```

!!! question

    Combien de stations sont listées dans la liste des stations ?

??? success "Cliquez pour révéler la réponse"

    Il y a 1 station, le fichier station_list.csv contient une ligne de métadonnées de station.

!!! question
    Essayez de convertir `message.txt` en format BUFR.

??? success "Cliquez pour révéler la réponse"

    Pour convertir le message SYNOP en format BUFR, utilisez la commande suivante :

    ```bash
    synop2bufr data transform --metadata station_list.csv --output-dir ./ --year 2024 --month 09 message.txt
    ```

!!! tip

    Consultez la section [synop2bufr primer](#synop2bufr-primer).

Inspectez les données BUFR résultantes en utilisant `bufr_dump`.

!!! question
     Trouvez comment comparer les valeurs de latitude et de longitude à celles de la liste des stations.

??? success "Cliquez pour révéler la réponse"

    Pour comparer les valeurs de latitude et de longitude dans les données BUFR à celles de la liste des stations, utilisez la commande suivante :

    ```bash
    bufr_dump -p WIGOS_0-20000-0-15015_20240921T120000.bufr4 | egrep -i 'latitude|longitude'
    ```

    Cela affichera les valeurs de latitude et de longitude dans les données BUFR.

!!! tip

    Consultez la section [ecCodes primer](#eccodes-primer).

### Exercice 2
Naviguez jusqu'au répertoire `exercise-materials/synop2bufr-exercises/ex_2` et inspectez le fichier de message SYNOP message.txt :

```bash
cd /root/synop2bufr-exercises/ex_2
more message.txt
```

!!! question

    Combien de rapports SYNOP y a-t-il dans ce fichier ?

??? success "Cliquez pour révéler la réponse"

    Il y a 3 rapports SYNOP, car il y a 3 délimiteurs (=) à la fin du message.

Inspectez la liste des stations :

```bash
more station_list.csv
```

!!! question

    Combien de stations sont listées dans la liste des stations ?

??? success "Cliquez pour révéler la réponse"

    Il y a 3 stations, le fichier station_list.csv contient trois lignes de métadonnées de station.

!!! question
    Convertissez `message.txt` en format BUFR.

??? success "Cliquez pour révéler la réponse"

    Pour convertir le message SYNOP en format BUFR, utilisez la commande suivante :

    ```bash
    synop2bufr data transform --metadata station_list.csv --output-dir ./ --year 2024 --month 09 message.txt
    ```

!!! question

    En vous basant sur les résultats des exercices dans cette session et la précédente, comment prédiriez-vous le nombre de
    fichiers BUFR résultants basé sur le nombre de rapports SYNOP et de stations listées dans le fichier de métadonnées de station ?

??? success "Cliquez pour révéler la réponse"

    Pour voir les fichiers BUFR produits, exécutez la commande suivante :

    ```bash
    ls -l *.bufr4
    ```

    Le nombre de fichiers BUFR produits sera égal au nombre de rapports SYNOP dans le fichier de message.

Inspectez les données BUFR résultantes en utilisant `bufr_dump`.

!!! question
    Comment pouvez-vous vérifier l'ID de la Station WIGOS encodé à l'intérieur des données BUFR de chaque fichier produit ?

??? success "Cliquez pour révéler la réponse"

    Cela peut être fait en utilisant les commandes suivantes :

    ```bash
    bufr_dump -p WIGOS_0-20000-0-15015_20240921T120000.bufr4 | egrep -i 'wigos'
    ```

    ```bash
    bufr_dump -p WIGOS_0-20000-0-15020_20240921T120000.bufr4 | egrep -i 'wigos'
    ```

    ```bash
    bufr_dump -p WIGOS_0-20000-0-15090_20240921T120000.bufr4 | egrep -i 'wigos'
    ```

    Notez que si vous avez un répertoire avec juste ces 3 fichiers BUFR, vous pouvez utiliser les jokers Linux comme suit :

    ```bash
    bufr_dump -p *.bufr4 | egrep -i 'wigos'
    ```

### Exercice 3
Naviguez jusqu'au répertoire `exercise-materials/synop2bufr-exercises/ex_3` et inspectez le fichier de message SYNOP message.txt :

```bash
cd /root/synop2bufr-exercises/ex_3
more message.txt
```

Ce message SYNOP contient seulement un rapport plus long avec plus de sections.

Inspectez la liste des stations :

```bash
more station_list.csv
```

!!! question

    Est-ce problématique que ce fichier contienne plus de stations qu'il n'y a de rapports dans le message SYNOP ?

??? success "Cliquez pour révéler la réponse"

    Non, ce n'est pas un problème à condition qu'il existe une ligne dans le fichier de liste des stations avec un TSI de station correspondant à celui du rapport SYNOP que nous essayons de convertir.

!!! note

    Le fichier de liste des stations est une source de métadonnées pour `synop2bufr` afin de fournir les informations manquantes dans le rapport SYNOP alphanumérique et requises dans le SYNOP BUFR.

!!! question
    Convertissez `message.txt` en format BUFR.

??? success "Cliquez pour révéler la réponse"

    Ceci est fait en utilisant la commande `transform`, par exemple :

    ```bash
    synop2bufr data transform --metadata station_list.csv --output-dir ./ --year 2024 --month 09 message.txt
    ```

Inspectez les données BUFR résultantes en utilisant `bufr_dump`.

!!! question

    Trouvez les variables suivantes :

    - Température de l'air (K) du rapport
    - Couverture nuageuse totale (%) du rapport
    - Durée totale d'ensoleillement (minutes) du rapport
    - Vitesse du vent (m/s) du rapport

??? success "Cliquez pour révéler la réponse"

    Pour trouver les variables par mot-clé dans les données BUFR, vous pouvez utiliser les commandes suivantes :

    ```bash
    bufr_dump -p WIGOS_0-20000-0-15260_20240921T115500.bufr4 | egrep -i 'temperature'
    ```

    Vous pouvez utiliser la commande suivante pour rechercher plusieurs mots-clés :

    ```bash
    bufr_dump -p WIGOS_0-20000-0-15260_20240921T115500.bufr4 | egrep -i 'temperature|cover|sunshine|wind'
    ```

!!! tip

    Vous pouvez trouver la dernière commande de la section [ecCodes primer](#eccodes-primer) utile.


### Exercice 4
Naviguez jusqu'au répertoire `exercise-materials/synop2bufr-exercises/ex_4` et inspectez le fichier de message SYNOP message.txt :

```bash
cd /root/synop2bufr-exercises/ex_4
more message_incorrect.txt
```

!!! question

    Qu'est-ce qui est incorrect dans ce fichier SYNOP ?

??? success "Cliquez pour révéler la réponse"

    Le rapport SYNOP pour 15015 manque le délimiteur (`=`) qui permet à `synop2bufr` de distinguer ce rapport du suivant.

Essayez de convertir `message_incorrect.txt` en utilisant `station_list.csv`

!!! question

    Quel(s) problème(s) avez-vous rencontré avec cette conversion ?

??? success "Cliquez pour révéler la réponse"

    Pour convertir le message SYNOP en format BUFR, utilisez la commande suivante :

    ```bash
    synop2bufr data transform --metadata station_list.csv --output-dir ./ --year 2024 --month 09 message_incorrect.txt
    ```

    Tenter de convertir devrait soulever les erreurs suivantes :
    
    - `[ERROR] Impossible de décoder le message SYNOP`
    - `[ERROR] Erreur lors de l'analyse du rapport SYNOP : AAXX 21121 15015 02999 02501 10103 21090 39765 42952 57020 60001 15020 02997 23104 10130 21075 30177 40377 58020 60001 81041. 10130 n'est pas un groupe valide !`

### Exercice 5
Naviguez jusqu'au répertoire `exercise-materials/synop2bufr-exercises/ex_5` et inspectez le fichier de message SYNOP message.txt :

```bash
cd /root/synop2bufr-exercises/ex_5
more message.txt
```

Essayez de convertir `message.txt` en format BUFR en utilisant `station_list_incorrect.csv` 

!!! question

    Quel(s) problème(s) avez-vous rencontré avec cette conversion ?  
    Considérant l'erreur présentée, justifiez le nombre de fichiers BUFR produits.

??? success "Cliquez pour révéler la réponse"

    Pour convertir le message SYNOP en format BUFR, utilisez la commande suivante :

    ```bash
    synop2bufr data transform --metadata station_list_incorrect.csv --output-dir ./ --year 2024 --month 09 message.txt
    ```

    L'un des TSIs de station (`15015`) n'a pas de métadonnées correspondantes dans la liste des stations, ce qui empêchera synop2bufr d'accéder aux métadonnées supplémentaires nécessaires pour convertir le premier rapport SYNOP en BUFR.

    Vous verrez l'avertissement suivant :

    - `[WARNING] Station 15015 non trouvée dans le fichier de station`

    Vous pouvez voir le nombre de fichiers BUFR produits en exécutant la commande suivante :

    ```bash
    ls -l *.bufr4
    ```

    Il y a 3 rapports SYNOP dans message.txt mais seulement 2 fichiers BUFR ont été produits. Cela est dû au fait qu'un des rapports SYNOP manquait des métadonnées nécessaires comme mentionné ci-dessus.

## Conclusion

!!! success "Félicitations !"

    Dans cette session pratique, vous avez appris :

    - comment l'outil synop2bufr peut être utilisé pour convertir les rapports SYNOP FM-12 en BUFR ;
    - comment diagnostiquer et corriger les erreurs de codage simples dans les rapports SYNOP FM-12 avant la conversion de format ;
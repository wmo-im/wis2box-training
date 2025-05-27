---
title: Travailler avec des données BUFR
---

# Travailler avec des données BUFR

!!! abstract "Résultats d'apprentissage"
    Dans cette session pratique, vous serez initié à certains outils BUFR inclus dans le conteneur **wis2box-api** qui sont utilisés pour transformer des données au format BUFR et pour lire le contenu encodé en BUFR.
    
    Vous apprendrez :

    - comment inspecter les en-têtes dans le fichier BUFR en utilisant la commande `bufr_ls`
    - comment extraire et inspecter les données dans un fichier bufr en utilisant `bufr_dump`
    - la structure de base des modèles bufr utilisés dans csv2bufr et comment utiliser l'outil en ligne de commande
    - et comment apporter des modifications de base aux modèles bufr et comment mettre à jour le wis2box pour utiliser la version révisée

## Introduction

Les plugins qui produisent des notifications avec des données BUFR utilisent des processus dans le wis2box-api pour travailler avec des données BUFR, par exemple pour transformer les données de CSV en BUFR ou de BUFR en geojson.

Le conteneur wis2box-api comprend un certain nombre d'outils pour travailler avec des données BUFR.

Ces outils incluent ceux développés par l'ECMWF et inclus dans le logiciel ecCodes, plus d'informations à ce sujet peuvent être trouvées sur le [site web ecCodes](https://confluence.ecmwf.int/display/ECC/BUFR+tools).

Dans cette session, vous serez initié aux commandes `bufr_ls` et `bufr_dump` du paquet logiciel ecCodes et à la configuration avancée de l'outil csv2bufr.

## Préparation

Pour utiliser les outils en ligne de commande BUFR, vous devrez être connecté au conteneur wis2box-api et à moins d'indication contraire, toutes les commandes doivent être exécutées sur ce conteneur. Vous devrez également avoir MQTT Explorer ouvert et connecté à votre courtier.

Connectez-vous d'abord à votre VM étudiant via votre client ssh, puis connectez-vous au conteneur wis2box-api :

```{.copy}
cd ~/wis2box-1.0.0rc1
python3 wis2box-ctl.py login wis2box-api
```

Confirmez que les outils sont disponibles, en commençant par ecCodes :

``` {.copy}
bufr_dump -V
```
Vous devriez obtenir la réponse suivante :

```
ecCodes Version 2.28.0
```

Ensuite, vérifiez csv2bufr :

```{.copy}
csv2bufr --version
```

Vous devriez obtenir la réponse suivante :

```
csv2bufr, version 0.7.4
```

Enfin, créez un répertoire de travail pour travailler :

```{.copy}
cd /data/wis2box
mkdir -p working/bufr-cli
cd working/bufr-cli
```

Vous êtes maintenant prêt à commencer à utiliser les outils BUFR.

## Utilisation des outils en ligne de commande BUFR

### Exercice 1 - bufr_ls
Dans ce premier exercice, vous utiliserez la commande `bufr_ls` pour inspecter les en-têtes d'un fichier BUFR et pour déterminer le contenu du fichier. Les en-têtes suivants sont inclus dans un fichier BUFR :

| en-tête                            | clé ecCodes                  | description                                                                                                                                           |
|-----------------------------------|------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------|
| centre d'origine/génération       | centre                       | Le centre d'origine / de génération des données                                                                                                       |
| sous-centre d'origine/génération  | bufrHeaderSubCentre          | Le sous-centre d'origine / de génération des données                                                                                                  |
| Numéro de séquence de mise à jour | updateSequenceNumber         | S'il s'agit de la première version des données (0) ou d'une mise à jour (>0)                                                                          |
| Catégorie de données              | dataCategory                 | Le type de données contenu dans le message BUFR, par ex. données de surface. Voir [Table A BUFR](https://github.com/wmo-im/BUFR4/blob/master/BUFR_TableA_en.csv)  |
| Sous-catégorie de données internationales | internationalDataSubCategory | Le sous-type de données contenu dans le message BUFR, par ex. données de surface. Voir [Tableau des codes communs C-13](https://github.com/wmo-im/CCT/blob/master/C13.csv) |
| Année                             | typicalYear (typicalDate)    | Moment le plus typique pour le contenu du message BUFR                                                                                                |
| Mois                              | typicalMonth (typicalDate)   | Moment le plus typique pour le contenu du message BUFR                                                                                                |
| Jour                              | typicalDay (typicalDate)     | Moment le plus typique pour le contenu du message BUFR                                                                                                |
| Heure                             | typicalHour (typicalTime)    | Moment le plus typique pour le contenu du message BUFR                                                                                                |
| Minute                            | typicalMinute (typicalTime)  | Moment le plus typique pour le contenu du message BUFR                                                                                                |
| Descripteurs BUFR                 | unexpandedDescriptors        | Liste d'un ou plusieurs descripteurs BUFR définissant les données contenues dans le fichier                                                           |

Téléchargez le fichier exemple directement dans le conteneur de gestion wis2box en utilisant la commande suivante :

``` {.copy}
curl https://training.wis2box.wis.wmo.int/sample-data/bufr-cli-ex1.bufr4 --output bufr-cli-ex1.bufr4
```

Utilisez maintenant la commande suivante pour exécuter `bufr_ls` sur ce fichier :

```bash
bufr_ls bufr-cli-ex1.bufr4
```

Vous devriez voir la sortie suivante :

```bash
bufr-cli-ex1.bufr4
centre                     masterTablesVersionNumber  localTablesVersionNumber   typicalDate                typicalTime                numberOfSubsets
cnmc                       29                         0                          20231002                   000000                     1
1 of 1 messages in bufr-cli-ex1.bufr4

1 of 1 total messages in 1 files
```

Par elle-même, cette information n'est pas très informative, avec seulement des informations limitées sur le contenu du fichier fournies.

La sortie par défaut ne fournit pas d'informations sur le type d'observation ou de données et est dans un format qui n'est pas très facile à lire. Cependant, diverses options peuvent être passées à `bufr_ls` pour changer à la fois le format et les champs d'en-tête imprimés.

Utilisez `bufr_ls` sans aucun argument pour voir les options :

```{.copy}
bufr_ls
```

Vous devriez voir la sortie suivante :

```
NAME    bufr_ls

DESCRIPTION
        List content of BUFR files printing values of some header keys.
        Only scalar keys can be printed.
        It does not fail when a key is not found.

USAGE
        bufr_ls [options] bufr_file bufr_file ...

OPTIONS
        -p key[:{s|d|i}],key[:{s|d|i}],...
                Declaration of keys to print.
                For each key a string (key:s), a double (key:d) or an integer (key:i)
                type can be requested. Default type is string.
        -F format
                C style format for floating-point values.
        -P key[:{s|d|i}],key[:{s|d|i}],...
                As -p adding the declared keys to the default list.
        -w key[:{s|d|i}]{=|!=}value,key[:{s|d|i}]{=|!=}value,...
                Where clause.
                Messages are processed only if they match all the key/value constraints.
                A valid constraint is of type key=value or key!=value.
                For each key a string (key:s), a double (key:d) or an integer (key:i)
                type can be specified. Default type is string.
                In the value you can also use the forward-slash character '/' to specify an OR condition (i.e. a logical disjunction)
                Note: only one -w clause is allowed.
        -j      JSON output
        -s key[:{s|d|i}]=value,key[:{s|d|i}]=value,...
                Key/values to set.
                For each key a string (key:s), a double (key:d) or an integer (key:i)
                type can be defined. By default the native type is set.
        -n namespace
                All the keys belonging to the given namespace are printed.
        -m      Mars keys are printed.
        -V      Version.
        -W width
                Minimum width of each column in output. Default is 10.
        -g      Copy GTS header.
        -7      Does not fail when the message has wrong length

SEE ALSO
        Full documentation and examples at:
        <https://confluence.ecmwf.int/display/ECC/bufr_ls>
```

Exécutez maintenant la même commande sur le fichier exemple mais affichez les informations au format JSON.

!!! question
    Quel indicateur passez-vous à la commande `bufr_ls` pour voir la sortie au format JSON ?

??? success "Cliquez pour révéler la réponse"
    Vous pouvez changer le format de sortie en json en utilisant l'indicateur `-j`, c'est-à-dire
    `bufr_ls -j <fichier-entrée>`. Cela peut être plus lisible que le format de sortie par défaut. Voir la sortie d'exemple ci-dessous :

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

Lors de l'examen d'un fichier BUFR, nous voulons souvent déterminer le type de données contenu dans le fichier et la date / heure typiques des données dans le fichier. Ces informations peuvent être listées en utilisant l'indicateur `-p` pour sélectionner les en-têtes à afficher. Plusieurs en-têtes peuvent être inclus en utilisant une liste séparée par des virgules.

En utilisant la commande `bufr_ls`, inspectez le fichier de test et identifiez le type de données contenu dans le fichier et la date et l'heure typiques pour ces données.

??? hint
    Les clés ecCodes sont données dans le tableau ci-dessus. Nous pouvons utiliser ce qui suit pour lister la dataCategory et
    internationalDataSubCategory des données BUFR :

    ```
    bufr_ls -p dataCategory,internationalDataSubCategory bufr-cli-ex1.bufr4
    ```

    Des clés supplémentaires peuvent être ajoutées si nécessaire.

!!! question
    Quel type de données (catégorie de données et sous-catégorie) sont contenues dans le fichier ? Quelle est la date et l'heure typiques pour les données ?

??? success "Cliquez pour révéler la réponse"
    La commande que vous devez exécuter aurait dû être similaire à :
    
    ```
    bufr_ls -p dataCategory,internationalDataSubCategory,typicalDate,typicalTime -j bufr-cli-ex1.bufr4
    ```

    Vous avez peut-être ajouté des clés supplémentaires, ou listé l'année, le mois, le jour, etc. individuellement. La sortie devrait
    être similaire à ci-dessous, selon que vous avez sélectionné le format JSON ou la sortie par défaut.

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

    - La catégorie de données est 2, à partir de [Table A BUFR](https://github.com/wmo-im/BUFR4/blob/master/BUFR_TableA_en.csv)
      nous pouvons voir que ce fichier contient des données "Sondages verticaux (autres que par satellite)".
    - La sous-catégorie internationale est 4, indiquant
      "Rapports de température/humidité/vent de niveau supérieur provenant de stations terrestres fixes (TEMP)" données. Cette information peut être consultée
      dans [Tableau des codes communs C-13](https://github.com/wmo-im/CCT/blob/master/C13.csv) (ligne 33). Notez la combinaison
      de catégorie et de sous-catégorie.
    - La date et l'heure typiques sont 2023/10/02 et 00:00:00z respectivement.

    

### Exercice 2 - bufr_dump

La commande `bufr_dump` peut être utilisée pour lister et examiner le contenu d'un fichier BUFR, y compris les données elles-mêmes.

Dans cet exercice, nous utiliserons un fichier BUFR qui est le même que celui que vous avez créé lors de la session pratique initiale csv2bufr en utilisant le wis2box-webapp.

Téléchargez le fichier exemple directement dans le conteneur de gestion wis2box avec la commande suivante :

``` {.copy}
curl https://training.wis2box.wis.wmo.int/sample-data/bufr-cli-ex2.bufr4 --output bufr-cli-ex2.bufr4
```

Exécutez maintenant la commande `bufr_dump` sur le fichier, en utilisant l'indicateur `-p` pour afficher les données au format texte brut (format clé=valeur) :

```{.copy}
bufr_dump -p bufr-cli-ex2.bufr4
```

Vous devriez voir environ 240 clés affichées, dont beaucoup sont manquantes. Cela est typique avec les données du monde réel car toutes les clés eccodes ne sont pas peuplées avec des données signalées.

!!! hint
    Les valeurs manquantes peuvent être filtrées à l'aide d'outils tels que `grep` :
    ```{.copy}
    bufr_dump -p bufr-cli-ex2.bufr4 | grep -v MISSING
    ```

Le fichier BUFR exemple pour cet exercice provient de la session pratique csv2bufr. Veuillez télécharger le fichier CSV original dans votre emplacement actuel comme suit :

```{.copy}
curl https://training.wis2box.wis.wmo.int/sample-data/csv2bufr-ex1.csv --output csv2bufr-ex1.csv
```

Et affichez le contenu du fichier avec :

```{.copy}
more csv2bufr-ex1.csv
```

!!! question
    Utilisez la commande suivante pour afficher la colonne 18 dans le fichier CSV et vous trouverez la pression moyenne au niveau de la mer signalée (msl_pressure) :

    ```{.copy}
    more csv2bufr-ex1.csv | cut -d ',' -f 18
    ```
    
    Quelle clé dans la sortie BUFR correspond à la pression moyenne au niveau de la mer ?

??? hint
    Des outils tels que `grep` peuvent être utilisés en combinaison avec `bufr_dump`. Par exemple :
    
    ```{.copy}
    bufr_dump -p bufr-cli-ex2.bufr4 | grep -i "pressure"
    ```
    
    filtrerait le contenu de `bufr_dump` pour ne montrer que les lignes contenant le mot pression. Alternativement,
    la sortie pourrait être filtrée sur une valeur.

??? success "Cliquez pour révéler la réponse"
    La clé "pressureReducedToMeanSeaLevel" correspond à la colonne msl_pressure dans le fichier CSV d'entrée.

Passez quelques minutes à examiner le reste de la sortie, en la comparant au fichier CSV d'entrée avant de passer à l'exercice suivant. Par exemple, vous pouvez essayer de trouver les clés dans la sortie BUFR qui correspondent à l'humidité relative (colonne 23 dans le fichier CSV) et à la température de l'air (colonne 21 dans le fichier CSV).

### Exercice 3 - fichiers de mappage csv2bufr

L'outil csv2bufr peut être configuré pour traiter des données tabulaires avec différentes colonnes et séquences BUFR.

Cela se fait par le biais d'un fichier de configuration écrit au format JSON.

Comme les données BUFR elles-mêmes, le fichier JSON contient une section d'en-tête et une section de données, qui correspondent largement aux mêmes sections dans BUFR.

De plus, certaines options de formatage sont spécifiées dans le fichier JSON.

Le fichier JSON pour le mappage par défaut peut être consulté via le lien ci-dessous (clic droit et ouvrir dans un nouvel onglet) :

[aws-template.json](https://raw.githubusercontent.com/wmo-im/csv2bufr/main/csv2bufr/templates/resources/aws-template.json)

Examinez la section `header` du fichier de mappage (montrée ci-dessous) et comparez-la au tableau de l'exercice 1 (colonne clé ecCodes) :

```
"header":[
    {"eccodes_key": "edition", "value": "const:4"},
    {"eccodes_key": "masterTableNumber", "value": "const:0"},
    {"eccodes_key": "bufrHeaderCentre", "value": "const:0"},
    {"eccodes_key": "bufrHeaderSubCentre", "value": "const:0"},
    {"eccodes_key": "updateSequenceNumber", "value": "const:0"},
    {"eccodes_key": "dataCategory", "value": "const:0"},
    {"eccodes_key": "internationalDataSubCategory", "value": "const:2"},
    {"eccodes_key": "masterTablesVersionNumber", "value": "const:30"},
    {"eccodes_key": "numberOfSubsets", "value": "const:1"},
    {"eccodes_key": "obs
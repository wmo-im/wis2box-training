---
title: Découverte des ensembles de données du Global Discovery Catalogue de WIS2
---

# Découverte des ensembles de données du Global Discovery Catalogue de WIS2

!!! abstract "Objectifs d'apprentissage !"

    À la fin de cette session pratique, vous serez capable de :

    - utiliser pywmocat pour découvrir des ensembles de données dans le Global Discovery Catalogue (GDC)

## Introduction

Dans cette session, vous apprendrez à découvrir des données dans le Global Discovery Catalogue (GDC) de WIS2 en utilisant [pywmocat](https://github.com/wmo-im/pywmocat), un outil en ligne de commande permettant de rechercher et de récupérer des métadonnées depuis un GDC de WIS2.

Actuellement, les GDC suivants sont disponibles :

- Environnement et Changement Climatique Canada, Service météorologique du Canada : <https://wis2-gdc.weather.gc.ca/collections/wis2-discovery-metadata>
- Administration météorologique de Chine : <https://gdc.wis.cma.cn/collections/wis2-discovery-metadata>
- Deutscher Wetterdienst : <https://wis2.dwd.de/gdc/collections/wis2-discovery-metadata>

Lors des sessions de formation locales, un GDC local est configuré pour permettre aux participants de consulter le GDC pour les métadonnées qu'ils ont publiées depuis leurs instances de wis2box. Dans ce cas, les formateurs fourniront l'URL du GDC local.

## Préparation

!!! note
    Avant de commencer, veuillez vous connecter à votre VM étudiant.

## Installation de pywmocat

Utilisez l'installateur de paquets Python `pip3` pour installer pywmocat sur votre VM :
```bash
pip3 install pywmocat
```

!!! note

    Si vous rencontrez l'erreur suivante :

    ```
    WARNING: The script pywmocat is installed in '/home/username/.local/bin' which is not on PATH.
    Consider adding this directory to PATH or, if you prefer to suppress this warning, use --no-warn-script-location.
    ```

    Exécutez alors la commande suivante :

    ```bash
    export PATH=$PATH:/home/$USER/.local/bin
    ```

    ...où `$USER` est votre nom d'utilisateur sur votre VM.

Vérifiez que l'installation a réussi :

```bash
pywmocat --version
```

## Recherche de données avec pywmocat

Par défaut, pywmocat se connecte au Global Discovery Catalogue (GDC) hébergé par Environnement et Changement Climatique Canada (ECCC).

!!! note "Changer l'URL du GDC"
    Si vous effectuez cet exercice lors d'une session de formation locale, vous pouvez configurer pywmocat pour interroger le GDC local en définissant la variable d'environnement `PYWISCAT_GDC_URL` :

    ```bash
    export PYWMOCAT_WIS2_GDC_URL=http://gdc.training.wis2dev.io/collections/wis2-discovery-metadata
    ```

Pour voir les options disponibles, exécutez :

```bash
pywmocat wis2-gdc search --help
```

Vous pouvez rechercher tous les enregistrements dans le GDC :

```bash
pywmocat wis2-gdc search
```

!!! question

    Combien d'enregistrements sont retournés par la recherche ?

??? success "Cliquez pour révéler la réponse"
    Le nombre d'enregistrements dépend du GDC que vous interrogez. Lors de l'utilisation du GDC de formation locale, vous devriez constater que le nombre d'enregistrements est égal au nombre d'ensembles de données qui ont été intégrés dans le GDC au cours des autres sessions pratiques.

Essayons de rechercher dans le GDC avec un mot-clé :

```bash
pywmocat wis2-gdc search -q observations
```

!!! question

    Quelle est la politique de données des résultats ?

??? success "Cliquez pour révéler la réponse"
    Toutes les données retournées devraient spécifier des données "core".

Essayez des recherches supplémentaires avec `-q`.

!!! tip

    Le drapeau `-q` permet la syntaxe suivante :

    - `-q synop` : trouver tous les enregistrements contenant le mot "synop"
    - `-q temp` : trouver tous les enregistrements contenant le mot "temp"
    - `-q "observations AND oman"` : trouver tous les enregistrements contenant les mots "observations" et "oman"
    - `-q "observations NOT oman"` : trouver tous les enregistrements contenant le mot "observations" mais pas le mot "oman"
    - `-q "synop OR temp"` : trouver tous les enregistrements contenant "synop" ou "temp"
    - `-q "obs*"` : recherche approximative

    Lors de la recherche de termes contenant des espaces, utilisez des guillemets doubles.

Obtenons plus de détails sur un résultat de recherche spécifique qui nous intéresse :

```bash
pywmocat wis2-gdc get <id>
```

!!! tip

    Utilisez la valeur `id` obtenue lors de la recherche précédente.

## Conclusion

!!! success "Félicitations !"

    Lors de cette session pratique, vous avez appris à :

    - utiliser pywmocat pour découvrir des ensembles de données dans le Global Discovery Catalogue de WIS2
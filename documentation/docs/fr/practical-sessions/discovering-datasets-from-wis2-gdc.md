---
title: Découverte des jeux de données depuis le WIS2 Global Discovery Catalogue
---

# Découverte des jeux de données depuis le WIS2 Global Discovery Catalogue

!!! abstract "Objectifs d'apprentissage!"

    À la fin de cette session pratique, vous serez capable de :

    - utiliser pywiscat pour découvrir des jeux de données depuis le Global Discovery Catalogue (GDC)

## Introduction

Dans cette session, vous apprendrez à découvrir des données depuis le WIS2 Global Discovery Catalogue (GDC).

Actuellement, les GDC suivants sont disponibles :

- Environment and Climate Change Canada, Meteorological Service of Canada : <https://wis2-gdc.weather.gc.ca>
- China Meteorological Administration : <https://gdc.wis.cma.cn>
- Deutscher Wetterdienst : <https://wis2.dwd.de/gdc>

Pendant les sessions de formation locales, un GDC local est configuré pour permettre aux participants d'interroger le GDC pour les métadonnées qu'ils ont publiées depuis leurs instances wis2box. Dans ce cas, les formateurs fourniront l'URL du GDC local.

## Préparation

!!! note
    Avant de commencer, veuillez vous connecter à votre machine virtuelle étudiante.

## Installation de pywiscat

Utilisez l'installateur de paquets Python `pip3` pour installer pywiscat sur votre machine virtuelle :
```bash
pip3 install pywiscat
```

!!! note

    Si vous rencontrez l'erreur suivante :

    ```
    WARNING: The script pywiscat is installed in '/home/username/.local/bin' which is not on PATH.
    Consider adding this directory to PATH or, if you prefer to suppress this warning, use --no-warn-script-location.
    ```

    Exécutez alors la commande suivante :

    ```bash
    export PATH=$PATH:/home/$USER/.local/bin
    ```

    ...où `$USER` est votre nom d'utilisateur sur votre machine virtuelle.

Vérifiez que l'installation a réussi :

```bash
pywiscat --version
```

## Recherche de données avec pywiscat

Par défaut, pywiscat se connecte au Global Discovery Catalogue du Canada. Configurons pywiscat pour interroger le GDC de formation en définissant la variable d'environnement `PYWISCAT_GDC_URL` :

```bash
export PYWISCAT_GDC_URL=http://gdc.wis2.training:5002
```

Utilisons [pywiscat](https://github.com/wmo-im/pywiscat) pour interroger le GDC configuré dans le cadre de la formation.

```bash
pywiscat search --help
```

Maintenant, recherchez tous les enregistrements dans le GDC :

```bash
pywiscat search
```

!!! question

    Combien d'enregistrements sont retournés par la recherche ?

??? success "Cliquez pour révéler la réponse"
    Le nombre d'enregistrements dépend du GDC que vous interrogez. En utilisant le GDC local de formation, vous devriez voir que le nombre d'enregistrements est égal au nombre de jeux de données qui ont été ingérés dans le GDC pendant les autres sessions pratiques.

Essayons d'interroger le GDC avec un mot-clé :

```bash
pywiscat search -q observations
```

!!! question

    Quelle est la politique de données des résultats ?

??? success "Cliquez pour révéler la réponse"
    Toutes les données retournées devraient spécifier des données "core"

Essayez d'autres requêtes avec `-q`

!!! tip

    Le drapeau `-q` permet la syntaxe suivante :

    - `-q synop` : trouve tous les enregistrements contenant le mot "synop"
    - `-q temp` : trouve tous les enregistrements contenant le mot "temp"
    - `-q "observations AND oman"` : trouve tous les enregistrements contenant les mots "observations" et "oman"
    - `-q "observations NOT oman"` : trouve tous les enregistrements contenant le mot "observations" mais pas le mot "oman"
    - `-q "synop OR temp"` : trouve tous les enregistrements contenant "synop" ou "temp"
    - `-q "obs*"` : recherche approximative

    Pour rechercher des termes contenant des espaces, entourez-les de guillemets doubles.

Obtenons plus de détails sur un résultat de recherche spécifique qui nous intéresse :

```bash
pywiscat get <id>
```

!!! tip

    Utilisez la valeur `id` de la recherche précédente.

## Conclusion

!!! success "Félicitations!"

    Dans cette session pratique, vous avez appris à :

    - utiliser pywiscat pour découvrir des jeux de données depuis le WIS2 Global Discovery Catalogue
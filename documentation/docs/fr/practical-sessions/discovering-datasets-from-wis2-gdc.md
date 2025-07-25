---
title: Découverte de jeux de données depuis le Catalogue de Découverte Global WIS2
---

# Découverte de jeux de données depuis le Catalogue de Découverte Global WIS2

!!! abstract "Résultats d'apprentissage !"

    À la fin de cette session pratique, vous serez capable de :

    - utiliser pywiscat pour découvrir des jeux de données depuis le Catalogue de Découverte Global (GDC)

## Introduction

Dans cette session, vous apprendrez à découvrir des données depuis le Catalogue de Découverte Global WIS2 (GDC).

Actuellement, les GDC suivants sont disponibles :

- Environnement et Changement Climatique Canada, Service Météorologique du Canada : <https://wis2-gdc.weather.gc.ca>
- Administration Météorologique de Chine : <https://gdc.wis.cma.cn>
- Service Météorologique Allemand : <https://wis2.dwd.de/gdc>


Lors des sessions de formation locales, un GDC local est mis en place pour permettre aux participants de consulter le GDC pour les métadonnées qu'ils ont publiées depuis leurs instances wis2box. Dans ce cas, les formateurs fourniront l'URL du GDC local.

## Préparation

!!! note
    Avant de commencer, veuillez vous connecter à votre VM étudiant.

## Installation de pywiscat

Utilisez l'installateur de paquets Python `pip3` pour installer pywiscat sur votre VM :
```bash
pip3 install pywiscat
```

!!! note

    Si vous rencontrez l'erreur suivante :

    ```
    WARNING: The script pywiscat is installed in '/home/username/.local/bin' which is not on PATH.
    Consider adding this directory to PATH or, if you prefer to suppress this warning, use --no-warn-script-location.
    ```

    Alors exécutez la commande suivante :

    ```bash
    export PATH=$PATH:/home/$USER/.local/bin
    ```

    ...où `$USER` est votre nom d'utilisateur sur votre VM.

Vérifiez que l'installation a été réussie :

```bash
pywiscat --version
```

## Trouver des données avec pywiscat

Par défaut, pywiscat se connecte au Catalogue de Découverte Global du Canada. Configurons pywiscat pour interroger le GDC de formation en définissant la variable d'environnement `PYWISCAT_GDC_URL` :

```bash
export PYWISCAT_GDC_URL=http://gdc.wis2.training:5002
```

Utilisons [pywiscat](https://github.com/wmo-im/pywiscat) pour interroger le GDC configuré dans le cadre de la formation.

```bash
pywiscat search --help
```

Recherchez maintenant dans le GDC tous les enregistrements :

```bash
pywiscat search
```

!!! question

    Combien d'enregistrements sont retournés de la recherche ?

??? success "Cliquez pour révéler la réponse"
    Le nombre d'enregistrements dépend du GDC que vous interrogez. Lors de l'utilisation du GDC de formation local, vous devriez voir que le nombre d'enregistrements est égal au nombre de jeux de données qui ont été ingérés dans le GDC lors des autres sessions pratiques.

Essayons d'interroger le GDC avec un mot-clé :

```bash
pywiscat search -q observations
```

!!! question

    Quelle est la politique de données des résultats ?

??? success "Cliquez pour révéler la réponse"
    Toutes les données retournées doivent spécifier des données "core"

Essayez des requêtes supplémentaires avec `-q`

!!! tip

    Le drapeau `-q` permet la syntaxe suivante :

    - `-q synop` : trouve tous les enregistrements avec le mot "synop"
    - `-q temp` : trouve tous les enregistrements avec le mot "temp"
    - `-q "observations AND oman"` : trouve tous les enregistrements avec les mots "observations" et "oman"
    - `-q "observations NOT oman"` : trouve tous les enregistrements contenant le mot "observations" mais pas le mot "oman"
    - `-q "synop OR temp"` : trouve tous les enregistrements avec "synop" ou "temp"
    - `-q "obs*"` : recherche floue

    Lors de la recherche de termes avec des espaces, les encadrer de guillemets doubles.

Obtenons plus de détails sur un résultat de recherche spécifique qui nous intéresse :

```bash
pywiscat get <id>
```

!!! tip

    Utilisez la valeur `id` de la recherche précédente.


## Conclusion

!!! success "Félicitations !"

    Dans cette session pratique, vous avez appris à :

    - utiliser pywiscat pour découvrir des jeux de données depuis le Catalogue de Découverte Global WIS2
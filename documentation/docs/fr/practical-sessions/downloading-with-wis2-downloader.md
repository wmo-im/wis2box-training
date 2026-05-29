---
title: Téléchargement avec WIS2 Downloader
---

# Téléchargement avec WIS2 Downloader

!!! abstract "Objectifs d'apprentissage !"

    À la fin de cette session pratique, vous serez capable de :

    - explorer et trouver des ensembles de données dans WIS2 Downloader
    - utiliser des filtres pour contrôler les fichiers téléchargés
    - utiliser l'authentification pour télécharger des ensembles de données à accès contrôlé
    - modifier la configuration par défaut de WIS2 Downloader pour des cas d'utilisation avancés

## Introduction

Dans WIS2, tous les ensembles de données possèdent un fichier de métadonnées qui peut être trouvé dans les **Global Discovery Catalogues**. Ainsi, il est prévu que les utilisateurs consultent toujours ces services pour trouver les données partagées sur WIS2.

WIS2 Downloader utilise ce principe en trouvant tous les enregistrements disponibles dans ces GDCs et en les combinant en interne pour permettre à l'utilisateur de naviguer parmi les données disponibles sur WIS2. Étant donné le grand nombre d'enregistrements à afficher, il est essentiel de fournir un moyen à l'utilisateur de les filtrer et de trouver le bon enregistrement. Même après avoir trouvé et souscrit au bon enregistrement, il peut y avoir des ensembles de données où le nombre de fichiers dépasse les besoins actuels de l'utilisateur. Pour cette raison, un deuxième niveau de filtrage est nécessaire — celui qui opère au moment de décider si un fichier doit être téléchargé.

## Explorer et trouver dans la vue Catalogue

La **vue Catalogue** est l'une des deux façons de trouver et de souscrire à des ensembles de données dans WIS2 Downloader. Elle regroupe les enregistrements des Global Discovery Catalogues et les présente dans une interface consultable et filtrable — similaire à la navigation directe sur un portail GDC.

Accédez à la **vue Catalogue** dans la barre latérale gauche.

![WIS2 Downloader Catalogue View](../assets/img/wis2-downloader-catalogue-view.png)

En haut de la page, vous trouverez une barre de recherche et un ensemble de filtres. Vous pouvez les utiliser pour réduire la liste des enregistrements disponibles par mot-clé, Centre ID ou politique de données (core vs. recommended).

Vous pouvez également filtrer spatialement en définissant une **boîte englobante** à l'aide de quatre entrées de coordonnées — **Nord**, **Ouest**, **Sud** et **Est** — exprimées en valeurs décimales de latitude et de longitude. Lorsqu'une boîte englobante est définie, vous pouvez choisir entre deux modes de correspondance :

- **Intersects** — retourne les enregistrements dont l'étendue spatiale chevauche la boîte englobante de quelque manière que ce soit.
- **Within** — retourne uniquement les enregistrements dont l'étendue spatiale se trouve entièrement à l'intérieur de la boîte englobante.

!!! note "Recharger le catalogue"

    Le catalogue est chargé à partir des GDCs lorsque WIS2 Downloader démarre. Si vous pensez que la liste n'est pas à jour, vous pouvez forcer un rechargement depuis la section **Settings** dans la barre latérale gauche.

### Exercice : trouver et souscrire à un ensemble de données

!!! question "Trouver un ensemble de données d'observations de surface"

    Utilisez les filtres dans la vue Catalogue pour trouver un ensemble de données **core** d'observations de surface lié à la température et aux précipitations.

    1. Tapez `surface` dans la barre de recherche et observez comment la liste des enregistrements est filtrée.
    2. Réglez le filtre de politique de données sur **core**.
    3. Configurez les mots-clés pour inclure `temperature, precipitation` et observez comment les résultats changent.
    4. Sélectionnez un enregistrement parmi les résultats pour développer ses détails.
    5. Examinez les métadonnées affichées — notez le sujet, le centre d'origine et la politique de données.
    6. Définissez le dossier de destination sur `surface-obs`.
    7. Cliquez sur **Subscribe** pour créer l'abonnement.

    Après avoir souscrit, accédez à **Manage Subscriptions** pour confirmer que le nouvel abonnement apparaît dans la liste.

??? success "Cliquez pour révéler la réponse"

    Tout enregistrement dont le sujet contient `surface-based-observations` et dont la politique de données est `core` est un choix valide. L'application du filtre de mots-clés pour `temperature, precipitation` réduira davantage les résultats aux ensembles de données pertinents pour ces variables.

    Une fois souscrit, la vue **Manage Subscriptions** affichera l'abonnement actif avec son sujet et son dossier cible. Les fichiers commenceront à se télécharger au fur et à mesure que de nouvelles notifications arriveront sur le broker.

!!! note "Supprimer les fichiers téléchargés"

    Il est recommandé de nettoyer le dossier de téléchargements après avoir terminé un exercice pour libérer de l'espace sur la VM étudiante :

    ```bash
    rm -fr wis2downloader/downloads/surface-obs
    ```

## Explorer et trouver dans la vue Arborescence

La **vue Arborescence** présente la hiérarchie des sujets WIS2 sous forme d'arbre extensible, permettant de parcourir les sujets disponibles niveau par niveau — similaire à la navigation des sujets dans MQTT Explorer. Elle est conçue pour une exploration de haut niveau, descendante, des données disponibles sur WIS2, en commençant par la racine de la hiérarchie et en approfondissant. Cela contraste avec la vue Catalogue, qui vous emmène directement aux enregistrements individuels des ensembles de données et est mieux adaptée lorsque vous savez déjà ce que vous recherchez.

Accédez à la **vue Arborescence** dans la barre latérale gauche.

![WIS2 Downloader Tree View](../assets/img/wis2-downloader-tree-view.png)

L'arbre est organisé selon la hiérarchie des sujets WIS2. Développez chaque niveau en cliquant sur un nœud pour révéler ses enfants. À n'importe quel niveau, vous pouvez souscrire en sélectionnant un nœud et en cliquant sur **Subscribe** — en utilisant un joker (`#`) pour capturer tous les sujets sous ce nœud.

!!! note "Souscrire à différents niveaux"

    Souscrire plus haut dans l'arbre (par exemple au niveau du Centre ID) capturera tous les ensembles de données publiés par ce centre. Souscrire plus bas offre un contrôle plus granulaire. Utilisez le suffixe joker `#` automatiquement ajouté par WIS2 Downloader lors de la souscription depuis la vue Arborescence.

### Exercice : trouver et souscrire via la vue Arborescence

!!! question "Souscrire à un ensemble de données via la vue Arborescence"

    Utilisez la vue Arborescence pour trouver et souscrire à des données d'observations de surface provenant d'un centre spécifique.

    1. Développez l'arbre en commençant par le nœud `cache`, puis naviguez à travers `a` → `wis2`.
    2. Sélectionnez un Centre ID de votre choix et continuez à développer jusqu'à atteindre un sujet lié à `surface-based-observations`.
    3. Examinez le chemin complet du sujet affiché — confirmez qu'il correspond à l'ensemble de données souhaité.
    4. Définissez le dossier de destination sur `surface-obs-tree`.
    5. Cliquez sur **Subscribe** pour créer l'abonnement.

    Accédez à **Manage Subscriptions** pour confirmer que l'abonnement est actif.

??? success "Cliquez pour révéler la réponse"

    Tout chemin de sujet suivant le modèle `cache/a/wis2/<centre-id>/data/core/weather/surface-based-observations/#` est un choix valide. Le segment Centre ID variera en fonction du centre que vous avez sélectionné dans l'arborescence.

    La vue **Manage Subscriptions** affichera le nouvel abonnement aux côtés de ceux créés précédemment.

!!! note "Supprimer les fichiers téléchargés"

    Nettoyez le dossier de téléchargements après avoir terminé l'exercice :

    ```bash
    rm -fr wis2downloader/downloads/surface-obs-tree
    ```
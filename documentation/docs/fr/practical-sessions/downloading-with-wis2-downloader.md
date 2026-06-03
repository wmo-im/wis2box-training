---
title: Téléchargement avec WIS2 Downloader
---

# Téléchargement avec WIS2 Downloader

!!! abstract "Objectifs d'apprentissage !"

    À la fin de cette session pratique, vous serez capable de :

    - explorer et trouver des ensembles de données dans WIS2 Downloader
    - utiliser des filtres pour contrôler les fichiers téléchargés
    - utiliser l'authentification pour télécharger des ensembles de données protégés
    - modifier la configuration par défaut de WIS2 Downloader pour des cas d'utilisation avancés

## Introduction

Dans WIS2, tous les ensembles de données possèdent un fichier de métadonnées qui peut être trouvé dans les **Global Discovery Catalogues**. Ainsi, il est prévu que les utilisateurs consultent toujours ces services pour trouver les données partagées sur WIS2.

WIS2 Downloader utilise ce principe en recherchant tous les enregistrements disponibles dans ces GDCs et en les combinant en interne pour permettre à l'utilisateur de naviguer parmi les données disponibles sur WIS2. Étant donné le grand nombre d'enregistrements à afficher, il est essentiel de fournir un moyen à l'utilisateur de les filtrer pour trouver l'enregistrement correct. Même après avoir trouvé et souscrit à l'enregistrement correct, certains ensembles de données peuvent contenir un nombre de fichiers supérieur aux besoins actuels de l'utilisateur. Pour cette raison, un deuxième niveau de filtrage est nécessaire — celui qui opère au moment de décider si un fichier doit être téléchargé.

## Utilisation dans la vue Catalogue

La **vue Catalogue** est l'une des deux façons de trouver et de souscrire à des ensembles de données dans WIS2 Downloader. Elle regroupe les enregistrements des Global Discovery Catalogues et les présente dans une interface consultable et filtrable — similaire à la navigation directe sur un portail GDC.

Accédez à la **vue Catalogue** dans la barre latérale gauche.

![WIS2 Downloader Catalogue View](../assets/img/wis2-downloader-catalogue-view.png)

En haut de la page, vous trouverez une barre de recherche et un ensemble de filtres. Vous pouvez les utiliser pour réduire la liste des enregistrements disponibles par mot-clé, Centre ID ou politique de données (core vs. recommended).

Vous pouvez également filtrer spatialement en définissant une **boîte englobante** à l'aide de quatre champs de coordonnées — **Nord**, **Ouest**, **Sud** et **Est** — exprimés en valeurs décimales de latitude et longitude. Lorsqu'une boîte englobante est définie, vous pouvez choisir entre deux modes de correspondance :

- **Intersects** — retourne les enregistrements dont l'étendue spatiale chevauche la boîte englobante de quelque manière que ce soit.
- **Within** — retourne uniquement les enregistrements dont l'étendue spatiale se trouve entièrement à l'intérieur de la boîte englobante.

!!! note "Recharger le catalogue"

    Le catalogue est chargé à partir des GDCs lorsque WIS2 Downloader démarre. Si vous pensez que la liste est obsolète, vous pouvez forcer un rechargement depuis la section **Settings** dans la barre latérale gauche.

### Exercice : trouver et souscrire à un ensemble de données

!!! question "Trouver un ensemble de données d'observations de surface"

    Utilisez les filtres dans la vue Catalogue pour trouver un ensemble de données d'observations de surface **core** lié à la température et aux précipitations.

    1. Tapez `surface` dans la barre de recherche et observez comment la liste des enregistrements est filtrée.
    2. Définissez le filtre de politique de données sur **core**.
    3. Ajoutez les mots-clés `temperature, precipitation` et observez comment les résultats changent.
    4. Sélectionnez un enregistrement parmi les résultats pour afficher ses détails.
    5. Examinez les métadonnées affichées — notez le sujet, le centre d'origine et la politique de données.
    6. Définissez le dossier de destination sur `surface-obs`.
    7. Cliquez sur **Subscribe** pour créer l'abonnement.

    Après avoir souscrit, accédez à **Manage Subscriptions** pour confirmer que le nouvel abonnement apparaît dans la liste.

??? success "Cliquez pour révéler la réponse"

    Tout enregistrement dont le sujet contient `surface-based-observations` et dont la politique de données est `core` est un choix valide. L'application du filtre de mots-clés `temperature, precipitation` permettra de réduire davantage les résultats aux ensembles de données pertinents pour ces variables.

    Une fois souscrit, la vue **Manage Subscriptions** affichera l'abonnement actif avec son sujet et son dossier cible. Les fichiers commenceront à être téléchargés à mesure que de nouvelles notifications arrivent sur le broker.

!!! note "Se désabonner et supprimer les fichiers téléchargés"
    
    Accédez à la vue **Manage Subscriptions** et `Unsubscribe` du sujet sélectionné dans l'exercice précédent.

    Ensuite, nettoyez le dossier de téléchargements :

    ```bash
    rm -fr /home/{USER}/wis2-downloads/surface-obs
    ```

## Utilisation dans la vue Arborescence

La **vue Arborescence** présente la hiérarchie des sujets WIS2 sous forme d'arborescence repliable, permettant de parcourir les sujets disponibles niveau par niveau — similaire à la navigation des sujets dans MQTT Explorer. Elle est conçue pour une exploration de haut niveau, en partant de la racine de la hiérarchie et en descendant progressivement. Cela contraste avec la vue Catalogue, qui vous mène directement aux enregistrements individuels des ensembles de données et est mieux adaptée lorsque vous savez déjà ce que vous recherchez.

Accédez à la **vue Arborescence** dans la barre latérale gauche.

![WIS2 Downloader Tree View](../assets/img/wis2-downloader-tree-view.png)

L'arborescence est organisée selon la hiérarchie des sujets WIS2. Développez chaque niveau en cliquant sur un nœud pour révéler ses enfants. À tout niveau, vous pouvez souscrire en sélectionnant un nœud et en cliquant sur **Subscribe** — en utilisant un caractère générique (`#`) pour capturer tous les sujets en dessous de ce nœud.

!!! note "Souscrire à différents niveaux"

    Souscrire plus haut dans l'arborescence (par exemple au niveau du Centre ID) capturera tous les ensembles de données publiés par ce centre. Souscrire plus bas offre un contrôle plus granulaire. Utilisez le suffixe générique `#` automatiquement ajouté par WIS2 Downloader lors de la souscription depuis la vue Arborescence.

### Exercice : trouver et souscrire via la vue Arborescence

!!! question "Souscrire à un ensemble de données via la vue Arborescence"

    Utilisez la vue Arborescence pour trouver et souscrire à des données d'observations de surface provenant d'un centre spécifique.

    1. Développez l'arborescence en commençant par le nœud `cache`, puis naviguez à travers `a` → `wis2`.
    2. Sélectionnez un Centre ID de votre choix et continuez à développer jusqu'à atteindre un sujet lié à `surface-based-observations`.
    3. Examinez le chemin complet du sujet affiché — confirmez qu'il correspond à l'ensemble de données souhaité.
    4. Définissez le dossier de destination sur `surface-obs-tree`.
    5. Cliquez sur **Subscribe** pour créer l'abonnement.

    Accédez à **Manage Subscriptions** pour confirmer que l'abonnement est actif.

??? success "Cliquez pour révéler la réponse"

    Tout chemin de sujet suivant le modèle `cache/a/wis2/<centre-id>/data/core/weather/surface-based-observations/#` est un choix valide. Le segment Centre ID variera en fonction du centre que vous avez sélectionné dans l'arborescence.

    La vue **Manage Subscriptions** affichera le nouvel abonnement aux côtés de ceux créés précédemment.

!!! note "Se désabonner et supprimer les fichiers téléchargés"
    
    Accédez à la vue **Manage Subscriptions** et `Unsubscribe` du sujet sélectionné dans l'exercice précédent.

    Ensuite, nettoyez le dossier de téléchargements :

    ```bash
    rm -fr /home/{USER}/wis2-downloads/surface-obs-tree
    ```

## Utilisation dans la vue Souscription manuelle

La **vue Souscription manuelle** vous permet de créer un abonnement en saisissant directement un sujet, sans dépendre des Global Discovery Catalogues. Contrairement aux vues Catalogue et Arborescence — qui tirent leurs sujets des GDCs — Souscription manuelle est utile lorsque vous connaissez déjà le sujet exact auquel vous souhaitez souscrire et que vous voulez le configurer sans parcourir le catalogue, avec plus de liberté sur le WTH à utiliser.

Accédez à la **vue Souscription manuelle** dans la barre latérale gauche.

![WIS2 Downloader Manual Subscribe](../assets/img/wis2-downloader-manual-subscribe.png)

Le formulaire vous permet de spécifier :

- **Topic** — le sujet MQTT complet auquel souscrire, incluant les caractères génériques (par exemple `#` & `+`).
- **Destination folder** — le sous-répertoire local où les fichiers téléchargés seront enregistrés.
- **Filter** — un objet de filtre optionnel sous forme de texte pour contrôler les notifications téléchargées.
- **Priority queue** — contrôle la priorité de téléchargement assignée aux notifications de cet abonnement.
- **Authentication** — les identifiants requis pour les ensembles de données protégés.

!!! note "Quand utiliser Souscription manuelle"

    Utilisez Souscription manuelle lorsque vous connaissez déjà le sujet exact souhaité et que vous voulez le configurer rapidement sans parcourir le catalogue, lorsque le sujet n'est pas inclus dans le catalogue, ou lorsque vous devez fournir des identifiants pour un ensemble de données protégé.

## Téléchargement depuis un ensemble de données protégé

Certains ensembles de données sur WIS2 sont protégés, ce qui signifie qu'ils nécessitent des identifiants valides avant que les fichiers puissent être téléchargés. WIS2 Downloader prend en charge deux méthodes d'authentification dans la vue Souscription manuelle :

- **Authentification HTTP basique** — fournissez un nom d'utilisateur et un mot de passe associés à vos identifiants d'accès.
- **Jeton Bearer** — fournissez un jeton émis par le fournisseur de données à la place d'un nom d'utilisateur et d'un mot de passe.

Ces identifiants sont stockés par abonnement et appliqués automatiquement lors du téléchargement des fichiers pour ce sujet.

### Exercice : souscrire à un ensemble de données protégé sur votre wis2box

Dans cet exercice, vous configurerez un ensemble de données protégé sur votre instance wis2box, configurerez WIS2 Downloader pour souscrire à son broker, et vérifierez que les fichiers sont correctement téléchargés lorsqu'un jeton Bearer est fourni.

!!! question "Configurer et souscrire à un ensemble de données protégé"

    **Étape 1 — Créer un ensemble de données protégé sur wis2box**

    Sur votre instance wis2box, créez un ensemble de données avec contrôle d'accès activé et notez le sujet et le jeton Bearer généré pour celui-ci. Si vous ne l'avez pas encore fait, consultez la session pratique [Datasets with access control](../datasets-with-access-control) pour les étapes complètes de configuration.

    **Étape 2 — Configurer WIS2 Downloader pour écouter le broker wis2box**

    Par défaut, WIS2 Downloader écoute le Global Broker. Pour recevoir des notifications directement de votre instance wis2box, vous devez ajouter un abonné dans le fichier compose de WIS2 Downloader qui pointe vers le broker MQTT interne de wis2box.

    Ouvrez le fichier `docker-compose.yml` dans votre répertoire WIS2 Downloader et ajoutez la configuration suivante pour l'abonné :

    ```yaml
      subscriber-test:
    container_name: subscriber-test
    restart: always
    build:
      context: .
      dockerfile: ./containers/subscriber/Dockerfile
      args:
        WIS2DOWNLOADER_UID: ${WIS2DOWNLOADER_UID:-10001}
        WIS2DOWNLOADER_GID: ${WIS2DOWNLOADER_GID:-988}
    env_file: *default-env
    environment:
      GLOBAL_BROKER_HOST: WIS2BOX_URL
      GLOBAL_BROKER_PORT: 443
      GLOBAL_BROKER_USERNAME: everyone
      GLOBAL_BROKER_PASSWORD: everyone
      MQTT_PROTOCOL: websockets
    depends_on:
      - redis
    networks:
      - redis-net
    logging: *loki-logging
    healthcheck:
      test: ["CMD", "pgrep", "-f", "subscriber_start"]
      interval: 30s
      timeout: 5s
      retries: 3
    ```

    Redémarrez la stack pour appliquer les modifications :

    ```bash
    docker compose down
    docker compose up -d
    ```

    **Étape 3 — Souscrire à l'ensemble de données dans WIS2 Downloader**

    1. Accédez à **Manual Subscribe** dans l'interface utilisateur de WIS2 Downloader.
    2. Définissez le sujet sur celui configuré pour votre ensemble de données protégé sur wis2box.
    3. Définissez le dossier de destination sur `restricted-data`.
    4. Entrez le jeton Bearer généré à l'étape 1 dans le champ **Authentication**.
    5. Cliquez sur **Subscribe** pour créer l'abonnement.

    **Étape 4 — Pousser des données vers l'ensemble de données sur wis2box**

    Sur votre instance wis2box, publiez un fichier dans l'ensemble de données protégé. Consultez la session pratique [Ingesting data for publication](../ingesting-data-for-publication) pour les étapes de publication des données.

    **Étape 5 — Vérifier le téléchargement**

    Vérifiez que le fichier a été téléchargé par WIS2 Downloader :

    ```bash
    ls /home/{USER}/wis2-downloads/restricted-data
    ```

??? success "Cliquez pour révéler la réponse"

    Avec un jeton Bearer valide, WIS2 Downloader s'authentifiera lors du téléchargement des fichiers pour le sujet protégé. Le fichier publié à l'étape 4 devrait apparaître dans le dossier `restricted-data` peu après avoir été ingéré par wis2box.

    Si l'authentification échoue, les fichiers ne seront pas téléchargés même si l'abonnement apparaît actif dans la vue **Manage Subscriptions**. Vérifiez que le jeton Bearer correspond à celui configuré sur l'ensemble de données dans wis2box.

!!! note "Se désabonner et supprimer les fichiers téléchargés"

    Accédez à la vue **Manage Subscriptions** et **Unsubscribe** du sujet, puis nettoyez le dossier de téléchargements :

    ```bash
    rm -fr /home/{USER}/wis2-downloads/restricted-data
    ```
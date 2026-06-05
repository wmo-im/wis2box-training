---
title: Téléchargement avec WIS2 Downloader
---

# Téléchargement avec WIS2 Downloader

!!! abstract "Objectifs d'apprentissage !"

    À la fin de cette session pratique, vous serez capable de :

    - trouver et vous abonner à des ensembles de données
    - utiliser des filtres pour contrôler les fichiers téléchargés
    - utiliser l'authentification pour télécharger des ensembles de données protégés par un accès
    - modifier la configuration par défaut de WIS2 Downloader pour des cas d'utilisation avancés

## Introduction

Dans WIS2, tous les ensembles de données possèdent un fichier de métadonnées qui peut être trouvé dans les **Global Discovery Catalogues**. Ainsi, il est prévu que les utilisateurs consultent toujours ces services pour trouver les données partagées sur WIS2.

WIS2 Downloader utilise ce principe en recherchant tous les enregistrements disponibles dans ces GDC et en les combinant en interne pour permettre à l'utilisateur de naviguer parmi les données disponibles sur WIS2. Étant donné le grand nombre d'enregistrements à afficher, il est essentiel de fournir un moyen à l'utilisateur de les filtrer pour trouver l'enregistrement approprié. Même après avoir trouvé et s'être abonné à l'enregistrement correct, certains ensembles de données peuvent contenir un nombre de fichiers supérieur aux besoins actuels de l'utilisateur. Pour cette raison, un deuxième niveau de filtrage est nécessaire — celui qui intervient au moment de décider si un fichier doit être téléchargé.

## Utilisation dans la vue Catalogue

La **vue Catalogue** est l'une des deux façons de trouver et de s'abonner à des ensembles de données dans WIS2 Downloader. Elle regroupe les enregistrements des Global Discovery Catalogues et les présente dans une interface consultable et filtrable — similaire à la navigation directe sur un portail GDC.

Accédez à la **vue Catalogue** dans la barre latérale gauche.

![WIS2 Downloader Catalogue View](../assets/img/wis2-downloader-catalogue-view.png)

En haut de la page, vous trouverez une barre de recherche et un ensemble de filtres. Vous pouvez les utiliser pour réduire la liste des enregistrements disponibles par mot-clé, Centre ID ou politique de données (core vs. recommended).

Vous pouvez également filtrer spatialement en définissant une **bounding box** à l'aide de quatre champs de coordonnées — **Nord**, **Ouest**, **Sud** et **Est** — exprimés en valeurs décimales de latitude et de longitude. Une fois la bounding box définie, vous pouvez choisir entre deux modes de correspondance :

- **Intersects** — retourne les enregistrements dont l'étendue spatiale chevauche la bounding box de quelque manière que ce soit.
- **Within** — retourne uniquement les enregistrements dont l'étendue spatiale se trouve entièrement à l'intérieur de la bounding box.

!!! note "Rechargement du catalogue"

    Le catalogue est chargé à partir des GDC lorsque WIS2 Downloader démarre. Si vous pensez que la liste est obsolète, vous pouvez forcer un rechargement depuis la section **Settings** dans la barre latérale gauche.

### Exercice : trouver et s'abonner à un ensemble de données

!!! question "Trouver un ensemble de données d'observations de surface"

    Utilisez les filtres dans la vue Catalogue pour trouver un ensemble de données **core** d'observations de surface lié à la température et aux précipitations.

    1. Tapez `surface` dans la barre de recherche et observez comment la liste des enregistrements est filtrée.
    2. Définissez le filtre de politique de données sur **core**.
    3. Ajoutez les mots-clés `temperature, precipitation` et observez comment les résultats changent.
    4. Sélectionnez un enregistrement dans les résultats pour afficher ses détails.
    5. Examinez les métadonnées affichées — notez le sujet, le centre d'origine et la politique de données.
    6. Définissez le dossier de destination sur `surface-obs`.
    7. Cliquez sur **Subscribe** pour créer l'abonnement.

    Après vous être abonné, accédez à **Manage Subscriptions** pour confirmer que le nouvel abonnement apparaît dans la liste.

??? success "Cliquez pour révéler la réponse"

    Tout enregistrement dont le sujet contient `surface-based-observations` et dont la politique de données est `core` est un choix valide. L'application du filtre de mots-clés `temperature, precipitation` permettra de réduire davantage les résultats aux ensembles de données pertinents pour ces variables.

    Une fois abonné, la vue **Manage Subscriptions** affichera l'abonnement actif avec son sujet et son dossier cible. Les fichiers commenceront à se télécharger à mesure que de nouvelles notifications arriveront sur le broker.

!!! note "Se désabonner et supprimer les fichiers téléchargés"
    
    Accédez à la vue **Manage Subscriptions** et cliquez sur `Unsubscribe` pour le sujet sélectionné dans l'exercice précédent.

    Ensuite, nettoyez le dossier de téléchargements :

    ```bash
    rm -fr /home/<username>/wis2-downloads/surface-obs
    ```

## Utilisation dans la vue Arborescence

La **vue Arborescence** présente la hiérarchie des sujets WIS2 sous forme d'arborescence repliable, permettant de parcourir les sujets disponibles niveau par niveau — similaire à la navigation dans les sujets avec MQTT Explorer. Elle est conçue pour une exploration de haut niveau des données disponibles sur WIS2, en commençant par la racine de la hiérarchie et en descendant. Cela contraste avec la vue Catalogue, qui vous mène directement aux enregistrements individuels des ensembles de données et est mieux adaptée lorsque vous savez déjà ce que vous recherchez.

Accédez à la **vue Arborescence** dans la barre latérale gauche.

![WIS2 Downloader Tree View](../assets/img/wis2-downloader-tree-view.png)

L'arborescence est organisée selon la hiérarchie des sujets WIS2. Développez chaque niveau en cliquant sur un nœud pour révéler ses enfants. À n'importe quel niveau, vous pouvez vous abonner en sélectionnant un nœud et en cliquant sur **Subscribe** — en utilisant un caractère générique (`#`) pour capturer tous les sujets sous ce nœud.

!!! note "S'abonner à différents niveaux"

    S'abonner plus haut dans l'arborescence (par exemple au niveau du Centre ID) capturera tous les ensembles de données publiés par ce centre. S'abonner plus bas permet un contrôle plus granulaire. Utilisez le suffixe `#` automatiquement ajouté par WIS2 Downloader lors de l'abonnement depuis la vue Arborescence.

### Exercice : trouver et s'abonner via la vue Arborescence

!!! question "S'abonner à un ensemble de données via la vue Arborescence"

    Utilisez la vue Arborescence pour trouver et vous abonner à des données d'observations de surface provenant d'un centre spécifique.

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
    
    Accédez à la vue **Manage Subscriptions** et cliquez sur `Unsubscribe` pour le sujet sélectionné dans l'exercice précédent.

    Ensuite, nettoyez le dossier de téléchargements :

    ```bash
    rm -fr /home/<username>/wis2-downloads/surface-obs-tree
    ```

## Utilisation de la vue Abonnement manuel

La **vue Abonnement manuel** vous permet de créer un abonnement en saisissant directement un sujet, sans dépendre des Global Discovery Catalogues. Contrairement aux vues Catalogue et Arborescence — qui tirent leurs sujets des GDC — l'abonnement manuel est utile lorsque vous connaissez déjà le sujet exact auquel vous souhaitez vous abonner et que vous souhaitez le configurer sans parcourir le catalogue, avec plus de liberté sur le WTH à utiliser.

Accédez à la **vue Abonnement manuel** dans la barre latérale gauche.

![WIS2 Downloader Manual Subscribe](../assets/img/wis2-downloader-manual-subscribe.png)

Le formulaire vous permet de spécifier :

- **Topic** — le sujet MQTT complet auquel s'abonner, y compris les caractères génériques (par exemple `#` et `+`).
- **Destination folder** — le sous-répertoire local où les fichiers téléchargés seront enregistrés.
- **Filter** — un objet de filtre optionnel sous forme de texte pour contrôler les notifications téléchargées.
- **Priority queue** — contrôle la priorité de téléchargement attribuée aux notifications de cet abonnement.
- **Authentication** — les identifiants requis pour les ensembles de données protégés par un accès.

!!! note "Quand utiliser l'abonnement manuel"

    Utilisez l'abonnement manuel lorsque vous connaissez déjà le sujet exact souhaité et que vous souhaitez le configurer rapidement sans parcourir le catalogue, lorsque le sujet n'est pas inclus dans le catalogue ou lorsque vous devez fournir des identifiants pour un ensemble de données protégé par un accès.

## Téléchargement à partir d'un ensemble de données protégé par un accès

Certains ensembles de données sur WIS2 sont protégés par un accès, ce qui signifie qu'ils nécessitent des identifiants valides avant que les fichiers puissent être téléchargés. WIS2 Downloader prend en charge deux méthodes d'authentification dans la vue Abonnement manuel :

- **Authentification HTTP basique** — fournissez un nom d'utilisateur et un mot de passe associés à vos identifiants d'accès.
- **Jeton Bearer** — fournissez un jeton émis par le fournisseur de données à la place d'un nom d'utilisateur et d'un mot de passe.

Ces identifiants sont stockés par abonnement et appliqués automatiquement lors du téléchargement des fichiers pour ce sujet.

### Exercice : s'abonner à un ensemble de données protégé par un accès sur votre wis2box

Dans cet exercice, vous configurerez un ensemble de données protégé par un accès sur votre instance wis2box, configurerez WIS2 Downloader pour s'abonner à son broker et vérifierez que les fichiers sont correctement téléchargés lorsqu'un jeton Bearer est fourni.

!!! question "Configurer et s'abonner à un ensemble de données protégé par un accès"

    **Étape 1 — Créer un ensemble de données protégé par un accès sur wis2box**

    Sur votre instance wis2box, créez un ensemble de données avec contrôle d'accès activé et notez le sujet et le jeton Bearer généré pour celui-ci. Si vous ne l'avez pas encore fait, consultez la session pratique [Datasets with access control](datasets-with-access-control.md) pour les étapes complètes de configuration.

**Étape 2 — Configurer WIS2 Downloader pour écouter le broker de wis2box**

Par défaut, WIS2 Downloader écoute le Global Broker. Pour recevoir des notifications directement depuis votre instance de wis2box, vous devez ajouter un abonné dans le fichier compose de WIS2 Downloader qui pointe vers le broker MQTT interne de wis2box.

Ouvrez le fichier `docker-compose.yml` dans le répertoire de WIS2 Downloader et ajoutez la configuration suivante pour l'abonné en remplaçant `WIS2BOX_URL` par l'URL de votre instance de wis2box :

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

**Étape 3 — S'abonner au dataset dans WIS2 Downloader**

1. Accédez à **Manual Subscribe** dans l'interface utilisateur de WIS2 Downloader.
2. Définissez le topic sur celui configuré pour votre dataset à accès contrôlé sur wis2box.
3. Définissez le dossier de destination sur `restricted-data`.
4. Entrez le bearer token généré à l'étape 1 dans le champ **Authentication**.
5. Cliquez sur **Subscribe** pour créer l'abonnement.

**Étape 4 — Pousser des données vers le dataset sur wis2box**

Sur votre instance de wis2box, publiez un fichier vers le dataset à accès contrôlé. Consultez la session pratique [Ingesting data for publication](ingesting-data-for-publication.md) pour les étapes d'ingestion des données.

**Étape 5 — Vérifier le téléchargement**

Vérifiez que le fichier a été téléchargé par WIS2 Downloader :

```bash
ls /home/<username>/wis2-downloads/restricted-data
```

??? success "Cliquez pour révéler la réponse"

Avec un bearer token valide, WIS2 Downloader authentifiera le téléchargement des fichiers pour le topic restreint. Le fichier publié à l'étape 4 devrait apparaître dans le dossier `restricted-data` peu après avoir été ingéré par wis2box.

Si l'authentification échoue, les fichiers ne seront pas téléchargés même si l'abonnement semble actif dans la vue **Manage Subscriptions**. Vérifiez que le bearer token correspond à celui configuré sur le dataset dans wis2box.

!!! note "Se désabonner et supprimer les fichiers téléchargés"

Accédez à la vue **Manage Subscriptions** et cliquez sur **Unsubscribe** pour le topic, puis nettoyez le dossier des téléchargements :

```bash
rm -fr /home/<username>/wis2-downloads/restricted-data
```

## Filtrage des téléchargements

Les filtres permettent de contrôler quels fichiers sont téléchargés depuis un abonnement au niveau des notifications — c'est le deuxième niveau de filtrage mentionné dans l'introduction. Plutôt que de télécharger tous les fichiers publiés sur un topic, vous pouvez définir un filtre pour que seules les notifications correspondant à des critères spécifiques déclenchent un téléchargement.

Après avoir sélectionné un dataset dans la **Catalogue View** ou la **Tree View**, un panneau de filtre apparaît sur le côté droit de l'écran avant de s'abonner. Ici, vous pouvez remplir les valeurs de filtre que vous souhaitez appliquer. WIS2 Downloader construit automatiquement l'objet filtre à partir de vos entrées.

Dans la vue **Manual Subscribe**, vous devez saisir cet objet filtre manuellement en remplissant le champ `Filter (JSON)` dans le formulaire.

!!! note "Entrées de filtre disponibles"

- **Type de média** — restreindre les téléchargements à des types de contenu spécifiques (par exemple, `application/bufr`).
- **Dataset** — restreindre les téléchargements à un dataset spécifique par son identifiant de métadonnées.
- **Boîte englobante** — restreindre les téléchargements aux notifications dont les données se trouvent dans une zone spatiale définie par les valeurs `north`, `south`, `east` et `west`.
- **Plage de date et heure** — restreindre les téléchargements aux notifications publiées dans une plage de temps spécifique.
- **Filtres personnalisés** — filtrer sur toute autre propriété de notification définie dans l'enregistrement de métadonnées en spécifiant la valeur de la propriété (par exemple, filtrer par `wigos_station_identifier` pour ne télécharger que les données d'une station spécifique).

Voici un exemple d'objet filtre généré à partir de ces entrées :

```json
{
  "rules": [
    {
      "id": "accept",
      "order": 1,
      "match": {
        "all": [
          {
            "any": [
              { "media_type": { "exists": false } },
              { "media_type": { "in": ["application/bufr", "application/x-bufr"] } }
            ]
          },
          { "metadata_id": { "in": ["urn:wmo:md:ir-irimo:core.surface-based-observations.temp"] } },
          { "bbox": { "north": 23.0, "south": 27.0, "east": 25.0, "west": 28.0 } },
          {
            "property": "pubtime",
            "type": "datetime",
            "between": ["2026-06-08T20:00:00+00:00", "2026-06-09T05:00:59+00:00"]
          },
          {
            "property": "wigos_station_identifier",
            "type": "string",
            "in": ["0-20000-0-78338"]
          }
        ]
      },
      "action": "accept"
    },
    {
      "id": "default",
      "order": 999,
      "match": { "always": true },
      "action": "reject",
      "reason": "No filter criteria matched"
    }
  ]
}
```

### Exercice : S'abonner avec un filtre

Utilisez la vue Catalogue pour trouver un dataset d'observation de surface et appliquez un filtre spatial avant de vous abonner.

1. Accédez à **Catalogue View** et recherchez un dataset d'observation de surface de votre choix.
2. Sélectionnez le dataset pour afficher ses détails dans le panneau de droite.
3. Dans les entrées de filtre, définissez une **boîte englobante** pour une région de votre choix.
4. Optionnellement, définissez un filtre de **type de média** pour restreindre les téléchargements aux fichiers BUFR.
5. Définissez le dossier de destination sur `filtered-obs`.
6. Cliquez sur **Subscribe** pour créer l'abonnement.

Attendez que les fichiers arrivent et vérifiez que seuls les fichiers correspondant à vos critères de filtre sont téléchargés.

??? success "Cliquez pour révéler la réponse"

Seules les notifications correspondant à toutes les conditions que vous avez définies seront acceptées et téléchargées. Toutes les autres seront rejetées par la règle par défaut.

!!! note "Se désabonner et supprimer les fichiers téléchargés"

Accédez à la vue **Manage Subscriptions** et cliquez sur **Unsubscribe** pour le topic, puis nettoyez le dossier des téléchargements :

```bash
rm -fr /home/<username>/wis2-downloads/filtered-obs
```

## Conclusion

!!! success "Félicitations !"

Dans cette session pratique, vous avez appris à :

- trouver et vous abonner à des datasets en utilisant les vues Catalogue et Tree View
- vous abonner directement à des topics en utilisant la vue Manual Subscribe
- appliquer des filtres pour contrôler quels fichiers sont téléchargés depuis un abonnement
- utiliser l'authentification pour télécharger des datasets à accès contrôlé
---
title: Configurer WIS2 Downloader sur votre VM étudiante
---

# Configurer WIS2 Downloader sur votre VM étudiante

!!! abstract "Objectifs d'apprentissage !"

    À la fin de cette session pratique, vous serez capable de :

    - configurer votre propre instance de "WIS2 Downloader" et gérer les configurations spécifiques requises
    - naviguer dans l'instance et configurer un abonnement
    - supprimer vos abonnements et retrouver vos données téléchargées

## Introduction

Dans cette session, vous apprendrez à configurer une instance de WIS2 Downloader sur la VM étudiante fournie et à naviguer dans ses différents services.

!!! note "À propos de WIS2 Downloader"
     
     WIS2 Downloader est disponible en tant que projet autonome Docker Compose. Il est recommandé de l'exécuter sur un serveur ou une machine virtuelle distincte de l'instance wis2box, afin d'éviter que les téléchargements n'interfèrent avec la publication des messages.

     Si vous souhaitez développer votre propre service pour vous abonner aux notifications WIS2 et télécharger des données, vous pouvez utiliser le [code source de WIS2 Downloader](https://github.com/World-Meteorological-Organization/wis2downloader) comme référence.
     
     Pour une alternative plus légère offrant des capacités de publication et de téléchargement de messages WIS2, veuillez consulter le projet [pywis-pubsub](https://github.com/World-Meteorological-Organization/pywis-pubsub).

## Préparation et exigences

!!! note "Si vous êtes sur un réseau restreint"

    Les étapes suivantes ne doivent être appliquées que si le downloader est exécuté sur un réseau différent et que les ports mentionnés sont inaccessibles. Dans toute configuration, ce sont les seuls ports nécessaires pour utiliser pleinement les capacités de la pile WIS2 Downloader.    

Avant de commencer, veuillez vous connecter à votre VM étudiante en vous assurant de tunneliser via SSH les ports suivants :

- `5002 (API)`
- `8080 (UI)`
- `3000 (Grafana)`

Pour ce faire, vous pouvez modifier les paramètres de votre connexion dans Putty en ajoutant les 3 mappages de ports vers les ports de votre propre PC (localhost) :

![ajouter des tunnels dans putty](../assets/img/putty-add-tunnel.png)

!!! note "Tunnelisation sous Linux et macOS"

    Sous Linux et macOS, vous pouvez configurer les mêmes tunnels directement depuis le terminal en utilisant l'option `-L` avec votre commande SSH :

    ```bash
    ssh -L 5002:localhost:5002 -L 8080:localhost:8080 -L 3000:localhost:3000 <username>@<WIS2DOWNLOADER_BASE_URL>
    ```

    Remplacez `<username>` et `<WIS2DOWNLOADER_BASE_URL>` par vos identifiants de VM étudiante.

## Installation de WIS2 Downloader

Téléchargez la dernière version tarball depuis GitHub et extrayez-la sur votre VM étudiante :

```bash
wget https://github.com/World-Meteorological-Organization/wis2downloader/archive/refs/tags/v1.0.0b1+rc4.tar.gz
tar -xzf v1.0.0b1+rc4.tar.gz
cd wis2downloader-*
```

Exécutez le script de configuration pour générer votre fichier de configuration :

```bash
bash setup.sh
```

Utilisez le chemin de téléchargement suivant `/home/<username>/wis2-downloads` en remplaçant `<username>` par votre nom d'utilisateur. Ensuite, appuyez sur Entrée pour utiliser les valeurs par défaut pour l'utilisateur et les groupes.

!!! note "Gestion des permissions utilisateur"
    Vous pouvez utiliser différentes valeurs pour l'utilisateur et le groupe en modifiant `WIS2DWONLOADER_UID` et `WIS2DWONLOADER_GID` dans le fichier .env.
    N'oubliez pas de reconstruire les images après avoir modifié ces valeurs pour appliquer les changements. 

Cela crée un fichier `.env` à partir des valeurs par défaut et génère des valeurs aléatoires pour `FLASK_SECRET_KEY` et `REDIS_PASSWORD`. Vous pouvez consulter le fichier avec `cat .env` — les valeurs par défaut conviennent à un déploiement sur une seule machine.

Démarrez la pile complète de services :

```bash
docker compose up -d
```

!!! note "Vérification des conteneurs en cours d'exécution"
    Vous pouvez vérifier que tous les conteneurs ont démarré avec succès avec :
    ```bash
    docker compose ps
    ```
    Vous devriez voir des services pour le gestionnaire d'abonnement, les abonnés MQTT, l'interface utilisateur, les workers Celery, Redis, Prometheus, Grafana et Loki.

## Accéder à l'interface utilisateur de WIS2 Downloader

Ouvrez un navigateur web et accédez à l'interface utilisateur de votre instance WIS2 Downloader en allant sur `http://<WIS2DOWNLOADER_BASE_URL>:8080`.

Vous vous retrouverez sur la page d'accueil qui est par défaut configurée sur la vue `Dashboard`, affichant le tableau de bord Grafana.

![Page d'accueil de WIS2 Downloader](../assets/img/wis2-downloader-landing-page.png)

Dans le menu latéral gauche, vous pourrez naviguer dans toutes les différentes sections de l'interface utilisateur.

Les principales sections disponibles sont :

- **Dashboard** — la page d'accueil par défaut, un tableau de bord Grafana intégré montrant l'activité de téléchargement, l'état de la file d'attente et les métriques du service en cours d'exécution. Également disponible à `http://<WIS2DOWNLOADER_BASE_URL>:3000`.
- **Catalogue View** — parcourir les ensembles de données WIS2 disponibles en recherchant ou en filtrant le catalogue global. Sélectionnez un sujet et un répertoire de sauvegarde, puis cliquez sur *Subscribe* pour commencer le téléchargement.
- **Tree View** — naviguer dans la hiérarchie des sujets WIS2 sous forme d'arbre pliable. Utile pour explorer les sujets disponibles avant de s'abonner.
- **Manual Subscribe** — créer un abonnement en saisissant directement les détails d'un sujet, sans dépendre des Global Discovery Catalogues. Utile pour s'abonner à des sujets plus librement en utilisant autant de jokers que nécessaire et permet d'accéder à des sujets non trouvés sur les GDC, tels que les passerelles GTS et les sujets publiés sur des brokers privés lorsqu'ils sont utilisés dans des configurations non par défaut.
- **Manage Subscriptions** — afficher et gérer tous les abonnements actifs. À partir de là, vous pouvez voir quels sujets sont surveillés et supprimer ceux dont vous n'avez plus besoin.
- **Settings** — permet actuellement de recharger le catalogue de données à partir des Global Discovery Catalogues. Cette section sera étendue dans les futures versions pour couvrir la configuration générale et la gestion de WIS2 Downloader.
- **Documentation** — affichant la documentation intégrée pour WIS2 Downloader.

## Gestion des abonnements dans l'interface utilisateur

Comme dans l'exemple précédent, vous accéderez à l'interface utilisateur de l'instance en cours d'exécution en allant sur `http://<WIS2DOWNLOADER_BASE_URL>:8080`.

Il existe 3 façons de configurer un abonnement :

- Dans la **Catalogue View** en parcourant les sujets disponibles de manière similaire aux portails GDC.
- Dans la **Tree View** en sélectionnant un sujet du catalogue GDC en explorant les sujets comme dans MQTT Explorer.
- Dans **Manual Subscribe** où vous pouvez saisir vos propres sujets, filtres et autres paramètres souhaités.

Pour l'exercice suivant, nous nous abonnerons à toutes les notifications synop provenant de tous les nœuds WIS2 :

- Tout d'abord, allez dans **Manual Subscribe**.
- Saisissez le sujet comme `cache/a/wis2/+/data/core/weather/surface-based-observations/synop`
- Définissez le dossier de destination comme `synop-data`

Le résultat final devrait ressembler à ceci :
![WIS2 Downloader Manual Subscribe](../assets/img/wis2-downloader-manual-subscribe.png)

Maintenant, appuyez sur le bouton **Subscribe** et confirmez votre abonnement.

Ensuite, vérifiez le dossier de téléchargement sur votre VM étudiante en utilisant la commande :

```bash
ls -R ~/wis2-downloads
```

Et vous devriez maintenant voir une série de fichiers qui ont été téléchargés par votre instance.

En dernière étape, nous pouvons supprimer l'abonnement en allant dans la vue **Manage Subscriptions** et en appuyant sur le bouton **Unsubscribe**.

![WIS2 Downloader Delete Subscription](../assets/img/wis2-downloader-delete-subscription.png)

!!! note "Suppression des fichiers téléchargés"

    Il est recommandé de nettoyer le dossier de téléchargements après avoir terminé un exercice afin de libérer de l'espace sur la VM étudiante. Pour ce faire, exécutez la commande suivante pour supprimer les fichiers des exercices précédents.

    ```bash
    rm -fr ~/wis2-downloads/synop-data
    ```

## Révision de la configuration de WIS2 Downloader

L'instance WIS2 Downloader est configurée à l'aide des variables d'environnement définies dans votre fichier `.env`.

Vous pouvez consulter une répartition des variables d'environnement dans la [Section 2.1 du Guide Administrateur de WIS2 Downloader](https://world-meteorological-organization.github.io/wis2downloader/en/admin-guide.html)

Pour examiner la configuration actuelle de WIS2 Downloader, vous pouvez utiliser la commande suivante :

```bash
cat .env
```

!!! question "Examiner la configuration de WIS2 Downloader"

    Quelle est la période de rétention par défaut pour les données téléchargées ?

    Quel port l'API du gestionnaire d'abonnement écoute-t-elle ?

??? success "Cliquez pour révéler la réponse"

    La période de rétention par défaut pour les données téléchargées est de `30` jours, comme défini par `DOWNLOAD_RETENTION_PERIOD`.

    L'API du gestionnaire d'abonnement écoute sur le port `5002`, comme défini dans `WIS2DOWNLOADER_SUBSCRIPTION_MANAGER_URL`.

!!! note "Mise à jour de la configuration de WIS2 Downloader"

    Pour mettre à jour la configuration, modifiez le fichier `.env` et redémarrez la pile pour appliquer les changements :

    ```bash
    docker compose up -d
    ```

Vous pouvez conserver la configuration par défaut pour les prochains exercices.

## API de WIS2 Downloader

WIS2 Downloader expose une API REST à `<WIS2DOWNLOADER_BASE_URL>:5002`. Confirmez que le service est prêt :

```bash
curl localhost:5002/health
```

Vous devriez voir :

```json
{"status": "healthy"}
```

Pour créer un abonnement, envoyez une requête `POST` avec le `topic` MQTT et un sous-répertoire `target` optionnel où les fichiers seront sauvegardés :

```bash
curl -s -X POST localhost:5002/subscriptions \
  -H "Content-Type: application/json" \
  -d '{"topic": "cache/a/wis2/+/data/core/weather/surface-based-observations/#", "target": "surface-obs"}'
```

Comme précédemment, les fichiers téléchargés peuvent être consultés en vérifiant le dossier `surface-obs` dans le répertoire de téléchargement :

```bash
ls -R ~/wis2-downloads/surface-obs
```

La réponse inclut l'UUID attribué au nouvel abonnement. Utilisez-le pour supprimer l'abonnement lorsqu'il n'est plus nécessaire :

```bash
curl -X DELETE localhost:5002/subscriptions/{id}
```

!!! note "Suppression des fichiers téléchargés"

    Il est recommandé de nettoyer le dossier de téléchargements après avoir terminé un exercice afin de libérer de l'espace sur la VM étudiante. Pour ce faire, exécutez la commande suivante pour supprimer les fichiers des exercices précédents.

    ```bash
    rm -fr ~/wis2-downloads/surface-obs
    ```

Pour la liste complète des points de terminaison disponibles (liste, récupération, mise à jour des abonnements, etc.), consultez la documentation interactive Swagger disponible à `localhost:5002/swagger`.

## Conclusion

!!! success "Félicitations !"

    Dans cette session pratique, vous avez appris à :

    - installer WIS2 Downloader sur votre système local et modifier les configurations par défaut
    - interagir avec l'interface utilisateur pour créer et supprimer des abonnements
    - gérer les abonnements à l'aide de l'API
    - consulter les données téléchargées sur votre système local
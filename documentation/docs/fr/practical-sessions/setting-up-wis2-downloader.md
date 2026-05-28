---
title: Configurer WIS2 Downloader sur votre VM étudiant
---

# Configurer WIS2 Downloader sur votre VM étudiant

!!! abstract "Objectifs d'apprentissage !"

    À la fin de cette session pratique, vous serez capable de :

    - configurer votre propre instance de "WIS2 Downloader" et gérer les configurations spécifiques requises
    - naviguer dans l'instance pour utiliser ses différentes fonctionnalités

## Introduction

Dans cette session, vous apprendrez à configurer une instance de WIS2 Downloader sur la VM étudiant fournie et à naviguer dans ses différents services.

!!! note "À propos de WIS2 Downloader"
     
     WIS2 Downloader est disponible en tant que projet autonome Docker Compose et il est recommandé de l'exécuter sur un serveur séparé de wis2box, afin d'éviter que les téléchargements n'interfèrent avec la publication des messages.

     Si vous souhaitez développer votre propre service pour vous abonner aux notifications WIS2 et télécharger des données, vous pouvez utiliser le [code source de WIS2 Downloader](https://github.com/World-Meteorological-Organization/wis2downloader) comme référence.

## Préparation et exigences

!!! note "Si ce n'est pas pendant la formation"

    Les étapes suivantes ne doivent être appliquées que si les ports mentionnés ne sont pas disponibles par défaut sur le serveur. Dans toute configuration, ce sont les seuls ports nécessaires pour accéder à toutes les fonctionnalités de la pile WIS2 Downloader.

Avant de commencer, connectez-vous à votre VM étudiant en vous assurant de tunneliser via SSH les ports suivants :

- `5002 (API)`
- `8080 (UI)`
- `3000 (Grafana)`

Pour ce faire, vous pouvez modifier les paramètres de votre connexion dans Putty :

![access putty tunnel settings](../assets/img/putty-tunnel-settings.png)

Ajoutez ensuite le mappage des 3 ports vers des ports sur votre propre PC (localhost) :

![adding tunnels in putty](../assets/img/putty-add-tunnel.png)

## Installation de WIS2 Downloader

Téléchargez la dernière version tarball depuis GitHub et extrayez-la sur votre VM étudiant :

```bash
wget https://github.com/World-Meteorological-Organization/wis2downloader/releases/latest/download/wis2downloader-latest.tar.gz
tar -xzf wis2downloader-latest.tar.gz
cd wis2downloader-*
```

Exécutez le script de configuration pour générer votre fichier de configuration :

```bash
bash setup.sh
```

Cela crée un fichier `.env` à partir des valeurs par défaut et génère des valeurs aléatoires pour `FLASK_SECRET_KEY` et `REDIS_PASSWORD`. Vous pouvez examiner le fichier avec `cat .env` — les valeurs par défaut conviennent à un déploiement sur une seule machine.

Installez le plugin Docker Loki utilisé pour l'envoi des journaux :

```bash
ARCH=$(uname -m | sed 's/x86_64/amd64/;s/aarch64/arm64/')
docker plugin install grafana/loki-docker-driver:3.6.7-${ARCH} --alias loki --grant-all-permissions
```

Vérifiez que le plugin est activé :

```bash
docker plugin ls
```

Vous devriez voir `loki:latest` listé avec `ENABLED` défini sur `true`.

Créez un groupe dédié `wis2`, ajoutez votre utilisateur à ce groupe et configurez le fichier `.env` ainsi que le répertoire de téléchargements en conséquence :

```bash
sudo groupadd wis2
sudo usermod -aG wis2 $USER
sed -i "s/^UID=.*/UID=$(id -u)/" .env
sed -i "s/^GID=.*/GID=$(getent group wis2 | cut -d: -f3)/" .env
mkdir -p downloads
sudo chown $(id -un):wis2 downloads
chmod 775 downloads
```

!!! note "Reconnexion requise"
    Le changement d'appartenance au groupe ne prend effet qu'après vous être déconnecté et reconnecté à votre session SSH.

Démarrez la pile complète de services :

```bash
docker compose up -d
```

Attendez environ 30 secondes que les vérifications de santé soient effectuées, puis confirmez que le gestionnaire d'abonnement est prêt :

```bash
curl http://localhost:5002/health
```

!!! note "Vérification des conteneurs en cours d'exécution"
    Vous pouvez vérifier que tous les conteneurs ont démarré avec succès avec :
    ```bash
    docker compose ps
    ```
    Vous devriez voir des services pour le gestionnaire d'abonnement, les abonnés MQTT, l'interface utilisateur, les workers Celery, Redis, Prometheus, Grafana et Loki.

### Accéder à l'interface utilisateur de WIS2 Downloader

Ouvrez un navigateur web et accédez à l'interface utilisateur de votre instance WIS2 Downloader en allant sur `http://localhost:8080`.

Vous arriverez sur la page d'accueil, qui est par défaut définie sur la section `Help` affichant la documentation.

![WIS2 Downloader Landing Page](../assets/img/wis2-downloader-landing-page.png)

Dans le menu de la barre latérale gauche, vous pourrez naviguer dans toutes les différentes sections de l'interface utilisateur.

Les principales sections disponibles sont :

- **Dashboard** — un tableau de bord Grafana intégré affichant l'activité de téléchargement, l'état des files d'attente et les métriques du service en cours d'exécution. Également disponible sur `http://localhost:3000`.
- **Catalogue View** — parcourez les ensembles de données WIS2 disponibles en recherchant ou en filtrant le catalogue global. Sélectionnez un sujet et un répertoire de sauvegarde, puis cliquez sur *Subscribe* pour commencer le téléchargement.
- **Tree View** — naviguez dans la hiérarchie des sujets WIS2 sous forme d'arborescence extensible. Utile pour explorer les sujets disponibles avant de s'abonner.
- **Manual Subscription** — créez un abonnement en entrant directement un sujet et les détails du broker, sans dépendre des Global Discovery Catalogues. Utile pour s'abonner à des sujets provenant de WIS2 Nodes spécifiques ou de brokers privés.
- **Subscriptions** — consultez et gérez tous les abonnements actifs. À partir de cette section, vous pouvez voir quels sujets sont surveillés et supprimer ceux dont vous n'avez plus besoin.
- **Settings** — permet actuellement de recharger le catalogue de données à partir des Global Discovery Catalogues. Cette section sera étendue dans les futures versions pour couvrir la configuration générale et la gestion de WIS2 Downloader.
- **Help** — la page d'accueil par défaut, affichant la documentation intégrée de WIS2 Downloader.

### Examiner la configuration de WIS2 Downloader

L'instance WIS2 Downloader peut être configurée à l'aide des variables d'environnement définies dans votre fichier `.env`.

Vous pouvez consulter une répartition des variables d'environnement dans la [Section 2.1 du Guide Administrateur de WIS2 Downloader](https://world-meteorological-organization.github.io/wis2downloader/en/admin-guide.html).

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

!!! note "Mettre à jour la configuration de WIS2 Downloader"

    Pour mettre à jour la configuration, modifiez le fichier `.env` et redémarrez la pile pour appliquer les modifications :

    ```bash
    docker compose up -d
    ```

Vous pouvez conserver la configuration par défaut pour les prochains exercices.

### API de WIS2 Downloader

WIS2 Downloader expose une API REST à `<WIS2DOWNLOADER_BASE_URL>:5002/api`. Confirmez que le service est prêt :

```bash
curl <WIS2DOWNLOADER_BASE_URL>:5002/api/health
```

Vous devriez voir :

```json
{"status": "healthy"}
```

Pour créer un abonnement, envoyez une requête `POST` avec le `topic` MQTT et un sous-répertoire `target` optionnel où les fichiers seront sauvegardés :

```bash
curl -s -X POST <WIS2DOWNLOADER_BASE_URL>:5002/api/subscriptions \
  -H "Content-Type: application/json" \
  -d '{"topic": "cache/a/wis2/+/data/core/weather/surface-based-observations/#", "target": "surface-obs"}'
```

La réponse inclut l'UUID attribué au nouvel abonnement. Utilisez-le pour supprimer l'abonnement lorsque vous n'en avez plus besoin :

```bash
curl -X DELETE <WIS2DOWNLOADER_BASE_URL>:5002/api/subscriptions/{id}
```

Pour la liste complète des points de terminaison disponibles (liste, consultation, mise à jour des abonnements, etc.), consultez la documentation interactive Swagger disponible à `<WIS2DOWNLOADER_BASE_URL>:5002/api/openapi`.

## Conclusion

!!! success "Félicitations !"

    Dans cette session pratique, vous avez appris à :

    - installer WIS2 Downloader sur votre système local et modifier les configurations par défaut
    - interagir avec l'interface utilisateur pour créer et supprimer des abonnements
    - gérer les abonnements via l'API
    - consulter les données téléchargées sur votre système local
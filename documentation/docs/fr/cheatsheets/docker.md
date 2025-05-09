---
title: Docker cheatsheet
---

# Docker cheatsheet

## Vue d'ensemble

Docker permet de créer des environnements virtuels de manière isolée pour soutenir la virtualisation des ressources informatiques. Le concept de base derrière Docker est la conteneurisation,
où le logiciel peut fonctionner comme des services, interagissant avec d'autres conteneurs de logiciels, par exemple.

Le flux de travail typique de Docker implique la création et la construction d'**images**, qui sont ensuite exécutées comme des **conteneurs** actifs.

Docker est utilisé pour exécuter la suite de services qui composent wis2box en utilisant des images préconstruites.

### Gestion des images

* Lister les images disponibles

```bash
docker image ls
```

* Mettre à jour une image :

```bash
docker pull my-image:latest
```

* Supprimer une image :

```bash
docker rmi my-image:local
```

### Gestion des volumes

* Lister tous les volumes créés :

```bash
docker volume ls
```

* Afficher des informations détaillées sur un volume :

```bash
docker volume inspect my-volume
```

* Supprimer un volume :

```bash
docker volume rm my-volume
```

* Supprimer tous les volumes inutilisés :

```bash
docker volume prune
```

### Gestion des conteneurs

* Afficher une liste des conteneurs actuellement en cours d'exécution :

```bash
docker ps
```

* Liste de tous les conteneurs :

```bash
docker ps -a
```

* Entrer dans le terminal interactif d'un conteneur en cours d'exécution :

!!! tip

    utilisez `docker ps` pour utiliser l'identifiant du conteneur dans la commande ci-dessous

```bash
docker exec -it my-container /bin/bash
```

* Supprimer un conteneur

```bash
docker rm my-container
```

* Supprimer un conteneur en cours d'exécution :

```bash
docker rm -f my-container
```
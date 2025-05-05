---
title: Docker cheatsheet
---

# Docker cheatsheet

## Panoramica

Docker permette la creazione di ambienti virtuali in modo isolato a supporto della virtualizzazione delle risorse di calcolo. Il concetto di base dietro Docker è la containerizzazione, dove il software può essere eseguito come servizi, interagendo con altri container di software, ad esempio.

Il flusso di lavoro tipico di Docker coinvolge la creazione e la costruzione di **immagini**, che vengono poi eseguite come **container** attivi.

Docker è utilizzato per eseguire la suite di servizi che compongono wis2box utilizzando immagini pre-costruite.

### Gestione delle immagini

* Elenca le immagini disponibili

```bash
docker image ls
```

* Aggiorna un'immagine:

```bash
docker pull my-image:latest
```

* Rimozione di un'immagine:

```bash
docker rmi my-image:local
```

### Gestione dei volumi

* Elenca tutti i volumi creati:

```bash
docker volume ls
```

* Visualizza informazioni dettagliate su un volume:

```bash
docker volume inspect my-volume
```

* Rimuovi un volume:

```bash
docker volume rm my-volume
```

* Rimuovi tutti i volumi inutilizzati:

```bash
docker volume prune
```

### Gestione dei container

* Visualizza un elenco dei container attualmente in esecuzione:

```bash
docker ps
```

* Elenco di tutti i container:

```bash
docker ps -a
```

* Entra nel terminale interattivo di un container in esecuzione:


!!! tip

    usa `docker ps` per utilizzare l'id del container nel comando sottostante

```bash
docker exec -it my-container /bin/bash
```

* Rimuovi un container

```bash
docker rm my-container
```

* Rimuovi un container in esecuzione:

```bash
docker rm -f my-container
```

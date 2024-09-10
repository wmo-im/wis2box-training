---
title: Docker cheatsheet
---

# Docker cheatsheet

## Overview

Docker allows for creating virtual environments in an isolated manner in support
of virtualization of computing resources.  The basic concept behind Docker is containerization,
where software can run as services, interacting with other software containers, for example.

The typical Docker workflow involves creating and building **images**, which are then run as live **containers**.

Docker is used to run the suite of services that make up wis2box using pre-built images.

### Image management

* List available images

```bash
docker image ls
```

* Update an image:

```bash
docker pull my-image:latest
```

* Removing an image:

```bash
docker rmi my-image:local
```

### Volume Management

* List all created volumes:

```bash
docker volume ls
```

* Display detailed information on a volume:

```bash
docker volume inspect my-volume
```

* Remove a volume:

```bash
docker volume rm my-volume
```

* Remove all unused volumes:

```bash
docker volume prune
```

### Container Management

* Display a list of currently running containers:

```bash
docker ps
```

* List of all containers:

```bash
docker ps -a
```

* Enter the interactive terminal of a running container:


!!! tip

    use `docker ps` to use the container id in the command below

```bash
docker exec -it my-container /bin/bash
```

* Remove a container

```bash
docker rm my-container
```

* Remove a running container:

```bash
docker rm -f my-container
```

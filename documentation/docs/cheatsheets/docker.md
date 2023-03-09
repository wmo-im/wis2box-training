---
title: Docker cheatsheet
---

# Docker cheatsheet

## Overview

Docker allows for creating virtual envronments in an isolated manner in support
of virtualization of computing resources.  The basic concept behind Docker is containerization,
where software can run as services, interacting with other software containers, for example.

The typical Docker workflow involves creating and building **images**, which are then run as live **containers**.

### Image management

* List available images

```bash
docker images
```

* Build an image from a Dockerfile:

```bash
cat << EOF > Dockerfile
FROM ubuntu:latest

RUN apt-get update
RUN apt-get install –y nginx

CMD ["echo", "Hello from my first Docker setup!"]
EOF
```

* Building the image:

```bash
docker build -t my-image:local .
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

* Create a volume:

```bash
docker volume create my-volume
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

* Create a container from an image, with an interactive terminal (`-it`) and a mounted volume (`v`):

```bash
docker run -it -v ${pwd}:/app my-image:local
```

* Display a list of currently running containers:

```bash
docker ps
```

* List of all containers:

```bash
docker ps -a
```

* Start a container:

```bash
docker start my-image:local  # starts a new container
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

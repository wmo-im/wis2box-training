---
title: Docker cheatsheet
---

# Docker cheatsheet

## Visión general

Docker permite la creación de entornos virtuales de manera aislada en apoyo
de la virtualización de recursos informáticos. El concepto básico detrás de Docker es la contenerización,
donde el software puede funcionar como servicios, interactuando con otros contenedores de software, por ejemplo.

El flujo de trabajo típico de Docker implica crear y construir **imágenes**, que luego se ejecutan como **contenedores** activos.

Docker se utiliza para ejecutar el conjunto de servicios que componen wis2box utilizando imágenes preconstruidas.

### Gestión de imágenes

* Listar imágenes disponibles

```bash
docker image ls
```

* Actualizar una imagen:

```bash
docker pull my-image:latest
```

* Eliminar una imagen:

```bash
docker rmi my-image:local
```

### Gestión de volúmenes

* Listar todos los volúmenes creados:

```bash
docker volume ls
```

* Mostrar información detallada de un volumen:

```bash
docker volume inspect my-volume
```

* Eliminar un volumen:

```bash
docker volume rm my-volume
```

* Eliminar todos los volúmenes no utilizados:

```bash
docker volume prune
```

### Gestión de contenedores

* Mostrar una lista de contenedores actualmente en ejecución:

```bash
docker ps
```

* Lista de todos los contenedores:

```bash
docker ps -a
```

* Entrar al terminal interactivo de un contenedor en ejecución:


!!! tip

    use `docker ps` para usar el id del contenedor en el comando a continuación

```bash
docker exec -it my-container /bin/bash
```

* Eliminar un contenedor

```bash
docker rm my-container
```

* Eliminar un contenedor en ejecución:

```bash
docker rm -f my-container
```
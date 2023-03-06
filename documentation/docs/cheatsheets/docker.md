---
title: Docker cheatsheet
---

# Docker Cheatsheet

### Using a New Image
* Building the image:

    ```console
    docker build -t <image_name> <dir_of_dockerfile>
    ```

    **Note**: If you are in the directory of the Docker file already, this is more simply:

    ```console
    docker build -t <image_name> .
    ```


### Volume Management
* Create a volume: 

    ```console
    docker volume create <volume_name>
    ```

* List all created volumes: 

    ```console
    docker volume ls
    ```

* Display detailed information on a volume: 

    ```console
    docker volume inspect <volume_name>
    ```

* Remove a volume: 

    ```console
    docker volume rm <volume_name>
    ```

* Remove all unused volumes:

    ```console
    docker volume prune
    ```

### Container Management
* Create a container from an image, with an interactive terminal (`it`) and a mounted volume (`v`): 

    ```console
    docker run -it -v ${pwd}:/app <image_name>
    ```

* Display a list of currently running containers:
    
    ```console
    docker ps
    ```

    ...or a list of all containers:
    
    ```console
    docker ps -a
    ```

* Start a stopped container: 

    ```console
    docker start <container_name>
    ```

* Enter the interactive terminal of a running container: 

    ```console
    docker exec -it <container_name> bash
    ```

* Remove a container 

    ```console
    docker rm <container_name>
    ```

* Remove a running container: 

    ```console
    docker rm -f <container_name>
    ```
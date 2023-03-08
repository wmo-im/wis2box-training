---
title: Access your student-VM
...

# Access your student-VM

## Introduction

During WIS2-in-a-box local training sessions you can access your personal student-VM on the local training network "WIS2-training". 

If you want to run this training outside of a local training session, please provide your own instance as detailed at [training-environment](https://wmoomm-my.sharepoint.com/:p:/g/personal/tproescholdt_wmo_int/EQoxn5WS7kBAoe5iNyfeteABAjw67YZBvEWM92NlWUu5wQ?e=gtgm13).

In this session you will ensure you can connect to your student-VM, check pre-installed software and download the exercise-materials.

## Connect to your student VM on the local training network

Use the following to connect your PC the local WiFi broadcasted in the room during WIS2-training:

- SSID: WIS2-training
- password: dataismagic!

Use an SSH-client to connect to your student-VM using the following:

-   Host: country-lastname.wis2box.training -> **replace with your country and lastname**
-   Port: 22
-   Username: lastname -> **replace with your lastname**
-   Password: namibia2023

!!! tip
    Contact a trainer if you are unsure about the host-name or have an issue connecting. 

Once connected, please change your password to ensure others can not access your VM:

```bash
limper@student-vm:~$ passwd
Changing password for limper.
Current password:
New password:
Retype new password:
passwd: password updated successfully
```

## Verify software versions

Your student-VM comes with python, docker and docker-compose installed. 


Check docker version:
```bash
docker --version
```
returns:
```bash
Docker version 20.10.17, build 100c701
```

Check docker-compose version:
```bash
docker-compose --version
```
returns:
```bash
docker-compose version 1.29.2, build unknown
```

Check python version:
```bash
python3 --version
```
returns:
```bash
Python 3.8.10
```

## Run docker 'hello-world'

On the local training environment your student-account has been added to the 'docker'-group to allow you to start docker-containers. You can verify this by running the docker 'hello-world' command:

```bash
docker run -it hello-world
```

This commands download the 'hello-world'-image from the local registry and interactively runs a docker-container for this image.

!!! tip
    
    If you get an error it is often an indication your user does not have permission to access the docker file-system. The user running docker-commands must be added to the 'docker'-group to be allowed to run docker-containers.

## Review docker system usage 

Inspect you local docker system usage using the command:

```bash
docker system df
```

!!! question
    What usage can you currently observe for your docker system?

Clean-up your docker system with the command:

```bash
docker system prune -a
```

Verify docker system is now clean:
```bash
docker system df
```

should return:
```bash
TYPE            TOTAL     ACTIVE    SIZE      RECLAIMABLE
Images          0         0         0B        0B
Containers      0         0         0B        0B
Local Volumes   0         0         0B        0B
Build Cache     0         0         0B        0
```

## Download the exercise materials

Please download the exercise materials on your local VM now and extract the archive with the following commands:

```bash
wget https://wmo-im.github.io/wis2box-training/exercise-materials.zip
unzip https://wmo-im.github.io/wis2box-training/exercise-materials.zip
```

Inspect the content of the new directory 'exercise-materials', these are the materials your will use in some of the other practical sessions:

```bash
ls exercise-materials/*
```

## Learning outcomes

You should now be able to:

- Access your student VM over SSH
- Verify the version for python, docker and docker-compose on your student-VM
- Verify docker commands can be successfully run
- Know how to check docker system usage
- Access the exercises-materials for this training on your student-VM


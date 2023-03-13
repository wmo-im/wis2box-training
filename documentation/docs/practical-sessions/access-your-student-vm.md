---
title: Access your student VM
---

# Access your student VM

## Introduction

In this session you will ensure you can connect to your student VM, check pre-installed software and download the exercise materials.

As part of locally run wis2box training sessions, you can access your personal student VM on the local training network named "WIS2-training".

If you want to run this training outside of a local training session, you can provide your own instance using any Cloud Provider:

- GCP (Google Cloud Platform) VM instance ‘e2-medium’
- AWS (Amazon Web Services)  ec2-instance ‘t3a.medium’ 
- Azure (Microsoft) Azure Virtual Machine ‘standard_b2s’

Select Ubuntu Server 20.0.4 LTS as OS and install docker engine (20.0.17) and docker-compose (1.29.2). Please also install python3 (3.8) and python3-pip. 

## Connect to your student VM on the local training network

Use the following configuraiton to connect your PC on the local WiFi broadcasted in the room during WIS2 training:

- **SSID: WIS2-training**
- **password: dataismagic!**

Use an SSH client to connect to your student VM using the following:

- **Host: country-lastname.wis2box.training** (replace with your country and lastname)
- **Port: 22**
- **Username: lastname** (replace with your lastname)
- **Password: namibia2023**

!!! tip
    Contact a trainer if you are unsure about the hostname or have issues connecting.

Once connected, please change your password to ensure others cannot access your VM:

```bash
limper@student-vm:~$ passwd
Changing password for limper.
Current password:
New password:
Retype new password:
passwd: password updated successfully
```

## Verify software versions

Your student VM comes with Python, Docker and Docker Compose pre-installed.

Check docker version:
```bash
docker --version
```
returns:
```bash
Docker version 20.10.17, build 100c701
```

Check Docker Compose version:
```bash
docker-compose --version
```
returns:
```bash
docker-compose version 1.29.2, build unknown
```

Check Python version:
```bash
python3 --version
```
returns:
```bash
Python 3.8.10
```

## Run docker 'hello-world'

In the local training environment, your student account has been added to the `docker` group to allow you to work with Docker.  You can verify this by running the Docker `hello-world` image:

```bash
docker run -it hello-world
```

This command downloads the `hello-world` image from the local registry and interactively runs a Docker container for this image.

!!! tip
    If you get an error it is often an indication that your username does not have the appropriate permissions to access the Docker filesystem.  The user running Docker commands must be added to the `docker` group in order to run Docker containers.

## Review Docker system usage

Inspect your local Docker system usage using the command:

```bash
docker system df
```

!!! question
    What usage can you currently observe for your Docker system?

Cleanup your Docker system with the command:

```bash
docker system prune -a
```

Verify Docker system is now clean of any Docker resources:
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

Please download the exercise materials to your local VM and extract the archive with the following commands:

```bash
wget https://wmo-im.github.io/wis2box-training/exercise-materials.zip
unzip exercise-materials.zip
```

Inspect the contents of the `exercise-materials` directory; these are the materials used as part of the training and practical sessions.

```bash
cd exercise-materials
ls
```


Return to your previous directory:

```bash
cd ..
```

## Conclusion

!!! success "Congratulations!"
    In this practical session, you learned how to:

    - access your student VM over SSH
    - verify the versions of Python, Docker and Docker Compose on your local student VM
    - verify that Docker commands can be successfully run
    - check Docker system resource usage
    - download, extract and review the exercise materials for this training on your local student VM

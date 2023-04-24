---
title: Accessing your student VM
---

# Accessing your student VM

## Introduction

In this session you will ensure you can connect to your student VM, check pre-installed software and download the exercise materials.

As part of locally run wis2box training sessions, you can access your personal student VM on the local training network named "WIS2-training".

If you want to run this training outside of a local training session, you can provide your own instance using any Cloud Provider:

- GCP (Google Cloud Platform) VM instance `e2-medium`
- AWS (Amazon Web Services)  ec2-instance `t3a.medium` 
- Azure (Microsoft) Azure Virtual Machine `standard_b2s`

Select Ubuntu Server 20.0.4 LTS as OS and run the setup script available in [student-vm-setup.zip](https://training.wis2box.wis.wmo.int/student-vm-setup.zip) on your instance to ensure you have all required software.

If you are using the student VM provided during local WIS2 training sessions, the required software will already be installed.

!!! note

    The student-VMs provided during WIS2 local training sessions have the following command-line editors pre-installed:

    - vi
    - vim
    - nano
    - emacs

## Connect to your student VM on the local training network

Use the following configuration to connect your PC on the local WiFi broadcasted in the room during WIS2 training:

- **SSID: WIS2-training**
- **password: dataismagic!**

Use an SSH client to connect to your student VM using the following:

- **Host: country-lastname.wis2.training** (replace with your country and your last name)
- **Port: 22**
- **Username: lastname** (replace with your last name)
- **Password: wis2training**

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

To be able to run wis2box, the student VM comes with Python Docker and Docker Compose pre-installed. 

Check docker version:
```bash
docker --version
```
returns:
```console
Docker version 20.10.17, build 100c701
```

Check Docker Compose version:
```bash
docker-compose --version
```
returns:
```console
docker-compose version 1.29.2, build unknown
```

Check Python version:
```bash
python3 --version
```
returns:
```console
Python 3.8.10
```
To be able to practice conversion to BUFR, the student VM also comes with ecCodes, synop2bufr and csv2bufr pre-installed:

Check the ecCodes version via the `bufr_dump` command:

```bash
bufr_dump -V
```
returns:
```console

ecCodes Version 2.28.0


```


Check synop2bufr version:
```bash
synop2bufr --version
```
returns:
```console
synop2bufr, version 0.3.2
```

Check csv2bufr version:
```bash
csv2bufr --version
```
returns:
```console
csv2bufr, version 0.5.1
```

## Test Docker

In the local training environment, your student account has been added to the `docker` group to allow you to work with Docker. It is important to verify Docker is working correctly before installing wis2box.

### Docker hello-world

You can verify Docker is working correctly on your system by running `hello-world` image:

```bash
docker run -it hello-world
```

This command downloads the `hello-world` image from the local registry and interactively runs a Docker container for this image.

!!! tip
    If you get an error it is often an indication that your username does not have the appropriate permissions to access the Docker filesystem.  The user running Docker commands must be added to the `docker` group in order to run Docker containers.

### Review Docker system usage

Inspect your local Docker system usage using the command:

```bash
docker system df
```

!!! question
    What usage can you currently observe for your Docker system?

Check the current images available on your Docker system:

```bash
docker image ls
```

Cleanup your Docker system with the command:

```bash
docker system prune -a
```

Verify Docker system is now clean of any Docker resources:
```bash
docker system df
```

should return:
```console
TYPE            TOTAL     ACTIVE    SIZE      RECLAIMABLE
Images          0         0         0B        0B
Containers      0         0         0B        0B
Local Volumes   0         0         0B        0B
Build Cache     0         0         0B        0
```

## Download the exercise materials

Please download the exercise materials to your home directory of your local VM and extract the archive with the following commands:

!!! warning
    Make sure you are on your home directory before downloading the exercise materials.
    Execute `cd ~/` to enter your home directory.

```bash
wget https://training.wis2box.wis.wmo.int/exercise-materials.zip
unzip exercise-materials.zip
```

Inspect the contents of the `exercise-materials` directory; these are the materials used as part of the training and practical sessions.

```bash
cd exercise-materials
ls
```

To access the material on your local machine rather than from the command line, you can use SCP. Using WinSCP, you can create a new SCP connection to your VM as follows:

<img alt="winscp-student-vm-scp.png" src="../../assets/img/winscp-student-vm-scp.png" width="400">

And you should be able to access the exercise-materials:

<img alt="winscp-student-vm-exercise-materials.png" src="../../assets/img/winscp-student-vm-exercise-materials.png" width="500">


## Conclusion

!!! success "Congratulations!"
    In this practical session, you learned how to:

    - access your student VM over SSH
    - verify the required software for the practical exercises is installed
    - verify that Docker commands can be successfully run
    - check Docker system resource usage
    - download, extract and review the exercise materials for this training on your local student VM

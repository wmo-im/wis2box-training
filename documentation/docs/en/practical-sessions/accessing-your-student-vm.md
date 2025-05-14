---
title: Accessing your student VM
---

# Accessing your student VM

!!! abstract "Learning outcomes"

    By the end of this practical session, you will be able to:

    - access your student VM over SSH and WinSCP
    - verify the required software for the practical exercises is installed
    - verify you have access to exercise materials for this training on your local student VM

## Introduction

As part of locally run wis2box training sessions, you can access your personal student VM on the local training network named "WIS2-training".

Your student VM has the following software pre-installed:

- Ubuntu 22.04 LTS [ubuntu-22.04.5-live-server-amd64.iso](https://releases.ubuntu.com/jammy/ubuntu-22.04.5-live-server-amd64.iso)
- Python 3.10.12
- Docker 24.0.6
- Docker Compose 2.21.0
- Text editors: vim, nano

!!! note

    If you want to run this training outside of a local training session, you can provide your own instance using any cloud provider, for example:

    - GCP (Google Cloud Platform) VM instance `e2-medium`
    - AWS (Amazon Web Services)  ec2-instance `t3a.medium` 
    - Azure (Microsoft) Azure Virtual Machine `standard_b2s`

    Select Ubuntu Server 22.0.4 LTS as OS.
    
    After creating your VM ensure you have installed python, docker and docker compose, as described at [wis2box-software-dependencies](https://docs.wis2box.wis.wmo.int/en/latest/user/getting-started.html#software-dependencies).
    
    The release archive for wis2box used in this training can be downloaded as follows:

    ```bash
    wget https://github.com/World-Meteorological-Organization/wis2box-release/releases/download/1.0.0/wis2box-setup.zip
    unzip wis2box-setup.zip
    ```
    
    You can always find the latest 'wis2box-setup' archive at [https://github.com/World-Meteorological-Organization/wis2box/releases](https://github.com/World-Meteorological-Organization/wis2box-release/releases).

    The exercise material used in this training can be downloaded as follows:

    ```bash
    wget https://training.wis2box.wis.wmo.int/exercise-materials.zip
    unzip exercise-materials.zip
    ```

    The following additional Python packages are required to run the exercise materials:

    ```bash
    pip3 install minio
    pip3 install pywiscat==0.2.2
    ```

    If you are using the student VM provided during local WIS2 training sessions, the required software will already be installed.

## Connect to your student VM on the local training network

Connect your PC on the local Wi-Fi broadcasted in the room during WIS2 training as per the instructions provided by the trainer.

Use an SSH client to connect to your student VM using the following:

- **Host: (provided during in-person training)**
- **Port: 22**
- **Username: (provided during in-person training)**
- **Password: (provided during in-person training)**

!!! tip
    Contact a trainer if you are unsure about the hostname/username or have issues connecting.

Once connected, please change your password to ensure others cannot access your VM:

```bash
limper@student-vm:~$ passwd
Changing password for testuser.
Current password:
New password:
Retype new password:
passwd: password updated successfully
```

## Verify software versions

To be able to run wis2box, the student VM should have Python, Docker and Docker Compose pre-installed. 

Check Python version:
```bash
python3 --version
```
returns:
```console
Python 3.10.12
```

Check docker version:
```bash
docker --version
```
returns:
```console
Docker version 24.0.6, build ed223bc
```

Check Docker Compose version:
```bash
docker compose version
```
returns:
```console
Docker Compose version v2.21.0
```

To ensure your user can run Docker commands your user has been added to the `docker` group. 

To test that your user can run docker hello-world, run the following command:
```bash
docker run hello-world
```

This should pull the hello-world image and run a container that prints a message. 

Check that you see the following in the output:

```console
...
Hello from Docker!
This message shows that your installation appears to be working correctly.
...
```

## Inspect the exercise materials

Inspect the contents of your home directory; these are the materials used as part of the training and practical sessions.

```bash
ls ~/
```
returns:
```console
exercise-materials  wis2box
```

If you have WinSCP installed on your local PC, you can use it to connect to your student VM and inspect the contents of your home directory and download or upload files between your VM and your local PC. 

WinSCP is not required for the training, but it can be useful if you want to edit files on your VM using a text editor on your local PC.

Here is how you can connect to your student VM using WinSCP:

Open WinSCP and click on the "New Site". You can create a new SCP connection to your VM as follows:

<img alt="winscp-student-vm-scp.png" src="/../assets/img/winscp-student-vm-scp.png" width="400">

Click 'Save' and then 'Login' to connect to your VM.

And you should be able to see the following content:

<img alt="winscp-student-vm-exercise-materials.png" src="/../assets/img/winscp-student-vm-exercise-materials.png" width="600">

## Conclusion

!!! success "Congratulations!"
    In this practical session, you learned how to:

    - access your student VM over SSH and WinSCP
    - verify the required software for the practical exercises is installed
    - verify you have access to exercise materials for this training on your local student VM

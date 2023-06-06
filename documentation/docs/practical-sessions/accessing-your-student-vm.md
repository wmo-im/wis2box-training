---
title: Accessing your student VM
---

# Accessing your student VM

## Introduction

As part of locally run wis2box training sessions, you can access your personal student VM on the local training network named "WIS2-training".

!!! note

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

- **Host: (provided during in-person training)**
- **Port: 22**
- **Username: (provided during in-person training)**
- **Password: wis2training** (default password to be changed after logging in)

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

To be able to practice conversion to BUFR, the student VM comes with ecCodes, synop2bufr and csv2bufr pre-installed:

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
synop2bufr, version 0.4.0
```

Check csv2bufr version:
```bash
csv2bufr --version
```
returns:
```console
csv2bufr, version 0.6.2
```

To be able to run wis2box, the student VM also comes with Python Docker and Docker Compose pre-installed. 

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
docker-compose version 1.29.0, build unknown
```

Check Python version:
```bash
python3 --version
```
returns:
```console
Python 3.8.10
```

## Inspect the exercise materials

Inspect the contents of your home directory; these are the materials used as part of the training and practical sessions.

```bash
ls ~/
```
returns:
```console
exercise-materials  wis2box-1.0b3
```

To access the material on your local machine rather than from the command line, you can use SCP. Using WinSCP, you can create a new SCP connection to your VM as follows:

<img alt="winscp-student-vm-scp.png" src="../../assets/img/winscp-student-vm-scp.png" width="400">

And you should be able to see the following content:

<img alt="winscp-student-vm-exercise-materials.png" src="../../assets/img/winscp-student-vm-exercise-materials.png" width="600">

## Exercise 1: Editing files on your Student VM

Connect to your Student VM using WinSCP and browse into the directory: **exercise-materials/accessing-your-student-vm/**

Right-click on the file **hello_world.txt** and select **edit->internal editor**.  Edit this file by adding a message of your own and save your changes.

<img alt="winscp_internal_editor.png" src="../../assets/img/winscp_internal_editor.png" width="600">

From within your SSH-client check the content of the file ~/exercise-materials/accessing-your-student-vm/hello_world.txt ":
```bash
cat ~/exercise-materials/accessing-your-student-vm/hello_world.txt
```
And confirm you see the changes you made in the file.

During the exercises you will be asked to edit files. It's up to you if you prefer to edit files from the command-line in the SSH-client-windows (using vi/vim/nano/exams) or using WinSCP.

## Conclusion

!!! success "Congratulations!"
    In this practical session, you learned how to:

    - access your student VM over SSH and WinSCP
    - verify the required software for the practical exercises is installed
    - verify you have access to exercise materials for this training on your local student VM

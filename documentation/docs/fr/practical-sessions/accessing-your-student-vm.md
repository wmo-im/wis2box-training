---
title: Accéder à votre VM étudiante
---

# Accéder à votre VM étudiante

!!! abstract "Objectifs d'apprentissage"

    À la fin de cette session pratique, vous serez capable de :

    - accéder à votre VM étudiante via SSH et WinSCP
    - vérifier que les logiciels requis pour les exercices pratiques sont installés
    - vérifier que vous avez accès aux supports d'exercices pour cette formation sur votre VM étudiante locale

## Introduction

Dans le cadre des sessions de formation wis2box organisées localement, vous pouvez accéder à votre VM étudiante personnelle sur le réseau local de formation nommé "WIS2-training".

Votre VM étudiante dispose des logiciels suivants pré-installés :

- Ubuntu 22.0.4.3 LTS [ubuntu-22.04.3-live-server-amd64.iso](https://releases.ubuntu.com/jammy/ubuntu-22.04.3-live-server-amd64.iso)
- Python 3.10.12
- Docker 24.0.6
- Docker Compose 2.21.0
- Éditeurs de texte : vim, nano

!!! note

    Si vous souhaitez suivre cette formation en dehors d'une session locale, vous pouvez utiliser votre propre instance via n'importe quel fournisseur cloud, par exemple :

    - Instance VM GCP (Google Cloud Platform) `e2-medium`
    - Instance AWS (Amazon Web Services) ec2 `t3a.medium`
    - Machine virtuelle Azure (Microsoft) `standard_b2s`

    Sélectionnez Ubuntu Server 22.0.4 LTS comme système d'exploitation.
    
    Après avoir créé votre VM, assurez-vous d'avoir installé python, docker et docker compose, comme décrit dans [wis2box-software-dependencies](https://docs.wis2box.wis.wmo.int/en/latest/user/getting-started.html#software-dependencies).
    
    L'archive de la version wis2box utilisée dans cette formation peut être téléchargée comme suit :

    ```bash
    wget https://github.com/World-Meteorological-Organization/wis2box-release/releases/download/1.0.0/wis2box-setup.zip
    unzip wis2box-setup.zip
    ```
    
    Vous pouvez toujours trouver la dernière archive 'wis2box-setup' sur [https://github.com/World-Meteorological-Organization/wis2box/releases](https://github.com/World-Meteorological-Organization/wis2box-release/releases).

    Le matériel d'exercice utilisé dans cette formation peut être téléchargé comme suit :

    ```bash
    wget https://training.wis2box.wis.wmo.int/exercise-materials.zip
    unzip exercise-materials.zip
    ```

    Les packages Python supplémentaires suivants sont nécessaires pour exécuter les supports d'exercices :

    ```bash
    pip3 install minio
    pip3 install pywiscat==0.2.2
    ```

    Si vous utilisez la VM étudiante fournie lors des sessions de formation WIS2 locales, les logiciels requis seront déjà installés.

## Se connecter à votre VM étudiante sur le réseau local de formation

Connectez votre PC au Wi-Fi local diffusé dans la salle pendant la formation WIS2 selon les instructions fournies par le formateur.

Utilisez un client SSH pour vous connecter à votre VM étudiante en utilisant les éléments suivants :

- **Hôte : (fourni pendant la formation en présentiel)**
- **Port : 22**
- **Nom d'utilisateur : (fourni pendant la formation en présentiel)**
- **Mot de passe : (fourni pendant la formation en présentiel)**

!!! tip
    Contactez un formateur si vous n'êtes pas sûr du nom d'hôte/nom d'utilisateur ou si vous avez des problèmes de connexion.

Une fois connecté, veuillez changer votre mot de passe pour empêcher l'accès à d'autres personnes :

```bash
limper@student-vm:~$ passwd
Changing password for testuser.
Current password:
New password:
Retype new password:
passwd: password updated successfully
```

## Vérifier les versions des logiciels

Pour pouvoir exécuter wis2box, la VM étudiante doit avoir Python, Docker et Docker Compose pré-installés.

Vérifier la version de Python :
```bash
python3 --version
```
retourne :
```console
Python 3.10.12
```

Vérifier la version de docker :
```bash
docker --version
```
retourne :
```console
Docker version 24.0.6, build ed223bc
```

Vérifier la version de Docker Compose :
```bash
docker compose version
```
retourne :
```console
Docker Compose version v2.21.0
```

Pour vous assurer que votre utilisateur peut exécuter les commandes Docker, votre utilisateur a été ajouté au groupe `docker`.

Pour tester que votre utilisateur peut exécuter docker hello-world, lancez la commande suivante :
```bash
docker run hello-world
```

Cela devrait télécharger l'image hello-world et exécuter un conteneur qui affiche un message.

Vérifiez que vous voyez ce qui suit dans la sortie :

```console
...
Hello from Docker!
This message shows that your installation appears to be working correctly.
...
```

## Examiner les supports d'exercices

Examinez le contenu de votre répertoire personnel ; ce sont les supports utilisés dans le cadre de la formation et des sessions pratiques.

```bash
ls ~/
```
retourne :
```console
exercise-materials  wis2box
```

Si vous avez WinSCP installé sur votre PC local, vous pouvez l'utiliser pour vous connecter à votre VM étudiante et examiner le contenu de votre répertoire personnel et télécharger ou transférer des fichiers entre votre VM et votre PC local.

WinSCP n'est pas requis pour la formation, mais il peut être utile si vous souhaitez éditer des fichiers sur votre VM en utilisant un éditeur de texte sur votre PC local.

Voici comment vous pouvez vous connecter à votre VM étudiante en utilisant WinSCP :

Ouvrez WinSCP et cliquez sur "Nouveau site". Vous pouvez créer une nouvelle connexion SCP vers votre VM comme suit :

<img alt="winscp-student-vm-scp.png" src="../../assets/img/winscp-student-vm-scp.png" width="400">

Cliquez sur 'Enregistrer' puis sur 'Connexion' pour vous connecter à votre VM.

Et vous devriez pouvoir voir le contenu suivant :

<img alt="winscp-student-vm-exercise-materials.png" src="../../assets/img/winscp-student-vm-exercise-materials.png" width="600">

## Conclusion

!!! success "Félicitations !"
    Dans cette session pratique, vous avez appris à :

    - accéder à votre VM étudiante via SSH et WinSCP
    - vérifier que les logiciels requis pour les exercices pratiques sont installés
    - vérifier que vous avez accès aux supports d'exercices pour cette formation sur votre VM étudiante locale
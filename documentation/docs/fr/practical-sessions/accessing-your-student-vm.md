---
title: Accéder à votre VM étudiant
---

# Accéder à votre VM étudiant

!!! abstract "Objectifs d'apprentissage"

    À la fin de cette session pratique, vous serez capable de :

    - accéder à votre VM étudiant via SSH et WinSCP
    - vérifier que les logiciels requis pour les exercices pratiques sont installés
    - vérifier que vous avez accès aux supports d'exercice pour cette formation sur votre VM étudiant locale

## Introduction

Dans le cadre des ateliers de formation WIS2 organisés localement, vous pouvez accéder à votre VM étudiant personnelle sur le réseau de formation local nommé "WIS2-training".

Votre VM étudiant dispose des logiciels suivants préinstallés :

- Ubuntu 22.04 LTS [ubuntu-22.04.5-live-server-amd64.iso](https://releases.ubuntu.com/jammy/ubuntu-22.04.5-live-server-amd64.iso)
- Python 3.10.12
- Docker 24.0.6
- Docker Compose 2.21.0
- Éditeurs de texte : vim, nano

!!! note

    Si vous souhaitez suivre cette formation en dehors d'une session de formation locale, vous pouvez fournir votre propre instance en utilisant n'importe quel fournisseur de cloud, par exemple :

    - GCP (Google Cloud Platform) instance VM `e2-medium`
    - AWS (Amazon Web Services) instance ec2 `t3a.medium` 
    - Azure (Microsoft) Azure Virtual Machine `standard_b2s`

    Sélectionnez Ubuntu Server 22.0.4 LTS comme système d'exploitation.
    
    Après avoir créé votre VM, assurez-vous d'avoir installé python, docker et docker compose, comme décrit dans [wis2box-software-dependencies](https://docs.wis2box.wis.wmo.int/en/latest/user/getting-started.html#software-dependencies).
    
    L'archive de la version de wis2box utilisée dans cette formation peut être téléchargée comme suit :

    ```bash
    wget https://github.com/World-Meteorological-Organization/wis2box-release/releases/download/1.1.0/wis2box-setup-1.1.0.zip
    unzip wis2box-setup-1.1.0.zip
    ```
    
    Vous pouvez toujours trouver la dernière archive 'wis2box-setup' à [https://github.com/World-Meteorological-Organization/wis2box/releases](https://github.com/World-Meteorological-Organization/wis2box-release/releases).

    Les supports d'exercice utilisés dans cette formation peuvent être téléchargés comme suit :

    ```bash
    wget https://training.wis2box.wis.wmo.int/exercise-materials.zip
    unzip exercise-materials.zip
    ```

    Les packages Python supplémentaires suivants sont nécessaires pour exécuter les supports d'exercice :

    ```bash
    pip3 install minio
    pip3 install pywiscat==0.2.2
    ```

    Si vous utilisez la VM étudiant fournie lors des sessions de formation WIS2 locales, les logiciels requis seront déjà installés.

## Se connecter à votre VM étudiant sur le réseau de formation local

Connectez votre PC au Wi-Fi local diffusé dans la salle pendant la formation WIS2, conformément aux instructions fournies par le formateur.

Utilisez un client SSH pour vous connecter à votre VM étudiant en utilisant les informations suivantes :

- **Hôte : (fourni pendant la formation en présentiel)**
- **Port : 22**
- **Nom d'utilisateur : (fourni pendant la formation en présentiel)**
- **Mot de passe : (fourni pendant la formation en présentiel)**

!!! tip
    Contactez un formateur si vous n'êtes pas sûr du nom d'hôte/nom d'utilisateur ou si vous rencontrez des problèmes de connexion.

Une fois connecté, veuillez changer votre mot de passe pour empêcher d'autres personnes d'accéder à votre VM :

```bash
limper@student-vm:~$ passwd
Changing password for testuser.
Current password:
New password:
Retype new password:
passwd: password updated successfully
```

## Vérifier les versions des logiciels

Pour pouvoir exécuter wis2box, la VM étudiant doit avoir Python, Docker et Docker Compose préinstallés. 

Vérifiez la version de Python :
```bash
python3 --version
```
renvoie :
```console
Python 3.10.12
```

Vérifiez la version de Docker :
```bash
docker --version
```
renvoie :
```console
Docker version 24.0.6, build ed223bc
```

Vérifiez la version de Docker Compose :
```bash
docker compose version
```
renvoie :
```console
Docker Compose version v2.21.0
```

Pour vous assurer que votre utilisateur peut exécuter des commandes Docker, votre utilisateur a été ajouté au groupe `docker`. 

Pour tester que votre utilisateur peut exécuter docker hello-world, exécutez la commande suivante :
```bash
docker run hello-world
```

Cela devrait télécharger l'image hello-world et exécuter un conteneur qui imprime un message. 

Vérifiez que vous voyez le message suivant dans la sortie :

```console
...
Hello from Docker!
This message shows that your installation appears to be working correctly.
...
```

## Inspecter les supports d'exercice

Inspectez le contenu de votre répertoire personnel ; ce sont les supports utilisés dans le cadre de la formation et des sessions pratiques.

```bash
ls ~/
```
renvoie :
```console
exercise-materials  wis2box
```

Si vous avez installé WinSCP sur votre PC local, vous pouvez l'utiliser pour vous connecter à votre VM étudiant et inspecter le contenu de votre répertoire personnel, ainsi que pour télécharger ou téléverser des fichiers entre votre VM et votre PC local. 

WinSCP n'est pas requis pour la formation, mais il peut être utile si vous souhaitez modifier des fichiers sur votre VM à l'aide d'un éditeur de texte sur votre PC local.

Voici comment vous connecter à votre VM étudiant en utilisant WinSCP :

Ouvrez WinSCP et cliquez sur "New Site". Vous pouvez créer une nouvelle connexion SCP à votre VM comme suit :

<img alt="winscp-student-vm-scp.png" src="/../assets/img/winscp-student-vm-scp.png" width="400">

Cliquez sur 'Save', puis sur 'Login' pour vous connecter à votre VM.

Vous devriez alors voir le contenu suivant :

<img alt="winscp-student-vm-exercise-materials.png" src="/../assets/img/winscp-student-vm-exercise-materials.png" width="600">

## Conclusion

!!! success "Félicitations !"
    Lors de cette session pratique, vous avez appris à :

    - accéder à votre VM étudiant via SSH et WinSCP
    - vérifier que les logiciels requis pour les exercices pratiques sont installés
    - vérifier que vous avez accès aux supports d'exercice pour cette formation sur votre VM étudiant locale
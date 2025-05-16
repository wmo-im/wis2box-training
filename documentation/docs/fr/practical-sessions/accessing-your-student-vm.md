---
title: Accéder à votre VM étudiant
---

# Accéder à votre VM étudiant

!!! abstract "Résultats d'apprentissage"

    À la fin de cette session pratique, vous serez capable de :

    - accéder à votre VM étudiant via SSH et WinSCP
    - vérifier que le logiciel nécessaire pour les exercices pratiques est installé
    - vérifier que vous avez accès aux matériaux d'exercice pour cette formation sur votre VM étudiant local

## Introduction

Dans le cadre des sessions de formation wis2box organisées localement, vous pouvez accéder à votre VM étudiant personnel sur le réseau de formation local nommé "WIS2-training".

Votre VM étudiant a le logiciel suivant préinstallé :

- Ubuntu 22.0.4.3 LTS [ubuntu-22.04.3-live-server-amd64.iso](https://releases.ubuntu.com/jammy/ubuntu-22.04.3-live-server-amd64.iso)
- Python 3.10.12
- Docker 24.0.6
- Docker Compose 2.21.0
- Éditeurs de texte : vim, nano

!!! note

    Si vous souhaitez suivre cette formation en dehors d'une session de formation locale, vous pouvez fournir votre propre instance en utilisant n'importe quel fournisseur de cloud, par exemple :

    - Instance VM GCP (Google Cloud Platform) `e2-medium`
    - Instance ec2 AWS (Amazon Web Services) `t3a.medium`
    - Machine virtuelle Azure (Microsoft) `standard_b2s`

    Sélectionnez Ubuntu Server 22.0.4 LTS comme système d'exploitation.
    
    Après avoir créé votre VM, assurez-vous d'avoir installé python, docker et docker compose, comme décrit à [wis2box-software-dependencies](https://docs.wis2box.wis.wmo.int/en/latest/user/getting-started.html#software-dependencies).
    
    L'archive de la version de wis2box utilisée dans cette formation peut être téléchargée comme suit :

    ```bash
    wget https://github.com/World-Meteorological-Organization/wis2box-release/releases/download/1.0.0/wis2box-setup.zip
    unzip wis2box-setup.zip
    ```
    
    Vous pouvez toujours trouver la dernière archive 'wis2box-setup' à [https://github.com/World-Meteorological-Organization/wis2box/releases](https://github.com/World-Meteorological-Organization/wis2box-release/releases).

    Le matériel d'exercice utilisé dans cette formation peut être téléchargé comme suit :

    ```bash
    wget https://training.wis2box.wis.wmo.int/exercise-materials.zip
    unzip exercise-materials.zip
    ```

    Les packages Python supplémentaires suivants sont nécessaires pour exécuter les matériaux d'exercice :

    ```bash
    pip3 install minio
    pip3 install pywiscat==0.2.2
    ```

    Si vous utilisez la VM étudiant fournie lors des sessions de formation WIS2 locales, le logiciel requis sera déjà installé.

## Connectez-vous à votre VM étudiant sur le réseau de formation local

Connectez votre PC au Wi-Fi local diffusé dans la salle pendant la formation WIS2 selon les instructions fournies par le formateur.

Utilisez un client SSH pour vous connecter à votre VM étudiant en utilisant les informations suivantes :

- **Hôte : (fourni pendant la formation en personne)**
- **Port : 22**
- **Nom d'utilisateur : (fourni pendant la formation en personne)**
- **Mot de passe : (fourni pendant la formation en personne)**

!!! tip
    Contactez un formateur si vous avez des doutes sur le nom d'hôte/le nom d'utilisateur ou si vous rencontrez des problèmes de connexion.

Une fois connecté, veuillez changer votre mot de passe pour garantir que d'autres ne puissent pas accéder à votre VM :

```bash
limper@student-vm:~$ passwd
Changing password for testuser.
Current password:
New password:
Retype new password:
passwd: password updated successfully
```

## Vérifiez les versions des logiciels

Pour pouvoir exécuter wis2box, la VM étudiant doit avoir Python, Docker et Docker Compose préinstallés. 

Vérifiez la version de Python :
```bash
python3 --version
```
retourne :
```console
Python 3.10.12
```

Vérifiez la version de docker :
```bash
docker --version
```
retourne :
```console
Docker version 24.0.6, build ed223bc
```

Vérifiez la version de Docker Compose :
```bash
docker compose version
```
retourne :
```console
Docker Compose version v2.21.0
```

Pour vous assurer que votre utilisateur peut exécuter des commandes Docker, votre utilisateur a été ajouté au groupe `docker`. 

Pour tester que votre utilisateur peut exécuter docker hello-world, exécutez la commande suivante :
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

## Inspectez les matériaux d'exercice

Inspectez le contenu de votre répertoire personnel ; ce sont les matériaux utilisés dans le cadre de la formation et des sessions pratiques.

```bash
ls ~/
```
retourne :
```console
exercise-materials  wis2box
```

Si vous avez WinSCP installé sur votre PC local, vous pouvez l'utiliser pour vous connecter à votre VM étudiant et inspecter le contenu de votre répertoire personnel et télécharger ou téléverser des fichiers entre votre VM et votre PC local. 

WinSCP n'est pas requis pour la formation, mais il peut être utile si vous souhaitez éditer des fichiers sur votre VM à l'aide d'un éditeur de texte sur votre PC local.

Voici comment vous pouvez vous connecter à votre VM étudiant en utilisant WinSCP :

Ouvrez WinSCP et cliquez sur "Nouveau site". Vous pouvez créer une nouvelle connexion SCP à votre VM comme suit :

<img alt="winscp-student-vm-scp.png" src="/../assets/img/winscp-student-vm-scp.png" width="400">

Cliquez sur 'Enregistrer' puis sur 'Connexion' pour vous connecter à votre VM.

Et vous devriez pouvoir voir le contenu suivant :

<img alt="winscp-student-vm-exercise-materials.png" src="/../assets/img/winscp-student-vm-exercise-materials.png" width="600">

## Conclusion

!!! success "Félicitations !"
    Dans cette session pratique, vous avez appris à :

    - accéder à votre VM étudiant via SSH et WinSCP
    - vérifier que le logiciel nécessaire pour les exercices pratiques est installé
    - vérifier que vous avez accès aux matériaux d'exercice pour cette formation sur votre VM étudiant local
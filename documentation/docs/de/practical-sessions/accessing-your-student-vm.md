---
title: Zugriff auf Ihre Studenten-VM
---

# Zugriff auf Ihre Studenten-VM

!!! abstract "Lernergebnisse"

    Am Ende dieser praktischen Sitzung werden Sie in der Lage sein:

    - Zugriff auf Ihre Studenten-VM über SSH und WinSCP
    - Überprüfung der erforderlichen Software für die praktischen Übungen
    - Überprüfung des Zugriffs auf Übungsmaterialien für dieses Training auf Ihrer lokalen Studenten-VM

## Einführung

Im Rahmen von lokal durchgeführten wis2box-Schulungen können Sie auf Ihre persönliche Studenten-VM im lokalen Schulungsnetzwerk namens "WIS2-training" zugreifen.

Ihre Studenten-VM hat die folgende Software vorinstalliert:

- Ubuntu 22.0.4.3 LTS [ubuntu-22.04.3-live-server-amd64.iso](https://releases.ubuntu.com/jammy/ubuntu-22.04.3-live-server-amd64.iso)
- Python 3.10.12
- Docker 24.0.6
- Docker Compose 2.21.0
- Texteditoren: vim, nano

!!! note

    Wenn Sie dieses Training außerhalb einer lokalen Schulungssitzung durchführen möchten, können Sie Ihre eigene Instanz über einen beliebigen Cloud-Anbieter bereitstellen, zum Beispiel:

    - GCP (Google Cloud Platform) VM-Instanz `e2-medium`
    - AWS (Amazon Web Services) ec2-Instanz `t3a.medium`
    - Azure (Microsoft) Azure Virtual Machine `standard_b2s`

    Wählen Sie Ubuntu Server 22.0.4 LTS als Betriebssystem.
    
    Nachdem Sie Ihre VM erstellt haben, stellen Sie sicher, dass Python, Docker und Docker Compose installiert sind, wie unter [wis2box-software-dependencies](https://docs.wis2box.wis.wmo.int/en/latest/user/getting-started.html#software-dependencies) beschrieben.
    
    Das Release-Archiv für wis2box, das in diesem Training verwendet wird, kann wie folgt heruntergeladen werden:

    ```bash
    wget https://github.com/World-Meteorological-Organization/wis2box-release/releases/download/1.0.0/wis2box-setup.zip
    unzip wis2box-setup.zip
    ```
    
    Das neueste 'wis2box-setup'-Archiv finden Sie immer unter [https://github.com/World-Meteorological-Organization/wis2box/releases](https://github.com/World-Meteorological-Organization/wis2box-release/releases).

    Das Übungsmaterial, das in diesem Training verwendet wird, kann wie folgt heruntergeladen werden:

    ```bash
    wget https://training.wis2box.wis.wmo.int/exercise-materials.zip
    unzip exercise-materials.zip
    ```

    Die folgenden zusätzlichen Python-Pakete sind erforderlich, um die Übungsmaterialien auszuführen:

    ```bash
    pip3 install minio
    pip3 install pywiscat==0.2.2
    ```

    Wenn Sie die Studenten-VM verwenden, die während der lokalen WIS2-Schulungen bereitgestellt wird, ist die erforderliche Software bereits installiert.

## Verbinden Sie sich mit Ihrer Studenten-VM im lokalen Schulungsnetzwerk

Verbinden Sie Ihren PC mit dem lokalen WLAN, das während der WIS2-Schulung im Raum ausgestrahlt wird, gemäß den Anweisungen des Trainers.

Verwenden Sie einen SSH-Client, um sich mit Ihrer Studenten-VM zu verbinden, indem Sie folgende Daten verwenden:

- **Host: (während der Präsenzschulung bereitgestellt)**
- **Port: 22**
- **Benutzername: (während der Präsenzschulung bereitgestellt)**
- **Passwort: (während der Präsenzschulung bereitgestellt)**

!!! tip
    Kontaktieren Sie einen Trainer, wenn Sie sich bezüglich des Hostnamens/Benutzernamens unsicher sind oder Probleme beim Verbinden haben.

Sobald Sie verbunden sind, ändern Sie bitte Ihr Passwort, um sicherzustellen, dass andere keinen Zugriff auf Ihre VM haben:

```bash
limper@student-vm:~$ passwd
Passwort ändern für testuser.
Aktuelles Passwort:
Neues Passwort:
Neues Passwort wiederholen:
passwd: Passwort erfolgreich aktualisiert
```

## Überprüfen Sie die Softwareversionen

Um wis2box ausführen zu können, sollten Python, Docker und Docker Compose auf der Studenten-VM vorinstalliert sein.

Überprüfen Sie die Python-Version:
```bash
python3 --version
```
gibt zurück:
```console
Python 3.10.12
```

Überprüfen Sie die Docker-Version:
```bash
docker --version
```
gibt zurück:
```console
Docker version 24.0.6, build ed223bc
```

Überprüfen Sie die Docker Compose-Version:
```bash
docker compose version
```
gibt zurück:
```console
Docker Compose version v2.21.0
```

Um sicherzustellen, dass Ihr Benutzer Docker-Befehle ausführen kann, wurde Ihr Benutzer zur `docker`-Gruppe hinzugefügt.

Um zu testen, dass Ihr Benutzer docker hello-world ausführen kann, führen Sie den folgenden Befehl aus:
```bash
docker run hello-world
```

Dies sollte das hello-world-Image herunterladen und einen Container ausführen, der eine Nachricht ausgibt.

Überprüfen Sie, ob Sie Folgendes in der Ausgabe sehen:

```console
...
Hello from Docker!
This message shows that your installation appears to be working correctly.
...
```

## Überprüfen Sie die Übungsmaterialien

Überprüfen Sie den Inhalt Ihres Home-Verzeichnisses; dies sind die Materialien, die als Teil des Trainings und der praktischen Sitzungen verwendet werden.

```bash
ls ~/
```
gibt zurück:
```console
exercise-materials  wis2box
```

Wenn Sie WinSCP auf Ihrem lokalen PC installiert haben, können Sie es verwenden, um sich mit Ihrer Studenten-VM zu verbinden und den Inhalt Ihres Home-Verzeichnisses zu inspizieren sowie Dateien zwischen Ihrer VM und Ihrem lokalen PC herunterzuladen oder hochzuladen.

WinSCP ist nicht erforderlich für das Training, kann jedoch nützlich sein, wenn Sie Dateien auf Ihrer VM mit einem Texteditor auf Ihrem lokalen PC bearbeiten möchten.

So können Sie sich mit WinSCP mit Ihrer Studenten-VM verbinden:

Öffnen Sie WinSCP und klicken Sie auf "Neue Seite". Sie können eine neue SCP-Verbindung zu Ihrer VM wie folgt erstellen:

<img alt="winscp-student-vm-scp.png" src="../../assets/img/winscp-student-vm-scp.png" width="400">

Klicken Sie auf 'Speichern' und dann auf 'Anmelden', um sich mit Ihrer VM zu verbinden.

Und Sie sollten in der Lage sein, den folgenden Inhalt zu sehen:

<img alt="winscp-student-vm-exercise-materials.png" src="../../assets/img/winscp-student-vm-exercise-materials.png" width="600">

## Schlussfolgerung

!!! success "Herzlichen Glückwunsch!"
    In dieser praktischen Sitzung haben Sie gelernt, wie Sie:

    - Zugriff auf Ihre Studenten-VM über SSH und WinSCP
    - Überprüfung der erforderlichen Software für die praktischen Übungen
    - Überprüfung des Zugriffs auf Übungsmaterialien für dieses Training auf Ihrer lokalen Studenten-VM
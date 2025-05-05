---
title: Zugriff auf Ihre Student-VM
---

# Zugriff auf Ihre Student-VM

!!! abstract "Lernziele"

    Nach Abschluss dieser praktischen Einheit werden Sie in der Lage sein:

    - auf Ihre Student-VM über SSH und WinSCP zuzugreifen
    - zu überprüfen, ob die erforderliche Software für die praktischen Übungen installiert ist
    - zu überprüfen, ob Sie Zugriff auf die Übungsmaterialien für diese Schulung auf Ihrer lokalen Student-VM haben

## Einführung

Im Rahmen lokaler wis2box-Schulungen haben Sie Zugriff auf Ihre persönliche Student-VM im lokalen Schulungsnetzwerk "WIS2-training".

Auf Ihrer Student-VM ist folgende Software vorinstalliert:

- Ubuntu 22.0.4.3 LTS [ubuntu-22.04.3-live-server-amd64.iso](https://releases.ubuntu.com/jammy/ubuntu-22.04.3-live-server-amd64.iso)
- Python 3.10.12
- Docker 24.0.6
- Docker Compose 2.21.0
- Texteditoren: vim, nano

!!! note

    Wenn Sie diese Schulung außerhalb einer lokalen Schulungseinheit durchführen möchten, können Sie Ihre eigene Instanz bei einem beliebigen Cloud-Anbieter bereitstellen, zum Beispiel:

    - GCP (Google Cloud Platform) VM-Instanz `e2-medium`
    - AWS (Amazon Web Services) ec2-Instanz `t3a.medium`
    - Azure (Microsoft) Azure Virtual Machine `standard_b2s`

    Wählen Sie Ubuntu Server 22.0.4 LTS als Betriebssystem.
    
    Stellen Sie nach der Erstellung Ihrer VM sicher, dass Sie Python, Docker und Docker Compose installiert haben, wie unter [wis2box-software-dependencies](https://docs.wis2box.wis.wmo.int/en/latest/user/getting-started.html#software-dependencies) beschrieben.
    
    Das in dieser Schulung verwendete Release-Archiv für wis2box kann wie folgt heruntergeladen werden:

    ```bash
    wget https://github.com/World-Meteorological-Organization/wis2box-release/releases/download/1.0.0/wis2box-setup.zip
    unzip wis2box-setup.zip
    ```
    
    Das aktuelle 'wis2box-setup'-Archiv finden Sie immer unter [https://github.com/World-Meteorological-Organization/wis2box/releases](https://github.com/World-Meteorological-Organization/wis2box-release/releases).

    Das in dieser Schulung verwendete Übungsmaterial kann wie folgt heruntergeladen werden:

    ```bash
    wget https://training.wis2box.wis.wmo.int/exercise-materials.zip
    unzip exercise-materials.zip
    ```

    Die folgenden zusätzlichen Python-Pakete sind erforderlich, um die Übungsmaterialien auszuführen:

    ```bash
    pip3 install minio
    pip3 install pywiscat==0.2.2
    ```

    Wenn Sie die während der lokalen WIS2-Schulungen bereitgestellte Student-VM verwenden, ist die erforderliche Software bereits installiert.

## Verbindung zu Ihrer Student-VM im lokalen Schulungsnetzwerk

Verbinden Sie Ihren PC mit dem lokalen WLAN, das während der WIS2-Schulung im Raum ausgestrahlt wird, gemäß den Anweisungen des Trainers.

Verwenden Sie einen SSH-Client, um sich mit folgenden Daten mit Ihrer Student-VM zu verbinden:

- **Host: (wird während der Präsenzschulung bereitgestellt)**
- **Port: 22**
- **Benutzername: (wird während der Präsenzschulung bereitgestellt)**
- **Passwort: (wird während der Präsenzschulung bereitgestellt)**

!!! tip
    Wenden Sie sich an einen Trainer, wenn Sie sich beim Hostnamen/Benutzernamen nicht sicher sind oder Probleme bei der Verbindung haben.

Ändern Sie nach der Verbindung Ihr Passwort, damit andere nicht auf Ihre VM zugreifen können:

```bash
limper@student-vm:~$ passwd
Changing password for testuser.
Current password:
New password:
Retype new password:
passwd: password updated successfully
```

## Überprüfen der Softwareversionen

Um wis2box ausführen zu können, sollten Python, Docker und Docker Compose auf der Student-VM vorinstalliert sein.

Python-Version überprüfen:
```bash
python3 --version
```
gibt zurück:
```console
Python 3.10.12
```

Docker-Version überprüfen:
```bash
docker --version
```
gibt zurück:
```console
Docker version 24.0.6, build ed223bc
```

Docker Compose-Version überprüfen:
```bash
docker compose version
```
gibt zurück:
```console
Docker Compose version v2.21.0
```

Damit Sie Docker-Befehle ausführen können, wurde Ihr Benutzer zur Gruppe `docker` hinzugefügt.

Um zu testen, ob Ihr Benutzer docker hello-world ausführen kann, führen Sie folgenden Befehl aus:
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

## Überprüfen der Übungsmaterialien

Überprüfen Sie den Inhalt Ihres Home-Verzeichnisses; dies sind die Materialien, die im Rahmen der Schulung und der praktischen Einheiten verwendet werden.

```bash
ls ~/
```
gibt zurück:
```console
exercise-materials  wis2box
```

Wenn Sie WinSCP auf Ihrem lokalen PC installiert haben, können Sie es verwenden, um sich mit Ihrer Student-VM zu verbinden und den Inhalt Ihres Home-Verzeichnisses zu überprüfen sowie Dateien zwischen Ihrer VM und Ihrem lokalen PC hoch- und herunterzuladen.

WinSCP ist für die Schulung nicht erforderlich, kann aber nützlich sein, wenn Sie Dateien auf Ihrer VM mit einem Texteditor auf Ihrem lokalen PC bearbeiten möchten.

So können Sie sich mit WinSCP mit Ihrer Student-VM verbinden:

Öffnen Sie WinSCP und klicken Sie auf "Neue Site". Sie können wie folgt eine neue SCP-Verbindung zu Ihrer VM erstellen:

<img alt="winscp-student-vm-scp.png" src="../../assets/img/winscp-student-vm-scp.png" width="400">

Klicken Sie auf 'Speichern' und dann auf 'Anmelden', um sich mit Ihrer VM zu verbinden.

Sie sollten dann den folgenden Inhalt sehen können:

<img alt="winscp-student-vm-exercise-materials.png" src="../../assets/img/winscp-student-vm-exercise-materials.png" width="600">

## Abschluss

!!! success "Herzlichen Glückwunsch!"
    In dieser praktischen Einheit haben Sie gelernt:

    - wie Sie auf Ihre Student-VM über SSH und WinSCP zugreifen
    - wie Sie überprüfen, ob die erforderliche Software für die praktischen Übungen installiert ist
    - wie Sie überprüfen, ob Sie Zugriff auf die Übungsmaterialien für diese Schulung auf Ihrer lokalen Student-VM haben
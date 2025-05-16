---
title: Docker Spickzettel
---

# Docker Spickzettel

## Übersicht

Docker ermöglicht das Erstellen virtueller Umgebungen auf isolierte Weise zur Unterstützung der Virtualisierung von Rechenressourcen. Das grundlegende Konzept hinter Docker ist die Containerisierung, bei der Software als Dienste ausgeführt werden kann, die mit anderen Softwarecontainern interagieren, zum Beispiel.

Der typische Docker-Workflow umfasst das Erstellen und Bauen von **Images**, die dann als laufende **Container** ausgeführt werden.

Docker wird verwendet, um die Suite von Diensten auszuführen, die wis2box mit vorab erstellten Images bilden.

### Bildverwaltung

* Liste verfügbarer Images

```bash
docker image ls
```

* Ein Image aktualisieren:

```bash
docker pull my-image:latest
```

* Ein Image entfernen:

```bash
docker rmi my-image:local
```

### Volumenverwaltung

* Liste aller erstellten Volumen:

```bash
docker volume ls
```

* Detaillierte Informationen zu einem Volumen anzeigen:

```bash
docker volume inspect my-volume
```

* Ein Volumen entfernen:

```bash
docker volume rm my-volume
```

* Alle ungenutzten Volumen entfernen:

```bash
docker volume prune
```

### Containerverwaltung

* Liste der aktuell laufenden Container anzeigen:

```bash
docker ps
```

* Liste aller Container:

```bash
docker ps -a
```

* Das interaktive Terminal eines laufenden Containers betreten:


!!! tip

    Verwenden Sie `docker ps`, um die Container-ID im folgenden Befehl zu verwenden

```bash
docker exec -it my-container /bin/bash
```

* Einen Container entfernen

```bash
docker rm my-container
```

* Einen laufenden Container entfernen:

```bash
docker rm -f my-container
```
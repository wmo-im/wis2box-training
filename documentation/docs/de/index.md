---
title: Startseite
---

<img alt="WMO logo" src="../assets/img/wmo-logo.png" width="200">
# WIS2 in a box Schulung

WIS2 in a box ([wis2box](https://docs.wis2box.wis.wmo.int)) ist eine freie und quelloffene (FOSS) Referenzimplementierung eines WMO WIS2 Node. Das Projekt bietet ein sofort einsetzbares Werkzeugset zur Aufnahme, Verarbeitung und Veröffentlichung von Wetter-/Klima-/Wasserdaten unter Verwendung standardbasierter Ansätze in Übereinstimmung mit den WIS2-Prinzipien. wis2box ermöglicht auch den Zugriff auf alle Daten im WIS2-Netzwerk. wis2box wurde entwickelt, um Datenanbietern einen niedrigschwelligen Einstieg zu ermöglichen und stellt Infrastruktur und Dienste für die Datenerkennung, den Datenzugriff und die Datenvisualisierung bereit.

Diese Schulung bietet schrittweise Erklärungen zu verschiedenen Aspekten des wis2box-Projekts sowie mehrere Übungen, die Ihnen helfen, Daten in WIS2 zu veröffentlichen und herunterzuladen. Die Schulung wird in Form von Überblickspräsentationen sowie praktischen Übungen angeboten.

Die Teilnehmer können sowohl mit Beispieldaten und -metadaten arbeiten als auch ihre eigenen Daten und Metadaten integrieren.

Diese Schulung deckt ein breites Spektrum an Themen ab (Installation/Einrichtung/Konfiguration, Veröffentlichung/Herunterladen von Daten, etc.).

## Ziele und Lernergebnisse

Die Ziele dieser Schulung sind die Vertrautheit mit folgenden Aspekten:

- Kernkonzepte und Komponenten der WIS2-Architektur
- Daten- und Metadatenformate für Auffindbarkeit und Zugriff in WIS2
- wis2box-Architektur und -Umgebung
- wis2box-Kernfunktionen:
    - Metadatenverwaltung
    - Datenaufnahme und Umwandlung in das BUFR-Format
    - MQTT-Broker für WIS2-Nachrichtenveröffentlichung
    - HTTP-Endpunkt für Datendownload
    - API-Endpunkt für programmatischen Datenzugriff

## Navigation

Die Navigation auf der linken Seite bietet ein Inhaltsverzeichnis für die gesamte Schulung.

Die Navigation auf der rechten Seite bietet ein Inhaltsverzeichnis für die jeweilige Seite.

## Voraussetzungen

### Kenntnisse

- Grundlegende Linux-Befehle (siehe [Spickzettel](cheatsheets/linux.md))
- Grundkenntnisse in Netzwerken und Internetprotokollen

### Software

Diese Schulung erfordert folgende Werkzeuge:

- Eine Instanz mit Ubuntu-Betriebssystem (wird von WMO-Trainern während lokaler Schulungen bereitgestellt), siehe [Zugriff auf Ihre Studenten-VM](practical-sessions/accessing-your-student-vm.md#introduction)
- SSH-Client für den Zugriff auf Ihre Instanz
- MQTT Explorer auf Ihrem lokalen Rechner
- SCP- und SFTP-Client zum Kopieren von Dateien von Ihrem lokalen Rechner

## Konventionen

!!! question

    Ein so markierter Abschnitt fordert Sie auf, eine Frage zu beantworten.

Außerdem werden Sie im Text Tipps und Hinweise finden:

!!! tip

    Tipps helfen Ihnen dabei, Aufgaben bestmöglich zu lösen.

!!! note

    Hinweise liefern zusätzliche Informationen zum Thema der praktischen Übung sowie Hilfestellung zur bestmöglichen Durchführung der Aufgaben.

Beispiele werden wie folgt dargestellt:

Konfiguration
``` {.yaml linenums="1"}
my-collection-defined-in-yaml:
    type: collection
    title: my title defined as a yaml attribute named title
    description: my description as a yaml attribute named description
```

Befehle, die in einem Terminal/einer Konsole eingegeben werden müssen, werden wie folgt dargestellt:

```bash
echo 'Hello world'
```

Container-Namen (laufende Images) werden in **Fettschrift** dargestellt.

## Schulungsort und Materialien

Die Schulungsinhalte, das Wiki und der Issue-Tracker werden auf GitHub unter [https://github.com/World-Meteorological-Organization/wis2box-training](https://github.com/World-Meteorological-Organization/wis2box-training) verwaltet.

## Drucken der Materialien

Diese Schulung kann als PDF exportiert werden. Um dieses Schulungsmaterial zu speichern oder zu drucken, gehen Sie zur [Druckseite](print_page) und wählen Sie Datei > Drucken > Als PDF speichern.

## Übungsmaterialien

Übungsmaterialien können aus der Datei [exercise-materials.zip](/exercise-materials.zip) heruntergeladen werden.

## Unterstützung

Für Probleme/Fehler/Vorschläge oder Verbesserungen/Beiträge zu dieser Schulung nutzen Sie bitte den [GitHub Issue Tracker](https://github.com/World-Meteorological-Organization/wis2box-training/issues).

Alle wis2box-Fehler, Verbesserungen und Probleme können auf [GitHub](https://github.com/World-Meteorological-Organization/wis2box/issues) gemeldet werden.

Für zusätzliche Unterstützung oder Fragen wenden Sie sich bitte an wis2-support@wmo.int.

Die wis2box-Kerndokumentation finden Sie jederzeit unter [https://docs.wis2box.wis.wmo.int](https://docs.wis2box.wis.wmo.int).

Beiträge sind immer willkommen und erwünscht!
---
title: Startseite
---

<img alt="WMO logo" src="assets/img/wmo-logo.png" width="200">
# WIS2 in a box Schulung

WIS2 in a box ([wis2box](https://docs.wis2box.wis.wmo.int)) ist eine freie und Open-Source (FOSS) Referenzimplementierung eines WMO WIS2-Knotens. Das Projekt bietet ein Plug-and-Play-Toolset zum Erfassen, Verarbeiten und Veröffentlichen von Wetter-/Klima-/Wasserdaten unter Verwendung von standardbasierten Ansätzen in Übereinstimmung mit den WIS2-Prinzipien. wis2box bietet auch Zugang zu allen Daten im WIS2-Netzwerk. wis2box ist so konzipiert, dass es für Datenanbieter eine niedrige Einstiegshürde bietet und Infrastruktur und Dienste zur Datenentdeckung, -zugriff und -visualisierung ermöglicht.

Diese Schulung bietet schrittweise Erklärungen zu verschiedenen Aspekten des wis2box-Projekts sowie eine Reihe von Übungen, um Ihnen zu helfen, Daten von WIS2 zu veröffentlichen und herunterzuladen. Die Schulung wird in Form von Übersichtspräsentationen sowie praktischen Übungen angeboten.

Teilnehmer werden in der Lage sein, mit Testdaten und Metadaten zu arbeiten sowie ihre eigenen Daten und Metadaten zu integrieren.

Diese Schulung deckt eine breite Palette von Themen ab (Installation/Konfiguration, Veröffentlichung/Download von Daten usw.).

## Ziele und Lernergebnisse

Die Ziele dieser Schulung sind, sich mit den folgenden Themen vertraut zu machen:

- Kernkonzepte und Komponenten der WIS2-Architektur
- Daten- und Metadatenformate, die in WIS2 für Entdeckung und Zugriff verwendet werden
- wis2box-Architektur und -Umgebung
- Kernfunktionen von wis2box:
    - Metadatenmanagement
    - Datenerfassung und -umwandlung in das BUFR-Format
    - MQTT-Broker für die Veröffentlichung von WIS2-Nachrichten
    - HTTP-Endpunkt für den Daten-Download
    - API-Endpunkt für den programmatischen Zugriff auf Daten

## Navigation

Die Navigation auf der linken Seite bietet ein Inhaltsverzeichnis für die gesamte Schulung.

Die Navigation auf der rechten Seite bietet ein Inhaltsverzeichnis für eine spezifische Seite.

## Voraussetzungen

### Wissen

- Grundlegende Linux-Befehle (siehe das [cheatsheet](./cheatsheets/linux.md))
- Grundkenntnisse über Netzwerk- und Internetprotokolle

### Software

Diese Schulung erfordert die folgenden Werkzeuge:

- Eine Instanz mit Ubuntu OS (wird von WMO-Trainern während lokaler Schulungssitzungen bereitgestellt) siehe [Zugriff auf Ihre Studenten-VM](./practical-sessions/accessing-your-student-vm.md#introduction)
- SSH-Client für den Zugriff auf Ihre Instanz
- MQTT Explorer auf Ihrem lokalen Rechner
- SCP- und SFTP-Client zum Kopieren von Dateien von Ihrem lokalen Rechner

## Konventionen

!!! question

    Ein Abschnitt, der so markiert ist, lädt Sie ein, eine Frage zu beantworten.

Außerdem werden Sie Tipps und Hinweise innerhalb des Textes bemerken:

!!! tip

    Tipps geben Hilfe, wie man Aufgaben am besten bewältigt.

!!! note

    Hinweise bieten zusätzliche Informationen zum behandelten Thema sowie dazu, wie Aufgaben am besten bewältigt werden.

Beispiele werden wie folgt angezeigt:

Konfiguration
``` {.yaml linenums="1"}
my-collection-defined-in-yaml:
    type: collection
    title: my title defined as a yaml attribute named title
    description: my description as a yaml attribute named description
```

Schnipsel, die in einem Terminal/Konsole eingegeben werden müssen, werden angezeigt als:

```bash
echo 'Hello world'
```

Container-Namen (laufende Images) sind in **Fett** gekennzeichnet.

## Schulungsort und -materialien

Die Schulungsinhalte, das Wiki und der Issue-Tracker werden auf GitHub verwaltet unter [https://github.com/World-Meteorological-Organization/wis2box-training](https://github.com/World-Meteorological-Organization/wis2box-training).

## Drucken des Materials

Diese Schulung kann als PDF exportiert werden. Um dieses Schulungsmaterial zu speichern oder zu drucken, gehen Sie zur [Druckseite](print_page) und wählen
Datei > Drucken > Als PDF speichern.

## Übungsmaterialien

Übungsmaterialien können von der [exercise-materials.zip](/exercise-materials.zip) Zip-Datei heruntergeladen werden.

## Unterstützung

Für Probleme/Bugs/Vorschläge oder Verbesserungen/Beiträge zu dieser Schulung nutzen Sie bitte den [GitHub-Issue-Tracker](https://github.com/World-Meteorological-Organization/wis2box-training/issues).

Alle wis2box-Bugs, Verbesserungen und Probleme können auf [GitHub](https://github.com/World-Meteorological-Organization/wis2box/issues) gemeldet werden.

Für zusätzliche Unterstützung oder Fragen kontaktieren Sie bitte wis2-support@wmo.int.

Wie immer kann die Kern-Dokumentation von wis2box immer unter [https://docs.wis2box.wis.wmo.int](https://docs.wis2box.wis.wmo.int) gefunden werden.

Beiträge sind immer ermutigt und willkommen!
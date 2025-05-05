---
title: Umwandlung von SYNOP-Daten in BUFR
---

# Umwandlung von SYNOP-Daten in BUFR mit der wis2box-Webapp

!!! abstract "Lernergebnisse"
    Am Ende dieser praktischen Sitzung werden Sie in der Lage sein:

    - gültige FM-12 SYNOP-Bulletins über die wis2box-Webanwendung zur Umwandlung in BUFR und zum Austausch über das WIS2.0 einzureichen
    - einfache Kodierungsfehler in einem FM-12 SYNOP-Bulletin vor der Formatumwandlung und dem Austausch zu validieren, zu diagnostizieren und zu beheben
    - sicherzustellen, dass die erforderlichen Stationsmetadaten in der wis2box verfügbar sind
    - erfolgreich umgewandelte Bulletins zu bestätigen und zu inspizieren

## Einführung

Um es manuellen Beobachtern zu ermöglichen, Daten direkt an das WIS2.0 zu übermitteln, verfügt die wis2box-Webapp über ein Formular zur Umwandlung von FM-12 SYNOP-Bulletins in BUFR. Das Formular ermöglicht es den Benutzern auch, einfache Kodierungsfehler im FM-12 SYNOP-Bulletin vor der Formatumwandlung und dem Austausch zu diagnostizieren und zu beheben sowie die resultierenden BUFR-Daten zu inspizieren.

## Vorbereitung

!!! warning "Voraussetzungen"

    - Stellen Sie sicher, dass Ihre wis2box konfiguriert und gestartet wurde.
    - Öffnen Sie ein Terminal und verbinden Sie sich über SSH mit Ihrer Studenten-VM.
    - Verbinden Sie sich mit dem MQTT-Broker Ihrer wis2box-Instanz mit MQTT Explorer.
    - Öffnen Sie die wis2box-Webanwendung (``http://<Ihr-Host-Name>/wis2box-webapp``) und stellen Sie sicher, dass Sie eingeloggt sind.

## Verwendung der wis2box-Webapp zur Umwandlung von FM-12 SYNOP in BUFR

### Übung 1 - Verwendung der wis2box-Webapp zur Umwandlung von FM-12 SYNOP in BUFR

Stellen Sie sicher, dass Sie das Auth-Token für "processes/wis2box" haben, das Sie in der vorherigen Übung generiert haben, und dass Sie mit Ihrem wis2box-Broker im MQTT Explorer verbunden sind.

Kopieren Sie die folgende Nachricht:
    
``` {.copy}
AAXX 27031
15015 02999 02501 10103 21090 39765 42952 57020 60001=
``` 

Öffnen Sie die wis2box-Webanwendung und navigieren Sie zur Seite synop2bufr über die linke Navigationsleiste und gehen Sie wie folgt vor:

- Fügen Sie den kopierten Inhalt in das Texteingabefeld ein.
- Wählen Sie den Monat und das Jahr mit dem Datumsauswahlwerkzeug aus, gehen Sie für diese Übung vom aktuellen Monat aus.
- Wählen Sie ein Thema aus dem Dropdown-Menü (die Optionen basieren auf den in der wis2box konfigurierten Datensätzen).
- Geben Sie das "processes/wis2box" Auth-Token ein, das Sie zuvor generiert haben.
- Stellen Sie sicher, dass "Publish on WIS2" eingeschaltet ist.
- Klicken Sie auf "SUBMIT"

<center><img alt="Dialog zeigt die synop2bufr-Seite, einschließlich Umschaltknopf" src="../../assets/img/synop2bufr-toggle.png"></center>

Klicken Sie auf submit. Sie erhalten eine Warnmeldung, da die Station nicht in der wis2box registriert ist. Gehen Sie zum Station-Editor und importieren Sie die folgende Station:

``` {.copy}
0-20000-0-15015
```

Stellen Sie sicher, dass die Station mit dem Thema verbunden ist, das Sie im vorherigen Schritt ausgewählt haben, und kehren Sie dann zur Seite synop2bufr zurück und wiederholen Sie den Vorgang mit denselben Daten wie zuvor.

!!! question
    Wie können Sie das Ergebnis der Umwandlung von FM-12 SYNOP in BUFR sehen?

??? success "Klicken Sie, um die Antwort zu enthüllen"
    Der Ergebnisbereich der Seite zeigt Warnungen, Fehler und ausgegebene BUFR-Dateien.

    Klicken Sie auf "Output BUFR files", um eine Liste der generierten Dateien zu sehen. Es sollte eine Datei aufgelistet sein.

    Der Download-Button ermöglicht es, die BUFR-Daten direkt auf Ihren Computer herunterzuladen.

    Der Inspektionsbutton führt einen Prozess aus, um die Daten aus BUFR zu konvertieren und zu extrahieren.

    <center><img alt="Dialog zeigt das Ergebnis der erfolgreich übermittelten Nachricht"
         src="../../assets/img/synop2bufr-ex2-success.png"></center>

!!! question
    Die FM-12 SYNOP-Eingabedaten enthielten keine Angaben zum Standort der Station, zur Höhe oder zur Barometerhöhe.
    Bestätigen Sie, dass diese im ausgegebenen BUFR-Daten vorhanden sind, woher kommen diese?

??? success "Klicken Sie, um die Antwort zu enthüllen"
    Ein Klick auf den Inspektionsbutton sollte einen Dialog wie den unten gezeigten öffnen.

    <center><img alt="Ergebnisse des Inspektionsbuttons, die die grundlegenden Stationsmetadaten, den Standort der Station und die beobachteten Eigenschaften zeigen"
         src="../../assets/img/synop2bufr-ex2.png"></center>

    Dies schließt den Standort der Station, der auf einer Karte angezeigt wird, und grundlegende Metadaten sowie die Beobachtungen in der Nachricht ein.
    
    Als Teil der Umwandlung von FM-12 SYNOP in BUFR wurden zusätzliche Metadaten zur BUFR-Datei hinzugefügt.
    
    Die BUFR-Datei kann auch durch Herunterladen der Datei und Validierung mit einem Tool wie dem ECMWF ecCodes BUFR-Validator inspiziert werden.

Gehen Sie zu MQTT Explorer und überprüfen Sie das WIS2-Benachrichtigungsthema, um die veröffentlichten WIS2-Benachrichtigungen zu sehen.

### Übung 2 - Verständnis der Stationsliste

In dieser nächsten Übung werden Sie eine Datei mit mehreren Berichten konvertieren, siehe die Daten unten:

``` {.copy}
AAXX 27031
15015 02999 02501 10103 21090 39765 42952 57020 60001=
15020 02997 23104 10130 21075 30177 40377 58020 60001 81041=
15090 02997 53102 10139 21075 30271 40364 58031 60001 82046=
```

!!! question
    Basierend auf der vorherigen Übung, betrachten Sie die FM-12 SYNOP-Nachricht und sagen Sie voraus, wie viele Ausgabe-BUFR-Nachrichten generiert werden.
    
    Kopieren Sie nun diese Nachricht in das SYNOP-Formular und übermitteln Sie die Daten.

    Entsprach die Anzahl der generierten Nachrichten Ihren Erwartungen und wenn nicht, warum nicht?

??? warning "Klicken Sie, um die Antwort zu enthüllen"
    
    Sie hätten vielleicht erwartet, dass drei BUFR-Nachrichten generiert werden, eine für jeden Wetterbericht. Stattdessen haben Sie jedoch 2 Warnungen erhalten und nur eine BUFR-Datei.
    
    Damit ein Wetterbericht in BUFR umgewandelt werden kann, sind die grundlegenden Metadaten, die in der Stationsliste enthalten sind, erforderlich. Während das obige Beispiel drei Wetterberichte enthält, waren zwei der drei berichtenden Stationen nicht in Ihrer wis2box registriert.
    
    Infolgedessen führte nur einer der drei Wetterberichte zu einer generierten BUFR-Datei und einer veröffentlichten WIS2-Benachrichtigung. Die anderen zwei Wetterberichte wurden ignoriert und Warnungen wurden generiert.

!!! hint
    Beachten Sie die Beziehung zwischen dem WIGOS-Identifier und dem traditionellen Stationsidentifier, der in der BUFR-Ausgabe enthalten ist. In vielen Fällen, für Stationen, die zum Zeitpunkt der Migration zu WIGOS-Stationenidentifiern in WMO-No. 9 Volume A aufgeführt sind, wird der WIGOS-Stationenidentifier durch Voranstellen von ``0-20000-0`` zum traditionellen Stationsidentifier gegeben, z. B. ist ``15015`` zu ``0-20000-0-15015`` geworden.

Verwenden Sie die Stationslistenseite, um die folgenden Stationen zu importieren:

``` {.copy}
0-20000-0-15020
0-20000-0-15090
```

Stellen Sie sicher, dass die Stationen mit dem Thema verbunden sind, das Sie in der vorherigen Übung ausgewählt haben, und kehren Sie dann zur Seite synop2bufr zurück und wiederholen Sie den Vorgang.

Es sollten nun drei BUFR-Dateien generiert werden, und es sollten keine Warnungen oder Fehler in der Webanwendung aufgeführt sein.

Zusätzlich zu den grundlegenden Stationsinformationen sind zusätzliche Metadaten wie die Höhe der Station über dem Meeresspiegel und die Höhe des Barometers über dem Meeresspiegel für die Kodierung zu BUFR erforderlich. Die Felder sind in den Seiten Stationsliste und Stationseditor enthalten.
    
### Übung 3 - Debugging

In dieser letzten Übung werden Sie zwei der häufigsten Probleme identifizieren und korrigieren, die beim Einsatz dieses Tools zur Umwandlung von FM-12 SYNOP in BUFR auftreten.

Beispiel Daten sind unten im Kasten gezeigt, untersuchen Sie die Daten und versuchen Sie, eventuelle Probleme zu lösen, bevor Sie die Daten über die Webanwendung einreichen.

!!! hint
    Sie können die Daten im Eingabefeld auf der Seite der Webanwendung bearbeiten. Wenn Sie irgendwelche Probleme übersehen, sollten diese als Warnung oder Fehler hervorgehoben werden, sobald der Submit-Button geklickt wurde.

``` {.copy}
AAXX 27031
15015 02999 02501 10103 21090 39765 42952 57020 60001
15020 02997 23104 10130 21075 30177 40377 58020 60001 81041=
15090 02997 53102 10139 21075 30271 40364 58031 60001 82046=
```

!!! question
    Welche Probleme haben Sie erwartet, beim Umwandeln der Daten in BUFR zu begegnen, und wie haben Sie diese überwunden? Gab es Probleme, die Sie nicht erwartet hatten?

??? success "Klicken Sie, um die Antwort zu enthüllen"
    Im ersten Beispiel fehlt das "Ende des Textes"-Symbol (=) oder der Datensatzbegrenzer zwischen dem ersten und zweiten Wetterbericht. Folglich werden die Zeilen 2 und 3 als ein einziger Bericht behandelt, was zu Fehlern bei der Interpretation der Nachricht führt.

Das zweite Beispiel unten enthält mehrere häufige Probleme, die in FM-12 SYNOP-Berichten gefunden werden. Untersuchen Sie die Daten und versuchen Sie, die Probleme zu identifizieren, und reichen Sie dann die korrigierten Daten über die Webanwendung ein.

```{.copy}
AAXX 27031
15020 02997 23104 10/30 21075 30177 40377 580200 60001 81041=
```

!!! question
    Welche Probleme haben Sie gefunden und wie haben Sie diese gelöst?

??? success "Klicken Sie, um die Antwort zu enthüllen"
    Es gibt zwei Probleme im Wetterbericht.
    
    Das erste, in der Gruppe der signierten Lufttemperatur, hat den Zehnercharakter auf fehlend (/) gesetzt, was zu einer ungültigen Gruppe führt. In diesem Beispiel wissen wir, dass die Temperatur 13,0 Grad Celsius beträgt (aus den obigen Beispielen), und daher kann dieses Problem korrigiert werden. Betrieblich müsste der korrekte Wert mit dem Beobachter bestätigt werden.

    Das zweite Problem tritt in Gruppe 5 auf, wo ein zusätzlicher Charakter vorhanden ist, mit dem letzten Charakter dupliziert. Dieses Problem kann behoben werden, indem der zusätzliche Charakter entfernt wird.

## Hausarbeit

Während der Übungen in dieser Sitzung haben Sie mehrere Dateien in Ihre Stationsliste importiert. Navigieren Sie zur Stationslistenseite und klicken Sie auf die Mülleimer-Symbole, um die Stationen zu löschen. Möglicherweise müssen Sie die Seite aktualisieren, um die Stationen aus der Liste zu entfernen, nachdem sie gelöscht wurden.

<center><img alt="Stationsmetadaten-Viewer"
         src="../../assets/img/synop2bufr-trash.png" width="600"></center>

## Schlussfolgerung

!!! success "Herzlichen Glückwunsch!"

    In dieser praktischen Sitzung haben Sie gelernt:

    - wie das synop2bufr-Tool verwendet werden kann, um FM-12 SYNOP-Berichte in BUFR zu konvertieren;
    - wie ein FM-12 SYNOP-Bericht über die Web-App eingereicht wird;
    - wie einfache Fehler in einem FM-12 SYNOP-Bericht diagnostiziert und korrigiert werden;
    - die Bedeutung der Registrierung von Stationen in der wis2box (und OSCAR/Surface);
    - und die Verwendung des Inspektionsbuttons, um den Inhalt von BUFR-Daten anzusehen.
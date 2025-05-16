---
title: Arbeiten mit BUFR-Daten
---

# Arbeiten mit BUFR-Daten

!!! abstract "Lernergebnisse"
    In dieser praktischen Sitzung werden Sie in einige der BUFR-Tools eingeführt, die im **wis2box-api** Container enthalten sind und die verwendet werden, um Daten in das BUFR-Format zu transformieren und den in BUFR kodierten Inhalt zu lesen.
    
    Sie werden lernen:

    - wie man die Header in der BUFR-Datei mit dem Befehl `bufr_ls` inspiziert
    - wie man die Daten in einer BUFR-Datei mit `bufr_dump` extrahiert und inspiziert
    - die grundlegende Struktur der BUFR-Vorlagen, die in csv2bufr verwendet werden, und wie man das Kommandozeilenwerkzeug verwendet
    - und wie man grundlegende Änderungen an den BUFR-Vorlagen vornimmt und wie man die wis2box aktualisiert, um die überarbeitete Version zu verwenden

## Einführung

Die Plugins, die Benachrichtigungen mit BUFR-Daten erzeugen, verwenden Prozesse in der wis2box-api, um mit BUFR-Daten zu arbeiten, zum Beispiel um die Daten von CSV in BUFR oder von BUFR in geojson zu transformieren.

Der wis2box-api Container enthält eine Reihe von Tools zur Arbeit mit BUFR-Daten.

Dazu gehören die von ECMWF entwickelten Tools, die in der ecCodes-Software enthalten sind. Weitere Informationen dazu finden Sie auf der [ecCodes-Website](https://confluence.ecmwf.int/display/ECC/BUFR+tools).

In dieser Sitzung werden Sie in die `bufr_ls` und `bufr_dump` aus dem ecCodes-Softwarepaket und die erweiterte Konfiguration des csv2bufr-Tools eingeführt.

## Vorbereitung

Um die BUFR-Kommandozeilenwerkzeuge verwenden zu können, müssen Sie im wis2box-api Container angemeldet sein, und sofern nicht anders angegeben, sollten alle Befehle in diesem Container ausgeführt werden. Sie müssen auch MQTT Explorer geöffnet und mit Ihrem Broker verbunden haben.

Verbinden Sie sich zuerst über Ihren SSH-Client mit Ihrer Studenten-VM und dann melden Sie sich im wis2box-api Container an:

```{.copy}
cd ~/wis2box-1.0.0rc1
python3 wis2box-ctl.py login wis2box-api
```

Bestätigen Sie, dass die Tools verfügbar sind, beginnend mit ecCodes:

``` {.copy}
bufr_dump -V
```
Sie sollten die folgende Antwort erhalten:

```
ecCodes Version 2.28.0
```

Überprüfen Sie als nächstes csv2bufr:

```{.copy}
csv2bufr --version
```

Sie sollten die folgende Antwort erhalten:

```
csv2bufr, Version 0.7.4
```

Erstellen Sie schließlich ein Arbeitsverzeichnis, in dem Sie arbeiten können:

```{.copy}
cd /data/wis2box
mkdir -p working/bufr-cli
cd working/bufr-cli
```

Sie sind jetzt bereit, die BUFR-Tools zu verwenden.

## Verwendung der BUFR-Kommandozeilenwerkzeuge

### Übung 1 - bufr_ls
In dieser ersten Übung verwenden Sie den Befehl `bufr_ls`, um die Header einer BUFR-Datei zu inspizieren und den Inhalt der Datei zu bestimmen. Die folgenden Header sind in einer BUFR-Datei enthalten:

| header                            | ecCodes-Schlüssel                  | Beschreibung                                                                                                                                           |
|-----------------------------------|------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------|
| Ursprungs-/Erzeugungszentrum     | centre                       | Das Ursprungs-/Erzeugungszentrum für die Daten                                                                                                      |
| Ursprungs-/Erzeugungsunterzentrum | bufrHeaderSubCentre          | Das Ursprungs-/Erzeugungsunterzentrum für die Daten                                                                                                  | 
| Aktualisierungssequenznummer            | updateSequenceNumber         | Ob dies die erste Version der Daten (0) oder ein Update (>0) ist                                                                                   |               
| Datenkategorie                     | dataCategory                 | Der Typ der Daten, die in der BUFR-Nachricht enthalten sind, z. B. Oberflächendaten. Siehe [BUFR Tabelle A](https://github.com/wmo-im/BUFR4/blob/master/BUFR_TableA_en.csv)  |
| Internationale Datenunterkategorie   | internationalDataSubCategory | Der Untertyp der Daten, die in der BUFR-Nachricht enthalten sind, z. B. Oberflächendaten. Siehe [Gemeinsame Code-Tabelle C-13](https://github.com/wmo-im/CCT/blob/master/C13.csv) |
| Jahr                              | typicalYear (typicalDate)    | Typischste Zeit für den Inhalt der BUFR-Nachricht                                                                                                       |
| Monat                             | typicalMonth (typicalDate)   | Typischste Zeit für den Inhalt der BUFR-Nachricht                                                                                                       |
| Tag                               | typicalDay (typicalDate)     | Typischste Zeit für den Inhalt der BUFR-Nachricht                                                                                                       |
| Stunde                              | typicalHour (typicalTime)    | Typischste Zeit für den Inhalt der BUFR-Nachricht                                                                                                       |
| Minute                            | typicalMinute (typicalTime)  | Typischste Zeit für den Inhalt der BUFR-Nachricht                                                                                                       |
| BUFR-Deskriptoren                  | unexpandedDescriptors        | Liste von einem oder mehreren BUFR-Deskriptoren, die die in der Datei enthaltenen Daten definieren                                                                        |

Laden Sie die Beispieldatei direkt in den wis2box-Management-Container mit dem folgenden Befehl herunter:

``` {.copy}
curl https://training.wis2box.wis.wmo.int/sample-data/bufr-cli-ex1.bufr4 --output bufr-cli-ex1.bufr4
```

Verwenden Sie nun den folgenden Befehl, um `bufr_ls` auf diese Datei auszuführen:

```bash
bufr_ls bufr-cli-ex1.bufr4
```

Sie sollten die folgende Ausgabe sehen:

```bash
bufr-cli-ex1.bufr4
centre                     masterTablesVersionNumber  localTablesVersionNumber   typicalDate                typicalTime                numberOfSubsets
cnmc                       29                         0                          20231002                   000000                     1
1 von 1 Nachrichten in bufr-cli-ex1.bufr4

1 von 1 Gesamtnachrichten in 1 Dateien
```

Für sich allein sind diese Informationen nicht sehr informativ, da nur begrenzte Informationen über den Dateiinhalt bereitgestellt werden.

Die Standardausgabe liefert keine Informationen über den Beobachtungs- oder Datentyp und ist in einem Format, das nicht sehr leicht zu lesen ist. Es können jedoch verschiedene Optionen an `bufr_ls` übergeben werden, um sowohl das Format als auch die gedruckten Headerfelder zu ändern.

Verwenden Sie `bufr_ls` ohne Argumente, um die Optionen anzuzeigen:

```{.copy}
bufr_ls
```

Sie sollten die folgende Ausgabe sehen:

```
NAME    bufr_ls

BESCHREIBUNG
        Listet den Inhalt von BUFR-Dateien auf, indem Werte einiger Header-Schlüssel gedruckt werden.
        Es können nur skalare Schlüssel gedruckt werden.
        Es wird nicht fehlschlagen, wenn ein Schlüssel nicht gefunden wird.

VERWENDUNG
        bufr_ls [Optionen] bufr_datei bufr_datei ...

OPTIONEN
        -p Schlüssel[:{s|d|i}],Schlüssel[:{s|d|i}],...
                Deklaration von Schlüsseln zum Drucken.
                Für jeden Schlüssel kann ein String (Schlüssel:s), ein Double (Schlüssel:d) oder ein Integer (Schlüssel:i)
                Typ angefordert werden. Standardtyp ist String.
        -F Format
                C-Stil-Format für Gleitkommawerte.
        -P Schlüssel[:{s|d|i}],Schlüssel[:{s|d|i}],...
                Wie -p, fügt die deklarierten Schlüssel zur Standardliste hinzu.
        -w Schlüssel[:{s|d|i}]{=|!=}Wert,Schlüssel[:{s|d|i}]{=|!=}Wert,...
                Where-Klausel.
                Nachrichten werden nur verarbeitet, wenn sie allen Schlüssel/Wert-Beschränkungen entsprechen.
                Eine gültige Beschränkung ist vom Typ Schlüssel=Wert oder Schlüssel!=Wert.
                Für jeden Schlüssel kann ein String (Schlüssel:s), ein Double (Schlüssel:d) oder ein Integer (Schlüssel:i)
                Typ angegeben werden. Standardtyp ist String.
                Im Wert können Sie auch das Schrägstrichzeichen '/' verwenden, um eine ODER-Bedingung anzugeben (d. h. eine logische Disjunktion)
                Hinweis: Nur eine -w-Klausel ist erlaubt.
        -j      JSON-Ausgabe
        -s Schlüssel[:{s|d|i}]=Wert,Schlüssel[:{s|d|i}]=Wert,...
                Schlüssel/Werte festlegen.
                Für jeden Schlüssel kann ein String (Schlüssel:s), ein Double (Schlüssel:d) oder ein Integer (Schlüssel:i)
                Typ definiert werden. Standardmäßig wird der native Typ festgelegt.
        -n Namensraum
                Alle Schlüssel, die zum angegebenen Namensraum gehören, werden gedruckt.
        -m      Mars-Schlüssel werden gedruckt.
        -V      Version.
        -W Breite
                Mindestbreite jeder Spalte in der Ausgabe. Standard ist 10.
        -g      Kopiert GTS-Header.
        -7      Fehlschlägt nicht, wenn die Nachricht falsche Länge hat

SIEHE AUCH
        Vollständige Dokumentation und Beispiele unter:
        <https://confluence.ecmwf.int/display/ECC/bufr_ls>
```

Führen Sie nun denselben Befehl auf der Beispieldatei aus, geben Sie jedoch die Informationen im JSON-Format aus.

!!! Frage
    Welchen Flag geben Sie dem `bufr_ls`-Befehl, um die Ausgabe im JSON-Format anzuzeigen?

??? Erfolg "Klicken Sie, um die Antwort zu enthüllen"
    Sie können das Ausgabeformat in json ändern, indem Sie den `-j`-Flag verwenden, d. h.
    `bufr_ls -j <Eingabedatei>`. Dies kann lesbarer sein als das Standardausgabeformat. Siehe das Beispiel unten:

    ```
    { "Nachrichten" : [
      {
        "Zentrum": "cnmc",
        "masterTablesVersionNumber": 29,
        "localTablesVersionNumber": 0,
        "typicalDate": 20231002,
        "typicalTime": "000000",
        "numberOfSubsets": 1
      }
    ]}
    ```

Beim Untersuchen einer BUFR-Datei möchten wir oft den Typ der in der Datei enthaltenen Daten und das typische Datum/die typische Zeit der Daten bestimmen. Diese Informationen können mit dem `-p`-Flag aufgelistet werden, um die Header auszugeben. Mehrere Header können mit einer durch Kommas getrennten Liste einbezogen werden.

Verwenden Sie den `bufr_ls`-Befehl, um die Testdatei zu inspizieren und den Typ der darin enthaltenen Daten sowie das typische Datum und die typische Zeit für diese Daten zu identifizieren.

??? Hinweis
    Die ecCodes-Schlüssel sind in der obigen Tabelle angegeben. Wir können die folgenden verwenden, um die dataCategory und
    internationalDataSubCategory der BUFR-Daten aufzulisten:

    ```
    bufr_ls -p dataCategory,internationalDataSubCategory bufr-cli-ex1.bufr4
    ```

    Weitere Schlüssel können bei Bedarf hinzugefügt werden.

!!! Frage
    Welcher Datentyp (Datenkategorie und Unterkategorie) ist in der Datei enthalten? Was ist das typische Datum und die typische Zeit
    für die Daten?

??? Erfolg "Klicken Sie, um die Antwort zu enthüllen"
    Der Befehl, den Sie ausführen müssen, sollte ähnlich gewesen sein:
    
    ```
    bufr_ls -p dataCategory,internationalDataSubCategory,typicalDate,typicalTime -j bufr-cli-ex1.bufr4
    ```

    Möglicherweise haben Sie zusätzliche Schlüssel hinzugefügt oder das Jahr, den Monat, den Tag usw. einzeln aufgelistet. Die Ausgabe sollte
    ähnlich sein wie unten, abhängig davon, ob Sie JSON oder die Standardausgabe ausgewählt haben.

    ```
    { "Nachrichten" : [
      {
        "dataCategory": 2,
        "internationalDataSubCategory": 4,
        "typicalDate": 20231002,
        "typicalTime": "000000"
      }
    ]}
    ```

    Daraus sehen wir, dass:

    - Die Datenkategorie 2 ist, aus [BUFR Tabelle A](https://github.com/wmo-im/BUFR4/blob/master/BUFR_TableA_en.csv)
      sehen wir, dass diese Datei Daten zu "Vertikalen Sondierungen (außer Satellit)" enthält.
    - Die internationale Unterkategorie ist 4, was
      "Obere Temperatur-/Feuchtigkeits-/Windberichte von festen Landstationen (TEMP)" Daten anzeigt. Diese Informationen können nachgeschlagen werden
      in [Gemeinsame Code-Tabelle C-13](https://github.com/wmo-im/CCT/blob/master/C13.csv) (Zeile 33). Beachten Sie die Kombination
      von Kategorie und Unterkategorie.
    - Das typische Datum und die typische Zeit sind 2023/10/02 und 00:00:00z bzw.

    

### Übung 2 - bufr_dump

Der Befehl `bufr_dump` kann verwendet werden, um den Inhalt einer BUFR-Datei aufzulisten und zu untersuchen, einschließlich der Daten selbst.

In dieser Übung verwenden wir eine BUFR-Datei, die dieselbe ist wie die, die Sie während der anfänglichen csv2bufr-Praxissitzung mit der wis2box-Webapp erstellt haben.

Laden Sie die Beispieldatei direkt in den wis2box-Management-Container mit dem folgenden Befehl herunter:

``` {.copy}
curl https://training.wis2box.wis.wmo.int/sample-data/bufr-cli-ex2.bufr4 --output bufr-cli-ex2.bufr4
```

Führen Sie nun den Befehl `bufr_dump` auf der Datei aus und verwenden Sie den `-p`-Flag, um die Daten im Klartextformat (Schlüssel=Wert-Format) auszugeben:

```{.copy}
bufr_dump -p bufr-cli-ex2.bufr4
```

Sie sollten etwa 240 Schlüssel sehen, von denen viele fehlen. Dies ist typisch für reale Daten, da nicht alle eccodes-Schlüssel mit gemeldeten Daten gefüllt sind.

!!! Hinweis
    Die fehlenden Werte können mit Tools wie `grep` gefiltert werden:
    ```{.copy}
    bufr_dump -p bufr-cli-ex2.bufr4 | grep -v MISSING
    ```

Die Beispiel-BUFR-Datei für diese Übung stammt aus der csv2bufr-Praxissitzung. Bitte laden Sie die ursprüngliche CSV-Datei an Ihren aktuellen Standort wie folgt herunter:

```{.copy}
curl https://training.wis2box.wis.wmo.int/sample-data/csv2bufr-ex1.csv --output csv2bufr-ex1.csv
```

Und zeigen Sie den Inhalt der Datei mit an:

```{.copy}
more csv2bufr-ex1.csv
```

!!! Frage
    Verwenden Sie den folgenden Befehl, um die Spalte 18 in der CSV-Datei anzuzeigen, und Sie finden den gemeldeten mittleren Meeresspiegeldruck (msl_pressure):

    ```{.copy}
    more csv2bufr-ex1.csv | cut -d ',' -f 18
    ```
    
    Welchem Schlüssel in der BUFR-Ausgabe entspricht der mittlere Meeresspiegeldruck?

??? Hinweis
    Tools wie `grep` können in Kombination mit `bufr_dump` verwendet werden. Zum Beispiel:
    
    ```{.copy}
    bufr_dump -p bufr-cli-ex2.bufr4 | grep -i "pressure"
    ```
    
    würde den Inhalt von `bufr_dump` filtern, sodass nur die Zeilen angezeigt werden, die das Wort Druck enthalten. Alternativ könnte
    die Ausgabe auf einen Wert gefiltert werden.

??? Erfolg "Klicken Sie, um die Antwort zu enthüllen"
    Der Schlüssel "pressureReducedToMeanSeaLevel" entspricht der Spalte msl_pressure in der Eingabe-CSV-Datei.

Verbringen Sie einige Minuten damit, den Rest der Ausgabe zu untersuchen und mit der Eingabe-CSV-Datei zu vergleichen, bevor Sie zur nächsten
Übung übergehen. Zum Beispiel können Sie versuchen, die Schlüssel in der BUFR-Ausgabe zu finden, die der relativen Luftfeuchtigkeit (Spalte 23 in der CSV-Datei) und der Lufttemperatur (Spalte 21 in der
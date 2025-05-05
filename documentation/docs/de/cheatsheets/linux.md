---
title: Linux Spickzettel
---

# Linux Spickzettel

## Übersicht

Die grundlegenden Konzepte der Arbeit in einem Linux-Betriebssystem sind **Dateien** und **Verzeichnisse** (Ordner), die in einer Baumstruktur innerhalb einer **Umgebung** organisiert sind.

Sobald Sie sich in ein Linux-System einloggen, arbeiten Sie in einer **Shell**, in der Sie Dateien und Verzeichnisse bearbeiten können, indem Sie Befehle ausführen, die auf dem System installiert sind. Die Bash-Shell ist eine häufige und beliebte Shell, die typischerweise auf Linux-Systemen zu finden ist.

## Bash

### Verzeichnisnavigation

* Betreten eines absoluten Verzeichnisses:

```bash
cd /dir1/dir2
```

* Betreten eines relativen Verzeichnisses:

```bash
cd ./somedir
```

* Ein Verzeichnis nach oben wechseln:

```bash
cd ..
```

* Zwei Verzeichnisse nach oben wechseln:

```bash
cd ../..
```

* Zum "home"-Verzeichnis wechseln:

```bash
cd -
```

### Dateiverwaltung

* Auflisten der Dateien im aktuellen Verzeichnis:

```bash
ls
```

* Detailliertes Auflisten der Dateien im aktuellen Verzeichnis:

```bash
ls -l
```

* Auflisten der Wurzel des Dateisystems:

```bash
ls -l /
```

* Eine leere Datei erstellen:

```bash
touch foo.txt
```

* Eine Datei aus einem `echo`-Befehl erstellen:

```bash
echo "hi there" > test-file.txt
```

* Den Inhalt einer Datei anzeigen:

```bash
cat test-file.txt
```

* Eine Datei kopieren:

```bash
cp file1 file2
```

* Platzhalter: Operieren auf Dateimustern:

```bash
ls -l fil*  # passt zu file1 und file2
```

* Zwei Dateien in eine neue Datei namens `newfile` zusammenführen:

```bash
cat file1 file2 > newfile
```

* Eine weitere Datei an `newfile` anhängen

```bash
cat file3 >> newfile
```

* Eine Datei löschen:

```bash
rm newfile
```

* Alle Dateien mit derselben Dateierweiterung löschen:

```bash
rm *.dat
```

* Ein Verzeichnis erstellen

```bash
mkdir dir1
```

### Befehle mit Pipes verketten

Pipes erlauben es einem Benutzer, die Ausgabe eines Befehls an einen anderen zu senden, indem das Pipe-Symbol `|` verwendet wird:

```bash
echo "hi" | sed 's/hi/bye/'
```

* Filtern von Befehlsausgaben mit grep:

```bash
echo "id,title" > test-file.txt
echo "1,birds" >> test-file.txt
echo "2,fish" >> test-file.txt
echo "3,cats" >> test-file.txt

cat test-file.txt | grep fish
```

* Groß- und Kleinschreibung ignorieren:

```bash
grep -i FISH test-file.txt
```

* Zählen von passenden Zeilen:

```bash
grep -c fish test-file.txt
```

* Ausgaben zurückgeben, die das Schlüsselwort nicht enthalten:

```bash
grep -v birds test-file.txt
```

* Zählen der Zeilen in `test-file.txt`:

```bash
wc -l test-file.txt
```

* Ausgabe seitenweise anzeigen:

```bash
more test-file.txt
```

...mit Steuerungen:

- Zeile für Zeile nach unten scrollen: *Enter*
- Zur nächsten Seite gehen: *Leertaste*
- Eine Seite zurückgehen: *b*

* Die ersten 3 Zeilen der Datei anzeigen:

```bash
head -3 test-file.txt
```

* Die letzten 2 Zeilen der Datei anzeigen:

```bash
tail -2 test-file.txt
```

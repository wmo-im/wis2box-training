---
title: Linux cheatsheet
---

# Linux cheatsheet

## Panoramica

I concetti di base del lavoro in un sistema operativo Linux sono **file** e **directory** (cartelle) organizzati in
una struttura ad albero all'interno di un **ambiente**.

Una volta effettuato l'accesso a un sistema Linux, si lavora in una **shell** in cui è possibile gestire file e directory,
eseguendo comandi installati sul sistema. La shell Bash è una shell comune e popolare che
si trova tipicamente sui sistemi Linux.

## Bash

### Navigazione nelle directory

* Accedere a una directory assoluta:

```bash
cd /dir1/dir2
```

* Accedere a una directory relativa:

```bash
cd ./somedir
```

* Spostarsi su di una directory:

```bash
cd ..
```

* Spostarsi su due directory:

```bash
cd ../..
```

* Tornare alla propria directory "home":

```bash
cd -
```

### Gestione dei file

* Elenca i file nella directory corrente:

```bash
ls
```

* Elenca i file nella directory corrente con maggiori dettagli:

```bash
ls -l
```

* Elenca la radice del filesystem:

```bash
ls -l /
```

* Crea un file vuoto:

```bash
touch foo.txt
```

* Crea un file dal comando `echo`:

```bash
echo "ciao" > test-file.txt
```

* Visualizza il contenuto di un file:

```bash
cat test-file.txt
```

* Copia un file:

```bash
cp file1 file2
```

* Jolly: operare su modelli di file:

```bash
ls -l fil*  # corrisponde a file1 e file2
```

* Concatena due file in un nuovo file chiamato `newfile`:

```bash
cat file1 file2 > newfile
```

* Aggiungi un altro file a `newfile`:

```bash
cat file3 >> newfile
```

* Elimina un file:

```bash
rm newfile
```

* Elimina tutti i file con la stessa estensione:

```bash
rm *.dat
```

* Crea una directory:

```bash
mkdir dir1
```

### Concatenazione di comandi con le pipe

Le pipe permettono di inviare l'output di un comando a un altro utilizzando il simbolo della pipe `|`:

```bash
echo "ciao" | sed 's/ciao/addio/'
```

* Filtrare gli output dei comandi usando grep:

```bash
echo "id,titolo" > test-file.txt
echo "1,uccelli" >> test-file.txt
echo "2,pesci" >> test-file.txt
echo "3,gatti" >> test-file.txt

cat test-file.txt | grep pesci
```

* Ignorare il maiuscolo/minuscolo:

```bash
grep -i PESCI test-file.txt
```

* Contare le righe corrispondenti:

```bash
grep -c pesci test-file.txt
```

* Restituire output che non contengono la parola chiave:

```bash
grep -v uccelli test-file.txt
```

* Contare il numero di righe in `test-file.txt`:

```bash
wc -l test-file.txt
```

* Visualizzare l'output una schermata alla volta:

```bash
more test-file.txt
```

...con controlli:

- Scorri verso il basso riga per riga: *invio*
- Vai alla pagina successiva: *barra spaziatrice*
- Torna indietro di una pagina: *b*

* Visualizza le prime 3 righe del file:

```bash
head -3 test-file.txt
```

* Visualizza le ultime 2 righe del file:

```bash
tail -2 test-file.txt
```

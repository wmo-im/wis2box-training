---
title: Linux cheatsheet
---

# Linux cheatsheet

## Vue d'ensemble

Les concepts de base pour travailler dans un système d'exploitation Linux sont les **fichiers** et les **répertoires** (dossiers) organisés dans une structure arborescente au sein d'un **environnement**.

Une fois connecté à un système Linux, vous travaillez dans un **shell** où vous pouvez manipuler des fichiers et des répertoires en exécutant des commandes installées sur le système. Le shell Bash est un shell courant et populaire qui se trouve généralement sur les systèmes Linux.

## Bash

### Navigation dans les répertoires

* Entrer dans un répertoire absolu :

```bash
cd /dir1/dir2
```

* Entrer dans un répertoire relatif :

```bash
cd ./somedir
```

* Monter d'un répertoire :

```bash
cd ..
```

* Monter de deux répertoires :

```bash
cd ../..
```

* Aller à votre répertoire "home" :

```bash
cd -
```

### Gestion des fichiers

* Lister les fichiers dans le répertoire courant :

```bash
ls
```

* Lister les fichiers dans le répertoire courant avec plus de détails :

```bash
ls -l
```

* Lister la racine du système de fichiers :

```bash
ls -l /
```

* Créer un fichier vide :

```bash
touch foo.txt
```

* Créer un fichier à partir d'une commande `echo` :

```bash
echo "hi there" > test-file.txt
```

* Voir le contenu d'un fichier :

```bash
cat test-file.txt
```

* Copier un fichier :

```bash
cp file1 file2
```

* Jokers : opérer sur des motifs de fichiers :

```bash
ls -l fil*  # correspond à file1 et file2
```

* Concaténer deux fichiers dans un nouveau fichier appelé `newfile` :

```bash
cat file1 file2 > newfile
```

* Ajouter un autre fichier dans `newfile` :

```bash
cat file3 >> newfile
```

* Supprimer un fichier :

```bash
rm newfile
```

* Supprimer tous les fichiers ayant la même extension de fichier :

```bash
rm *.dat
```

* Créer un répertoire :

```bash
mkdir dir1
```

### Chaînage de commandes avec des tubes

Les tubes permettent à un utilisateur d'envoyer la sortie d'une commande à une autre en utilisant le symbole de tube `|` :

```bash
echo "hi" | sed 's/hi/bye/'
```

* Filtrer les sorties de commandes en utilisant grep :

```bash
echo "id,title" > test-file.txt
echo "1,birds" >> test-file.txt
echo "2,fish" >> test-file.txt
echo "3,cats" >> test-file.txt

cat test-file.txt | grep fish
```

* Ignorer la casse :

```bash
grep -i FISH test-file.txt
```

* Compter les lignes correspondantes :

```bash
grep -c fish test-file.txt
```

* Retourner les sorties ne contenant pas le mot-clé :

```bash
grep -v birds test-file.txt
```

* Compter le nombre de lignes dans `test-file.txt` :

```bash
wc -l test-file.txt
```

* Afficher la sortie écran par écran :

```bash
more test-file.txt
```

...avec contrôles :

- Défiler ligne par ligne : *entrée*
- Aller à la page suivante : *barre d'espace*
- Revenir à la page précédente : *b*

* Afficher les 3 premières lignes du fichier :

```bash
head -3 test-file.txt
```

* Afficher les 2 dernières lignes du fichier :

```bash
tail -2 test-file.txt
```
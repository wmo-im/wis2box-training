---
title: Linux cheatsheet
---

# Linux cheatsheet

## Overview

The basic concepts of working in a Linux operating system are **files** and **directories** (folders) organized in
a tree structure within an **environment**.

Once you login to a Linux system, you are working in a **shell** in which you can work on files and directories,
by executing commands which are installed on the system.  The Bash shell is a common and popular shell which
is typically found on Linux systems.

## Bash

### Directory Navigation

* Entering an absolute directory:

```bash
cd /dir1/dir2
```

* Entering a relative directory:

```bash
cd ./somedir
```

* Move one directory up:

```bash
cd ..
```

* Move two directories up:

```bash
cd ../..
```

* Move to your "home" directory:

```bash
cd -
```

### File Management

* Listing files in the current directory:

```bash
ls
```

* Listing files in the current directory with more detail:

```bash
ls -l
```

* List the root of the filessystem:

```bash
ls -l /
```

* Create an empty file:

```bash
touch foo.txt
```

* Create a file from an `echo` command:

```bash
echo "hi there" > test-file.txt
```

* View the contents of a file:

```bash
cat test-file.txt
```

* Copy a file:

```bash
cp file1 file2
```

* Wildcards: operate on file patterns:

```bash
ls -l fil*  # matches file1 and file2
```

* Concatenate two files into a new file called `newfile`:

```bash
cat file1 file2 > newfile
```

* Append another file into `newfile`

```bash
cat file3 >> newfile
```

* Delete a file:

```bash
rm newfile
```

* Delete all files with the same file extension:

```bash
rm *.dat
```

* Create a directory

```bash
mkdir dir1
```

### Chaining commands together with pipes

Pipes allow a user to send the output of one command to another using the pipe `|` symbol:

```bash
echo "hi" | sed 's/hi/bye/'
```

* Filtering command outputs using grep:


```bash
echo "id,title" > test-file.txt
echo "1,birds" >> test-file.txt
echo "2,fish" >> test-file.txt
echo "3,cats" >> test-file.txt

cat test-file.txt | grep fish
```

* Ignoring case:

```bash
grep -i FISH test-file.txt
```

* Count matching lines:

```bash
grep -c fish test-file.txt
```

* Return outputs not containing keyword:

```bash
grep -v birds test-file.txt
```

* Count the number of lines in `test-file.txt`:

```bash
wc -l test-file.txt
```

* Display output one screen at a time:

```bash
more test-file.txt
```

...with controls:

- Scroll down line by line: *enter*
- Go to next page: *space bar*
- Go back one page: *b*

* Display the first 3 lines of the file:

```bash
head -3 test-file.txt
```

* Display the last 2 lines of the file:

```bash
tail -2 test-file.txt
```

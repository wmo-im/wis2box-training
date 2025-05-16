---
title: Linux cheatsheet
---

# Linux cheatsheet

## Visão Geral

Os conceitos básicos de trabalho em um sistema operacional Linux são **arquivos** e **diretórios** (pastas) organizados em
uma estrutura de árvore dentro de um **ambiente**.

Uma vez que você faz login em um sistema Linux, você está trabalhando em um **shell** no qual pode trabalhar com arquivos e diretórios,
executando comandos que estão instalados no sistema. O shell Bash é um shell comum e popular que
é tipicamente encontrado em sistemas Linux.

## Bash

### Navegação de Diretórios

* Entrando em um diretório absoluto:

```bash
cd /dir1/dir2
```

* Entrando em um diretório relativo:

```bash
cd ./somedir
```

* Mover um diretório para cima:

```bash
cd ..
```

* Mover dois diretórios para cima:

```bash
cd ../..
```

* Mover para o seu diretório "home":

```bash
cd -
```

### Gerenciamento de Arquivos

* Listando arquivos no diretório atual:

```bash
ls
```

* Listando arquivos no diretório atual com mais detalhes:

```bash
ls -l
```

* Listar a raiz do sistema de arquivos:

```bash
ls -l /
```

* Criar um arquivo vazio:

```bash
touch foo.txt
```

* Criar um arquivo a partir de um comando `echo`:

```bash
echo "hi there" > test-file.txt
```

* Visualizar o conteúdo de um arquivo:

```bash
cat test-file.txt
```

* Copiar um arquivo:

```bash
cp file1 file2
```

* Curingas: operar em padrões de arquivo:

```bash
ls -l fil*  # corresponde a file1 e file2
```

* Concatenar dois arquivos em um novo arquivo chamado `newfile`:

```bash
cat file1 file2 > newfile
```

* Anexar outro arquivo em `newfile`

```bash
cat file3 >> newfile
```

* Excluir um arquivo:

```bash
rm newfile
```

* Excluir todos os arquivos com a mesma extensão de arquivo:

```bash
rm *.dat
```

* Criar um diretório

```bash
mkdir dir1
```

### Encadeando comandos juntos com pipes

Pipes permitem que um usuário envie a saída de um comando para outro usando o símbolo de pipe `|`:

```bash
echo "hi" | sed 's/hi/bye/'
```

* Filtrando saídas de comandos usando grep:


```bash
echo "id,title" > test-file.txt
echo "1,birds" >> test-file.txt
echo "2,fish" >> test-file.txt
echo "3,cats" >> test-file.txt

cat test-file.txt | grep fish
```

* Ignorando maiúsculas e minúsculas:

```bash
grep -i FISH test-file.txt
```

* Contar linhas correspondentes:

```bash
grep -c fish test-file.txt
```

* Retornar saídas que não contêm a palavra-chave:

```bash
grep -v birds test-file.txt
```

* Contar o número de linhas em `test-file.txt`:

```bash
wc -l test-file.txt
```

* Exibir saída uma tela por vez:

```bash
more test-file.txt
```

...com controles:

- Rolar para baixo linha por linha: *enter*
- Ir para a próxima página: *barra de espaço*
- Voltar uma página: *b*

* Exibir as primeiras 3 linhas do arquivo:

```bash
head -3 test-file.txt
```

* Exibir as últimas 2 linhas do arquivo:

```bash
tail -2 test-file.txt
```
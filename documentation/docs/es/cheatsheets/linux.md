---
title: Linux cheatsheet
---

# Linux cheatsheet

## Resumen

Los conceptos básicos para trabajar en un sistema operativo Linux son **archivos** y **directorios** (carpetas) organizados en
una estructura de árbol dentro de un **entorno**.

Una vez que inicias sesión en un sistema Linux, estás trabajando en una **shell** en la que puedes trabajar con archivos y directorios,
ejecutando comandos que están instalados en el sistema. La shell Bash es una shell común y popular que
se encuentra típicamente en los sistemas Linux.

## Bash

### Navegación de directorios

* Ingresar a un directorio absoluto:

```bash
cd /dir1/dir2
```

* Ingresar a un directorio relativo:

```bash
cd ./somedir
```

* Moverse un directorio hacia arriba:

```bash
cd ..
```

* Moverse dos directorios hacia arriba:

```bash
cd ../..
```

* Moverse a tu directorio "home":

```bash
cd -
```

### Gestión de archivos

* Listar archivos en el directorio actual:

```bash
ls
```

* Listar archivos en el directorio actual con más detalle:

```bash
ls -l
```

* Listar la raíz del sistema de archivos:

```bash
ls -l /
```

* Crear un archivo vacío:

```bash
touch foo.txt
```

* Crear un archivo desde un comando `echo`:

```bash
echo "hi there" > test-file.txt
```

* Ver el contenido de un archivo:

```bash
cat test-file.txt
```

* Copiar un archivo:

```bash
cp file1 file2
```

* Comodines: operar sobre patrones de archivos:

```bash
ls -l fil*  # coincide con file1 y file2
```

* Concatenar dos archivos en un nuevo archivo llamado `newfile`:

```bash
cat file1 file2 > newfile
```

* Añadir otro archivo a `newfile`

```bash
cat file3 >> newfile
```

* Eliminar un archivo:

```bash
rm newfile
```

* Eliminar todos los archivos con la misma extensión de archivo:

```bash
rm *.dat
```

* Crear un directorio

```bash
mkdir dir1
```

### Encadenar comandos juntos con tuberías

Las tuberías permiten a un usuario enviar la salida de un comando a otro usando el símbolo de tubería `|`:

```bash
echo "hi" | sed 's/hi/bye/'
```

* Filtrar salidas de comandos usando grep:


```bash
echo "id,title" > test-file.txt
echo "1,birds" >> test-file.txt
echo "2,fish" >> test-file.txt
echo "3,cats" >> test-file.txt

cat test-file.txt | grep fish
```

* Ignorar mayúsculas y minúsculas:

```bash
grep -i FISH test-file.txt
```

* Contar líneas coincidentes:

```bash
grep -c fish test-file.txt
```

* Devolver salidas que no contienen la palabra clave:

```bash
grep -v birds test-file.txt
```

* Contar el número de líneas en `test-file.txt`:

```bash
wc -l test-file.txt
```

* Mostrar salida una pantalla a la vez:

```bash
more test-file.txt
```

...con controles:

- Desplazarse hacia abajo línea por línea: *enter*
- Ir a la siguiente página: *barra espaciadora*
- Volver una página: *b*

* Mostrar las primeras 3 líneas del archivo:

```bash
head -3 test-file.txt
```

* Mostrar las últimas 2 líneas del archivo:

```bash
tail -2 test-file.txt
```
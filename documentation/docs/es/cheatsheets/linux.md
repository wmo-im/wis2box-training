---
title: Hoja de trucos de Linux
---

# Hoja de trucos de Linux

## Visión general

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

* Subir un directorio:

```bash
cd ..
```

* Subir dos directorios:

```bash
cd ../..
```

* Moverse al directorio "home":

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
echo "hola" > archivo-prueba.txt
```

* Ver el contenido de un archivo:

```bash
cat archivo-prueba.txt
```

* Copiar un archivo:

```bash
cp archivo1 archivo2
```

* Comodines: operar con patrones de archivos:

```bash
ls -l arch*  # coincide con archivo1 y archivo2
```

* Concatenar dos archivos en un nuevo archivo llamado `nuevoarchivo`:

```bash
cat archivo1 archivo2 > nuevoarchivo
```

* Añadir otro archivo a `nuevoarchivo`

```bash
cat archivo3 >> nuevoarchivo
```

* Eliminar un archivo:

```bash
rm nuevoarchivo
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
echo "hola" | sed 's/hola/adiós/'
```

* Filtrar salidas de comandos usando grep:

```bash
echo "id,título" > archivo-prueba.txt
echo "1,pájaros" >> archivo-prueba.txt
echo "2,peces" >> archivo-prueba.txt
echo "3,gatos" >> archivo-prueba.txt

cat archivo-prueba.txt | grep peces
```

* Ignorar mayúsculas y minúsculas:

```bash
grep -i PECES archivo-prueba.txt
```

* Contar líneas coincidentes:

```bash
grep -c peces archivo-prueba.txt
```

* Devolver salidas que no contienen la palabra clave:

```bash
grep -v pájaros archivo-prueba.txt
```

* Contar el número de líneas en `archivo-prueba.txt`:

```bash
wc -l archivo-prueba.txt
```

* Mostrar salida una pantalla a la vez:

```bash
more archivo-prueba.txt
```

...con controles:

- Desplazarse hacia abajo línea por línea: *enter*
- Ir a la siguiente página: *barra espaciadora*
- Regresar una página: *b*

* Mostrar las primeras 3 líneas del archivo:

```bash
head -3 archivo-prueba.txt
```

* Mostrar las últimas 2 líneas del archivo:

```bash
tail -2 archivo-prueba.txt
```
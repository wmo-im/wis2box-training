---
title: Conversión de datos SYNOP a BUFR
---

# Conversión de datos SYNOP a BUFR desde la línea de comandos

!!! abstract "Resultados de aprendizaje"
    Al final de esta sesión práctica, podrás:

    - usar la herramienta synop2bufr para convertir informes SYNOP FM-12 a BUFR;
    - diagnosticar y corregir errores de codificación simples en informes SYNOP FM-12 antes de la conversión de formato;

## Introducción

Los informes meteorológicos de superficie de las estaciones terrestres se han informado históricamente cada hora o en las horas sinópticas principales
(00, 06, 12 y 18 UTC) e intermedias (03, 09, 15, 21 UTC). Antes de la migración
a BUFR, estos informes se codificaban en el formato de texto plano SYNOP FM-12. Aunque la migración a BUFR
estaba programada para completarse en 2012, todavía se intercambian un gran número de informes en el formato legado
FM-12 SYNOP. Puedes encontrar más información sobre el formato FM-12 SYNOP en el Manual de Códigos de la OMM, 
Volumen I.1 (OMM-No. 306, Volumen I.1).

[Manual de Códigos de la OMM, Volumen I.1](https://library.wmo.int/records/item/35713-manual-on-codes-international-codes-volume-i-1)

Para ayudar a completar la migración a BUFR, se han desarrollado algunas herramientas para
codificar informes SYNOP FM-12 a BUFR, en esta sesión aprenderás a usar estas herramientas así
como la relación entre la información contenida en los informes SYNOP FM-12 y los mensajes BUFR.

## Preparación

!!! warning "Prerrequisitos"

    - Asegúrate de que tu wis2box ha sido configurado y iniciado.
    - Confirma el estado visitando la API de wis2box (``http://<tu-nombre-de-host>/oapi``) y verificando que la API está funcionando.
    - Asegúrate de leer las secciones **synop2bufr primer** y **ecCodes primer** antes de comenzar los ejercicios.

## synop2bufr primer

A continuación, se presentan los comandos y configuraciones esenciales de `synop2bufr`:

### transform
La función `transform` convierte un mensaje SYNOP a BUFR:

```bash
synop2bufr data transform --metadata my_file.csv --output-dir ./my_directory --year message_year --month message_month my_SYNOP.txt
```

Nota que si no se especifican las opciones de metadatos, directorio de salida, año y mes, asumirán sus valores predeterminados:

| Opción      | Predeterminado |
| ----------- | ----------- |
| --metadata | station_list.csv |
| --output-dir | El directorio de trabajo actual. |
| --year | El año actual. |
| --month | El mes actual. |

!!! note
    Debe tenerse cuidado al usar el año y mes predeterminados, ya que el día del mes especificado en el informe puede no corresponder (por ejemplo, junio no tiene 31 días).

En los ejemplos, no se dan el año y el mes, así que siéntete libre de especificar una fecha tú mismo o usar los valores predeterminados.

## ecCodes primer

ecCodes proporciona tanto herramientas de línea de comandos como puede ser integrado en tus propias aplicaciones. A continuación, se presentan algunas utilidades de línea de comandos útiles para trabajar con datos BUFR.

### bufr_dump

El comando `bufr_dump` es una herramienta genérica de información BUFR. Tiene muchas opciones, pero las siguientes serán las más aplicables a los ejercicios:

```bash
bufr_dump -p my_bufr.bufr4
```

Esto mostrará el contenido BUFR en tu pantalla. Si estás interesado en los valores que toma una variable en particular, usa el comando `egrep`:

```bash
bufr_dump -p my_bufr.bufr4 | egrep -i temperature
```

Esto mostrará variables relacionadas con la temperatura en tus datos BUFR. Si quieres hacer esto para múltiples tipos de variables, filtra la salida usando un pipe (`|`):

```bash
bufr_dump -p my_bufr.bufr4 | egrep -i 'temperature|wind'
```

## Conversión de SYNOP FM-12 a BUFR usando synop2bufr desde la línea de comandos

La biblioteca eccodes y el módulo synop2bufr están instalados en el contenedor wis2box-api. Para realizar los próximos ejercicios, copiaremos el directorio synop2bufr-exercises al contenedor wis2box-api y ejecutaremos los ejercicios desde allí.

```bash
docker cp ~/exercise-materials/synop2bufr-exercises wis2box-api:/root
```

Ahora podemos entrar al contenedor y ejecutar los ejercicios:

```bash
docker exec -it wis2box-api /bin/bash
```

### Ejercicio 1
Navega al directorio `/root/synop2bufr-exercises/ex_1` e inspecciona el archivo de mensaje SYNOP message.txt:

```bash
cd /root/synop2bufr-exercises/ex_1
more message.txt
```

!!! question

    ¿Cuántos informes SYNOP hay en este archivo?

??? success "Haz clic para revelar la respuesta"
    
    Hay 1 informe SYNOP, ya que solo hay 1 delimitador (=) al final del mensaje.

Inspecciona la lista de estaciones:

```bash
more station_list.csv
```

!!! question

    ¿Cuántas estaciones están listadas en la lista de estaciones?

??? success "Haz clic para revelar la respuesta"

    Hay 1 estación, el archivo station_list.csv contiene una fila de metadatos de estación.

!!! question
    Intenta convertir `message.txt` a formato BUFR.

??? success "Haz clic para revelar la respuesta"

    Para convertir el mensaje SYNOP a formato BUFR, usa el siguiente comando:

    ```bash
    synop2bufr data transform --metadata station_list.csv --output-dir ./ --year 2024 --month 09 message.txt
    ```

!!! tip

    Consulta la sección [synop2bufr primer](#synop2bufr-primer).

Inspecciona los datos BUFR resultantes usando `bufr_dump`.

!!! question
     Averigua cómo comparar los valores de latitud y longitud con los de la lista de estaciones.

??? success "Haz clic para revelar la respuesta"

    Para comparar los valores de latitud y longitud en los datos BUFR con los de la lista de estaciones, usa el siguiente comando:

    ```bash
    bufr_dump -p WIGOS_0-20000-0-15015_20240921T120000.bufr4 | egrep -i 'latitude|longitude'
    ```

    Esto mostrará los valores de latitud y longitud en los datos BUFR.

!!! tip

    Consulta la sección [ecCodes primer](#eccodes-primer).

### Ejercicio 2
Navega al directorio `exercise-materials/synop2bufr-exercises/ex_2` e inspecciona el archivo de mensaje SYNOP message.txt:

```bash
cd /root/synop2bufr-exercises/ex_2
more message.txt
```

!!! question

    ¿Cuántos informes SYNOP hay en este archivo?

??? success "Haz clic para revelar la respuesta"

    Hay 3 informes SYNOP, ya que hay 3 delimitadores (=) al final del mensaje.

Inspecciona la lista de estaciones:

```bash
more station_list.csv
```

!!! question

    ¿Cuántas estaciones están listadas en la lista de estaciones?

??? success "Haz clic para revelar la respuesta"

    Hay 3 estaciones, el archivo station_list.csv contiene tres filas de metadatos de estación.

!!! question
    Convierte `message.txt` a formato BUFR.

??? success "Haz clic para revelar la respuesta"

    Para convertir el mensaje SYNOP a formato BUFR, usa el siguiente comando:

    ```bash
    synop2bufr data transform --metadata station_list.csv --output-dir ./ --year 2024 --month 09 message.txt
    ```

!!! question

    Basado en los resultados de los ejercicios en esta y la sesión anterior, ¿cómo predecirías el número de
    archivos BUFR resultantes basado en el número de informes SYNOP y estaciones listadas en el archivo de metadatos de la estación?

??? success "Haz clic para revelar la respuesta"

    Para ver los archivos BUFR producidos ejecuta el siguiente comando:

    ```bash
    ls -l *.bufr4
    ```

    El número de archivos BUFR producidos será igual al número de informes SYNOP en el archivo de mensaje.

Inspecciona los datos BUFR resultantes usando `bufr_dump`.

!!! question
    ¿Cómo puedes verificar el ID de Estación WIGOS codificado dentro de los datos BUFR de cada archivo producido?

??? success "Haz clic para revelar la respuesta"

    Esto se puede hacer usando los siguientes comandos:

    ```bash
    bufr_dump -p WIGOS_0-20000-0-15015_20240921T120000.bufr4 | egrep -i 'wigos'
    ```

    ```bash
    bufr_dump -p WIGOS_0-20000-0-15020_20240921T120000.bufr4 | egrep -i 'wigos'
    ```

    ```bash
    bufr_dump -p WIGOS_0-20000-0-15090_20240921T120000.bufr4 | egrep -i 'wigos'
    ```

    Ten en cuenta que si tienes un directorio con solo estos 3 archivos BUFR, puedes usar comodines de Linux de la siguiente manera:

    ```bash
    bufr_dump -p *.bufr4 | egrep -i 'wigos'
    ```

### Ejercicio 3
Navega al directorio `exercise-materials/synop2bufr-exercises/ex_3` e inspecciona el archivo de mensaje SYNOP message.txt:

```bash
cd /root/synop2bufr-exercises/ex_3
more message.txt
```

Este mensaje SYNOP solo contiene un informe más largo con más secciones.

Inspecciona la lista de estaciones:

```bash
more station_list.csv
```

!!! question

    ¿Es problemático que este archivo contenga más estaciones de las que hay informes en el mensaje SYNOP?

??? success "Haz clic para revelar la respuesta"

    No, esto no es un problema siempre y cuando exista una fila en el archivo de la lista de estaciones con un TSI de estación que coincida con el del informe SYNOP que estamos tratando de convertir.

!!! note

    El archivo de la lista de estaciones es una fuente de metadatos para `synop2bufr` para proporcionar la información que falta en el informe SYNOP alfanumérico y que se requiere en el SYNOP BUFR.

!!! question
    Convierte `message.txt` a formato BUFR.

??? success "Haz clic para revelar la respuesta"

    Esto se hace usando el comando `transform`, por ejemplo:

    ```bash
    synop2bufr data transform --metadata station_list.csv --output-dir ./ --year 2024 --month 09 message.txt
    ```

Inspecciona los datos BUFR resultantes usando `bufr_dump`.

!!! question

    Encuentra las siguientes variables:

    - Temperatura del aire (K) del informe
    - Cobertura total de nubes (%) del informe
    - Periodo total de sol (minutos) del informe
    - Velocidad del viento (m/s) del informe

??? success "Haz clic para revelar la respuesta"

    Para encontrar las variables por palabra clave en los datos BUFR, puedes usar los siguientes comandos:

    ```bash
    bufr_dump -p WIGOS_0-20000-0-15260_20240921T115500.bufr4 | egrep -i 'temperature'
    ```

    Puedes usar el siguiente comando para buscar múltiples palabras clave:

    ```bash
    bufr_dump -p WIGOS_0-20000-0-15260_20240921T115500.bufr4 | egrep -i 'temperature|cover|sunshine|wind'
    ```

!!! tip

    Puedes encontrar útil el último comando de la sección [ecCodes primer](#eccodes-primer).


### Ejercicio 4
Navega al directorio `exercise-materials/synop2bufr-exercises/ex_4` e inspecciona el archivo de mensaje SYNOP message.txt:

```bash
cd /root/synop2bufr-exercises/ex_4
more message_incorrect.txt
```

!!! question

    ¿Qué es incorrecto sobre este archivo SYNOP?

??? success "Haz clic para revelar la respuesta"

    El informe SYNOP para 15015 está faltando el delimitador (`=`) que permite a `synop2bufr` distinguir este informe del siguiente.

Intenta convertir `message_incorrect.txt` usando `station_list.csv`

!!! question

    ¿Qué problema(s) encontraste con esta conversión?

??? success "Haz clic para revelar la respuesta"

    Para convertir el mensaje SYNOP a formato BUFR, usa el siguiente comando:

    ```bash
    synop2bufr data transform --metadata station_list.csv --output-dir ./ --year 2024 --month 09 message_incorrect.txt
    ```

    Intentar convertir debería generar los siguientes errores:
    
    - `[ERROR] No se pudo decodificar el mensaje SYNOP`
    - `[ERROR] Error al analizar el informe SYNOP: AAXX 21121 15015 02999 02501 10103 21090 39765 42952 57020 60001 15020 02997 23104 10130 21075 30177 40377 58020 60001 81041. ¡10130 no es un grupo válido!`

### Ejercicio 5
Navega al directorio `exercise-materials/synop2bufr-exercises/ex_5` e inspecciona el archivo de mensaje SYNOP message.txt:

```bash
cd /root/synop2bufr-exercises/ex_5
more message.txt
```

Intenta convertir `message.txt` a formato BUFR usando `station_list_incorrect.csv` 

!!! question

    ¿Qué problema(s) encontraste con esta conversión?  
    Considerando el error presentado, justifica el número de archivos BUFR producidos.

??? success "Haz clic para revelar la respuesta"

    Para convertir el mensaje SYNOP a formato BUFR, usa el siguiente comando:

    ```bash
    synop2bufr data transform --metadata station_list_incorrect.csv --output-dir ./ --year 2024 --month 09 message.txt
    ```

    Uno de los TSIs de la estación (`15015`) no tiene metadatos correspondientes en la lista de estaciones, lo que impedirá que synop2bufr acceda a metadatos adicionales necesarios para convertir el primer informe SYNOP a BUFR.

    Verás la siguiente advertencia:

    - `[ADVERTENCIA] Estación 15015 no encontrada en el archivo de estaciones`

    Puedes ver el número de archivos BUFR producidos ejecutando el siguiente comando:

    ```bash
    ls -l *.bufr4
    ```

    Hay 3 informes SYNOP en message.txt pero solo se han producido 2 archivos BUFR. Esto es porque a uno de los informes SYNOP le faltaban los metadatos necesarios como se mencionó anteriormente.

## Conclusión

!!! success "¡Felicidades!"

    En esta sesión práctica, aprendiste:

    - cómo la herramienta synop2bufr puede ser usada para convertir informes SYNOP FM-12 a BUFR;
    - cómo diagnosticar y corregir errores de codificación simples en informes SYNOP FM-12 antes de la conversión de formato;

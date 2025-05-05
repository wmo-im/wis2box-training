---
title: Herramientas de Conversión de Datos
---

# Herramientas de Conversión de Datos

!!! abstract "Resultados de Aprendizaje"
    Al finalizar esta sesión práctica, podrás:

    - Acceder a las herramientas de línea de comandos de ecCodes dentro del contenedor wis2box-api
    - Usar la herramienta synop2bufr para convertir reportes FM-12 SYNOP a BUFR desde la línea de comandos
    - Activar la conversión synop2bufr a través de wis2box-webapp
    - Usar la herramienta csv2bufr para convertir datos CSV a BUFR desde la línea de comandos

## Introducción

Los datos publicados en WIS2 deben cumplir con los requisitos y estándares definidos por las diversas comunidades expertas en disciplinas y dominios del sistema Tierra. Para reducir las barreras en la publicación de datos para observaciones terrestres de superficie, wis2box proporciona herramientas para convertir datos al formato BUFR. Estas herramientas están disponibles a través del contenedor wis2box-api y pueden utilizarse desde la línea de comandos para probar el proceso de conversión de datos.

Las principales conversiones actualmente soportadas por wis2box son de reportes FM-12 SYNOP a BUFR y de datos CSV a BUFR. Los datos FM-12 son soportados ya que todavía son ampliamente utilizados e intercambiados en la comunidad de la WMO, mientras que los datos CSV son soportados para permitir el mapeo de datos producidos por estaciones meteorológicas automáticas al formato BUFR.

### Acerca de FM-12 SYNOP

Los reportes meteorológicos de superficie de estaciones terrestres históricamente se han reportado cada hora o en las horas sinópticas principales (00, 06, 12 y 18 UTC) e intermedias (03, 09, 15, 21 UTC). Antes de la migración a BUFR, estos reportes se codificaban en el formato de texto plano FM-12 SYNOP. Aunque la migración a BUFR estaba programada para completarse en 2012, una gran cantidad de reportes todavía se intercambian en el formato heredado FM-12 SYNOP. Puede encontrar más información sobre el formato FM-12 SYNOP en el Manual de Códigos de la WMO, Volumen I.1 (WMO-No. 306, Volumen I.1).

### Acerca de ecCodes

La biblioteca ecCodes es un conjunto de bibliotecas de software y utilidades diseñadas para decodificar y codificar datos meteorológicos en los formatos GRIB y BUFR. Es desarrollada por el Centro Europeo de Previsiones Meteorológicas a Medio Plazo (ECMWF), consulte la [documentación de ecCodes](https://confluence.ecmwf.int/display/ECC/ecCodes+documentation) para más información.

El software wis2box incluye la biblioteca ecCodes en la imagen base del contenedor wis2box-api. Esto permite a los usuarios acceder a las herramientas de línea de comandos y bibliotecas desde dentro del contenedor. La biblioteca ecCodes se utiliza dentro del wis2box-stack para decodificar y codificar mensajes BUFR.

### Acerca de csv2bufr y synop2bufr

Además de ecCodes, wis2box utiliza los siguientes módulos Python que trabajan con ecCodes para convertir datos al formato BUFR:

- **synop2bufr**: para soportar el formato heredado FM-12 SYNOP tradicionalmente utilizado por observadores manuales. El módulo synop2bufr depende de metadatos adicionales de la estación para codificar parámetros adicionales en el archivo BUFR. Consulte el [repositorio synop2bufr en GitHub](https://github.com/World-Meteorological-Organization/synop2bufr)
- **csv2bufr**: para permitir la conversión de extractos CSV producidos por estaciones meteorológicas automáticas al formato BUFR. El módulo csv2bufr se utiliza para convertir datos CSV al formato BUFR usando una plantilla de mapeo que define cómo los datos CSV deben mapearse al formato BUFR. Consulte el [repositorio csv2bufr en GitHub](https://github.com/World-Meteorological-Organization/csv2bufr)

Estos módulos pueden utilizarse de forma independiente o como parte del stack wis2box.

## Preparación

!!! warning "Prerrequisitos"

    - Asegúrate de que tu wis2box ha sido configurado e iniciado
    - Asegúrate de haber configurado un conjunto de datos y al menos una estación en tu wis2box
    - Conéctate al broker MQTT de tu instancia wis2box usando MQTT Explorer
    - Abre la aplicación web wis2box (`http://YOUR-HOST/wis2box-webapp`) y asegúrate de haber iniciado sesión
    - Abre el panel de Grafana para tu instancia accediendo a `http://YOUR-HOST:3000`

Para usar las herramientas de línea de comandos BUFR, necesitarás estar conectado al contenedor wis2box-api. A menos que se especifique lo contrario, todos los comandos deben ejecutarse en este contenedor. También necesitarás tener MQTT Explorer abierto y conectado a tu broker.

Primero, conéctate a tu VM de estudiante a través de tu cliente SSH y copia los materiales de ejercicio al contenedor wis2box-api:

```bash
docker cp ~/exercise-materials/data-conversion-exercises wis2box-api:/root
```

Luego inicia sesión en el contenedor wis2box-api y cambia al directorio donde se encuentran los materiales de ejercicio:

```bash
cd ~/wis2box
python3 wis2box-ctl.py login wis2box-api
cd /root/data-conversion-exercises
```

Confirma que las herramientas están disponibles, comenzando con ecCodes:

```bash
bufr_dump -V
```

Deberías obtener la siguiente respuesta:

```
ecCodes Version 2.36.0
```

Luego, verifica la versión de synop2bufr:

```bash
synop2bufr --version
```

Deberías obtener la siguiente respuesta:

```
synop2bufr, version 0.7.0
```

Luego, verifica csv2bufr:

```bash
csv2bufr --version
```

Deberías obtener la siguiente respuesta:

```
csv2bufr, version 0.8.5
```

## Herramientas de línea de comandos ecCodes

La biblioteca ecCodes incluida en el contenedor wis2box-api proporciona varias herramientas de línea de comandos para trabajar con archivos BUFR. 
Los siguientes ejercicios demuestran cómo usar `bufr_ls` y `bufr_dump` para verificar el contenido de un archivo BUFR.

### bufr_ls

En este primer ejercicio, usarás el comando `bufr_ls` para inspeccionar los encabezados de un archivo BUFR y determinar el tipo de contenido del archivo.

Usa el siguiente comando para ejecutar `bufr_ls` en el archivo `bufr-cli-ex1.bufr4`:

```bash
bufr_ls bufr-cli-ex1.bufr4
```

Deberías ver la siguiente salida:

```bash
bufr-cli-ex1.bufr4
centre                     masterTablesVersionNumber  localTablesVersionNumber   typicalDate                typicalTime                numberOfSubsets
cnmc                       29                         0                          20231002                   000000                     1
1 of 1 messages in bufr-cli-ex1.bufr4

1 of 1 total messages in 1 file
```

Se pueden pasar varias opciones a `bufr_ls` para cambiar tanto el formato como los campos de encabezado impresos.

!!! question
     
    ¿Cuál sería el comando para listar la salida anterior en formato JSON?

    Puedes ejecutar el comando `bufr_ls` con la bandera `-h` para ver las opciones disponibles.

??? success "Haz clic para revelar la respuesta"
    Puedes cambiar el formato de salida a JSON usando la bandera `-j`, es decir:
    ```bash
    bufr_ls -j bufr-cli-ex1.bufr4
    ```

    Al ejecutarlo, deberías obtener la siguiente salida:
    ```
    { "messages" : [
      {
        "centre": "cnmc",
        "masterTablesVersionNumber": 29,
        "localTablesVersionNumber": 0,
        "typicalDate": 20231002,
        "typicalTime": "000000",
        "numberOfSubsets": 1
      }
    ]}
    ```

La salida impresa representa los valores de algunas de las claves de encabezado en el archivo BUFR.

Por sí sola, esta información no es muy informativa, ya que solo proporciona información limitada sobre el contenido del archivo.

Al examinar un archivo BUFR, a menudo queremos determinar el tipo de datos contenidos en el archivo y la fecha/hora típica de los datos en el archivo. Esta información se puede listar usando la bandera `-p` para seleccionar los encabezados a mostrar. Se pueden incluir múltiples encabezados usando una lista separada por comas.

Puedes usar el siguiente comando para listar la categoría de datos, subcategoría, fecha típica y hora:
    
```bash
bufr_ls -p dataCategory,internationalDataSubCategory,typicalDate,typicalTime -j bufr-cli-ex1.bufr4
```

!!! question

    Ejecuta el comando anterior e interpreta la salida usando la [Tabla Común de Códigos C-13](https://github.com/wmo-im/CCT/blob/master/C13.csv) para determinar la categoría y subcategoría de datos.

    ¿Qué tipo de datos (categoría y subcategoría) contiene el archivo? ¿Cuál es la fecha y hora típica de los datos?

??? success "Haz clic para revelar la respuesta"
    
    ```
    { "messages" : [
      {
        "dataCategory": 2,
        "internationalDataSubCategory": 4,
        "typicalDate": 20231002,
        "typicalTime": "000000"
      }
    ]}
    ```

    De esto, vemos que:

    - La categoría de datos es 2, indicando datos de **"Sondeos verticales (distintos de satélite)"**.
    - La subcategoría internacional es 4, indicando **"Reportes de temperatura/humedad/viento en altura desde estaciones terrestres fijas (TEMP)"**.
    - La fecha y hora típicas son 2023-10-02 y 00:00:00z, respectivamente.

### bufr_dump

El comando `bufr_dump` puede usarse para listar y examinar el contenido de un archivo BUFR, incluyendo los datos mismos.

Intenta ejecutar el comando `bufr_dump` en el segundo archivo de ejemplo `bufr-cli-ex2.bufr4`:

```{.copy}
bufr_dump bufr-cli-ex2.bufr4
```

Esto resulta en un JSON que puede ser difícil de analizar, intenta usar la bandera `-p` para mostrar los datos en formato de texto plano (formato clave=valor):

```{.copy}
bufr_dump -p bufr-cli-ex2.bufr4
```

Verás una gran cantidad de claves como salida, muchas de las cuales están ausentes. Esto es típico con datos del mundo real ya que no todas las claves de eccodes están pobladas con datos reportados.

Puedes usar el comando `grep` para filtrar la salida y mostrar solo las claves que no están ausentes. Por ejemplo, para mostrar todas las claves que no están ausentes, puedes usar el siguiente comando:

```{.copy}
bufr_dump -p bufr-cli-ex2.bufr4 | grep -v MISSING
```

!!! question

    ¿Cuál es la presión reducida al nivel medio del mar reportada en el archivo BUFR `bufr-cli-ex2.bufr4`?

??? success "Haz clic para revelar la respuesta"

    Usando el siguiente comando:

    ```bash
    bufr_dump -p bufr-cli-ex2.bufr4 | grep -i 'pressureReducedToMeanSeaLevel'
    ```

    Deberías ver la siguiente salida:

    ```
    pressureReducedToMeanSeaLevel=105590
    ```
    Esto indica que la presión reducida al nivel medio del mar es 105590 Pa (1055.90 hPa).

!!! question

    ¿Cuál es el identificador de estación WIGOS de la estación que reportó los datos en el archivo BUFR `bufr-cli-ex2.bufr4`?

??? success "Haz clic para revelar la respuesta"

    Usando el siguiente comando:

    ```bash
    bufr_dump -p bufr-cli-ex2.bufr4 | grep -i 'wigos'
    ```

    Deberías ver la siguiente salida:

    ```
    wigosIdentifierSeries=0
    wigosIssuerOfIdentifier=20000
    wigosIssueNumber=0
    wigosLocalIdentifierCharacter="99100"
    ```

    Esto indica que el identificador de estación WIGOS es `0-20000-0-99100`.

## Conversión synop2bufr

Ahora, veamos cómo convertir datos FM-12 SYNOP al formato BUFR usando el módulo `synop2bufr`. El módulo `synop2bufr` se usa para convertir datos FM-12 SYNOP al formato BUFR. El módulo está instalado en el contenedor wis2box-api y puede usarse desde la línea de comandos de la siguiente manera:

```{.copy}
synop2bufr data transform \
    --metadata <station-metadata.csv> \
    --output-dir <output-directory-path> \
    --year <year-of-observation> \
    --month <month-of-observation> \
    <input-fm12.txt>
```

El argumento `--metadata` se usa para especificar el archivo de metadatos de la estación, que proporciona información adicional para ser codificada en el archivo BUFR.
El argumento `--output-dir` se usa para especificar el directorio donde se escribirán los archivos BUFR convertidos. Los argumentos `--year` y `--month` se usan para especificar el año y mes de la observación.

El módulo `synop2bufr` también se usa en wis2box-webapp para convertir datos FM-12 SYNOP a formato BUFR usando un formulario web.

Los siguientes ejercicios demostrarán cómo funciona el módulo `synop2bufr` y cómo usarlo para convertir datos FM-12 SYNOP al formato BUFR.

### revisar el mensaje SYNOP de ejemplo

Inspecciona el archivo de mensaje SYNOP de ejemplo para este ejercicio `synop_message.txt`:

```bash
cd /root/data-conversion-exercises
more synop_message.txt
```

!!! question

    ¿Cuántos reportes SYNOP hay en este archivo?

??? success "Haz clic para revelar la respuesta"
    
    La salida muestra lo siguiente:
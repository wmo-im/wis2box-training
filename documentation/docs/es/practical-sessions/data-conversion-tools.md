---
title: Herramientas de Conversión de Datos
---

# Herramientas de Conversión de Datos

!!! abstract "Resultados de Aprendizaje"
    Al final de esta sesión práctica, podrás:

    - Acceder a las herramientas de línea de comandos ecCodes dentro del contenedor wis2box-api
    - Utilizar la herramienta synop2bufr para convertir informes SYNOP FM-12 a BUFR desde la línea de comandos
    - Activar la conversión synop2bufr a través de wis2box-webapp
    - Utilizar la herramienta csv2bufr para convertir datos CSV a BUFR desde la línea de comandos

## Introducción

Los datos publicados en WIS2 deben cumplir con los requisitos y estándares definidos por las diversas comunidades de expertos en disciplinas/sistemas terrestres. Para reducir las barreras para la publicación de datos de observaciones superficiales terrestres, wis2box proporciona herramientas para convertir datos al formato BUFR. Estas herramientas están disponibles a través del contenedor wis2box-api y se pueden utilizar desde la línea de comandos para probar el proceso de conversión de datos.

Las principales conversiones actualmente soportadas por wis2box son informes SYNOP FM-12 a BUFR y datos CSV a BUFR. Los datos FM-12 son soportados ya que todavía se utilizan y se intercambian ampliamente en la comunidad de la OMM, mientras que los datos CSV son soportados para permitir el mapeo de datos producidos por estaciones meteorológicas automáticas al formato BUFR.

### Acerca de FM-12 SYNOP

Los informes meteorológicos superficiales de estaciones terrestres se han informado históricamente cada hora o en las horas sinópticas principales (00, 06, 12 y 18 UTC) e intermedias (03, 09, 15, 21 UTC). Antes de la migración a BUFR, estos informes se codificaban en el formato de texto plano FM-12 SYNOP. Aunque la migración a BUFR estaba programada para completarse en 2012, todavía se intercambia un gran número de informes en el formato FM-12 SYNOP heredado. Puede encontrar más información sobre el formato FM-12 SYNOP en el Manual de Códigos de la OMM, Volumen I.1 (WMO-No. 306, Volumen I.1).

### Acerca de ecCodes

La biblioteca ecCodes es un conjunto de bibliotecas de software y utilidades diseñadas para decodificar y codificar datos meteorológicos en los formatos GRIB y BUFR. Es desarrollado por el Centro Europeo de Previsiones Meteorológicas a Medio Plazo (ECMWF), consulte la [documentación de ecCodes](https://confluence.ecmwf.int/display/ECC/ecCodes+documentation) para obtener más información.

El software wis2box incluye la biblioteca ecCodes en la imagen base del contenedor wis2box-api. Esto permite a los usuarios acceder a las herramientas y bibliotecas de línea de comandos desde dentro del contenedor. La biblioteca ecCodes se utiliza dentro del stack de wis2box para decodificar y codificar mensajes BUFR.

### Acerca de csv2bufr y synop2bufr

Además de ecCodes, wis2box utiliza los siguientes módulos de Python que trabajan con ecCodes para convertir datos al formato BUFR:

- **synop2bufr**: para soportar el formato FM-12 SYNOP heredado tradicionalmente utilizado por observadores manuales. El módulo synop2bufr depende de metadatos adicionales de la estación para codificar parámetros adicionales en el archivo BUFR. Vea el [repositorio de synop2bufr en GitHub](https://github.com/World-Meteorological-Organization/synop2bufr)
- **csv2bufr**: para habilitar la conversión de datos CSV producidos por estaciones meteorológicas automáticas a formato BUFR. El módulo csv2bufr se utiliza para convertir datos CSV a formato BUFR utilizando una plantilla de mapeo que define cómo se deben mapear los datos CSV al formato BUFR. Vea el [repositorio de csv2bufr en GitHub](https://github.com/World-Meteorological-Organization/csv2bufr)

Estos módulos pueden utilizarse de forma independiente o como parte del stack de wis2box.

## Preparación

!!! warning "Prerrequisitos"

    - Asegúrate de que tu wis2box ha sido configurado y iniciado
    - Asegúrate de haber configurado un conjunto de datos y configurado al menos una estación en tu wis2box
    - Conéctate al broker MQTT de tu instancia de wis2box usando MQTT Explorer
    - Abre la aplicación web de wis2box (`http://YOUR-HOST/wis2box-webapp`) y asegúrate de estar conectado
    - Abre el tablero de Grafana para tu instancia yendo a `http://YOUR-HOST:3000`

Para utilizar las herramientas de línea de comandos BUFR, necesitarás estar conectado al contenedor wis2box-api. A menos que se especifique lo contrario, todos los comandos deben ejecutarse en este contenedor. También necesitarás tener MQTT Explorer abierto y conectado a tu broker.

Primero, conéctate a tu VM de estudiante a través de tu cliente SSH y copia los materiales del ejercicio al contenedor wis2box-api:

```bash
docker cp ~/exercise-materials/data-conversion-exercises wis2box-api:/root
```

Luego inicia sesión en el contenedor wis2box-api y cambia al directorio donde se encuentran los materiales del ejercicio:

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

A continuación, verifica la versión de synop2bufr:

```bash
synop2bufr --version
```

Deberías obtener la siguiente respuesta:

```
synop2bufr, versión 0.7.0
```

A continuación, verifica csv2bufr:

```bash
csv2bufr --version
```

Deberías obtener la siguiente respuesta:

```
csv2bufr, versión 0.8.5
```

## Herramientas de línea de comandos ecCodes

La biblioteca ecCodes incluida en el contenedor wis2box-api proporciona una serie de herramientas de línea de comandos para trabajar con archivos BUFR.
Los siguientes ejercicios demuestran cómo usar `bufr_ls` y `bufr_dump` para verificar el contenido de un archivo BUFR.

### bufr_ls

En este primer ejercicio, utilizarás el comando `bufr_ls` para inspeccionar las cabeceras de un archivo BUFR y determinar el tipo de contenido del archivo.

Utiliza el siguiente comando para ejecutar `bufr_ls` en el archivo `bufr-cli-ex1.bufr4`:

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

Se pueden pasar diversas opciones a `bufr_ls` para cambiar tanto el formato como los campos de cabecera impresos.

!!! question
     
    ¿Cuál sería el comando para listar la salida anterior en formato JSON?

    Puedes ejecutar el comando `bufr_ls` con la bandera `-h` para ver las opciones disponibles.

??? success "Haz clic para revelar la respuesta"
    Puedes cambiar el formato de salida a JSON usando la bandera `-j`, es decir,
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

La salida impresa representa los valores de algunas de las claves de cabecera en el archivo BUFR.

Por sí sola, esta información no es muy informativa, ya que solo proporciona información limitada sobre el contenido del archivo.

Al examinar un archivo BUFR, a menudo queremos determinar el tipo de datos contenidos en el archivo y la fecha/hora típica de los datos en el archivo. Esta información se puede listar usando la bandera `-p` para seleccionar las cabeceras a mostrar. Se pueden incluir múltiples cabeceras usando una lista separada por comas.

Puedes usar el siguiente comando para listar la categoría de datos, subcategoría, fecha típica y hora:
    
```bash
bufr_ls -p dataCategory,internationalDataSubCategory,typicalDate,typicalTime -j bufr-cli-ex1.bufr4
```

!!! question

    Ejecuta el comando anterior e interpreta la salida usando la [Tabla de Códigos Comunes C-13](https://github.com/wmo-im/CCT/blob/master/C13.csv) para determinar la categoría de datos y subcategoría.

    ¿Qué tipo de datos (categoría de datos y subcategoría) contiene el archivo? ¿Cuál es la fecha y hora típicas para los datos?

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

    - La categoría de datos es 2, indicando datos de **"sondeos verticales (otros que no son de satélite)"**.
    - La subcategoría internacional es 4, indicando datos de **"informes de temperatura/humedad/viento de nivel superior de estaciones fijas terrestres (TEMP)"**.
    - La fecha y hora típicas son 2023-10-02 y 00:00:00z, respectivamente.

### bufr_dump

El comando `bufr_dump` se puede usar para listar y examinar el contenido de un archivo BUFR, incluidos los datos mismos.

Intenta ejecutar el comando `bufr_dump` en el segundo archivo de ejemplo `bufr-cli-ex2.bufr4`:

```{.copy}
bufr_dump bufr-cli-ex2.bufr4
```

Esto resulta en un JSON que puede ser difícil de analizar, intenta usar la bandera `-p` para mostrar los datos en formato de texto plano (formato clave=valor):

```{.copy}
bufr_dump -p bufr-cli-ex2.bufr4
```

Deberías ver una gran cantidad de claves como salida, muchas de las cuales están ausentes. Esto es típico con datos del mundo real, ya que no todas las claves de eccodes están pobladas con datos reportados.

Puedes usar el comando `grep` para filtrar la salida y mostrar solo las claves que no están ausentes. Por ejemplo, para mostrar todas las claves que no están ausentes, puedes usar el siguiente comando:

```{.copy}
bufr_dump -p bufr-cli-ex2.bufr4 | grep -v MISSING
```

!!! question

    ¿Cuál es la presión reducida al nivel del mar reportada en el archivo BUFR `bufr-cli-ex2.bufr4`?

??? success "Haz clic para revelar la respuesta"

    Usando el siguiente comando:

    ```bash
    bufr_dump -p bufr-cli-ex2.bufr4 | grep -i 'pressureReducedToMeanSeaLevel'
    ```

    Deberías ver la siguiente salida:

    ```
    pressureReducedToMeanSeaLevel=105590
    ```
    Esto indica que la presión reducida al nivel del mar es 105590 Pa (1055.90 hPa).

!!! question

    ¿Cuál es el identificador de la estación WIGOS de la estación que reportó los datos en el archivo BUFR `bufr-cli-ex2.bufr4`?

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

    Esto indica que el identificador de la estación WIGOS es `0-20000-0-99100`.

## Conversión synop2bufr

A continuación, veamos cómo convertir datos SYNOP FM-12 a formato BUFR utilizando el módulo `synop2bufr`. El módulo `synop2bufr` se utiliza para convertir datos SYNOP FM-12 a formato BUFR. El módulo está instalado en el contenedor wis2box-api y se puede utilizar desde la línea de comandos de la siguiente manera:

```{.copy}
synop2bufr data transform \
    --metadata <station-metadata.csv> \
    --output-dir <output-directory-path> \
    --year <year-of-observation> \
    --month <month-of-observation> \
    <input-fm12.txt>
```

El argumento `--metadata` se utiliza para especificar el archivo de metadatos de la estación, que proporciona información adicional para ser codificada en el archivo BUFR.
El argumento `--output-dir` se utiliza para especificar el directorio donde se escribirán los archivos BUFR convertidos. Los argumentos `--year` y `--month` se utilizan para especificar el año y el mes de la observación.

El módulo `synop2bufr` también se utiliza en wis2box-webapp para convertir datos SYNOP FM-12 a formato BUFR utilizando un formulario de entrada basado en la web.

Los siguientes ejercicios demostrarán cómo funciona el módulo `synop2bufr` y cómo usarlo para convertir datos SYNOP FM-12 a formato BUFR.

### revisa el mensaje SYNOP de ejemplo

Inspecciona el archivo de mensaje SYNOP de ejemplo para este ejercicio `synop_message.txt`:

```bash
cd /root/data-conversion-exercises
more synop_message.txt
```

!!! question

    ¿Cuántos informes SYNOP hay en este archivo?

??? success "Haz clic para revelar la respuesta"
    
    La salida muestra lo siguiente:

    ```{.copy}
    AAXX 21121
    15015 02999 02501 10103 21090 39765 42952 57020 60001=
    15020 02997 23104 10130 21075 30177 40377 58020 60001 81041=
    15090 02997 53102 10139 21075 30271 40364 58031 60001 82046=
    ```

    Hay 3 informes SYNOP en el archivo, correspondientes a 3 estaciones diferentes (identificadas por los identificadores de estación tradicionales de 5 dígitos: 15015, 15020 y 15090).
    Note que el final de cada informe está marcado por el carácter `=`. 

### revisa la lista de estaciones

El argumento `--metadata` requiere un archivo CSV utilizando un formato predefinido, se proporciona un ejemplo funcional en el archivo `station_list.csv`:

Utiliza el siguiente comando para inspeccionar el contenido del archivo `station_list.csv`:

```bash
more station_list.csv
```

!!! question

    ¿Cuántas estaciones están listadas en la lista de estaciones? ¿Cuáles son los identificadores de estación WIGOS de las estaciones?

??? success "Haz clic para revelar la respuesta"

    La salida muestra lo siguiente:

    ```{.copy}
    station_name,wigos_station_identifier,traditional_station_identifier,facility_type,latitude,longitude,elevation,barometer_height,territory_name,wmo_region
    OCNA SUGATAG,0-20000-0-15015,15015,landFixed,47.7770616258,23.9404602638,503.0,504.0,ROU,europe
    BOTOSANI,0-20000-0-15020,15020,landFixed,47.7356532437,26.6455501701,161.0,162.1,ROU,europe
    ```

    Esto corresponde a los metadatos de la estación para 2 estaciones: para los identificadores de estación WIGOS `0-20000-0-15015` y `0-20000-0-15020`.

### convertir SYNOP a BUFR

A continuación, usa el siguiente comando para convertir el mensaje SYNOP FM-12 al formato BUFR:

```bash
synop2bufr data transform --metadata station_list.csv --output-dir ./ --year 2024 --month 09 synop_message.txt
```

!!! question
    ¿Cuántos archivos BUFR se crearon? ¿Qué significa el mensaje de ADVERTENCIA en la salida?

??? success "Haz clic para revelar la respuesta"
    La salida muestra lo siguiente:

    ```{.copy}
    [WARNING] Station 15090 not found in station file
    ```

    Si revisas el contenido de tu directorio con el comando `ls -lh`, deberías ver que se crearon 2 nuevos archivos BUFR: `WIGOS_0-20000-0-15015_20240921T120000.bufr4` y `WIGOS_0-20000-0-15020_20240921T120000.bufr4`.

    El mensaje de advertencia indica que la estación con el identificador de estación tradicional `15090` no se encontró en el archivo de lista de estaciones `station_list.csv`. Esto significa que el informe SYNOP para esta estación no se convirtió al formato BUFR.

!!! question
    Revisa el contenido del archivo BUFR `WIGOS_0-20000-0-15015_20240921T120000.bufr4` usando el comando `bufr_dump`. 

    ¿Puedes verificar que la información proporcionada en el archivo `station_list.csv` está presente en el archivo BUFR?

??? success "Haz clic para revelar la respuesta"
    Puedes usar el siguiente comando para revisar el contenido del archivo BUFR:

    ```bash
    bufr_dump -p WIGOS_0-20000-0-15015_20240921T120000.bufr4 | grep -v MISSING
    ```

    Notarás la siguiente salida:

    ```{.copy}
    wigosIdentifierSeries=0
    wigosIssuerOfIdentifier=20000
    wigosIssueNumber=0
    wigosLocalIdentifierCharacter="15015"
    blockNumber=15
    stationNumber=15
    stationOrSiteName="OCNA SUGATAG"
    stationType=1
    year=2024
    month=9
    day=21
    hour=12
    minute=0
    latitude=47.7771
    longitude=23.9405
    heightOfStationGroundAboveMeanSeaLevel=503
    heightOfBarometerAboveMeanSeaLevel=504
    ```

    Ten en cuenta que esto incluye los datos proporcionados por el archivo `station_list.csv`.

### Formulario SYNOP en wis2box-webapp

El módulo `synop2bufr` también se utiliza en el wis2box-webapp para convertir datos SYNOP FM-12 al formato BUFR utilizando un formulario de entrada basado en la web.
Para probar esto, ve a `http://YOUR-HOST/wis2box-webapp` e inicia sesión.

Selecciona el `Formulario SYNOP` del menú de la izquierda y copia y pega el contenido del archivo `synop_message.txt`:

```{.copy}
AAXX 21121
15015 02999 02501 10103 21090 39765 42952 57020 60001=
15020 02997 23104 10130 21075 30177 40377 58020 60001 81041=
15090 02997 53102 10139 21075 30271 40364 58031 60001 82046=
```

En el área de texto `Mensaje SYNOP`:

<img alt="synop-form" src="/../assets/img/wis2box-webapp-synop-form.png" width="800">

!!! question
    ¿Pudiste enviar el formulario? ¿Cuál es el resultado?

??? success "Haz clic para revelar la respuesta"

    Necesitas seleccionar un conjunto de datos y proporcionar el token para "processes/wis2box" que creaste en el ejercicio anterior para enviar el formulario.

    Si proporcionas un token no válido, verás:
    
    - Resultado: No autorizado, por favor proporciona un token 'processes/wis2box' válido

    Si proporcionas un token válido, verás "ADVERTENCIAS: 3". Haz clic en "ADVERTENCIAS" para abrir el desplegable que mostrará:

    - Estación 15015 no encontrada en el archivo de estaciones
    - Estación 15020 no encontrada en el archivo de estaciones
    - Estación 15090 no encontrada en el archivo de estaciones

    Para convertir estos datos al formato BUFR necesitarías configurar las estaciones correspondientes en tu wis2box y asegurarte de que las estaciones estén asociadas al tema de tu conjunto de datos.

!!! note

    En el ejercicio para [ingesting-data-for-publication](./ingesting-data-for-publication.md) ingresas el archivo "synop_202412030900.txt" y fue convertido al formato BUFR por el módulo synop2bufr.

    En el flujo de trabajo automatizado en el wis2box, el año y el mes se extraen automáticamente del nombre del archivo y se utilizan para completar los argumentos `--year` y `--month` requeridos por synop2bufr, mientras que los metadatos de la estación se extraen automáticamente de la configuración de la estación en el wis2box.

## Conversión de csv a BUFR

!!! note
    Asegúrate de seguir conectado en el contenedor wis2box-api y en el directorio `/root/data-conversion-exercises`, si saliste del contenedor en el ejercicio anterior, puedes volver a iniciar sesión de la siguiente manera:

    ```bash
    cd ~/wis2box
    python3 wis2box-ctl.py login wis2box-api
    cd /root/data-conversion-exercises
    ```

Ahora veamos cómo convertir datos CSV al formato BUFR utilizando el módulo `csv2bufr`. El módulo está instalado en el contenedor wis2box-api y se puede usar desde la línea de comandos de la siguiente manera:

```{.copy}
csv2bufr data transform \
    --bufr-template <bufr-mapping-template> \
    <input-csv-file>
```

El argumento `--bufr-template` se utiliza para especificar el archivo de plantilla de mapeo BUFR, que proporciona el mapeo entre los datos CSV de entrada y los datos BUFR de salida especificados en un archivo JSON. Las plantillas de mapeo predeterminadas están instaladas en el directorio `/opt/csv2bufr/templates` en el contenedor wis2box-api.

### revisar el archivo CSV de ejemplo

Revisa el contenido del archivo CSV de ejemplo `aws-example.csv`:

```bash
more aws-example.csv
```

!!! question
    ¿Cuántas filas de datos hay en el archivo CSV? ¿Cuál es el identificador de estación WIGOS de las estaciones que informan en el archivo CSV?

??? question "Haz clic para revelar la respuesta"

    La salida muestra lo siguiente:

    ```{.copy}
    wsi_series,wsi_issuer,wsi_issue_number,wsi_local,wmo_block_number,wmo_station_number,station_type,year,month,day,hour,minute,latitude,longitude,station_height_above_msl,barometer_height_above_msl,station_pressure,msl_pressure,geopotential_height,thermometer_height,air_temperature,dewpoint_temperature,relative_humidity,method_of_ground_state_measurement,ground_state,method_of_snow_depth_measurement,snow_depth,precipitation_intensity,anemometer_height,time_period_of_wind,wind_direction,wind_speed,maximum_wind_gust_direction_10_minutes,maximum_wind_gust_speed_10_minutes,maximum_wind_gust_direction_1_hour,maximum_wind_gust_speed_1_hour,maximum_wind_gust_direction_3_hours,maximum_wind_gust_speed_3_hours,rain_sensor_height,total_precipitation_1_hour,total_precipitation_3_hours,total_precipitation_6_hours,total_precipitation_12_hours,total_precipitation_24_hours
    0,20000,0,60355,60,355,1,2024,3,31,1,0,47.77706163,23.94046026,503,504.43,100940,101040,1448,5,298.15,294.55,80,3,1,1,0,0.004,10,-10,30,3,30,5,40,9,20,11,2,4.7,5.3,7.9,9.5,11.4
    0,20000,0,60355,60,355,1,2024,3,31,2,0,47.77706163,23.94046026,503,504.43,100940,101040,1448,5,25.,294.55,80,3,1,1,0,0.004,10,-10,30,3,30,5,40,9,20,11,2,4.7,5.3,7.9,9.5,11.4
    0,20000,0,60355,60,355,1,2024,3,31,3,0,47.77706163,23.94046026,503,504.43,100940,101040,1448,5,298.15,294.55,80,3,1,1,0,0.004,10,-10,30,3,30,5,40,9,20,11,2,4.7,5.3,7.9,9.5,11.4
    ```

    La primera fila del archivo CSV contiene los encabezados de las columnas, que se utilizan para identificar los datos en cada columna.

    Después de la fila de encabezados, hay 3 filas de datos, que representan 3 observaciones meteorológicas de la misma estación con el identificador de estación WIGOS `0-20000-0-60355` en tres marcas de tiempo diferentes `2024-03-31 01:00:00`, `2024-03-31 02:00:00`, y `2024-03-31 03:00:00`.

### revisar la plantilla aws

El wis2box-api incluye un conjunto de plantillas de mapeo BUFR predefinidas que están instaladas en el directorio `/opt/csv2bufr/templates`.

Revisa el contenido del directorio `/opt/csv2bufr/templates`:

```bash
ls /opt/csv2bufr/templates
```
Deberías ver la siguiente salida:

```{.copy}
CampbellAfrica-v1-template.json  aws-template.json  daycli-template.json
```

Revisemos el contenido del archivo `aws-template.json`:

```bash
cat /opt/csv2bufr/templates/aws-template.json
```

Esto devuelve un archivo JSON grande, proporcionando el mapeo para 43 columnas CSV.

!!! question
    ¿A qué clave de eccodes está mapeada la columna CSV `airTemperature`? ¿Cuáles son los valores mínimos y máximos válidos para esta clave?

??? success "Haz clic para revelar la respuesta"

    Usando el siguiente comando para filtrar la salida:

    ```bash
    cat /opt/csv2bufr/templates/aws-template.json | grep -i airTemperature
    ```
    Deberías ver la siguiente salida:

    ```{.copy}
    {"eccodes_key": "#1#airTemperature", "value": "data:air_temperature", "valid_min": "const:193.15", "valid_max": "const:333.15"},
    ```

    El valor que se codificará para la clave de eccodes `airTemperature` se tomará de los datos en la columna CSV: **air_temperature**.

    Los valores mínimos y máximos para esta clave son `193.15` y `333.15`, respectivamente.

!!! question

    ¿A qué clave de eccodes está mapeada la columna CSV `internationalDataSubCategory`? ¿Cuál es el valor de esta clave?

??? success "Haz clic para revelar la respuesta"
    Usando el siguiente comando para filtrar la salida:

    ```bash
    cat /opt/csv2bufr/templates/aws-template.json | grep -i internationalDataSubCategory
    ```
    Deberías ver la siguiente salida:

    ```{.copy}
    {"eccodes_key": "internationalDataSubCategory", "value": "const:2"},
    ```

    **No hay ninguna columna CSV mapeada a la clave de eccodes `internationalDataSubCategory`**, en su lugar se utiliza el valor constante 2 y se codificará en todos los archivos BUFR producidos con esta plantilla de mapeo.

### convertir CSV a BUFR

Intentemos convertir el archivo al formato BUFR usando el comando `csv2bufr`:

```{.copy}
csv2bufr data transform --bufr-template aws-template ./aws-example.csv
```

!!! question
    ¿Cuántos archivos BUFR se crearon?

??? success "Haz clic para revelar la respuesta"

    La salida muestra lo siguiente:

    ```{.copy}
    CLI:    ... Transformando ./aws-example.csv a BUFR ...
    CLI:    ... Procesando subconjuntos:
    CLI:    ..... 384 bytes escritos en ./WIGOS_0-20000-0-60355_20240331T010000.bufr4
    #1#airTemperature: Valor (25.0) fuera del rango válido (193.15 - 333.15).; Elemento establecido como ausente
    CLI:    ..... 384 bytes escritos en ./WIGOS_0-20000-0-60355_20240331T020000.bufr4
    CLI:    ..... 384 bytes escritos en ./WIGOS_0-20000-0-60355_20240331T030000.bufr4
    CLI:    Fin del procesamiento, saliendo.
    ```

    La salida indica que se crearon 3 archivos BUFR: `WIGOS_0-20000-0-60355_20240331T010000.bufr4`, `WIGOS_0-20000-0-60355_20240331T020000.bufr4`, y `WIGOS_0-20000-0-60355_20240331T030000.bufr4`.

Para verificar el contenido de los archivos BUFR mientras se ignoran los valores ausentes, puedes usar el siguiente comando:

```bash
bufr_dump -p WIGOS_0-20000-0-60355_20240331T010000.bufr4 | grep -v MISSING
```

!!! question
    ¿Cuál es el valor de la clave de eccodes `airTemperature` en el archivo BUFR `WIGOS_0-20000-0-60355_20240331T010000.bufr4`? ¿Y en el archivo BUFR `WIGOS_0-20000-0-60355_20240331T020000.bufr4`?

??? success "Haz clic para revelar la respuesta"
    Para filtrar la salida, puedes usar el siguiente comando:

    ```bash
    bufr_dump -p WIGOS_0-20000-0-60355_20240331T010000.bufr4 | grep -v MISSING | grep airTemperature
    ```
    Deberías ver la siguiente salida:

    ```{.copy}
    #1#airTemperature=298.15
    ```

    Mientras que para el segundo archivo:

    ```bash
    bufr_dump -p WIGOS_0-20000-0-60355_20240331T020000.bufr4 | grep -v MISSING | grep airTemperature
    ```

No obtienes ningún resultado, lo que indica que falta el valor para la clave `airTemperature` en el archivo BUFR `WIGOS_0-20000-0-60355_20240331T020000.bufr4`. El csv2bufr se negó a codificar el valor `25.0` de los datos CSV ya que está fuera del rango válido de `193.15` y `333.15` como se define en la plantilla de mapeo.

Ten en cuenta que convertir CSV a BUFR usando una de las plantillas de mapeo BUFR predefinidas tiene limitaciones:

- el archivo CSV debe estar en el formato definido en la plantilla de mapeo, es decir, los nombres de las columnas CSV deben coincidir con los nombres definidos en la plantilla de mapeo
- solo puedes codificar las claves definidas en la plantilla de mapeo
- los controles de calidad están limitados a los controles definidos en la plantilla de mapeo

Para información sobre cómo crear y usar plantillas de mapeo BUFR personalizadas, consulta el siguiente ejercicio práctico [csv2bufr-templates](./csv2bufr-templates.md).

## Conclusión

!!! success "¡Felicidades!"
    En esta sesión práctica has aprendido:

    - cómo acceder a las herramientas de línea de comandos de ecCodes dentro del contenedor de wis2box-api
    - cómo usar `synop2bufr` para convertir informes SYNOP FM-12 a BUFR desde la línea de comandos
    - cómo usar el Formulario SYNOP en el wis2box-webapp para convertir informes SYNOP FM-12 a BUFR
    - cómo usar `csv2bufr` para convertir datos CSV a BUFR desde la línea de comandos
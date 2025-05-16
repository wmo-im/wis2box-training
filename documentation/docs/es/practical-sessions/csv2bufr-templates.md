---
title: Plantillas de mapeo de CSV a BUFR
---

# Plantillas de mapeo de CSV a BUFR

!!! abstract "Resultados de aprendizaje"
    Al final de esta sesión práctica, podrás:

    - crear una nueva plantilla de mapeo BUFR para tus datos CSV
    - editar y depurar tu plantilla de mapeo BUFR personalizada desde la línea de comandos
    - configurar el complemento de datos CSV a BUFR para usar una plantilla de mapeo BUFR personalizada
    - usar las plantillas integradas de AWS y DAYCLI para convertir datos CSV a BUFR

## Introducción

Los archivos de datos en valores separados por comas (CSV) se utilizan a menudo para registrar datos observacionales y otros datos en un formato tabular.
La mayoría de los registradores de datos utilizados para registrar la salida de sensores pueden exportar las observaciones en archivos delimitados, incluyendo en CSV.
De manera similar, cuando los datos se ingieren en una base de datos, es fácil exportar los datos requeridos en archivos formateados CSV.

El módulo csv2bufr de wis2box proporciona una herramienta de línea de comandos para convertir datos CSV a formato BUFR. Al usar csv2bufr necesitas proporcionar una plantilla de mapeo BUFR que mapee las columnas CSV a los elementos BUFR correspondientes. Si no deseas crear tu propia plantilla de mapeo, puedes usar las plantillas integradas de AWS y DAYCLI para convertir datos CSV a BUFR, pero necesitarás asegurarte de que los datos CSV que estás usando están en el formato correcto para estas plantillas. Si deseas decodificar parámetros que no están incluidos en las plantillas de AWS y DAYCLI, necesitarás crear tu propia plantilla de mapeo.

En esta sesión aprenderás cómo crear tu propia plantilla de mapeo para convertir datos CSV a BUFR. También aprenderás cómo usar las plantillas integradas de AWS y DAYCLI para convertir datos CSV a BUFR.

## Preparación

Asegúrate de que el wis2box-stack ha sido iniciado con `python3 wis2box.py start`

Asegúrate de que tienes un navegador web abierto con la interfaz de usuario de MinIO para tu instancia accediendo a `http://YOUR-HOST:9000`
Si no recuerdas tus credenciales de MinIO, puedes encontrarlas en el archivo `wis2box.env` en el directorio `wis2box` en tu VM de estudiante.

Asegúrate de que tienes MQTT Explorer abierto y conectado a tu broker usando las credenciales `everyone/everyone`.

## Creando una plantilla de mapeo

El módulo csv2bufr viene con una herramienta de línea de comandos para crear tu propia plantilla de mapeo usando un conjunto de secuencias BUFR y/o elemento BUFR como entrada.

Para encontrar secuencias BUFR y elementos específicos puedes referirte a las tablas BUFR en [https://confluence.ecmwf.int/display/ECC/BUFR+tables](https://confluence.ecmwf.int/display/ECC/BUFR+tables).

### Herramienta de línea de comandos csv2bufr mappings

Para acceder a la herramienta de línea de comandos csv2bufr, necesitas iniciar sesión en el contenedor wis2box-api:

```bash
cd ~/wis2box
python3 wis2box-ctl.py login wis2box-api
```

Para imprimir la página de ayuda para el comando `csv2bufr mapping`:

```bash
csv2bufr mappings --help
```

La página de ayuda muestra 2 subcomandos:

- `csv2bufr mappings create` : Crear una nueva plantilla de mapeo
- `csv2bufr mappings list` : Listar las plantillas de mapeo disponibles en el sistema

!!! Note "csv2bufr mapping list"

    El comando `csv2bufr mapping list` te mostrará las plantillas de mapeo disponibles en el sistema.
    Las plantillas predeterminadas están almacenadas en el directorio `/opt/wis2box/csv2bufr/templates` en el contenedor.

    Para compartir plantillas de mapeo personalizadas con el sistema puedes almacenarlas en el directorio definido por `$CSV2BUFR_TEMPLATES`, que está configurado por defecto en `/data/wis2box/mappings` en el contenedor. Dado que el directorio `/data/wis2box/mappings` en el contenedor está montado en el directorio `$WIS2BOX_HOST_DATADIR/mappings` en el host, encontrarás tus plantillas de mapeo personalizadas en el directorio `$WIS2BOX_HOST_DATADIR/mappings` en el host.

Intentemos crear una nueva plantilla de mapeo personalizada usando el comando `csv2bufr mapping create` usando como entrada la secuencia BUFR 301150 más el elemento BUFR 012101.

```bash
csv2bufr mappings create 301150 012101 --output /data/wis2box/mappings/my_custom_template.json
```

Puedes verificar el contenido de la plantilla de mapeo que acabas de crear usando el comando `cat`:

```bash
cat /data/wis2box/mappings/my_custom_template.json
```

!!! question "Inspección de la plantilla de mapeo"

    ¿Cuántas columnas CSV están siendo mapeadas a elementos BUFR? ¿Cuál es el encabezado CSV para cada elemento BUFR mapeado?

??? success "Haz clic para revelar la respuesta"
    
    La plantilla de mapeo que creaste mapea **5** columnas CSV a elementos BUFR, específicamente los 4 elementos BUFR en la secuencia 301150 más el elemento BUFR 012101. 

    Las siguientes columnas CSV están siendo mapeadas a elementos BUFR:

    - **wigosIdentifierSeries** se mapea a `"eccodes_key": "#1#wigosIdentifierSeries"` (elemento BUFR 001125)
    - **wigosIssuerOfIdentifier** se mapea a `"eccodes_key": "#1#wigosIssuerOfIdentifier` (elemento BUFR 001126)
    - **wigosIssueNumber** se mapea a `"eccodes_key": "#1#wigosIssueNumber"` (elemento BUFR 001127)
    - **wigosLocalIdentifierCharacter** se mapea a `"eccodes_key": "#1#wigosLocalIdentifierCharacter"` (elemento BUFR 001128)
    - **airTemperature** se mapea a `"eccodes_key": "#1#airTemperature"` (elemento BUFR 012101)

La plantilla de mapeo que creaste omite información importante sobre la observación que se realizó, la fecha y hora de la observación, y la latitud y longitud de la estación.

A continuación, actualizaremos la plantilla de mapeo y añadiremos las siguientes secuencias:
    
- **301011** para Fecha (Año, mes, día)
- **301012** para Hora (Hora, minuto)
- **301023** para Ubicación (Latitud/longitud (precisión gruesa))

Y los siguientes elementos:

- **010004** para Presión
- **007031** para Altura del barómetro sobre el nivel medio del mar

Ejecuta el siguiente comando para actualizar la plantilla de mapeo:

```bash
csv2bufr mappings create 301150 301011 301012 301023 007031 012101 010004  --output /data/wis2box/mappings/my_custom_template.json
```

E inspecciona el contenido de la plantilla de mapeo nuevamente:

```bash
cat /data/wis2box/mappings/my_custom_template.json
```

!!! question "Inspección de la plantilla de mapeo actualizada"

    ¿Cuántas columnas CSV están ahora siendo mapeadas a elementos BUFR? ¿Cuál es el encabezado CSV para cada elemento BUFR mapeado?

??? success "Haz clic para revelar la respuesta"
    
    La plantilla de mapeo que creaste ahora mapea **18** columnas CSV a elementos BUFR:
    - 4 elementos BUFR de la secuencia BUFR 301150
    - 3 elementos BUFR de la secuencia BUFR 301011
    - 2 elementos BUFR de la secuencia BUFR 301012
    - 2 elementos BUFR de la secuencia BUFR 301023
    - Elemento BUFR 007031
    - Elemento BUFR 012101

    Las siguientes columnas CSV están siendo mapeadas a elementos BUFR:

    - **wigosIdentifierSeries** se mapea a `"eccodes_key": "#1#wigosIdentifierSeries"` (elemento BUFR 001125)
    - **wigosIssuerOfIdentifier** se mapea a `"eccodes_key": "#1#wigosIssuerOfIdentifier` (elemento BUFR 001126)
    - **wigosIssueNumber** se mapea a `"eccodes_key": "#1#wigosIssueNumber"` (elemento BUFR 001127)
    - **wigosLocalIdentifierCharacter** se mapea a `"eccodes_key": "#1#wigosLocalIdentifierCharacter"` (elemento BUFR 001128)
    - **year** se mapea a `"eccodes_key": "#1#year"` (elemento BUFR 004001)
    - **month** se mapea a `"eccodes_key": "#1#month"` (elemento BUFR 004002)
    - **day** se mapea a `"eccodes_key": "#1#day"` (elemento BUFR 004003)
    - **hour** se mapea a `"eccodes_key": "#1#hour"` (elemento BUFR 004004)
    - **minute** se mapea a `"eccodes_key": "#1#minute"` (elemento BUFR 004005)
    - **latitude** se mapea a `"eccodes_key": "#1#latitude"` (elemento BUFR 005002)
    - **longitude** se mapea a `"eccodes_key": "#1#longitude"` (elemento BUFR 006002)
    - **heightOfBarometerAboveMeanSeaLevel"** se mapea a `"eccodes_key": "#1#heightOfBarometerAboveMeanSeaLevel"` (elemento BUFR 007031)
    - **airTemperature** se mapea a `"eccodes_key": "#1#airTemperature"` (elemento BUFR 012101)
    - **nonCoordinatePressure** se mapea a `"eccodes_key": "#1#nonCoordinatePressure"` (elemento BUFR 010004)

Revisa el contenido del archivo `custom_template_data.csv` en el directorio `/root/data-conversion-exercises`:

```bash
cat /root/data-conversion-exercises/custom_template_data.csv
```

Nota que los encabezados de este archivo CSV son los mismos que los encabezados CSV en la plantilla de mapeo que creaste.

Para probar la conversión de datos podemos usar la herramienta de línea de comandos `csv2bufr` para convertir el archivo CSV a BUFR usando la plantilla de mapeo que creamos:

```bash
csv2bufr data transform --bufr-template my_custom_template /root/data-conversion-exercises/custom_template_data.csv
```

Deberías ver la siguiente salida:

```bash
CLI:    ... Transformando /root/data-conversion-exercises/custom_template_data.csv a BUFR ...
CLI:    ... Procesando subconjuntos:
CLI:    ..... 94 bytes escritos en ./WIGOS_0-20000-0-15015_20250412T210000.bufr4
CLI:    Fin del procesamiento, saliendo.
```

!!! question "Verificar el contenido del archivo BUFR"
    
    ¿Cómo puedes verificar el contenido del archivo BUFR que acabas de crear y verificar que ha codificado los datos correctamente?

??? success "Haz clic para revelar la respuesta"

    Puedes usar el comando `bufr_dump -p` para verificar el contenido del archivo BUFR que acabas de crear.
    El comando te mostrará el contenido del archivo BUFR en un formato legible por humanos.

    ```bash
    bufr_dump -p ./WIGOS_0-20000-0-15015_20250412T210000.bufr4
    ```

    En la salida verás valores para los elementos BUFR que mapeaste en la plantilla, por ejemplo, la "airTemperature" mostrará:
    
    ```bash
    airTemperature=298.15
    ```

Ahora puedes salir del contenedor:

```bash
exit
```

### Usando la plantilla de mapeo en el wis2box

Para asegurar que la nueva plantilla de mapeo sea reconocida por el contenedor wis2box-api, necesitas reiniciar el contenedor:

```bash
docker restart wis2box-api
```

Ahora puedes configurar tu conjunto de datos en el wis2box-webapp para usar la plantilla de mapeo personalizada para el complemento de conversión de CSV a BUFR.

El wis2box-webapp detectará automáticamente la plantilla de mapeo que creaste y la hará disponible en la lista de plantillas para el complemento de conversión de CSV a BUFR.

Haz clic en el conjunto de datos que creaste en la sesión práctica anterior y haz clic en "ACTUALIZAR" junto al complemento con el nombre "Datos CSV convertidos a BUFR":

<img alt="Imagen que muestra el editor de conjuntos de datos en el wis2box-webapp" src="/../assets/img/wis2box-webapp-data-mapping-update-csv2bufr.png"/>

Deberías ver la nueva plantilla que creaste en la lista de plantillas disponibles:

<img alt="Imagen que muestra las plantillas csv2bufr en el wis2box-webapp" src="/../assets/img/wis2box-webapp-csv2bufr-templates.png"/>

!!! hint

    Ten en cuenta que si no ves la nueva plantilla que creaste, intenta actualizar la página o abrirla en una ventana de incógnito nueva.

Por ahora, mantén la selección predeterminada de la plantilla AWS (haz clic en la parte superior derecha para cerrar la configuración del complemento).

## Usando la plantilla 'AWS'

La plantilla 'AWS' proporciona una plantilla de mapeo para convertir datos CSV a la secuencia BUFR 301150, 307096, en apoyo de los requisitos mínimos de GBON.

La descripción de la plantilla AWS se puede encontrar aquí [aws-template](./../csv2bufr-templates/aws-template.md).

### Revisar los datos de entrada de ejemplo de aws

Descarga el ejemplo para este ejercicio desde el siguiente enlace:

[aws-example.csv](./../../sample-data/aws-example.csv)

Abre el archivo que descargaste en un editor e inspecciona el contenido:

!!! question
    Examinando la fecha, la hora y los campos de identificación (identificadores WIGOS y tradicionales) ¿qué
    notas? ¿Cómo se representaría la fecha de hoy?

??? success "Haz clic para revelar la respuesta"
    Cada columna contiene una sola pieza de información. Por ejemplo, la fecha se divide en
    año, mes y día, reflejando cómo se almacenan los datos en BUFR. La fecha de hoy se dividiría
    en las columnas "año", "mes" y "día". De manera similar, la hora necesita dividirse en "hora" y "minuto" y el identificador de la estación WIGOS en sus respectivos componentes.

!!! question
    Mirando el archivo de datos, ¿cómo se codifican los datos faltantes?
    
??? success "Haz clic para revelar la respuesta"
    Los datos faltantes dentro del archivo están representados por celdas vacías. En un archivo CSV esto se codificaría como ``,,``. Ten en cuenta que esto es una celda vacía y no se codifica como una cadena de longitud cero, 
    por ejemplo, ``,"",``.

!!! hint "Datos faltantes"
    Se reconoce que los datos pueden faltar por diversas razones, ya sea debido a fallos en los sensores o a que el parámetro no se observó. En estos casos, los datos faltantes pueden codificarse según la respuesta anterior, los demás datos en el informe siguen siendo válidos.

### Actualiza el archivo de ejemplo

Actualiza el archivo de ejemplo que descargaste para usar la fecha y hora de hoy y cambia los identificadores de estación WIGOS para usar estaciones que hayas registrado en la `wis2box-webapp`.

### Sube los datos a MinIO y verifica el resultado

Navega a la interfaz de usuario de MinIO e inicia sesión usando las credenciales del archivo `wis2box.env`.

Navega al **wis2box-incoming** y haz clic en el botón "Crear nueva ruta":

<img alt="Image showing MinIO UI with the create folder button highlighted" src="/../assets/img/minio-create-new-path.png"/>

Crea una nueva carpeta en el bucket de MinIO que coincida con el dataset-id para el conjunto de datos que creaste con el template='weather/surface-weather-observations/synop':

<img alt="Image showing MinIO UI with the create folder button highlighted" src="/../assets/img/minio-create-new-path-metadata_id.png"/>

Sube el archivo de ejemplo que descargaste a la carpeta que creaste en el bucket de MinIO:

<img alt="Image showing MinIO UI with aws-example uploaded" src="/../assets/img/minio-upload-aws-example.png"/>

Verifica el tablero de Grafana en `http://YOUR-HOST:3000` para ver si hay algún WARNING o ERROR. Si ves alguno, intenta solucionarlo y repite el ejercicio.

Revisa el MQTT Explorer para ver si recibes notificaciones de datos WIS2.

Si la ingestión de datos fue exitosa, deberías ver 3 notificaciones en MQTT Explorer en el tema `origin/a/wis2/<centre-id>/data/weather/surface-weather-observations/synop` para las 3 estaciones de las que reportaste datos:

<img width="450" alt="Image showing MQTT explorer after uploading AWS" src="/../assets/img/mqtt-explorer-aws-upload.png"/>

## Usando la plantilla 'DayCLI'

La plantilla **DayCLI** proporciona una plantilla de mapeo para convertir datos diarios de clima en CSV a la secuencia BUFR 307075, en apoyo del reporte de datos climáticos diarios.

La descripción de la plantilla DAYCLI se puede encontrar aquí [daycli-template](./../csv2bufr-templates/daycli-template.md).

Para compartir estos datos en WIS2 necesitarás crear un nuevo conjunto de datos en la `wis2box-webapp` que tenga la Jerarquía de Temas WIS2 correcta y que use la plantilla DAYCLI para convertir datos CSV a BUFR.

### Creando un conjunto de datos wis2box para publicar mensajes DAYCLI

Ve al editor de conjuntos de datos en la `wis2box-webapp` y crea un nuevo conjunto de datos. Usa el mismo centre-id que en las sesiones prácticas anteriores y selecciona **Data Type='climate/surface-based-observations/daily'**:

<img alt="Create a new dataset in the wis2box-webapp for DAYCLI" src="/../assets/img/wis2box-webapp-create-dataset-daycli.png"/>

Haz clic en "CONTINUE TO FORM" y añade una descripción para tu conjunto de datos, establece el cuadro delimitador y proporciona la información de contacto para el conjunto de datos. Una vez que hayas completado todas las secciones, haz clic en 'VALIDATE FORM' y revisa el formulario.

Revisa los plugins de datos para los conjuntos de datos. Haz clic en "UPDATE" junto al plugin con nombre "CSV data converted to BUFR" y verás que la plantilla está configurada para **DayCLI**:

<img alt="Update the data plugin for the dataset to use the DAYCLI template" src="/../assets/img/wis2box-webapp-update-data-plugin-daycli.png"/>

Cierra la configuración del plugin y envía el formulario usando el token de autenticación que creaste en la sesión práctica anterior.

Ahora deberías tener un segundo conjunto de datos en la `wis2box-webapp` que está configurado para usar la plantilla DAYCLI para convertir datos CSV a BUFR.

### Revisar los datos de entrada del ejemplo daycli

Descarga el ejemplo para este ejercicio desde el siguiente enlace:

[daycli-example.csv](./../../sample-data/daycli-example.csv)

Abre el archivo que descargaste en un editor e inspecciona el contenido:

!!! question
    ¿Qué variables adicionales se incluyen en la plantilla daycli?

??? success "Haz clic para revelar la respuesta"
    La plantilla daycli incluye metadatos importantes sobre la ubicación del instrumento y las clasificaciones de calidad de la medición para temperatura y humedad, banderas de control de calidad e información sobre cómo se ha calculado la temperatura media diaria.

### Actualiza el archivo de ejemplo

El archivo de ejemplo contiene una fila de datos para cada día en un mes, y reporta datos para una estación. Actualiza el archivo de ejemplo que descargaste para usar la fecha y hora de hoy y cambia los identificadores de estación WIGOS para usar una estación que hayas registrado en la `wis2box-webapp`.

### Sube los datos a MinIO y verifica el resultado

Como antes, necesitarás subir los datos al bucket 'wis2box-incoming' en MinIO para ser procesados por el convertidor csv2bufr. Esta vez necesitarás crear una nueva carpeta en el bucket de MinIO que coincida con el dataset-id para el conjunto de datos que creaste con el template='climate/surface-based-observations/daily' que será diferente del dataset-id que usaste en el ejercicio anterior:

<img alt="Image showing MinIO UI with DAYCLI-example uploaded" src="/../assets/img/minio-upload-daycli-example.png"/>

Después de subir los datos verifica que no haya WARNINGS o ERRORS en el tablero de Grafana y revisa el MQTT Explorer para ver si recibes notificaciones de datos WIS2.

Si la ingestión de datos fue exitosa, deberías ver 30 notificaciones en MQTT Explorer en el tema `origin/a/wis2/<centre-id>/data/climate/surface-based-observations/daily` para los 30 días del mes que reportaste datos para:

<img width="450" alt="Image showing MQTT explorer after uploading DAYCLI" src="/../assets/img/mqtt-daycli-template-success.png"/>

## Conclusión

!!! success "Felicidades"
    En esta sesión práctica has aprendido:

    - cómo crear una plantilla de mapeo personalizada para convertir datos CSV a BUFR
    - cómo usar las plantillas integradas de AWS y DAYCLI para convertir datos CSV a BUFR
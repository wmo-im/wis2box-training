---
title: Plantillas de mapeo de CSV a BUFR
---

# Plantillas de mapeo de CSV a BUFR

!!! abstract "Resultados de aprendizaje"
    Al final de esta sesión práctica, podrás:

    - crear una nueva plantilla de mapeo BUFR para tus datos CSV
    - editar y depurar tu plantilla de mapeo BUFR personalizada desde la línea de comandos
    - configurar el complemento de datos CSV a BUFR para usar una plantilla de mapeo BUFR personalizada
    - usar las plantillas integradas AWS y DAYCLI para convertir datos CSV a BUFR

## Introducción

Los archivos de datos con valores separados por comas (CSV) se utilizan frecuentemente para registrar datos observacionales y otros datos en un formato tabular. 
La mayoría de los registradores de datos utilizados para registrar la salida de sensores pueden exportar las observaciones en archivos delimitados, incluidos los CSV.
De manera similar, cuando los datos se ingresan en una base de datos, es fácil exportar los datos requeridos en archivos con formato CSV.

El módulo wis2box csv2bufr proporciona una herramienta de línea de comandos para convertir datos CSV al formato BUFR. Al usar csv2bufr, necesitas proporcionar una plantilla de mapeo BUFR que asigne las columnas del CSV a los elementos correspondientes de BUFR. Si no deseas crear tu propia plantilla de mapeo, puedes usar las plantillas integradas AWS y DAYCLI para convertir datos CSV a BUFR, pero deberás asegurarte de que los datos CSV que estás utilizando estén en el formato correcto para estas plantillas. Si deseas decodificar parámetros que no están incluidos en las plantillas AWS y DAYCLI, necesitarás crear tu propia plantilla de mapeo.

En esta sesión aprenderás cómo crear tu propia plantilla de mapeo para convertir datos CSV a BUFR. También aprenderás cómo usar las plantillas integradas AWS y DAYCLI para convertir datos CSV a BUFR.

## Preparación

Asegúrate de que el wis2box-stack se haya iniciado con `python3 wis2box.py start`.

Asegúrate de que tienes un navegador web abierto con la interfaz de usuario de MinIO para tu instancia accediendo a `http://YOUR-HOST:9000`.
Si no recuerdas tus credenciales de MinIO, puedes encontrarlas en el archivo `wis2box.env` en el directorio `wis2box` de tu máquina virtual de estudiante.

Asegúrate de que tienes MQTT Explorer abierto y conectado a tu broker usando las credenciales `everyone/everyone`.

## Creación de una plantilla de mapeo

El módulo csv2bufr incluye una herramienta de línea de comandos para crear tu propia plantilla de mapeo utilizando un conjunto de secuencias BUFR y/o elementos BUFR como entrada.

Para encontrar secuencias y elementos BUFR específicos, puedes consultar las tablas BUFR en [https://confluence.ecmwf.int/display/ECC/BUFR+tables](https://confluence.ecmwf.int/display/ECC/BUFR+tables).

### Herramienta de línea de comandos csv2bufr mappings

Para acceder a la herramienta de línea de comandos csv2bufr, necesitas iniciar sesión en el contenedor wis2box-api:

```bash
cd ~/wis2box
python3 wis2box-ctl.py login wis2box-api
```

Para imprimir la página de ayuda del comando `csv2bufr mapping`:

```bash
csv2bufr mappings --help
```

La página de ayuda muestra dos subcomandos:

- `csv2bufr mappings create` : Crear una nueva plantilla de mapeo
- `csv2bufr mappings list` : Listar las plantillas de mapeo disponibles en el sistema

!!! Note "csv2bufr mapping list"

    El comando `csv2bufr mapping list` mostrará las plantillas de mapeo disponibles en el sistema. 
    Las plantillas predeterminadas se almacenan en el directorio `/opt/wis2box/csv2bufr/templates` dentro del contenedor.

    Para compartir plantillas de mapeo personalizadas con el sistema, puedes almacenarlas en el directorio definido por `$CSV2BUFR_TEMPLATES`, que está configurado como `/data/wis2box/mappings` de forma predeterminada en el contenedor. Dado que el directorio `/data/wis2box/mappings` en el contenedor está montado en el directorio `$WIS2BOX_HOST_DATADIR/mappings` en el host, encontrarás tus plantillas de mapeo personalizadas en el directorio `$WIS2BOX_HOST_DATADIR/mappings` en el host.

Intentemos crear una nueva plantilla de mapeo personalizada utilizando el comando `csv2bufr mapping create` con la secuencia BUFR 301150 más el elemento BUFR 012101 como entrada.

```bash
csv2bufr mappings create 301150 012101 --output /data/wis2box/mappings/my_custom_template.json
```

Puedes verificar el contenido de la plantilla de mapeo que acabas de crear utilizando el comando `cat`:

```bash
cat /data/wis2box/mappings/my_custom_template.json
```

!!! question "Inspección de la plantilla de mapeo"

    ¿Cuántas columnas CSV están siendo asignadas a elementos BUFR? ¿Cuál es el encabezado CSV para cada elemento BUFR asignado?

??? success "Haz clic para revelar la respuesta"
    
    La plantilla de mapeo que creaste asigna **5** columnas CSV a elementos BUFR, específicamente los 4 elementos BUFR en la secuencia 301150 más el elemento BUFR 012101.

    Las siguientes columnas CSV están siendo asignadas a elementos BUFR:

    - **wigosIdentifierSeries** se asigna a `"eccodes_key": "#1#wigosIdentifierSeries"` (elemento BUFR 001125)
    - **wigosIssuerOfIdentifier** se asigna a `"eccodes_key": "#1#wigosIssuerOfIdentifier` (elemento BUFR 001126)
    - **wigosIssueNumber** se asigna a `"eccodes_key": "#1#wigosIssueNumber"` (elemento BUFR 001127)
    - **wigosLocalIdentifierCharacter** se asigna a `"eccodes_key": "#1#wigosLocalIdentifierCharacter"` (elemento BUFR 001128)
    - **airTemperature** se asigna a `"eccodes_key": "#1#airTemperature"` (elemento BUFR 012101)

La plantilla de mapeo que creaste carece de metadatos importantes sobre la observación realizada, la fecha y hora de la observación, y la latitud y longitud de la estación.

A continuación, actualizaremos la plantilla de mapeo y añadiremos las siguientes secuencias:
    
- **301011** para Fecha (Año, mes, día)
- **301012** para Hora (Hora, minuto)
- **301023** para Ubicación (Latitud/longitud (precisión aproximada))

Y los siguientes elementos:

- **010004** para Presión
- **007031** para Altura del barómetro sobre el nivel medio del mar

Ejecuta el siguiente comando para actualizar la plantilla de mapeo:

```bash
csv2bufr mappings create 301150 301011 301012 301023 007031 012101 010004  --output /data/wis2box/mappings/my_custom_template.json
```

Y vuelve a inspeccionar el contenido de la plantilla de mapeo:

```bash
cat /data/wis2box/mappings/my_custom_template.json
```

!!! question "Inspección de la plantilla de mapeo actualizada"

    ¿Cuántas columnas CSV están siendo asignadas ahora a elementos BUFR? ¿Cuál es el encabezado CSV para cada elemento BUFR asignado?

??? success "Haz clic para revelar la respuesta"
    
    La plantilla de mapeo que creaste ahora asigna **18** columnas CSV a elementos BUFR:
    - 4 elementos BUFR de la secuencia BUFR 301150
    - 3 elementos BUFR de la secuencia BUFR 301011
    - 2 elementos BUFR de la secuencia BUFR 301012
    - 2 elementos BUFR de la secuencia BUFR 301023
    - Elemento BUFR 007031
    - Elemento BUFR 012101

    Las siguientes columnas CSV están siendo asignadas a elementos BUFR:

    - **wigosIdentifierSeries** se asigna a `"eccodes_key": "#1#wigosIdentifierSeries"` (elemento BUFR 001125)
    - **wigosIssuerOfIdentifier** se asigna a `"eccodes_key": "#1#wigosIssuerOfIdentifier` (elemento BUFR 001126)
    - **wigosIssueNumber** se asigna a `"eccodes_key": "#1#wigosIssueNumber"` (elemento BUFR 001127)
    - **wigosLocalIdentifierCharacter** se asigna a `"eccodes_key": "#1#wigosLocalIdentifierCharacter"` (elemento BUFR 001128)
    - **year** se asigna a `"eccodes_key": "#1#year"` (elemento BUFR 004001)
    - **month** se asigna a `"eccodes_key": "#1#month"` (elemento BUFR 004002)
    - **day** se asigna a `"eccodes_key": "#1#day"` (elemento BUFR 004003)
    - **hour** se asigna a `"eccodes_key": "#1#hour"` (elemento BUFR 004004)
    - **minute** se asigna a `"eccodes_key": "#1#minute"` (elemento BUFR 004005)
    - **latitude** se asigna a `"eccodes_key": "#1#latitude"` (elemento BUFR 005002)
    - **longitude** se asigna a `"eccodes_key": "#1#longitude"` (elemento BUFR 006002)
    - **heightOfBarometerAboveMeanSeaLevel"** se asigna a `"eccodes_key": "#1#heightOfBarometerAboveMeanSeaLevel"` (elemento BUFR 007031)
    - **airTemperature** se asigna a `"eccodes_key": "#1#airTemperature"` (elemento BUFR 012101)
    - **nonCoordinatePressure** se asigna a `"eccodes_key": "#1#nonCoordinatePressure"` (elemento BUFR 010004)

Verifica el contenido del archivo `custom_template_data.csv` en el directorio `/wis2box-api/data-conversion-exercises`:

```bash
cat /wis2box-api/data-conversion-exercises/custom_template_data.csv
```

Tenga en cuenta que los encabezados de este archivo CSV son los mismos que los encabezados del CSV en la plantilla de mapeo que creó.

Para probar la conversión de datos, podemos usar la herramienta de línea de comandos `csv2bufr` para convertir el archivo CSV a BUFR utilizando la plantilla de mapeo que creamos:

```bash
csv2bufr data transform --bufr-template my_custom_template /wis2box-api/data-conversion-exercises/custom_template_data.csv
```

Debería ver la siguiente salida:

```bash
CLI:    ... Transformando /wis2box-api/data-conversion-exercises/custom_template_data.csv a BUFR ...
CLI:    ... Procesando subconjuntos:
CLI:    ..... 94 bytes escritos en ./WIGOS_0-20000-0-15015_20250412T210000.bufr4
CLI:    Fin del procesamiento, saliendo.
```

!!! question "Verificar el contenido del archivo BUFR"
    
    ¿Cómo puede verificar el contenido del archivo BUFR que acaba de crear y confirmar que los datos se han codificado correctamente?

??? success "Haga clic para revelar la respuesta"

    Puede usar el comando `bufr_dump -p` para verificar el contenido del archivo BUFR que acaba de crear. 
    El comando mostrará el contenido del archivo BUFR en un formato legible para humanos.

    ```bash
    bufr_dump -p ./WIGOS_0-20000-0-15015_20250412T210000.bufr4
    ```

    En la salida verá los valores de los elementos BUFR que mapeó en la plantilla. Por ejemplo, "airTemperature" mostrará:
    
    ```bash
    airTemperature=298.15
    ```

Ahora puede salir del contenedor:

```bash
exit
```

### Usar la plantilla de mapeo en el wis2box

Para asegurarse de que la nueva plantilla de mapeo sea reconocida por el contenedor wis2box-api, necesita reiniciar el contenedor:

```bash
docker restart wis2box-api
```

Ahora puede configurar su conjunto de datos en la wis2box-webapp para usar la plantilla de mapeo personalizada para el complemento de conversión de CSV a BUFR.

La wis2box-webapp detectará automáticamente la plantilla de mapeo que creó y la hará disponible en la lista de plantillas para el complemento de conversión de CSV a BUFR.

Haga clic en el conjunto de datos que creó en la sesión práctica anterior y haga clic en "ACTUALIZAR" junto al complemento con el nombre "CSV data converted to BUFR":

<img alt="Imagen que muestra el editor de conjuntos de datos en la wis2box-webapp" src="/../assets/img/wis2box-webapp-data-mapping-update-csv2bufr.png"/>

Debería ver la nueva plantilla que creó en la lista de plantillas disponibles:

<img alt="Imagen que muestra las plantillas csv2bufr en la wis2box-webapp" src="/../assets/img/wis2box-webapp-csv2bufr-templates.png"/>

!!! hint

    Tenga en cuenta que si no ve la nueva plantilla que creó, intente actualizar la página o abrirla en una nueva ventana de incógnito.

Por ahora mantenga la selección predeterminada de la plantilla AWS (haga clic en la parte superior derecha para cerrar la configuración del complemento).

## Usar la plantilla 'AWS'

La plantilla 'AWS' proporciona una plantilla de mapeo para convertir datos CSV a la secuencia BUFR 301150, 307096, en apoyo de los requisitos mínimos de GBON.

La descripción de la plantilla AWS se puede encontrar aquí [aws-template](./../csv2bufr-templates/aws-template.md).

### Revisar los datos de entrada del ejemplo aws

Descargue el ejemplo para este ejercicio desde el enlace a continuación:

[aws-example.csv](./../sample-data/aws-example.csv)

Abra el archivo que descargó en un editor e inspeccione el contenido:

!!! question
    Al examinar los campos de fecha, hora e identificación (identificadores WIGOS y tradicionales), ¿qué nota? ¿Cómo se representaría la fecha de hoy?

??? success "Haga clic para revelar la respuesta"
    Cada columna contiene una sola pieza de información. Por ejemplo, la fecha está dividida en año, mes y día, reflejando cómo los datos se almacenan en BUFR. La fecha de hoy se dividiría en las columnas "year", "month" y "day". De manera similar, la hora debe dividirse en "hour" y "minute", y el identificador de estación WIGOS en sus respectivos componentes.

!!! question
    Al observar el archivo de datos, ¿cómo se codifican los datos faltantes?
    
??? success "Haga clic para revelar la respuesta"
    Los datos faltantes dentro del archivo están representados por celdas vacías. En un archivo CSV esto se codificaría como ``,,``. Tenga en cuenta que esto es una celda vacía y no está codificada como una cadena de longitud cero, por ejemplo, ``,"",``.

!!! hint "Datos faltantes"
    Se reconoce que los datos pueden faltar por una variedad de razones, ya sea debido a fallos en el sensor o porque el parámetro no se observó. En estos casos, los datos faltantes pueden codificarse como se indica en la respuesta anterior, mientras que los otros datos del informe permanecen válidos.

### Actualizar el archivo de ejemplo

Actualice el archivo de ejemplo que descargó para usar la fecha y hora de hoy y cambie los identificadores de estación WIGOS para usar estaciones que haya registrado en la wis2box-webapp.

### Subir los datos a MinIO y verificar el resultado

Navegue a la interfaz de usuario de MinIO e inicie sesión utilizando las credenciales del archivo `wis2box.env`.

Navegue a **wis2box-incoming** y haga clic en el botón "Crear nueva ruta":

<img alt="Imagen que muestra la interfaz de usuario de MinIO con el botón de crear carpeta resaltado" src="/../assets/img/minio-create-new-path.png"/>

Cree una nueva carpeta en el bucket de MinIO que coincida con el dataset-id del conjunto de datos que creó con la plantilla='weather/surface-weather-observations/synop':

<img alt="Imagen que muestra la interfaz de usuario de MinIO con el botón de crear carpeta resaltado" src="/../assets/img/minio-create-new-path-metadata_id.png"/>

Suba el archivo de ejemplo que descargó a la carpeta que creó en el bucket de MinIO:

<img alt="Imagen que muestra la interfaz de usuario de MinIO con aws-example subido" src="/../assets/img/minio-upload-aws-example.png"/></center>

Verifique el panel de Grafana en `http://YOUR-HOST:3000` para ver si hay ADVERTENCIAS o ERRORES. Si ve alguno, intente solucionarlos y repita el ejercicio.

Verifique el MQTT Explorer para ver si recibe notificaciones de datos WIS2.

Si ingirió los datos correctamente, debería ver 3 notificaciones en MQTT Explorer en el tema `origin/a/wis2/<centre-id>/data/weather/surface-weather-observations/synop` para las 3 estaciones para las que reportó datos:

<img width="450" alt="Imagen que muestra MQTT Explorer después de subir AWS" src="/../assets/img/mqtt-explorer-aws-upload.png"/>

## Usar la plantilla 'DayCLI'

La plantilla **DayCLI** proporciona una plantilla de mapeo para convertir datos climáticos diarios en CSV a la secuencia BUFR 307075, en apoyo de la generación de informes de datos climáticos diarios.

La descripción de la plantilla DAYCLI se puede encontrar aquí [daycli-template](./../csv2bufr-templates/daycli-template.md).

Para compartir estos datos en WIS2, necesitará crear un nuevo conjunto de datos en la wis2box-webapp que tenga la jerarquía de temas WIS2 correcta y que utilice la plantilla DAYCLI para convertir datos CSV a BUFR.

### Crear un conjunto de datos en wis2box para publicar mensajes DAYCLI

Vaya al editor de conjuntos de datos en la wis2box-webapp y cree un nuevo conjunto de datos. Use el mismo centre-id que en las sesiones prácticas anteriores y seleccione **Data Type='climate/surface-based-observations/daily'**:

<img alt="Crear un nuevo conjunto de datos en la wis2box-webapp para DAYCLI" src="/../assets/img/wis2box-webapp-create-dataset-daycli.png"/>

Haga clic en "CONTINUAR AL FORMULARIO" y agregue una descripción para su conjunto de datos, establezca el cuadro delimitador y proporcione la información de contacto para el conjunto de datos. Una vez que haya completado todas las secciones, haga clic en 'VALIDAR FORMULARIO' y revise el formulario.

Revise los complementos de datos para los conjuntos de datos. Haga clic en "ACTUALIZAR" junto al complemento con el nombre "CSV data converted to BUFR" y verá que la plantilla está configurada como **DayCLI**:

<img alt="Actualizar el complemento de datos para el conjunto de datos para usar la plantilla DAYCLI" src="/../assets/img/wis2box-webapp-update-data-plugin-daycli.png"/>

Cierre la configuración del complemento y envíe el formulario utilizando el token de autenticación que creó en la sesión práctica anterior.

Ahora debería tener un segundo conjunto de datos en la wis2box-webapp configurado para usar la plantilla DAYCLI para convertir datos CSV a BUFR.

### Revisar los datos de entrada del ejemplo daycli

Descargue el ejemplo para este ejercicio desde el enlace a continuación:

[daycli-example.csv](./../sample-data/daycli-example.csv)

Abra el archivo que descargó en un editor e inspeccione el contenido:

!!! question
    ¿Qué variables adicionales se incluyen en la plantilla daycli?

??? success "Haga clic para revelar la respuesta"
    La plantilla daycli incluye metadatos importantes sobre la ubicación del instrumento y las clasificaciones de calidad de medición para temperatura y humedad, indicadores de control de calidad e información sobre cómo se ha calculado la temperatura promedio diaria.

### Actualizar el archivo de ejemplo

El archivo de ejemplo contiene una fila de datos para cada día de un mes y reporta datos para una estación. Actualice el archivo de ejemplo que descargó para usar la fecha y hora de hoy y cambie los identificadores de estación WIGOS para usar una estación que haya registrado en la wis2box-webapp.

### Subir los datos a MinIO y verificar el resultado

Como antes, necesitarás cargar los datos en el bucket 'wis2box-incoming' en MinIO para que sean procesados por el convertidor csv2bufr. Esta vez tendrás que crear una nueva carpeta en el bucket de MinIO que coincida con el dataset-id del conjunto de datos que creaste con el template='climate/surface-based-observations/daily', el cual será diferente del dataset-id que utilizaste en el ejercicio anterior:

<img alt="Image showing MinIO UI with DAYCLI-example uploaded" src="/../assets/img/minio-upload-daycli-example.png"/></center>

Después de cargar los datos, verifica que no haya WARNINGS ni ERRORS en el panel de control de Grafana y revisa en MQTT Explorer si recibes notificaciones de datos WIS2.

Si los datos se ingirieron correctamente, deberías ver 30 notificaciones en MQTT Explorer en el tema `origin/a/wis2/<centre-id>/data/climate/surface-based-observations/daily` correspondientes a los 30 días del mes para los cuales reportaste datos:

<img width="450" alt="Image showing MQTT explorer after uploading DAYCLI" src="/../assets/img/mqtt-daycli-template-success.png"/>

## Conclusión

!!! success "¡Felicidades!"
    En esta sesión práctica has aprendido:

    - cómo crear una plantilla de mapeo personalizada para convertir datos CSV a BUFR
    - cómo usar las plantillas integradas de AWS y DAYCLI para convertir datos CSV a BUFR
---
title: Convertir datos CSV a BUFR
---

# Convertir datos CSV a BUFR

!!! abstract "Resultados de aprendizaje"
    Al final de esta sesión práctica, serás capaz de:

    - usar la **Interfaz de Usuario de MinIO** para subir archivos de datos CSV de entrada y monitorear el resultado
    - conocer el formato de datos CSV para usar con la plantilla automática de estación meteorológica BUFR por defecto
    - usar el editor de conjuntos de datos en la **aplicación web wis2box** para crear un conjunto de datos para publicar mensajes DAYCLI
    - conocer el formato de datos CSV para usar con la plantilla DAYCLI BUFR
    - usar **wis2box webapp** para validar y convertir datos de muestra para estaciones AWS a BUFR (opcional)

## Introducción

Los archivos de datos de valores separados por comas (CSV) se utilizan a menudo para registrar datos observacionales y otros datos en un formato tabular.
La mayoría de los registradores de datos utilizados para registrar la salida de sensores pueden exportar las observaciones en archivos delimitados, incluyendo en CSV.
De manera similar, cuando los datos se ingieren en una base de datos, es fácil exportar los datos requeridos en archivos formateados CSV.
Para ayudar en el intercambio de datos originalmente almacenados en formatos de datos tabulares, se ha implementado un convertidor de CSV a BUFR en
wis2box utilizando el mismo software que para SYNOP a BUFR.

En esta sesión aprenderás sobre el uso del convertidor csv2bufr en wis2box para las siguientes plantillas integradas:

- **AWS** (aws-template.json) : Plantilla de mapeo para convertir datos CSV de un archivo simplificado de estación meteorológica automática a la secuencia BUFR 301150, 307096"
- **DayCLI** (daycli-template.json) : Plantilla de mapeo para convertir datos CSV climáticos diarios a la secuencia BUFR 307075

## Preparación

Asegúrate de que el stack de wis2box haya sido iniciado con `python3 wis2box.py start`

Asegúrate de que tienes un navegador web abierto con la Interfaz de Usuario de MinIO para tu instancia yendo a `http://<tu-host>:9000`
Si no recuerdas tus credenciales de MinIO, puedes encontrarlas en el archivo `wis2box.env` en el directorio `wis2box-1.0.0rc1` en tu VM de estudiante.

Asegúrate de que tienes MQTT Explorer abierto y conectado a tu broker usando las credenciales `everyone/everyone`.

## Ejercicio 1: Usar csv2bufr con la plantilla 'AWS'

La plantilla 'AWS' proporciona una plantilla de mapeo predefinida para convertir datos CSV de estaciones AWS en apoyo a los requisitos de informes de GBON.

La descripción de la plantilla AWS se puede encontrar [aquí](./../csv2bufr-templates/aws-template.md).

### Revisar los datos de entrada de ejemplo aws

Descarga el ejemplo para este ejercicio desde el enlace a continuación:

[aws-example.csv](./../../sample-data/aws-example.csv)

Abre el archivo que descargaste en un editor e inspecciona el contenido:

!!! question
    Examinando los campos de fecha, hora e identificación (identificadores WIGOS y tradicionales) ¿qué
    notas? ¿Cómo se representaría la fecha de hoy?

??? success "Haz clic para revelar la respuesta"
    Cada columna contiene una sola pieza de información. Por ejemplo, la fecha se divide en
    año, mes y día, reflejando cómo se almacenan los datos en BUFR. La fecha de hoy se dividiría
    en las columnas "año", "mes" y "día". De manera similar, la hora necesita ser
    dividida en "hora" y "minuto" y el identificador de la estación WIGOS en sus respectivos componentes.

!!! question
    Mirando el archivo de datos, ¿cómo se codifican los datos faltantes?

??? success "Haz clic para revelar la respuesta"
    Los datos faltantes en el archivo están representados por celdas vacías. En un archivo CSV esto sería
    codificado por ``,,``. Nota que esto es una celda vacía y no codificada como una cadena de longitud cero,
    e.g. ``,"",``.

!!! hint "Datos faltantes"
    Se reconoce que los datos pueden faltar por una variedad de razones, ya sea debido a fallos del sensor
    o al parámetro no observado. En estos casos, los datos faltantes pueden codificarse
    según la respuesta anterior, los otros datos en el informe siguen siendo válidos.

!!! question
    ¿Cuáles son los identificadores de estación WIGOS para las estaciones que reportan datos en el archivo de ejemplo? ¿Cómo se definen en el archivo de entrada?

??? success "Haz clic para revelar la respuesta"

    El identificador de estación WIGOS está definido por 4 columnas separadas en el archivo:

    - **wsi_series**: Serie de identificador WIGOS
    - **wsi_issuer**: Emisor WIGOS del identificador
    - **wsi_issue_number**: Número de emisión WIGOS
    - **wsi_local**: Identificador local WIGOS

    Los identificadores de estación WIGOS utilizados en el archivo de ejemplo son `0-20000-0-60351`, `0-20000-0-60355` y `0-20000-0-60360`.	

### Actualizar el archivo de ejemplo

Actualiza el archivo de ejemplo que descargaste para usar la fecha y hora de hoy y cambia los identificadores de estación WIGOS para usar estaciones que hayas registrado en wis2box-webapp.

### Subir los datos a MinIO y verificar el resultado

Navega a la Interfaz de Usuario de MinIO y inicia sesión usando las credenciales del archivo `wis2box.env`.

Navega a **wis2box-incoming** y haz clic en el botón "Crear nueva ruta":

<img alt="Imagen mostrando la Interfaz de Usuario de MinIO con el botón de crear carpeta destacado" src="/../assets/img/minio-create-new-path.png"/>

Crea una nueva carpeta en el bucket de MinIO que coincida con el id de conjunto de datos para el conjunto de datos que creaste con la plantilla='weather/surface-weather-observations/synop':

<img alt="Imagen mostrando la Interfaz de Usuario de MinIO con el botón de crear carpeta destacado" src="/../assets/img/minio-create-new-path-metadata_id.png"/>

Sube el archivo de ejemplo que descargaste a la carpeta que creaste en el bucket de MinIO:

<img alt="Imagen mostrando la Interfaz de Usuario de MinIO con aws-example subido" src="/../assets/img/minio-upload-aws-example.png"/></center>

Revisa el tablero de Grafana en `http://<tu-host>:3000` para ver si hay alguna ADVERTENCIA o ERROR. Si ves alguno, intenta solucionarlo y repite el ejercicio.

Revisa el MQTT Explorer para ver si recibes notificaciones de datos WIS2.

Si has ingestado los datos con éxito, deberías ver 3 notificaciones en el explorador MQTT en el tema `origin/a/wis2/<id-centro>/data/weather/surface-weather-observations/synop` para las 3 estaciones de las que informaste datos:

<img width="450" alt="Imagen mostrando el explorador MQTT después de subir AWS" src="/../assets/img/mqtt-explorer-aws-upload.png"/>

## Ejercicio 2 - Usar la plantilla 'DayCLI'

En el ejercicio anterior usamos el conjunto de datos que creaste con el tipo de datos='weather/surface-weather-observations/synop', que ha preconfigurado la plantilla de conversión de CSV a BUFR a la plantilla AWS.

En el próximo ejercicio usaremos la plantilla 'DayCLI' para convertir datos climáticos diarios a BUFR.

La descripción de la plantilla DAYCLI se puede encontrar [aquí](./../csv2bufr-templates/daycli-template.md).

!!! Note "Acerca de la plantilla DAYCLI"
    Ten en cuenta que la secuencia BUFR DAYCLI se actualizará durante 2025 para incluir información adicional y banderas de control de calidad revisadas. La plantilla DAYCLI incluida en wis2box se actualizará para reflejar estos cambios. La OMM comunicará cuando el software de wis2box se actualice para incluir la nueva plantilla DAYCLI, para permitir a los usuarios actualizar sus sistemas en consecuencia.

### Crear un conjunto de datos wis2box para publicar mensajes DAYCLI

Ve al editor de conjuntos de datos en la aplicación web wis2box y crea un nuevo conjunto de datos. Usa el mismo id de centro que en las sesiones prácticas anteriores y selecciona **Tipo de Datos='climate/surface-based-observations/daily'**:

<img alt="Crear un nuevo conjunto de datos en la aplicación web wis2box para DAYCLI" src="/../assets/img/wis2box-webapp-create-dataset-daycli.png"/>

Haz clic en "CONTINUAR AL FORMULARIO" y añade una descripción para tu conjunto de datos, establece el cuadro delimitador y proporciona la información de contacto para el conjunto de datos. Una vez que hayas terminado de llenar todas las secciones, haz clic en 'VALIDAR FORMULARIO' y revisa el formulario.

Revisa los complementos de datos para los conjuntos de datos. Haz clic en "ACTUALIZAR" al lado del complemento con nombre "Datos CSV convertidos a BUFR" y verás que la plantilla está configurada para **DayCLI**:

<img alt="Actualizar el complemento de datos para el conjunto de datos para usar la plantilla DAYCLI" src="/../assets/img/wis2box-webapp-update-data-plugin-daycli.png"/>

Cierra la configuración del complemento y envía el formulario usando el token de autenticación que creaste en la sesión práctica anterior.

Ahora deberías tener un segundo conjunto de datos en la aplicación web wis2box configurado para usar la plantilla DAYCLI para convertir datos CSV a BUFR.

### Revisar los datos de entrada de ejemplo daycli

Descarga el ejemplo para este ejercicio desde el enlace a continuación:

[daycli-example.csv](./../../sample-data/daycli-example.csv)

Abre el archivo que descargaste en un editor e inspecciona el contenido:

!!! question
    ¿Qué variables adicionales están incluidas en la plantilla daycli?

??? success "Haz clic para revelar la respuesta"
    La plantilla daycli incluye metadatos importantes sobre el emplazamiento del instrumento y las clasificaciones de calidad de medición para temperatura y humedad, banderas de control de calidad e información sobre cómo se ha calculado la temperatura media diaria.

### Actualizar el archivo de ejemplo

El archivo de ejemplo contiene una fila de datos para cada día en un mes, e informa datos para una estación. Actualiza el archivo de ejemplo que descargaste para usar la fecha y hora de hoy y cambia los identificadores de estación WIGOS para usar una estación que hayas registrado en wis2box-webapp.

### Subir los datos a MinIO y verificar el resultado

Como antes, necesitarás subir los datos al bucket 'wis2box-incoming' en MinIO para ser procesados por el convertidor csv2bufr. Esta vez necesitarás crear una nueva carpeta en el bucket de MinIO que coincida con el id de conjunto de datos para el conjunto de datos que creaste con la plantilla='climate/surface-based-observations/daily' que será diferente del id de conjunto de datos que usaste en el ejercicio anterior:

<img alt="Imagen mostrando la Interfaz de Usuario de MinIO con DAYCLI-example subido" src="/../assets/img/minio-upload-daycli-example.png"/></center>

Después de subir los datos, verifica que no haya ADVERTENCIAS o ERRORES en el tablero de Grafana y revisa el explorador MQTT para ver si recibes notificaciones de datos WIS2.

Si has ingestado los datos con éxito, deberías ver 30 notificaciones en el explorador MQTT en el tema `origin/a/wis2/<id-centro>/data/climate/surface-based-observations/daily` para los 30 días del mes que informaste datos para:

<img width="450" alt="Imagen mostrando el explorador MQTT después de subir DAYCLI" src="/../assets/img/mqtt-daycli-template-success.png"/>

## Ejercicio 3 - usando el formulario CSV en wis2box-webapp (opcional)

La aplicación web wis2box proporciona una interfaz para subir datos CSV y convertirlos a BUFR antes de publicarlos en WIS2, usando la plantilla AWS.

El uso de este formulario está destinado a propósitos de depuración y validación, el método de envío recomendado para publicar datos de Estaciones Meteorológicas Automatizadas es configurar un proceso que suba automáticamente los datos al bucket de MinIO.

### Usar el formulario CSV en la aplicación web wis2box

Navega al formulario CSV en la aplicación web wis2box
(``http://<tu-nombre-de-host>/wis2box-webapp/csv2bufr_form``).
Usa el archivo [aws-example.csv](../sample-data/aws-example.csv) para este ejercicio.
Ahora deberías poder hacer clic en siguiente para previsualizar y validar el archivo.

<center><img alt="Imagen mostrando la pantalla de carga de CSV a BUFR" src="/../assets/img/csv2bufr-ex1.png"/></center>

Al hacer clic en el botón siguiente, se carga el archivo en el navegador y se valida el contenido contra un esquema predefinido.
Aún no se ha convertido ni publicado ningún dato. En la pestaña de previsualización / validación, se te debería presentar una lista de advertencias
sobre datos faltantes, pero en este ejercicio se pueden ignorar.

<center><img alt="Imagen mostrando la página de validación de ejemplo de CSV a BUFR con advertencias" src="/../assets/img/csv2bufr-warnings.png"/></center>

Haz clic en *siguiente* para continuar y se te pedirá que proporciones un id de conjunto de datos para los datos a publicar. Selecciona el id de conjunto de datos que creaste anteriormente y haz clic en *siguiente*.

Ahora deberías estar en una página de autorización donde se te pedirá que ingreses el token ``processes/wis2box``
que has creado previamente. Ingresa este token y haz clic en el interruptor "Publicar en WIS2" para asegurarte
de que "Publicar en WIS2" esté seleccionado (ver captura de pantalla a continuación).

<center><img alt="pantalla de autenticación y publicación csv2bufr" src="/../assets/img/csv2bufr-toggle-publish.png"/></center>

Haz clic en siguiente para transformar a BUFR y publicar, luego deberías ver la siguiente pantalla:

<center><img alt="Imagen mostrando la pantalla de éxito de ejemplo de CSV a BUFR" src="/../assets/img/csv2bufr-success.png"/></center>

Al hacer clic en la flecha hacia abajo a la derecha de ``Archivos BUFR de salida`` deberían aparecer los botones ``Descargar`` e ``Inspeccionar``.
Haz clic en inspeccionar para ver los datos y confirmar que los valores son los esperados.

<center><img alt="Imagen mostrando la inspección de salida de CSV a BUFR" src="/../assets/img/csv2bufr-inspect.png"/></center>

### Depuración de datos de entrada inválidos

En este ejercicio examinaremos qué sucede con los datos de entrada inválidos. Descarga el siguiente archivo de ejemplo haciendo clic en el
enlace a continuación. Este contiene los mismos datos que el primer archivo pero con las columnas vacías eliminadas.
Examina el archivo y confirma qué columnas han sido eliminadas y luego sigue el mismo proceso para convertir los datos a BUFR.

[csv2bufr-ex3a.csv](./../../sample-data/csv2bufr-ex3a.csv)

!!! question
    Con las columnas faltantes en el archivo, ¿pudiste convertir los datos a BUFR?
    ¿Notaste algún cambio en las advertencias en la página de validación?

??? success "Haz clic para revelar la respuesta"
    Deberías haber podido convertir los datos a BUFR, pero los mensajes de advertencia se habrán actualizado
    para indicar que las columnas faltaban completamente en lugar de contener un valor faltante.

En este siguiente ejemplo se ha añadido una columna adicional al archivo CSV.

[csv2bufr-ex3b.csv](./../../sample-data/csv2bufr-ex3b.csv)

!!! question
    Sin subir ni enviar el archivo, ¿puedes predecir qué sucederá cuando lo hagas?

Ahora sube y confirma si tu predicción fue correcta.

??? success "Haz clic para revelar la respuesta"
    Cuando se valide el archivo, ahora deberías recibir una advertencia de que la columna ``index``
    no se encuentra en el esquema y que los datos serán omitidos. Deberías poder hacer clic
    y convertir a BUFR como en el ejemplo anterior.

En el último ejemplo de este ejercicio, los datos han sido modificados. Examina el contenido del archivo CSV.

[csv2bufr-ex3c.csv](./../../sample-data/csv2bufr-ex3c.csv)

!!! question
    ¿Qué ha cambiado en el archivo y qué crees que sucederá?

Ahora sube el archivo y confirma si estabas en lo correcto.

??? warning "Haz clic para revelar la respuesta"
    Los campos de presión han sido convertidos de Pa a hPa en los datos de entrada. Sin embargo, el convertidor de CSV a BUFR
    espera las mismas unidades que BUFR (Pa) y, como resultado, estos campos fallan la validación por estar
    fuera de rango. Deberías poder editar el CSV para corregir el problema y volver a enviar los datos regresando
    a la primera pantalla y
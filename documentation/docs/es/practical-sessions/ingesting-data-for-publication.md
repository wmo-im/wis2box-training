---
title: Ingestar datos para su publicación
---

# Ingestar datos para su publicación

!!! abstract "Resultados de aprendizaje"

    Al final de esta sesión práctica, serás capaz de:
    
    - Activar el flujo de trabajo de wis2box subiendo datos a MinIO utilizando la interfaz web de MinIO, SFTP o un script en Python.
    - Acceder al panel de Grafana para monitorear el estado de la ingesta de datos y ver los registros de tu instancia de wis2box.
    - Ver las notificaciones de datos WIS2 publicadas por tu wis2box utilizando MQTT Explorer.

## Introducción

En WIS2, los datos se comparten en tiempo real utilizando notificaciones de datos WIS2 que contienen un enlace "canónico" desde el cual se pueden descargar los datos.

Para activar el flujo de trabajo de datos en un WIS2 Node utilizando el software wis2box, los datos deben subirse al bucket **wis2box-incoming** en **MinIO**, lo que inicia el flujo de trabajo de datos de wis2box para procesar y publicar los datos.

Para monitorear el estado del flujo de trabajo de datos de wis2box, puedes usar el **panel de Grafana** y **MQTT Explorer**. El panel de Grafana utiliza datos de Prometheus y Loki para mostrar el estado de tu wis2box, mientras que MQTT Explorer te permite ver las notificaciones de datos WIS2 publicadas por tu instancia de wis2box.

En esta sección, nos centraremos en cómo subir datos a tu instancia de wis2box y verificar la ingesta y publicación exitosa. La transformación de datos se cubrirá más adelante en la sesión práctica [Herramientas de Conversión de Datos](./data-conversion-tools.md).

Para probar manualmente el proceso de ingesta de datos, utilizaremos la interfaz web de MinIO, que permite descargar y subir datos a MinIO utilizando un navegador web.

En un entorno de producción, los datos generalmente se ingieren utilizando procesos automatizados, como scripts o aplicaciones que envían datos a MinIO a través de S3 o SFTP.

## Preparación

Esta sección asume que has completado con éxito la sesión práctica [Configuración de Conjuntos de Datos en wis2box](./configuring-wis2box-datasets.md). Si seguiste las instrucciones de esa sesión, deberías tener un conjunto de datos que utiliza el plugin `Universal` y otro que utiliza el plugin `FM-12 data converted to BUFR`.

Asegúrate de poder iniciar sesión en tu VM de estudiante utilizando tu cliente SSH (por ejemplo, PuTTY).

Asegúrate de que wis2box esté funcionando:

```bash
cd ~/wis2box/
python3 wis2box-ctl.py start
python3 wis2box-ctl.py status
```

Asegúrate de que MQTT Explorer esté en ejecución y conectado a tu instancia utilizando las credenciales públicas `everyone/everyone` con una suscripción al tema `origin/a/wis2/#`.

## El Panel de Grafana

Abre el panel de Grafana disponible en `http://YOUR-HOST:3000` y verás el panel de publicación de datos de wis2box:

<img alt="grafana_dashboard" src="/../assets/img/grafana-homepage.png" width="800">

Mantén el panel de Grafana abierto en tu navegador, ya que lo utilizaremos más adelante para monitorear el estado de la ingesta de datos.

## Usando la Interfaz Web de MinIO

Abre la interfaz web de MinIO disponible en `http://YOUR-HOST:9001` y verás la pantalla de inicio de sesión:

<img alt="Minio UI: minio ui" src="/../assets/img/minio-login.png" width="400">

Para iniciar sesión, necesitas usar las credenciales definidas por WIS2BOX_STORAGE_USERNAME y WIS2BOX_STORAGE_PASSWORD en el archivo wis2box.env. Puedes verificar los valores de estas variables ejecutando los siguientes comandos en tu VM de estudiante:

```bash
cat wis2box.env | grep WIS2BOX_STORAGE_USERNAME
cat wis2box.env | grep WIS2BOX_STORAGE_PASSWORD
```

Después de iniciar sesión, estarás en la vista del Navegador de Objetos de MinIO. Aquí puedes ver los buckets utilizados por wis2box:

- *wis2box-incoming*: Este es el bucket donde subes datos para activar el flujo de trabajo de wis2box.
- *wis2box-public*: Este es el bucket donde wis2box publica los datos que han sido ingeridos y procesados con éxito.

Haz clic en el bucket *wis2box-incoming*. Prueba la opción para definir una nueva ruta en este bucket haciendo clic en `Create new path`:

<img alt="minio ui: minio ui after login" src="/../assets/img/minio-incoming-create-new-path.png" width="800">

Introduce la nueva Ruta de Carpeta = *new-directory* y sube este archivo de ejemplo [mydata.nc](./../sample-data/mydata.nc) (haz clic derecho y selecciona "guardar como" para descargar el archivo). Puedes usar el botón "Upload" en MinIO para subir el archivo al nuevo directorio:

<img alt="minio ui: create new path" src="/../assets/img/minio-initial-example-upload.png" width="800">

!!! question "Pregunta"

    Después de subir el archivo, ¿cómo puedes verificar si el flujo de trabajo de datos en wis2box se activó con éxito?

??? success "Haz clic para revelar la respuesta"

    Puedes verificar el panel de Grafana para ver si los datos fueron ingeridos y publicados con éxito.

    Mira el panel inferior del panel de Grafana y verás un **Error de validación de ruta** indicando que la ruta no coincide con ningún conjunto de datos configurado:

    ```bash
    ERROR - Path validation error: Could not match http://minio:9000/wis2box-incoming/new-directory/mydata.nc to dataset, path should include one of the following: ['urn:wmo:md:int-wmo-example:synop-dataset-wis2-training', 'urn:wmo:md:int-wmo-example:forecast-dataset' ...
    ``` 
    
## Ingestar y Publicar: Plugin "Universal"

Ahora que sabes cómo subir datos a MinIO, intentemos subir datos para el conjunto de datos de pronóstico que creaste en la sesión práctica anterior y que utiliza el plugin "Universal".

Vuelve a la interfaz web de MinIO en tu navegador, selecciona el bucket `wis2box-incoming` y haz clic en `Create new path`.

Esta vez asegúrate de **crear un directorio que coincida con el identificador de metadatos para el conjunto de datos de pronóstico** que creaste en la sesión práctica anterior:

<img alt="minio-filepath-forecast-dataset" src="/../assets/img/minio-filepath-forecast-dataset.png" width="800">

Entra en el directorio recién creado, haz clic en `Upload` y sube el archivo que usaste previamente, *mydata.nc*, al nuevo directorio. Verifica el panel de Grafana para ver si los datos fueron ingeridos y publicados con éxito.

Deberías ver el siguiente error en el panel de Grafana:

```bash
ERROR - Path validation error: Unknown file type (nc) for metadata_id=urn:wmo:md:int-wmo-example:forecast-dataset. Did not match any of the following:grib2
```

!!! question "Pregunta"

    ¿Por qué no se ingresaron ni publicaron los datos?

??? success "Haz clic para revelar la respuesta"

    El conjunto de datos fue configurado para procesar únicamente archivos con la extensión `.grib2`. La configuración de la Extensión de Archivo es parte de los mapeos de datos que definiste en la sesión práctica anterior.

Descarga este archivo [GEPS_18August2025.grib2](../sample-data/GEPS_18August2025.grib2) a tu computadora local y súbelo al directorio que creaste para el conjunto de datos de pronóstico. Verifica el panel de Grafana y MQTT Explorer para ver si los datos fueron ingeridos y publicados con éxito.

Verás el siguiente ERROR en el panel de Grafana:

```bash
ERROR - Failed to transform file http://minio:9000/wis2box-incoming/urn:wmo:md:int-wmo-example:forecast-dataset/GEPS_18August2025.grib2 : GEPS_18August2025.grib2 did not match ^.*?_(\d{8}).*?\..*$
```

!!! question "Pregunta"

    ¿Cómo puedes solucionar este error?

??? success "Haz clic para revelar la respuesta"

    El nombre del archivo no coincide con la expresión regular que definiste en la configuración del conjunto de datos. El nombre del archivo debe coincidir con el patrón `^.*?_(\d{8}).*?\..*$`, que requiere una fecha de 8 dígitos (YYYYMMDD) en el nombre del archivo.

    Renombra el archivo a *GEPS_202508180000.grib2* y súbelo nuevamente a la misma ruta en MinIO para reactivar el flujo de trabajo de wis2box (o descarga el archivo renombrado desde aquí: [GEPS_202508180000.grib2](../sample-data/GEPS_202508180000.grib2)).

Después de solucionar el problema con el nombre del archivo, verifica el panel de Grafana y MQTT Explorer para ver si los datos fueron ingeridos y publicados con éxito.

Deberías ver una nueva notificación de datos WIS2 en MQTT Explorer:

<img alt="mqtt explorer: message notification geps data" src="/../assets/img/mqtt-explorer-wis2-notification-geps-sample.png" width="800">

!!! note "Acerca del Plugin Universal"

    El plugin "Universal" te permite publicar datos sin ninguna transformación. Es un plugin de *paso directo* que ingiere el archivo de datos y lo publica tal cual. Para agregar la propiedad "datetime" a la notificación de datos WIS2, el plugin se basa en el primer grupo de la Expresión Regular del Patrón de Archivo para coincidir con la fecha de los datos que estás publicando.

!!! question "Pregunta adicional"

    Intenta subir el mismo archivo nuevamente a la misma ruta en MinIO. ¿Recibes otra notificación en MQTT Explorer?

??? success "Haz clic para revelar la respuesta"

    No. 
    En el panel de Grafana verás un error indicando que los datos ya fueron publicados:

```bash
ERROR - Data already published for GEPS_202508180000-grib2; not publishing
```

Esto demuestra que el flujo de trabajo de datos se activó, pero los datos no se volvieron a publicar. El wis2box no publicará los mismos datos dos veces.

Si deseas forzar el reenvío de la notificación para los mismos datos, elimina los datos del bucket 'wis2box-public' antes de volver a ingerir los datos.

## Ingestar y Publicar: Plugin "synop2bufr"

A continuación, trabajarás con el conjunto de datos que creaste en la sesión práctica anterior utilizando **Template='weather/surface-based-observations/synop'**. La plantilla preconfiguró los siguientes plugins de datos para ti:

<img alt="synop-dataset-plugins" src="/../assets/img/wis2box-data-mappings.png" width="1000">

Ten en cuenta que uno de los plugins es **FM-12 data converted to BUFR** (synop2bufr), que está configurado para ejecutarse en archivos con la extensión **txt**.

Descarga este archivo de muestra [synop_202502040900.txt](../sample-data/synop_202502040900.txt) (haz clic derecho y selecciona "guardar como" para descargar el archivo) en tu computadora local. Crea una nueva ruta en MinIO que coincida con el identificador de metadatos para el conjunto de datos synop y sube los datos de muestra a esta ruta.

Verifica el panel de Grafana y MQTT Explorer para confirmar si los datos se ingirieron y publicaron correctamente.

!!! question "Pregunta"

    ¿Por qué no recibiste una notificación en MQTT Explorer?

??? success "Haz clic para revelar la respuesta"

    En el panel de Grafana verás una advertencia que indica:

    ```bash
    WARNING - Station 64400 not found in station file
    ```

    O si no tenías estaciones asociadas con el tema, verás:

    ```bash
    ERROR - No stations found
    ```

    El flujo de trabajo de datos se activó, pero el plugin de datos no pudo procesar los datos debido a la falta de metadatos de la estación.

!!! note "Sobre el plugin FM-12 data converted to BUFR"

    Este plugin intenta transformar los datos de entrada FM-12 al formato BUFR.

    Como parte de la transformación, el plugin agrega metadatos faltantes a los datos de salida, como el identificador de estación WIGOS, la ubicación y la altura del barómetro de la estación. Para agregar estos metadatos, el plugin busca esta información en la lista de estaciones de tu instancia de wis2box utilizando el identificador tradicional (de 5 dígitos) (64400 en este caso).

    Si la estación no se encuentra en la lista de estaciones, el plugin no puede agregar los metadatos faltantes y no publicará ningún dato.

Agrega la estación con el identificador WIGOS `0-20000-0-64400` a tu instancia de wis2box utilizando el editor de estaciones en la wis2box-webapp, como aprendiste en la sesión práctica [Configuring Station Metadata](./configuring-station-metadata.md).

Recupera la estación desde OSCAR:

<img alt="oscar-station" src="/../assets/img/webapp-test-station-oscar-search.png" width="600">

Agrega la estación al tema '../weather/surface-based-observations/synop' y guarda los cambios utilizando tu token de autenticación.

Después de agregar la estación, vuelve a activar el flujo de trabajo de wis2box subiendo nuevamente el archivo de datos de muestra *synop_202502040900.txt* en la misma ruta en MinIO.

Verifica el panel de Grafana y MQTT Explorer para confirmar que los datos se publicaron correctamente. Si ves la notificación a continuación, entonces publicaste los datos de muestra synop con éxito:

<img alt="webapp-test-station" src="/../assets/img/mqtt-explorer-wis2box-notification-synop-sample.png" width="800">

!!! question "Pregunta"

    ¿Cuál es la extensión del archivo que se publicó en la notificación de datos de WIS2?

??? success "Haz clic para revelar la respuesta"

    Revisa la sección de Enlaces de la notificación de datos de WIS2 en MQTT Explorer y verás el enlace canónico:

    ```json
    {
      "rel": "canonical",
      "type": "application/bufr",
      "href": "http://example.wis2.training/data/2025-02-04/wis/urn:wmo:md:int-wmo-example:synop-dataset/WIGOS_0-20000-0-64400_20250204T090000.bufr4",
      "length": 387
    }
    ```

    La extensión del archivo es `.bufr4`, lo que indica que los datos se transformaron con éxito del formato FM-12 al formato BUFR mediante el plugin.

## Ingestar datos usando Python

Usar la interfaz web de MinIO es una forma conveniente de subir datos manualmente a MinIO para fines de prueba. Sin embargo, en un entorno de producción, normalmente usarías procesos automatizados para subir datos a MinIO, por ejemplo, utilizando scripts o aplicaciones que usen la API compatible con S3 de MinIO.

En este ejercicio, usaremos el cliente de Python de MinIO para copiar datos en MinIO.

MinIO proporciona un cliente de Python, que puede instalarse de la siguiente manera:

```bash
pip3 install minio
```

En tu máquina virtual de estudiante, el paquete 'minio' para Python ya estará instalado.

Copia el directorio `exercise-materials/data-ingest-exercises` al directorio que definiste como `WIS2BOX_HOST_DATADIR` en tu archivo `wis2box.env`:

```bash
cp -r ~/exercise-materials/data-ingest-exercises ~/wis2box-data/
```

!!! note
    El `WIS2BOX_HOST_DATADIR` está montado como `/data/wis2box/` dentro del contenedor wis2box-management por el archivo `docker-compose.yml` incluido en el directorio `wis2box`.

    Esto te permite compartir datos entre el host y el contenedor.

En el directorio `exercise-materials/data-ingest-exercises`, encontrarás un script de ejemplo `copy_file_to_incoming.py` que puede usarse para copiar archivos en MinIO.

Intenta ejecutar el script para copiar el archivo de datos de muestra `synop_202501030900.txt` en el bucket `wis2box-incoming` en MinIO de la siguiente manera:

```bash
cd ~/wis2box-data/data-ingest-exercises
python3 copy_file_to_incoming.py synop_202501030900.txt
```

!!! note

    Obtendrás un error ya que el script no está configurado para acceder al endpoint de MinIO en tu wis2box todavía.

El script necesita conocer el endpoint correcto para acceder a MinIO en tu wis2box. Si wis2box se está ejecutando en tu host, el endpoint de MinIO está disponible en `http://YOUR-HOST:9000`. El script también necesita ser actualizado con tu contraseña de almacenamiento y la ruta en el bucket de MinIO para almacenar los datos.

!!! question "Actualizar el Script e Ingestar los Datos CSV"

    Edita el script `copy_file_to_incoming.py` para solucionar los errores, utilizando uno de los siguientes métodos:
    - Desde la línea de comandos: usa el editor de texto `nano` o `vim` para editar el script.
    - Usando WinSCP: inicia una nueva conexión utilizando el Protocolo de Archivo `SCP` y las mismas credenciales que tu cliente SSH. Navega al directorio `wis2box-data/data-ingest-exercises` y edita `copy_file_to_incoming.py` utilizando el editor de texto integrado.

    Asegúrate de:

    - Definir el endpoint correcto de MinIO para tu host.
    - Proporcionar la contraseña de almacenamiento correcta para tu instancia de MinIO.
    - Proporcionar la ruta correcta en el bucket de MinIO para almacenar los datos.

    Vuelve a ejecutar el script para ingerir el archivo de datos de muestra `synop_202501030900.txt` en MinIO:

    ```bash
    python3 ~/wis2box-data/ ~/wis2box-data/synop_202501030900.txt
    ```

    Asegúrate de que los errores se resuelvan.

Una vez que logres ejecutar el script con éxito, verás un mensaje que indica que el archivo fue copiado a MinIO, y deberías ver notificaciones de datos publicadas por tu instancia de wis2box en MQTT Explorer.

También puedes verificar el panel de Grafana para confirmar si los datos se ingirieron y publicaron correctamente.

Ahora que el script funciona, puedes intentar copiar otros archivos en MinIO utilizando el mismo script.

!!! question "Ingestar Datos Binarios en Formato BUFR"

    Ejecuta el siguiente comando para copiar el archivo de datos binarios `bufr-example.bin` en el bucket `wis2box-incoming` en MinIO:

    ```bash
    python3 copy_file_to_incoming.py bufr-example.bin
    ```

Verifica el panel de Grafana y MQTT Explorer para confirmar si los datos de prueba se ingirieron y publicaron correctamente. Si ves algún error, intenta resolverlo.

!!! question "Verificar la Ingesta de Datos"

    ¿Cuántos mensajes se publicaron en el broker MQTT para esta muestra de datos?

??? success "Haz clic para revelar la respuesta"

    Verás errores reportados en Grafana ya que las estaciones en el archivo BUFR no están definidas en la lista de estaciones de tu instancia de wis2box.

    Si todas las estaciones utilizadas en el archivo BUFR están definidas en tu instancia de wis2box, deberías ver 10 mensajes publicados en el broker MQTT. Cada notificación corresponde a datos de una estación para una marca de tiempo de observación.

    El plugin `wis2box.data.bufr4.ObservationDataBUFR` divide el archivo BUFR en mensajes BUFR individuales y publica un mensaje por cada estación y marca de tiempo de observación.

## Ingestar datos mediante SFTP
```

El servicio MinIO en wis2box también se puede acceder a través de SFTP. Si tienes un sistema existente que puede configurarse para enviar datos mediante SFTP, puedes usar esto como un método alternativo para automatizar la ingesta de datos.

El servidor SFTP para MinIO está vinculado al puerto 8022 en el host (el puerto 22 se utiliza para SSH).

En este ejercicio, demostraremos cómo usar WinSCP para cargar datos en MinIO utilizando SFTP.

Puedes configurar una nueva conexión en WinSCP como se muestra en esta captura de pantalla:

<img alt="winscp-sftp-connection" src="/../assets/img/winscp-sftp-login.png" width="400">

Las credenciales para la conexión SFTP están definidas por `WIS2BOX_STORAGE_USERNAME` y `WIS2BOX_STORAGE_PASSWORD` en tu archivo `wis2box.env` y son las mismas que utilizaste para conectarte a la interfaz de usuario de MinIO.

Cuando inicies sesión, verás los buckets utilizados por wis2box en MinIO:

<img alt="winscp-sftp-bucket" src="/../assets/img/winscp-buckets.png" width="600">

Puedes navegar al bucket `wis2box-incoming` y luego a la carpeta de tu conjunto de datos. Verás los archivos que cargaste en los ejercicios anteriores:

<img alt="winscp-sftp-incoming-path" src="/../assets/img/winscp-incoming-data-path.png" width="600">

!!! question "Cargar datos usando SFTP"

    Descarga este archivo de ejemplo en tu computadora local:

    [synop_202503030900.txt](./../sample-data/synop_202503030900.txt) (haz clic derecho y selecciona "guardar como" para descargar el archivo).

    Luego, súbelo a la ruta del conjunto de datos entrante en MinIO utilizando tu sesión SFTP en WinSCP.

    Revisa el panel de Grafana y MQTT Explorer para verificar si los datos se ingirieron y publicaron correctamente.

??? success "Haz clic para revelar la respuesta"

    Deberías ver una nueva notificación de datos WIS2 publicada para la estación de prueba `0-20000-0-64400`, indicando que los datos se ingirieron y publicaron correctamente.

    <img alt="grafana_data_ingest" src="/../assets/img/grafana_data-ingest-test3.png" width="400"> 

    Si utilizas una ruta incorrecta, verás un mensaje de error en los registros.

## Conclusión

!!! success "¡Felicidades!"
    En esta sesión práctica, aprendiste a:

    - Activar el flujo de trabajo de wis2box cargando datos en MinIO utilizando varios métodos.
    - Depurar errores comunes en el proceso de ingesta de datos utilizando el panel de Grafana y los registros de tu instancia de wis2box.
    - Monitorear las notificaciones de datos WIS2 publicadas por tu wis2box en el panel de Grafana y MQTT Explorer.
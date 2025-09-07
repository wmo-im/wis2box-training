---
title: Ingestando datos para su publicación
---

# Ingestando datos para su publicación

!!! abstract "Resultados de aprendizaje"

    Al final de esta sesión práctica, serás capaz de:
    
    - Activar el flujo de trabajo de wis2box subiendo datos a MinIO utilizando la interfaz web de MinIO, SFTP o un script en Python.
    - Acceder al panel de Grafana para monitorear el estado de la ingestión de datos y ver los registros de tu instancia de wis2box.
    - Ver notificaciones de datos de WIS2 publicadas por tu wis2box utilizando MQTT Explorer.

## Introducción

En WIS2, los datos se comparten en tiempo real utilizando notificaciones de datos de WIS2 que contienen un enlace "canónico" desde el cual se pueden descargar los datos.

Para activar el flujo de trabajo de datos en un WIS2 Node utilizando el software wis2box, los datos deben subirse al bucket **wis2box-incoming** en **MinIO**, lo que inicia el flujo de trabajo de wis2box. Este proceso da como resultado la publicación de los datos a través de una notificación de datos de WIS2. Dependiendo de los mapeos de datos configurados en tu instancia de wis2box, los datos pueden transformarse al formato BUFR antes de ser publicados.

En este ejercicio, utilizaremos archivos de datos de muestra para activar el flujo de trabajo de wis2box y **publicar notificaciones de datos de WIS2** para el conjunto de datos que configuraste en la sesión práctica anterior.

Durante el ejercicio, monitorearemos el estado de la ingestión de datos utilizando el **panel de Grafana** y **MQTT Explorer**. El panel de Grafana utiliza datos de Prometheus y Loki para mostrar el estado de tu wis2box, mientras que MQTT Explorer te permite ver las notificaciones de datos de WIS2 publicadas por tu instancia de wis2box.

En este ejercicio, nos centraremos en los diferentes métodos para subir datos a tu instancia de wis2box y verificar la ingestión y publicación exitosa. La transformación de datos se cubrirá más adelante en la sesión práctica [Herramientas de Conversión de Datos](./data-conversion-tools.md).

## Preparación

Esta sección utiliza el conjunto de datos para "surface-based-observations/synop" y "other" previamente creado en la sesión práctica [Configurando Conjuntos de Datos en wis2box](./configuring-wis2box-datasets.md).

También requiere conocimiento sobre la configuración de estaciones en la **wis2box-webapp**, como se describe en la sesión práctica [Configurando Metadatos de Estaciones](./configuring-station-metadata.md).

Asegúrate de poder iniciar sesión en tu máquina virtual de estudiante utilizando tu cliente SSH (por ejemplo, PuTTY).

Asegúrate de que wis2box esté en funcionamiento:

```bash
cd ~/wis2box/
python3 wis2box-ctl.py start
python3 wis2box-ctl.py status
```

Asegúrate de que MQTT Explorer esté en ejecución y conectado a tu instancia utilizando las credenciales públicas `everyone/everyone` con una suscripción al tema `origin/a/wis2/#`.

Asegúrate de tener un navegador web abierto con el panel de Grafana para tu instancia navegando a `http://YOUR-HOST:3000`.

## Ingestando datos utilizando la interfaz de MinIO

Primero, utilizaremos la interfaz web de MinIO, que permite descargar y subir datos a MinIO utilizando un navegador web.

### Accediendo a la interfaz de MinIO

Abre la interfaz web de MinIO, generalmente disponible en `http://YOUR-HOST:9001`.

<img alt="Minio UI: minio ui" src="/../assets/img/minio-ui.png" width="400">

Las credenciales WIS2BOX_STORAGE_USERNAME y WIS2BOX_STORAGE_PASSWORD se pueden encontrar en el archivo wis2box.env.

Si no estás seguro de los valores, navega al directorio raíz de tu wis2box y ejecuta el siguiente comando para mostrar solo las credenciales relevantes:

```bash
grep -E '^(WIS2BOX_STORAGE_USERNAME|WIS2BOX_STORAGE_PASSWORD)=' wis2box.env
```
Utiliza los valores de WIS2BOX_STORAGE_USERNAME y WIS2BOX_STORAGE_PASSWORD como nombre de usuario y contraseña al iniciar sesión en MinIO.

### Ingestar y Publicar utilizando el plugin Universal

Descarga los datos de muestra geps [geps_202508180000.grib2](../sample-data/geps_202508180000.grib2) en tu entorno local:

Selecciona el bucket wis2box-incoming y haz clic en `Create new path`.

<img alt="minio ui: create new path" src="/../assets/img/minio-create-new-path.png" width="800">

El nombre de la ruta debe corresponder al Identificador de Metadatos de tu conjunto de datos "other", que creaste previamente en la sesión práctica [Configurando Conjuntos de Datos en wis2box](./configuring-wis2box-datasets.md).

<img alt="minio ui: create new path empty" src="/../assets/img/minio-ui-create-path-empty.png" width="700">

Por lo tanto, en este caso, crea el directorio:

```bash
urn:wmo:md:my-centre-id:my-other-dataset
```

Entra en el directorio recién creado, haz clic en `Upload`, encuentra el archivo [geps_202508180000.grib2](../sample-data/geps_202508180000.grib2) que descargaste en tu máquina local anteriormente y sube este archivo al bucket wis2box-incoming.

<img alt="minio ui: upload your file" src="/../assets/img/minio-other-dataset-upload.png" width="650">

Una vez que termines de subirlo, verás este archivo en el bucket wis2box-incoming de MinIO:

<img alt="minio ui: upload your file" src="/../assets/img/minio-geps-file-upload.png" width="650">

Después de subirlo, verifica con MQTT Explorer para confirmar que los datos se publicaron exitosamente.

<img alt="Metadata Editor: title, description, keywords" src="/../assets/img/mqtt-explorer-wis2-notification-geps-sample.png" width="800">

A continuación, descarga los datos de muestra geps en una extensión de archivo diferente [geps_202508180000.nc](../sample-data/geps_202508180000.nc) en tu entorno local. Sube este archivo al mismo directorio que en el ejercicio anterior.

!!! question "Pregunta"

    ¿Puedes subir exitosamente al bucket wis2box-incoming?

??? success "Haz clic para revelar la respuesta"

    Sí.
    <img alt="Minio ui: geps nc file" src="/../assets/img/minio-upload-geps-with-nc-extension.png" width="800">

!!! question "Pregunta"

    ¿Puedes publicar exitosamente mensajes de notificación de datos a través de MinIO? 
    Verifica el panel de Grafana y MQTT Explorer para ver si los datos se ingresaron y publicaron exitosamente.

!!! hint

    Al crear un conjunto de datos personalizado, ¿qué plugin utilizaste?
    ¿El plugin tiene algún requisito de formato de archivo y dónde están especificados?

??? success "Haz clic para revelar la respuesta"

    No.
    Verás un mensaje indicando que hay un error de tipo de archivo desconocido.

    ```bash
    ERROR - Path validation error: Unknown file type (nc) for metadata_id=urn:wmo:md:nl-knmi-test:customized-geps-dataset-wis2-training. Did not match any of the following:grib2
    ``` 
    
    Esto demuestra que el flujo de trabajo de datos se activó, pero los datos no se volvieron a publicar. El wis2box no publicará los datos si no puede coincidir con la extensión de archivo grib2.

Luego, descarga los datos de muestra geps renombrados [geps_renamed_sample_data.grib2](../sample-data/geps_renamed_sample_data.grib2) en tu entorno local. Sube este archivo al mismo directorio que en los dos ejercicios anteriores.

!!! question "Pregunta"

    ¿Puedes subir exitosamente al bucket wis2box-incoming?

??? success "Haz clic para revelar la respuesta"

    Sí.
    <img alt="Minio ui: geps nc file" src="/../assets/img/minio-upload-renamed-geps.png" width="800">

!!! question "Pregunta"

    ¿Puedes publicar exitosamente mensajes de notificación de datos a través de MinIO? 
    Verifica el panel de Grafana y MQTT Explorer para ver si los datos se ingresaron y publicaron exitosamente.

!!! hint

    ¿El plugin personalizado que utilizaste impone algún requisito o restricción en el nombre del archivo?

??? success "Haz clic para revelar la respuesta"

    No.
        Verás un mensaje indicando que hay un error sobre el patrón del archivo que no coincide con la expresión regular.

    ```bash
    ERROR - ERROR - geps_renamed_sample_data.grib2 did not match ^.*?_(\d{8}).*?\..*$
    ``` 
    
    Esto demuestra que el flujo de trabajo de datos se activó, pero los datos no se volvieron a publicar. El wis2box no publicará los datos si no puede coincidir con el patrón de archivo ^.*?_(\d{8}).*?\..*$.

El plugin Universal proporciona un mecanismo genérico para ingerir y publicar archivos sin aplicar decodificación específica de dominio. En su lugar, realiza un conjunto de verificaciones básicas antes de publicar una notificación de WIS2:

`Extensión de archivo` – el archivo debe usar la extensión permitida por la configuración del conjunto de datos.

`Patrón de nombre de archivo` – el nombre del archivo debe coincidir con la expresión regular definida en el conjunto de datos.

Si se cumplen ambas condiciones, el archivo se ingiere y se publica una notificación.

Subir un archivo a MinIO siempre tiene éxito mientras el usuario tenga acceso. Sin embargo, publicar una notificación de datos WIS2 requiere una validación más estricta. Los archivos que no cumplan con las reglas de extensión o nombre de archivo se almacenarán en el bucket `incoming`, pero el `Universal plugin` no publicará una notificación para ellos. Esto explica por qué archivos con una extensión no soportada (por ejemplo, `geps_202508180000.nc`) o con un nombre de archivo no válido (por ejemplo, `geps_renamed_sample_data.grib2`) son aceptados por MinIO pero no aparecen en WIS2.

A continuación, ve a la interfaz web de MinIO en tu navegador y navega al bucket `wis2box-incoming`. Verás el archivo `geps_202508180000.grib2` que subiste en los ejercicios anteriores.

Haz clic en el archivo, y tendrás la opción de descargarlo:

<img alt="minio-wis2box-incoming-dataset-folder" src="/../assets/img/minio-download.png" width="800">

Por favor, descarga este archivo y vuelve a subirlo a la misma ruta en MinIO para reactivar el flujo de trabajo de wis2box.

!!! question "Pregunta"

    ¿Puedes volver a publicar mensajes de notificación de datos a través de MinIO? 
    Revisa el panel de Grafana y MQTT Explorer para verificar si los datos fueron ingeridos y publicados con éxito.

??? success "Haz clic para revelar la respuesta"

    Verás un mensaje indicando que wis2box ya publicó estos datos:

    ```bash
    ERROR - Data already published for geps_202508180000-grib2; not publishing
    ``` 
    
    Esto demuestra que el flujo de trabajo de datos se activó, pero los datos no se volvieron a publicar. Wis2box no publicará los mismos datos dos veces.

### Ingestar y publicar usando synop2bufr-plugin

Descarga los datos de muestra de synop [synop_202502040900.txt](../sample-data/synop_202502040900.txt) para este ejercicio en tu entorno local:

Como en los ejercicios anteriores, crea un directorio bajo el bucket `wis2box-incoming` que coincida con el Identificador de Metadatos de tu conjunto de datos de observaciones basadas en superficie/synop.

Entra en el directorio recién creado, haz clic en `Upload` y selecciona el archivo [synop_202502040900.txt](../sample-data/synop_202502040900.txt) que descargaste en tu máquina local antes y luego súbelo.

!!! question "Pregunta"

    ¿Puedes publicar con éxito mensajes de notificación de datos a través de MinIO? 
    Revisa el panel de Grafana y MQTT Explorer para verificar si los datos fueron ingeridos y publicados con éxito.

??? success "Haz clic para revelar la respuesta"

    No. 
    En el panel de Grafana verás una advertencia que indica que falta el registro de la estación 64400:

    ```bash
    WARNING - Station 64400 not found in station file
    ``` 
    
    Esto demuestra que el flujo de trabajo de datos se activó, pero se necesita una metadato específico de la estación.

En este caso, estás usando el plugin `FM-12 data converted to BUFR`.

El propósito de este plugin es manejar datos FM-12 proporcionados en formato de texto plano y convertirlos en BUFR binario. Durante este proceso, el plugin necesita analizar y mapear la información de la estación contenida en los datos.

Si falta el metadato esencial de la estación, el plugin no puede analizar el archivo correctamente y la conversión fallará.

Por lo tanto, debes asegurarte de que los metadatos relevantes de la estación se hayan agregado a wis2box antes de publicar datos SYNOP.

Ahora, agreguemos una estación de prueba para este ejercicio.

Agrega la estación con el identificador WIGOS `0-20000-0-64400` a tu instancia de wis2box usando el editor de estaciones en la aplicación web de wis2box.

Recupera la estación desde OSCAR:

<img alt="oscar-station" src="/../assets/img/webapp-test-station-oscar-search.png" width="600">

Agrega la estación a los conjuntos de datos que creaste para publicar en "../surface-based-observations/synop" y guarda los cambios usando tu token de autenticación:

<img alt="webapp-test-station" src="/../assets/img/webapp-test-station-save.png" width="800">

Ten en cuenta que puedes eliminar esta estación de tu conjunto de datos después de la sesión práctica.

Después de terminar de configurar los metadatos de la estación, verifica con MQTT Explorer para confirmar que los datos se publicaron con éxito. Si ves la notificación a continuación, entonces publicaste los datos de muestra de synop con éxito.

<img alt="webapp-test-station" src="/../assets/img/mqtt-explorer-wis2box-notification-synop-sample.png" width="800">

## Ingestar datos usando Python (opcional)

En este ejercicio, usaremos el cliente de Python de MinIO para copiar datos en MinIO.

MinIO proporciona un cliente de Python, que puede instalarse de la siguiente manera:

```bash
pip3 install minio
```

En tu máquina virtual de estudiante, el paquete 'minio' para Python ya estará instalado.

Copia el directorio `exercise-materials/data-ingest-exercises` al directorio que definiste como el `WIS2BOX_HOST_DATADIR` en tu archivo `wis2box.env`:

```bash
cp -r ~/exercise-materials/data-ingest-exercises ~/wis2box-data/
```

!!! note
    El `WIS2BOX_HOST_DATADIR` está montado como `/data/wis2box/` dentro del contenedor de gestión de wis2box por el archivo `docker-compose.yml` incluido en el directorio `wis2box`.
    
    Esto permite compartir datos entre el host y el contenedor.

En el directorio `exercise-materials/data-ingest-exercises`, encontrarás un script de ejemplo `copy_file_to_incoming.py` que puede usarse para copiar archivos en MinIO.

Intenta ejecutar el script para copiar el archivo de datos de muestra `synop_202501030900.txt` en el bucket `wis2box-incoming` en MinIO de la siguiente manera:

```bash
cd ~/wis2box-data/data-ingest-exercises
python3 copy_file_to_incoming.py synop_202501030900.txt
```

!!! note

    Obtendrás un error ya que el script no está configurado para acceder al endpoint de MinIO en tu wis2box aún.

El script necesita conocer el endpoint correcto para acceder a MinIO en tu wis2box. Si wis2box se está ejecutando en tu host, el endpoint de MinIO está disponible en `http://YOUR-HOST:9000`. El script también necesita ser actualizado con tu contraseña de almacenamiento y la ruta en el bucket de MinIO para almacenar los datos.

!!! question "Actualiza el Script e Ingresa los Datos CSV"
    
    Edita el script `copy_file_to_incoming.py` para solucionar los errores, utilizando uno de los siguientes métodos:
    - Desde la línea de comandos: usa el editor de texto `nano` o `vim` para editar el script.
    - Usando WinSCP: inicia una nueva conexión usando el Protocolo de Archivo `SCP` y las mismas credenciales que tu cliente SSH. Navega al directorio `wis2box-data/data-ingest-exercises` y edita `copy_file_to_incoming.py` usando el editor de texto integrado.
    
    Asegúrate de:

    - Definir el endpoint correcto de MinIO para tu host.
    - Proporcionar la contraseña de almacenamiento correcta para tu instancia de MinIO.
    - Proporcionar la ruta correcta en el bucket de MinIO para almacenar los datos.

    Vuelve a ejecutar el script para ingresar el archivo de datos de muestra `synop_202501030900.txt` en MinIO:

    ```bash
    python3 ~/wis2box-data/ ~/wis2box-data/synop_202501030900.txt
    ```

    Asegúrate de que los errores se hayan resuelto.

Una vez que logres ejecutar el script con éxito, verás un mensaje indicando que el archivo fue copiado a MinIO, y deberías ver notificaciones de datos publicadas por tu instancia de wis2box en MQTT Explorer.

También puedes verificar el panel de Grafana para ver si los datos fueron ingeridos y publicados con éxito.

Ahora que el script está funcionando, puedes intentar copiar otros archivos en MinIO usando el mismo script.

!!! question "Ingresar Datos Binarios en Formato BUFR"

    Ejecuta el siguiente comando para copiar el archivo de datos binarios `bufr-example.bin` en el bucket `wis2box-incoming` en MinIO:

    ```bash
    python3 copy_file_to_incoming.py bufr-example.bin
    ```

Revisa el panel de Grafana y MQTT Explorer para ver si los datos de prueba fueron ingeridos y publicados con éxito. Si ves algún error, intenta resolverlo.

!!! question "Verificar la Ingesta de Datos"

    ¿Cuántos mensajes fueron publicados al broker MQTT para esta muestra de datos?

??? success "Haz clic para revelar la respuesta"

    Verás errores reportados en Grafana ya que las estaciones en el archivo BUFR no están definidas en la lista de estaciones de tu instancia de wis2box. 
    
    Si todas las estaciones utilizadas en el archivo BUFR están definidas en tu instancia de wis2box, deberías ver 10 mensajes publicados al broker MQTT. Cada notificación corresponde a datos para una estación en un momento de observación.

    El plugin `wis2box.data.bufr4.ObservationDataBUFR` divide el archivo BUFR en mensajes BUFR individuales y publica un mensaje para cada estación y momento de observación.

## Ingestar datos a través de SFTP (opcional)

El servicio MinIO en wis2box también puede ser accedido a través de SFTP. El servidor SFTP para MinIO está vinculado al puerto 8022 en el host (el puerto 22 se usa para SSH).

En este ejercicio, demostraremos cómo usar WinSCP para subir datos a MinIO usando SFTP.

Puedes configurar una nueva conexión en WinSCP como se muestra en esta captura de pantalla:

<img alt="winscp-sftp-connection" src="/../assets/img/winscp-sftp-login.png" width="400">

Las credenciales para la conexión SFTP están definidas por `WIS2BOX_STORAGE_USERNAME` y `WIS2BOX_STORAGE_PASSWORD` en tu archivo `wis2box.env` y son las mismas credenciales que utilizaste para conectarte a la interfaz de usuario de MinIO.

Cuando inicies sesión, verás los buckets utilizados por wis2box en MinIO:

<img alt="winscp-sftp-bucket" src="/../assets/img/winscp-buckets.png" width="600">

Puedes navegar al bucket `wis2box-incoming` y luego a la carpeta de tu conjunto de datos. Verás los archivos que subiste en los ejercicios anteriores:

<img alt="winscp-sftp-incoming-path" src="/../assets/img/winscp-incoming-data-path.png" width="600">

!!! question "Subir datos usando SFTP"

    Descarga este archivo de ejemplo a tu computadora local:

    [synop_202503030900.txt](./../sample-data/synop_202503030900.txt) (haz clic derecho y selecciona "guardar como" para descargar el archivo).

    Luego súbelo a la ruta del conjunto de datos entrante en MinIO utilizando tu sesión SFTP en WinSCP.

    Verifica el panel de Grafana y MQTT Explorer para confirmar si los datos fueron ingeridos y publicados con éxito.

??? success "Haz clic para revelar la respuesta"

    Deberías ver una nueva notificación de datos WIS2 publicada para la estación de prueba `0-20000-0-64400`, indicando que los datos fueron ingeridos y publicados con éxito.

    <img alt="grafana_data_ingest" src="/../assets/img/grafana_data-ingest-test3.png" width="400"> 

    Si utilizas una ruta incorrecta, verás un mensaje de error en los registros.

## Conclusión

!!! success "¡Felicidades!"
    En esta sesión práctica, aprendiste a:

    - Activar el flujo de trabajo de wis2box subiendo datos a MinIO utilizando varios métodos.
    - Depurar errores comunes en el proceso de ingestión de datos utilizando el panel de Grafana y los registros de tu instancia de wis2box.
    - Monitorear las notificaciones de datos WIS2 publicadas por tu wis2box en el panel de Grafana y MQTT Explorer.
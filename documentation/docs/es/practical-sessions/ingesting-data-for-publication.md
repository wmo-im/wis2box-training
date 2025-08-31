---
title: Ingestión de Datos para Publicación
---

# Ingestión de datos para publicación

!!! abstract "Resultados de Aprendizaje"

    Al final de esta sesión práctica, serás capaz de:
    
    - Activar el flujo de trabajo de wis2box subiendo datos a MinIO utilizando la línea de comandos, la interfaz web de MinIO, SFTP o un script en Python.
    - Acceder al panel de Grafana para monitorear el estado de la ingestión de datos y ver los registros de tu instancia de wis2box.
    - Ver las notificaciones de datos WIS2 publicadas por tu wis2box utilizando MQTT Explorer.

## Introducción

En WIS2, los datos se comparten en tiempo real utilizando notificaciones de datos WIS2 que contienen un enlace "canónico" desde el cual se pueden descargar los datos.

Para activar el flujo de trabajo de datos en un WIS2 Node utilizando el software wis2box, los datos deben subirse al bucket **wis2box-incoming** en **MinIO**, lo que inicia el flujo de trabajo de wis2box. Este proceso da como resultado la publicación de los datos a través de una notificación de datos WIS2. Dependiendo de los mapeos de datos configurados en tu instancia de wis2box, los datos pueden transformarse al formato BUFR antes de ser publicados.

En este ejercicio, utilizaremos archivos de datos de ejemplo para activar el flujo de trabajo de wis2box y **publicar notificaciones de datos WIS2** para el conjunto de datos que configuraste en la sesión práctica anterior.

Durante el ejercicio, monitorearemos el estado de la ingestión de datos utilizando el **panel de Grafana** y **MQTT Explorer**. El panel de Grafana utiliza datos de Prometheus y Loki para mostrar el estado de tu wis2box, mientras que MQTT Explorer te permite ver las notificaciones de datos WIS2 publicadas por tu instancia de wis2box.

Ten en cuenta que wis2box transformará los datos de ejemplo al formato BUFR antes de publicarlos en el broker MQTT, según los mapeos de datos preconfigurados en tu conjunto de datos. Para este ejercicio, nos centraremos en los diferentes métodos para subir datos a tu instancia de wis2box y verificar la ingestión y publicación exitosa. La transformación de datos se cubrirá más adelante en la sesión práctica [Herramientas de Conversión de Datos](./data-conversion-tools.md).

## Preparación

Esta sección utiliza dos conjuntos de datos preparados en la sesión práctica Configuración de Conjuntos de Datos en wis2box:

1. El conjunto de datos predefinido weather/surface-based-observations/synop.

2. Un conjunto de datos personalizado creado con la plantilla Other (ejemplo GEPS).

La ingestión de **weather/surface-based-observations/synop** requiere que los metadatos de la estación estén configurados en wis2box-webapp, como se describe en la sesión práctica [Configuración de Metadatos de Estaciones](./configuring-station-metadata.md).

Para el conjunto de datos **other** utilizado en este entrenamiento, se selecciona el complemento de datos universales sin conversión para publicar archivos GRIB2 sin transformación. Dado que este conjunto de datos de entrenamiento no representa observaciones de estaciones, no es necesario configurar estaciones. Asegúrate de que la extensión del archivo sea .grib2 y que la expresión regular del patrón de archivo coincida con los nombres de tus archivos de datos.

En operaciones reales de WIS2, sin embargo, si el conjunto de datos creado con la plantilla **other** está destinado a publicar datos de observación basados en estaciones, los metadatos de la estación deben crearse y configurarse de la misma manera que para *surface-based-observations/synop*.

Asegúrate de poder iniciar sesión en tu VM de estudiante utilizando tu cliente SSH (por ejemplo, PuTTY).

Asegúrate de que wis2box esté en funcionamiento:

```bash
cd ~/wis2box/
python3 wis2box-ctl.py start
python3 wis2box-ctl.py status
```

Asegúrate de que MQTT Explorer esté en ejecución y conectado a tu instancia utilizando las credenciales públicas `everyone/everyone` con una suscripción al tema `origin/a/wis2/#`.

Asegúrate de tener un navegador web abierto con el panel de Grafana para tu instancia navegando a `http://YOUR-HOST:3000`.

## Preparar Datos de Ejemplo

Copia el directorio `exercise-materials/data-ingest-exercises` al directorio que definiste como `WIS2BOX_HOST_DATADIR` en tu archivo `wis2box.env`:

```bash
cp -r ~/exercise-materials/data-ingest-exercises ~/wis2box-data/
```

!!! note
    El `WIS2BOX_HOST_DATADIR` está montado como `/data/wis2box/` dentro del contenedor wis2box-management por el archivo `docker-compose.yml` incluido en el directorio `wis2box`.
    
    Esto permite compartir datos entre el host y el contenedor.

## Agregar la Estación de Prueba (Solo para datos de observación basados en estaciones)

Vamos a utilizar el conjunto de datos predefinido weather/surface-based-observations/synop que se creó anteriormente en la sesión práctica (./configuring-wis2box-datasdets.md), que es un buen ejemplo basado en observaciones reales de estaciones.

Agrega la estación con el identificador WIGOS `0-20000-0-64400` a tu instancia de wis2box utilizando el editor de estaciones en wis2box-webapp.

Recupera la estación desde OSCAR:

<img alt="oscar-station" src="/../assets/img/webapp-test-station-oscar-search.png" width="600">

Agrega la estación a los conjuntos de datos que creaste para publicar en "../surface-based-observations/synop" y guarda los cambios utilizando tu token de autenticación:

<img alt="webapp-test-station" src="/../assets/img/webapp-test-station-save.png" width="800">

Ten en cuenta que puedes eliminar esta estación de tu conjunto de datos después de la sesión práctica.

## Prueba de Ingestión de Datos desde la Línea de Comandos

En este ejercicio, utilizaremos el comando `wis2box data ingest` para subir datos a MinIO.

Asegúrate de estar en el directorio `wis2box` e inicia sesión en el contenedor **wis2box-management**:

```bash
cd ~/wis2box
python3 wis2box-ctl.py login
```

Verifica que los siguientes datos de ejemplo estén disponibles en el directorio `/data/wis2box/` dentro del contenedor **wis2box-management**:

```bash
ls -lh /data/wis2box/data-ingest-exercises/synop_202412030900.txt
```

!!! question "Ingestión de Datos Usando `wis2box data ingest`"

    Ejecuta el siguiente comando para ingerir el archivo de datos de ejemplo en tu instancia de wis2box:

    ```bash
    wis2box data ingest -p /data/wis2box/data-ingest-exercises/synop_202412030900.txt --metadata-id urn:wmo:md:not-my-centre:synop-test
    ```

    ¿Se ingresaron los datos correctamente? Si no, ¿cuál fue el mensaje de error y cómo puedes solucionarlo?

??? success "Haz clic para Revelar la Respuesta"

    Los datos **no** se ingresaron correctamente. Deberías ver lo siguiente:

    ```bash
    Error: metadata_id=urn:wmo:md:not-my-centre:synop-test not found in data mappings
    ```

    El mensaje de error indica que el identificador de metadatos que proporcionaste no coincide con ninguno de los conjuntos de datos que has configurado en tu instancia de wis2box.

    Proporciona el ID de metadatos correcto que coincida con el conjunto de datos que creaste en la sesión práctica anterior y repite el comando de ingestión de datos hasta que veas la siguiente salida:

    ```bash 
    Processing /data/wis2box/data-ingest-exercises/synop_202412030900.txt
    Done
    ```

Ve a la consola de MinIO en tu navegador y verifica si el archivo `synop_202412030900.txt` se subió al bucket `wis2box-incoming`. Deberías ver un nuevo directorio con el nombre del conjunto de datos que proporcionaste en la opción `--metadata-id`, y dentro de este directorio, encontrarás el archivo `synop_202412030900.txt`:

<img alt="minio-wis2box-incoming-dataset-folder" src="/../assets/img/minio-data-ingest-test-data.png" width="800">

!!! note
    El comando `wis2box data ingest` subió el archivo al bucket `wis2box-incoming` en MinIO en un directorio nombrado según el identificador de metadatos que proporcionaste.

Ve al panel de Grafana en tu navegador y verifica el estado de la ingestión de datos.

!!! question "Verificar el Estado de la Ingestión de Datos en Grafana"
    
    Ve al panel de Grafana en **http://your-host:3000** y verifica el estado de la ingestión de datos en tu navegador.
    
    ¿Cómo puedes saber si los datos se ingresaron y publicaron correctamente?

??? success "Haz clic para Revelar la Respuesta"
    
    Si ingresaste los datos correctamente, deberías ver lo siguiente:
    
    <img alt="grafana_data_ingest" src="/../assets/img/grafana_data-ingest-test.png" width="400">  
    
    Si no ves esto, verifica los mensajes de WARNING o ERROR que se muestran en la parte inferior del panel e intenta resolverlos.

!!! question "Verificar el Broker MQTT para Notificaciones WIS2"
    
    Ve a MQTT Explorer y verifica si puedes ver el mensaje de notificación WIS2 para los datos que acabas de ingresar.
    
    ¿Cuántas notificaciones de datos WIS2 fueron publicadas por tu wis2box?
    
    ¿Cómo accedes al contenido de los datos que se están publicando?

??? success "Haz clic para Revelar la Respuesta"

    Deberías ver 1 notificación de datos WIS2 publicada por tu wis2box.

    Para acceder al contenido de los datos que se están publicando, puedes expandir la estructura del tema para ver los diferentes niveles del mensaje hasta llegar al último nivel y revisar el contenido del mensaje.

El contenido del mensaje tiene una sección "links" con una clave "rel" de "canonical" y una clave "href" con la URL para descargar los datos. La URL tendrá el formato `http://YOUR-HOST/data/...`.

Ten en cuenta que el formato de los datos es BUFR, y necesitarás un analizador BUFR para visualizar el contenido de los datos. El formato BUFR es un formato binario utilizado por los servicios meteorológicos para intercambiar datos. Los complementos de datos dentro de wis2box transformaron los datos a BUFR antes de publicarlos.

Después de completar este ejercicio, sal del contenedor **wis2box-management**:

```bash
exit
```

## Subir datos usando SFTP (Opcional)

El servicio MinIO en wis2box también puede ser accedido mediante SFTP. El servidor SFTP para MinIO está vinculado al puerto 8022 en el host (el puerto 22 se utiliza para SSH).

En este ejercicio, demostraremos cómo usar WinSCP para subir datos a MinIO utilizando SFTP.

Puedes configurar una nueva conexión en WinSCP como se muestra en esta captura de pantalla:

<img alt="winscp-sftp-connection" src="/../assets/img/winscp-sftp-login.png" width="400">

Las credenciales para la conexión SFTP están definidas por `WIS2BOX_STORAGE_USERNAME` y `WIS2BOX_STORAGE_PASSWORD` en tu archivo `wis2box.env` y son las mismas que usaste para conectarte a la interfaz de usuario de MinIO.

Cuando inicies sesión, verás los buckets utilizados por wis2box en MinIO:

<img alt="winscp-sftp-bucket" src="/../assets/img/winscp-buckets.png" width="600">

Puedes navegar al bucket `wis2box-incoming` y luego a la carpeta de tu conjunto de datos. Verás los archivos que subiste en los ejercicios anteriores:

<img alt="winscp-sftp-incoming-path" src="/../assets/img/winscp-incoming-data-path.png" width="600">

!!! question "Subir datos usando SFTP"

    Descarga este archivo de ejemplo a tu computadora local:

    [synop_202503030900.txt](./../sample-data/synop_202503030900.txt) (haz clic derecho y selecciona "guardar como" para descargar el archivo).

    Luego súbelo a la ruta del conjunto de datos entrante en MinIO utilizando tu sesión SFTP en WinSCP.

    Verifica el panel de control de Grafana y MQTT Explorer para comprobar si los datos fueron ingeridos y publicados con éxito.

??? success "Haz clic para revelar la respuesta"

    Deberías ver una nueva notificación de datos WIS2 publicada para la estación de prueba `0-20000-0-64400`, indicando que los datos fueron ingeridos y publicados con éxito.

    <img alt="grafana_data_ingest" src="/../assets/img/grafana_data-ingest-test3.png" width="400"> 

    Si usas una ruta incorrecta, verás un mensaje de error en los registros.

## Subir datos usando un script de Python (Opcional)

En este ejercicio, utilizaremos el cliente de Python de MinIO para copiar datos en MinIO.

MinIO proporciona un cliente de Python, que puede instalarse de la siguiente manera:

```bash
pip3 install minio
```

En tu máquina virtual de estudiante, el paquete 'minio' para Python ya estará instalado.

En el directorio `exercise-materials/data-ingest-exercises`, encontrarás un script de ejemplo llamado `copy_file_to_incoming.py` que puede usarse para copiar archivos en MinIO.

Intenta ejecutar el script para copiar el archivo de datos de ejemplo `synop_202501030900.txt` en el bucket `wis2box-incoming` en MinIO de la siguiente manera:

```bash
cd ~/wis2box-data/data-ingest-exercises
python3 copy_file_to_incoming.py synop_202501030900.txt
```

!!! note

    Obtendrás un error porque el script no está configurado para acceder al endpoint de MinIO en tu wis2box.

El script necesita conocer el endpoint correcto para acceder a MinIO en tu wis2box. Si wis2box se está ejecutando en tu host, el endpoint de MinIO está disponible en `http://YOUR-HOST:9000`. El script también necesita ser actualizado con tu contraseña de almacenamiento y la ruta en el bucket de MinIO donde se almacenarán los datos.

!!! question "Actualizar el script e ingerir los datos CSV"
    
    Edita el script `copy_file_to_incoming.py` para solucionar los errores, utilizando uno de los siguientes métodos:
    - Desde la línea de comandos: usa el editor de texto `nano` o `vim` para editar el script.
    - Usando WinSCP: inicia una nueva conexión utilizando el protocolo de archivo `SCP` y las mismas credenciales que tu cliente SSH. Navega al directorio `wis2box-data/data-ingest-exercises` y edita `copy_file_to_incoming.py` utilizando el editor de texto integrado.
    
    Asegúrate de:

    - Definir el endpoint correcto de MinIO para tu host.
    - Proporcionar la contraseña de almacenamiento correcta para tu instancia de MinIO.
    - Proporcionar la ruta correcta en el bucket de MinIO para almacenar los datos.

    Vuelve a ejecutar el script para ingerir el archivo de datos de ejemplo `synop_202501030900.txt` en MinIO:

    ```bash
    python3 ~/wis2box-data/ ~/wis2box-data/synop_202501030900.txt
    ```

    Asegúrate de que los errores se resuelvan.

Una vez que logres ejecutar el script con éxito, verás un mensaje indicando que el archivo fue copiado a MinIO, y deberías ver notificaciones de datos publicadas por tu instancia de wis2box en MQTT Explorer.

También puedes verificar el panel de control de Grafana para comprobar si los datos fueron ingeridos y publicados con éxito.

Ahora que el script funciona, puedes intentar copiar otros archivos en MinIO utilizando el mismo script.

!!! question "Ingesta de datos binarios en formato BUFR"

    Ejecuta el siguiente comando para copiar el archivo de datos binarios `bufr-example.bin` en el bucket `wis2box-incoming` en MinIO:

    ```bash
    python3 copy_file_to_incoming.py bufr-example.bin
    ```

Verifica el panel de control de Grafana y MQTT Explorer para comprobar si los datos de prueba fueron ingeridos y publicados con éxito. Si ves algún error, intenta resolverlo.

!!! question "Verificar la ingesta de datos"

    ¿Cuántos mensajes fueron publicados en el broker MQTT para esta muestra de datos?

??? success "Haz clic para revelar la respuesta"

    Verás errores reportados en Grafana porque las estaciones en el archivo BUFR no están definidas en la lista de estaciones de tu instancia de wis2box. 
    
    Si todas las estaciones utilizadas en el archivo BUFR están definidas en tu instancia de wis2box, deberías ver 10 mensajes publicados en el broker MQTT. Cada notificación corresponde a los datos de una estación para una marca de tiempo de observación.

    El complemento `wis2box.data.bufr4.ObservationDataBUFR` divide el archivo BUFR en mensajes BUFR individuales y publica un mensaje para cada estación y marca de tiempo de observación.

## Subir datos usando la interfaz web de MinIO 

En los primeros tres métodos de ingesta, hemos utilizado de manera consistente el conjunto de datos basado en estaciones (synop) y sus datos de observación asociados. En esta sección, introduciremos un cuarto método, uno de los enfoques más comúnmente utilizados. Aquí trabajaremos con el conjunto de datos "Other" e ingeriremos datos GEPS utilizando la interfaz web de MinIO, que permite subir y descargar datos directamente a través de un navegador web.

### Iniciar sesión en el navegador de MinIO

Abre la interfaz web de MinIO (generalmente disponible en http://localhost:9001).

Las credenciales `WIS2BOX_STORAGE_USERNAME` y `WIS2BOX_STORAGE_PASSWORD` se pueden encontrar en el archivo `wis2box.env`.

### Navegar al bucket wis2box-incoming

Selecciona el bucket `wis2box-incoming` y haz clic en Crear nueva ruta. El nombre del directorio debe corresponder al Identificador de Metadatos de tu conjunto de datos. Para este entrenamiento, utilizamos el conjunto de datos GEPS creado previamente, así que crea el directorio:

```bash
urn:wmo:md:nl-knmi-test:customized-geps-dataset-wis2-training
```

### Subir archivos de datos GEPS

Entra en el directorio recién creado, haz clic en Subir y selecciona los archivos de datos GEPS locales para subir.

<img alt="minio-incoming-path" src="/../assets/img/minio-incoming-data-GEPS.png" width="800">

### Verificar el éxito de la subida con MQTT Explorer

Después de subir los archivos, verifica con MQTT Explorer para confirmar que los datos fueron publicados con éxito.

Si no fue exitoso, verifica lo siguiente:

1. Comprueba qué complemento fue configurado para el conjunto de datos GEPS. Una discrepancia entre el nombre del archivo y la expresión regular configurada puede impedir la ingesta. Ajusta la expresión regular o renombra los archivos de datos para que coincidan.

2. Reinicia wis2box y repite el proceso de subida.

Una vez que los datos se publiquen con éxito, verás un mensaje de confirmación similar al siguiente:

<img alt="minio-incoming-path" src="/../assets/img/minio-incoming-data-path-publish.png" width="800">

!!! question "Volver a subir datos usando la interfaz web de MinIO"

    Ve a la interfaz web de MinIO en tu navegador y navega al bucket `wis2box-incoming`. Verás el archivo `Z_NAFP_C_BABJ_20250818000000_P_CMA-GEPS-GLB-024` que subiste en los ejercicios anteriores.

    Haz clic en el archivo, y tendrás la opción de descargarlo:

    <img alt="minio-wis2box-incoming-dataset-folder" src="/../assets/img/minio-download.png" width="800">

    Puedes descargar este archivo y volver a subirlo a la misma ruta en MinIO para reactivar el flujo de trabajo de wis2box.

Consulta el panel de Grafana y MQTT Explorer para verificar si los datos fueron ingeridos y publicados con éxito.

??? success "Haz clic para revelar la respuesta"

    Verás un mensaje indicando que el wis2box ya publicó estos datos:

    ```bash
    ERROR - Data already published for Z_NAFP_C_BABJ_20250818000000_P_CMA-GEPS-GLB-024-grib2; not publishing
    ``` 
    
    Esto demuestra que el flujo de trabajo de datos fue activado, pero los datos no se volvieron a publicar. El wis2box no publicará los mismos datos dos veces.

Para **otros** conjuntos de datos:

## Conclusión

!!! success "¡Felicidades!"
    En esta sesión práctica, aprendiste a:

    - Activar el flujo de trabajo de wis2box subiendo datos a MinIO utilizando varios métodos.
    - Depurar errores comunes en el proceso de ingestión de datos utilizando el panel de Grafana y los registros de tu instancia de wis2box.
    - Monitorear las notificaciones de datos WIS2 publicadas por tu wis2box en el panel de Grafana y MQTT Explorer.
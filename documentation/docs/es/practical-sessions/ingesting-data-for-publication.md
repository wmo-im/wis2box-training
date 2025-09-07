---
title: Ingestar datos para su publicación
---

# Ingestar datos para su publicación

!!! abstract "Resultados de aprendizaje"

    Al final de esta sesión práctica, serás capaz de:
    
    - Activar el flujo de trabajo de wis2box subiendo datos a MinIO utilizando la interfaz web de MinIO, SFTP o un script en Python.
    - Acceder al panel de Grafana para monitorear el estado de la ingesta de datos y ver los registros de tu instancia de wis2box.
    - Ver notificaciones de datos WIS2 publicadas por tu wis2box utilizando MQTT Explorer.

## Introducción

En WIS2, los datos se comparten en tiempo real mediante notificaciones de datos WIS2 que contienen un enlace "canónico" desde el cual se pueden descargar los datos.

Para activar el flujo de trabajo de datos en un WIS2 Node utilizando el software wis2box, los datos deben subirse al bucket **wis2box-incoming** en **MinIO**, lo que inicia el flujo de trabajo de wis2box. Este proceso da como resultado la publicación de los datos a través de una notificación de datos WIS2. Dependiendo de los mapeos de datos configurados en tu instancia de wis2box, los datos pueden transformarse al formato BUFR antes de ser publicados.

En este ejercicio, utilizaremos archivos de datos de ejemplo para activar el flujo de trabajo de wis2box y **publicar notificaciones de datos WIS2** para el conjunto de datos que configuraste en la sesión práctica anterior.

Durante el ejercicio, monitorearemos el estado de la ingesta de datos utilizando el **panel de Grafana** y **MQTT Explorer**. El panel de Grafana utiliza datos de Prometheus y Loki para mostrar el estado de tu wis2box, mientras que MQTT Explorer te permite ver las notificaciones de datos WIS2 publicadas por tu instancia de wis2box.

Ten en cuenta que wis2box transformará los datos de ejemplo al formato BUFR antes de publicarlos en el broker MQTT, según los mapeos de datos preconfigurados en tu conjunto de datos. Para este ejercicio, nos centraremos en los diferentes métodos para subir datos a tu instancia de wis2box y verificar la ingesta y publicación exitosas. La transformación de datos se cubrirá más adelante en la sesión práctica [Herramientas de Conversión de Datos](./data-conversion-tools.md).

## Preparación

Esta sección utiliza el conjunto de datos para "surface-based-observations/synop" y "other" creado previamente en la sesión práctica [Configuración de Conjuntos de Datos en wis2box](./configuring-wis2box-datasets.md).

También requiere conocimiento sobre la configuración de estaciones en la **wis2box-webapp**, como se describe en la sesión práctica [Configuración de Metadatos de Estaciones](./configuring-station-metadata.md).

Asegúrate de poder iniciar sesión en tu VM de estudiante utilizando tu cliente SSH (por ejemplo, PuTTY).

Asegúrate de que wis2box esté funcionando:

```bash
cd ~/wis2box/
python3 wis2box-ctl.py start
python3 wis2box-ctl.py status
```

Asegúrate de que MQTT Explorer esté ejecutándose y conectado a tu instancia utilizando las credenciales públicas `everyone/everyone` con una suscripción al tema `origin/a/wis2/#`.

Asegúrate de tener un navegador web abierto con el panel de Grafana para tu instancia navegando a `http://YOUR-HOST:3000`.

### Preparar datos de ejemplo

Copia el directorio `exercise-materials/data-ingest-exercises` al directorio que definiste como `WIS2BOX_HOST_DATADIR` en tu archivo `wis2box.env`:

```bash
cp -r ~/exercise-materials/data-ingest-exercises ~/wis2box-data/
```

!!! note
    El `WIS2BOX_HOST_DATADIR` está montado como `/data/wis2box/` dentro del contenedor wis2box-management por el archivo `docker-compose.yml` incluido en el directorio `wis2box`.
    
    Esto permite compartir datos entre el host y el contenedor.

## Ingestar datos utilizando la interfaz de MinIO

Primero, utilizaremos la interfaz web de MinIO, que permite descargar y subir datos a MinIO utilizando un navegador web.

### Acceder a la interfaz de MinIO

Abre la interfaz web de MinIO (generalmente disponible en http://your-localhost:9001).

Las credenciales WIS2BOX_STORAGE_USERNAME y WIS2BOX_STORAGE_PASSWORD se pueden encontrar en el archivo wis2box.env.

### Ingestar y publicar utilizando el plugin Universal

Descarga los datos de ejemplo universales para este ejercicio desde el siguiente enlace en tu entorno local:  
[sample-data-for-universal-plugin](../sample-data/Z_NAFP_C_BABJ_20250818000000_P_CMA-GEPS-GLB-024.grib2)

Selecciona el bucket wis2box-incoming y haz clic en Crear nueva ruta. El nombre del directorio debe corresponder al Identificador de Metadatos de tu conjunto de datos "other", que creaste previamente en la sesión práctica [Configuración de Conjuntos de Datos en wis2box](./configuring-wis2box-datasets.md). Por lo tanto, en este caso, crea el directorio:

```bash
urn:wmo:md:nl-knmi-test:customized-geps-dataset-wis2-training
```

Ingresa al nuevo directorio creado, haz clic en "Subir" y selecciona el archivo [sample-data-for-universal-plugin](../sample-data/Z_NAFP_C_BABJ_20250818000000_P_CMA-GEPS-GLB-024.grib2) que descargaste previamente en tu máquina local.

Después de subirlo, verifica con MQTT Explorer para confirmar que los datos se publicaron exitosamente.

<img alt="Metadata Editor: title, description, keywords" src="/../assets/img/mqtt-explorer-wis2-notification-geps-sample.png" width="800">

!!! question "Renombrar el archivo a sample-geps-data.grib2"

    Sube el archivo renombrado utilizando la interfaz web a la misma ruta en MinIO que el archivo anterior.

    ¿Se publicará exitosamente el archivo renombrado? ¿Por qué o por qué no?

??? success "Haz clic para revelar la respuesta"

    No, porque al cambiar el nombre del archivo a "sample-geps-data.grib2", no seguirá la regla de expresión regular.

    <img alt="Metadata Editor: title, description, keywords" src="/../assets/img/mqtt-explorer-wis2-notification-geps-regex-error.png" width="800">
    
    Al subir datos, los nombres de los archivos deben cumplir con la convención de nombres requerida definida por una expresión regular:

    ```bash
    ^.*?_(\d{8}).*?\..*$
    ```

    Este patrón exige que cada nombre de archivo contenga:

    Un guion bajo (_), seguido inmediatamente por una cadena de fecha de 8 dígitos en el formato YYYYMMDD (por ejemplo, 20250904).

    Por ejemplo, los siguientes nombres son válidos:

    1. *Z_NAFP_C_BABJ_20250904_P_CMA-GEPS-GLB-024.grib2*

    2. *forecast_20250904.grib2*

    3. *sample-geps_20250101_data.grib2*

    Un nombre como sample-geps-data.grib2 no será aceptado, porque no contiene la fecha de 8 dígitos requerida.

!!! question "Renombrar la extensión del archivo de .grib2 a .bufr4 (sin cambiar el contenido interno del archivo)"

    Sube el archivo renombrado utilizando la interfaz web a la misma ruta en MinIO que el archivo anterior.

    ¿Se publicará exitosamente el archivo renombrado? ¿Por qué o por qué no?

??? success "Haz clic para revelar la respuesta"

    No, porque al cambiar el formato de datos de "grib2" a "bufr4", no seguirá la regla de extensión de archivo que definiste al crear ese conjunto de datos.

    <img alt="Metadata Editor: title, description, keywords" src="/../assets/img/mqtt-explorer-wis2-notification-geps-file-extension-error.png" width="800">
    
    Al subir datos utilizando el plugin Universal, el archivo debe tener la extensión de archivo correcta según lo definido en la configuración del conjunto de datos. Este requisito asegura que el proceso de ingesta pueda reconocer y manejar correctamente el formato del archivo. Por ejemplo, si el conjunto de datos está configurado para archivos grib2, solo se aceptarán archivos que terminen en .grib2. Usar una extensión incorrecta (por ejemplo, .txt o .bin) hará que el archivo sea rechazado y no se publique.

!!! question "Volver a subir datos utilizando la interfaz web de MinIO"

    Ve a la interfaz web de MinIO en tu navegador y navega al bucket `wis2box-incoming`. Verás el archivo `Z_NAFP_C_BABJ_20250818000000_P_CMA-GEPS-GLB-024.grib2` que subiste en los ejercicios anteriores.

    Haz clic en el archivo y tendrás la opción de descargarlo:

    <img alt="minio-wis2box-incoming-dataset-folder" src="/../assets/img/minio-download.png" width="800">

    Puedes descargar este archivo y volver a subirlo a la misma ruta en MinIO para reactivar el flujo de trabajo de wis2box.

    Verifica el panel de Grafana y MQTT Explorer para ver si los datos se ingirieron y publicaron exitosamente.

??? success "Haz clic para revelar la respuesta"

    Verás un mensaje indicando que wis2box ya publicó estos datos:

    ```bash
    ERROR - Data already published for Z_NAFP_C_BABJ_20250818000000_P_CMA-GEPS-GLB-024-grib2; not publishing
    ``` 
    
    Esto demuestra que el flujo de trabajo de datos se activó, pero los datos no se volvieron a publicar. El wis2box no publicará los mismos datos dos veces.

### Ingestar y publicar utilizando el plugin synop2bufr-plugin

Descargue los datos de muestra de synop [synop_202502040900.txt](../sample-data/synop_202502040900.txt) para este ejercicio desde el enlace a continuación en su entorno local:

Seleccione el bucket wis2box-incoming y haga clic en Crear nueva ruta. El nombre del directorio debe corresponder al Identificador de Metadatos de su conjunto de datos "surface-based-observations/synop", que creó previamente en la sesión práctica [Configuring Datasets in wis2box](./configuring-wis2box-datasets.md). Por lo tanto, en este caso, cree el directorio:

```bash
urn:wmo:md:nl-knmi-test:synop-dataset-wis2-training
```

Ingrese al directorio recién creado, haga clic en "Upload" y seleccione el archivo [synop_202502040900.txt](../sample-data/synop_202502040900.txt) que descargó previamente en su máquina local y luego cárguelo.

!!! question "¿Recibió una nueva notificación indicando que los datos fueron publicados? ¿Por qué?"

??? success "Haga clic para revelar la respuesta"

    No. En el panel de Grafana verá un error que indica que la ingesta falló:

    <img alt="grafana_data_ingest" src="/../assets/img/grafana_data-ingest-error.png" width="800"> 

    Al usar la plantilla del conjunto de datos synop con los complementos synop predeterminados (para datos SYNOP en formato CSV, TXT y BUFR), cada registro debe incluir un identificador de estación válido. La ingesta falla si la estación no es conocida por su instancia de wis2box. Por lo tanto, debe agregar la estación primero antes de publicar datos SYNOP.

    Ahora, agreguemos una estación de prueba para este ejercicio.
    
    Agregue la estación con el identificador WIGOS `0-20000-0-64400` a su instancia de wis2box utilizando el editor de estaciones en la aplicación wis2box-webapp.

    Recupere la estación desde OSCAR:

    <img alt="oscar-station" src="/../assets/img/webapp-test-station-oscar-search.png" width="600">

    Agregue la estación a los conjuntos de datos que creó para publicar en "../surface-based-observations/synop" y guarde los cambios utilizando su token de autenticación:

    <img alt="webapp-test-station" src="/../assets/img/webapp-test-station-save.png" width="800">

    Tenga en cuenta que puede eliminar esta estación de su conjunto de datos después de la sesión práctica.

Después de terminar de configurar los metadatos de la estación, verifique con MQTT Explorer para confirmar que los datos se publicaron correctamente. Si ve la notificación a continuación, entonces publicó los datos de muestra synop con éxito.

<img alt="webapp-test-station" src="/../assets/img/mqtt-explorer-wis2box-notification-synop-sample.png" width="800">

## Ingesta de datos usando Python (opcional)

En este ejercicio, utilizaremos el cliente Python de MinIO para copiar datos en MinIO.

MinIO proporciona un cliente Python, que se puede instalar de la siguiente manera:

```bash
pip3 install minio
```

En su máquina virtual de estudiante, el paquete 'minio' para Python ya estará instalado.

En el directorio `exercise-materials/data-ingest-exercises`, encontrará un script de ejemplo `copy_file_to_incoming.py` que se puede usar para copiar archivos en MinIO.

Intente ejecutar el script para copiar el archivo de datos de muestra `synop_202501030900.txt` en el bucket `wis2box-incoming` en MinIO de la siguiente manera:

```bash
cd ~/wis2box-data/data-ingest-exercises
python3 copy_file_to_incoming.py synop_202501030900.txt
```

!!! note

    Obtendrá un error ya que el script no está configurado para acceder al endpoint de MinIO en su wis2box.

El script necesita conocer el endpoint correcto para acceder a MinIO en su wis2box. Si wis2box se está ejecutando en su host, el endpoint de MinIO está disponible en `http://YOUR-HOST:9000`. El script también debe actualizarse con su contraseña de almacenamiento y la ruta en el bucket de MinIO para almacenar los datos.

!!! question "Actualizar el Script e Ingerir los Datos CSV"
    
    Edite el script `copy_file_to_incoming.py` para solucionar los errores, utilizando uno de los siguientes métodos:
    - Desde la línea de comandos: use el editor de texto `nano` o `vim` para editar el script.
    - Usando WinSCP: inicie una nueva conexión utilizando el Protocolo de Archivo `SCP` y las mismas credenciales que su cliente SSH. Navegue al directorio `wis2box-data/data-ingest-exercises` y edite `copy_file_to_incoming.py` utilizando el editor de texto integrado.
    
    Asegúrese de:

    - Definir el endpoint correcto de MinIO para su host.
    - Proporcionar la contraseña de almacenamiento correcta para su instancia de MinIO.
    - Proporcionar la ruta correcta en el bucket de MinIO para almacenar los datos.

    Ejecute nuevamente el script para ingerir el archivo de datos de muestra `synop_202501030900.txt` en MinIO:

    ```bash
    python3 ~/wis2box-data/ ~/wis2box-data/synop_202501030900.txt
    ```

    Asegúrese de que los errores se hayan resuelto.

Una vez que logre ejecutar el script con éxito, verá un mensaje que indica que el archivo fue copiado a MinIO, y debería ver notificaciones de datos publicadas por su instancia de wis2box en MQTT Explorer.

También puede verificar el panel de Grafana para ver si los datos se ingresaron y publicaron correctamente.

Ahora que el script está funcionando, puede intentar copiar otros archivos en MinIO utilizando el mismo script.

!!! question "Ingesta de Datos Binarios en Formato BUFR"

    Ejecute el siguiente comando para copiar el archivo de datos binarios `bufr-example.bin` en el bucket `wis2box-incoming` en MinIO:

    ```bash
    python3 copy_file_to_incoming.py bufr-example.bin
    ```

Verifique el panel de Grafana y MQTT Explorer para ver si los datos de prueba se ingresaron y publicaron correctamente. Si ve algún error, intente resolverlo.

!!! question "Verificar la Ingesta de Datos"

    ¿Cuántos mensajes se publicaron en el broker MQTT para esta muestra de datos?

??? success "Haga clic para revelar la respuesta"

    Verá errores reportados en Grafana ya que las estaciones en el archivo BUFR no están definidas en la lista de estaciones de su instancia de wis2box. 
    
    Si todas las estaciones utilizadas en el archivo BUFR están definidas en su instancia de wis2box, debería ver 10 mensajes publicados en el broker MQTT. Cada notificación corresponde a datos de una estación para una marca de tiempo de observación.

    El complemento `wis2box.data.bufr4.ObservationDataBUFR` divide el archivo BUFR en mensajes BUFR individuales y publica un mensaje para cada estación y marca de tiempo de observación.

## Ingesta de datos mediante SFTP (opcional)

El servicio MinIO en wis2box también se puede acceder mediante SFTP. El servidor SFTP para MinIO está vinculado al puerto 8022 en el host (el puerto 22 se utiliza para SSH).

En este ejercicio, demostraremos cómo usar WinSCP para cargar datos en MinIO utilizando SFTP.

Puede configurar una nueva conexión WinSCP como se muestra en esta captura de pantalla:

<img alt="winscp-sftp-connection" src="/../assets/img/winscp-sftp-login.png" width="400">

Las credenciales para la conexión SFTP están definidas por `WIS2BOX_STORAGE_USERNAME` y `WIS2BOX_STORAGE_PASSWORD` en su archivo `wis2box.env` y son las mismas que utilizó para conectarse a la interfaz de usuario de MinIO.

Cuando inicie sesión, verá los buckets utilizados por wis2box en MinIO:

<img alt="winscp-sftp-bucket" src="/../assets/img/winscp-buckets.png" width="600">

Puede navegar al bucket `wis2box-incoming` y luego a la carpeta de su conjunto de datos. Verá los archivos que cargó en los ejercicios anteriores:

<img alt="winscp-sftp-incoming-path" src="/../assets/img/winscp-incoming-data-path.png" width="600">

!!! question "Cargar Datos Usando SFTP"

    Descargue este archivo de muestra en su computadora local:

    [synop_202503030900.txt](./../sample-data/synop_202503030900.txt) (haga clic derecho y seleccione "guardar como" para descargar el archivo).

    Luego cárguelo en la ruta del conjunto de datos incoming en MinIO utilizando su sesión SFTP en WinSCP.

    Verifique el panel de Grafana y MQTT Explorer para ver si los datos se ingresaron y publicaron correctamente.

??? success "Haga clic para revelar la respuesta"

    Debería ver una nueva notificación de datos WIS2 publicada para la estación de prueba `0-20000-0-64400`, indicando que los datos se ingresaron y publicaron correctamente.

    <img alt="grafana_data_ingest" src="/../assets/img/grafana_data-ingest-test3.png" width="400"> 

    Si utiliza la ruta incorrecta, verá un mensaje de error en los registros.

## Conclusión

!!! success "¡Felicidades!"
    En esta sesión práctica, aprendió a:

    - Activar el flujo de trabajo de wis2box cargando datos en MinIO utilizando varios métodos.
    - Depurar errores comunes en el proceso de ingesta de datos utilizando el panel de Grafana y los registros de su instancia de wis2box.
    - Monitorear las notificaciones de datos WIS2 publicadas por su wis2box en el panel de Grafana y MQTT Explorer.
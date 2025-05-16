---
title: Ingesta de Datos para Publicación
---

# Ingesta de datos para publicación

!!! abstract "Resultados de Aprendizaje"

    Al final de esta sesión práctica, podrás:
    
    - Activar el flujo de trabajo de wis2box subiendo datos a MinIO usando la línea de comandos, la interfaz web de MinIO, SFTP o un script de Python.
    - Acceder al tablero de Grafana para monitorear el estado de la ingestión de datos y ver los registros de tu instancia de wis2box.
    - Ver las notificaciones de datos WIS2 publicadas por tu wis2box usando MQTT Explorer.

## Introducción

En WIS2, los datos se comparten en tiempo real utilizando notificaciones de datos WIS2 que contienen un enlace "canónico" desde el cual se pueden descargar los datos.

Para activar el flujo de trabajo de datos en un WIS2 Node usando el software wis2box, los datos deben subirse al bucket **wis2box-incoming** en **MinIO**, lo que inicia el flujo de trabajo de wis2box. Este proceso resulta en la publicación de los datos a través de una notificación de datos WIS2. Dependiendo de las configuraciones de mapeo de datos en tu instancia de wis2box, los datos pueden transformarse al formato BUFR antes de ser publicados.

En este ejercicio, utilizaremos archivos de datos de muestra para activar el flujo de trabajo de wis2box y **publicar notificaciones de datos WIS2** para el conjunto de datos que configuraste en la sesión práctica anterior.

Durante el ejercicio, monitorearemos el estado de la ingestión de datos usando el **tablero de Grafana** y **MQTT Explorer**. El tablero de Grafana utiliza datos de Prometheus y Loki para mostrar el estado de tu wis2box, mientras que MQTT Explorer te permite ver las notificaciones de datos WIS2 publicadas por tu instancia de wis2box.

Ten en cuenta que wis2box transformará los datos de ejemplo al formato BUFR antes de publicarlos en el broker MQTT, según los mapeos de datos preconfigurados en tu conjunto de datos. Para este ejercicio, nos centraremos en los diferentes métodos para subir datos a tu instancia de wis2box y verificar la ingestión y publicación exitosas. La transformación de datos se cubrirá más adelante en la sesión práctica [Herramientas de Conversión de Datos](./data-conversion-tools).

## Preparación

Esta sección utiliza el conjunto de datos para "surface-based-observations/synop" previamente creado en la sesión práctica [Configurando Conjuntos de Datos en wis2box](./configuring-wis2box-datasets). También requiere conocimiento sobre la configuración de estaciones en **wis2box-webapp**, como se describe en la sesión práctica [Configuración de Metadatos de Estación](./configuring-station-metadata).

Asegúrate de poder iniciar sesión en tu VM de estudiante usando tu cliente SSH (por ejemplo, PuTTY).

Asegúrate de que wis2box esté en funcionamiento:

```bash
cd ~/wis2box/
python3 wis2box-ctl.py start
python3 wis2box-ctl.py status
```

Asegúrate de que MQTT Explorer esté ejecutándose y conectado a tu instancia usando las credenciales públicas `everyone/everyone` con una suscripción al tema `origin/a/wis2/#`.

Asegúrate de tener un navegador web abierto con el tablero de Grafana para tu instancia navegando a `http://YOUR-HOST:3000`.

### Preparar Datos de Ejemplo

Copia el directorio `exercise-materials/data-ingest-exercises` al directorio que definiste como `WIS2BOX_HOST_DATADIR` en tu archivo `wis2box.env`:

```bash
cp -r ~/exercise-materials/data-ingest-exercises ~/wis2box-data/
```

!!! note
    El `WIS2BOX_HOST_DATADIR` está montado como `/data/wis2box/` dentro del contenedor wis2box-management por el archivo `docker-compose.yml` incluido en el directorio `wis2box`.
    
    Esto te permite compartir datos entre el host y el contenedor.

### Agregar la Estación de Prueba

Agrega la estación con el identificador WIGOS `0-20000-0-64400` a tu instancia de wis2box usando el editor de estaciones en wis2box-webapp.

Recupera la estación de OSCAR:

<img alt="oscar-station" src="/../assets/img/webapp-test-station-oscar-search.png" width="600">

Agrega la estación a los conjuntos de datos que creaste para publicar en "../surface-based-observations/synop" y guarda los cambios usando tu token de autenticación:

<img alt="webapp-test-station" src="/../assets/img/webapp-test-station-save.png" width="800">

Ten en cuenta que puedes eliminar esta estación de tu conjunto de datos después de la sesión práctica.

## Prueba de Ingestión de Datos desde la Línea de Comandos

En este ejercicio, utilizaremos el comando `wis2box data ingest` para subir datos a MinIO.

Asegúrate de estar en el directorio `wis2box` e inicia sesión en el contenedor **wis2box-management**:

```bash
cd ~/wis2box
python3 wis2box-ctl.py login
```

Verifica que los siguientes datos de muestra estén disponibles en el directorio `/data/wis2box/` dentro del contenedor **wis2box-management**:

```bash
ls -lh /data/wis2box/data-ingest-exercises/synop_202412030900.txt
```

!!! question "Ingestión de Datos Usando `wis2box data ingest`"

    Ejecuta el siguiente comando para ingerir el archivo de datos de muestra en tu instancia de wis2box:

    ```bash
    wis2box data ingest -p /data/wis2box/data-ingest-exercises/synop_202412030900.txt --metadata-id urn:wmo:md:not-my-centre:synop-test
    ```

    ¿Se ingirieron los datos con éxito? Si no, ¿cuál fue el mensaje de error y cómo puedes solucionarlo?

??? success "Haz Clic para Revelar la Respuesta"

    Los datos **no** se ingirieron con éxito. Deberías ver lo siguiente:

    ```bash
    Error: metadata_id=urn:wmo:md:not-my-centre:synop-test not found in data mappings
    ```

    El mensaje de error indica que el identificador de metadatos que proporcionaste no coincide con ninguno de los conjuntos de datos que has configurado en tu instancia de wis2box.

    Proporciona el ID de metadatos correcto que coincida con el conjunto de datos que creaste en la sesión práctica anterior y repite el comando de ingestión de datos hasta que veas la siguiente salida:

    ```bash 
    Processing /data/wis2box/data-ingest-exercises/synop_202412030900.txt
    Done
    ```

Ve a la consola de MinIO en tu navegador y verifica si el archivo `synop_202412030900.txt` fue subido al bucket `wis2box-incoming`. Deberías ver un nuevo directorio con el nombre del conjunto de datos que proporcionaste en la opción `--metadata-id`, y dentro de este directorio, encontrarás el archivo `synop_202412030900.txt`:

<img alt="minio-wis2box-incoming-dataset-folder" src="/../assets/img/minio-data-ingest-test-data.png" width="800">

!!! note
    El comando `wis2box data ingest` subió el archivo al bucket `wis2box-incoming` en MinIO en un directorio nombrado según el identificador de metadatos que proporcionaste.

Ve al tablero de Grafana en tu navegador y verifica el estado de la ingestión de datos.

!!! question "Verifica el Estado de la Ingestión de Datos en Grafana"
    
    Ve al tablero de Grafana en **http://your-host:3000** y verifica el estado de la ingestión de datos en tu navegador.
    
    ¿Cómo puedes saber si los datos se ingirieron y publicaron con éxito?

??? success "Haz Clic para Revelar la Respuesta"
    
    Si ingiriste los datos con éxito, deberías ver lo siguiente:
    
    <img alt="grafana_data_ingest" src="/../assets/img/grafana_data-ingest-test.png" width="400">  
    
    Si no ves esto, verifica si hay mensajes de ADVERTENCIA o ERROR mostrados en la parte inferior del tablero e intenta resolverlos.

!!! question "Verifica el Broker MQTT para Notificaciones WIS2"
    
    Ve a MQTT Explorer y verifica si puedes ver el mensaje de notificación WIS2 para los datos que acabas de ingerir.
    
    ¿Cuántas notificaciones de datos WIS2 fueron publicadas por tu wis2box?
    
    ¿Cómo accedes al contenido de los datos publicados?

??? success "Haz Clic para Revelar la Respuesta"

    Deberías ver 1 notificación de datos WIS2 publicada por tu wis2box.

    Para acceder al contenido de los datos publicados, puedes expandir la estructura del tema para ver los diferentes niveles del mensaje hasta llegar al último nivel y revisar el contenido del mensaje.

    El contenido del mensaje tiene una sección de "links" con una clave "rel" de "canonical" y una clave "href" con la URL para descargar los datos. La URL estará en el formato `http://YOUR-HOST/data/...`. 
    
    Ten en cuenta que el formato de los datos es BUFR, y necesitarás un analizador de BUFR para ver el contenido de los datos. El formato BUFR es un formato binario utilizado por los servicios meteorológicos para intercambiar datos. Los complementos de datos dentro de wis2box transformaron los datos a BUFR antes de publicarlos.

Después de completar este ejercicio, sal del contenedor **wis2box-management**:

```bash
exit
```

## Subir Datos Usando la Interfaz Web de MinIO

En los ejercicios anteriores, subiste datos disponibles en el host de wis2box a MinIO usando el comando `wis2box data ingest`. 

A continuación, utilizaremos la interfaz web de MinIO, que te permite descargar y subir datos a MinIO usando un navegador web.

!!! question "Vuelve a Subir Datos Usando la Interfaz Web de MinIO"

    Ve a la interfaz web de MinIO en tu navegador y navega al bucket `wis2box-incoming`. Verás el archivo `synop_202412030900.txt` que subiste en los ejercicios anteriores.

    Haz clic en el archivo, y tendrás la opción de descargarlo:

    <img alt="minio-wis2box-incoming-dataset-folder" src="/../assets/img/minio-download.png" width="800">

    Puedes descargar este archivo y volver a subirlo al mismo camino en MinIO para volver a activar el flujo de trabajo de wis2box.

    Verifica el tablero de Grafana y MQTT Explorer para ver si los datos se ingirieron y publicaron con éxito.

??? success "Haz Clic para Revelar la Respuesta"

    Verás un mensaje indicando que wis2box ya publicó estos datos:

    ```bash
    ERROR - Data already published for WIGOS_0-20000-0-64400_20241203T090000-bufr4; not publishing
    ``` 
    
    Esto demuestra que se activó el flujo de trabajo de datos, pero los datos no se volvieron a publicar. wis2box no publicará los mismos datos dos veces. 
    
!!! question "Sube Nuevos Datos Usando la Interfaz Web de MinIO"
    
    Descarga este archivo de muestra [synop_202502040900.txt](./../../sample-data/synop_202502040900.txt) (haz clic derecho y selecciona "guardar como" para descargar el archivo).
    
    Sube el archivo que descargaste usando la interfaz web al mismo camino en MinIO que el archivo anterior.

    ¿Se ingirieron y publicaron los datos con éxito?

??? success "Haz Clic para Revelar la Respuesta"

    Ve al tablero de Grafana y verifica si los datos se ingirieron y publicaron con éxito.

    Si usas el camino incorrecto, verás un mensaje de error en los registros.

    Si usas el camino correcto, verás una notificación de datos WIS2 más publicada para la estación de prueba `0-20000-0-64400`, indicando que los datos se ingirieron y publicaron con éxito.

    <img alt="grafana_data_ingest" src="/../assets/img/grafana_data-ingest-test2.png" width="400"> 

## Subir Datos Usando SFTP

El servicio MinIO en wis2box también se puede acceder a través de SFTP. El servidor SFTP para MinIO está vinculado al puerto 8022 en el host (el puerto 22 se usa para SSH).

En este ejercicio, demostraremos cómo usar WinSCP para subir datos a MinIO usando SFTP.

Puedes configurar una nueva conexión WinSCP como se muestra en esta captura de pantalla:

<img alt="winscp-sftp-connection" src="/../assets/img/winscp-sftp-login.png" width="400">

Las credenciales para la conexión SFTP están definidas por `WIS2BOX_STORAGE_USERNAME` y `WIS2BOX_STORAGE_PASSWORD` en tu archivo `wis2box.env` y son las mismas que las credenciales que usaste para conectarte a la interfaz de MinIO.

Cuando inicies sesión, verás los buckets utilizados por wis2box en MinIO:

<img alt="winscp-sftp-bucket" src="/../assets/img/winscp-buckets.png" width="600">

Puedes navegar al bucket `wis2box-incoming` y luego a la carpeta de tu conjunto de datos. Verás los archivos que subiste en los ejercicios anteriores:

<img alt="winscp-sftp-incoming-path" src="/../assets/img/winscp-incoming-data-path.png" width="600">

!!! question "Sube Datos Usando SFTP"

    Descarga este archivo de muestra a tu computadora local:

    [synop_202503030900.txt](./../../sample-data/synop_202503030900.txt) (haz clic derecho y selecciona "guardar como" para descargar el archivo).

    Luego súbelo al camino del conjunto de datos entrante en MinIO usando tu sesión SFTP en WinSCP.

    Verifica el tablero de Grafana y MQTT Explorer para ver si los datos se ingirieron y publicaron con éxito.

??? success "Haz Clic para Revelar la Respuesta"

    Deberías ver una nueva notificación de datos WIS2 publicada para la estación de prueba `0-20000-0-64400`, indicando que los datos se ingirieron y publicaron con éxito.

    <img alt="grafana_data_ingest" src="/../assets/img/grafana_data-ingest-test3.png" width="400">

Si utiliza una ruta incorrecta, verá un mensaje de error en los registros.

## Subiendo Datos Usando un Script de Python

En este ejercicio, utilizaremos el cliente de Python de MinIO para copiar datos en MinIO.

MinIO proporciona un cliente de Python, que se puede instalar de la siguiente manera:

```bash
pip3 install minio
```

En su VM de estudiante, el paquete 'minio' para Python ya estará instalado.

En el directorio `exercise-materials/data-ingest-exercises`, encontrará un script de ejemplo `copy_file_to_incoming.py` que se puede usar para copiar archivos en MinIO.

Intente ejecutar el script para copiar el archivo de datos de muestra `synop_202501030900.txt` en el bucket `wis2box-incoming` en MinIO de la siguiente manera:

```bash
cd ~/wis2box-data/data-ingest-exercises
python3 copy_file_to_incoming.py synop_202501030900.txt
```

!!! note

    Obtendrá un error ya que el script no está configurado para acceder al punto final de MinIO en su wis2box todavía.

El script necesita conocer el punto final correcto para acceder a MinIO en su wis2box. Si wis2box está ejecutándose en su host, el punto final de MinIO está disponible en `http://YOUR-HOST:9000`. El script también necesita ser actualizado con su contraseña de almacenamiento y la ruta en el bucket de MinIO para almacenar los datos.

!!! question "Actualice el Script e Ingeste los Datos CSV"
    
    Edite el script `copy_file_to_incoming.py` para abordar los errores, utilizando uno de los siguientes métodos:
    - Desde la línea de comandos: use el editor de texto `nano` o `vim` para editar el script.
    - Usando WinSCP: inicie una nueva conexión usando el Protocolo de Archivos `SCP` y las mismas credenciales que su cliente SSH. Navegue hasta el directorio `wis2box-data/data-ingest-exercises` y edite `copy_file_to_incoming.py` usando el editor de texto incorporado.
    
    Asegúrese de que:

    - Defina el punto final correcto de MinIO para su host.
    - Proporcione la contraseña de almacenamiento correcta para su instancia de MinIO.
    - Proporcione la ruta correcta en el bucket de MinIO para almacenar los datos.

    Vuelva a ejecutar el script para ingerir el archivo de datos de muestra `synop_202501030900.txt` en MinIO:

    ```bash
    python3 ~/wis2box-data/ ~/wis2box-data/synop_202501030900.txt
    ```

    Asegúrese de que los errores estén resueltos.

Una vez que logre ejecutar el script con éxito, verá un mensaje indicando que el archivo fue copiado a MinIO, y debería ver notificaciones de datos publicadas por su instancia de wis2box en MQTT Explorer.

También puede verificar el tablero de Grafana para ver si los datos fueron ingeridos y publicados con éxito.

Ahora que el script está funcionando, puede intentar copiar otros archivos en MinIO usando el mismo script.

!!! question "Ingestión de Datos Binarios en Formato BUFR"

    Ejecute el siguiente comando para copiar el archivo de datos binarios `bufr-example.bin` en el bucket `wis2box-incoming` en MinIO:

    ```bash
    python3 copy_file_to_incoming.py bufr-example.bin
    ```

Verifique el tablero de Grafana y MQTT Explorer para ver si los datos de prueba fueron ingeridos y publicados con éxito. Si ve algún error, intente resolverlo.

!!! question "Verifique la Ingesta de Datos"

    ¿Cuántos mensajes se publicaron en el broker MQTT para esta muestra de datos?

??? success "Haga clic para Revelar la Respuesta"

    Verá errores reportados en Grafana ya que las estaciones en el archivo BUFR no están definidas en la lista de estaciones de su instancia de wis2box.
    
    Si todas las estaciones utilizadas en el archivo BUFR están definidas en su instancia de wis2box, debería ver 10 mensajes publicados en el broker MQTT. Cada notificación corresponde a datos de una estación para una marca de tiempo de observación.

    El plugin `wis2box.data.bufr4.ObservationDataBUFR` divide el archivo BUFR en mensajes BUFR individuales y publica un mensaje para cada estación y marca de tiempo de observación.

## Conclusión

!!! success "¡Felicidades!"
    En esta sesión práctica, aprendió cómo:

    - Activar el flujo de trabajo de wis2box subiendo datos a MinIO utilizando varios métodos.
    - Depurar errores comunes en el proceso de ingestión de datos usando el tablero de Grafana y los registros de su instancia de wis2box.
    - Monitorear las notificaciones de datos WIS2 publicadas por su wis2box en el tablero de Grafana y MQTT Explorer.
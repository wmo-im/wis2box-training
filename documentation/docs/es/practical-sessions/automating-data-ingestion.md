---
title: Automatización de la ingestión de datos
---

# Automatización de la ingestión de datos

!!! abstract "Resultados de aprendizaje"

    Al final de esta sesión práctica, serás capaz de:
    
    - entender cómo los plugins de datos de tu conjunto de datos determinan el flujo de trabajo de ingestión de datos
    - ingresar datos en wis2box usando un script con el cliente Python de MinIO
    - ingresar datos en wis2box accediendo a MinIO a través de SFTP

## Introducción

El contenedor **wis2box-management** escucha eventos del servicio de almacenamiento MinIO para activar la ingestión de datos basada en los plugins de datos configurados para tu conjunto de datos. Esto te permite subir datos al bucket de MinIO y activar el flujo de trabajo de wis2box para publicar datos en el broker WIS2.

Los plugins de datos definen los módulos de Python que son cargados por el contenedor **wis2box-management** y determinan cómo se transforman y publican los datos.

En el ejercicio anterior deberías haber creado un conjunto de datos usando la plantilla `surface-based-observations/synop` que incluía los siguientes plugins de datos:

<img alt="mapeos de datos" src="/../assets/img/wis2box-data-mappings.png" width="800">

Cuando se sube un archivo a MinIO, wis2box coincidirá el archivo con un conjunto de datos cuando la ruta del archivo contenga el id del conjunto de datos (`metadata_id`) y determinará los plugins de datos a usar basándose en la extensión del archivo y el patrón de archivo definido en los mapeos del conjunto de datos.

En las sesiones anteriores, activamos el flujo de trabajo de ingestión de datos usando la funcionalidad de línea de comandos de wis2box, que sube datos al almacenamiento de MinIO en la ruta correcta.

Los mismos pasos se pueden realizar programáticamente usando cualquier software cliente de MinIO o S3, permitiéndote automatizar tu ingestión de datos como parte de tus flujos de trabajo operativos.

Alternativamente, también puedes acceder a MinIO usando el protocolo SFTP para subir datos y activar el flujo de trabajo de ingestión de datos.

## Preparación

Inicia sesión en tu VM de estudiante usando tu cliente SSH (PuTTY u otro).

Asegúrate de que wis2box está funcionando:

```bash
cd ~/wis2box-1.0.0rc1/
python3 wis2box-ctl.py start
python3 wis2box-ctl.py status
```

Asegúrate de que MQTT Explorer está funcionando y conectado a tu instancia. Si todavía estás conectado desde la sesión anterior, borra cualquier mensaje anterior que puedas haber recibido de la cola.
Esto se puede hacer desconectándote y reconectándote o haciendo clic en el icono del cubo de basura para el tema dado.

Asegúrate de tener un navegador web abierto con el tablero de Grafana para tu instancia yendo a `http://<tu-host>:3000`

Y asegúrate de tener una segunda pestaña abierta con la interfaz de usuario de MinIO en `http://<tu-host>:9001`. Recuerda que necesitas iniciar sesión con el `WIS2BOX_STORAGE_USER` y `WIS2BOX_STORAGE_PASSWORD` definidos en tu archivo `wis2box.env`.

## Ejercicio 1: configurar un script de Python para ingresar datos en MinIO

En este ejercicio usaremos el cliente Python de MinIO para copiar datos en MinIO.

MinIO proporciona un cliente Python que se puede instalar de la siguiente manera:

```bash
pip3 install minio
```

En tu VM de estudiante el paquete 'minio' para Python ya estará instalado.

Ve al directorio `exercise-materials/data-ingest-exercises`; este directorio contiene un script de muestra `copy_file_to_incoming.py` que usa el cliente Python de MinIO para copiar un archivo en MinIO.

Intenta ejecutar el script para copiar el archivo de datos de muestra `csv-aws-example.csv` en el bucket `wis2box-incoming` en MinIO de la siguiente manera:

```bash
cd ~/exercise-materials/data-ingest-exercises
python3 copy_file_to_incoming.py csv-aws-example.csv
```

!!! note

    Obtendrás un error ya que el script no está configurado para acceder al punto final de MinIO en tu wis2box aún.

El script necesita conocer el punto final correcto para acceder a MinIO en tu wis2box. Si wis2box está ejecutándose en tu host, el punto final de MinIO está disponible en `http://<tu-host>:9000`. El script también necesita ser actualizado con tu contraseña de almacenamiento y la ruta en el bucket de MinIO para almacenar los datos.

!!! question "Actualiza el script e ingresa los datos CSV"
    
    Edita el script `copy_file_to_incoming.py` para corregir los errores, utilizando uno de los siguientes métodos:
    - Desde la línea de comandos: usa el editor de texto `nano` o `vim` para editar el script
    - Usando WinSCP: inicia una nueva conexión usando el Protocolo de Archivo `SCP` y las mismas credenciales que tu cliente SSH. Navega al directorio `exercise-materials/data-ingest-exercises` y edita `copy_file_to_incoming.py` usando el editor de texto incorporado
    
    Asegúrate de:

    - definir el punto final correcto de MinIO para tu host
    - proporcionar la contraseña de almacenamiento correcta para tu instancia de MinIO
    - proporcionar la ruta correcta en el bucket de MinIO para almacenar los datos

    Vuelve a ejecutar el script para ingresar el archivo de datos de muestra `csv-aws-example.csv` en MinIO:

    ```bash
    python3 copy_file_to_incoming.py csv-aws-example.csv
    ```

    Y asegúrate de que los errores estén resueltos.

Puedes verificar que los datos se subieron correctamente revisando la interfaz de usuario de MinIO y viendo si los datos de muestra están disponibles en el directorio correcto en el bucket `wis2box-incoming`.

Puedes usar el tablero de Grafana para verificar el estado del flujo de trabajo de ingestión de datos.

Finalmente, puedes usar MQTT Explorer para verificar si se publicaron notificaciones para los datos que ingresaste. Deberías ver que los datos CSV fueron transformados al formato BUFR y que se publicó una notificación de datos WIS2 con una URL "canónica" para habilitar la descarga de los datos BUFR.

## Ejercicio 2: Ingestión de datos binarios

A continuación, intentaremos ingresar datos binarios en formato BUFR usando el cliente Python de MinIO.

wis2box puede ingresar datos binarios en formato BUFR usando el plugin `wis2box.data.bufr4.ObservationDataBUFR` incluido en wis2box.

Este plugin dividirá el archivo BUFR en mensajes BUFR individuales y publicará cada mensaje en el broker MQTT. Si la estación para el mensaje BUFR correspondiente no está definida en los metadatos de la estación de wis2box, el mensaje no será publicado.

Dado que usaste la plantilla `surface-based-observations/synop` en la sesión anterior, tus mapeos de datos incluyen el plugin `FM-12 data converted to BUFR` para los mapeos del conjunto de datos. Este plugin carga el módulo `wis2box.data.synop2bufr.ObservationDataSYNOP2BUFR` para ingresar los datos.

!!! question "Ingestión de datos binarios en formato BUFR"

    Ejecuta el siguiente comando para copiar el archivo de datos binarios `bufr-example.bin` en el bucket `wis2box-incoming` en MinIO:

    ```bash
    python3 copy_file_to_incoming.py bufr-example.bin
    ```

Revisa el tablero de Grafana y MQTT Explorer para ver si los datos de prueba fueron ingresados y publicados con éxito y si ves algún error, intenta resolverlo.

!!! question "Verifica la ingestión de datos"

    ¿Cuántos mensajes fueron publicados en el broker MQTT para esta muestra de datos?

??? success "Haz clic para revelar la respuesta"

    Si ingresaste y publicaste con éxito la última muestra de datos, deberías haber recibido 10 nuevas notificaciones en el broker MQTT de wis2box. Cada notificación corresponde a datos para una estación para una marca de tiempo de observación.

    El plugin `wis2box.data.bufr4.ObservationDataBUFR` divide el archivo BUFR en mensajes BUFR individuales y publica un mensaje para cada estación y marca de tiempo de observación.

## Ejercicio 3: Ingestión de datos SYNOP en formato ASCII

En la sesión anterior usamos el formulario SYNOP en la **wis2box-webapp** para ingresar datos SYNOP en formato ASCII. También puedes ingresar datos SYNOP en formato ASCII subiéndolos a MinIO.

En la sesión anterior deberías haber creado un conjunto de datos que incluyera el plugin 'FM-12 data converted to BUFR' para los mapeos del conjunto de datos:

<img alt="mapeos del conjunto de datos" src="/../assets/img/wis2box-data-mappings.png" width="800">

Este plugin carga el módulo `wis2box.data.synop2bufr.ObservationDataSYNOP2BUFR` para ingresar los datos.

Intenta usar el cliente Python de MinIO para ingresar los datos de prueba `synop-202307.txt` y `synop-202308.txt` en tu instancia de wis2box.

Ten en cuenta que los 2 archivos contienen el mismo contenido, pero el nombre del archivo es diferente. El nombre del archivo se utiliza para determinar la fecha de la muestra de datos.

El plugin synop2bufr depende de un patrón de archivo para extraer la fecha del nombre del archivo. El primer grupo en la expresión regular se utiliza para extraer el año y el segundo grupo se utiliza para extraer el mes.

!!! question "Ingesta de datos SYNOP FM-12 en formato ASCII"

    Regresa a la interfaz de MinIO en tu navegador y navega al bucket `wis2box-incoming` y al camino donde subiste los datos de prueba en el ejercicio anterior.
    
    Sube los nuevos archivos en el camino correcto en el bucket `wis2box-incoming` en MinIO para activar el flujo de trabajo de ingestión de datos.

    Revisa el tablero de Grafana y MQTT Explorer para ver si los datos de prueba fueron ingresados y publicados con éxito.

    ¿Cuál es la diferencia en el `properties.datetime` entre los dos mensajes publicados en el broker MQTT?

??? success "Haz clic para revelar la respuesta"

    Revisa las propiedades de las últimas 2 notificaciones en MQTT Explorer y notarás que una notificación tiene:

    ```{.copy}
    "properties": {
        "data_id": "wis2/urn:wmo:md:nl-knmi-test:surface-based-observations.synop/WIGOS_0-20000-0-60355_20230703T090000",
        "datetime": "2023-07-03T09:00:00Z",
        ...
    ```

    y la otra notificación tiene:

    ```{.copy}
    "properties": {
        "data_id": "wis2/urn:wmo:md:nl-knmi-test:surface-based-observations.synop/WIGOS_0-20000-0-60355_20230803T09:00:00Z",
        ...
    ```

    El nombre del archivo fue utilizado para determinar el año y el mes de la muestra de datos.

## Ejercicio 4: Ingestión de datos en MinIO usando SFTP

Los datos también pueden ser ingresados en MinIO a través de SFTP.

El servicio MinIO habilitado en el stack de wis2box tiene SFTP habilitado en el puerto 8022. Puedes acceder a MinIO a través de SFTP usando las mismas credenciales que para la interfaz de usuario de MinIO. En este ejercicio usaremos las credenciales de administrador para el servicio MinIO como se define en `wis2box.env`, pero también puedes crear usuarios adicionales en la interfaz de usuario de MinIO.

Para acceder a MinIO a través de SFTP puedes usar cualquier software cliente SFTP. En este ejercicio usaremos WinSCP, que es un cliente SFTP gratuito para Windows.

Usando WinSCP, tu conexión se vería de la siguiente manera:

<img alt="conexión sftp-winscp" src="/../assets/img/winscp-sftp-connection.png" width="400">

Para el nombre de usuario y contraseña, usa los valores de las variables de entorno `WIS2BOX_STORAGE_USERNAME` y `WIS2BOX_STORAGE_PASSWORD` de tu archivo `wis2box.env`. Haz clic en 'guardar' para guardar la sesión y luego en 'iniciar sesión' para conectar.

Cuando inicies sesión verás el bucket `wis2box-incoming` y `wis2box-public` en el directorio raíz. Puedes subir datos al bucket `wis2box-incoming` para activar el flujo de trabajo de ingestión de datos.

Haz clic en el bucket `wis2box-incoming` para navegar a este bucket, luego haz clic derecho y selecciona *Nuevo*->*Directorio* para crear un nuevo directorio en el bucket `wis2box-incoming`.

Crea el directorio *not-a-valid-path* y sube el archivo *randomfile.txt* en este directorio (puedes usar cualquier archivo que desees).

Luego revisa el tablero de Grafana en el puerto 3000 para ver si se activó el flujo de trabajo de ingestión de datos. Deberías ver:

*ERROR - Error de validación de ruta: No se pudo coincidir http://minio:9000/wis2box-incoming/not-a-valid-path/randomfile.txt con el conjunto de datos, la ruta debería incluir uno de los siguientes: ...*

El error indica que el archivo fue subido a MinIO y se activó el flujo de trabajo de ingestión de datos, pero dado que la ruta no coincide con ningún conjunto de datos en la instancia de wis2box, el mapeo de datos falló.

También puedes usar `sftp` desde la línea de comandos:

```bash
sftp -P 8022 -oBatchMode=no -o StrictHostKeyChecking=no <mi-hostname-o-ip>
```
Inicia sesión usando las credenciales definidas en `wis2box.env` para las variables de entorno `WIS2BOX_STORAGE_USERNAME` y `WIS2BOX_STORAGE_PASSWORD`, navega al bucket `wis2box-incoming` y luego crea un directorio y sube un archivo de la siguiente manera:

```bash
cd wis2box-incoming
mkdir not-a-valid-path
cd not-a-valid-path
put ~/exercise-materials/data-ingest-exercises/synop.txt .
```

Esto resultará en un "Error de validación de ruta" en el tablero de Grafana indicando que el archivo fue subido a MinIO.

Para salir del cliente sftp, escribe `exit`. 

!!! Question "Ingesta de datos en MinIO usando SFTP"

    Intenta ingresar el archivo `synop.txt` en tu instancia de wis2box usando SFTP para activar el flujo de trabajo de ingestión de datos.

    Revisa la interfaz de usuario de MinIO para ver si el archivo fue subido al camino correcto en el bucket `wis2box-incoming`.
    
    Revisa el tablero de Grafana para ver si se activó el flujo de trabajo de ingestión de datos o si hubo algún error.

 Para asegurarte de que tus datos se ingieren correctamente, asegúrate de que el archivo se suba en el bucket `wis2box-incoming` en un directorio que coincida con el id del conjunto de datos o el tema de tu conjunto de datos.

## Conclusión

!!! success "¡Felicidades!"
    En esta sesión práctica, aprendiste cómo:

    - activar el flujo de trabajo de wis2box usando un script de Python y el cliente Python de MinIO
    - usar diferentes plugins de datos para ingresar diferentes formatos de datos
    - subir datos a MinIO usando SFTP
---
title: Descarga y decodificación de datos desde WIS2
---

# Descarga y decodificación de datos desde WIS2

!!! abstract "Objetivos de aprendizaje"

    Al finalizar esta sesión práctica, podrás:

    - usar el "wis2downloader" para suscribirte a notificaciones de datos WIS2 y descargar datos a tu sistema local
    - ver el estado de las descargas en el panel de control de Grafana
    - decodificar algunos datos descargados usando el contenedor "decode-bufr-jupyter"

## Introducción

En esta sesión aprenderás cómo configurar una suscripción a un Broker WIS2 y descargar automáticamente datos a tu sistema local usando el servicio "wis2downloader" incluido en wis2box.

!!! note "Acerca de wis2downloader"
     
     El wis2downloader también está disponible como un servicio independiente que puede ejecutarse en un sistema diferente al que está publicando las notificaciones WIS2. Consulta [wis2downloader](https://pypi.org/project/wis2downloader/) para más información sobre el uso de wis2downloader como servicio independiente.

     Si deseas desarrollar tu propio servicio para suscribirte a notificaciones WIS2 y descargar datos, puedes usar el [código fuente de wis2downloader](https://github.com/World-Meteorological-Organization/wis2downloader) como referencia.

!!! Otras herramientas para acceder a datos WIS2

    Las siguientes herramientas también pueden usarse para descubrir y acceder a datos desde WIS2:

    - [pywiscat](https://github.com/wmo-im/pywiscat) proporciona capacidad de búsqueda sobre el WIS2 Global Discovery Catalogue para apoyar el reporte y análisis del Catálogo WIS2 y sus metadatos de descubrimiento asociados
    - [pywis-pubsub](https://github.com/World-Meteorological-Organization/pywis-pubsub) proporciona capacidad de suscripción y descarga de datos WMO desde servicios de infraestructura WIS2

## Preparación

Antes de comenzar, inicia sesión en tu VM de estudiante y asegúrate de que tu instancia wis2box esté funcionando.

## Visualización del panel de wis2downloader en Grafana

Abre un navegador web y navega al panel de control de Grafana para tu instancia wis2box accediendo a `http://YOUR-HOST:3000`.

Haz clic en paneles en el menú de la izquierda, y luego selecciona el **panel de wis2downloader**.

Deberías ver el siguiente panel:

![panel de wis2downloader](../assets/img/wis2downloader-dashboard.png)

Este panel se basa en métricas publicadas por el servicio wis2downloader y te mostrará el estado de las descargas actualmente en progreso.

En la esquina superior izquierda puedes ver las suscripciones que están actualmente activas.

Mantén este panel abierto ya que lo usarás para monitorear el progreso de la descarga en el siguiente ejercicio.

## Revisión de la configuración de wis2downloader

El servicio wis2downloader iniciado por wis2box-stack puede configurarse usando las variables de entorno definidas en tu archivo wis2box.env.

Las siguientes variables de entorno son utilizadas por el wis2downloader:

    - DOWNLOAD_BROKER_HOST: El nombre del host del broker MQTT al que conectarse. Por defecto es globalbroker.meteo.fr
    - DOWNLOAD_BROKER_PORT: El puerto del broker MQTT al que conectarse. Por defecto es 443 (HTTPS para websockets)
    - DOWNLOAD_BROKER_USERNAME: El nombre de usuario para conectarse al broker MQTT. Por defecto es everyone
    - DOWNLOAD_BROKER_PASSWORD: La contraseña para conectarse al broker MQTT. Por defecto es everyone
    - DOWNLOAD_BROKER_TRANSPORT: websockets o tcp, el mecanismo de transporte para conectarse al broker MQTT. Por defecto es websockets
    - DOWNLOAD_RETENTION_PERIOD_HOURS: El período de retención en horas para los datos descargados. Por defecto es 24
    - DOWNLOAD_WORKERS: El número de trabajadores de descarga a utilizar. Por defecto es 8. Determina el número de descargas paralelas.
    - DOWNLOAD_MIN_FREE_SPACE_GB: El espacio libre mínimo en GB a mantener en el volumen que aloja las descargas. Por defecto es 1.

Para revisar la configuración actual del wis2downloader, puedes usar el siguiente comando:

```bash
cat ~/wis2box/wis2box.env | grep DOWNLOAD
```

!!! question "Revisa la configuración del wis2downloader"
    
    ¿Cuál es el broker MQTT predeterminado al que se conecta el wis2downloader?

    ¿Cuál es el período de retención predeterminado para los datos descargados?

??? success "Haz clic para revelar la respuesta"

    El broker MQTT predeterminado al que se conecta el wis2downloader es `globalbroker.meteo.fr`.

    El período de retención predeterminado para los datos descargados es 24 horas.

!!! note "Actualización de la configuración del wis2downloader"

    Para actualizar la configuración del wis2downloader, puedes editar el archivo wis2box.env. Para aplicar los cambios puedes volver a ejecutar el comando de inicio para wis2box-stack:

    ```bash
    python3 wis2box-ctl.py start
    ```

    Y verás que el servicio wis2downloader se reinicia con la nueva configuración.

Puedes mantener la configuración predeterminada para el propósito de este ejercicio.

## Agregar suscripciones al wis2downloader

Dentro del contenedor **wis2downloader**, puedes usar la línea de comandos para listar, agregar y eliminar suscripciones.

Para iniciar sesión en el contenedor **wis2downloader**, usa el siguiente comando:

```bash
python3 wis2box-ctl.py login wis2downloader
```

Luego usa el siguiente comando para listar las suscripciones que están actualmente activas:

```bash
wis2downloader list-subscriptions
```

Este comando devuelve una lista vacía ya que no hay suscripciones activas actualmente.

Para este ejercicio, nos suscribiremos al tema `cache/a/wis2/de-dwd-gts-to-wis2/#`, para suscribirnos a los datos publicados por la pasarela GTS-to-WIS2 alojada en DWD y descargar notificaciones desde el Global Cache.

Para agregar esta suscripción, usa el siguiente comando:

```bash
wis2downloader add-subscription --topic cache/a/wis2/de-dwd-gts-to-wis2/#
```

Luego sal del contenedor **wis2downloader** escribiendo `exit`:

```bash
exit
```

Revisa el panel de wis2downloader en Grafana para ver la nueva suscripción agregada. Espera unos minutos y deberías ver que comienzan las primeras descargas. Continúa con el siguiente ejercicio una vez que hayas confirmado que las descargas están comenzando.

## Visualización de los datos descargados

El servicio wis2downloader en wis2box-stack descarga los datos en el directorio 'downloads' en el directorio que definiste como WIS2BOX_HOST_DATADIR en tu archivo wis2box.env. Para ver el contenido del directorio de descargas, puedes usar el siguiente comando:

```bash
ls -R ~/wis2box-data/downloads
```

Ten en cuenta que los datos descargados se almacenan en directorios nombrados según el tema en el que se publicó la Notificación WIS2.

## Eliminar suscripciones del wis2downloader

A continuación, vuelve a iniciar sesión en el contenedor wis2downloader:

```bash
python3 wis2box-ctl.py login wis2downloader
```

y elimina la suscripción que hiciste del wis2downloader, usando el siguiente comando:

```bash
wis2downloader remove-subscription --topic cache/a/wis2/de-dwd-gts-to-wis2/#
```

Y sal del contenedor wis2downloader escribiendo `exit`:
    
```bash
exit
```

Revisa el panel de wis2downloader en Grafana para ver la suscripción eliminada. Deberías ver que las descargas se detienen.

## Descarga y decodificación de datos para una trayectoria de ciclón tropical

En este ejercicio, te suscribirás al WIS2 Training Broker que está publicando datos de ejemplo para fines de capacitación. Configurarás una suscripción para descargar datos de una trayectoria de ciclón tropical. Luego decodificarás los datos descargados usando el contenedor "decode-bufr-jupyter".

### Suscríbete al wis2training-broker y configura una nueva suscripción

Esto demuestra cómo suscribirse a un broker que no es el predeterminado y te permitirá descargar algunos datos publicados desde el WIS2 Training Broker.

Edita el archivo wis2box.env y cambia el DOWNLOAD_BROKER_HOST a `wis2training-broker.wis2dev.io`, cambia DOWNLOAD_BROKER_PORT a `1883` y cambia DOWNLOAD_BROKER_TRANSPORT a `tcp`:

```copy
# downloader settings
DOWNLOAD_BROKER_HOST=wis2training-broker.wis2dev.io
DOWNLOAD_BROKER_PORT=1883
DOWNLOAD_BROKER_USERNAME=everyone
DOWNLOAD_BROKER_PASSWORD=everyone
# download transport mechanism (tcp or websockets)
DOWNLOAD_BROKER_TRANSPORT=tcp
```

Luego ejecuta el comando 'start' nuevamente para aplicar los cambios:

```bash
python3 wis2box-ctl.py start
```

Revisa los registros del wis2downloader para ver si la conexión al nuevo broker fue exitosa:

```bash
docker logs wis2downloader
```

Deberías ver el siguiente mensaje en el registro:

```copy
...
INFO - Connecting...
INFO - Host: wis2training-broker.wis2dev.io, port: 1883
INFO - Connected successfully
```

Ahora configuraremos una nueva suscripción al tema para descargar datos de trayectoria de ciclones desde el WIS2 Training Broker.

Inicia sesión en el contenedor **wis2downloader**:

```bash
python3 wis2box-ctl.py login wis2downloader
```

Y ejecuta el siguiente comando (copia y pega esto para evitar errores de escritura):

```bash
wis2downloader add-subscription --topic origin/a/wis2/int-wis2-training/data/core/weather/prediction/forecast/medium-range/probabilistic/trajectory
```

Sal del contenedor **wis2downloader** escribiendo `exit`.

Espera hasta que veas que comienzan las descargas en el panel de wis2downloader en Grafana.

!!! note "Descarga de datos desde el WIS2 Training Broker"

    El WIS2 Training Broker es un broker de prueba que se usa para fines de capacitación y puede no publicar datos todo el tiempo.

    Durante las sesiones de capacitación presencial, el instructor local se asegurará de que el WIS2 Training Broker publique datos para que los descargues.

    Si estás haciendo este ejercicio fuera de una sesión de capacitación, es posible que no veas ningún dato siendo descargado.

Verifica que los datos se descargaron revisando nuevamente los registros del wis2downloader con:

```bash
docker logs wis2downloader
```

Deberías ver un mensaje de registro similar al siguiente:

```copy
[...] INFO - Message received under topic origin/a/wis2/int-wis2-training/data/core/weather/prediction/forecast/medium-range/probabilistic/trajectory
[...] INFO - Downloaded A_JSXX05ECEP020000_C_ECMP_...
```

### Decodificación de datos descargados

Para demostrar cómo puedes decodificar los datos descargados, iniciaremos un nuevo contenedor usando la imagen 'decode-bufr-jupyter'.

Este contenedor iniciará un servidor Jupyter notebook en tu instancia que incluye la biblioteca "ecCodes" que puedes usar para decodificar datos BUFR.

Usaremos los cuadernos de ejemplo incluidos en `~/exercise-materials/notebook-examples` para decodificar los datos descargados para las trayectorias de ciclones.

Para iniciar el contenedor, usa el siguiente comando:

```bash
docker run -d --name decode-bufr-jupyter \
    -v ~/wis2box-data/downloads:/root/downloads \
    -p 8888:8888 \
    -e JUPYTER_TOKEN=dataismagic! \
    mlimper/decode-bufr-jupyter
```

!!! note "Acerca del contenedor decode-bufr-jupyter"

    El contenedor `decode-bufr-jupyter` es un contenedor personalizado que incluye la biblioteca ecCodes y ejecuta un servidor Jupyter notebook. El contenedor está basado en una imagen que incluye la biblioteca `ecCodes` para decodificar datos BUFR, junto con bibliotecas para graficar y análisis de datos.

    El comando anterior inicia el contenedor en modo desconectado, con el nombre `decode-bufr-jupyter`, el puerto 8888 está mapeado al sistema host y la variable de entorno `JUPYTER_TOKEN` está configurada como `dataismagic!`.
    
    El comando anterior también monta el directorio `~/wis2box-data/downloads` en `/root/downloads` en el contenedor. Esto asegura que los datos descargados estén disponibles para el servidor Jupyter notebook.
    
Una vez que el contenedor se haya iniciado, puedes acceder al servidor Jupyter notebook navegando a `http://YOUR-HOST:8888` en tu navegador web.

Verás una pantalla solicitando que ingreses una "Contraseña o token".

Proporciona el token `dataismagic!` para iniciar sesión en el servidor Jupyter notebook.

Después de iniciar sesión, deberías ver la siguiente pantalla que lista los directorios en el contenedor:

![Inicio de Jupyter notebook](../assets/img/jupyter-files-screen1.png)

Haz doble clic en el directorio `example-notebooks` para abrirlo.

Deberías ver la siguiente pantalla que lista los cuadernos de ejemplo, haz doble clic en el cuaderno `tropical_cyclone_track.ipynb` para abrirlo:

![Cuadernos de ejemplo de Jupyter notebook](../assets/img/jupyter-files-screen2.png)

Ahora deberías estar en el cuaderno Jupyter para decodificar los datos de trayectoria de ciclón tropical:

![Cuaderno Jupyter de trayectoria de ciclón tropical](../assets/img/jupyter-tropical-cyclone-track.png)

Lee las instrucciones en el cuaderno y ejecuta las celdas para decodificar los datos descargados para las trayectorias de ciclones tropicales. Ejecuta cada celda
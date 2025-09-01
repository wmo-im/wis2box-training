---
title: Descargando datos de WIS2 usando wis2downloader
---

# Descargando datos de WIS2 usando wis2downloader

!!! abstract "¡Resultados de aprendizaje!"

    Al final de esta sesión práctica, serás capaz de:

    - usar el "wis2downloader" para suscribirte a notificaciones de datos de WIS2 y descargar datos en tu sistema local
    - visualizar el estado de las descargas en el panel de Grafana
    - aprender a configurar el wis2downloader para suscribirte a un broker no predeterminado

## Introducción

En esta sesión aprenderás a configurar una suscripción a un WIS2 Broker y descargar automáticamente datos en tu sistema local utilizando el servicio "wis2downloader" incluido en el wis2box.

!!! note "Acerca de wis2downloader"
     
     El wis2downloader también está disponible como un servicio independiente que puede ejecutarse en un sistema diferente al que publica las notificaciones de WIS2. Consulta [wis2downloader](https://pypi.org/project/wis2downloader/) para obtener más información sobre cómo usar el wis2downloader como un servicio independiente.

     Si deseas desarrollar tu propio servicio para suscribirte a notificaciones de WIS2 y descargar datos, puedes usar el [código fuente de wis2downloader](https://github.com/World-Meteorological-Organization/wis2downloader) como referencia.

## Preparación

Antes de comenzar, inicia sesión en tu máquina virtual de estudiante y asegúrate de que tu instancia de wis2box esté en funcionamiento.

## Conceptos básicos de wis2downloader

El wis2downloader está incluido como un contenedor separado en wis2box, tal como se define en los archivos de Docker Compose. El contenedor de Prometheus en wis2box está configurado para recopilar métricas del contenedor de wis2downloader, y estas métricas pueden visualizarse en un panel de Grafana.

### Visualización del panel de wis2downloader en Grafana

Abre un navegador web y navega al panel de Grafana de tu instancia de wis2box accediendo a `http://YOUR-HOST:3000`.

Haz clic en "dashboards" en el menú de la izquierda y luego selecciona el **wis2downloader dashboard**.

Deberías ver el siguiente panel:

![wis2downloader dashboard](../assets/img/wis2downloader-dashboard.png)

Este panel se basa en métricas publicadas por el servicio wis2downloader y te mostrará el estado de las descargas que están actualmente en progreso.

En la esquina superior izquierda, puedes ver las suscripciones que están activas en ese momento.

Mantén este panel abierto, ya que lo usarás para monitorear el progreso de las descargas en el próximo ejercicio.

### Revisión de la configuración de wis2downloader

El servicio wis2downloader en wis2box puede configurarse utilizando las variables de entorno definidas en tu archivo `wis2box.env`.

Las siguientes variables de entorno son utilizadas por el wis2downloader:

    - DOWNLOAD_BROKER_HOST: El nombre del host del broker MQTT al que conectarse. Por defecto es globalbroker.meteo.fr
    - DOWNLOAD_BROKER_PORT: El puerto del broker MQTT al que conectarse. Por defecto es 443 (HTTPS para websockets)
    - DOWNLOAD_BROKER_USERNAME: El nombre de usuario para conectarse al broker MQTT. Por defecto es everyone
    - DOWNLOAD_BROKER_PASSWORD: La contraseña para conectarse al broker MQTT. Por defecto es everyone
    - DOWNLOAD_BROKER_TRANSPORT: websockets o tcp, el mecanismo de transporte para conectarse al broker MQTT. Por defecto es websockets
    - DOWNLOAD_RETENTION_PERIOD_HOURS: El período de retención en horas para los datos descargados. Por defecto es 24
    - DOWNLOAD_WORKERS: El número de trabajadores de descarga a utilizar. Por defecto es 8. Determina el número de descargas paralelas.
    - DOWNLOAD_MIN_FREE_SPACE_GB: El espacio libre mínimo en GB que se debe mantener en el volumen que aloja las descargas. Por defecto es 1.

Para revisar la configuración actual del wis2downloader, puedes usar el siguiente comando:

```bash
cat ~/wis2box/wis2box.env | grep DOWNLOAD
```

!!! question "Revisar la configuración de wis2downloader"
    
    ¿Cuál es el broker MQTT predeterminado al que se conecta el wis2downloader?

    ¿Cuál es el período de retención predeterminado para los datos descargados?

??? success "Haz clic para revelar la respuesta"

    El broker MQTT predeterminado al que se conecta el wis2downloader es `globalbroker.meteo.fr`.

    El período de retención predeterminado para los datos descargados es de 24 horas.

!!! note "Actualizar la configuración de wis2downloader"

    Para actualizar la configuración de wis2downloader, puedes editar el archivo wis2box.env. Para aplicar los cambios, puedes volver a ejecutar el comando de inicio para el stack de wis2box:

    ```bash
    python3 wis2box-ctl.py start
    ```

    Y verás que el servicio wis2downloader se reinicia con la nueva configuración.

Puedes mantener la configuración predeterminada para el próximo ejercicio.

### Interfaz de línea de comandos de wis2downloader

Para acceder a la interfaz de línea de comandos de wis2downloader dentro de wis2box, puedes iniciar sesión en el contenedor **wis2downloader** usando el siguiente comando:

```bash
python3 wis2box-ctl.py login wis2downloader
```

Usa el siguiente comando para listar las suscripciones que están activas actualmente:

```bash
wis2downloader list-subscriptions
```

Este comando devuelve una lista vacía, ya que aún no se han configurado suscripciones.

## Descargar datos GTS usando un WIS2 Global Broker

Si mantuviste la configuración predeterminada de wis2downloader, actualmente está conectado al WIS2 Global Broker alojado por Météo-France.

### Configurar la suscripción

Usa el siguiente comando `cache/a/wis2/de-dwd-gts-to-wis2/#` para suscribirte a los datos publicados por el gateway GTS-to-WIS2 alojado por DWD, disponible a través de los Global Caches:

```bash
wis2downloader add-subscription --topic cache/a/wis2/de-dwd-gts-to-wis2/#
```

Luego, sal del contenedor **wis2downloader** escribiendo `exit`:

```bash
exit
```

### Verificar los datos descargados

Consulta el panel de wis2downloader en Grafana para ver la nueva suscripción añadida. Espera unos minutos y deberías ver que comienzan las primeras descargas. Pasa al siguiente ejercicio una vez que hayas confirmado que las descargas están comenzando.

El servicio wis2downloader en wis2box descarga los datos en el directorio 'downloads' dentro del directorio que definiste como `WIS2BOX_HOST_DATADIR` en tu archivo `wis2box.env`. Para ver el contenido del directorio de descargas, usa el siguiente comando:

```bash
ls -R ~/wis2box-data/downloads
```

Ten en cuenta que los datos descargados se almacenan en directorios nombrados según el tema en el que se publicó la notificación de WIS2.

!!! question "Visualizar los datos descargados"

    ¿Qué directorios ves en el directorio de descargas?

    ¿Puedes ver algún archivo descargado en estos directorios?

??? success "Haz clic para revelar la respuesta"
    Deberías ver una estructura de directorios que comienza con `cache/a/wis2/de-dwd-gts-to-wis2/`, debajo de la cual verás más directorios nombrados según los encabezados de boletines GTS de los datos descargados.

    Dependiendo de cuándo iniciaste la suscripción, es posible que veas o no archivos descargados en este directorio. Si aún no ves archivos, espera unos minutos más y verifica nuevamente.

Vamos a limpiar la suscripción y los datos descargados antes de pasar al siguiente ejercicio.

Vuelve a iniciar sesión en el contenedor wis2downloader:

```bash
python3 wis2box-ctl.py login wis2downloader
```

y elimina la suscripción que creaste en wis2downloader usando el siguiente comando:

```bash
wis2downloader remove-subscription --topic cache/a/wis2/de-dwd-gts-to-wis2/#
```

Elimina los datos descargados usando el siguiente comando:

```bash
rm -rf /wis2box-data/downloads/cache/*
```

Y sal del contenedor wis2downloader escribiendo `exit`:
    
```bash
exit
```

Consulta el panel de wis2downloader en Grafana para ver que la suscripción ha sido eliminada. Deberías ver que las descargas se detienen.

!!! note "Acerca de los gateways GTS-to-WIS2"
    Actualmente hay dos gateways GTS-to-WIS2 que publican datos a través del WIS2 Global Broker y los Global Caches:

    - DWD (Alemania): centre-id=*de-dwd-gts-to-wis2*
    - JMA (Japón): centre-id=*jp-jma-gts-to-wis2*
    
    Si en el ejercicio anterior reemplazas `de-dwd-gts-to-wis2` con `jp-jma-gts-to-wis2`, recibirías las notificaciones y datos publicados por el gateway GTS-to-WIS2 de JMA.

!!! note "Temas de origen vs temas de caché"

    Al suscribirte a un tema que comienza con `origin/`, recibirás notificaciones con una URL canónica que apunta a un servidor de datos proporcionado por el Centro WIS que publica los datos.

    Al suscribirte a un tema que comienza con `cache/`, recibirás múltiples notificaciones para los mismos datos, una por cada Global Cache. Cada notificación contendrá una URL canónica que apunta al servidor de datos de la respectiva Global Cache. El wis2downloader descargará los datos desde la primera URL canónica que pueda alcanzar.

## Descargar datos de ejemplo del WIS2 Training Broker

En este ejercicio, te suscribirás al WIS2 Training Broker, que publica datos de ejemplo con fines de capacitación.

### Cambiar la configuración de wis2downloader

Esto demuestra cómo suscribirse a un broker que no es el broker predeterminado y permitirá descargar algunos datos publicados desde el WIS2 Training Broker.

Edita el archivo `wis2box.env` y cambia `DOWNLOAD_BROKER_HOST` a `wis2training-broker.wis2dev.io`, `DOWNLOAD_BROKER_PORT` a `1883` y `DOWNLOAD_BROKER_TRANSPORT` a `tcp`:

```copy
# downloader settings
DOWNLOAD_BROKER_HOST=wis2training-broker.wis2dev.io
DOWNLOAD_BROKER_PORT=1883
DOWNLOAD_BROKER_USERNAME=everyone
DOWNLOAD_BROKER_PASSWORD=everyone
# download transport mechanism (tcp or websockets)
DOWNLOAD_BROKER_TRANSPORT=tcp
```

Luego ejecuta nuevamente el comando 'start' para aplicar los cambios:

```bash
python3 wis2box-ctl.py start
```

Revisa los logs del wis2downloader para verificar si la conexión al nuevo broker fue exitosa:

```bash
docker logs wis2downloader
```

Deberías ver el siguiente mensaje en los logs:

```copy
...
INFO - Connecting...
INFO - Host: wis2training-broker.wis2dev.io, port: 1883
INFO - Connected successfully
```

### Configurar nuevas suscripciones

Ahora configuraremos una nueva suscripción al tópico para descargar datos de las trayectorias de ciclones desde el WIS2 Training Broker.

Inicia sesión en el contenedor **wis2downloader**:

```bash
python3 wis2box-ctl.py login wis2downloader
```

Y ejecuta el siguiente comando (copia y pega esto para evitar errores tipográficos):

```bash
wis2downloader add-subscription --topic origin/a/wis2/int-wis2-training/data/core/weather/prediction/forecast/medium-range/probabilistic/trajectory
```

Sal del contenedor **wis2downloader** escribiendo `exit`.

### Verificar los datos descargados

Espera hasta que veas que las descargas comienzan en el panel de control de wis2downloader en Grafana.

Verifica que los datos se hayan descargado revisando nuevamente los logs de wis2downloader con:

```bash
docker logs wis2downloader
```

Deberías ver un mensaje en los logs similar al siguiente:

```copy
[...] INFO - Message received under topic origin/a/wis2/int-wis2-training/data/core/weather/prediction/forecast/medium-range/probabilistic/trajectory
[...] INFO - Downloaded A_JSXX05ECEP020000_C_ECMP_...
```

Revisa el contenido del directorio de descargas nuevamente:

```bash
ls -R ~/wis2box-data/downloads
```

Deberías ver un nuevo directorio llamado `origin/a/wis2/int-wis2-training/data/core/weather/prediction/forecast/medium-range/probabilistic/trajectory` que contiene los datos descargados.

!!! question "Revisar los datos descargados"
    
    ¿Cuál es el formato de archivo de los datos descargados?

??? success "Haz clic para revelar la respuesta"

    Los datos descargados están en formato BUFR, como lo indica la extensión de archivo `.bufr`.

A continuación, intenta agregar otras dos suscripciones para descargar anomalías mensuales de temperatura superficial y datos globales de pronósticos de conjuntos desde los siguientes tópicos:

- `origin/a/wis2/int-wis2-training/data/core/weather/prediction/forecast/medium-range/probabilistic/global`
- `origin/a/wis2/int-wis2-training/data/core/climate/experimental/anomalies/monthly/surface-temperature`

Espera hasta que veas que las descargas comienzan en el panel de control de wis2downloader en Grafana.

Revisa el contenido del directorio de descargas nuevamente:

```bash
ls -R ~/wis2box-data/downloads
```

Deberías ver dos nuevos directorios llamados `origin/a/wis2/int-wis2-training/data/core/weather/prediction/forecast/medium-range/probabilistic/global` y `origin/a/wis2/int-wis2-training/data/core/climate/experimental/anomalies/monthly/surface-temperature` que contienen los datos descargados.

!!! question "Revisar los datos descargados para los dos nuevos tópicos"
    
    ¿Cuál es el formato de archivo de los datos descargados para el tópico `../prediction/forecast/medium-range/probabilistic/global`?

    ¿Cuál es el formato de archivo de los datos descargados para el tópico `../climate/experimental/anomalies/monthly/surface-temperature`?

??? success "Haz clic para revelar la respuesta"

    Los datos descargados para el tópico `../prediction/forecast/medium-range/probabilistic/global` están en formato GRIB2, como lo indica la extensión de archivo `.grib2`.

    Los datos descargados para el tópico `../climate/experimental/anomalies/monthly/surface-temperature` están en formato NetCDF, como lo indica la extensión de archivo `.nc`.

## Conclusión

!!! success "¡Felicidades!"

    En esta sesión práctica, aprendiste a:

    - usar el 'wis2downloader' para suscribirte a un WIS2 Broker y descargar datos a tu sistema local
    - ver el estado de las descargas en el panel de control de Grafana
    - cambiar la configuración predeterminada del wis2downloader para suscribirte a un broker diferente
    - visualizar los datos descargados en tu sistema local
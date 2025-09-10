---
title: Inicializando wis2box
---

# Inicializando wis2box

!!! abstract "Resultados de aprendizaje"

    Al final de esta sesión práctica, serás capaz de:

    - ejecutar el script `wis2box-create-config.py` para crear la configuración inicial
    - iniciar wis2box y verificar el estado de sus componentes
    - visualizar el contenido de **wis2box-api**
    - acceder a **wis2box-webapp**
    - conectarte al **wis2box-broker** local utilizando MQTT Explorer

!!! note

    Los materiales de formación actuales están basados en wis2box-release 1.1.0. 
    
    Consulta [accessing-your-student-vm](./accessing-your-student-vm.md) para obtener instrucciones sobre cómo descargar e instalar el conjunto de herramientas de software de wis2box si estás realizando esta formación fuera de una sesión de formación local.

## Preparación

Inicia sesión en tu máquina virtual asignada con tu nombre de usuario y contraseña, y asegúrate de estar en el directorio `wis2box`:

```bash
cd ~/wis2box
```

## Creando la configuración inicial

La configuración inicial de wis2box requiere:

- un archivo de entorno `wis2box.env` que contenga los parámetros de configuración
- un directorio en la máquina anfitriona para compartir entre la máquina anfitriona y los contenedores de wis2box definido por la variable de entorno `WIS2BOX_HOST_DATADIR`

El script `wis2box-create-config.py` puede ser utilizado para crear la configuración inicial de tu wis2box. 

Te hará una serie de preguntas para ayudarte a configurar tu entorno.

Podrás revisar y actualizar los archivos de configuración después de que el script haya finalizado.

Ejecuta el script de la siguiente manera:

```bash
python3 wis2box-create-config.py
```

### Directorio wis2box-host-data

El script te pedirá que ingreses el directorio que se utilizará para la variable de entorno `WIS2BOX_HOST_DATADIR`.

Ten en cuenta que necesitas definir la ruta completa a este directorio.

Por ejemplo, si tu nombre de usuario es `username`, la ruta completa al directorio será `/home/username/wis2box-data`:

```{.copy}
username@student-vm-username:~/wis2box$ python3 wis2box-create-config.py
Please enter the directory to be used for WIS2BOX_HOST_DATADIR:
/home/username/wis2box-data
The directory to be used for WIS2BOX_HOST_DATADIR will be set to:
    /home/username/wis2box-data
Is this correct? (y/n/exit)
y
The directory /home/username/wis2box-data has been created.
```

### URL de wis2box

A continuación, se te pedirá que ingreses la URL de tu wis2box. Esta es la URL que se utilizará para acceder a la aplicación web, API y UI de wis2box.

Por favor, utiliza `http://<your-hostname-or-ip>` como la URL.

```{.copy}
Please enter the URL of the wis2box:
 For local testing the URL is http://localhost
 To enable remote access, the URL should point to the public IP address or domain name of the server hosting the wis2box.
http://username.wis2.training
The URL of the wis2box will be set to:
  http://username.wis2.training
Is this correct? (y/n/exit)
```

### Contraseñas de WEBAPP, STORAGE y BROKER

Puedes utilizar la opción de generación aleatoria de contraseñas cuando se te solicite para `WIS2BOX_WEBAPP_PASSWORD`, `WIS2BOX_STORAGE_PASSWORD`, `WIS2BOX_BROKER_PASSWORD` o definir las tuyas propias.

No te preocupes por recordar estas contraseñas, ya que se almacenarán en el archivo `wis2box.env` dentro del directorio de wis2box.

### Revisar `wis2box.env`

Una vez que el script haya finalizado, verifica el contenido del archivo `wis2box.env` en tu directorio actual:

```bash
cat ~/wis2box/wis2box.env
```

O revisa el contenido del archivo a través de WinSCP.

!!! question

    ¿Cuál es el valor de WISBOX_BASEMAP_URL en el archivo wis2box.env?

??? success "Haz clic para revelar la respuesta"

    El valor predeterminado de WIS2BOX_BASEMAP_URL es `https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png`.

    Esta URL se refiere al servidor de mosaicos de OpenStreetMap. Si deseas usar un proveedor de mapas diferente, puedes cambiar esta URL para apuntar a otro servidor de mosaicos.

!!! question 

    ¿Cuál es el valor de la variable de entorno WIS2BOX_STORAGE_DATA_RETENTION_DAYS en el archivo wis2box.env?

??? success "Haz clic para revelar la respuesta"

    El valor predeterminado de WIS2BOX_STORAGE_DATA_RETENTION_DAYS es de 30 días. Puedes cambiar este valor a un número diferente de días si lo deseas.
    
    El contenedor wis2box-management ejecuta un cronjob diariamente para eliminar datos más antiguos que el número de días definido por WIS2BOX_STORAGE_DATA_RETENTION_DAYS del bucket `wis2box-public` y del backend de la API:
    
    ```{.copy}
    0 0 * * * su wis2box -c "wis2box data clean --days=$WIS2BOX_STORAGE_DATA_RETENTION_DAYS"
    ```

!!! note

    El archivo `wis2box.env` contiene variables de entorno que definen la configuración de tu wis2box. Para más información, consulta la [documentación de wis2box](https://docs.wis2box.wis.wmo.int/en/latest/reference/configuration.html).

    No edites el archivo `wis2box.env` a menos que estés seguro de los cambios que estás realizando. Cambios incorrectos pueden hacer que tu wis2box deje de funcionar.

    No compartas el contenido de tu archivo `wis2box.env` con nadie, ya que contiene información sensible como contraseñas.

## Iniciar wis2box

Asegúrate de estar en el directorio que contiene los archivos de definición del conjunto de herramientas de software de wis2box:

```{.copy}
cd ~/wis2box
```

Inicia wis2box con el siguiente comando:

```{.copy}
python3 wis2box-ctl.py start
```

Cuando ejecutes este comando por primera vez, verás la siguiente salida:

```
No docker-compose.images-*.yml files found, creating one
Current version=Undefined, latest version=1.1.0
Would you like to update ? (y/n/exit)
```

Selecciona ``y`` y el script creará el archivo ``docker-compose.images-1.1.0.yml``, descargará las imágenes de Docker necesarias e iniciará los servicios.

La descarga de las imágenes puede tardar un tiempo dependiendo de la velocidad de tu conexión a internet. Este paso solo es necesario la primera vez que inicias wis2box.

Inspecciona el estado con el siguiente comando:

```{.copy}
python3 wis2box-ctl.py status
```

Repite este comando hasta que todos los servicios estén en funcionamiento.

!!! note "wis2box y Docker"
    wis2box se ejecuta como un conjunto de contenedores Docker gestionados por docker-compose.
    
    Los servicios están definidos en los diversos archivos `docker-compose*.yml` que se encuentran en el directorio `~/wis2box/`.
    
    El script de Python `wis2box-ctl.py` se utiliza para ejecutar los comandos subyacentes de Docker Compose que controlan los servicios de wis2box.

    No necesitas conocer los detalles de los contenedores Docker para ejecutar el conjunto de herramientas de software de wis2box, pero puedes inspeccionar los archivos `docker-compose*.yml` para ver cómo están definidos los servicios. Si estás interesado en aprender más sobre Docker, puedes encontrar más información en la [documentación de Docker](https://docs.docker.com/).

Para iniciar sesión en el contenedor wis2box-management, utiliza el siguiente comando:

```{.copy}
python3 wis2box-ctl.py login
```

Ten en cuenta que después de iniciar sesión, tu indicador cambiará, indicando que ahora estás dentro del contenedor wis2box-management:

```{bash}
root@025381da3c40:/home/wis2box#
```

Dentro del contenedor wis2box-management puedes ejecutar varios comandos para gestionar tu wis2box, como:

- `wis2box auth add-token --path processes/wis2box` : para crear un token de autorización para el endpoint *processes/wis2box*
- `wis2box data clean --days=<number-of-days>` : para limpiar datos más antiguos que un cierto número de días del bucket *wis2box-public*

Para salir del contenedor y volver a tu máquina anfitriona, utiliza el siguiente comando:

```{.copy}
exit
```

Ejecuta el siguiente comando para ver los contenedores Docker que se están ejecutando en tu máquina anfitriona:

```{.copy}
docker ps --format "table {{.Names}} \t{{.Status}} \t{{.Image}}"
```

Deberías ver los siguientes contenedores en ejecución:

```{bash}
NAMES                     STATUS                   IMAGE
nginx                     Up About a minute         nginx:alpine
wis2box-auth              Up About a minute         ghcr.io/world-meteorological-organization/wis2box-auth:1.1.0
mqtt_metrics_collector    Up About a minute         ghcr.io/world-meteorological-organization/wis2box-mqtt-metrics-collector:1.1.0
wis2box-ui                Up 3 minutes              ghcr.io/world-meteorological-organization/wis2box-ui:1.1.0
wis2box-management        Up About a minute         ghcr.io/world-meteorological-organization/wis2box-management:1.1.1
wis2box-minio             Up 4 minutes (healthy)    minio/minio:RELEASE.2024-08-03T04-33-23Z-cpuv1
wis2box-api               Up 3 minutes (healthy)    ghcr.io/world-meteorological-organization/wis2box-api:1.1.0
wis2box-webapp            Up 4 minutes (healthy)    ghcr.io/world-meteorological-organization/wis2box-webapp:1.1.0
elasticsearch             Up 4 minutes (healthy)    docker.elastic.co/elasticsearch/elasticsearch:8.6.2
mosquitto                 Up 4 minutes              ghcr.io/world-meteorological-organization/wis2box-broker:1.1.0
grafana                   Up 4 minutes              grafana/grafana-oss:9.0.3
elasticsearch-exporter    Up 4 minutes              quay.io/prometheuscommunity/elasticsearch-exporter:latest
wis2downloader            Up 4 minutes (healthy)    ghcr.io/wmo-im/wis2downloader:v0.3.2
prometheus                Up 4 minutes              prom/prometheus:v2.37.0
loki                      Up 4 minutes              grafana/loki:2.4.1

```

Estos contenedores son parte del conjunto de software de wis2box y proporcionan los diversos servicios necesarios para ejecutar wis2box.

Ejecute el siguiente comando para ver los volúmenes de Docker que se están ejecutando en su máquina anfitriona:

```{.copy}
docker volume ls
```

Debería ver los siguientes volúmenes:

- wis2box_project_auth-data
- wis2box_project_es-data
- wis2box_project_htpasswd
- wis2box_project_minio-data
- wis2box_project_prometheus-data
- wis2box_project_loki-data
- wis2box_project_mosquitto-config

Así como algunos volúmenes anónimos utilizados por los diversos contenedores.

Los volúmenes que comienzan con `wis2box_project_` se utilizan para almacenar datos persistentes para los diversos servicios en el conjunto de software de wis2box.

## wis2box API

El wis2box contiene una API (Interfaz de Programación de Aplicaciones) que proporciona acceso a datos y procesos para visualización interactiva, transformación de datos y publicación.

Abra una nueva pestaña y navegue a la página `http://YOUR-HOST/oapi`.

<img alt="wis2box-api.png" src="/../assets/img/wis2box-api.png" width="800">

Esta es la página de inicio de la API de wis2box (ejecutándose a través del contenedor **wis2box-api**).

!!! question
     
     ¿Qué colecciones están disponibles actualmente?

??? success "Haga clic para revelar la respuesta"
    
    Para ver las colecciones disponibles actualmente a través de la API, haga clic en `View the collections in this service`:

    <img alt="wis2box-api-collections.png" src="/../assets/img/wis2box-api-collections.png" width="600">

    Las siguientes colecciones están disponibles actualmente:

    - Estaciones
    - Notificaciones de datos
    - Metadatos de descubrimiento


!!! question

    ¿Cuántas notificaciones de datos se han publicado?

??? success "Haga clic para revelar la respuesta"

    Haga clic en "Data notifications", luego haga clic en `Browse through the items of "Data Notifications"`. 
    
    Notará que la página dice "No items" ya que aún no se han publicado notificaciones de datos.

## wis2box webapp

Abra un navegador web y visite la página `http://YOUR-HOST/wis2box-webapp`.

Verá una ventana emergente solicitando su nombre de usuario y contraseña. Use el nombre de usuario predeterminado `wis2box-user` y la contraseña `WIS2BOX_WEBAPP_PASSWORD` definida en el archivo `wis2box.env` y haga clic en "Sign in":

!!! note 

    Verifique su archivo wis2box.env para el valor de su WIS2BOX_WEBAPP_PASSWORD. Puede usar el siguiente comando para verificar el valor de esta variable de entorno:

    ```{.copy}
    cat ~/wis2box/wis2box.env | grep WIS2BOX_WEBAPP_PASSWORD
    ```

Una vez que haya iniciado sesión, mueva el mouse al menú de la izquierda para ver las opciones disponibles en la aplicación web de wis2box:

<img alt="wis2box-webapp-menu.png" src="/../assets/img/wis2box-webapp-menu.png" width="400">

Esta es la aplicación web de wis2box que le permite interactuar con su wis2box:

- crear y gestionar conjuntos de datos
- actualizar/revisar los metadatos de su estación
- cargar observaciones manuales utilizando el formulario FM-12 synop
- monitorear las notificaciones publicadas en su wis2box-broker

Usaremos esta aplicación web en una sesión posterior.

## wis2box-broker

Abra el MQTT Explorer en su computadora y prepare una nueva conexión para conectarse a su broker (ejecutándose a través del contenedor **wis2box-broker**).

Haga clic en `+` para agregar una nueva conexión:

<img alt="mqtt-explorer-new-connection.png" src="/../assets/img/mqtt-explorer-new-connection.png" width="300">

Puede hacer clic en el botón 'ADVANCED' y verificar que tiene suscripciones a los siguientes temas:

- `#`
- `$SYS/#`

<img alt="mqtt-explorer-topics.png" src="/../assets/img/mqtt-explorer-topics.png" width="550">

!!! note

    El tema `#` es una suscripción comodín que se suscribirá a todos los temas publicados en el broker.

    Los mensajes publicados bajo el tema `$SYS` son mensajes del sistema publicados por el servicio mosquitto.

Use los siguientes detalles de conexión, asegurándose de reemplazar el valor de `<your-host>` con su nombre de host y `<WIS2BOX_BROKER_PASSWORD>` con el valor de su archivo `wis2box.env`:

- **Protocol: mqtt://**
- **Host: `<your-host>`**
- **Port: 1883**
- **Username: wis2box**
- **Password: `<WIS2BOX_BROKER_PASSWORD>`**

!!! note 

    Puede verificar su archivo wis2box.env para el valor de su WIS2BOX_BROKER_PASSWORD. Puede usar el siguiente comando para verificar el valor de esta variable de entorno:

    ```{.copy}
    cat ~/wis2box/wis2box.env | grep WIS2BOX_BROKER_PASSWORD
    ```

    Tenga en cuenta que esta es su contraseña **interna** del broker; el Global Broker utilizará credenciales diferentes (de solo lectura) para suscribirse a su broker. Nunca comparta esta contraseña con nadie.

Asegúrese de hacer clic en "SAVE" para guardar los detalles de su conexión.

Luego haga clic en "CONNECT" para conectarse a su **wis2box-broker**.

<img alt="mqtt-explorer-wis2box-broker.png" src="/../assets/img/mqtt-explorer-wis2box-broker.png" width="600">

Una vez conectado, verifique que las estadísticas internas de mosquitto se estén publicando en su broker bajo el tema `$SYS`:

<img alt="mqtt-explorer-sys-topic.png" src="/../assets/img/mqtt-explorer-sys-topic.png" width="400">

Mantenga abierto el MQTT Explorer, ya que lo utilizaremos para monitorear los mensajes publicados en el broker.

## Conclusión

!!! success "¡Felicidades!"
    En esta sesión práctica, aprendió a:

    - ejecutar el script `wis2box-create-config.py` para crear la configuración inicial
    - iniciar wis2box y verificar el estado de sus componentes
    - acceder a wis2box-webapp y wis2box-API en un navegador
    - conectarse al broker MQTT en su máquina virtual de estudiante utilizando MQTT Explorer
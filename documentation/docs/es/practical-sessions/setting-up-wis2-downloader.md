---
title: Configurar WIS2 Downloader en tu VM de estudiante
---

# Configurar WIS2 Downloader en tu VM de estudiante

!!! abstract "¡Resultados de aprendizaje!"

    Al final de esta sesión práctica, serás capaz de:

    - configurar tu propia instancia de "WIS2 Downloader" y gestionar las configuraciones específicas requeridas
    - navegar por la instancia y configurar una suscripción

## Introducción

En esta sesión aprenderás cómo configurar una instancia de WIS2 Downloader en la VM de estudiante proporcionada y cómo navegar por sus diferentes servicios.

!!! note "Sobre WIS2 Downloader"
     
     WIS2 Downloader está disponible como un proyecto independiente de Docker Compose y se recomienda ejecutarlo en un servidor separado del wis2box, para evitar que las descargas interfieran con la publicación de mensajes.

     Si deseas desarrollar tu propio servicio para suscribirte a notificaciones de WIS2 y descargar datos, puedes usar el [código fuente de WIS2 Downloader](https://github.com/World-Meteorological-Organization/wis2downloader) como referencia.

## Preparación y requisitos

!!! note "Si no es durante el entrenamiento"

    Los siguientes pasos solo deben aplicarse si los puertos mencionados no están disponibles por defecto en el servidor. En cualquier configuración, estos son los únicos puertos necesarios para acceder a todas las capacidades del stack de WIS2 Downloader.    

Antes de comenzar, inicia sesión en tu VM de estudiante asegurándote de tunelizar vía SSH los siguientes puertos:

- `5002 (API)`
- `8080 (UI)`
- `3000 (Grafana)`

Para hacerlo, puedes cambiar la configuración de tu conexión en Putty:

![access putty tunnel settings](../assets/img/putty-tunnel-settings.png)

Luego agrega el mapeo de los 3 puertos a los puertos de tu propia PC (localhost):

![adding tunnels in putty](../assets/img/putty-add-tunnel.png)

## Instalación de WIS2 Downloader

Descarga el último archivo tarball de GitHub y extráelo en tu VM de estudiante:

```bash
wget https://github.com/World-Meteorological-Organization/wis2downloader/archive/refs/tags/v1.0.0b1+rc4.tar.gz
tar -xzf v1.0.0b1+rc4.tar.gz
cd wis2downloader-*
```

Ejecuta el script de configuración para generar tu archivo de configuración:

```bash
bash setup.sh
```

Usa la siguiente ruta de descarga `/home/{USER}/wis2-downloads` y presiona Enter para usar los valores predeterminados tanto para el usuario como para los grupos.

!!! note "Gestionar permisos de usuario"
    Puedes usar diferentes valores para el usuario y el grupo modificando `WIS2DWONLOADER_UID` y `WIS2DWONLOADER_GID` en el archivo .env.
    Recuerda reconstruir las imágenes al realizar cualquier cambio en estos valores para aplicarlos. 

Esto crea un archivo `.env` con los valores predeterminados y genera valores aleatorios para `FLASK_SECRET_KEY` y `REDIS_PASSWORD`. Puedes revisar el archivo con `cat .env` — los valores predeterminados son adecuados para un despliegue en una sola máquina.

Inicia el stack completo de servicios:

```bash
docker compose up -d
```

!!! note "Verificar los contenedores en ejecución"
    Puedes verificar que todos los contenedores se hayan iniciado correctamente con:
    ```bash
    docker compose ps
    ```
    Deberías ver servicios para el gestor de suscripciones, suscriptores MQTT, UI, trabajadores Celery, Redis, Prometheus, Grafana y Loki.

## Acceder a la interfaz de WIS2 Downloader

Abre un navegador web y navega a la interfaz de tu instancia de WIS2 Downloader accediendo a `http://<WIS2DOWNLOADER_BASE_URL>:8080`.

Te encontrarás en la página de inicio, que está configurada en la vista `Dashboard` por defecto, mostrando el panel de Grafana.

![WIS2 Downloader Landing Page](../assets/img/wis2-downloader-landing-page.png)

En el menú de la barra lateral izquierda podrás navegar por todas las secciones disponibles de la interfaz.

Las principales secciones disponibles son:

- **Dashboard** — un panel de Grafana integrado que muestra la actividad de descarga, el estado de la cola y métricas del servicio en ejecución. También disponible en `http://<WIS2DOWNLOADER_BASE_URL>:3000`.
- **Catalogue View** — explora los conjuntos de datos disponibles de WIS2 buscando o filtrando el catálogo global. Selecciona un tema y un directorio de guardado, luego haz clic en *Subscribe* para comenzar a descargar.
- **Tree View** — navega por la jerarquía de temas de WIS2 como un árbol colapsable. Útil para explorar qué temas están disponibles antes de suscribirse.
- **Manual Subscribe** — crea una suscripción ingresando directamente los detalles del tema, sin depender de los catálogos de descubrimiento global. Útil para suscribirse a temas de manera más libre utilizando tantos comodines como sea necesario y permite el acceso a temas que no se encuentran en los GDCs, como las puertas de enlace GTS y temas publicados en brokers privados cuando se usan configuraciones no predeterminadas.
- **Manage Subscriptions** — visualiza y gestiona todas las suscripciones activas. Desde aquí puedes ver qué temas están siendo monitoreados y eliminar los que ya no necesites.
- **Settings** — actualmente permite recargar el catálogo de conjuntos de datos desde los catálogos de descubrimiento global. Esta sección se ampliará en futuras versiones para cubrir la configuración general y la gestión de WIS2 Downloader.
- **Help** — la página de inicio predeterminada, que muestra la documentación integrada de WIS2 Downloader.

## Gestionar suscripciones en la interfaz

Como en el último ejemplo, accederás a la interfaz de la instancia en ejecución yendo a `http://<WIS2DOWNLOADER_BASE_URL>:8080`.

Desde allí hay 3 formas de configurar una suscripción:

- En **Catalogue View** navegando por los temas disponibles de manera similar a los portales GDC.
- En **Tree View** seleccionando un tema del catálogo GDC explorando temas como en MQTT Explorer.
- En **Manual Subscribe** donde puedes escribir tus propios temas deseados, filtros y otros parámetros.

Para el siguiente ejercicio nos suscribiremos a todas las notificaciones synop provenientes de todos los nodos WIS2:

- Primero, ve a **Manual Subscribe**.
- Escribe el tema como `cache/a/wis2/+/data/core/weather/surface-based-observations/synop`
- Configura la carpeta de destino como `synop-data`

El resultado final debería ser similar a:
![WIS2 Downloader Manual Subscribe](../assets/img/wis2-downloader-manual-subscribe.png)

Ahora presiona el botón **Subscribe** y confirma tu suscripción.

Después de esto, verifica la carpeta de descargas en tu VM de estudiante usando el comando:

```bash
ls -R /home/{USER}/wis2-downloads
```

Ahora deberías ver una serie de archivos que han sido descargados por tu instancia.

Como paso final, podemos eliminar la suscripción yendo a la vista **Manage Subscriptions** y presionando el botón **Unsubscribe**.

![WIS2 Downloader Delete Subscription](../assets/img/wis2-downloader-delete-subscription.png)

!!! note "Eliminar archivos descargados"

    Se recomienda limpiar la carpeta de descargas después de completar un ejercicio para liberar espacio en la VM de estudiante. Por lo tanto, ejecuta el siguiente comando para eliminar los archivos del ejercicio anterior.

    ```bash
    rm -fr /home/{USER}/wis2-downloads/synop-data
    ```

## Revisar la configuración de WIS2 Downloader

La instancia de WIS2 Downloader puede configurarse utilizando las variables de entorno definidas en tu archivo `.env`.

Puedes consultar un desglose de las variables de entorno en la [Sección 2.1 de la Guía de Administración de WIS2 Downloader](https://world-meteorological-organization.github.io/wis2downloader/en/admin-guide.html).

Para revisar la configuración actual de WIS2 Downloader, puedes usar el siguiente comando:

```bash
cat .env
```

!!! question "Revisar la configuración de WIS2 Downloader"

    ¿Cuál es el período de retención predeterminado para los datos descargados?

    ¿En qué puerto escucha la API del gestor de suscripciones?

??? success "Haz clic para revelar la respuesta"

    El período de retención predeterminado para los datos descargados es de `30` días, según lo establecido por `DOWNLOAD_RETENTION_PERIOD`.

    La API del gestor de suscripciones escucha en el puerto `5002`, según lo definido en `WIS2DOWNLOADER_SUBSCRIPTION_MANAGER_URL`.

!!! note "Actualizar la configuración de WIS2 Downloader"

    Para actualizar la configuración, edita el archivo `.env` y reinicia el stack para aplicar los cambios:

    ```bash
    docker compose up -d
    ```

Puedes mantener la configuración predeterminada para los próximos ejercicios.

## API de WIS2 Downloader

WIS2 Downloader expone una API REST en `<WIS2DOWNLOADER_BASE_URL>:5002/api`. Confirma que el servicio está listo:

```bash
curl <WIS2DOWNLOADER_BASE_URL>:5002/api/health
```

Deberías ver:

```json
{"status": "healthy"}
```

Para crear una suscripción, envía una solicitud `POST` con el `topic` de MQTT y un subdirectorio opcional `target` donde se guardarán los archivos:

```bash
curl -s -X POST <WIS2DOWNLOADER_BASE_URL>:5002/subscriptions \
  -H "Content-Type: application/json" \
  -d '{"topic": "cache/a/wis2/+/data/core/weather/surface-based-observations/#", "target": "surface-obs"}'
```

Como antes, los archivos descargados pueden revisarse verificando la carpeta `surface-obs` en el directorio de descargas:

```bash
ls -R /home/{USER}/wis2-downloads/surface-obs
```

La respuesta incluye el UUID asignado a la nueva suscripción. Úsalo para eliminar la suscripción cuando ya no sea necesaria:

```bash
curl -X DELETE <WIS2DOWNLOADER_BASE_URL>:5002/subscriptions/{id}
```

!!! note "Eliminar archivos descargados"

    Se recomienda limpiar la carpeta de descargas después de completar un ejercicio para liberar espacio en la VM de estudiante. Por lo tanto, ejecuta el siguiente comando para eliminar los archivos del ejercicio anterior.

    ```bash
    rm -fr /home/{USER}/wis2-downloads/surface-obs
    ```

Para la lista completa de endpoints disponibles (listar, obtener, actualizar suscripciones y más), consulta la documentación interactiva Swagger disponible en `<WIS2DOWNLOADER_BASE_URL>:5002/swagger`.

## Conclusión

!!! success "¡Felicidades!"

    En esta sesión práctica, aprendiste a:

    - instalar WIS2 Downloader en tu sistema local y cambiar las configuraciones predeterminadas
    - interactuar con la interfaz para crear y eliminar suscripciones
    - gestionar suscripciones usando la API
    - visualizar los datos descargados en tu sistema local
---
title: Configurar WIS2 Downloader en tu VM de estudiante
---

# Configurar WIS2 Downloader en tu VM de estudiante

!!! abstract "Resultados de aprendizaje"

    Al final de esta sesión práctica, serás capaz de:

    - configurar tu propia instancia de "WIS2 Downloader" y gestionar las configuraciones específicas requeridas
    - navegar por la instancia para aprovechar sus diferentes capacidades

## Introducción

En esta sesión aprenderás a configurar una instancia de WIS2 Downloader en la VM de estudiante proporcionada y a navegar por sus diferentes servicios.

!!! note "Sobre WIS2 Downloader"
     
     WIS2 Downloader está disponible como un proyecto independiente de Docker Compose y se recomienda ejecutarlo en un servidor separado del wis2box, para evitar que las descargas interfieran con la publicación de mensajes.

     Si deseas desarrollar tu propio servicio para suscribirte a notificaciones de WIS2 y descargar datos, puedes usar el [código fuente de WIS2 Downloader](https://github.com/World-Meteorological-Organization/wis2downloader) como referencia.

## Preparación y requisitos

!!! note "Si no es durante el entrenamiento"

    Los siguientes pasos solo deben aplicarse si los puertos mencionados no están disponibles por defecto en el servidor. En cualquier configuración, estos son los únicos puertos que deben ser accesibles para utilizar todas las capacidades del stack de WIS2 Downloader.    

Antes de comenzar, inicia sesión en tu VM de estudiante asegurándote de tunelar vía SSH los siguientes puertos:

- `5002 (API)`
- `8080 (UI)`
- `3000 (Grafana)`

Para hacerlo, puedes cambiar la configuración de tu conexión en Putty:

![access putty tunnel settings](../assets/img/putty-tunnel-settings.png)

Luego agrega el mapeo de los 3 puertos a los puertos de tu propio PC (localhost):

![adding tunnels in putty](../assets/img/putty-add-tunnel.png)

## Instalación de WIS2 Downloader

Descarga el último archivo tarball de GitHub y extráelo en tu VM de estudiante:

```bash
wget https://github.com/World-Meteorological-Organization/wis2downloader/releases/latest/download/wis2downloader-latest.tar.gz
tar -xzf wis2downloader-latest.tar.gz
cd wis2downloader-*
```

Ejecuta el script de configuración para generar tu archivo de configuración:

```bash
bash setup.sh
```

Esto crea un archivo `.env` a partir de los valores predeterminados y genera valores aleatorios para `FLASK_SECRET_KEY` y `REDIS_PASSWORD`. Puedes revisar el archivo con `cat .env` — los valores predeterminados son adecuados para un despliegue en una sola máquina.

Instala el plugin Docker de Loki utilizado para el envío de logs:

```bash
ARCH=$(uname -m | sed 's/x86_64/amd64/;s/aarch64/arm64/')
docker plugin install grafana/loki-docker-driver:3.6.7-${ARCH} --alias loki --grant-all-permissions
```

Verifica que el plugin esté habilitado:

```bash
docker plugin ls
```

Deberías ver `loki:latest` listado con `ENABLED` configurado como `true`.

Crea un grupo dedicado `wis2`, agrega tu usuario a él y configura el archivo `.env` y el directorio de descargas en consecuencia:

```bash
sudo groupadd wis2
sudo usermod -aG wis2 $USER
sed -i "s/^UID=.*/UID=$(id -u)/" .env
sed -i "s/^GID=.*/GID=$(getent group wis2 | cut -d: -f3)/" .env
mkdir -p downloads
sudo chown $(id -un):wis2 downloads
chmod 775 downloads
```

!!! note "Reinicio de sesión requerido"
    El cambio de membresía del grupo solo entra en efecto después de cerrar sesión y volver a iniciar sesión en tu sesión SSH.

Inicia el stack completo de servicios:

```bash
docker compose up -d
```

Espera aproximadamente 30 segundos para que las verificaciones de salud pasen, luego confirma que el gestor de suscripciones está listo:

```bash
curl http://localhost:5002/health
```

!!! note "Verificando los contenedores en ejecución"
    Puedes verificar que todos los contenedores se iniciaron correctamente con:
    ```bash
    docker compose ps
    ```
    Deberías ver servicios para el gestor de suscripciones, suscriptores MQTT, UI, trabajadores Celery, Redis, Prometheus, Grafana y Loki.

### Acceso a la interfaz de usuario de WIS2 Downloader

Abre un navegador web y navega a la interfaz de usuario de tu instancia de WIS2 Downloader accediendo a `http://localhost:8080`.

Te encontrarás en la página de inicio, que está configurada en la sección `Help` por defecto mostrando la documentación.

![WIS2 Downloader Landing Page](../assets/img/wis2-downloader-landing-page.png)

En el menú de la barra lateral izquierda podrás navegar por todas las diferentes secciones de la interfaz de usuario.

Las principales secciones disponibles son:

- **Dashboard** — un panel de Grafana integrado que muestra la actividad de descargas, el estado de la cola y métricas del servicio en ejecución. También disponible en `http://localhost:3000`.
- **Catalogue View** — explora los conjuntos de datos disponibles de WIS2 buscando o filtrando el catálogo global. Selecciona un tema y un directorio de guardado, luego haz clic en *Subscribe* para comenzar a descargar.
- **Tree View** — navega por la jerarquía de temas de WIS2 como un árbol colapsable. Útil para explorar qué temas están disponibles antes de suscribirse.
- **Manual Subscription** — crea una suscripción ingresando directamente un tema y detalles del broker, sin depender de los Global Discovery Catalogues. Útil para suscribirse a temas de WIS2 Nodes específicos o brokers privados.
- **Subscriptions** — visualiza y gestiona todas las suscripciones activas. Desde aquí puedes ver qué temas están siendo monitoreados y eliminar los que ya no necesites.
- **Settings** — actualmente permite recargar el catálogo de conjuntos de datos desde los Global Discovery Catalogues. Esta sección se ampliará en futuras versiones para cubrir la configuración general y la gestión de WIS2 Downloader.
- **Help** — la página de inicio predeterminada, que muestra la documentación integrada de WIS2 Downloader.

### Revisando la configuración de WIS2 Downloader

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

!!! note "Actualizando la configuración de WIS2 Downloader"

    Para actualizar la configuración, edita el archivo `.env` y reinicia el stack para aplicar los cambios:

    ```bash
    docker compose up -d
    ```

Puedes mantener la configuración predeterminada para los próximos ejercicios.

### API de WIS2 Downloader

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
curl -s -X POST <WIS2DOWNLOADER_BASE_URL>:5002/api/subscriptions \
  -H "Content-Type: application/json" \
  -d '{"topic": "cache/a/wis2/+/data/core/weather/surface-based-observations/#", "target": "surface-obs"}'
```

La respuesta incluye el UUID asignado a la nueva suscripción. Úsalo para eliminar la suscripción cuando ya no sea necesaria:

```bash
curl -X DELETE <WIS2DOWNLOADER_BASE_URL>:5002/api/subscriptions/{id}
```

Para la lista completa de endpoints disponibles (listar, obtener, actualizar suscripciones y más), consulta la documentación interactiva de Swagger disponible en `<WIS2DOWNLOADER_BASE_URL>:5002/api/openapi`.

## Conclusión

!!! success "¡Felicidades!"

    En esta sesión práctica, aprendiste a:

    - instalar WIS2 Downloader en tu sistema local y cambiar las configuraciones predeterminadas
    - interactuar con la interfaz de usuario para crear y eliminar suscripciones
    - gestionar suscripciones utilizando la API
    - visualizar los datos descargados en tu sistema local
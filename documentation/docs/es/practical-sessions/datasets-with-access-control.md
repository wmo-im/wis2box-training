---
title: Configuración de un conjunto de datos recomendado con control de acceso
---

# Configuración de un conjunto de datos recomendado con control de acceso

!!! abstract "Resultados de aprendizaje"
    Al final de esta sesión práctica, serás capaz de:

    - crear un nuevo conjunto de datos con la política de datos 'recommended'
    - añadir un token de acceso al conjunto de datos
    - validar que el conjunto de datos no puede ser accedido sin el token de acceso
    - añadir el token de acceso a los encabezados HTTP para acceder al conjunto de datos
    - añadir un archivo de licencia personalizado alojado en tu instancia de wis2box

## Introducción

Los datos se comparten en WIS2 de acuerdo con la Política Unificada de Datos de la OMM, que describe dos categorías de datos:

- **core**: datos que se proporcionan de forma gratuita y sin restricciones, sin costo y sin condiciones de uso.
- **recommended**: datos que pueden proporcionarse con condiciones de uso y/o sujetos a una licencia.

Los datos que se comparten como 'recommended':

- Pueden estar sujetos a condiciones de uso y reutilización;
- Pueden tener controles de acceso aplicados a los datos;
- No se almacenan en caché dentro de WIS2 por los Global Caches;
- Deben incluir un enlace a una licencia que especifique las condiciones de uso de los datos en los metadatos de descubrimiento.

El editor de conjuntos de datos en la wis2box-webapp requerirá que proporciones una URL de licencia cuando selecciones la política de datos 'recommended'. Opcionalmente, puedes añadir un token de acceso a dicho conjunto de datos para restringir el acceso a los datos.

En esta sesión práctica, crearás un nuevo conjunto de datos con la política de datos 'recommended' y aprenderás cómo añadir control de acceso. También te guiará a través de los pasos para añadir un archivo de licencia personalizado a tu instancia de wis2box.

## Preparación

Asegúrate de tener acceso SSH a tu máquina virtual de estudiante y que tu instancia de wis2box esté en funcionamiento.

Asegúrate de estar conectado al broker MQTT de tu instancia de wis2box usando MQTT Explorer. Puedes usar las credenciales públicas `everyone/everyone` para conectarte al broker.

Asegúrate de tener un navegador web abierto con la wis2box-webapp de tu instancia accediendo a `http://YOUR-HOST/wis2box-webapp`.

## Crear un nuevo conjunto de datos con la política de datos 'recommended'

Ve a la página 'dataset editor' en la wis2box-webapp y crea un nuevo conjunto de datos. Selecciona el Data Type = 'weather/surface-weather-observations/synop'.

<img alt="create-dataset-recommended" src="/../assets/img/create-dataset-template.png" width="800">

Para "Centre ID", usa el mismo que utilizaste en las sesiones prácticas anteriores.

Haz clic en 'CONTINUE TO FORM' para continuar.

Reemplaza el 'Local ID' generado automáticamente con un nombre descriptivo para el conjunto de datos, por ejemplo, 'recommended-data-with-access-control', y actualiza los campos 'Title' y 'Description':

<img alt="create-dataset-recommended" src="/../assets/img/create-dataset-recommended.png" width="800">

Cambia la política de datos de la OMM a 'recommended' y verás que el formulario añadió un nuevo campo de entrada para una URL que proporcione la información de la licencia para el conjunto de datos:

<img alt="create-dataset-license" src="/../assets/img/create-dataset-license.png" width="800">

Tienes la opción de proporcionar una URL a una licencia que describa los términos de uso del conjunto de datos. Por ejemplo, podrías usar 
`https://creativecommons.org/licenses/by/4.0/`
para apuntar a la licencia Creative Commons Attribution 4.0 International (CC BY 4.0).

O puedes usar `WIS2BOX_URL/data/license.txt` para apuntar a un archivo de licencia personalizado alojado en tu propio servidor web, donde `WIS2BOX_URL` es la URL que definiste en el archivo wis2box.env:

<img alt="create-dataset-license-url" src="/../assets/img/create-dataset-license-custom.png" width="800">

Continúa completando los campos requeridos para las Propiedades Espaciales y la Información de Contacto, y 'Validate form' para verificar si hay errores.

Finalmente, envía el conjunto de datos, usando el token de autenticación creado previamente, y verifica que el nuevo conjunto de datos se haya creado en la wis2box-webapp.

Revisa MQTT Explorer para ver que recibes el WIS2 Notification Message anunciando el nuevo registro de Metadatos de Descubrimiento en el tema `origin/a/wis2/<your-centre-id>/metadata`.

## Revisa tu nuevo conjunto de datos en la wis2box-api

Visualiza la lista de conjuntos de datos en la wis2box-api abriendo la URL `WIS2BOX_URL/oapi/collections/discovery-metadata/items` en tu navegador web, reemplazando `WIS2BOX_URL` con la URL de tu instancia de wis2box.

Abre el enlace del conjunto de datos que acabas de crear y desplázate hacia abajo hasta la sección 'links' de la respuesta JSON:

<img alt="wis2box-api-recommended-dataset-links" src="/../assets/img/wis2box-api-recommended-dataset-links.png" width="600">

Deberías ver un enlace para "License for this dataset" apuntando a la URL que proporcionaste en el editor de conjuntos de datos.

Si usaste `http://YOUR-HOST/data/license.txt` como la URL de la licencia, el enlace actualmente no funcionará, porque aún no hemos añadido un archivo de licencia a la instancia de wis2box.

Si el tiempo lo permite, puedes añadir un archivo de licencia personalizado a tu instancia de wis2box al final de esta sesión práctica. Primero, continuaremos añadiendo un token de acceso al conjunto de datos.

## Añadir un token de acceso al conjunto de datos

Inicia sesión en el contenedor wis2box-management,

```bash
cd ~/wis2box
python3 wis2box-ctl.py login
```

Desde la línea de comandos dentro del contenedor, puedes asegurar un conjunto de datos usando el comando `wis2box auth add-token`, utilizando la bandera `--metadata-id` para especificar el identificador de metadatos del conjunto de datos y el token de acceso como argumento.

Por ejemplo, para añadir el token de acceso `S3cr3tT0k3n` al conjunto de datos con identificador de metadatos `urn:wmo:md:not-my-centre:core.surface-based-observations.synop`:

```bash
wis2box auth add-token --metadata-id urn:wmo:md:not-my-centre:reco.surface-based-observations.synop S3cr3tT0k3n
```

Sal del contenedor wis2box-management:

```bash
exit
```

## Publicar algunos datos en el conjunto de datos

Copia el archivo `exercise-materials/access-control-exercises/aws-example.csv` al directorio definido por `WIS2BOX_HOST_DATADIR` en tu archivo `wis2box.env`:

```bash
cp ~/exercise-materials/access-control-exercises/aws-example.csv ~/wis2box-data
```

Luego usa WinSCP o un editor de línea de comandos para editar el archivo `aws-example.csv` y actualiza los identificadores de estaciones WIGOS en los datos de entrada para que coincidan con las estaciones que tienes en tu instancia de wis2box.

A continuación, ve al editor de estaciones en la wis2box-webapp. Para cada estación que usaste en `aws-example.csv`, actualiza el campo 'topic' para que coincida con el 'topic' del conjunto de datos que creaste en el ejercicio anterior.

Esta estación ahora estará asociada a 2 temas, uno para el conjunto de datos 'core' y otro para el conjunto de datos 'recommended':

<img alt="edit-stations-add-topics" src="/../assets/img/edit-stations-add-topics.png" width="600">

Necesitarás usar tu token para `collections/stations` para guardar los datos de la estación actualizados.

Luego, inicia sesión en el contenedor wis2box-management:

```bash
cd ~/wis2box
python3 wis2box-ctl.py login
```

Desde la línea de comandos de wis2box, podemos ingerir el archivo de datos de ejemplo `aws-example.csv` en un conjunto de datos específico de la siguiente manera:

```bash
wis2box data ingest -p /data/wis2box/aws-example.csv --metadata-id urn:wmo:md:not-my-centre:reco.surface-based-observations.synop
```

Asegúrate de proporcionar el identificador de metadatos correcto para tu conjunto de datos y **verifica que recibes notificaciones de datos WIS2 en MQTT Explorer**, en el tema `origin/a/wis2/<your-centre-id>/data/recommended/surface-based-observations/synop`.

Revisa el enlace canónico en el WIS2 Notification Message y copia/pega el enlace en el navegador para intentar descargar los datos.

Deberías ver un *401 Authorization Required*.

## Añadir el token de acceso a los encabezados HTTP para acceder al conjunto de datos

Para demostrar que se requiere el token de acceso para acceder al conjunto de datos, reproduciremos el error que viste en el navegador usando la función de línea de comandos `wget`.

Desde la línea de comandos en tu máquina virtual de estudiante, usa el comando `wget` con el enlace canónico que copiaste del WIS2 Notification Message.

```bash
wget <canonical-link>
```

Deberías ver que la solicitud HTTP devuelve *401 Unauthorized* y los datos no se descargan.

Ahora añade el token de acceso a los encabezados HTTP para acceder al conjunto de datos.

```bash
wget --header="Authorization: Bearer S3cr3tT0k3n" <canonical-link>
```

Ahora los datos deberían descargarse correctamente.

## Añadir un archivo de licencia personalizado a tu instancia de wis2box

Este paso solo es necesario si deseas proporcionar una licencia personalizada alojada en tu instancia de wis2box, en lugar de usar una URL de licencia externa.

Crea un archivo de texto en tu máquina local usando tu editor de texto favorito y añade información de licencia al archivo, como:

*Este es un archivo de licencia personalizado para el conjunto de datos recomendado con control de acceso. 
Eres libre de usar estos datos, pero por favor reconoce al proveedor de los datos.*

Para subir un archivo localmente creado llamado license.txt, usa la consola de MinIO disponible en el puerto 9001 de la instancia de wis2box, accediendo a un navegador web y visitando `http://YOUR-HOST:9001`.

Las credenciales para acceder a la consola de MinIO en el archivo wis2box.env están definidas por las variables de entorno `WIS2BOX_STORAGE_USERNAME` y `WIS2BOX_STORAGE_PASSWORD`. Puedes encontrarlas en el archivo wis2box.env de la siguiente manera:

```bash
cat wis2box.env | grep WIS2BOX_STORAGE_USERNAME
cat wis2box.env | grep WIS2BOX_STORAGE_PASSWORD
```

Una vez que hayas iniciado sesión en la consola de MinIO, puedes subir el archivo de licencia en la ruta base del bucket **wis2box-public** usando el botón “Upload”:

<img alt="minio-upload-license" src="/../assets/img/minio-upload-license.png" width="800">

Después de subir el archivo de licencia, verifica si el archivo es accesible visitando `WIS2BOX_URL/data/license.txt` en tu navegador web, reemplazando `WIS2BOX_URL` con la URL de tu instancia de wis2box.

!!! note

    El proxy web en wis2box redirige todos los archivos almacenados en el bucket "wis2box-public" bajo la ruta `WIS2BOX_URL/data/`

El enlace para "License for this dataset" incluido en los metadatos de tu conjunto de datos recomendado ahora debería funcionar.

## Conclusión

!!! success "¡Felicidades!"
    En esta sesión práctica, aprendiste a:

    - crear un nuevo conjunto de datos con la política de datos 'recommended'
    - añadir un token de acceso al conjunto de datos
    - validar que el conjunto de datos no puede ser accedido sin el token de acceso
    - añadir el token de acceso a los encabezados HTTP para acceder al conjunto de datos
    - añadir un archivo de licencia personalizado a tu instancia de wis2box
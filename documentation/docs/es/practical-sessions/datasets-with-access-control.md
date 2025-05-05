---
title: Configuración de un conjunto de datos recomendado con control de acceso
---

# Configuración de un conjunto de datos recomendado con control de acceso

!!! abstract "Objetivos de aprendizaje"
    Al finalizar esta sesión práctica, podrás:

    - crear un nuevo conjunto de datos con política de datos 'recommended'
    - agregar un token de acceso al conjunto de datos
    - verificar que no se puede acceder al conjunto de datos sin el token de acceso
    - agregar el token de acceso a los encabezados HTTP para acceder al conjunto de datos

## Introducción

Los conjuntos de datos que no se consideran conjuntos de datos 'core' en WMO pueden configurarse opcionalmente con una política de control de acceso. wis2box proporciona un mecanismo para agregar un token de acceso a un conjunto de datos que impedirá que los usuarios descarguen datos a menos que proporcionen el token de acceso en los encabezados HTTP.

## Preparación

Asegúrate de tener acceso SSH a tu máquina virtual de estudiante y que tu instancia de wis2box esté funcionando.

Asegúrate de estar conectado al broker MQTT de tu instancia wis2box usando MQTT Explorer. Puedes usar las credenciales públicas `everyone/everyone` para conectarte al broker.

Asegúrate de tener un navegador web abierto con wis2box-webapp para tu instancia accediendo a `http://YOUR-HOST/wis2box-webapp`.

## Crear un nuevo conjunto de datos con política de datos 'recommended'

Ve a la página 'dataset editor' en wis2box-webapp y crea un nuevo conjunto de datos. Selecciona Data Type = 'weather/surface-weather-observations/synop'.

<img alt="create-dataset-recommended" src="../../assets/img/create-dataset-template.png" width="800">

Para "Centre ID", usa el mismo que utilizaste en las sesiones prácticas anteriores.

Haz clic en 'CONTINUE To FORM' para continuar.

En el editor de conjuntos de datos, establece la política de datos como 'recommended' (ten en cuenta que cambiar la política de datos actualizará la 'Topic Hierarchy').
Reemplaza el 'Local ID' generado automáticamente con un nombre descriptivo para el conjunto de datos, por ejemplo, 'recommended-data-with-access-control':

<img alt="create-dataset-recommended" src="../../assets/img/create-dataset-recommended.png" width="800">

Continúa completando los campos requeridos para Propiedades Espaciales e Información de Contacto, y 'Validate form' para verificar si hay errores.

Finalmente, envía el conjunto de datos utilizando el token de autenticación creado anteriormente y verifica que el nuevo conjunto de datos se haya creado en wis2box-webapp.

Verifica en MQTT-explorer que recibes el Mensaje de Notificación WIS2 anunciando el nuevo registro de Metadatos de Descubrimiento en el tema `origin/a/wis2/<your-centre-id>/metadata`.

## Agregar un token de acceso al conjunto de datos

Inicia sesión en el contenedor wis2box-management,

```bash
cd ~/wis2box
python3 wis2box-ctl.py login
```

Desde la línea de comandos dentro del contenedor, puedes asegurar un conjunto de datos usando el comando `wis2box auth add-token`, utilizando la bandera `--metadata-id` para especificar el identificador de metadatos del conjunto de datos y el token de acceso como argumento.

Por ejemplo, para agregar el token de acceso `S3cr3tT0k3n` al conjunto de datos con identificador de metadatos `urn:wmo:md:not-my-centre:core.surface-based-observations.synop`:

```bash
wis2box auth add-token --metadata-id urn:wmo:md:not-my-centre:reco.surface-based-observations.synop S3cr3tT0k3n
```

Sal del contenedor wis2box-management:

```bash
exit
```

## Publicar datos en el conjunto de datos

Copia el archivo `exercise-materials/access-control-exercises/aws-example.csv` al directorio definido por `WIS2BOX_HOST_DATADIR` en tu `wis2box.env`:

```bash
cp ~/exercise-materials/access-control-exercises/aws-example.csv ~/wis2box-data
```

Luego usa WinSCP o un editor de línea de comandos para editar el archivo `aws-example.csv` y actualizar los identificadores WIGOS-station en los datos de entrada para que coincidan con las estaciones que tienes en tu instancia wis2box.

A continuación, ve al editor de estaciones en wis2box-webapp. Para cada estación que usaste en `aws-example.csv`, actualiza el campo 'topic' para que coincida con el 'topic' del conjunto de datos que creaste en el ejercicio anterior.

Esta estación ahora estará asociada a 2 temas, uno para el conjunto de datos 'core' y otro para el conjunto de datos 'recommended':

<img alt="edit-stations-add-topics" src="../../assets/img/edit-stations-add-topics.png" width="600">

Necesitarás usar tu token para `collections/stations` para guardar los datos actualizados de la estación.

Luego, inicia sesión en el contenedor wis2box-management:

```bash
cd ~/wis2box
python3 wis2box-ctl.py login
```

Desde la línea de comandos de wis2box podemos ingerir el archivo de datos de ejemplo `aws-example.csv` en un conjunto de datos específico de la siguiente manera:

```bash
wis2box data ingest -p /data/wis2box/aws-example.csv --metadata-id urn:wmo:md:not-my-centre:reco.surface-based-observations.synop
```

Asegúrate de proporcionar el identificador de metadatos correcto para tu conjunto de datos y **verifica que recibes notificaciones de datos WIS2 en MQTT Explorer**, en el tema `origin/a/wis2/<your-centre-id>/data/recommended/surface-based-observations/synop`.

Verifica el enlace canónico en el Mensaje de Notificación WIS2 y copia/pega el enlace en el navegador para intentar descargar los datos.

Deberías ver un error 403 Forbidden.

## Agregar el token de acceso a los encabezados HTTP para acceder al conjunto de datos

Para demostrar que se requiere el token de acceso para acceder al conjunto de datos, reproduciremos el error que viste en el navegador usando la función de línea de comandos `wget`.

Desde la línea de comandos en tu máquina virtual de estudiante, usa el comando `wget` con el enlace canónico que copiaste del Mensaje de Notificación WIS2.

```bash
wget <canonical-link>
```

Deberías ver que la solicitud HTTP devuelve *401 Unauthorized* y los datos no se descargan.

Ahora agrega el token de acceso a los encabezados HTTP para acceder al conjunto de datos.

```bash
wget --header="Authorization: Bearer S3cr3tT0k3n" <canonical-link>
```

Ahora los datos deberían descargarse correctamente.

## Conclusión

!!! success "¡Felicitaciones!"
    En esta sesión práctica, aprendiste a:

    - crear un nuevo conjunto de datos con política de datos 'recommended'
    - agregar un token de acceso al conjunto de datos
    - verificar que no se puede acceder al conjunto de datos sin el token de acceso
    - agregar el token de acceso a los encabezados HTTP para acceder al conjunto de datos
---
title: Consulta de datos utilizando la API de wis2box
---

# Consulta de datos utilizando la API de wis2box

!!! abstract "Resultados de aprendizaje"
    Al final de esta sesión práctica, podrás:

    - usar la API de wis2box para consultar y filtrar tus estaciones
    - usar la API de wis2box para consultar y filtrar tus datos

## Introducción

La API de wis2box proporciona acceso de descubrimiento y consulta de manera legible por máquina a los datos que han sido ingeridos en wis2box. La API se basa en el estándar OGC API - Features y se implementa utilizando [pygeoapi](https://pygeoapi.io).

La API de wis2box proporciona acceso a las siguientes colecciones:

- Estaciones
- Metadatos de descubrimiento
- Notificaciones de datos
- más una colección por conjunto de datos configurado, que almacena la salida de bufr2geojson (el complemento `bufr2geojson` debe estar habilitado en la configuración de mapeo de datos para llenar los elementos en la colección de conjuntos de datos).

En esta sesión práctica aprenderás a usar la API de datos para explorar y consultar datos que han sido ingeridos en wis2box.

## Preparación

!!! note
    Navega a la página de inicio de la API de wis2box en tu navegador web:

    `http://YOUR-HOST/oapi`

<img alt="wis2box-api-landing-page" src="/../assets/img/wis2box-api-landing-page.png" width="600">

## Inspeccionando colecciones

Desde la página de inicio, haz clic en el enlace 'Colecciones'.

!!! question
    ¿Cuántas colecciones de conjuntos de datos ves en la página resultante? ¿Qué crees que representa cada colección?

??? success "Haz clic para revelar la respuesta"
    Deberían mostrarse 4 colecciones, incluyendo "Estaciones", "Metadatos de descubrimiento" y "Notificaciones de datos"

## Inspeccionando estaciones

Desde la página de inicio, haz clic en el enlace 'Colecciones', luego haz clic en el enlace 'Estaciones'.

<img alt="wis2box-api-collections-stations" src="/../assets/img/wis2box-api-collections-stations.png" width="600">

Haz clic en el enlace 'Explorar', luego haz clic en el enlace 'json'.

!!! question
    ¿Cuántas estaciones se devuelven? Compara este número con la lista de estaciones en `http://YOUR-HOST/wis2box-webapp/station`

??? success "Haz clic para revelar la respuesta"
    El número de estaciones de la API debería ser igual al número de estaciones que ves en la wis2box-webapp.

!!! question
    ¿Cómo podemos consultar por una sola estación (por ejemplo, `Balaka`)?

??? success "Haz clic para revelar la respuesta"
    Consulta la API con `http://YOUR-HOST/oapi/collections/stations/items?q=Balaka`.

!!! note
    El ejemplo anterior se basa en los datos de prueba de Malawi. Intenta probar con las estaciones que has ingerido como parte de los ejercicios anteriores.

## Inspeccionando observaciones

!!! note
    El ejemplo anterior se basa en los datos de prueba de Malawi. Intenta probar con la observación que has ingerido como parte de los ejercicios.

Desde la página de inicio, haz clic en el enlace 'Colecciones', luego haz clic en el enlace 'Observaciones meteorológicas superficiales de Malawi'.

<img alt="wis2box-api-collections-malawi-obs" src="/../assets/img/wis2box-api-collections-malawi-obs.png" width="600">

Haz clic en el enlace 'Consultables'.

<img alt="wis2box-api-collections-malawi-obs-queryables" src="/../assets/img/wis2box-api-collections-malawi-obs-queryables.png" width="600">

!!! question
    ¿Qué consultable se usaría para filtrar por identificador de estación?

??? success "Haz clic para revelar la respuesta"
    El `wigos_station_identifer` es el consultable correcto.

Navega a la página anterior (es decir, `http://YOUR-HOST/oapi/collections/urn:wmo:md:mwi:mwi_met_centre:surface-weather-observations`)

Haz clic en el enlace 'Explorar'.

!!! question
    ¿Cómo podemos visualizar la respuesta JSON?

??? success "Haz clic para revelar la respuesta"
    Haciendo clic en el enlace 'JSON' en la parte superior derecha de la página, o agregando `f=json` a la solicitud de API en el navegador web.

Inspecciona la respuesta JSON de las observaciones.

!!! question
    ¿Cuántos registros se devuelven?

!!! question
    ¿Cómo podemos limitar la respuesta a 3 observaciones?

??? success "Haz clic para revelar la respuesta"
    Agrega `limit=3` a la solicitud de API.

!!! question
    ¿Cómo podemos ordenar la respuesta por las observaciones más recientes?

??? success "Haz clic para revelar la respuesta"
    Agrega `sortby=-resultTime` a la solicitud de API (nota el signo `-` para denotar orden descendente). Para ordenar por las observaciones más antiguas, actualiza la solicitud para incluir `sortby=resultTime`.

!!! question
    ¿Cómo podemos filtrar las observaciones por una sola estación?

??? success "Haz clic para revelar la respuesta"
    Agrega `wigos_station_identifier=<WSI>` a la solicitud de API.

!!! question
    ¿Cómo podemos recibir las observaciones como un CSV?

??? success "Haz clic para revelar la respuesta"
    Agrega `f=csv` a la solicitud de API.

!!! question
    ¿Cómo podemos mostrar una sola observación (id)?

??? success "Haz clic para revelar la respuesta"
    Usando el identificador de característica de una solicitud de API contra las observaciones, consulta la API para `http://YOUR-HOST/oapi/collections/{collectionId}/items/{featureId}`, donde `{collectionId}` es el nombre de tu colección de observaciones y `{itemId}` es el identificador de la única observación de interés.

## Conclusión

!!! success "¡Felicidades!"
    En esta sesión práctica, aprendiste cómo:

    - usar la API de wis2box para consultar y filtrar tus estaciones
    - usar la API de wis2box para consultar y filtrar tus datos
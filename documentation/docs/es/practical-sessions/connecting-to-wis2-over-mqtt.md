---
title: Conexión a WIS2 mediante MQTT
---

# Conexión a WIS2 mediante MQTT

!!! abstract "Resultados de aprendizaje"

    Al final de esta sesión práctica, serás capaz de:

    - conectarte al WIS2 Global Broker utilizando MQTT Explorer
    - revisar la estructura de los temas de WIS2
    - revisar la estructura de los mensajes de notificación de WIS2

## Introducción

WIS2 utiliza el protocolo MQTT para anunciar la disponibilidad de datos sobre clima/meteorología/agua. El WIS2 Global Broker se suscribe a todos los WIS2 Nodes en la red y republica los mensajes que recibe. El Global Cache se suscribe al Global Broker, descarga los datos del mensaje y luego republica el mensaje en el tema `cache` con una nueva URL. El Global Discovery Catalogue publica metadatos de descubrimiento desde el Broker y proporciona una API de búsqueda.

Este es un ejemplo de la estructura de un mensaje de notificación de WIS2 para un mensaje recibido en el tema `origin/a/wis2/br-inmet/data/core/weather/surface-based-observations/synop`:

```json
{
   "id":"7a34051b-aa92-40f3-bbab-439143657c8c",
   "type":"Feature",
   "conformsTo":[
      "http://wis.wmo.int/spec/wnm/1/conf/core"
   ],
   "geometry":{
      "type":"Polygon",
      "coordinates":[
         [
            [
               -73.98723548042966,
               5.244486395687602
            ],
            [
               -34.729993455533034,
               5.244486395687602
            ],
            [
               -34.729993455533034,
               -33.768377780900764
            ],
            [
               -73.98723548042966,
               -33.768377780900764
            ],
            [
               -73.98723548042966,
               5.244486395687602
            ]
         ]
      ]
   },
   "properties":{
      "data_id":"br-inmet/metadata/urn:wmo:md:br-inmet:rr1ieq",
      "datetime":"2026-01-20T08:30:21Z",
      "pubtime":"2026-01-20T08:30:22Z",
      "integrity":{
         "method":"sha512",
         "value":"RN+GzqgONURtkzOCo5vQJ5t7SzlAvaGONywEnTXHrHew9RQmUhrHbASvmDlCeRTb8vhE+1/h/7/20f2XJFHCcA=="
      },
      "content":{
         "encoding":"base64",
         "value":"eyJpZCI6ICJ1cm46d21vOm1kOmJyLWlubWV0OnJyMWllcSIsICJjb25mb3Jtc1RvIjogWyJodHRwOi8vd2lzLndtby5pbnQvc3BlYy93Y21wLzIvY29uZi9jb3JlIl0sICJ0eXBlIjogIkZlYXR1cmUiLCAidGltZSI6IHsiaW50ZXJ2YWwiOiBbIjIwMjYtMDEtMjAiLCAiLi4iXSwgInJlc29sdXRpb24iOiAiUFQxSCJ9LCAiZ2VvbWV0cnkiOiB7InR5cGUiOiAiUG9seWdvbiIsICJjb29yZGluYXRlcyI6IFtbWy03My45ODcyMzU0ODA0Mjk2NiwgNS4yNDQ0ODYzOTU2ODc2MDJdLCBbLTM0LjcyOTk5MzQ1NTUzMzAzNCwgNS4yNDQ0ODYzOTU2ODc2MDJdLCBbLTM0LjcyOTk5MzQ1NTUzMzAzNCwgLTMzLjc2ODM3Nzc4MDkwMDc2NF0sIFstNzMuOTg3MjM1NDgwNDI5NjYsIC0zMy43NjgzNzc3ODA5MDA3NjRdLCBbLTczLjk4NzIzNTQ4MDQyOTY2LCA1LjI0NDQ4NjM5NTY4NzYwMl1dXX0sICJwcm9wZXJ0aWVzIjogeyJ0eXBlIjogImRhdGFzZXQiLCAiaWRlbnRpZmllciI6ICJ1cm46d21vOm1kOmJyLWlubWV0OnJyMWllcSIsICJ0aXRsZSI6ICJIb3VybHkgc3lub3B0aWMgb2JzZXJ2YXRpb25zIGZyb20gZml4ZWQtbGFuZCBzdGF0aW9ucyAoU1lOT1ApIChici1pbm1ldCkiLCAiZGVzY3JpcHRpb24iOiAidGVzdCIsICJrZXl3b3JkcyI6IFsib2JzZXJ2YXRpb25zIiwgInRlbXBlcmF0dXJlIiwgInZpc2liaWxpdHkiLCAicHJlY2lwaXRhdGlvbiIsICJwcmVzc3VyZSIsICJjbG91ZHMiLCAic25vdyBkZXB0aCIsICJldmFwb3JhdGlvbiIsICJyYWRpYXRpb24iLCAid2luZCIsICJ0b3RhbCBzdW5zaGluZSIsICJodW1pZGl0eSJdLCAidGhlbWVzIjogW3siY29uY2VwdHMiOiBbeyJpZCI6ICJ3ZWF0aGVyIiwgInRpdGxlIjogIldlYXRoZXIifV0sICJzY2hlbWUiOiAiaHR0cDovL2NvZGVzLndtby5pbnQvd2lzL3RvcGljLWhpZXJhcmNoeS9lYXJ0aC1zeXN0ZW0tZGlzY2lwbGluZSJ9XSwgImNvbnRhY3RzIjogW3sib3JnYW5pemF0aW9uIjogIndtbyIsICJlbWFpbHMiOiBbeyJ2YWx1ZSI6ICJ0ZXN0QGNuLmNvbSJ9XSwgImFkZHJlc3NlcyI6IFt7ImNvdW50cnkiOiAiQlJBIn1dLCAibGlua3MiOiBbeyJyZWwiOiAiYWJvdXQiLCAiaHJlZiI6ICJodHRwOi8vdGVzdC5jb20iLCAidHlwZSI6ICJ0ZXh0L2h0bWwifV0sICJyb2xlcyI6IFsiaG9zdCJdfV0sICJjcmVhdGVkIjogIjIwMjYtMDEtMjBUMDg6MzA6MjFaIiwgInVwZGF0ZWQiOiAiMjAyNi0wMS0yMFQwODozMDoyMVoiLCAid21vOmRhdGFQb2xpY3kiOiAiY29yZSIsICJpZCI6ICJ1cm46d21vOm1kOmJyLWlubWV0OnJyMWllcSJ9LCAibGlua3MiOiBbeyJocmVmIjogIm1xdHQ6Ly9ldmVyeW9uZTpldmVyeW9uZUBsb2NhbGhvc3Q6MTg4MyIsICJ0eXBlIjogImFwcGxpY2F0aW9uL2pzb24iLCAibmFtZSI6ICJvcmlnaW4vYS93aXMyL2JyLWlubWV0L2RhdGEvY29yZS93ZWF0aGVyL3N1cmZhY2UtYmFzZWQtb2JzZXJ2YXRpb25zL3N5bm9wIiwgInJlbCI6ICJpdGVtcyIsICJjaGFubmVsIjogIm9yaWdpbi9hL3dpczIvYnItaW5tZXQvZGF0YS9jb3JlL3dlYXRoZXIvc3VyZmFjZS1iYXNlZC1vYnNlcnZhdGlvbnMvc3lub3AiLCAiZmlsdGVycyI6IHsid2lnb3Nfc3RhdGlvbl9pZGVudGlmaWVyIjogeyJ0eXBlIjogInN0cmluZyIsICJ0aXRsZSI6ICJXSUdPUyBTdGF0aW9uIElkZW50aWZpZXIiLCAiZGVzY3JpcHRpb24iOiAiRmlsdGVyIGJ5IFdJR09TIFN0YXRpb24gSWRlbnRpZmllciJ9fSwgInRpdGxlIjogIk5vdGlmaWNhdGlvbnMifSwgeyJocmVmIjogImh0dHA6Ly9sb2NhbGhvc3QvbWV0YWRhdGEvZGF0YS91cm46d21vOm1kOmJyLWlubWV0OnJyMWllcS5qc29uIiwgInR5cGUiOiAiYXBwbGljYXRpb24vZ2VvK2pzb24iLCAibmFtZSI6ICJ1cm46d21vOm1kOmJyLWlubWV0OnJyMWllcSIsICJyZWwiOiAiY2Fub25pY2FsIiwgInRpdGxlIjogInVybjp3bW86bWQ6YnItaW5tZXQ6cnIxaWVxIn1dfQ==",
         "size":1957
      }
   },
   "links":[
      {
         "rel":"canonical",
         "type":"application/geo+json",
         "href":"http://localhost/data/metadata/urn:wmo:md:br-inmet:rr1ieq.json",
         "length":1957
      }
   ],
   "generated_by":"wis2box 1.2.0"
}
```

En esta sesión práctica aprenderás cómo usar la herramienta MQTT Explorer para configurar una conexión de cliente MQTT a un WIS2 Global Broker y poder visualizar mensajes de notificación de WIS2.

MQTT Explorer es una herramienta útil para explorar y revisar la estructura de temas de un broker MQTT y analizar los datos publicados.

!!! note "Sobre MQTT"
    MQTT Explorer proporciona una interfaz fácil de usar para conectarse a un broker MQTT y explorar los temas y la estructura de mensajes utilizada por WIS2.
    
    En la práctica, MQTT está diseñado para comunicación máquina a máquina, donde una aplicación o servicio se suscribe a temas y procesa mensajes programáticamente en tiempo real.
    
    Para trabajar con MQTT de forma programática (por ejemplo, en Python), puedes usar bibliotecas de cliente MQTT como [paho-mqtt](https://pypi.org/project/paho-mqtt) para conectarte a un broker MQTT y procesar mensajes entrantes. Existen numerosos software de cliente y servidor MQTT, dependiendo de tus requisitos y entorno técnico.

## Usar MQTT Explorer para conectarse al Global Broker

Para visualizar mensajes publicados por un WIS2 Global Broker puedes usar "MQTT Explorer", que se puede descargar desde el [sitio web de MQTT Explorer](https://mqtt-explorer.com).

Abre MQTT Explorer y agrega una nueva conexión al Global Broker alojado por MeteoFrance utilizando los siguientes detalles:

- host: globalbroker.meteo.fr
- port: 8883
- username: everyone
- password: everyone

<img alt="mqtt-explorer-global-broker-connection" src="/../assets/img/mqtt-explorer-global-broker-connection.png" width="800">

Haz clic en el botón 'ADVANCED', elimina los temas preconfigurados y agrega los siguientes temas para suscribirte:

- `origin/a/wis2/#`

<img alt="mqtt-explorer-global-broker-advanced" src="/../assets/img/mqtt-explorer-global-broker-sub-origin.png" width="800">

!!! note
    Al configurar suscripciones MQTT puedes usar los siguientes comodines:

    - **Nivel único (+)**: un comodín de nivel único reemplaza un nivel de tema.
    - **Nivel múltiple (#)**: un comodín de nivel múltiple reemplaza múltiples niveles de tema.

    En este caso, `origin/a/wis2/#` se suscribirá a todos los temas bajo el tema `origin/a/wis2`.

Haz clic en 'BACK', luego en 'SAVE' para guardar los detalles de tu conexión y suscripción. Luego haz clic en 'CONNECT':

Los mensajes deberían comenzar a aparecer en tu sesión de MQTT Explorer como se muestra a continuación:

<img alt="mqtt-explorer-global-broker-topics" src="/../assets/img/mqtt-explorer-global-broker-msg-origin.png" width="800">

Ahora estás listo para comenzar a explorar los temas y la estructura de mensajes de WIS2.

## Ejercicio 1: Revisar la estructura de temas de WIS2

Usa MQTT para explorar la estructura de temas bajo los temas `origin`.

!!! question
    
    ¿Cómo podemos distinguir el centro WIS que publicó los datos?

??? success "Haz clic para revelar la respuesta"

    Puedes hacer clic en la ventana del lado izquierdo en MQTT Explorer para expandir la estructura de temas.
    
    Podemos distinguir el centro WIS que publicó los datos observando el cuarto nivel de la estructura de temas. Por ejemplo, el siguiente tema:

    `origin/a/wis2/br-inmet/data/core/weather/surface-based-observations/synop`

    nos indica que los datos fueron publicados por un centro WIS con el centre-id `br-inmet`, que corresponde al Instituto Nacional de Meteorología - INMET, Brasil.

!!! question

    ¿Cómo podemos distinguir entre mensajes publicados por centros WIS que alojan un gateway GTS-to-WIS2 y mensajes publicados por centros WIS que alojan un nodo WIS2?

??? success "Haz clic para revelar la respuesta"

    Podemos distinguir los mensajes provenientes de un gateway GTS-to-WIS2 observando el centre-id en la estructura de temas. Por ejemplo, el siguiente tema:

    `origin/a/wis2/de-dwd-gts-to-wis2/data/core/I/S/A/I/01/sbbr`

    nos indica que los datos fueron publicados por el gateway GTS-to-WIS2 alojado por Deutscher Wetterdienst (DWD), Alemania. El gateway GTS-to-WIS2 es un tipo especial de publicador de datos que publica datos del Sistema Global de Telecomunicaciones (GTS) a WIS2. La estructura de temas está compuesta por los encabezados TTAAii CCCC para los mensajes GTS.

## Ejercicio 2: Revisar la estructura de mensajes de WIS2

Desconéctate de MQTT Explorer y actualiza las secciones 'Advanced' para cambiar la suscripción a lo siguiente:

* `origin/a/wis2/+/data/core/weather/surface-based-observations/synop`
* `cache/a/wis2/+/data/core/weather/surface-based-observations/synop`

<img alt="mqtt-explorer-global-broker-topics-exercise2" src="/../assets/img/mqtt-explorer-global-broker-sub-origin-cache-synop.png" width="800">

!!! note
    El comodín `+` se utiliza para suscribirse a todos los centros WIS.

Reconéctate al Global Broker y espera a que aparezcan los mensajes.

Puedes visualizar el contenido del mensaje WIS2 en la sección "Value" en el lado derecho. Intenta expandir la estructura de temas para ver los diferentes niveles del mensaje hasta llegar al último nivel y revisar el contenido de uno de los mensajes.

!!! question

    ¿Cómo podemos identificar la marca de tiempo en que se publicaron los datos? ¿Y cómo podemos identificar la marca de tiempo en que se recopilaron los datos?

??? success "Haz clic para revelar la respuesta"

    La marca de tiempo en que se publicaron los datos está contenida en la sección `properties` del mensaje con una clave llamada `pubtime`.

    La marca de tiempo en que se recopilaron los datos está contenida en la sección `properties` del mensaje con una clave llamada `datetime`.

    <img alt="mqtt-explorer-global-broker-msg-properties" src="/../assets/img/mqtt-explorer-global-broker-msg-properties.png" width="800">

!!! question

    ¿Cómo podemos descargar los datos desde la URL proporcionada en el mensaje?

??? success "Haz clic para revelar la respuesta"

    La URL está contenida en la sección `links` con `rel="canonical"` y definida por la clave `href`.

    Puedes copiar la URL y pegarla en un navegador web para descargar los datos.

## Ejercicio 3: Revisar la diferencia entre los temas 'origin' y 'cache'

Asegúrate de que sigues conectado al Global Broker utilizando las suscripciones de temas `origin/a/wis2/+/data/core/weather/surface-based-observations/synop` y `cache/a/wis2/+/data/core/weather/surface-based-observations/synop` como se describe en el Ejercicio 2.

Intenta identificar un mensaje para el mismo centre-id publicado en ambos temas `origin` y `cache`.

!!! question

    ¿Cuál es la diferencia entre los mensajes publicados en los temas `origin` y `cache`?

??? success "Haz clic para revelar la respuesta"

    Los mensajes publicados en los temas `origin` son los mensajes originales que el Global Broker republica desde los nodos WIS2 en la red.

    Los mensajes publicados en los temas `cache` son los mensajes cuyos datos han sido descargados por el Global Cache. Si revisas el contenido del mensaje del tema que comienza con `cache`, verás que el enlace 'canonical' ha sido actualizado a una nueva URL.
    
    Hay múltiples Global Caches en la red WIS2, por lo que recibirás un mensaje de cada Global Cache que haya descargado el mensaje.

    El Global Cache solo descargará y republicará mensajes que hayan sido publicados en la jerarquía de temas `../data/core/...`.

## Conclusión

!!! success "¡Felicidades!"
    En esta sesión práctica aprendiste:

    - cómo suscribirte a los servicios de WIS2 Global Broker usando MQTT Explorer
    - la estructura de temas de WIS2
    - la estructura de mensajes de notificación de WIS2
    - la diferencia entre datos principales y recomendados
    - la estructura de temas utilizada por el gateway GTS-to-WIS2
    - la diferencia entre los mensajes del Global Broker publicados en los temas `origin` y `cache`
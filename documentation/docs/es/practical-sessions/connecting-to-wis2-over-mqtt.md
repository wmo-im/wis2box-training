---
title: Conectarse a WIS2 mediante MQTT
---

# Conectarse a WIS2 mediante MQTT

!!! abstract "Resultados de aprendizaje"

    Al final de esta sesión práctica, podrás:

    - conectarte al WIS2 Global Broker utilizando MQTT Explorer
    - revisar la estructura de los temas de WIS2
    - revisar la estructura de los mensajes de notificación de WIS2

## Introducción

WIS2 utiliza el protocolo MQTT para anunciar la disponibilidad de datos meteorológicos, climáticos e hidrológicos. El WIS2 Global Broker se suscribe a todos los WIS2 Nodes en la red y republica los mensajes que recibe. El Global Cache se suscribe al Global Broker, descarga los datos del mensaje y luego republica el mensaje en el tema `cache` con una nueva URL. El Global Discovery Catalogue publica metadatos de descubrimiento desde el Broker y proporciona una API de búsqueda.

Este es un ejemplo de la estructura de un mensaje de notificación de WIS2 para un mensaje recibido en el tema `origin/a/wis2/br-inmet/data/core/weather/surface-based-observations/synop`:	

```json
{
   "id":"3c14d7bf-e6b9-4f59-b4ea-f2fc52a33cd3",
   "type":"Feature",
   "conformsTo":[
      "http://wis.wmo.int/spec/wnm/1/conf/core"
   ],
   "geometry":{
      "coordinates":[
         -99.1964,
         19.404,
         2314
      ],
      "type":"Point"
   },
   "properties":{
      "data_id":"br-inmet:data:core:weather:surface-based-observations:synop/WIGOS_0-20000-0-76679_20250206T231600",
      "datetime":"2025-02-06T23:16:00Z",
      "pubtime":"2026-01-20T13:14:52Z",
      "integrity":{
         "method":"sha512",
         "value":"qtlI3Noay2I4zcdA1XCpn8vzVLIt0RKrR398VGFgTttc1XRUVb4dHWNCDKPXUo4mNkiFKx5TTHBvrxlzqWmMnQ=="
      },
      "metadata_id":"urn:wmo:md:br-inmet:data:core:weather:surface-based-observations:synop",
      "wigos_station_identifier":"0-20000-0-76679"
   },
   "links":[
      {
         "rel":"canonical",
         "type":"application/bufr",
         "href":"http://localhost/data/2025-02-06/wis/urn:wmo:md:br-inmet:data:core:weather:surface-based-observations:synop/WIGOS_0-20000-0-76679_20250206T231600.bufr4",
         "length":125117
      },
      {
         "rel":"via",
         "type":"text/html",
         "href":"https://oscar.wmo.int/surface/#/search/station/stationReportDetails/0-20000-0-76679"
      }
   ],
   "generated_by":"wis2box 1.2.0"
}
``` 

En esta sesión práctica aprenderás a usar la herramienta MQTT Explorer para configurar una conexión de cliente MQTT a un WIS2 Global Broker y poder visualizar mensajes de notificación de WIS2.

MQTT Explorer es una herramienta útil para explorar y revisar la estructura de temas de un broker MQTT y analizar los datos que se están publicando.

!!! note "Acerca de MQTT"
    MQTT Explorer proporciona una interfaz fácil de usar para conectarse a un broker MQTT y explorar los temas y la estructura de mensajes utilizados por WIS2.
    
    En la práctica, MQTT está diseñado para ser utilizado en comunicación máquina a máquina, donde una aplicación o servicio se suscribe a temas y procesa mensajes programáticamente en tiempo real.
    
    Para trabajar con MQTT de forma programática (por ejemplo, en Python), puedes usar bibliotecas de cliente MQTT como [paho-mqtt](https://pypi.org/project/paho-mqtt) para conectarte a un broker MQTT y procesar mensajes entrantes. Existen numerosos software de cliente y servidor MQTT, dependiendo de tus requisitos y entorno técnico.

## Usar MQTT Explorer para conectarse al Global Broker

Para ver los mensajes publicados por un WIS2 Global Broker, puedes usar "MQTT Explorer", que se puede descargar desde el [sitio web de MQTT Explorer](https://mqtt-explorer.com).

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

    - **Nivel único (+)**: un comodín de nivel único reemplaza un nivel de tema
    - **Nivel múltiple (#)**: un comodín de nivel múltiple reemplaza múltiples niveles de tema

    En este caso, `origin/a/wis2/#` se suscribirá a todos los temas bajo el tema `origin/a/wis2`.

Haz clic en 'BACK', luego 'SAVE' para guardar los detalles de tu conexión y suscripción. Luego haz clic en 'CONNECT':

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

    nos indica que los datos fueron publicados por un centro WIS con el centre-id `br-inmet`, que es el centre-id del Instituto Nacional de Meteorologia - INMET, Brasil.

!!! question

    ¿Cómo podemos distinguir entre mensajes publicados por centros WIS que alojan un gateway GTS-to-WIS2 y mensajes publicados por centros WIS que alojan un WIS2 Node?

??? success "Haz clic para revelar la respuesta"

    Podemos distinguir los mensajes provenientes de un gateway GTS-to-WIS2 observando el centre-id en la estructura de temas. Por ejemplo, el siguiente tema:

    `origin/a/wis2/de-dwd-gts-to-wis2/data/core/I/S/A/I/01/sbbr`

    nos indica que los datos fueron publicados por el gateway GTS-to-WIS2 alojado por Deutscher Wetterdienst (DWD), Alemania. El gateway GTS-to-WIS2 es un tipo especial de publicador de datos que publica datos del Global Telecommunication System (GTS) a WIS2. La estructura de temas está compuesta por los encabezados TTAAii CCCC de los mensajes GTS.

## Ejercicio 2: Revisar la estructura de mensajes de WIS2

Desconéctate de MQTT Explorer y actualiza la sección 'Advanced' para cambiar la suscripción a lo siguiente:

* `origin/a/wis2/+/data/core/weather/surface-based-observations/synop`
* `cache/a/wis2/+/data/core/weather/surface-based-observations/synop`

<img alt="mqtt-explorer-global-broker-topics-exercise2" src="/../assets/img/mqtt-explorer-global-broker-sub-origin-cache-synop.png" width="800">

!!! note
    El comodín `+` se utiliza para suscribirse a todos los centros WIS.

Reconéctate al Global Broker y espera a que aparezcan mensajes. 

Puedes ver el contenido del mensaje de WIS2 en la sección "Value" en el lado derecho. Intenta expandir la estructura de temas para ver los diferentes niveles del mensaje hasta llegar al último nivel y revisar el contenido de uno de los mensajes.

!!! question

    ¿Cómo podemos identificar la marca de tiempo en la que se publicaron los datos? ¿Y cómo podemos identificar la marca de tiempo en la que se recopilaron los datos?

??? success "Haz clic para revelar la respuesta"

    La marca de tiempo en la que se publicaron los datos está contenida en la sección `properties` del mensaje con la clave `pubtime`.

    La marca de tiempo en la que se recopilaron los datos está contenida en la sección `properties` del mensaje con la clave `datetime`.

    <img alt="mqtt-explorer-global-broker-msg-properties" src="/../assets/img/mqtt-explorer-global-broker-msg-properties.png" width="800">

!!! question

    ¿Cómo podemos descargar los datos desde la URL proporcionada en el mensaje?

??? success "Haz clic para revelar la respuesta"

    La URL está contenida en la sección `links` con `rel="canonical"` y definida por la clave `href`.

    Puedes copiar la URL y pegarla en un navegador web para descargar los datos.

## Ejercicio 3: Revisar la diferencia entre los temas 'origin' y 'cache'

Asegúrate de que sigues conectado al Global Broker utilizando las suscripciones a los temas `origin/a/wis2/+/data/core/weather/surface-based-observations/synop` y `cache/a/wis2/+/data/core/weather/surface-based-observations/synop` como se describe en el Ejercicio 2.

Intenta identificar un mensaje para el mismo centre-id publicado en ambos temas, `origin` y `cache`.

!!! question

    ¿Cuál es la diferencia entre los mensajes publicados en los temas `origin` y `cache`?

??? success "Haz clic para revelar la respuesta"

    Los mensajes publicados en los temas `origin` son los mensajes originales que el Global Broker republica desde los WIS2 Nodes en la red. 

    Los mensajes publicados en los temas `cache` son los mensajes para los cuales los datos han sido descargados por el Global Cache. Si revisas el contenido del mensaje del tema que comienza con `cache`, verás que el enlace 'canonical' ha sido actualizado a una nueva URL.
    
    Hay múltiples Global Caches en la red WIS2, por lo que recibirás un mensaje de cada Global Cache que haya descargado el mensaje.

    El Global Cache solo descargará y republicará mensajes que hayan sido publicados en la jerarquía de temas `../data/core/...`.

## Conclusión

!!! success "¡Felicidades!"
    En esta sesión práctica, aprendiste:

    - cómo suscribirte a los servicios del WIS2 Global Broker utilizando MQTT Explorer
    - la estructura de temas de WIS2
    - la estructura de mensajes de notificación de WIS2
    - la diferencia entre datos core y recomendados
    - la estructura de temas utilizada por el gateway GTS-to-WIS2
    - la diferencia entre los mensajes del Global Broker publicados en los temas `origin` y `cache`
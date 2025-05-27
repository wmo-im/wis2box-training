---
title: Conectándose a WIS2 a través de MQTT
---

# Conectándose a WIS2 a través de MQTT

!!! abstract "Resultados de aprendizaje"

    Al final de esta sesión práctica, podrás:

    - conectarte al Global Broker de WIS2 usando MQTT Explorer
    - revisar la estructura de temas de WIS2
    - revisar la estructura de mensajes de notificación de WIS2

## Introducción

WIS2 utiliza el protocolo MQTT para anunciar la disponibilidad de datos de clima/agua. El Global Broker de WIS2 se suscribe a todos los WIS2 Nodes en la red y republica los mensajes que recibe. El Global Cache se suscribe al Global Broker, descarga los datos en el mensaje y luego republica el mensaje en el tema `cache` con una nueva URL. El Global Discovery Catalogue publica metadatos de descubrimiento del Broker y proporciona una API de búsqueda.

Este es un ejemplo de la estructura de mensaje de notificación de WIS2 para un mensaje recibido en el tema `origin/a/wis2/br-inmet/data/core/weather/surface-based-observations/synop`:	

```json
{
  "id": "59f9b013-c4b3-410a-a52d-fff18f3f1b47",
  "type": "Feature",
  "version": "v04",
  "geometry": {
    "coordinates": [
      -38.69389,
      -17.96472,
      60
    ],
    "type": "Point"
  },
  "properties": {
    "data_id": "br-inmet/data/core/weather/surface-based-observations/synop/WIGOS_0-76-2-2900801000W83499_20240815T060000",
    "datetime": "2024-08-15T06:00:00Z",
    "pubtime": "2024-08-15T09:52:02Z",
    "integrity": {
      "method": "sha512",
      "value": "TBuWycx/G0lIiTo47eFPBViGutxcIyk7eikppAKPc4aHgOmTIS5Wb9+0v3awMOyCgwpFhTruRRCVReMQMp5kYw=="
    },
    "content": {
      "encoding": "base64",
      "value": "QlVGUgAA+gQAABYAACsAAAAAAAIAHAAH6AgPBgAAAAALAAABgMGWx1AAAM0ABOIAAAODM0OTkAAAAAAAAAAAAAAKb5oKEpJ6YkJ6mAAAAAAAAAAAAAAAAv0QeYA29WQa87ZhH4CQP//z+P//BD////+ASznXuUb///8MgAS3/////8X///e+AP////AB/+R/yf////////////////////6/1/79H/3///gEt////////4BLP6QAf/+/pAB//4H0YJ/YeAh/f2///7TH/////9+j//f///////////////////v0f//////////////////////wNzc3Nw==",
      "size": 250
    },
    "wigos_station_identifier": "0-76-2-2900801000W83499"
  },
  "links": [
    {
      "rel": "canonical",
      "type": "application/bufr",
      "href": "http://wis2bra.inmet.gov.br/data/2024-08-15/wis/br-inmet/data/core/weather/surface-based-observations/synop/WIGOS_0-76-2-2900801000W83499_20240815T060000.bufr4",
      "length": 250
    }
  ]
}
``` 

En esta sesión práctica aprenderás a usar la herramienta MQTT Explorer para configurar una conexión de cliente MQTT al Global Broker de WIS2 y podrás visualizar mensajes de notificación de WIS2.

MQTT Explorer es una herramienta útil para explorar y revisar la estructura de temas para un broker MQTT dado para revisar los datos que se están publicando.

Ten en cuenta que MQTT se utiliza principalmente para comunicación "máquina a máquina"; lo que significa que normalmente habría un cliente que analiza automáticamente los mensajes a medida que se reciben. Para trabajar con MQTT de manera programática (por ejemplo, en Python), puedes usar bibliotecas de cliente MQTT como [paho-mqtt](https://pypi.org/project/paho-mqtt) para conectarte a un broker MQTT y procesar mensajes entrantes. Existen numerosos software de cliente y servidor MQTT, dependiendo de tus requisitos y entorno técnico.

## Usando MQTT Explorer para conectarse al Global Broker

Para ver mensajes publicados por un Global Broker de WIS2 puedes usar "MQTT Explorer" que se puede descargar desde el [sitio web de MQTT Explorer](https://mqtt-explorer.com).

Abre MQTT Explorer y agrega una nueva conexión al Global Broker alojado por MeteoFrance usando los siguientes detalles:

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

    En este caso `origin/a/wis2/#` se suscribirá a todos los temas bajo el tema `origin/a/wis2`.

Haz clic en 'BACK', luego en 'SAVE' para guardar los detalles de tu conexión y suscripción. Luego haz clic en 'CONNECT':

Los mensajes deberían comenzar a aparecer en tu sesión de MQTT Explorer de la siguiente manera:

<img alt="mqtt-explorer-global-broker-topics" src="/../assets/img/mqtt-explorer-global-broker-msg-origin.png" width="800">

Ahora estás listo para comenzar a explorar los temas y la estructura de mensajes de WIS2.

## Ejercicio 1: Revisar la estructura de temas de WIS2

Usa MQTT para explorar la estructura de temas bajo los temas `origin`.

!!! question
    
    ¿Cómo podemos distinguir el centro WIS que publicó los datos?

??? success "Haz clic para revelar la respuesta"

    Puedes hacer clic en la ventana del lado izquierdo en MQTT Explorer para expandir la estructura de temas.
    
    Podemos distinguir el centro WIS que publicó los datos mirando el cuarto nivel de la estructura de temas. Por ejemplo, el siguiente tema:

    `origin/a/wis2/br-inmet/data/core/weather/surface-based-observations/synop`

    nos dice que los datos fueron publicados por un centro WIS con el Centre ID `br-inmet`, que es el Centre ID para el Instituto Nacional de Meteorología - INMET, Brasil.

!!! question

    ¿Cómo podemos distinguir entre mensajes publicados por centros WIS que alojan una puerta de enlace GTS-to-WIS2 y mensajes publicados por centros WIS que alojan un nodo WIS2?

??? success "Haz clic para revelar la respuesta"

    Podemos distinguir los mensajes provenientes de la puerta de enlace GTS-to-WIS2 mirando el Centre ID en la estructura del tema. Por ejemplo, el siguiente tema:

    `origin/a/wis2/de-dwd-gts-to-wis2/data/core/I/S/A/I/01/sbbr`

    nos dice que los datos fueron publicados por la puerta de enlace GTS-to-WIS2 alojada por Deutscher Wetterdienst (DWD), Alemania. La puerta de enlace GTS-to-WIS2 es un tipo especial de publicador de datos que publica datos del Sistema Global de Telecomunicaciones (GTS) a WIS2. La estructura del tema está compuesta por los encabezados TTAAii CCCC para los mensajes GTS.

## Ejercicio 2: Revisar la estructura de mensajes de WIS2

Desconéctate de MQTT Explorer y actualiza las secciones 'Advanced' para cambiar la suscripción a los siguientes:

* `origin/a/wis2/+/data/core/weather/surface-based-observations/synop`
* `cache/a/wis2/+/data/core/weather/surface-based-observations/synop`

<img alt="mqtt-explorer-global-broker-topics-exercise2" src="/../assets/img/mqtt-explorer-global-broker-sub-origin-cache-synop.png" width="800">

!!! note
    El comodín `+` se utiliza para suscribirse a todos los centros WIS.

Vuelve a conectarte al Global Broker y espera a que aparezcan los mensajes.

Puedes ver el contenido del mensaje de WIS2 en la sección "Value" en el lado derecho. Intenta expandir la estructura del tema para ver los diferentes niveles del mensaje hasta llegar al último nivel y revisar el contenido del mensaje de uno de los mensajes.

!!! question

    ¿Cómo podemos identificar la marca de tiempo en que se publicaron los datos? ¿Y cómo podemos identificar la marca de tiempo en que se recopilaron los datos?

??? success "Haz clic para revelar la respuesta"

    La marca de tiempo en que se publicaron los datos está contenida en la sección `properties` del mensaje con una clave de `pubtime`.

    La marca de tiempo en que se recopilaron los datos está contenida en la sección `properties` del mensaje con una clave de `datetime`.

    <img alt="mqtt-explorer-global-broker-msg-properties" src="/../assets/img/mqtt-explorer-global-broker-msg-properties.png" width="800">

!!! question

    ¿Cómo podemos descargar los datos desde la URL proporcionada en el mensaje?

??? success "Haz clic para revelar la respuesta"

    La URL está contenida en la sección `links` con `rel="canonical"` y definida por la clave `href`.

    Puedes copiar la URL y pegarla en un navegador web para descargar los datos.

## Ejercicio 3: Revisar la diferencia entre los temas 'origin' y 'cache'

Asegúrate de seguir conectado al Global Broker usando las suscripciones de temas `origin/a/wis2/+/data/core/weather/surface-based-observations/synop` y `cache/a/wis2/+/data/core/weather/surface-based-observations/synop` como se describió en el Ejercicio 2.

Intenta identificar un mensaje para el mismo Centre ID publicado en ambos temas `origin` y `cache`.


!!! question

    ¿Cuál es la diferencia entre los mensajes publicados en los temas `origin` y `cache`?

??? success "Haz clic para revelar la respuesta"

    Los mensajes publicados en los temas `origin` son los mensajes originales que el Global Broker republica de los WIS2 Nodes en la red. 

    Los mensajes publicados en los temas `cache` son los mensajes para los datos que ha descargado el Global Cache. Si revisas el contenido del mensaje del tema que comienza con `cache`, verás que el enlace 'canonical' ha sido actualizado a una nueva URL.
    
    Hay múltiples Global Caches en la red WIS2, por lo que recibirás un mensaje de cada Global Cache que haya descargado el mensaje.

    El Global Cache solo descargará y republicará mensajes que se publicaron en la jerarquía de temas `../data/core/...`.

## Conclusión

!!! success "¡Felicidades!"
    En esta sesión práctica, aprendiste:

    - cómo suscribirte a los servicios del Global Broker de WIS2 usando MQTT Explorer
    - la estructura de temas de WIS2
    - la estructura de mensajes de notificación de WIS2
    - la diferencia entre datos básicos y recomendados
    - la estructura de temas utilizada por la puerta de enlace GTS-to-WIS2
    - la diferencia entre los mensajes del Global Broker publicados en los temas `origin` y `cache`
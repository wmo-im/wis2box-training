---
title: Conexión a WIS2 a través de MQTT
---

# Conexión a WIS2 a través de MQTT

!!! abstract "Resultados de aprendizaje"

    Al final de esta sesión práctica, podrás:

    - conectarte al Broker Global de WIS2 utilizando MQTT Explorer
    - revisar la estructura de tópicos de WIS2
    - revisar la estructura de mensajes de notificación de WIS2

## Introducción

WIS2 utiliza el protocolo MQTT para anunciar la disponibilidad de datos de clima/agua. El Broker Global de WIS2 se suscribe a todos los Nodos WIS2 en la red y republica los mensajes que recibe. El Cache Global se suscribe al Broker Global, descarga los datos en el mensaje y luego republica el mensaje en el tópico `cache` con una nueva URL. El Catálogo de Descubrimiento Global publica metadatos de descubrimiento desde el Broker y proporciona una API de búsqueda.

Este es un ejemplo de la estructura de mensaje de notificación de WIS2 para un mensaje recibido en el tópico `origin/a/wis2/br-inmet/data/core/weather/surface-based-observations/synop`:	

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

En esta sesión práctica aprenderás a usar la herramienta MQTT Explorer para configurar una conexión de cliente MQTT a un Broker Global de WIS2 y podrás visualizar mensajes de notificación de WIS2.

MQTT Explorer es una herramienta útil para explorar y revisar la estructura de tópicos para un broker MQTT dado y revisar los datos que se están publicando.

Ten en cuenta que MQTT se utiliza principalmente para la comunicación "máquina a máquina"; lo que significa que normalmente habría un cliente que analiza automáticamente los mensajes a medida que se reciben. Para trabajar con MQTT programáticamente (por ejemplo, en Python), puedes usar bibliotecas de clientes MQTT como [paho-mqtt](https://pypi.org/project/paho-mqtt) para conectarte a un broker MQTT y procesar mensajes entrantes. Existen numerosos software de cliente y servidor MQTT, dependiendo de tus requisitos y entorno técnico.

## Usando MQTT Explorer para conectarte al Broker Global

Para ver mensajes publicados por un Broker Global de WIS2 puedes usar "MQTT Explorer" que se puede descargar desde el [sitio web de MQTT Explorer](https://mqtt-explorer.com).

Abre MQTT Explorer y agrega una nueva conexión al Broker Global alojado por MeteoFrance usando los siguientes detalles:

- host: globalbroker.meteo.fr
- puerto: 8883
- usuario: everyone
- contraseña: everyone

<img alt="mqtt-explorer-global-broker-connection" src="../../assets/img/mqtt-explorer-global-broker-connection.png" width="800">

Haz clic en el botón 'ADVANCED', elimina los tópicos preconfigurados y agrega los siguientes tópicos para suscribirte:

- `origin/a/wis2/#`

<img alt="mqtt-explorer-global-broker-advanced" src="../../assets/img/mqtt-explorer-global-broker-sub-origin.png" width="800">

!!! note
    Al configurar suscripciones MQTT puedes usar los siguientes comodines:

    - **Comodín de un nivel (+)**: un comodín de un nivel reemplaza un nivel de tópico
    - **Comodín de múltiples niveles (#)**: un comodín de múltiples niveles reemplaza varios niveles de tópicos

    En este caso `origin/a/wis2/#` se suscribirá a todos los tópicos bajo el tópico `origin/a/wis2`.

Haz clic en 'BACK', luego en 'SAVE' para guardar tus detalles de conexión y suscripción. Luego haz clic en 'CONNECT':

Los mensajes deberían comenzar a aparecer en tu sesión de MQTT Explorer como sigue:

<img alt="mqtt-explorer-global-broker-topics" src="../../assets/img/mqtt-explorer-global-broker-msg-origin.png" width="800">

Ahora estás listo para comenzar a explorar los tópicos y la estructura de mensajes de WIS2.

## Ejercicio 1: Revisar la estructura de tópicos de WIS2

Usa MQTT para explorar la estructura de tópicos bajo los tópicos `origin`.

!!! question
    
    ¿Cómo podemos distinguir el centro WIS que publicó los datos?

??? success "Haz clic para revelar la respuesta"

    Puedes hacer clic en la ventana del lado izquierdo en MQTT Explorer para expandir la estructura de tópicos.
    
    Podemos distinguir el centro WIS que publicó los datos mirando el cuarto nivel de la estructura de tópicos. Por ejemplo, el siguiente tópico:

    `origin/a/wis2/br-inmet/data/core/weather/surface-based-observations/synop`

    nos dice que los datos fueron publicados por un centro WIS con el id de centro `br-inmet`, que es el id de centro para el Instituto Nacional de Meteorología - INMET, Brasil.

!!! question

    ¿Cómo podemos distinguir entre los mensajes publicados por los centros WIS que albergan una puerta de enlace de GTS a WIS2 y los mensajes publicados por los centros WIS que albergan un nodo WIS2?

??? success "Haz clic para revelar la respuesta"

    Podemos distinguir los mensajes provenientes de la puerta de enlace de GTS a WIS2 mirando el id de centro en la estructura del tópico. Por ejemplo, el siguiente tópico:

    `origin/a/wis2/de-dwd-gts-to-wis2/data/core/I/S/A/I/01/sbbr`

    nos dice que los datos fueron publicados por la puerta de enlace de GTS a WIS2 alojada por el Servicio Meteorológico Alemán (DWD), Alemania. La puerta de enlace de GTS a WIS2 es un tipo especial de publicador de datos que publica datos del Sistema Global de Telecomunicaciones (GTS) a WIS2. La estructura del tópico está compuesta por los encabezados TTAAii CCCC para los mensajes GTS.

## Ejercicio 2: Revisar la estructura de mensajes de WIS2

Desconéctate de MQTT Explorer y actualiza las secciones 'Advanced' para cambiar la suscripción a los siguientes:

* `origin/a/wis2/+/data/core/weather/surface-based-observations/synop`
* `cache/a/wis2/+/data/core/weather/surface-based-observations/synop`

<img alt="mqtt-explorer-global-broker-topics-exercise2" src="../../assets/img/mqtt-explorer-global-broker-sub-origin-cache-synop.png" width="800">

!!! note
    El comodín `+` se utiliza para suscribirse a todos los centros WIS.

Reconéctate al Broker Global y espera a que aparezcan los mensajes.

Puedes ver el contenido del mensaje de WIS2 en la sección "Value" en el lado derecho. Intenta expandir la estructura del tópico para ver los diferentes niveles del mensaje hasta llegar al último nivel y revisa el contenido del mensaje de uno de los mensajes.

!!! question

    ¿Cómo podemos identificar la marca de tiempo en que se publicaron los datos? ¿Y cómo podemos identificar la marca de tiempo en que se recopilaron los datos?

??? success "Haz clic para revelar la respuesta"

    La marca de tiempo en que se publicaron los datos está contenida en la sección `properties` del mensaje con una clave de `pubtime`.

    La marca de tiempo en que se recopilaron los datos está contenida en la sección `properties` del mensaje con una clave de `datetime`.

    <img alt="mqtt-explorer-global-broker-msg-properties" src="../../assets/img/mqtt-explorer-global-broker-msg-properties.png" width="800">

!!! question

    ¿Cómo podemos descargar los datos desde la URL proporcionada en el mensaje?

??? success "Haz clic para revelar la respuesta"

    La URL está contenida en la sección `links` con `rel="canonical"` y definida por la clave `href`.

    Puedes copiar la URL y pegarla en un navegador web para descargar los datos.

## Ejercicio 3: Revisar la diferencia entre los tópicos 'origin' y 'cache'

Asegúrate de seguir conectado al Broker Global usando las suscripciones de tópicos `origin/a/wis2/+/data/core/weather/surface-based-observations/synop` y `cache/a/wis2/+/data/core/weather/surface-based-observations/synop` como se describió en el Ejercicio 2.

Intenta identificar un mensaje para el mismo id de centro publicado tanto en los tópicos `origin` como `cache`.


!!! question

    ¿Cuál es la diferencia entre los mensajes publicados en los tópicos `origin` y `cache`?

??? success "Haz clic para revelar la respuesta"

    Los mensajes publicados en los tópicos `origin` son los mensajes originales que el Broker Global republica de los Nodos WIS2 en la red. 

    Los mensajes publicados en los tópicos `cache` son los mensajes para los datos que han sido descargados por el Cache Global. Si revisas el contenido del mensaje del tópico que comienza con `cache`, verás que el enlace 'canonical' ha sido actualizado a una nueva URL.
    
    Hay múltiples Caches Globales en la red WIS2, por lo que recibirás un mensaje de cada Cache Global que haya descargado el mensaje.

    El Cache Global solo descargará y republicará mensajes que fueron publicados en la jerarquía de tópicos `../data/core/...`.

## Conclusión

!!! success "¡Felicidades!"
    En esta sesión práctica, aprendiste:

    - cómo suscribirte a los servicios del Broker Global de WIS2 usando MQTT Explorer
    - la estructura de tópicos de WIS2
    - la estructura de mensajes de notificación de WIS2
    - la diferencia entre datos básicos y recomendados
    - la estructura de tópicos utilizada por la puerta de enlace de GTS a WIS2
    - la diferencia entre los mensajes del Broker Global publicados en los tópicos `origin` y `cache`
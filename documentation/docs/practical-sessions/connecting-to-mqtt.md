---
title: Connecting to WIS2 over MQTT
---

# Connecting to WIS2 over MQTT

!!! abstract

    In this session you will practice connecting to the WIS2 Global Broker using MQTT Explorer.

## Introduction

WIS2 uses the MQTT protocol to advertise the availability of weather/climate/water data. The WIS2 Global Broker subscribes to all WIS2 Nodes in the network and republishes the messages it receives. The Global Cache subscribes to the Global Broker, downloads the data in the message and then republishes the message on the `cache` topic with a new URL.  The Global Discovery Catalogue publishes discovery metadata from the Broker and provides a search API.

As part of the WIS2 Pilot Phase in 2023, two Global Brokers are available, one hosted by CMA and one hosted by Meteo-France.

This is an example of the WIS2-notification message structure for a message received on the topic `origin/a/wis2/arg/sabm/data/core/weather/surface-based-observations/synop`:	

```json
{
  "id": "fa587559-b02e-40a2-9fd5-2c141c39b130",
  "type": "Feature",
  "version": "v04",
  "geometry": {
    "type": "Point",
    "coordinates": [
      -56.625,
      -64.24139,
      208
    ]
  },
  "properties": {
    "data_id": "wis2/arg/sabm/data/core/weather/surface-based-observations/synop/WIGOS_0-20000-0-89055_20230926T190000",
    "datetime": "2023-09-26T19:00:00Z",
    "pubtime": "2023-09-26T18:48:51Z",
    "integrity": {
      "method": "sha512",
      "value": "5a239b5d2ba7a04bd3b2fa44a73a9fb98167d0d4424d7fd19c0a83c75a7715212e2b97b5db6581bb3e1895b92232614d4cc4841ee9164baf47183c8403668dbd"
    },
    "wigos_station_identifier": "0-20000-0-89055"
  },
  "links": [
    {
      "rel": "canonical",
      "type": "application/x-bufr",
      "href": "http://w2b.smn.gov.ar/data/2023-09-26/wis/arg/sabm/data/core/weather/surface-based-observations/synop/WIGOS_0-20000-0-89055_20230926T190000.bufr4",
      "length": 254
    },
    {
      "rel": "via",
      "type": "text/html",
      "href": "https://oscar.wmo.int/surface/#/search/station/stationReportDetails/0-20000-0-89055"
    }
  ]
}
``` 

In this practical session you will learn how to use the MQTT Explorer tool to review the topics available on this Global Broker and be able to display WIS2 notification messages.

MQTT Explorer is a helpful tool to review the topic structure for a given MQTT broker and visually work with the MQTT protocol. There exist many MQTT client and server software. 
    
To work with MQTT programmatically (for example, in Python), you can use MQTT client libraries such as [paho-mqtt](https://pypi.org/project/paho-mqtt/) to connect to an MQTT broker and process incoming messages.

## Using MQTT Explorer to connect to the Global Broker

One way to view messages published by this Global Broker is using the MQTT Explorer which can be downloaded from the [MQTT Explorer website](https://mqtt-explorer.com).

Open MQTT Explorer and add a new connection to the Global Broker hosted by CMA using the following details:

- host: gb.wis.cma.cn
- port: 8883
- username: everyone
- password: everyone

<img alt="mqtt-explorer-global-broker-connection" src="../../assets/img/mqtt-explorer-global-broker-connection-china.png" width="600">

Click on the 'ADVANCED' button and add the following topics to subscribe to:

- origin/#
- cache/#

<img alt="mqtt-explorer-global-broker-advanced" src="../../assets/img/mqtt-explorer-global-broker-advanced.png" width="600">

!!! note
    When setting up MQTT subscriptions you can use the following wildcards:

    - **Single-level (+)**: a single-level wildcard replaces one topic level
    - **Multi-level (#)**: a multi-level wildcard replaces multiple topic levels

Click 'BACK', then 'SAVE' to save your connection and subscription details.  Then click 'CONNECT':

Wait a little a bit and messages should start appearing in your MQTT Explorer session:

<img alt="mqtt-explorer-global-broker-topics" src="../../assets/img/mqtt-explorer-global-broker-topics.png" width="600">

You are now ready to start exploring the WIS2 topics and message structure.

## Exercise 1: Review the WIS2 topic structure

Use MQTT to browse topic structure under the `origin` and `cache` topics.

!!! question
    
    How can we distinguish the originating country providing the data? 

??? note "Click to reveal answer"

    We can distinguish the originating country by looking at the fourth level of the topic structure.  For example, the following topic:

    `origin/a/wis2/zmb/zambia_met_service/data/core/weather/surface-based-observations/synop`

    tells us that the data was published by Zambia (zmb). 
    
    The fifth level of the topic structure provides the id of the centre where the data originated from
    (in this case, the Zambia Meteorological Service).

!!! question

    How can we distinguish the data type?

??? note "Click to reveal answer"

    We can distinguish the data type by looking at the ninth of the topic structure.  For example, the following topic:

    `origin/a/wis2/zmb/zambia_met_service/data/core/weather/surface-based-observations/synop`

    tells us that the data type is surface-based observations (synop).

## Exercise 2: Review the WIS2 message structure

Disconnect from MQTT Explorer and update the 'Advanced' sections to change the subscription to the following:

* origin/a/wis2/+/+/data/core/weather/surface-based-observations/synop
* cache/a/wis2/+/+/data/core/weather/surface-based-observations/synop

<img alt="mqtt-explorer-global-broker-topics-exercise2" src="../../assets/img/mqtt-explorer-global-broker-topics-exercise2.png" width="600">

!!! note
    The `+` wildcard is used to subscribe to all countries (fourth level) and centres (fifth level) while the remaining topic structure is fixed to ensure we subscribe to sub-topics `data/core/weather/surface-based-observations/synop`.	

Wait for a bit until messages start appearing again.

You can view the content of the WIS2 message in the "Value" section on the right hand side.

!!! question

    How can we identify the timestamp that the data was published? And how can we identify the timestamp that the data was collected?

??? note "Click to reveal answer"

    The timestamp that the data was published is contained in the "properties"-section of the message with a key of "pubtime".

    The timestamp that the data was collected is contained in the "properties"-section of the message with a key of "datetime".

!!! question

    How can we download the data from the URL provided in the message?

??? note "Click to reveal answer"

    The URL is contained in the "links"-section with "rel"="canonical" and defined by the "href"-key.

    You can copy the URL and paste it into a web browser to download the data.

## Exercise 3: cache vs origin topics

The same message is published on both the `origin` and `cache` topics. Find a message that has been published on both topics and compare the content.

!!! question

    What is the difference between the messages published on the `origin` and `cache` topics?

??? note "Click to reveal answer"

    The message published on the `origin` topic contains a URL to the original data.  The message published on the `cache` topic contains a URL to the data cached by the Global Cache.

## Conclusion

!!! success "Congratulations!"
    In this practical session, you learned:

    - how to subscribe to WIS2 Global Broker services using MQTT Explorer
    - the WIS2 topic structure
    - the WIS2 notification message structure
    - the difference between Global Broker messages published on the `origin` and `cache` topics

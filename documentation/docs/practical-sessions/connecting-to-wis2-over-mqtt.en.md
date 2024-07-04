---
title: Connecting to WIS2 over MQTT
---

# Connecting to WIS2 over MQTT

!!! abstract "Learning outcomes"

    By the end of this practical session, you will be able to:

    - connect to the WIS2 Global Broker using MQTT Explorer
    - review the WIS2 topic structure
    - review the WIS2 notification message structure

## Introduction

WIS2 uses the MQTT protocol to advertise the availability of weather/climate/water data. The WIS2 Global Broker subscribes to all WIS2 Nodes in the network and republishes the messages it receives. The Global Cache subscribes to the Global Broker, downloads the data in the message and then republishes the message on the `cache` topic with a new URL.  The Global Discovery Catalogue publishes discovery metadata from the Broker and provides a search API.

This is an example of the WIS2 notification message structure for a message received on the topic `origin/a/wis2/arg/sabm/data/core/weather/surface-based-observations/synop`:	

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

In this practical session you will learn how to use the MQTT Explorer tool to setup an MQTT-client connection to a WIS2 Global Broker and be able to display WIS2 notification messages.

MQTT Explorer is a helpful tool to browse and review the topic structure for a given MQTT broker to review data being published.

Note that MQTT is primarily used for "machine-to-machine" communication; meaning that there would normally be a client automatically parsing the messages as they are received. To work with MQTT programmatically (for example, in Python), you can use MQTT client libraries such as [paho-mqtt](https://pypi.org/project/paho-mqtt) to connect to an MQTT broker and process incoming messages. There exist numerous MQTT client and server software, depending on your requirements and technical environment.

## Using MQTT Explorer to connect to the Global Broker

To view messages published by a WIS2 Global Broker you can "MQTT Explorer" which can be downloaded from the [MQTT Explorer website](https://mqtt-explorer.com).

Open MQTT Explorer and add a new connection to the Global Broker hosted by China Meteorological Administration using the following details:

- host: globalbroker.meteo.fr
- port: 8883
- username: everyone
- password: everyone

<img alt="mqtt-explorer-global-broker-connection" src="../../assets/img/mqtt-explorer-global-broker-connection.png" width="600">

Click on the 'ADVANCED' button and add the following topics to subscribe to:

- `origin/#`
- `cache/#`

<img alt="mqtt-explorer-global-broker-advanced" src="../../assets/img/mqtt-explorer-global-broker-advanced.png" width="600">

!!! note
    When setting up MQTT subscriptions you can use the following wildcards:

    - **Single-level (+)**: a single-level wildcard replaces one topic level
    - **Multi-level (#)**: a multi-level wildcard replaces multiple topic levels

Click 'BACK', then 'SAVE' to save your connection and subscription details.  Then click 'CONNECT':

Messages should start appearing in your MQTT Explorer session as follows:

<img alt="mqtt-explorer-global-broker-topics" src="../../assets/img/mqtt-explorer-global-broker-topics.png" width="600">

You are now ready to start exploring the WIS2 topics and message structure.

## Exercise 1: Review the WIS2 topic structure

Use MQTT to browse topic structure under the `origin` and `cache` topics.

!!! question
    
    How can we distinguish the WIS centre that published the data?

??? success "Click to reveal answer"

    We can distinguish the WIS centre that published the data by looking at the fourth level of the topic structure.  For example, the following topic:

    `origin/a/wis2/zm-zmd/data/core/weather/surface-based-observations/synop`

    tells us that the data was published a WIS centre with the centre-id `zm-zmd` (in this case, the Zambia Meteorological Service).

!!! question

    How can we distinguish between core and recommended data?

??? success "Click to reveal answer"

    We can distinguish the data type by looking at the fifth level of the topic structure.  For example, the following topic:

    `origin/a/wis2/zm-zmd/data/core/weather/surface-based-observations/synop`

    tells us that the data is a core dataset.  If the topic was:

    `origin/a/wis2/zm-zmd/data/recommended/weather/surface-based-observations/synop`

    then the data would be a recommended dataset.

## Exercise 2: Review the WIS2 message structure

Disconnect from MQTT Explorer and update the 'Advanced' sections to change the subscription to the following:

* `origin/a/wis2/+/data/core/weather/surface-based-observations/#`

<img alt="mqtt-explorer-global-broker-topics-exercise2" src="../../assets/img/mqtt-explorer-global-broker-topics-exercise2.png" width="600">

!!! note
    The `+` wildcard is used to subscribe to all WIS-centres. The `#` wildcard is used to subscribe to all sub-topics under the `surface-based-observations` topic.

Re-connect to the Global Broker and wait for messages to appear. 

You can view the content of the WIS2 message in the "Value" section on the right hand side.

!!! question

    How can we identify the timestamp that the data was published? And how can we identify the timestamp that the data was collected?

??? success "Click to reveal answer"

    The timestamp that the data was published is contained in the `properties` section of the message with a key of `pubtime`.

    The timestamp that the data was collected is contained in the `properties` section of the message with a key of `datetime`.

!!! question

    How can we download the data from the URL provided in the message?

??? success "Click to reveal answer"

    The URL is contained in the `links` section with `rel="canonical"` and defined by the `href` key.

    You can copy the URL and paste it into a web browser to download the data.

## Exercise 3: Review the WIS2 topic structure for the GTS-to-WIS2 gateway

Disconnect from MQTT Explorer and update the 'Advanced' sections to change the subscription to the following:

* `origin/a/de-dwd-gts-to-wis2/#`
* `cache/a/de-dwd-gts-to-wis2/#`

<img alt="mqtt-explorer-global-broker-topics-exercise4" src="../../assets/img/mqtt-explorer-global-broker-topics-exercise4.png" width="600">

Re-connect to the Global Broker and wait for messages to appear.

!!! question

    What is the difference between the topic structure for the GTS-to-WIS2 gateway and the WIS2 topics?

??? success "Click to reveal answer"

    The topic structure for the GTS-to-WIS2 gateway is different from the WIS2 topics. The postfix 'gts-to-wis2' indicates that this data-publisher is a GTS-to-WIS2 gateway, serving as a bridge between the GTS and WIS2. The GTS-to-WIS2 gateway uses a topic-hierarchy composed by the TTAAii CCCC headers for the GTS messages.

!!! question

    What is the difference between the messages published on the `origin` and `cache` topics?

??? success "Click to reveal answer"

    The messages published on the `origin` topics are the original messages received by the Global Broker. The messages published on the `cache` topics are the messages that have been downloaded by the Global Cache and republished with a new URL. Note that the Global Cache will only download and republish messages that were published on the `../data/core/...` topic hierarchy.

## Conclusion

!!! success "Congratulations!"
    In this practical session, you learned:

    - how to subscribe to WIS2 Global Broker services using MQTT Explorer
    - the WIS2 topic structure
    - the WIS2 notification message structure
    - the difference between core and recommended data
    - the topic structure used by the GTS-to-WIS2 gateway
    - the difference between Global Broker messages published on the `origin` and `cache` topics

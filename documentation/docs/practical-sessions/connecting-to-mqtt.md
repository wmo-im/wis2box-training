---
title: Connecting to WIS2 over MQTT
---

# Connecting to WIS2 over MQTT

## Introduction

WIS2 uses the MQTT protocol to advertise the availability of weather/climate/water data. The WIS2 Global Broker subscribes to all WIS2 Nodes in the network and republishes the messages it receives. The Global Cache subscribes to the Global Broker, downloads the data in the message and then republishes the message on the `cache` topic with a new URL.  The Global Discovery Catalogue publishes discovery metadata from the Broker and provides a search API.

As part of the WIS2 Pilot Phase in 2023, the following Global Broker services are available:

### Météo-France

- host: globalbroker.meteo.fr
- port: 8883
- username: everyone
- password: everyone

### CMA

- host: gb.wis.cma.cn
- port: 8883
- username: everyone
- password: everyone

In this practical session you will learn how to use the MQTT Explorer tool to review the topics available on this Global Broker and be able to display WIS2 notification messages.

## Using MQTT Explorer to connect to the Global Broker

One way to view messages published by this Global Broker is using the MQTT Explorer which can be downloaded from the [MQTT Explorer website](https://mqtt-explorer.com).

Open MQTT Explorer and add a new connection as follows:

<img alt="mqtt-explorer-global-broker-connection" src="../../assets/img/mqtt-explorer-global-broker-connection.png" width="600">

Click on the 'ADVANCED' button and add the following topics to subscribe to:

<img alt="mqtt-explorer-global-broker-advanced" src="../../assets/img/mqtt-explorer-global-broker-advanced.png" width="600">

!!! note
    When setting up MQTT subscriptions you can use the following wildcards:

    - **Single-level (+)**: a single-level wildcard replaces one topic level
    - **Multi-level (#)**: a multi-level wildcard replaces multiple topic levels

Click 'BACK', then 'SAVE' to save your connection and subscription details.  Then click 'CONNECT':

At this point, the following should appear in the MQTT Explorer session:

<img alt="mqtt-explorer-global-broker-topics" src="../../assets/img/mqtt-explorer-global-broker-topics.png" width="600">

You are now ready to start exploring the WIS2 topics and message structure and answer the following questions:

!!! question "Review the WIS2 topic structure"
    Use MQTT to browse topic structure under the `origin` and `cache` topics.
    
    How can we distinguish the originating country providing the data?
    
    How many countries are sharing data?

!!! question "Zambia data from origin"
    Find the latest message received in the following topic:

    `origin/a/wis2/zmb/zambia_met_service/data/core/weather/surface-based-observations/synop`

    You can view the content of the WIS2 message in the "Value" section on the right hand side.

    What is the timestamp in UTC for when this data was published?

    What is the URL from which we can download the data in BUFR format?

!!! question "Zambia data from cache"
    Find the latest message received on the following topic:

    `cache/a/wis2/zmb/zambia_met_service/data/core/weather/surface-based-observations/synop`

    What is the timestamp in UTC for when this data was published?

    What is the URL we can use to download the data?  What is the difference between this URL and the URL in the previous question?

!!! note
    MQTT Explorer is a helpful tool to review the topic structure for a given MQTT broker and visually work with the MQTT protocol. There exist many MQTT client and server software. 
    
    To work with MQTT programmatically (for example, in Python), you can use MQTT client libraries such as [paho-mqtt](https://pypi.org/project/paho-mqtt/) to connect to an MQTT broker and process incoming messages.

## Conclusion

!!! success "Congratulations!"
    Congratulations!  In this practical session, you learned:

    - how to subscribe to WIS2 Global Broker services using MQTT Explorer
    - the WIS2 topic structure
    - the WIS2 notification message structure
    - the difference between Global Broker messages published on the `origin` and `cache` topics

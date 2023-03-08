---
title: Connecting to WIS2 over MQTT
---

# Connecting to WIS2 over MQTT

## Introduction

WIS2.0 uses the MQTT protocol to advertize the availability of weather data. The WIS2 Global Broker subscribes to all WIS2-nodes in the network and republishes the messages it receives. The Global Cache subscribes to the Global Broker, downloads the data in the message and then republishes the message on the 'cache'-topic with a new URL.

As part of the WIS2 Pilot Phase, MeteoFrance is running a Global Broker. In this practical session you will learn how to use MQTT explorer to review the topics available on this Global Broker and see what the WIS2-message structure looks like.

## Using MQTT-explorer to connect to the Global Broker

One way to view messages published by this Global Broker is using the tool ‘MQTT-explorer’ which can be downloaded [here](https://mqtt-explorer.com/).

Open MQTT-explorer and prepare the following new connection:

<img alt="mqtt-explorer-global-broker-connection" src="../../assets/img/mqtt-explorer-global-broker-connection.png" width="600">

Click on 'advanced' and setup the following subscriptions:

<img alt="mqtt-explorer-global-broker-advanced" src="../../assets/img/mqtt-explorer-global-broker-advanced.png" width="600">

!!! note
    When setting up MQTT-subscriptions you can use the following wildcards:

    - **Single-level (+)** A single-level wildcard replaces one topic level
    - **Multi-level (#)** A multi-level wildcard replaces multiple topic levels

Click 'back', then 'save' to save your setup then click 'connect':

You should see the following:

<img alt="mqtt-explorer-global-broker-topics" src="../../assets/img/mqtt-explorer-global-broker-topics.png" width="600">

You are now ready to start exploring the WIS2 topics and message structure and answer the following questions:

!!! question
    How to distinguish the originating country providing the data? How many countries can you identify sharing data?

!!! question
    Find the latest message received on the following topic: **'origin/a/wis2/mwi/malawi_wmo_demo/data/core/weather/surface-based-observations/synop'**. 
    
    What is the URL from which you can download the data in .bufr format ?

!!! question
    Find the latest message received on the following topic: **'cache/a/wis2/mwi/malawi_wmo_demo/data/core/weather/surface-based-observations/synop'**. 
        
    What is the URL you can use to download the data? What is the difference between the url in the previous question ?

!!! question
    How does the WIS2-message define the location where the data was observed? And how you can determine the time that the data was published ?

!!! note
    MQTT-explorer can be a helpful tool to review the topic-structure on a MQTT broker.  To setup an MQTT-subscription and parse the message-content in real-time you can use various software-libraries, such as paho-mqtt for python.

## Learning outcomes

Learning outcomes for this session:

- know how to subscribe to the MeteoFrance Global Broker using MQTT-explorer
- be familiar with the WIS2 topic structure
- be familiar with the WIS2 message structure
- understand the difference between messages published on the origin and cache topic



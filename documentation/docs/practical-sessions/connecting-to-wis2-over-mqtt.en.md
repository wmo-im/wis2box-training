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

This is an example of the WIS2 notification message structure for a message received on the topic `origin/a/wis2/br-inmet/data/core/weather/surface-based-observations/synop`:	

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

In this practical session you will learn how to use the MQTT Explorer tool to setup an MQTT client connection to a WIS2 Global Broker and be able to display WIS2 notification messages.

MQTT Explorer is a useful tool to browse and review the topic structure for a given MQTT broker to review data being published.

Note that MQTT is primarily used for "machine-to-machine" communication; meaning that there would normally be a client automatically parsing the messages as they are received. To work with MQTT programmatically (for example, in Python), you can use MQTT client libraries such as [paho-mqtt](https://pypi.org/project/paho-mqtt) to connect to an MQTT broker and process incoming messages. There exist numerous MQTT client and server software, depending on your requirements and technical environment.

## Using MQTT Explorer to connect to the Global Broker

To view messages published by a WIS2 Global Broker you can "MQTT Explorer" which can be downloaded from the [MQTT Explorer website](https://mqtt-explorer.com).

Open MQTT Explorer and add a new connection to the Global Broker hosted by MeteoFrance using the following details:

- host: globalbroker.meteo.fr
- port: 8883
- username: everyone
- password: everyone

<img alt="mqtt-explorer-global-broker-connection" src="../../assets/img/mqtt-explorer-global-broker-connection.png" width="800">

Click on the 'ADVANCED' button, remove the pre-configured topics and add the following topics to subscribe to:

- `origin/a/wis2/#`

<img alt="mqtt-explorer-global-broker-advanced" src="../../assets/img/mqtt-explorer-global-broker-sub-origin.png" width="800">

!!! note
    When setting up MQTT subscriptions you can use the following wildcards:

    - **Single-level (+)**: a single-level wildcard replaces one topic level
    - **Multi-level (#)**: a multi-level wildcard replaces multiple topic levels

    In this case `origin/a/wis2/#` will subscribe to all topics under the `origin/a/wis2` topic.

Click 'BACK', then 'SAVE' to save your connection and subscription details.  Then click 'CONNECT':

Messages should start appearing in your MQTT Explorer session as follows:

<img alt="mqtt-explorer-global-broker-topics" src="../../assets/img/mqtt-explorer-global-broker-msg-origin.png" width="800">

You are now ready to start exploring the WIS2 topics and message structure.

## Exercise 1: Review the WIS2 topic structure

Use MQTT to browse topic structure under the `origin` topics.

!!! question
    
    How can we distinguish the WIS centre that published the data?

??? success "Click to reveal answer"

    You can click on the left hand side window in MQTT Explorer to expand the topic structure.
    
    We can distinguish the WIS centre that published the data by looking at the fourth level of the topic structure.  For example, the following topic:

    `origin/a/wis2/br-inmet/data/core/weather/surface-based-observations/synop`

    tells us that the data was published a WIS centre with the centre-id `br-inmet`, which is the centre-id for Instituto Nacional de Meteorologia - INMET, Brazil.

!!! question

    How can we distinguish between messages published by WIS-centres hosting a GTS-to-WIS2 gateway and messages published by WIS-centres hosting a WIS2 node?

??? success "Click to reveal answer"

    We can distinguish messages coming from GTS-to-WIS2 gateway by looking at the centre-id in the topic structure. For example, the following topic:

    `origin/a/wis2/de-dwd-gts-to-wis2/data/core/I/S/A/I/01/sbbr`

    tells us that the data was published by the GTS-to-WIS2 gateway hosted by Deutscher Wetterdienst (DWD), Germany. The GTS-to-WIS2 gateway is a special type of data-publisher that publishes data from the Global Telecommunication System (GTS) to WIS2. The topic structure is composed by the TTAAii CCCC headers for the GTS messages.

## Exercise 2: Review the WIS2 message structure

Disconnect from MQTT Explorer and update the 'Advanced' sections to change the subscription to the following:

* `origin/a/wis2/+/data/core/weather/surface-based-observations/synop`
* `cache/a/wis2/+/data/core/weather/surface-based-observations/synop`

<img alt="mqtt-explorer-global-broker-topics-exercise2" src="../../assets/img/mqtt-explorer-global-broker-sub-origin-cache-synop.png" width="800">

!!! note
    The `+` wildcard is used to subscribe to all WIS-centres.

Reconnect to the Global Broker and wait for messages to appear. 

You can view the content of the WIS2 message in the "Value" section on the right hand side. Try to expand the topic structure to see the different levels of the message until you reach the last level and review message content of one of the messages.

!!! question

    How can we identify the timestamp that the data was published? And how can we identify the timestamp that the data was collected?

??? success "Click to reveal answer"

    The timestamp that the data was published is contained in the `properties` section of the message with a key of `pubtime`.

    The timestamp that the data was collected is contained in the `properties` section of the message with a key of `datetime`.

    <img alt="mqtt-explorer-global-broker-msg-properties" src="../../assets/img/mqtt-explorer-global-broker-msg-properties.png" width="800">

!!! question

    How can we download the data from the URL provided in the message?

??? success "Click to reveal answer"

    The URL is contained in the `links` section with `rel="canonical"` and defined by the `href` key.

    You can copy the URL and paste it into a web browser to download the data.

## Exercise 3: Review the difference between 'origin' and 'cache' topics

Make sure you are still connected to the Global Broker using the topic subscriptions `origin/a/wis2/+/data/core/weather/surface-based-observations/synop` and `cache/a/wis2/+/data/core/weather/surface-based-observations/synop` as described in Exercise 2.

Try to identify a message for the same centre-id published on both the `origin` and `cache` topics.


!!! question

    What is the difference between the messages published on the `origin` and `cache` topics?

??? success "Click to reveal answer"

    The messages published on the `origin` topics are the original messages which the Global Broker republishes from the WIS2 Nodes in the network. 

    The messages published on the `cache` topics are the messages for data has been downloaded by the Global Cache. If you check the content of the message from the topic starting with `cache`, you will see that the 'canonical' link has been updated to a new URL.
    
    There are multiple Global Caches in the WIS2 network, so you will receive one message from each Global Cache that has downloaded the message.

    The Global Cache will only download and republish messages that were published on the `../data/core/...` topic hierarchy.

## Conclusion

!!! success "Congratulations!"
    In this practical session, you learned:

    - how to subscribe to WIS2 Global Broker services using MQTT Explorer
    - the WIS2 topic structure
    - the WIS2 notification message structure
    - the difference between core and recommended data
    - the topic structure used by the GTS-to-WIS2 gateway
    - the difference between Global Broker messages published on the `origin` and `cache` topics

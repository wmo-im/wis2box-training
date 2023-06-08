---
title: wis2box introduction
---

#  wis2box introduction

## Introduction

In this session you will run the wis2box software that was pre-installed on your student VM using the test data configuration.

You will review and access the services provided by your wis2box: the MQTT broker and HTTP accessible services and view how the services work when manually ingesting some test-data.

!!! note "wis2box installation and configuration"
    The latest wis2box release has been pre-installed on your student VM using the release archive available on GitHub:

    ```bash
    wget https://github.com/wmo-im/wis2box/releases/download/1.0b3/wis2box-setup-1.0b3.zip
    unzip wis2box-setup-1.0b3.zip
    ```
    
    You can always find the latest 'wis2box-setup' archive at [https://github.com/wmo-im/wis2box/releases](https://github.com/wmo-im/wis2box/releases).

    Your student VM has been pre-configured with a dataset for Malawi and includes some previously ingested data. Later during this training you will learn how to setup datasets of your own.

    All the required steps for installation and configuration of the wis2box can be found in the [wis2box-documentation](https://docs.wis2box.wis.wmo.int/en/latest/)

## Preparation

Login to your designated VM with your username and password.

## wis2box start and status

Navigate to the directory containing the wis2box software stack:

```bash
cd ~/wis2box-1.0b3
```

Start wis2box with the following command:

```bash
python3 wis2box-ctl.py start
```

Inspect the status with the following command:

```bash
python3 wis2box-ctl.py status
```

Repeat this command until all services are up and running.

!!! question
    What services are running? Which ports are used for each service?

!!! note "wis2box and Docker"
    wis2box runs as a set of Docker containers managed by docker-compose.
    
    The services are defined in the various `docker-compose*.yml` which can be found in the `~/wis2box-1.0b3/` directory.
    
    The Python script `wis2box-ctl.py` is used to run the underlying Docker Compose commands that control the wis2box services.

## wis2box UI

Open a web browser and visit the page `http://<your-host>`.

This is the default wis2box web application (running via the **wis2box-ui** container). 

Click the "EXPLORE" option on `http://<your-host>`.

!!! question "View latest data per station on the wis2box UI"
    Click on on a station in the station list or hover your mouse over a station in the map to see the latest data for that station.

<img alt="wis2box-ui-map.png" src="../../assets/img/wis2box-ui-map.png" width="600">

!!! question "View data profile over time per measured variable"
    After selecting a station in the map, click on "data" and select a variable to see a graph of the measured variable over time.

<img alt="wis2box-ui-data.png" src="../../assets/img/wis2box-ui-data.png" width="600">

!!! question
    What is last timestamp in UTC for which the Malawi station "Bilira" received data?

## wis2box API

Open a new tab and navigate to the page `http://<your-host>/oapi`.

<img alt="wis2box-api.png" src="../../assets/img/wis2box-api.png" width="600">

This is the wis2box API (running via the **wis2box-api** container).

To view collections currently published to the API, click `View the collections in this service`.

!!! question
     What collections are currently available?
!!! question
    How many data notifications have been published?
!!! question
    How many stations are configured?

## wis2box-broker

Open the MQTT Explorer on your computer and prepare a new connection to connect to your broker (running via the **wis2box-broker** container).

Use the following connection details:

- **Protocol: mqtt://**
- **Host: `<your-host>`**
- **Port: 1883**
- **Username: wis2box**
- **Password: wis2box**
- under 'ADVANCED', subscribe to the topics `$SYS/#` and `origin/#`

Make sure to click "SAVE" to store your connection details.

<img alt="mqtt-explorer-wis2box-broker.png" src="../../assets/img/mqtt-explorer-wis2box-broker.png" width="600">

Once you are connected, you should see statistics being published by your broker on the `$SYS` topic.

Make sure MQTT Explorer is connected to your broker before proceeding to the next exercise: 

## Publishing WIS2 data

To demonstrate how wis2box can publish WIS2 data we will manually ingest some data from the command line:

In your SSH client window, ensure you are in the `~/wis2box-1.0b3` directory and login to the **wis2box-management** container as follows:

```bash
cd ~/wis2box-1.0b3/
python3 wis2box-ctl.py login
```

!!! note
    This command is equivalent to `docker exec -it wis2box-management /bin/bash`, meaning that you have entered an interactive shell inside the **wis2box-management** container.

Run the following command to ingest some additional data:
```bash
wis2box data ingest -th mwi.mwi_wmo_demo.data.core.weather.surface-based-observations.synop -p /data/wis2box/observations/malawi-new-data/
```

After the data ingest runs successfully, you should be able to view new messages that have been published on your wis2box broker in MQTT Explorer.

!!! question
    What is the topic used to publish notifications for new data? How many WIS2 data notifications have been published?

!!! question "download data"
    What is the URL that allows you to download the published data in BUFR-format?
    Copy and paste the URL in your browser to verify you can download the corresponding `.bufr4` file.

Go back to your browser and visit the wis2box UI.

!!! question "review new data"
    Did your new data appear in wis2box? Find the stations for which you ingested new data and verify new data is available.

## Publishing WIS2 data with access control

We will now publish some more data on the topic containing `data.recommended`

In your SSH client window, login to the **wis2box-management** container:

```bash
cd ~/wis2box-1.0b3/
python3 wis2box-ctl.py login
```

Run the following command to ingest some additional data:
```bash
wis2box data ingest -th mwi.mwi_wmo_demo.data.recommended.weather.surface-based-observations.synop -p /data/wis2box/observations/malawi-new-data/
```

!!! question
    What is the topic used to publish notifications for the new data? How many WIS2 data notifications have been published?

!!! question "download data"
    What is the URL that allows you to download the newly published data in BUFR-format?
    Copy and paste the URL in your browser to verify you can download the corresponding `.bufr4` file.

!!! note "Downloading restricted data"
    You will not be able to download the data using the URL in the message published on `origin/a/wis2/mwi/mwi_wmo_demo/data/recommended/` as the data access has been restricted by the data supplier.

The data is currently restricted with the access-token `mysecrettoken`. In order to download the data you would need to add this token to the header:

```bash
wget --header "Authorization: Bearer mysecrettoken" http://testuser.wis2.training/data/2023-06-07/wis/mwi/mwi_wmo_demo/data/recommended/weather/surface-based-observations/synop/WIGOS_0-454-2-AWSCHIKWAWA_20230607T085500.bufr4
```

## Conclusion

!!! success "Congratulations!"
    In this practical session, you learned how to:

    - start wis2box and check the status of its components
    - ingest some data test observations
    - access the wis2box UI, API, MinIO UI and Grafana dashboard
    - use access control for restricted datasets

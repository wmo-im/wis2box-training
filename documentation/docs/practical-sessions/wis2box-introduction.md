---
title: Initializing the wis2box
---

#  Initializing the wis2box

## Introduction

In this session you will prepare the initial configuration of your wis2box and start the services.

!!! note "wis2box installation and configuration"
    The latest wis2box release has been pre-installed on your student VM using the release archive available on GitHub:

    ```bash
    wget https://github.com/wmo-im/wis2box/releases/download/1.0b5/wis2box-setup-1.0b5.zip
    unzip wis2box-setup-1.0b5.zip
    ```
    
    You can always find the latest 'wis2box-setup' archive at [https://github.com/wmo-im/wis2box/releases](https://github.com/wmo-im/wis2box/releases).

    All the required steps for installation and configuration of the wis2box can be found in the [wis2box-documentation](https://docs.wis2box.wis.wmo.int/en/latest/)

## Preparation

Login to your designated VM with your username and password.

## wis2box start and status

Navigate to the directory containing the wis2box software stack:

```bash
cd ~/wis2box-1.0b5
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
    
    The services are defined in the various `docker-compose*.yml` which can be found in the `~/wis2box-1.0b4/` directory.
    
    The Python script `wis2box-ctl.py` is used to run the underlying Docker Compose commands that control the wis2box services.

## wis2box webapp

Open a web browser and visit the page `http://<your-host>/wis2box-webapp`.

This is the (new) wis2box web-application where you can ingest SYNOP and csv data and manage your station metadata.

## wis2box UI

Open a web browser and visit the page `http://<your-host>`.

The wis2box UI will display your configured datasets and allow you to view surface based weather observations published by your wis2box.

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

## Conclusion

!!! success "Congratulations!"
    In this practical session, you learned how to:

    - Run the wis2box-create-config script to create the initial configuration
    - Start wis2box and check the status of its components
    - access the wis2box-webapp, API, MinIO UI and Grafana dashboard

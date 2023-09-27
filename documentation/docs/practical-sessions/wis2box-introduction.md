---
title: Initializing the wis2box
---

#  Initializing the wis2box

!!! abstract

    In this session you will prepare the initial configuration of your wis2box and start the services.


The current training materials are using wis2box-1.0b5. See [accessing-your-student-vm](accessing-your-student-vm.md) for instructions on how to download and install the wis2box software stack if you are running this training outside of a local training session.

## Preparation

Login to your designated VM with your username and password and ensure you are in the 'wis2box-1.0b5' directory:

```bash
cd ~/wis2box-1.0b5
```

## wis2box-create-config

The wis2box-create-config script is used to create the initial configuration of your wis2box. 

It will ask you a set of question to help setup your configuration.

You will be able to review and update the configuration files after the script has completed.

Run the script as follows:

```bash
python3 wis2box-create-config.py
```

We recommend you use the directory "wis2box-data" in your home-directory to store your configuration and data. 

Note that you need to define the full path to this directory.

For example if your username is "mlimper", the full path to the directory is "/home/mlimper/wis2box-data".

```bash
mlimper@student-vm-mlimper:~/wis2box-1.0b5$ python3 wis2box-create-config.py
Please enter the directory on the host where wis2box-configuration-files are to be stored:
/home/mlimper/wis2box-data
Configuration-files will be stored in the following directory:
    /home/mlimper/wis2box-data
Is this correct? (y/n/exit)
y
The directory /home/mlimper/wis2box-data has been created.
```

Next, you will be asked to enter the URL for your wis2box. This is the URL that will be used to access the wis2box web-application, API and UI.

Please use `http://<your-hostname>` as the URL. Remember that your hostname is defined by your `username.wis2.training`

```bash
Please enter the URL of the wis2box:
 For local testing the URL is http://localhost
 To enable remote access, the URL should point to the public IP address or domain name of the server hosting the wis2box.
http://mlimper.wis2.training
The URL of the wis2box will be set to:
  http://mlimper.wis2.training
Is this correct? (y/n/exit)
y
```

We recommend that you use the option of random password generation when prompted for WIS2BOX_STORAGE_PASSWORD and WIS2BOX_BROKER_PASSWORD.

Next you will be asked for a 3-letter iso-code for your country and centre-id for your wis2box. The centre-id can be a string of your choosing for the purpose of this training.

```bash
Please enter your 3-letter ISO country code:
nld
Please enter the centre-id for your wis2box:
maaike_test
The country-code will be set to:
  nld
The centre-id will be set to:
  maaike_test
Is this correct? (y/n/exit)
y
```

Next you will answer a set of question to generate the discovery metadata for your wis2box. The answers do not need to be correct for the purpose of this training.

```bash
********************************************************************************
Creating initial configuration for surface and upper-air data.
********************************************************************************
Please enter the email address of the wis2box administrator:
mlimper@wmo.int
The email address of the wis2box administrator will be set to:
    mlimper@wmo.int
Is this correct? (y/n/exit)
n
Please enter the email address of the wis2box administrator:
me@gmail.com
The email address of the wis2box administrator will be set to:
    me@gmail.com
Is this correct? (y/n/exit)
y
Please enter the name of your organization:
Maaike-TEST
Your organization name will be set to:
    Maaike-TEST
Is this correct? (y/n/exit)
y
Getting bounding box for "nld".
bounding box: -68.6255319,11.825,7.2274985,53.744395.
Do you want to use this bounding box? (y/n/exit)
y
Created new metadata file: /home/mlimper/wis2box-data/metadata/discovery/metadata-synop.yml
Created new metadata file: /home/mlimper/wis2box-data/metadata/discovery/metadata-temp.yml
```

## wis2box start and status

Ensure you are in the directory containing the wis2box software stack:

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

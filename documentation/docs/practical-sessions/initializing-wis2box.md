---
title: Initializing wis2box
---

#  Initializing wis2box

!!! abstract "Learning outcomes"

    By the end of this session you will be able to:

    * Run the `wis2box-create-config.py` script to create the initial configuration
    * Start wis2box and check the status of its components
    * Access the **wis2box-webapp**, API, MinIO UI and Grafana dashboard in a browser
    * Connect to the local **wis2box-broker** using MQTT Explorer

!!! note

    The current training materials are using wis2box-1.0b5. 
    
    See [accessing-your-student-vm](accessing-your-student-vm.md) for instructions on how to download and install the wis2box software stack if you are running this training outside of a local training session.

## Preparation

Login to your designated VM with your username and password and ensure you are in the `wis2box-1.0b5` directory:

```bash
cd ~/wis2box-1.0b5
```

## `wis2box-create-config.py`

The `wis2box-create-config.py` script can be used to create the initial configuration of your wis2box. 

It will ask you a set of question to help setup your configuration.

You will be able to review and update the configuration files after the script has completed.

Run the script as follows:

```bash
python3 wis2box-create-config.py
```

We recommend you use the directory `wis2box-data` in your home directory to store your configuration and data. 
Note that you need to define the full path to this directory.

For example if your username is `mlimper`, the full path to the directory is `/home/mlimper/wis2box-data`:

```{.copy}
mlimper@student-vm-mlimper:~/wis2box-1.0b5$ python3 wis2box-create-config.py
Please enter the directory on the host where wis2box-configuration-files are to be stored:
/home/mlimper/wis2box-data
Configuration-files will be stored in the following directory:
    /home/mlimper/wis2box-data
Is this correct? (y/n/exit)
y
The directory /home/mlimper/wis2box-data has been created.
```

Next, you will be asked to enter the URL for your wis2box. This is the URL that will be used to access the wis2box web application, API and UI.

Please use `http://<your-hostname>` as the URL. Remember that your hostname is defined by your `username.wis2.training`

```{.copy}
Please enter the URL of the wis2box:
 For local testing the URL is http://localhost
 To enable remote access, the URL should point to the public IP address or domain name of the server hosting the wis2box.
http://mlimper.wis2.training
The URL of the wis2box will be set to:
  http://mlimper.wis2.training
Is this correct? (y/n/exit)
```

We recommend that you use the option of random password generation when prompted for `WIS2BOX_STORAGE_PASSWORD` and `WIS2BOX_BROKER_PASSWORD`.

Next you will be asked for the 3-letter ISO code for your country and centre-id for your wis2box. The centre-id can be a string of your choosing for the purpose of this training.

```{.copy}
Please enter your 3-letter ISO country code:
nld
Please enter the centre-id for your wis2box:
maaike_test
The country-code will be set to:
  nld
The centre-id will be set to:
  maaike_test
Is this correct? (y/n/exit)
```

Next you will answer a set of question to generate discovery metadata templates for your wis2box. The answers do not need to be correct for the purpose of this training.

```{.copy}
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

We will review the discovery metadata templates in a later session.

Once the scripts is completed check the contents of the `wis2box.env` file in your current directory:

```bash
cat ~/wis2box-1.0b5/wis2box.env
```

Or check the content of the file via WinSCP.

!!! note

    The `wis2box.env` file contains environment variables defining the configuration of your wis2box. For more information consult the [wis2box-documentation](https://docs.wis2box.wis.wmo.int/en/latest/reference/configuration.html)

You can also check the contents of the `data-mappings.yml` file in your wis2box data directory:

```bash
cat ~/wis2box-data/data-mappings.yml
```

Or check the content of the file via WinSCP.

!!! note

    The `data-mappings.yml` define the plugins used to transform your data. For more information see [data pipeline plugins in the wis2box-documentation](https://docs.wis2box.wis.wmo.int/en/latest/reference/running/data-pipeline-plugins.html)


## wis2box start and status

Ensure you are in the directory containing the wis2box software stack:

```{.copy}
cd ~/wis2box-1.0b5
```

Start wis2box with the following command:

```{.copy}
python3 wis2box-ctl.py start
```

Inspect the status with the following command:

```{.copy}
python3 wis2box-ctl.py status
```

Repeat this command until all services are up and running.


!!! note "wis2box and Docker"
    wis2box runs as a set of Docker containers managed by docker-compose.
    
    The services are defined in the various `docker-compose*.yml` which can be found in the `~/wis2box-1.0b5/` directory.
    
    The Python script `wis2box-ctl.py` is used to run the underlying Docker Compose commands that control the wis2box services.

## wis2box API

Open a new tab and navigate to the page `http://<your-host>/oapi`.

<img alt="wis2box-api.png" src="../../assets/img/wis2box-api.png" width="600">

This is the wis2box API (running via the **wis2box-api** container).

!!! question
     
     What collections are currently available?

??? success "Click to reveal answer"
    
    To view collections currently available through the API, click `View the collections in this service`:

    <img alt="wis2box-api-collections.png" src="../../assets/img/wis2box-api-collections.png" width="600">

    The following collections are currently available:

    - Discovery metadata
    - Station metadata
    - Data notifications

!!! question

    How many data notifications have been published?

??? success "Click to reveal answer"

    Click on "Data notifications", then click on `Browse through the items of "Data Notifications"`. 
    
    You will note that the page says "No items" as no Data notifications have been published yet.

## wis2box webapp

Open a web browser and visit the page `http://<your-host>/wis2box-webapp`:

<img alt="wis2box-webapp.png" src="../../assets/img/wis2box-webapp.png" width="600">

This is the (new) wis2box web application to enable you to interact with your wis2box:

- ingest ASCII and CSV data
- update/review your station metadata
- monitor notifications published on your wis2box-broker

We will use this web application in a later session.

## wis2box UI

Open a web browser and visit the page `http://<your-host>`:

<img alt="wis2box-ui.png" src="../../assets/img/wis2box-ui-empty.png" width="600">

The wis2box UI will display your configured datasets. For the surface-weather-observations/synop dataset, you can `explore` the data that has been ingested.

The UI is currently empty, as datasets have not yet been configured.

## wis2box-broker

Open the MQTT Explorer on your computer and prepare a new connection to connect to your broker (running via the **wis2box-broker** container).

Click `+` to add a new connection:

<img alt="mqtt-explorer-new-connection.png" src="../../assets/img/mqtt-explorer-new-connection.png" width="300">

Click on the 'ADVANCED' button and add the following topics to subscribe to:

- `$SYS/#`
- `origin/a/wis2/#`
- `wis2box/#`

<img alt="mqtt-explorer-topics.png" src="../../assets/img/mqtt-explorer-topics.png" width="550">

!!! note

    The messages published under the `$SYS` topic are system messages published by the mosquitto service itself.

    The messages published under topics starting with `origin/a/wis2/#` are the WIS2 data notifications published by the **wis2box-broker**.

    The messages published under topics starting with `wis2box` are internal messages between the various components of the wis2box software stack.

Use the following connection details, making sure to replace the value of `<your-host>` with your hostname and `<WIS2BOX_BROKER_PASSWORD>` with the value from your `wis2box.env` file:

- **Protocol: mqtt://**
- **Host: `<your-host>`**
- **Port: 1883**
- **Username: wis2box**
- **Password: `<WIS2BOX_BROKER_PASSWORD>`**

!!! note 

    Check you wis2box.env for the value of your WIS2BOX_BROKER_PASSWORD.

Make sure to click "SAVE" to store your connection details.

Then click "CONNECT" to connect to your **wis2box-broker**.

<img alt="mqtt-explorer-wis2box-broker.png" src="../../assets/img/mqtt-explorer-wis2box-broker.png" width="600">

Once you are connected, you should see statistics being published by your broker on the `$SYS/#`.

Later during the training you will use the MQTT connection you saved to view notifications published by your wis2box-broker.

## MinIO UI

Open a web browser and visit the page `http://<your-host>:9001`:

<img alt="minio-ui.png" src="../../assets/img/minio-ui.png" width="600">

This is the MinIO UI (running via the **wis2box-storage** container).

The username and password are defined in the `wis2box.env` file in your wis2box data directory by the environment variables `WIS2BOX_STORAGE_USERNAME` and `WIS2BOX_STORAGE_PASSWORD`.

Use the command below to check the values of these environment variables from the command line in your SSH session:

```{.copy}
cat ~/wis2box-1.0b5/wis2box.env
```

Or check the content of the file via WinSCP.

Try to login to your MinIO UI. You will see that there 3 buckets already defined:

- `wis2box-incoming`: used to receive incoming data
- `wis2box-public`: used to store data that is made available in the WIS2 notifications, the content of this bucket is proxied as `/data` on your `WIS2BOX_URL` via the nginx container
- `wis2box-archive`: used to archive data from `wis2box-incoming` on a daily basis

<img alt="minio-ui-buckets.png" src="../../assets/img/wis2box-minio-buckets.png" width="600">

!!! note

    The **wis2box-storage** container will send a notification on the **wis2box-broker** when data is received. The **wis2box-management** container is subscribed to all messages on `wis2box/#` and will receive these notifications, triggering the data pipelines defined in your `data-mappings.yml`.

## Grafana UI

Open a web browser and visit the page `http://<your-host>:3000`:

<img alt="wis2box-grafana-ui.png" src="../../assets/img/wis2box-grafana-ui.png" width="600">

This is the Grafana UI, where you can view the wis2box workflow monitoring dashboard. You can also access the logs of the various containers in the wis2box software stack via the 'Explore' option in the menu.

## Conclusion

!!! success "Congratulations!"
    In this practical session, you learned how to:

    - Run the `wis2box-create-config.py` script to create the initial configuration
    - Start wis2box and check the status of its components
    - Access the **wis2box-webapp**, API, MinIO UI and Grafana dashboard in a browser
    - Connect to the **wis2box-broker** using MQTT Explorer

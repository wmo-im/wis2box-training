---
title: Installing wis2box with test data
---

#  Installing wis2box with test data

## Introduction

In this session you will learn how to install wis2box on your student VM and get familiar with the runtime configuration steps and web interfaces. You will also use predefined configuration and sample data to allow for review of the services provided by your wis2box.

## Preparation

Login to your designated VM with your username and password.

Ensure you have [downloaded the exercise materials](../practical-sessions/accessing-your-student-vm.md#download-the-exercise-materials) in the previous session.

Go into the directory containing the wis2box training setup:

```bash
cd ~/exercise-materials/wis2box-setup
```

!!! note
    You can always find the latest 'wis2box-setup' archive at [https://github.com/wmo-im/wis2box/releases](https://github.com/wmo-im/wis2box/releases)

    The contents of the 'wis2box-setup' directory are similar to that you will find when downloading and extracting `wis2box-setup-*.zip` from the official wis2box download page.

## wis2box setup using test data

Before starting the wis2box, you should review the content of the test data you will use and set the hostname of your wis2box.

### dev.env

The wis2box setup reads environment variables from `dev.env`. A basic example is provided by `test.env` in your current directory.

Copy `test.env` to `dev.env`:

```bash
cp test.env dev.env
```

Review the contents of `dev.env`:

```bash
cat dev.env
```

!!! note
    `dev.env` is a required file always used by wis2box

!!! note
    `WIS2BOX_HOST_DATADIR` is set to `${PWD}/test-data`.  This directory will be mapped as `/data/wis2box` inside the **wis2box-management** container.

!!! note
    ``LOGGING_LEVEL`` is set to ``INFO``.  The ``LOGGING_LEVEL`` for a wisbox default installation is ``WARNING``.

Before starting wis2box, edit the `dev.env` file using a command-line editor (vi/vim/emacs/nano), and add the `WIS2BOX_URL` and `WISB2BOX_API_URL` variables as follows:

```bash
# Required
# Host machine data directory path
WIS2BOX_HOST_DATADIR=${PWD}/test-data

WIS2BOX_DATADIR_DATA_MAPPINGS=/data/wis2box/data-mappings.yml

# Optional
# Environment variable overrides
WIS2BOX_LOGGING_LOGLEVEL=INFO

MYHOSTNAME=trainer-limper.wis2.training
WIS2BOX_URL=http://${MYHOSTNAME}
WIS2BOX_API_URL=http://${MYHOSTNAME}/oapi
```

And ensure you specify **your** VM host for `MYHOSTNAME`.

### data-mappings.yml

The wis2box setup determines the topic hierarchy and the plugins for the data it ingests from the `data-mappings.yml` provided in the `WIS2BOX_HOST_DATADIR`. 

The test-data directory provides the configuration you will use in this exercise.

Inspect the content of `test-data/data-mappings.yml`:

```bash
cat test-data/data-mappings.yml
```

!!! question
    What topics are configured in this file?

!!! note
    The `wis2box.data.csv2bufr.ObservationDataCSV2BUFR` converts csv-data into BUFR format. The attribute `notify: true` indicates that the broker should publish a WIS2 notification for each BUFR file that was produced

    The plugin for `wis2box.data.bufr2geojson.ObservationDataBUFR2GeoJSON` converts bufr4 to GeoJSON which is stored in the **wis2box-api** backend (Elasticsearch).

### metadata/station/station_list.csv

The wis2box setup reads metadata about the stations for which it will process data from the file `metadata/station/station_list.csv` provided in the `WIS2BOX_HOST_DATADIR`. 

Inspect the content of `test-data/metadata/station/station_list.csv`:  

```bash
cat test-data/metadata/station/station_list.csv
```

!!! question
    How many stations are defined in this file?

Inspect the content in the `test-data/observations` directory:

```bash
ls test-data/observations/*/*
```

!!! question
    Check the content of the individual files. What type of observations are reported in this data?

## Start wis2box

Start wis2box with the following command:

```bash
python3 wis2box-ctl.py start
```

Wait until the command has completed.

Inspect the status with the following command:

```bash
python3 wis2box-ctl.py status
```

Repeat this command until you are sure all services are up and running.

Open a web browser and visit the page `http://<your-host>`.

<img alt="wis2box-ui-empty.png" src="../../assets/img/wis2box-ui-empty.png" width="600">

This is the default wis2box web application (running via the **wis2box-ui** container).  We see that the homepage is empty, given no datasets are setup yet.

Open a new tab and navigate to the page `http://<your-host>/oapi`.

<img alt="wis2box-api.png" src="../../assets/img/wis2box-api.png" width="600">

This is the wis2box API (running via the **wis2box-api** container).

To view collections currently published to the API, navigate to the page `http://<your-host>/oapi/collections`.

!!! question
     What collections are currently available?
!!! question
    How many data notifications have been published?
!!! question
    Which stations are configured?

## Connect MQTT Explorer to your wis2box-broker

Go to MQTT Explorer on your computer and prepare a new connection to connect to your broker (running via the **wis2box-broker** container).

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

Keep MQTT Explorer running and continue with the runtime configuration steps.

## Runtime configuration steps for wis2box

Login to the **wis2box-management** container using the following command:

```bash
python3 wis2box-ctl.py login
```

!!! note
    This command is equivalent to `docker exec -it wis2box-management /bin/bash`, meaning that you have entered an interactive shell inside the **wis2box-management** container.

Run the following command to see the environment variables used by your wis2box:

```bash
wis2box environment show
```

Note the variables you have set for `WIS2BOX_HOST_DATADIR`, `WIS2BOX_URL` and `WIS2BOX_API_URL`.

Run the following command to see the content of `/data/wis2box` directory inside the **wis2box-management** container:

```bash
ls /data/wis2box/
```

!!! note
    The content of `/data/wis2box` matches that of the directory defined by `$WIS2BOX_HOST_DATADIR` on your VM.

Run the following command to add the test dataset:

```bash
wis2box data add-collection /data/wis2box/mwi-surface-weather-observations.yml
```

- Go back to your web browser and refresh the `http://<your-host>/oapi/collections` page.  Inspect the new collection.

Run the following command to publish discovery metadata for the test dataset:

```bash
wis2box metadata discovery publish /data/wis2box/mwi-surface-weather-observations.yml
```

Go back to your web browser and refresh the `http://<your-host>/oapi/collections` page.

!!! question
    What new collection is now available?

Switch back to MQTT Explorer and find the discovery metadata message that was published by your broker.

!!! question
    What is the topic used to publish the discovery metadata message?

## Ingesting data

Make you are logged in to the **wis2box-management** container (`python3 wis2box-ctl.py login`) and execute the following command:

```bash
wis2box data ingest -th mwi.mwi_met_centre.data.core.weather.surface-based-observations.synop -p /data/wis2box/observations/malawi/
```

Ensure that the command completes successfully without errors. You should see the following:

```console
Setting up logger with level: INFO
Processing /data/wis2box/observations/malawi/WIGOS_0-454-2-AWSTOLEZA_2021-11-18T0955.csv
Processing /data/wis2box/observations/malawi/WIGOS_0-454-2-AWSBALAKA_2021-11-18T0955.csv
Processing /data/wis2box/observations/malawi/WIGOS_0-454-2-AWSNKHOMA_2021-11-18T0955.csv
Processing /data/wis2box/observations/malawi/WIGOS_0-454-2-AWSNAMITAMBO_2021-11-18T0955.csv
Processing /data/wis2box/observations/malawi/WIGOS_0-454-2-AWSMULANJE_2023-03-14T0655.csv
Processing /data/wis2box/observations/malawi/WIGOS_0-454-2-AWSLOBI_2021-11-11T1255.csv
Processing /data/wis2box/observations/malawi/WIGOS_0-454-2-AWSNAMITAMBO_2021-07-07.csv
Processing /data/wis2box/observations/malawi/WIGOS_0-454-2-AWSMALOMO_2021-11-18T0955.csv
Processing /data/wis2box/observations/malawi/WIGOS_0-454-2-AWSKAYEREKERA_2021-11-18T0955.csv
Done

```

Browse through the new items available in the collections on your API on `http://<your-host>/oapi/collections`.

!!! question
    What changes do you observe?

Check your wis2box workflow monitoring on `http://<your-host>:3000` (powered by the **grafana** container). You should see the following:

<img alt="grafana-wis2box-with-test-data.png" src="../../assets/img/grafana-wis2box-with-test-data.png" width="750">

!!! question
    Try to understand the information shown on your monitoring dashboard. How many WIS2 notifications were published on your broker? Can you determine the source of reported ERRORs?

View the messages that have been published on your local broker in MQTT Explorer.

!!! question
    What is the topic used to publish messages advertising new data? What is the URL to download the data?

Click the the "EXPLORE" option on `http://<your-host>`.

!!! question
    What changes do you observe?

## Conclusion

!!! success "Congratulations!"
    In this practical session, you learned how to:

    - install wis2box on your personal VM
    - setup wis2box with the pre-defined configuration
    - start wis2box and check the status of its components
    - run the various wis2box runtime configuration steps
    - access the wis2box web application, API, and Grafana dashboard

!!! note "In case you finish the exercise early"
    For extra credit: try to address the ERRORs until you can successfully publish the data for all the observations in `test-data/observations/malawi/`.

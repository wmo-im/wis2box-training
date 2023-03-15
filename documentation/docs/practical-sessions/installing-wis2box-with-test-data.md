---
title: Installing wis2box with test data
---

#  Installing wis2box with test data

## Introduction

In this session you will learn how to install wis2box on your student VM and get familiar with the runtime configuration steps and web interfaces. You will also use predefined configuration and sample data to allow for review of the services provided by your wis2box.

## Access your wis2box setup

Login to your designated VM with your username and password.

Your home directory should already contain the exercise materials you downloaded earlier as part of the [Accessing your student VM](../practical-sessions/accessing-your-student-vm.md) session.

Go into the directory containing the wis2box training setup:

```bash
cd ~/exercise-materials/wis2box-setup
```

!!! note
    You can always find the latest 'wis2box-setup' archive at [https://github.com/wmo-im/wis2box/releases](https://github.com/wmo-im/wis2box/releases)

    The contents of the 'wis2box-setup' directory are similar to that you will find when downloading and extracting `wis2box-setup-*.zip` from the official wis2box download page.

## Review and setup environment variables in `dev.env`

Copy `test.env` to `dev.env`:

```bash
cp test.env dev.env
```

Review the contents of `dev.env`.

```bash
cat dev.env
```

!!! note
    `dev.env` is a required file always used by wis2box

!!! note
    `WIS2BOX_HOST_DATADIR` is set to `${PWD}/test-data`.  This directory will be mapped as `/data/wis2box` inside the **wis2box-management** container.

!!! note
    ``LOGGING_LEVEL`` is set to ``INFO``.  The ``LOGGING_LEVEL`` for a wisbox default installation is ``WARNING``.

!!! question
    Inspect the content of `test-data/data-mappings.yml`, what topics are configured in this file?

!!! question
    Inspect the content of `test-data/metadata/station/station_list.csv`.  How many stations are defined in this file?

!!! question
    Inspect the content in the `test-data/observations` directory.  What is the data format used?  What type of observations are reported?

Before starting wis2box, add your student VM host to the VM by editing the `dev.env` file using a command-line editor (vi/vim/emacs/nano):

And ensure you dev.env now has the additional environment-variables specifying **your** VM host:

```
WIS2BOX_URL=http://<your-host>
WIS2BOX_API_URL=http://<your-host>/oapi
```

## Start wis2box

start wis2box with the following command:

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

This is the default wis2box web application (running via the **wis2box-ui** container).  We see that the homepage is empty, given no datasets are setup yet.

On your web browser, open a new tab and navigate to the page `http://<your-host>/oapi`.

This is the wis2box API (running via the **wis2box-api** container).

To view collections currently published to the API, navigate to the page `http://<your-host>/oapi/collections`.

!!! question
     What collection is currently available?
!!! question
    How many data notifications have been published?

Make sure you can connect to your broker (running via the **wis2box-broker** container) using MQTT Explorer with the following connection details:

- **Protocol: mqtt://**
- **Host: <your-host>**
- **Port: 1883**
- **Username: wis2box**
- **Password: wis2box**
- under 'ADVANCED', subscribe to the topics `$SYS` and `origin/#`

You should see statistics being published by your broker on the `$SYS` topic. Keep MQTT Explorer running and continue with the runtime configuration steps.

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
    What is the topic is used to publish the discovery metadata message?

Run the following command to publish the station metadata in `test-data/metadata/station/station_list.csv`:

```bash
wis2box metadata station publish-collection
```

Go back to your web browser and refresh the `http://<your-host>/oapi/collections` page. Inspect the collection called "Stations" and confirm that all stations from `test-data/station/station_list.csv` are now visible.

## Ingesting data

Make you are logged in to the **wis2box-management** container (`python3 wis2box-ctl.py login`) and execute the following command:

```bash
wis2box data ingest -th mwi.mwi_met_centre.data.core.weather.surface-based-observations.synop -p /data/wis2box/observations/malawi/
```

Ensure that the command completes successfully without errors.

Review the collections on your API `http://<your-host>/oapi/collections` page.

!!! question
    What changes do you observe?

Click the the "EXPLORE" option on `http://<your-host>`.

!!! question
    What changes do you observe?

Check your wis2box workflow monitoring on `http://<your-host>:3000` (powered by the **grafana** container).

!!! question
    Can you identify any errors?

View the messages that have been published on your local broker in MQTT Explorer.

!!! question
    What is the topic used to publish messages advertising new data? What is the URL to download the data?

## Conclusion

!!! success "Congratulations!"
    In this practical session, you learned how to:

    - install wis2box on your personal VM
    - setup wis2box with the pre-defined configuration
    - start wis2box and check the status of its components
    - run the various wis2box runtime configuration steps
    - access the wis2box web application, API, and Grafana dashboard

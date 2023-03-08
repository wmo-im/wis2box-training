---
title: "Installing WIS2-in-a-box (with test-data)"
...

# Installing WIS2-in-a-box (with test-data)

## Introduction

In this session you will learn how to install the WIS2-in-a-box on your student-VM and get familiar with the run-time configuration steps and the web-accessible interfaces. You will use predefined configuration and data-samples for test-data to allow you to review the services provided by your WIS2-in-a-box.

## Access wis2box-setup

Login to your designated VM with your username and password.

Your home-directory should already contain the exercise-materials you downloaded in the session [access-your-student-vm](../practical-sessions/access-your-student-vm.md)

Go into the directory containing the wis2box-setup prepared for this training:

```bash
cd ~/exercise-materials/wis2box-setup
```

!!! note
    You can find the latest 'wis2box-setup'-archive here:
    [wis2box-releases](https://github.com/wmo-im/wis2box/releases).
    The contents of the directory 'wis2box-setup' are similar to that you will find when downloading and extracting 'wis2box-setup-*.zip' from the wis2box-releases-page.

## Review/setup environment variables in dev.env

Copy test.env to dev.env:

```
cp test.env dev.env
```

Review the contents of dev.env. 

```
cat dev.env
```

!!! note
    Note that the WIS2BOX_HOST_DATADIR is set to '${PWD}/test-data'. This directory will be mapped as /data/wis2box inside the wis2box-management container.

!!! note
    Note that the LOGGING_LEVEL is set to INFO. The default LOGGING_LEVEL is WARNING.

!!! question
    Inspect the content of test-data/data-mappings.yml, what topics are configured in this file ?

!!! question
    Inspect the content of test-data/metadata/station/station_list.csv. How many stations are defined in this file?

!!! question
    Inspect the content in the 'test-data/observations'-directory. What is the data-format used? What type of observations are reported in this file?

Before starting the wis2box add your student-VM host to the VM by editing the file using a command-line editor (vi/vim/nano)

And ensure you dev.env now has the additional environment-variables specifying **your** VM-host:

```
WIS2BOX_URL=http://<your-host>
WIS2BOX_API_URL=http://<your-host>/oapi
```

## Start the WIS2-in-a-box services

start the wis2box with the following command:

```
python3 wis2box-ctl.py start
```

Wait until the command has completed.

Inspect the status with the following command:

```
python3 wis2box-ctl.py status
```

Repeat the status-command until you are sure all services are Up.

Open a browser and visit the page `http://<your-host>`. 

This is the wis2box-ui, is is empty as you have not yet setup any datasets.

In an new tab, open the page `http://<your-host>/oapi/collections`. 

These are the collections currently published the wis2box-api. 

!!! question
     What collection is currently available?
!!! question
    How many data-notifications have been published ?

Make sure you can connect to your wis2box-broker using MQTT-explorer. 
- protocol=mqtt:// host=`<your-host>` port=1883
- username=wis2box password=wis2box
- under 'advanced' subscribe to the topics '$SYS' and 'origin/#'

You should see statistics being published by your broker on the $SYS-topic. Keep MQTT-explorer running and proceed with the runtime configuration steps.

## Runtime configuration steps for the wis2box

Login to the wis2box-management container using the following command:

```
python3 wis2box-ctl.py login
```

Note this command is equivalent to `docker exec -it wis2box-management /bin/bash`, meaning that you have entered an interactive shell inside the `wis2box-management` container

Run the following command to see the environment variables used by your wis2box

```
wis2box environment show
```

Note the variables you have set for WIS2BOX_HOST_DATADIR, WIS2BOX_URL and WIS2BOX_API_URL

Run the following command to see the content of /data/wis2box inside the wis2box-management-container:

```
ls /data/wis2box/
```

Note that the content of /data/wis2box matches that of the directory defined by $WIS2BOX_HOST_DATADIR on your VM.

Run the following command to add the test dataset:

```
wis2box data add-collection /data/wis2box/mwi-surface-weather-observations.yml
```

- Go back to your browser and refresh `http://<your-host>/oapi/collections` collections. Inspect the new collection.

Run the following command to publish discovery metadata for the test dataset:

```
wis2box metadata discovery publish /data/wis2box/mwi-surface-weather-observations.yml
```

!!! question
    Go back to your browser and refresh `http://<your-host>/oapi/collections`. What new collection is now available ?

!!! question
    Check MQTT-explorer: find the message metadata-message that was published by your wis2box-broker. What is the topic is used to publish the metadata-message ?

Run the following command to publish the data in test-data/metadata/station/station_list.csv :

```
wis2box metadata station publish-collection
```

- Go back to your browser and refresh `http://<your-host>/oapi/collections`. Inspect the 'stations'-collection and confirm that all stations from test-data/station/station_list.csv are now visible.

## Ingesting data

Make you are logged in to the wis2box-management-container (python3 wis2box-ctl.py login) and execute the following command:

```
wis2box data ingest -th mwi.mwi_met_centre.data.core.weather.surface-based-observations.synop -p /data/wis2box/observations/malawi/
```

Check the command completes successfully without errors before proceeding to answer the following questions.

!!! question
    Review the collections on your API `http://<your-host>/oapi/collections`. What changes can you observe ?

!!! question
    Check out the 'explore'-option on `http://<your-host>`. What changes can you observe ?

!!! question
    Check your the wis2box workflow monitoring on `http://<your-host>:3000` (Grafana). Can you identify any errors ?

View the messages that have been published on your local broker in MQTT-explorer.

!!! question
    What is the topic used to publish messages advertizing the new data? What is the url to download the data ?

# Learning outcomes

Learning outcomes for this session:

- Installed wis2box on your personal VM
- Setup the wis2box with pre-defined configuration
- Know how to start the wis2box and check the status of its components
- Be familiar with the wis2box runtime configuration steps
- Know how to access the wis2box-UI, wis2box-API and Grafana dashboard

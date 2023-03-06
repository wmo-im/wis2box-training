---
title: "Installing WIS2box with test-data"
...

# WIS2box with test-data

# Total Learning outcomes

Learning outcomes for this session:
- Installed wis2box on your personal VM
- Setup the wis2box with pre-defined configuration
- Know how to start the wis2box and check the status of its components
- Be familiar with the wis2box runtime configuration steps
- Know how to access the wis2box-UI, wis2box-API and Grafana dashboard

# Essentials

Here are some essential commands you wil use in these exercises :

## wis2box-ctl.py
`wis2box-ctl.py` is a python script that defines the docker-compose commands to control the stack of wis2box-services:

```console
csv2bufr data transform --bufr-template <my_template.json> --output-dir <./my_folder> <my_data.csv>
```

## inside the wis2box-management container

Inside the wis2box-management container, accessible using ``python3 wis2box-ctl.py login`, the following commands are available:

### wis2box data

```console
Usage: wis2box data [OPTIONS] COMMAND [ARGS]...

  Data workflow

Options:
  --help  Show this message and exit.

Commands:
  add-collection        Add collection index to API backend
  add-collection-items  Add collection items to API backend
  archive               Move data from incoming storage to archive storage
  clean                 Clean data directories and API indexes
  delete-collection     Delete collection from api backend
  ingest                Ingest data file or directory
```

### wis2box metadata

Usage: wis2box metadata [OPTIONS] COMMAND [ARGS]...

  Metadata management

Options:
  --help  Show this message and exit.

Commands:
  discovery  Discovery metadata management
  station    Station metadata management


## Prepare training materials

Login to your designated VM with your username and password.

Download the archive and unzip it:

```
wget http://www.wis2.training/exercise-materials/wis2box-training-release.zip
unzip wis2box-training-release.zip
```

Go into the new directory:

```
cd wis2box-training-release
```

## Ex. 1 review the test-data-setup

Copy test.env to dev.env:

```
cp test.env dev.env
```

Review the contents of dev.env. 

```
cat dev.env
```

Note that the WIS2BOX_HOST_DATADIR is set to '${PWD}/test-data'. This directory will be mapped as /data/wis2box inside the wis2box-management container.
Note that the LOGGING_LEVEL is set to INFO. The default LOGGING_LEVEL is WARNING.

- Inspect the content of test-data/data-mappings.yml, what topics are configured in this file ?
- Inspect the content of test-data/metadata/station/station_list.csv. How many stations are defined in this file?
- Inspect the content in the 'test-data/observations'-directory. What is the data-format used? What type of observations are reported in this file?

Before starting the wis2box add your student-VM host to the VM by editing the file using a command-line editor (vi/vim/nano)

And ensure you dev.env now has the additional environment-variables specifying **your** VM-host:

```
WIS2BOX_URL=http://<your-host>
WIS2BOX_API_URL=http://<your-host>/oapi
```

## Ex. 2 start the wis2box

1. start the wis2box with the following command:

```
python3 wis2box-ctl.py start
```

Wait until the command has completed.

2. Inspect the status with the following command:

```
python3 wis2box-ctl.py status
```

Repeat the status-command until you are sure all services are Up.

3. Open a browser and visit the page `http://<your-host>`. 

This is the wis2box-ui, is is empty as you have not yet setup any datasets.

4. In an new tab, open the page `http://<your-host>/oapi/collections`. 

These are the collections currently published the wis2box-api. 

- What collection is currently available?
- How many data-notifications have been published ?

5. Make sure you can connect to your wis2box-broker using MQTT-explorer. 
- protocol=mqtt:// host=`<your-host>` port=1883
- username=wis2box password=wis2box
- under 'advanced' subscribe to the topics '$SYS' and 'origin/#'

You should see statistics being published by your broker on the $SYS-topic. Keep MQTT-explorer running and proceed with the runtime configuration steps.

## Ex. 3 Runtime configuration steps for the wis2box

1. Login to the wis2box-management container using the following command:

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

2. Run the following command to add the test dataset:

```
wis2box data add-collection /data/wis2box/mwi-surface-weather-observations.yml
```

- Go back to your browser and refresh `http://<your-host>/oapi/collections` collections. Inspect the new collection.

3. Run the following command to publish discovery metadata for the test dataset

```
wis2box metadata discovery publish /data/wis2box/mwi-surface-weather-observations.yml
```

- Go back to your browser and refresh `http://<your-host>/oapi/collections`. Inspect the new collection.
- Check MQTT-explorer: find the message metadata-message that was published by your wis2box-broker

4. Run the following command to publish the data in test-data/metadata/station/station_list.csv :

```
wis2box metadata station publish-collection
```

- Go back to your browser and refresh `http://<your-host>/oapi/collections`. Inspect the 'stations'-collection and confirm that all stations from test-data/station/station_list.csv are now visible.

## Ex. 4 Ingesting data

Make you are logged in to the wis2box-management-container (python3 wis2box-ctl.py login) and execute the following command:

```
wis2box data ingest -th mwi.mwi_met_centre.data.core.weather.surface-based-observations.synop -p /data/wis2box/observations/malawi/
```

Stuff should happen, if not, check for errors !

1. Review the collections on your API `http://<your-host>/oapi/collections`. What changes can you observe ?

2. Check out the 'explore'-option on `http://<your-host>`. What changes can you observe ?

3. Check your the wis2box workflow monitoring on `http://<your-host>:3000` (Grafana). What changes can you observe ?

4. View the messages that have been published on your local broker in MQTT-explorer.




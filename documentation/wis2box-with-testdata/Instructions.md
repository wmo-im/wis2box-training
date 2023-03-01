# Run wis2box using test-data

Login to your designated VM with your username and password.

Download the archive and unzip it:

```
wget http://10.0.2.222/exercise-materials/wis2box-training-release.zip
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
WIS2BOX_URL=http://<your-host-ip>
WIS2BOX_API_URL=http://<your-host-ip>/oapi
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
- under advanced ensure you subscribe to the topics '#' and 'origin/#'

You should see statistics being published by your broker on the $SYS-topic. Keep MQTT-explorer running and proceed with the runtime configuration steps.

## Ex. 3 Runtime configuration steps for the wis2box

1. Login to the wis2box-management container using the following command:

```
python3 wis2box-ctl.py login
```

2. Run the following command to see the content of /data/wis2box inside the wis2box-management-container:

```
ls /data/wis2box/
```
 (you should see the same files as in test-data/ on the VM-host)

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

## Ex. 5 connecting to your broker

Re-ingest and view the messages being published on mqtt-explorer by connecting your local broker.




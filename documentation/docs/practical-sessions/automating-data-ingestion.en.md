---
title: Automating data ingestion
---

# Automating data ingestion

!!! abstract "Learning outcomes"

    By the end of this practical session, you will be able to:
    
    - understand how the data-plugins of your dataset determine the data-ingest workflow
    - ingest data into wis2box using a script using the MinIO Python client
    - ingest data into wis2box using the wis2box-ftp service

## Introduction

The **wis2box-management** container listens to events from the MinIO storage service to trigger data ingestion based on the data-plugins configured for your dataset. This allows you to upload data into the MinIO bucket and trigger the wis2box workflow to publish data on the WIS2 broker. 

In the previous sessions, we triggered the data ingest workflow by using the MinIO user interface to upload data files.
The same steps can be done programmatically by using any MinIO or S3 client software, allowing you to automate your data ingestion as part of your operational workflows. 

If you are unable to adapt your system to upload data to MinIO directly, you can also use the **wis2box-ftp** service to forward data to the MinIO storage service.

## Preparation

Login to you student VM using your SSH client (PuTTY or other).

Make sure wis2box is up and running:

```bash
cd ~/wis2box-1.0b8/
python3 wis2box-ctl.py start
python3 wis2box-ctl.py status
```

Make sure your have MQTT Explorer running and connected to your instance.
If you are still connected from the previous session, clear any previous messages you may have received from the queue.
This can be done by either by disconnecting and reconnecting or by clicking the trash can for the topic.

Make sure you have a web browser open with the Grafana dashboard for your instance by going to `http://<your-host>:3000`

<img alt="grafana-homepage" src="../../assets/img/grafana-homepage.png" width="800">

And make sure you have a second tab open with the MinIO user interface at `http://<your-host>:9001`. Remember you need to login with the `WIS2BOX_STORAGE_USER` and `WIS2BOX_STORAGE_PASSWORD` defined in your `wis2box.env` file:

<img alt="minio-second-tab" src="../../assets/img/minio-second-tab.png" width="800">






## Exercise 1: setup a python script to ingest data into MinIO

In this exercise we will use the MinIO Python client to copy data into MinIO.

MinIO provides a Python client which can be installed as follows:

```bash
pip3 install minio
```

On your student VM the 'minio' package for Python will already be installed.

Go to the directory `exercise-materials/data-ingest` and run the example script using the following command:

```bash
cd ~/exercise-materials/data-ingest
python3 copy_data_to_incoming.py
```

!!! note
    
    You will get an error as the script is not configured to access the MinIO endpoint on your wis2box yet.

The script needs to know the correct endpoint for accessing MinIO on your wis2box. If wis2box is running on your host, the MinIO endpoint is available at `http://<your-host>:9000`.

The sample script provides the basic structure for copying a file into MinIO.

!!! question "ingest data using Python"
    Use the Python example provided to create to ingest data into your wis2box.  
    
    Ensure that you:

    - define the correct MinIO endpoint for your host
    - provide the correct storage credentials for your MinIO instance

You can verify that the data was uploaded correctly by checking the MinIO user interface and seeing if the sample data is available in the correct directory in the `wis2box-incoming` bucket.

You can use the Grafana dashboard to check the status of the data ingest workflow.

Finally you can use MQTT Explorer to check if notifications were published for the data you ingested.

## Ingesting binary data

wis2box can ingest binary data in BUFR format using the `wis2box.data.bufr4.ObservationDataBUFR` plugin included in wis2box.

You can verify that the plugin is configured in your wis2box by checking the contents of `data-mappings.yml` from the SSH command line: 

```bash
cat ~/wis2box-data/data-mappings.yml
```

And you should see it contains an entry that specifies that files with the extension `.bin` should be processed by the `wis2box.data.bufr4.ObservationDataBUFR` plugin:

```{.copy}
            bin:
                - plugin: wis2box.data.bufr4.ObservationDataBUFR
                  notify: true
                  buckets:
                    - ${WIS2BOX_STORAGE_INCOMING}
                  file-pattern: '^.*\.bin$'
```

This plugin will split the BUFR file into individual BUFR messages and publish each message to the MQTT broker. If the station for the corresponding BUFR message is not defined in the wis2box station metadata, the message will not be published.

Please download the following sample data file to your local machine:

[bufr-example.bin](/sample-data/bufr-example.bin)

!!! question "Exercise 4: ingest binary data in BUFR format"

    Upload the sample data file 'bufr-example.bin' to the same path in MinIO you used in the previous exercise:

    <img alt="minio-admin-uploaded-bufr-file" src="../../assets/img/minio-admin-uploaded-bufr-file.png" width="800">

    Check the Grafana dashboard and MQTT Explorer to see if the test-data was successfully ingested and published.

    How many messages were published to the MQTT broker for this data sample?

??? success "Click to reveal answer"

    If you successfully ingested and published the last data sample, you should have received 10 new notifications on the wis2box MQTT broker. Each notification correspond to data for one station for one observation timestamp.

## Ingesting SYNOP data in ASCII format

In the previous session we used the SYNOP form in the **wis2box-webapp** to ingest SYNOP data in ASCII format. You can also ingest SYNOP data in ASCII format by uploading the data into MinIO. 

In the previous session you should have created a dataset which included the plugin 'FM-12 data converted to BUFR' for the dataset mappings:

<img alt="dataset-mappings" src="../../assets/img/dataset-mappings.png" width="800">

This plugin loads the module `wis2box.data.synop2bufr.ObservationDataSYNOP2BUFR` to ingest the data.

Download the following two sample data files to your local machine:

[synop-202307.txt](/sample-data/synop-202307.txt)

[synop-202308.txt](/sample-data/synop-202308.txt)

(click 'save as' in your browser to download the files)

Note that the 2 files contain the same content, but the filename is different. The filename is used to determine the date of the data sample.

The file pattern in `data-mappings.yml` specifies that the regular expression `^.*-(\d{4})(\d{2}).*\.txt$` that is used to extract the date from the filename. The first group in the regular expression is used to extract the year and the second group is used to extract the month.

!!! question "Exercise 5: ingest SYNOP data in ASCII format"

    Go back to the MinIO interface in your browse and navigate to the `wis2box-incoming` bucket and into the path where you uploaded the test data in the previous exercise.
    
    Upload the new files in the correct path in the `wis2box-incoming` bucket in MinIO to trigger the data ingest workflow.

    Check the Grafana dashboard and MQTT Explorer to see if the test data was successfully ingested and published.

    What is the difference in the `properties.datetime` between the two messages published to the MQTT broker?

??? success "Click to reveal answer"

    Check the properties of the last 2 notifications in MQTT Explorer and you will note that one notification has:

    ```{.copy}
    "properties": {
        "data_id": "wis2/rou/test/data/core/weather/surface-based-observations/synop/WIGOS_0-20000-0-60355_20230703T090000",
        "datetime": "2023-07-03T09:00:00Z",
        ...
    ```

    and the other notification has:

    ```{.copy}
    "properties": {
        "data_id": "wis2/rou/test/data/core/weather/surface-based-observations/synop/WIGOS_0-20000-0-60355_20230803T090000",
        "datetime": "2023-08-03T09:00:00Z",
        ...
    ```

    The filename was used to determine the year and month of the data sample.

## Exercise 2: ingesting bufr data using the MinIO Python client

This plugin will split the BUFR file into individual BUFR messages and publish each message to the MQTT broker. If the station for the corresponding BUFR message is not defined in the wis2box station metadata, the message will not be published.

Please download the following sample data file to your local machine:

[bufr-example.bin](/sample-data/bufr-example.bin)

!!! question "Exercise 4: ingest binary data in BUFR format"

    How many messages were published to the MQTT broker for this data sample?

??? success "Click to reveal answer"

    If you successfully ingested and published the last data sample, you should have received 10 new notifications on the wis2box MQTT broker. Each notification correspond to data for one station for one observation timestamp.

## Exercise 3: ingesting data using the wis2box-ftp service

You can add an additional service that adds an ftp-endpoint on your wis2box-instance. This service will forward data uploaded via ftp to the MinIO storage service, preserving the directory structure of the uploaded data.

To use the docker-compose.wis2box-ftp.yml template included in wis2box, create a new file called ftp.env using any text editor, and add the following content:

```{.copy}
MYHOSTNAME=mlimper.wis2.training

FTP_USER=wis2box
FTP_PASS=wis2box123
FTP_HOST=${MYHOSTNAME}

WIS2BOX_STORAGE_ENDPOINT=http://${MYHOSTNAME}:9000
WIS2BOX_STORAGE_USERNAME=wis2box
WIS2BOX_STORAGE_PASSWORD=MYSTORAGEPASSWORD
```

Replace `mlimper.wis2.training` with the hostname of your wis2box instance, and `MYSTORAGEPASSWORD` with the WIS2BOX_STORAGE_PASSWORD password defined in your `wis2box.env` file.

Then start the wis2box-ftp service using the following command:

```bash
docker-compose -f docker-compose.wis2box-ftp.yml up -d
```


## Conclusion

!!! success "Congratulations!"
    In this practical session, you learned how to:

    - trigger wis2box workflow using different data ingest methods
    - monitor the status of your data ingest and publishing

---
title: Automating data ingestion
---

# Automating data ingestion

!!! abstract "Learning outcomes"

    By the end of this practical session, you will be able to:
    
    - understand how the data plugins of your dataset determine the data ingest workflow
    - ingest data into wis2box using a script using the MinIO Python client
    - ingest data into wis2box using the wis2box-ftp service

## Introduction

The **wis2box-management** container listens to events from the MinIO storage service to trigger data ingestion based on the data-plugins configured for your dataset. This allows you to upload data into the MinIO bucket and trigger the wis2box workflow to publish data on the WIS2 broker. 

The data-plugins define the Python modules that are loaded by the **wis2box-management** container and determine how the data is transformed and published.

In the previous exercise you should have created a dataset using the template `surface-based-observations/synop` which included the following data-plugins:

<img alt="data-mappings" src="../../assets/img/wis2box-data-mappings.png" width="800">

When a file is uploaded to MinIO, wis2box will match the file to a dataset when the filepath contains the dataset id (`metadata_id`) and it will determine the data plugins to use based on the file extension and file pattern defined in the dataset mappings.

In the previous sessions, we triggered the data ingest workflow by using the wis2box command line functionality, which uploads data to the MinIO storage in the correct path.

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

Make sure MQTT Explorer is running and connected to your instance. If you are still connected from the previous session, clear any previous messages you may have received from the queue.
This can be done by either by disconnecting and reconnecting or by clicking the trash can icon for the given topic.

Make sure you have a web browser open with the Grafana dashboard for your instance by going to `http://<your-host>:3000`

And make sure you have a second tab open with the MinIO user interface at `http://<your-host>:9001`. Remember you need to login with the `WIS2BOX_STORAGE_USER` and `WIS2BOX_STORAGE_PASSWORD` defined in your `wis2box.env` file.

## Exercise 1: setup a Python script to ingest data into MinIO

In this exercise we will use the MinIO Python client to copy data into MinIO.

MinIO provides a Python client which can be installed as follows:

```bash
pip3 install minio
```

On your student VM the 'minio' package for Python will already be installed.

Go to the directory `exercise-materials/data-ingest-exercises`; this directory contains a sample script `copy_file_to_incoming.py` that uses the MinIO Python client to copy a file into MinIO.

Try to run the script to copy the sample data file `csv-aws-example.csv` into the `wis2box-incoming` bucket in MinIO" as follows:

```bash
cd ~/exercise-materials/data-ingest-exercises
python3 copy_file_to_incoming.py csv-aws-example.csv
```

!!! note

    You will get an error as the script is not configured to access the MinIO endpoint on your wis2box yet.

The script needs to know the correct endpoint for accessing MinIO on your wis2box. If wis2box is running on your host, the MinIO endpoint is available at `http://<your-host>:9000`. The script also needs to be updated with your storage password and the path in the MinIO bucket to store the data.

!!! question "Update the script and ingest the CSV data"
    
    Edit the script `copy_file_to_incoming.py` to address the errors, using one of the following methods:
    - From the command line: use the `nano` or `vim` text editor to edit the script
    - Using WinSCP: start a new connection using File Protocol `SCP` and the same credentials as your SSH client. Navigate to the directory `exercise-materials/data-ingest-exercises` and edit `copy_file_to_incoming.py` using the built-in text editor
    
    Ensure that you:

    - define the correct MinIO endpoint for your host
    - provide the correct storage password for your MinIO instance
    - provide the correct path in the MinIO bucket to store the data

    Re-run the script to ingest the sample data file `csv-aws-example.csv` into MinIO:

    ```bash
    python3 copy_file_to_incoming.py csv-aws-example.csv
    ```

    And make sure the errors are resolved.

You can verify that the data was uploaded correctly by checking the MinIO user interface and seeing if the sample data is available in the correct directory in the `wis2box-incoming` bucket.

You can use the Grafana dashboard to check the status of the data ingest workflow.

Finally you can use MQTT Explorer to check if notifications were published for the data you ingested. You should see that the CSV data was transformed into BUFR format and that a WIS2 data notification was published with a "canonical" url to enable downloading the BUFR data.

## Exercise 2: Ingesting binary data

Next, we try to ingest binary data in BUFR format using the MinIO Python client.

wis2box can ingest binary data in BUFR format using the `wis2box.data.bufr4.ObservationDataBUFR` plugin included in wis2box.

This plugin will split the BUFR file into individual BUFR messages and publish each message to the MQTT broker. If the station for the corresponding BUFR message is not defined in the wis2box station metadata, the message will not be published.

Since you used the `surface-based-observations/synop` template in the previous session you data mappings include the plugin `FM-12 data converted to BUFR` for the dataset mappings. This plugin loads the module `wis2box.data.synop2bufr.ObservationDataSYNOP2BUFR` to ingest the data.

!!! question "Ingesting binary data in BUFR format"

    Run the following command to copy the binary data file `bufr-example.bin` into the `wis2box-incoming` bucket in MinIO:

    ```bash
    python3 copy_file_to_incoming.py bufr-example.bin
    ```

Check the Grafana dashboard and MQTT Explorer to see if the test-data was successfully ingested and published and if you see any errors, try to resolve them.

!!! question "Verify the data ingest"

    How many messages were published to the MQTT broker for this data sample?

??? success "Click to reveal answer"

    If you successfully ingested and published the last data sample, you should have received 10 new notifications on the wis2box MQTT broker. Each notification correspond to data for one station for one observation timestamp.

    The plugin `wis2box.data.bufr4.ObservationDataBUFR` splits the BUFR file into individual BUFR messages and publishes one message for each station and observation timestamp.

## Exercise 3: Ingesting SYNOP data in ASCII format

In the previous session we used the SYNOP form in the **wis2box-webapp** to ingest SYNOP data in ASCII format. You can also ingest SYNOP data in ASCII format by uploading the data into MinIO. 

In the previous session you should have created a dataset which included the plugin 'FM-12 data converted to BUFR' for the dataset mappings:

<img alt="dataset-mappings" src="../../assets/img/wis2box-data-mappings.png" width="800">

This plugin loads the module `wis2box.data.synop2bufr.ObservationDataSYNOP2BUFR` to ingest the data.

Try to use the MinIO Python client to ingest the test data `synop-202307.txt` and `synop-202308.txt` into your wis2box instance.

Note that the 2 files contain the same content, but the filename is different. The filename is used to determine the date of the data sample.

The synop2bufr plugin relies on a file-pattern to extract the date from the filename. The first group in the regular expression is used to extract the year and the second group is used to extract the month.

!!! question "Ingest FM-12 SYNOP data in ASCII format"

    Go back to the MinIO interface in your browse and navigate to the `wis2box-incoming` bucket and into the path where you uploaded the test data in the previous exercise.
    
    Upload the new files in the correct path in the `wis2box-incoming` bucket in MinIO to trigger the data ingest workflow.

    Check the Grafana dashboard and MQTT Explorer to see if the test data was successfully ingested and published.

    What is the difference in the `properties.datetime` between the two messages published to the MQTT broker?

??? success "Click to reveal answer"

    Check the properties of the last 2 notifications in MQTT Explorer and you will note that one notification has:

    ```{.copy}
    "properties": {
        "data_id": "wis2/urn:wmo:md:nl-knmi-test:surface-based-observations.synop/WIGOS_0-20000-0-60355_20230703T090000",
        "datetime": "2023-07-03T09:00:00Z",
        ...
    ```

    and the other notification has:

    ```{.copy}
    "properties": {
        "data_id": "wis2/urn:wmo:md:nl-knmi-test:surface-based-observations.synop/WIGOS_0-20000-0-60355_20230803T090000",
        "datetime": "2023-08-03T09:00:00Z",
        ...
    ```

    The filename was used to determine the year and month of the data sample.

## Exercise 4: ingesting data using the wis2box-ftp service

You can add an additional service that adds an ftp-endpoint on your wis2box-instance. This service will forward data uploaded via ftp to the MinIO storage service, preserving the directory structure of the uploaded data.

To use the `docker-compose.wis2box-ftp.yml` template included in wis2box, you need to pass some additional environment variables to the wis2box-ftp service.

You can use the file `wis2box-ftp.env` file from the `exercise-materials/` directory to define the required environment variables. Start by copying the file to the `wis2box-1.0b8` directory:

```bash
cp ~/exercise-materials/data-ingest-exercises/wis2box-ftp.env ~/wis2box-1.0b8/
```

!!! question "Configuring and starting the wis2box-ftp service"

    Edit the file `wis2box-ftp.env` to define the required environment variables:

    - `FTP_USER`: the username for the ftp-endpoint (to be defined by the user)
    - `FTP_PASS`: the password for the ftp-endpoint (to be defined by the user)
    - `FTP_HOST`: the hostname of your wis2box-instance (e.g. `username.wis2.training`)
    - `WIS2BOX_STORAGE_USERNAME`: the MinIO storage user (e.g. `wis2box`)
    - `WIS2BOX_STORAGE_PASSWORD`: the MinIO storage password (see your `wis2box.env` file)
    - `WIS2BOX_STORAGE_ENDPOINT`: the MinIO storage endpoint, you can leave this set to `http://minio:9000` when running the wis2box-ftp on the same docker network as the MinIO service.

    You can use the `nano` or `vim` text editor to edit the file or the built-in text editor of WinSCP.

    Then start the wis2box-ftp service using the following command:

    ```bash
    cd ~/wis2box-1.0b8/
    docker compose -f docker-compose.wis2box-ftp.yml -p wis2box_project --env-file wis2box-ftp.env up -d
    ```

    NOTE: the option `-p wis2box_project` is used to ensure the wis2box-ftp service is started in the same docker network as the MinIO service for wis2box.

    You can check if the wis2box-ftp service is running using the following command:

    ```bash
    docker logs wis2box-ftp
    ```

To test the wis2box-ftp service, you can use an ftp client to upload a file to the ftp-endpoint on your wis2box-instance. The credentials for the ftp-endpoint are the ones you defined in the `wis2box-ftp.env` file by the `FTP_USER` and `FTP_PASS` environment variables.

Using WinSCP, your connection would look as follows:

<img alt="winscp-ftp-connection" src="../../assets/img/winscp-ftp-connection.png" width="400">

In WinSCP, right-click and select *New*->*Directory* to create a new directory on the FTP endpoint. 

Uploading *randomfile.txt* to the directory *not-a-valid-path*:

<img alt="FTP-not-a-valid-path" src="../../assets/img/FTP-not-a-valid-path.png" width="600">

will result in the following message on the wis2box Grafana dashboard:

*ERROR - Path validation error: Could not match http://minio:9000/wis2box-incoming/not-a-valid-path/randomfile.txt to dataset, path should include one of the following: ...*

The file was forwarded by the wis2box-ftp service to the 'wis2box-incoming' bucket in MinIO, but the path did not match any of the dataset identifiers defined in your wis2box instance, resulting in an error.

You can also use `ftp` from the command line:

```bash
ftp username.wis2.training
```
Login using the credentials defined in `wis2box-ftp.env` for the `FTP_USER` and `FTP_PASS` environment variables, and then create a directory and upload a file as follows:

```bash
mkdir not-a-valid-path
cd not-a-valid-path
put ~/exercise-materials/data-ingest-exercises/synop.txt synop.txt
```

This will result a "Path validation error" in the Grafana dashboard indicating that the file was uploaded to MinIO.

To exit the ftp client, type `exit`. 

!!! Question "Test the wis2box-ftp service"

    Try to ingest the file `synop.txt` into your wis2box instance using the wis2box-ftp service to trigger the data ingest workflow.

    Check the MinIO user interface to see if the file was uploaded to the correct path in the `wis2box-incoming` bucket. If you don't see the file in MinIO you can check the logs of the wis2box-ftp service to see if there were any errors in the process forwarding the data to MinIO.
    
    Check the Grafana dashboard to see if the data ingest workflow was triggered or if there were any errors.

The wis2box-ftp service will forward the data to the MinIO storage service, preserving the directory structure of the uploaded data. To ensure your data is ingested correctly, make sure the file is uploaded to a directory that matches the dataset-id or topic of your dataset.

## Conclusion

!!! success "Congratulations!"
    In this practical session, you learned how to:

    - trigger wis2box workflow using a Python script and the MinIO Python client
    - use different data plugins to ingest different data formats
    - forward data to wis2box using the wis2box-ftp service

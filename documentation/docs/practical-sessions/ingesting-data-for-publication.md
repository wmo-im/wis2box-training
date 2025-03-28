---
title: Monitoring WIS2 Notifications
---

# Monitoring WIS2 Notifications 

!!! abstract "Learning outcomes"

    By the end of this practical session, you will be able to:
    
    - trigger the wis2box workflow by uploading data in MinIO using the command-line, the MinIO web interface, SFTP or a python script
    - learn how to access the Grafana dashboard to see the status of the data ingest and the logs of your wis2box instance
    - view the WIS2 data notifications published by your wis2box using MQTT Explorer


## Introduction

In this exercise we will use a sample CSV data file to trigger the wis2box workflow and publish WIS2 notifications using the dataset you configured in the previous practical session. 
 Note that wis2box will converts CSV into BUFR format before publishing it to the MQTT broker as per the data-mappings pre-configured in your dataset. In the next exercises, you will learn more about how data-conversion in the wis2box works. For this exercise, we will focus on the different methods to upload data to your wis2box instance and how to see if you correctly ingested and published the data.

The **Grafana dashboard** uses data from Prometheus and Loki to display the status of your wis2box. Prometheus store time-series data from the metrics collected, while Loki store the logs from the containers running on your wis2box instance. This data allows you to check how much data is received on MinIO and how many WIS2 notifications are published, and if there are any errors detected in the logs.

## Preparation

This section will use the dataset for "surface-based-observations/synop" previously created in the [Configuring datasets in wis2box](/practical-sessions/configuring-wis2box-datasets) practical session and requires you to have configured stations in the **wis2box-webapp** as described in the [Configuring station metadata](/practical-sessions/configuring-station-metadata) practical session. 

Login to your student VM using your SSH client (PuTTY or other).

Make sure wis2box is up and running:

```bash
cd ~/wis2box-1.0.0rc1/
python3 wis2box-ctl.py start
python3 wis2box-ctl.py status
```

Make sure your have MQTT Explorer running and connected to your instance using the public credentials `everyone/everyone` with a subscription to the topic `origin/a/wis2/#`.

Make sure you have access to the MinIO web interface by going to `http://<your-host>:9000` and you are logged (using `WIS2BOX_STORAGE_USERNAME` and `WIS2BOX_STORAGE_PASSWORD` from your `wis2box.env` file).

Make sure you have a web browser open with the Grafana dashboard for your instance by going to `http://<your-host>:3000`.

## Testing the data ingest from the command line

Please execute the following commands from your SSH-client session:

Copy the sample data file `aws-example.csv` to the the directory you defined as the `WI2BOX_HOST_DATADIR` in your `wis2box.env` file.

```bash
cp ~/exercise-materials/data-ingest-exercises/aws-example.csv ~/wis2box-data/
```

Make sure you are in the `wis2box-1.0.0rc1` directory and login to the **wis2box-management** container:

```bash
cd ~/wis2box-1.0.0rc1
python3 wis2box-ctl.py login
```

Verify the sample data is available in the directory `/data/wis2box/` within the **wis2box-management** container:

```bash
ls -lh /data/wis2box/aws-example.csv
```

You can edit the file using nano or vim:

```bash
nano /data/wis2box/aws-example.csv
```

Don't edit the file for now, just check the content and exit the editor.

!!! note
    The `WIS2BOX_HOST_DATADIR` is mounted as `/data/wis2box/` inside the wis2box-management container by the `docker-compose.yml` file included in the `wis2box-1.0.0rc1` directory.
    
    This allows you to share data between the host and the container.

!!! question "Ingesting data using `wis2box data ingest`"

    Execute the following command to ingest the sample data file `aws-example.csv` to your wis2box-instance:

    ```bash
    wis2box data ingest -p /data/wis2box/aws-example.csv --metadata-id urn:wmo:md:not-my-centre:core.surface-based-observations.synop
    ```

    Was the data successfully ingested? If not, what was the error message and how can you fix it?

??? success "Click to reveal answer"

    You will see the following output:

    ```bash
    Error: metadata_id=urn:wmo:md:not-my-centre:core.surface-based-observations.synop not found in data mappings
    ```

    The error message indicates that the metadata identifier you provided does not match any of the datasets you have configured in your wis2box-instance.

    Provide the correct metadata-id that matches the dataset you created in the previous practical session and repeat the data ingest command until you should see the following output:

    ```bash 
    Processing /data/wis2box/aws-example.csv
    Done
    ```

Go to the MinIO console in your browser and check if the file `aws-example.csv` was uploaded to the `wis2box-incoming` bucket. You should see there is a new directory with the name of the dataset you provided in the `--metadata-id` option:

<img alt="minio-wis2box-incoming-dataset-folder" src="../../assets/img/minio-wis2box-incoming-dataset-folder.png" width="800">

!!! note
    The `wis2box data ingest` command uploaded the file to the `wis2box-incoming` bucket in MinIO in a directory named after the metadata identifier you provided.

Go to the Grafana dashboard in your browser and check the status of the data ingest.

!!! question "Check the status of the data ingest"
    
    Go to the Grafana dashboard in your browser and check the status of the data ingest.
    
    Was the data successfully ingested?

??? success "Click to reveal answer"
    The panel at the bottom of the Grafana home dashboard reports the following warnings:    
    
    `WARNING - input=aws-example.csv warning=Station 0-20000-0-60355 not in station list; skipping`
    `WARNING - input=aws-example.csv warning=Station 0-20000-0-60360 not in station list; skipping`

    This warning indicates that the stations are not defined in the station list of your wis2box. No WIS2 notifications will be published for this station until you add it to the station list and associate it with the topic for your dataset.

!!! question "Update the input data to match the stations in your wis2box instance"

    Edit the example .csv file and update the WIGOS-station-identifiers in the input-data to match the stations you have in your wis2box instance.

    Now re-upload the sample data file `aws-example.csv` to the same path in MinIO you used in the previous exercise.

    Check the Grafana dashboard, are there any new errors or warnings ? How can you see that the test data was successfully ingested and published?

??? success "Click to reveal answer"

    You can check the charts on the Grafana home dashboard to see if the test data was successfully ingested and published.
    
    If successful, you should see the following:

    <img alt="grafana_success" src="../../assets/img/grafana_success.png" width="800">

!!! question "Check the MQTT broker for WIS2 notifications"
    
    Go to the MQTT Explorer and check if you can see the WIS2 Notification Message for the data you just ingested.
    
    How many WIS2 data notifications were published by your wis2box?
    
    How do you access the content of the data being published?

??? success "Click to reveal answer"

    You should see 6 WIS2 data notifications published by your wis2box.

    To access the content of the data being published, you can expand the topic structure to see the different levels of the message until you reach the last level and review message content of one of the messages.

    The message content has a "links" section with a "rel" key of "canonical" and a "href" key with the URL to download the data. The URL will be in the format `http://<your-host>/data/...`. 
    
    Note that the data-format is BUFR and you will need a BUFR parser to view the content of the data. The BUFR format is a binary format used by meteorological services to exchange data. The data-plugins inside wis2box transformed the data from CSV to BUFR before publishing it.

## Uploading data using the MinIO web interface

In the previous exercises, you uploaded data available on the wis2box-host to MinIO using the `wis2box data ingest` command. 

Next we will use the MinIO web interface, which allows you to download and upload data to MinIO using a web browser.

!!! question "Upload data using the MinIO web interface"

    Go to the MinIO web interface in your browser and browse to the `wis2box-incoming` bucket. You will see the file `aws-example.csv` you uploaded in the previous exercises.

    You can download this file and re-upload it to the same path in MinIO to re-trigger the wis2box workflow.

    Check the Grafana dashboard and MQTT Explorer to see if the data was successfully ingested and published.

??? success "Click to reveal answer"

    You will see a message indicate that the wis2box already published this data. The wis2box will not publish the same data twice. You can change the content of the file and re-upload it to trigger the workflow again. You can also upload a random file from your computer and you will note the Grafana dashboard will show errors indicating could not be ingested.

## Uploading data using SFTP

The MinIO server also supports SFTP. You can use an SFTP client to upload data to MinIO.

!!! question "Upload data using SFTP"

    Use an SFTP client to connect to your wis2box instance using the credentials `WIS2BOX_STORAGE_USERNAME` and `WIS2BOX_STORAGE_PASSWORD` from your `wis2box.env` file.

    Upload the sample data file `aws-example.csv` to the same path in MinIO you used in the previous exercises.

    Check the Grafana dashboard and MQTT Explorer to see if the data was successfully ingested and published.

??? success "Click to reveal answer"

    If you uploaded the data correctly you will see a message indicating that the wis2box already published this data. If you use the wrong path or bucket name, you will see an error message in the logs of the wis2box-management container.

## Uploading data using a Python script

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
python3 copy_file_to_incoming.py ~/wis2box-data/aws-example.csv
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
    python3 copy_file_to_incoming.py ~/wis2box-data/aws-example.csv
    ```

    And make sure the errors are resolved.

## Conclusion

!!! success "Congratulations!"
    In this practical session, you learned how to:

    - trigger the wis2box workflow by uploading data in MinIO using various methods
    - debug common errors in the data ingest process using the Grafana dashboard and the logs of your wis2box instance
    - monitor WIS2 data notifications published by your wis2box in the Grafana dashboard and MQTT Explorer


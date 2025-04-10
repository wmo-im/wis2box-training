---
title: Ingesting Data for Publication
---

# Ingesting data for publication

!!! abstract "Learning Outcomes"

    By the end of this practical session, you will be able to:
    
    - Trigger the wis2box workflow by uploading data to MinIO using the command line, the MinIO web interface, SFTP, or a Python script.
    - Access the Grafana dashboard to monitor the status of data ingestion and view logs of your wis2box instance.
    - View WIS2 data notifications published by your wis2box using MQTT Explorer.

## Introduction

In WIS2, data is shared in real-time using WIS2 data notifications that contain a "canonical" link from which the data can be downloaded.

To trigger the data workflow in a WIS2 Node using the wis2box software, data must be uploaded to the **wis2box-incoming** bucket in **MinIO**, which initiates the wis2box workflow. This process results in the data being published via a WIS2 data notification. Depending on the data mappings configured in your wis2box instance, the data may be transformed into BUFR format before being published.

In this exercise, we will use sample data files to trigger the wis2box workflow and **publish WIS2 data notifications** for the dataset you configured in the previous practical session.

During the exercise, we will monitor the status of the data ingestion using the **Grafana dashboard** and **MQTT Explorer**. The Grafana dashboard uses data from Prometheus and Loki to display the status of your wis2box, while MQTT Explorer allows you to see the WIS2 data notifications published by your wis2box instance.

Note that wis2box will transform the example data into BUFR format before publishing it to the MQTT broker, as per the data mappings pre-configured in your dataset. For this exercise, we will focus on the different methods to upload data to your wis2box instance and verify successful ingestion and publication. Data transformation will be covered later in the [Data Conversion Tools](../data-conversion-tools) practical session.

## Preparation

This section uses the dataset for "surface-based-observations/synop" previously created in the [Configuring Datasets in wis2box](/practical-sessions/configuring-wis2box-datasets) practical session. It also requires knowledge of configuring stations in the **wis2box-webapp**, as described in the [Configuring Station Metadata](/practical-sessions/configuring-station-metadata) practical session.

Ensure you can log in to your student VM using your SSH client (e.g., PuTTY).

Ensure wis2box is up and running:

```bash
cd ~/wis2box/
python3 wis2box-ctl.py start
python3 wis2box-ctl.py status
```

Ensure MQTT Explorer is running and connected to your instance using the public credentials `everyone/everyone` with a subscription to the topic `origin/a/wis2/#`.

Ensure you have a web browser open with the Grafana dashboard for your instance by navigating to `http://YOUR-HOST:3000`.

### Prepare Example Data

Copy the directory `exercise-materials/data-ingest-exercises` to the directory you defined as the `WIS2BOX_HOST_DATADIR` in your `wis2box.env` file:

```bash
cp -r ~/exercise-materials/data-ingest-exercises ~/wis2box-data/
```

!!! note
    The `WIS2BOX_HOST_DATADIR` is mounted as `/data/wis2box/` inside the wis2box-management container by the `docker-compose.yml` file included in the `wis2box` directory.
    
    This allows you to share data between the host and the container.

### Add the Test Station

Add the station with WIGOS identifier `0-20000-0-64400` to your wis2box instance using the station editor in the wis2box-webapp.

Retrieve the station from OSCAR:

<img alt="oscar-station" src="../../assets/img/webapp-test-station-oscar-search.png" width="600">

Add the station to the datasets you created for publishing on "../surface-based-observations/synop" and save the changes using your authentication token:

<img alt="webapp-test-station" src="../../assets/img/webapp-test-station-save.png" width="800">

Note that you can remove this station from your dataset after the practical session.

## Testing Data Ingestion from the Command Line

In this exercise, we will use the `wis2box data ingest` command to upload data to MinIO.

Ensure you are in the `wis2box` directory and log in to the **wis2box-management** container:

```bash
cd ~/wis2box
python3 wis2box-ctl.py login
```

Verify the following sample data is available in the directory `/data/wis2box/` within the **wis2box-management** container:

```bash
ls -lh /data/wis2box/data-ingest-exercises/synop_202412030900.txt
```

!!! question "Ingesting Data Using `wis2box data ingest`"

    Execute the following command to ingest the sample data file into your wis2box instance:

    ```bash
    wis2box data ingest -p /data/wis2box/data-ingest-exercises/synop_202412030900.txt --metadata-id urn:wmo:md:not-my-centre:synop-test
    ```

    Was the data successfully ingested? If not, what was the error message, and how can you fix it?

??? success "Click to Reveal Answer"

    The data was **not** successfully ingested. You should see the following:

    ```bash
    Error: metadata_id=urn:wmo:md:not-my-centre:synop-test not found in data mappings
    ```

    The error message indicates that the metadata identifier you provided does not match any of the datasets you have configured in your wis2box instance.

    Provide the correct metadata ID that matches the dataset you created in the previous practical session and repeat the data ingestion command until you see the following output:

    ```bash 
    Processing /data/wis2box/data-ingest-exercises/synop_202412030900.txt
    Done
    ```

Go to the MinIO console in your browser and check if the file `synop_202412030900.txt` was uploaded to the `wis2box-incoming` bucket. You should see a new directory with the name of the dataset you provided in the `--metadata-id` option, and inside this directory, you will find the file `synop_202412030900.txt`:

<img alt="minio-wis2box-incoming-dataset-folder" src="../../assets/img/minio-data-ingest-test-data.png" width="800">

!!! note
    The `wis2box data ingest` command uploaded the file to the `wis2box-incoming` bucket in MinIO in a directory named after the metadata identifier you provided.

Go to the Grafana dashboard in your browser and check the status of the data ingestion.

!!! question "Check the Status of the Data Ingestion on Grafana"
    
    Go to the Grafana dashboard at **http://your-host:3000** and check the status of the data ingestion in your browser.
    
    How can you see if the data was successfully ingested and published?

??? success "Click to Reveal Answer"
    
    If you successfully ingested the data, you should see the following:
    
    <img alt="grafana_data_ingest" src="../../assets/img/grafana_data-ingest-test.png" width="400">  
    
    If you do not see this, please check for WARNING or ERROR messages displayed at the bottom of the dashboard and attempt to resolve them.

!!! question "Check the MQTT Broker for WIS2 Notifications"
    
    Go to the MQTT Explorer and check if you can see the WIS2 notification message for the data you just ingested.
    
    How many WIS2 data notifications were published by your wis2box?
    
    How do you access the content of the data being published?

??? success "Click to Reveal Answer"

    You should see 1 WIS2 data notification published by your wis2box.

    To access the content of the data being published, you can expand the topic structure to see the different levels of the message until you reach the last level and review the message content.

    The message content has a "links" section with a "rel" key of "canonical" and a "href" key with the URL to download the data. The URL will be in the format `http://YOUR-HOST/data/...`. 
    
    Note that the data format is BUFR, and you will need a BUFR parser to view the content of the data. The BUFR format is a binary format used by meteorological services to exchange data. The data plugins inside wis2box transformed the data into BUFR before publishing it.

After completing this exercise, exit the **wis2box-management** container:

```bash
exit
```

## Uploading Data Using the MinIO Web Interface

In the previous exercises, you uploaded data available on the wis2box host to MinIO using the `wis2box data ingest` command. 

Next, we will use the MinIO web interface, which allows you to download and upload data to MinIO using a web browser.

!!! question "Re-upload Data Using the MinIO Web Interface"

    Go to the MinIO web interface in your browser and browse to the `wis2box-incoming` bucket. You will see the file `synop_202412030900.txt` you uploaded in the previous exercises.

    Click on the file, and you will have the option to download it:

    <img alt="minio-wis2box-incoming-dataset-folder" src="../../assets/img/minio-download.png" width="800">

    You can download this file and re-upload it to the same path in MinIO to re-trigger the wis2box workflow.

    Check the Grafana dashboard and MQTT Explorer to see if the data was successfully ingested and published.

??? success "Click to Reveal Answer"

    You will see a message indicating that the wis2box already published this data:

    ```bash
    ERROR - Data already published for WIGOS_0-20000-0-64400_20241203T090000-bufr4; not publishing
    ``` 
    
    This demonstrates that the data workflow was triggered, but the data was not re-published. The wis2box will not publish the same data twice. 
    
!!! question "Upload New Data Using the MinIO Web Interface"
    
    Download this sample file [synop_202502040900.txt](/sample-data/synop_202502040900.txt) (right-click and select "save as" to download the file).
    
    Upload the file you downloaded using the web interface to the same path in MinIO as the previous file.

    Did the data ingest and publish successfully?

??? success "Click to Reveal Answer"

    Go to the Grafana dashboard and check if the data was successfully ingested and published.

    If you use the wrong path, you will see an error message in the logs.

    If you use the correct path, you will see one more WIS2 data notification published for test station `0-20000-0-64400`, indicating that the data was successfully ingested and published.

    <img alt="grafana_data_ingest" src="../../assets/img/grafana_data-ingest-test2.png" width="400"> 

## Uploading Data Using SFTP

The MinIO service in wis2box can also be accessed over SFTP. The SFTP server for MinIO is bound to port 8022 on the host (port 22 is used for SSH).

In this exercise, we will demonstrate how to use WinSCP to upload data to MinIO using SFTP.

You can set up a new WinSCP connection as shown in this screenshot:

<img alt="winscp-sftp-connection" src="../../assets/img/winscp-sftp-login.png" width="400">

The credentials for the SFTP connection are defined by `WIS2BOX_STORAGE_USERNAME` and `WIS2BOX_STORAGE_PASSWORD` in your `wis2box.env` file and are the same as the credentials you used to connect to the MinIO UI.

When you log in, you will see the buckets used by wis2box in MinIO:

<img alt="winscp-sftp-bucket" src="../../assets/img/winscp-buckets.png" width="600">

You can navigate to the `wis2box-incoming` bucket and then to the folder for your dataset. You will see the files you uploaded in the previous exercises:

<img alt="winscp-sftp-incoming-path" src="../../assets/img/winscp-incoming-data-path.png" width="600">

!!! question "Upload Data Using SFTP"

    Download this sample file to your local computer:

    [synop_202503030900.txt](/sample-data/synop_202503030900.txt) (right-click and select "save as" to download the file).

    Then upload it to the incoming dataset path in MinIO using your SFTP session in WinSCP.

    Check the Grafana dashboard and MQTT Explorer to see if the data was successfully ingested and published.

??? success "Click to Reveal Answer"

    You should see a new WIS2 data notification published for the test station `0-20000-0-64400`, indicating that the data was successfully ingested and published.

    <img alt="grafana_data_ingest" src="../../assets/img/grafana_data-ingest-test3.png" width="400"> 

    If you use the wrong path, you will see an error message in the logs.

## Uploading Data Using a Python Script

In this exercise, we will use the MinIO Python client to copy data into MinIO.

MinIO provides a Python client, which can be installed as follows:

```bash
pip3 install minio
```

On your student VM, the 'minio' package for Python will already be installed.

In the `exercise-materials/data-ingest-exercises` directory, you will find an example script `copy_file_to_incoming.py` that can be used to copy files into MinIO.

Try to run the script to copy the sample data file `synop_202501030900.txt` into the `wis2box-incoming` bucket in MinIO as follows:

```bash
cd ~/wis2box-data/data-ingest-exercises
python3 copy_file_to_incoming.py synop_202501030900.txt
```

!!! note

    You will get an error as the script is not configured to access the MinIO endpoint on your wis2box yet.

The script needs to know the correct endpoint for accessing MinIO on your wis2box. If wis2box is running on your host, the MinIO endpoint is available at `http://YOUR-HOST:9000`. The script also needs to be updated with your storage password and the path in the MinIO bucket to store the data.

!!! question "Update the Script and Ingest the CSV Data"
    
    Edit the script `copy_file_to_incoming.py` to address the errors, using one of the following methods:
    - From the command line: use the `nano` or `vim` text editor to edit the script.
    - Using WinSCP: start a new connection using File Protocol `SCP` and the same credentials as your SSH client. Navigate into the directory `wis2box-data/data-ingest-exercises` and edit `copy_file_to_incoming.py` using the built-in text editor.
    
    Ensure that you:

    - Define the correct MinIO endpoint for your host.
    - Provide the correct storage password for your MinIO instance.
    - Provide the correct path in the MinIO bucket to store the data.

    Re-run the script to ingest the sample data file `synop_202501030900.txt` into MinIO:

    ```bash
    python3 ~/wis2box-data/ ~/wis2box-data/synop_202501030900.txt
    ```

    Ensure the errors are resolved.

Once you manage to run the script successfully, you will see a message indicating that the file was copied to MinIO, and you should see data notifications published by your wis2box instance in MQTT Explorer.

You can also check the Grafana dashboard to see if the data was successfully ingested and published.

Now that the script is working, you can try to copy other files into MinIO using the same script.

!!! question "Ingesting Binary Data in BUFR Format"

    Run the following command to copy the binary data file `bufr-example.bin` into the `wis2box-incoming` bucket in MinIO:

    ```bash
    python3 copy_file_to_incoming.py bufr-example.bin
    ```

Check the Grafana dashboard and MQTT Explorer to see if the test data was successfully ingested and published. If you see any errors, try to resolve them.

!!! question "Verify the Data Ingest"

    How many messages were published to the MQTT broker for this data sample?

??? success "Click to Reveal Answer"

    You will see errors reported in Grafana as the stations in the BUFR file are not defined in the station list of your wis2box instance. 
    
    If all stations used in the BUFR file are defined in your wis2box instance, you should see 10 messages published to the MQTT broker. Each notification corresponds to data for one station for one observation timestamp.

    The plugin `wis2box.data.bufr4.ObservationDataBUFR` splits the BUFR file into individual BUFR messages and publishes one message for each station and observation timestamp.

## Conclusion

!!! success "Congratulations!"
    In this practical session, you learned how to:

    - Trigger the wis2box workflow by uploading data to MinIO using various methods.
    - Debug common errors in the data ingestion process using the Grafana dashboard and the logs of your wis2box instance.
    - Monitor WIS2 data notifications published by your wis2box in the Grafana dashboard and MQTT Explorer.


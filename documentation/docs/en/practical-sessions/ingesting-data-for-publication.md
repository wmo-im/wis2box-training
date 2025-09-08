---
title: Ingesting Data for Publication
---

# Ingesting data for publication

!!! abstract "Learning Outcomes"

    By the end of this practical session, you will be able to:
    
    - Trigger the wis2box workflow by uploading data to MinIO using the MinIO web interface, SFTP, or a Python script.
    - Access the Grafana dashboard to monitor the status of data ingestion and view logs of your wis2box instance.
    - View WIS2 data notifications published by your wis2box using MQTT Explorer.

## Introduction

In WIS2, data is shared in real-time using WIS2 data notifications that contain a "canonical" link from which the data can be downloaded.

To trigger the data workflow in a WIS2 Node using the wis2box software, data must be uploaded to the **wis2box-incoming** bucket in **MinIO**, which initiates the wis2box data workflow to process and publish the data.

To monitor the status of the wis2box data workflow you can use the **Grafana dashboard** and **MQTT Explorer**. The Grafana dashboard uses data from Prometheus and Loki to display the status of your wis2box, while MQTT Explorer allows you to see the WIS2 data notifications published by your wis2box instance.

In this section, we will focus on how to upload data to your wis2box instance and verify successful ingestion and publication. Data transformation will be covered later in the [Data Conversion Tools](./data-conversion-tools.md) practical session.

To manually test the data ingestion process, we will use the MinIO web interface, which allows you to download and upload data to MinIO using a web browser. 

In a production environment, data would typically be ingested using automated processes, such as scripts or applications that forward data to MinIO over S3 or SFTP.

## Preparation

This section assumes you have successfully completed the [Configuring Datasets in wis2box](./configuring-wis2box-datasets.md) practical session. If you followed the instructions in that session, you should have one dataset using the `Universal` plugin, and another that uses the `FM-12 data converted to BUFR` plugin.

Ensure you can log in to your student VM using your SSH client (e.g., PuTTY).

Ensure wis2box is up and running:

```bash
cd ~/wis2box/
python3 wis2box-ctl.py start
python3 wis2box-ctl.py status
```

Ensure MQTT Explorer is running and connected to your instance using the public credentials `everyone/everyone` with a subscription to the topic `origin/a/wis2/#`.

## The Grafana Dashboard

Open the Grafana dashboard available at `http://YOUR-HOST:3000` and you will see the wis2box data publication dashboard:

<img alt="grafana_dashboard" src="/../assets/img/grafana-homepage.png" width="800">

Keep the Grafana dashboard open in your browser as we will use it later to monitor the status of data ingestion.

## Using the MinIO Web Interface

Open the MinIO web interface available at `http://YOUR-HOST:9001` and you will see the login screen:

<img alt="Minio UI: minio ui" src="/../assets/img/minio-login.png" width="400">

To login you need to use the credentials defined by WIS2BOX_STORAGE_USERNAME and WIS2BOX_STORAGE_PASSWORD in the wis2box.env file.
You can check the values of these variables by running the following commands on your student VM:

```bash
cat wis2box.env | grep WIS2BOX_STORAGE_USERNAME
cat wis2box.env | grep WIS2BOX_STORAGE_PASSWORD
```

After login you are in the Object Browser view of MinIO. Here you can see the buckets used by wis2box:

- *wis2box-incoming*: This is the bucket where you upload data to trigger the wis2box workflow.
- *wis2box-public*: This is the bucket where wis2box publishes data that has been successfully ingested and processed.

Click on the bucket *wis2box-incoming*. Try the option to define a new path in this bucket by clicking `Create new path`:

<img alt="minio ui: minio ui after login" src="/../assets/img/minio-incoming-create-new-path.png" width="800">

Enter the new Folder Path = *new-directory" and upload this example file [mydata.nc](./../sample-data/mydata.nc) (right-click and select "save as" to download the file). You can use the "Upload" button in MinIO to upload the file into the new directory:

<img alt="minio ui: create new path" src="/../assets/img/minio-initial-example-upload.png" width="800">

!!! question "Question"

    After uploading the file, how do you see if data workflow in wis2box was triggered successfully?F

??? success "Click to Reveal Answer"

    You can check the Grafana dashboard to see if the data was successfully ingested and published.

    Look the bottom panel of the Grafana dashboard and you will see a **Path validation error** indicating that the path does not match any configured dataset:

    ```bash
    ERROR - Path validation error: Could not match http://minio:9000/wis2box-incoming/new-directory/mydata.nc to dataset, path should include one of the following: ['urn:wmo:md:int-wmo-example:synop-dataset-wis2-training', 'urn:wmo:md:int-wmo-example:forecast-dataset' ...
    ``` 
    
## Ingest & Publish using Universal plugin 

Now that you know how to upload data to MinIO, let's try to upload data for the dataset you created in the previous practical session using the `Universal` plugin.

Go back to the MinIO web interface in your browser, select the bucket `wis2box-incoming`, and click `Create new path`.

This time make sure to **create a directory that matches the metadata identifier for the forecast dataset** you created in the previous practical session:

<img alt="minio-filepath-forecast-dataset" src="/../assets/img/minio-filepath-forecast-dataset.png" width="800">

Enter the newly created directory, click `Upload` and upload the file you used previously, *mydata.nc*, into the new directory. Check the Grafana dashboard to see if the data was successfully ingested and published.

You should see the following error in the Grafana dashboard:

```bash
ERROR - Path validation error: Unknown file type (nc) for metadata_id=urn:wmo:md:int-wmo-example:forecast-dataset. Did not match any of the following:grib2
```

!!! question "Question"

    Why was the data not ingested and published?

??? success "Click to Reveal Answer"

    The dataset was configured to only process files with the `.grib2` extension only. The File Extension configuration is part of data mappings you defined in the previous practical session.

Download this file [GEPS_18August2025.grib2](../sample-data/GEPS_18August2025.grib2) to your local computer and upload it into the directory you created for the forecast dataset. Check the Grafana dashboard and MQTT Explorer to see if the data was successfully ingested and published.

You will see the following ERROR in the Grafana dashboard:

```bash
ERROR - Failed to transform file http://minio:9000/wis2box-incoming/urn:wmo:md:int-wmo-example:forecast-dataset/GEPS_18August2025.grib2 : GEPS_18August2025.grib2 did not match ^.*?_(\d{8}).*?\..*$
```

!!! question "Question"

    How can you address this error?

??? success "Click to Reveal Answer"

    The filename does not match the regular expression you defined in the dataset configuration. The filename must match the pattern `^.*?_(\d{8}).*?\..*$`, which requires an 8-digit date (YYYYMMDD) in the filename.

    Rename the file to *GEPS_202508180000.grib2* and upload it again to the same path in MinIO to re-trigger the wis2box workflow. (or download the renamed file from here: [GEPS_202508180000.grib2](../sample-data/GEPS_202508180000.grib2)).

After fixing the issue with the filename, check the Grafana dashboard and MQTT Explorer to see if the data was successfully ingested and published.

You should see a new WIS2 data notification in MQTT Explorer:

<img alt="mqtt explorer: message notification geps data" src="/../assets/img/mqtt-explorer-wis2-notification-geps-sample.png" width="800">

!!! note "About the Universal Plugin"

    The "Universal"-plugin allows you to publish data without any transformation. It is a *pass-through* plugin that ingests the data file and publishes it as-is. In order to add the property "datetime" to the WIS2 data notification, the plugin relies of the first group in the File Pattern to match the date for data you are publishing.

!!! question "Bonus Question"

    Try uploading the same file again to the same path in MinIO. Do you get another notification in MQTT Explorer?

??? success "Click to Reveal Answer"

    No. 
    In the Grafana Dashboard you will see an error indicating that the data was already published:

    ```bash
    ERROR - Data already published for GEPS_202508180000-grib2; not publishing
    ``` 
    
    This demonstrates that the data workflow was triggered, but the data was not re-published. The wis2box will not publish the same data twice.

    If you want to force re-sending the notification for the same data, delete the data from the 'wis2box-public' bucket before re-ingesting the data.

## Ingest & Publish using synop2bufr-plugin

Next you will dataset you created in the previous practical session using **Template='weather/surface-based-observations/synop'**. The template pre-configured the following data plugins for you:

<img alt="synop-dataset-plugins" src="/../assets/img/wis2box-data-mappings.png" width="1000">

Note that one of the plugins is **FM-12 data converted to BUFR** (synop2bufr) which is configured to run on files with File extension **txt**.

Download this sample data [synop_202502040900.txt](../sample-data/synop_202502040900.txt) (right-click and select "save as" to download the file) to your local computer. Create a new path in MinIO that matches the metadata identifier for the synop dataset, and upload the sample data into this path.

Check the Grafana dashboard and MQTT Explorer to see if the data was successfully ingested and published.

!!! question "Question"

    Why did you not get a notification in MQTT Explorer?

??? success "Click to Reveal Answer"

    In the Grafana Dashboard you will see a warning indicating:

    ```bash
    WARNING - Station 64400 not found in station file
    ``` 
    
    Or if you had no stations associated with the topic you will see:

    ```bash
    ERROR - No stations found
    ```

    The data workflow was triggered, but the data plugin could not process the data due to missing station metadata.

!!! note "About the plugin FM-12 data converted to BUFR"

    This plugin attempts to transform the FM-12 input data into BUFR format. 
    
    As part of the transformation, the plugin adds missing metadata to the output data, such as the WIGOS station identifier, location and barometer height of the station. In order to add this metadata, the plugin looks up this information in the station list of your wis2box instance using the traditional (5-digit) identifier (64400 in this case).

    If the station is not found in the station list, the plugin cannot add the missing metadata and will not publish any data.
    
Add the station with WIGOS identifier `0-20000-0-64400` to your wis2box instance using the station editor in the wis2box-webapp, as you you learned in the [Configuring Station Metadata](./configuring-station-metadata.md) practical session.

Retrieve the station from OSCAR:

<img alt="oscar-station" src="/../assets/img/webapp-test-station-oscar-search.png" width="600">

Add the station to the topic for '../weather/surface-based-observations/synop' and save the changes using your authentication token.

After adding the station, re-trigger the wis2box workflow by uploading the sample data file *synop_202502040900.txt* again into the same path in MinIO.

Check the Grafana dashboard and check MQTT Explorer to confirm that the data was published successfully. If you see the notification below then you published the synop sample data successfully:

<img alt="webapp-test-station" src="/../assets/img/mqtt-explorer-wis2box-notification-synop-sample.png" width="800">

!!! question "Question"

    What is the extension of the file that was published in the WIS2 data notification?

??? success "Click to Reveal Answer"

    Check the Links section of the WIS2 data notification in MQTT Explorer and you will see the canonical link:

    ```json
    {
      "rel": "canonical",
      "type": "application/bufr",
      "href": "http://example.wis2.training/data/2025-02-04/wis/urn:wmo:md:int-wmo-example:synop-dataset/WIGOS_0-20000-0-64400_20250204T090000.bufr4",
      "length": 387
    }
    ```      

    The file extension is `.bufr4`, indicating that the data was successfully transformed from FM-12 format to BUFR format by the plugin.

## Ingesting data using Python

In this exercise, we will use the MinIO Python client to copy data into MinIO.

MinIO provides a Python client, which can be installed as follows:

```bash
pip3 install minio
```

On your student VM, the 'minio' package for Python will already be installed.

Copy the directory `exercise-materials/data-ingest-exercises` to the directory you defined as the `WIS2BOX_HOST_DATADIR` in your `wis2box.env` file:

```bash
cp -r ~/exercise-materials/data-ingest-exercises ~/wis2box-data/
```

!!! note
    The `WIS2BOX_HOST_DATADIR` is mounted as `/data/wis2box/` inside the wis2box-management container by the `docker-compose.yml` file included in the `wis2box` directory.
    
    This allows you to share data between the host and the container.

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

## Ingesting data over SFTP

The MinIO service in wis2box can also be accessed over SFTP. The SFTP server for MinIO is bound to port 8022 on the host (port 22 is used for SSH).

In this exercise, we will demonstrate how to use WinSCP to upload data to MinIO using SFTP.

You can set up a new WinSCP connection as shown in this screenshot:

<img alt="winscp-sftp-connection" src="/../assets/img/winscp-sftp-login.png" width="400">

The credentials for the SFTP connection are defined by `WIS2BOX_STORAGE_USERNAME` and `WIS2BOX_STORAGE_PASSWORD` in your `wis2box.env` file and are the same as the credentials you used to connect to the MinIO UI.

When you log in, you will see the buckets used by wis2box in MinIO:

<img alt="winscp-sftp-bucket" src="/../assets/img/winscp-buckets.png" width="600">

You can navigate to the `wis2box-incoming` bucket and then to the folder for your dataset. You will see the files you uploaded in the previous exercises:

<img alt="winscp-sftp-incoming-path" src="/../assets/img/winscp-incoming-data-path.png" width="600">

!!! question "Upload Data Using SFTP"

    Download this sample file to your local computer:

    [synop_202503030900.txt](./../sample-data/synop_202503030900.txt) (right-click and select "save as" to download the file).

    Then upload it to the incoming dataset path in MinIO using your SFTP session in WinSCP.

    Check the Grafana dashboard and MQTT Explorer to see if the data was successfully ingested and published.

??? success "Click to Reveal Answer"

    You should see a new WIS2 data notification published for the test station `0-20000-0-64400`, indicating that the data was successfully ingested and published.

    <img alt="grafana_data_ingest" src="/../assets/img/grafana_data-ingest-test3.png" width="400"> 

    If you use the wrong path, you will see an error message in the logs.

## Conclusion

!!! success "Congratulations!"
    In this practical session, you learned how to:

    - Trigger the wis2box workflow by uploading data to MinIO using various methods.
    - Debug common errors in the data ingestion process using the Grafana dashboard and the logs of your wis2box instance.
    - Monitor WIS2 data notifications published by your wis2box in the Grafana dashboard and MQTT Explorer.


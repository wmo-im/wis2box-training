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

To trigger the data workflow in a WIS2 Node using the wis2box software, data must be uploaded to the **wis2box-incoming** bucket in **MinIO**, which initiates the wis2box workflow. This process results in the data being published via a WIS2 data notification. Depending on the data mappings configured in your wis2box instance, the data may be transformed into BUFR format before being published.

In this exercise, we will use sample data files to trigger the wis2box workflow and **publish WIS2 data notifications** for the dataset you configured in the previous practical session.

During the exercise, we will monitor the status of the data ingestion using the **Grafana dashboard** and **MQTT Explorer**. The Grafana dashboard uses data from Prometheus and Loki to display the status of your wis2box, while MQTT Explorer allows you to see the WIS2 data notifications published by your wis2box instance.

For this exercise, we will focus on the different methods to upload data to your wis2box instance and verify successful ingestion and publication. Data transformation will be covered later in the [Data Conversion Tools](./data-conversion-tools.md) practical session.

## Preparation

This section uses the dataset for "surface-based-observations/synop" and "other" previously created in the [Configuring Datasets in wis2box](./configuring-wis2box-datasets.md) practical session. 

It also requires knowledge of configuring stations in the **wis2box-webapp**, as described in the [Configuring Station Metadata](./configuring-station-metadata.md) practical session.

Ensure you can log in to your student VM using your SSH client (e.g., PuTTY).

Ensure wis2box is up and running:

```bash
cd ~/wis2box/
python3 wis2box-ctl.py start
python3 wis2box-ctl.py status
```

Ensure MQTT Explorer is running and connected to your instance using the public credentials `everyone/everyone` with a subscription to the topic `origin/a/wis2/#`.

Ensure you have a web browser open with the Grafana dashboard for your instance by navigating to `http://YOUR-HOST:3000`.

## Ingesting data using the MinIO Interface

Firstly, we will use the MinIO web interface, which allows you to download and upload data to MinIO using a web browser.

### Accessing the MinIO Interface

Open the MinIO web interface, usually available at `http://YOUR-HOST:9001`.

<img alt="Minio UI: minio ui" src="/../assets/img/minio-ui.png" width="400">

The credentials WIS2BOX_STORAGE_USERNAME and WIS2BOX_STORAGE_PASSWORD can be found in the wis2box.env file.

If you are not sure about the values, please navigate to the root directory of your wis2box and run the following command to display only the relevant credentials:

```bash
grep -E '^(WIS2BOX_STORAGE_USERNAME|WIS2BOX_STORAGE_PASSWORD)=' wis2box.env
```
Use the values of WIS2BOX_STORAGE_USERNAME and WIS2BOX_STORAGE_PASSWORD as the username and password when logging into MinIO.

### Ingest & Publish using Universal plugin 

Download the geps sample data [geps_202508180000.grib2](../sample-data/geps_202508180000.grib2) in your local environment:

Select the bucket wis2box-incoming and click `Create new path`. 

<img alt="minio ui: create new path" src="/../assets/img/minio-create-new-path.png" width="800">

The path name must correspond to the Metadata Identifier of your "other" dataset, which you previously created in the [Configuring Datasets in wis2box](./configuring-wis2box-datasets.md) practical session. 

<img alt="minio ui: create new path empty" src="/../assets/img/minio-ui-create-path-empty.png" width="700">

So in this case, please create the directory:

```bash
urn:wmo:md:my-centre-id:my-other-dataset
```

Enter the newly created directory, click `Upload`, find the [geps_202508180000.grib2](../sample-data/geps_202508180000.grib2) you downloaded to your local machine before and upload this file to wis2box-incoming bucket.

<img alt="minio ui: upload your file" src="/../assets/img/minio-other-dataset-upload.png" width="650">

Once you finish uploading it, you will see this file in MinoIO wis2box-incoming bucket:

<img alt="minio ui: upload your file" src="/../assets/img/minio-geps-file-upload.png" width="650">

After uploading, check with MQTT Explorer to confirm that the data was published successfully.

<img alt="Metadata Editor: title, description, keywords" src="/../assets/img/mqtt-explorer-wis2-notification-geps-sample.png" width="800">

Next, download the geps sample data in a different file extension [geps_202508180000.nc](../sample-data/geps_202508180000.nc) in your local environment. Upload this file into the same directory as you did in the previous exercise.

!!! question "Question"

    Can you successfully upload to the wis2box-incoming bucket?

??? success "Click to Reveal Answer"

    Yes.
    <img alt="Minio ui: geps nc file" src="/../assets/img/minio-upload-geps-with-nc-extension.png" width="800">

!!! question "Question"

    Can you successfully publish data notification messages through MinIO? 
    Check the Grafana dashboard and MQTT Explorer to see if the data was successfully ingested and published.

!!! hint

    When creating a custom dataset, which plugin did you use?
    Does the plugin have any file format requirements, and where are they specified?

??? success "Click to Reveal Answer"

    No.
    You will see a message indicating that there is an unknown file type error.

    ```bash
    ERROR - Path validation error: Unknown file type (nc) for metadata_id=urn:wmo:md:nl-knmi-test:customized-geps-dataset-wis2-training. Did not match any of the following:grib2
    ``` 
    
    This demonstrates that the data workflow was triggered, but the data was not re-published. The wis2box will not publish the data if it can not match grib2 file extension.

Then, download the renamed geps sample data [geps_renamed_sample_data.grib2](../sample-data/geps_renamed_sample_data.grib2) in your local environment. Upload this file into the same directory as you did in the previous two exercises.

!!! question "Question"

    Can you successfully upload to the wis2box-incoming bucket?

??? success "Click to Reveal Answer"

    Yes.
    <img alt="Minio ui: geps nc file" src="/../assets/img/minio-upload-renamed-geps.png" width="800">

!!! question "Question"

    Can you successfully publish data notification messages through MinIO? 
    Check the Grafana dashboard and MQTT Explorer to see if the data was successfully ingested and published.

!!! hint

    Does the custom plugin you used impose any requirements or restrictions on the filename?

??? success "Click to Reveal Answer"

    No.
        You will see a message indicating that there is an error about the data does not match the regex.

    ```bash
    ERROR - ERROR - geps_renamed_sample_data.grib2 did not match ^.*?_(\d{8}).*?\..*$
    ``` 
    
    This demonstrates that the data workflow was triggered, but the data was not re-published. The wis2box will not publish the data if it can not match file pattern ^.*?_(\d{8}).*?\..*$.

The Universal plugin provides a generic mechanism to ingest and publish files without applying domain-specific decoding. Instead, it performs a set of basic checks before publishing a WIS2 notification:

`File extension` – the file must use the extension allowed by the dataset configuration.

`Filename pattern` – the file name must match the regular expression defined in the dataset.

If both conditions are met, the file is ingested and a notification is published.

Uploading a file to MinIO always succeeds as long as the user has access. However, publishing a WIS2 data notification requires stricter validation. Files that do not satisfy the extension or filename rules will be stored in the incoming bucket, but the `Universal plugin` will not publish a notification for them. This explains why files with an unsupported extension (e.g. `geps_202508180000.nc`) or with an invalid filename (e.g. `geps_renamed_sample_data.grib2`) are accepted by MinIO but do not appear in WIS2.

Next, go to the MinIO web interface in your browser and browse to the `wis2box-incoming` bucket. You will see the file `geps_202508180000.grib2` you uploaded in the previous exercises.

Click on the file, and you will have the option to download it:

<img alt="minio-wis2box-incoming-dataset-folder" src="/../assets/img/minio-download.png" width="800">

Please download this file and re-upload it to the same path in MinIO to re-trigger the wis2box workflow.

!!! question "Question"

    Can you successfully re-publish data notification messages through MinIO? 
    Check the Grafana dashboard and MQTT Explorer to see if the data was successfully ingested and published.

??? success "Click to Reveal Answer"

    You will see a message indicating that the wis2box already published this data:

    ```bash
    ERROR - Data already published for geps_202508180000-grib2; not publishing
    ``` 
    
    This demonstrates that the data workflow was triggered, but the data was not re-published. The wis2box will not publish the same data twice. 

### Ingest & Publish using synop2bufr-plugin

Download the synop sample data [synop_202502040900.txt](../sample-data/synop_202502040900.txt) for this exercise in your local environment:

As in the previous exercises, create a directory under the wis2box-incoming bucket that matches the Metadata Identifier of your surface-based-observations/synop dataset.

Enter the newly created directory, click `Upload`, and select the [synop_202502040900.txt](../sample-data/synop_202502040900.txt) you downloaded to your local machine before and then upload.

!!! question "Question"

    Can you successfully publish data notification messages through MinIO? 
    Check the Grafana dashboard and MQTT Explorer to see if the data was successfully ingested and published.

??? success "Click to Reveal Answer"

    No. 
    In the Grafana Dashboard you will see a warning indicating that missing station 64400 record:

    ```bash
    WARNING - Station 64400 not found in station file
    ``` 
    
    This demonstrates that the data workflow was triggered, but a specific station metadata is needed. 

In this case, you are using the `FM-12 data converted to BUFR` plugin.

The purpose of this plugin is to handle FM-12 data provided in plain text format and convert it into binary BUFR.
During this process, the plugin needs to parse and map the station information contained in the data.

If essential station metadata is missing, the plugin cannot parse the file correctly and the conversion will fail.

Therefore, you must ensure that the relevant station metadata has been added to wis2box before publishing SYNOP data.

So now, let add a test station for this exercise.
    
Add the station with WIGOS identifier `0-20000-0-64400` to your wis2box instance using the station editor in the wis2box-webapp.

Retrieve the station from OSCAR:

<img alt="oscar-station" src="/../assets/img/webapp-test-station-oscar-search.png" width="600">

Add the station to the datasets you created for publishing on "../surface-based-observations/synop" and save the changes using your authentication token:

<img alt="webapp-test-station" src="/../assets/img/webapp-test-station-save.png" width="800">

Note that you can remove this station from your dataset after the practical session.

After finishing configuring the station metadata, check with MQTT Explorer to confirm that the data was published successfully. If you see the notification below then you publish the synop sample data successfully.

<img alt="webapp-test-station" src="/../assets/img/mqtt-explorer-wis2box-notification-synop-sample.png" width="800">

## Ingesting data using Python (optional)

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

## Ingesting data over SFTP (optional)

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


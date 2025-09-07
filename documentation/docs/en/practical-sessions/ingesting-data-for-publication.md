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

Note that wis2box will transform the example data into BUFR format before publishing it to the MQTT broker, as per the data mappings pre-configured in your dataset. For this exercise, we will focus on the different methods to upload data to your wis2box instance and verify successful ingestion and publication. Data transformation will be covered later in the [Data Conversion Tools](./data-conversion-tools.md) practical session.

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

### Prepare Example Data

Copy the directory `exercise-materials/data-ingest-exercises` to the directory you defined as the `WIS2BOX_HOST_DATADIR` in your `wis2box.env` file:

```bash
cp -r ~/exercise-materials/data-ingest-exercises ~/wis2box-data/
```

!!! note
    The `WIS2BOX_HOST_DATADIR` is mounted as `/data/wis2box/` inside the wis2box-management container by the `docker-compose.yml` file included in the `wis2box` directory.
    
    This allows you to share data between the host and the container.

## Ingesting data using the MinIO Interface

Firstly, we will use the MinIO web interface, which allows you to download and upload data to MinIO using a web browser.

### Accessing the MinIO Interface

Open the MinIO web interface (usually available at http://your-localhost:9001).

The credentials WIS2BOX_STORAGE_USERNAME and WIS2BOX_STORAGE_PASSWORD can be found in the wis2box.env file.

### Ingest & Publish using Universal plugin 

Download the universal sample data for this exercise from the link below in your local environment:
[sample-data-for-universal-plugin](../sample-data/Z_NAFP_C_BABJ_20250818000000_P_CMA-GEPS-GLB-024.grib2)

Select the bucket wis2box-incoming and click Create new path. The directory name must correspond to the Metadata Identifier of your "other" dataset, which you previously created in the [Configuring Datasets in wis2box](./configuring-wis2box-datasets.md) practical session. So in this case, please create the directory:

```bash
urn:wmo:md:nl-knmi-test:customized-geps-dataset-wis2-training
```

Enter the newly created directory, click "Upload", and select the [sample-data-for-universal-plugin](../sample-data/Z_NAFP_C_BABJ_20250818000000_P_CMA-GEPS-GLB-024.grib2) you downloaded to your local machine before

After uploading, check with MQTT Explorer to confirm that the data was published successfully.

<img alt="Metadata Editor: title, description, keywords" src="/../assets/img/mqtt-explorer-wis2-notification-geps-sample.png" width="800">

!!! question "Rename the file to sample-geps-data.grib2"

    Upload the renamed file using the web interface to the same path in MinIO as the previous file.

    Will the renamed file be published successfully? Why or why not?

??? success "Click to Reveal Answer"

    No, because when you change the data name to "sample-geps-data.grib2", then it will not follow the regex rule.

    <img alt="Metadata Editor: title, description, keywords" src="/../assets/img/mqtt-explorer-wis2-notification-geps-regex-error.png" width="800">
    
    When uploading data, file names must comply with the required naming convention defined by a regular expression:

    ```bash
    ^.*?_(\d{8}).*?\..*$
    ```

    This pattern enforces that each file name contains:

    An underscore (_), followed immediately by an 8-digit date string in the format YYYYMMDD (for example, 20250904).

    For example, the following names are valid:

    1. *Z_NAFP_C_BABJ_20250904_P_CMA-GEPS-GLB-024.grib2*

    2. *forecast_20250904.grib2*

    3. *sample-geps_20250101_data.grib2*

    A name such as sample-geps-data.grib2 will not be accepted, because it does not contain the required 8-digit date.

!!! question "Rename the file extension from .grib2 to .bufr4 (without changing the file’s internal content)"

    Upload the renamed file using the web interface to the same path in MinIO as the previous file.

    Will the renamed file be published successfully? Why or why not?

??? success "Click to Reveal Answer"

    No, because when you change the data format from "grib2" to "bufr4", then it will not follow the file extension rule you defined when you create that dataset.

    <img alt="Metadata Editor: title, description, keywords" src="/../assets/img/mqtt-explorer-wis2-notification-geps-file-extension-error.png" width="800">
    
    When uploading data using the Universal plugin, the file must have the correct file extension as defined in the dataset configuration. This requirement ensures that the ingestion process can correctly recognize and handle the file format. For example, if the dataset is configured for grib2 files, only files ending with .grib2 will be accepted. Using an incorrect extension (e.g., .txt or .bin) will cause the file to be rejected and not published.

!!! question "Re-upload Data Using the MinIO Web Interface"

    Go to the MinIO web interface in your browser and browse to the `wis2box-incoming` bucket. You will see the file `sZ_NAFP_C_BABJ_20250818000000_P_CMA-GEPS-GLB-024.grib2` you uploaded in the previous exercises.

    Click on the file, and you will have the option to download it:

    <img alt="minio-wis2box-incoming-dataset-folder" src="/../assets/img/minio-download.png" width="800">

    You can download this file and re-upload it to the same path in MinIO to re-trigger the wis2box workflow.

    Check the Grafana dashboard and MQTT Explorer to see if the data was successfully ingested and published.

??? success "Click to Reveal Answer"

    You will see a message indicating that the wis2box already published this data:

    ```bash
    ERROR - Data already published for Z_NAFP_C_BABJ_20250818000000_P_CMA-GEPS-GLB-024-grib2; not publishing
    ``` 
    
    This demonstrates that the data workflow was triggered, but the data was not re-published. The wis2box will not publish the same data twice. 

### Ingest & Publish using synop2bufr-plugin

Download the synop sample data [synop_202502040900.txt](../sample-data/synop_202502040900.txt) for this exercise from the link below in your local environment:

Select the bucket wis2box-incoming and click Create new path. The directory name must correspond to the Metadata Identifier of your "surface-based-observations/synop" dataset, which you previously created in the [Configuring Datasets in wis2box](./configuring-wis2box-datasets.md) practical session. So in this case, please create the directory:

```bash
urn:wmo:md:nl-knmi-test:synop-dataset-wis2-training
```

Enter the newly created directory, click "Upload", and select the [synop_202502040900.txt](../sample-data/synop_202502040900.txt) you downloaded to your local machine before and then upload.

!!! question "Did you receive a new notification indicating that the data was published? Why?"

??? success "Click to Reveal Answer"

    No. In the Grafana Dashboard you will see an error indicating that ingestion failed:

    <img alt="grafana_data_ingest" src="/../assets/img/grafana_data-ingest-error.png" width="800"> 

    When using the synop dataset template with the default synop plugins (for CSV, TXT, and BUFR SYNOP data), each record must include a valid station identifier. Ingest fails if the station is not known to your wis2box instance. Therefore, you must add the station first before publishing SYNOP data.

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


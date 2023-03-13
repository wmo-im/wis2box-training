---
title: Data ingest and monitoring
---

# Data ingest and monitoring

## Introduction

In this session you will learn various ways to ingest data into your wis2box and learn how you can monitor if your data is being ingested without errors.

Note that the starting point for wis2box workflow is the MinIO container publishing a message on the `wisbox-storage/#` topic on the local broker.

## Preparation

!!! note
    Before starting please login to your student VM and ensure your wis2box is started and all services are up:

    ```bash
    python3 wis2box-ctl.py start
    python3 wis2box-ctl.py status
    ```

### Verify data mappings

Ensure you are logged into the wis2box-management container on your student VM:

```bash
python3 wis2box-ctl.py login
```

Open your data mappings file:

```bash
vi $WIS2BOX_DATA_MAPPINGS
```

Verify the topic hierarchy and plugin type that was updated [previously](configuring-data-mappings.md).

### Verify discovery metadata

Open the discovery metadata file created [previously](configuring-data-mappings.md) and verify that the values
in the `wis2box` section are consistent with the topic defined in your data mappings.

### Verify station metadata

Open the station metadata file updated [previously](configuring-station-metadata.md) and verify that the values
in the `wis2box` section are consistent with the topic defined in your data mappings.

### Restart and verify wis2box status

For good measure, restart to ensure that the data mappings are registered.  

Restart the **wis2box-management** container with the following command:

```bash
python3 wis2box-ctl.py restart wis2box-management
python3 wis2box-ctl.py status
```

## Open the Grafana dashboard

Please ensure you have opened the Grafana dashboard home-page at http://<your-host>:3000

<img alt="grafana-homepage" src="../../assets/img/grafana-homepage.png" width="600">

!!! question

    Can you see all the stations you have configured in the panel on the left hand side ?

    Are there any errors reported so far?

    Have there been any WIS2 notifications published so far? 

Keep a browser-tab open with the Grafana dashboard during the next few exercises to monitor the status of your data publishing.

## Upload your data

You can use multiple methods to ingest data into wis2box and start publishing WIS2-notifications. 

It is recommended to test your configuration is setup correctly by ingesting a single data-sample manually before setting up automatic ingestion of your data.

Manual ingestion can be done using the `MinIO` admin interface to upload a file into the `wis2box-incoming`-bucket or by using the `wis2box data ingest`-command inside the `wis2box-management container`.

When automating ingesting you can use scripts to copy data into the `wis2box-incoming`-bucket at regular intervals or you can use the optional wis2box-ftp.

!!! note

    Uploading data to MinIO or via the command automatically triggers data ingest and publishing.

### MinIO admin interface

Open your web browser and navigate to the MinIO admin interface of of your student VM (`http://<your-host>:9000`):

User the username and password that are specified in your wis2box environment:

```bash
echo $MINIO_ROOT_USER
echo $MINIO_ROOT_PASSWORD
```

Navigate to the **wis2box-incoming** bucket:

<img alt="minio-admin-buckets" src="../../assets/img/minio-admin-buckets.png" width="600">

Click the **Create new path** button:

<img alt="minio-admin-create-new-path" src="../../assets/img/minio-admin-create-new-path.png" width="600">

Enter the topic hierarchy value of your dataset as a directory.

!!! tip

    Ensure that you replace all periods (`.`) with slashes (`/`).  For example, the topic hierarchy value:

    `mwi.mwi_met_centre.data.core.weather.surface-based-observations.synop`

    should be entered as:

    `mwi/mwi_met_centre/data/core/weather/surface-based-observations/synop`.

It's time to upload your data to the new path!  Click the **Upload** button to add a file or folder to MinIO:

<img alt="minio-admin-create-new-path" src="../../assets/img/minio-admin-create-new-path.png" width="600">

### wis2box-management command line

If you prefer, you can manually trigger the data ingestion action using the wis2box-management command line. 

Ensure your data is available in a directory inside the directory defined by `$WIS2BOX_HOST_DATADIR` in your `dev.env` on your student VM.  You will then be able to access your access your data when logged into the **wis2box-management** container as follows:

```bash
wis2box data ingest --topic-hierarchy mwi.mwi_met_centre.data.core.weather.surface-based-observations.synop --path $WIS2BOX_DATADIR/my-data-directory`
```

!!! tip

    For the topic hierarchy, use the value as defined for `topic_hierarchy:` in your discovery metadata file.

    You do not have to adjust the topic hierarchy (i.e. replacing periods to slashes) when using the **wis2box-management** command line.

### Ingesting data using python

This will be an example of how to ingest data using python. A sample-script will be provided and the participant is required to correctly define the path for their data, the topic, and the wis2box connection details.

### Ingesting data using the optional FTP-server

This will be an example of how to start the optional wis2box-ftp service. The participant will need to start the service and define the correct directory-structure on their ftp-server for their data to successfully ingest data. 

### Viewing data in the WIS2BOX-UI

Open your web browser and navigate to `http://<your-host>.  You should see a dataset with same title as you configured
in your discovery metadata configuration.  Click the **EXPLORE** button.

TODO add screenshots, add exercise

## Conclusion

!!! success "Congratulations!"
    In this practical session, you learned how to:

    - prepare and verify your data mappings, discovery metadata, and station metadata
    - trigger the wis2box workflow using different data ingestion methods
    - monitor the status of your data ingest and publishing
    - view your data on the wis2box UI

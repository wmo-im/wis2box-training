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

Ensure you are logged into the **wis2box-management** container on your student VM:

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

Ensure you have opened the Grafana dashboard home-page at `http://<your-host>:3000`

<img alt="grafana-homepage" src="../../assets/img/grafana-homepage.png" width="600">

!!! question

    Can you see all the stations you have configured in the panel on the left hand side?

    Are there any errors reported so far?

    Have there been any WIS2 notifications published so far? 

Keep a web browser tab open with the Grafana dashboard during the next few exercises to monitor the status of your data publishing.

## Ingesting your data into the wis2box

You can use multiple methods to ingest data into wis2box and start publishing notifications to WIS2.

It is recommended to test your configuration is setup correctly by ingesting a single data-sample manually before setting up automatic ingestion of your data.

Manual ingestion can be done using the `MinIO` admin interface to upload a file into the `wis2box-incoming` bucket or by using the `wis2box data ingest` command from within the **wis2box-management** container.

When automating data ingest you can also use scripts to copy data into the `wis2box-incoming` bucket at regular intervals or you can use the optional **wis2box-ftp** container setup (more on this later).

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

### MinIO Python client

At some point you may want to automate data ingestion from your system into the wis2box using Python.

MinIO provides a Python client which can be installed as follows:

```bash
pip3 install minio
```

Login to your student VM and you will note that this library should already be installed.

Go to the directory `exercise-materials/wis2box-setup` and view the example script:

Run the script using the following command:

```bash 
python3 example/scripts/copy_to_incoming.py
```

!!! question
    The sample script needs to be modified before it can be used.  Why did the script fail?

The script needs to know the correct endpoint for accessing MinIO on your wis2box. If wis2box is running on your host, the MinIO endpoint is available at `http://<your-host>:9000`.

The sample script provides the basic structure for copying a file into MinIO. Try to ingest a data sample of your choosing using this script.

!!! question 
    Use the Python example provided to create your own Python script to ingest data into your wis2box.  What is the correct topic for your data?  Are you able to detect new WIS2 notification on the Grafana dashboard? If not, try to understand the errors and adjust the script accordingly.

### wis2box FTP

You can add an additional service to allow your data to be accessible over FTP.

To define the FTP username and password, add the following additional environment variables to your `dev.env`:

```bash
FTP_USER=wis2box
FTP_PASSWORD=wis2box123
```

Then start the `wis2box-ftp` service with the following command:

```bash
docker-compose -f docker-compose.wis2box-ftp.yml -p wis2box_project --env-file dev.env up -d
```

Now open WinSCP on your local laptop and prepare the connection to the **wis2box-ftp** container as follows:

<img alt="winscp-new-session" src="../../assets/img/winscp-new-session.png" width="400">

Replace "Host name" with that of **your** student VM and use the username and password for the FTP you specified in your `dev.env`.

Once you have established the connection you will land in an empty directory. 

Select the option to create a 'new directory':

<img alt="winscp-empty" src="../../assets/img/winscp-empty.png" width="500">

Enter the topic hierarchy value of your dataset as a directory:

<img alt="winscp_wis2box-ftp_example" src="../../assets/img/winscp-example.png" width="400">

Now enter the directory you created and you can copy your data sample from your host machine to trigger the wis2box data ingest.

Check your Grafana dashboard.

!!! Question

    Did you manage to successfully publish WIS2 notifications for your data?

    If not, review the errors reported and try to determine what went wrong.

### Viewing data in the WIS2BOX-UI

Open your web browser and navigate to `http://<your-host>`.  You should see a dataset with same title as you configured
in your discovery metadata configuration.  Click the **EXPLORE** button.

TODO add screenshots, add exercise

## Conclusion

!!! success "Congratulations!"
    In this practical session, you learned how to:

    - prepare and verify your data mappings, discovery metadata, and station metadata
    - trigger the wis2box workflow using different data ingest methods
    - monitor the status of your data ingest and publishing
    - view your data on the wis2box UI

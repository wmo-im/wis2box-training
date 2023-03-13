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

    Ensure you are logged into the wis2box-management container on your student VM:

    ```bash
    python3 wis2box-ctl.py login
    ```

## Verify data mappings

Open your data mappings file:

```bash
vi $WIS2BOX_DATA_MAPPINGS
```

Verify the topic hierarchy and plugin type that was updated [previously](configuring-data-mappings.md).

## Verify discovery metadata

Open the discovery metadata file created [previously](configuring-data-mappings.md) and verify that the values
in the `wis2box` section are consistent with the topic defined in your data mappings.

## Verify station metadata

Open the station metadata file updated [previously](configuring-station-metadata.md) and verify that the values
in the `wis2box` section are consistent with the topic defined in your data mappings.

## Restart and verify wis2box

For good measure, we want to ensure that the data mappings are registered.  Restart the **wis2box-management** container:

```bash
python3 wis2box-ctl.py restart wis2box-management
```

## Upload your data

Choose one of the options of data upload to wis2box

!!! note

    Uploading data to MinIO or via the command automatically triggers data ingest and publishing.

### MinIO

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

If you prefer, upload your data using the wis2box-management command line. Ensure your data is in the `$WIS2BOX_DATADIR`
directory that is defined in `dev.env` in your student VM.  You will then be able to see this directory when logged into
the **wis2box-management** container.

```bash
wis2box data ingest --topic-hierarchy mwi.mwi_met_centre.data.core.weather.surface-based-observations.synop --path $WIS2BOX_DATADIR/my-data-directory`
```

!!! tip

    You do not have to adjust the topic hierarchy (i.e. replacing periods to slashes) when using the **wis2box-management** command line.

## Monitoring for errors

TODO

## Verify the data publishing

TODO

### Visualizing your data

Open your web browser and navigate to `http://<your-host>.  You should see a dataset with same title as you configured
in your discovery metadata configuration.  Click the **EXPLORE** button.

TODO

## Conclusion

!!! success "Congratulations!"
    In this practical session, you learned how to:

    - prepare and verify your data mappings, dicovery metadta, and station metadata
    - ingest and publish your data
    - monitoring the status of your data ingest and publishing
    - visualize your data on the wis2box API

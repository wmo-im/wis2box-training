---
title: Automating data ingestion
---

# Data ingest and monitoring

!!! abstract "Learning outcomes"

    By the end of this practical session, you will be able to:
    
    - view the WIS2 notifications published by your wis2box
    - check the content of the data being published

## Introduction

The **wis2box-management** container listens to events from the MinIO storage service to trigger data ingestion based on the configuration of ``data-mappings.yml``. This allows you to upload data into MinIO and have wis2box automatically ingest and publish data in real-time.

For the purpose of next few exercises we will use the MinIO admin interface to upload data into MinIO. 

The same steps can be done programmatically by using any MinIO or S3 client software, allowing you to automate your data ingestion as part of your operational workflows.

## Preparation

We will the test dataset you created in the previous session to ingest data into your wis2box.

Make sure you have a web browser open with the Grafana dashboard for your instance by going to `http://<your-host>:3000`

<img alt="grafana-homepage" src="../../assets/img/grafana-homepage.png" width="800">

And make sure you have a second tab open with the MinIO user interface at `http://<your-host>:9001`. Remember you need to login with the `WIS2BOX_STORAGE_USER` and `WIS2BOX_STORAGE_PASSWORD` defined in your `wis2box.env` file:

<img alt="minio-second-tab" src="../../assets/img/minio-second-tab.png" width="800">

## Ingesting some data

Download the following sample data files to your local machine:

[aws-example.csv](/sample-data/aws-example.csv)

Now go back to MinIO in your web browser and navigate to the `wis2box-incoming` bucket and click 'Create new path' to create the following directory:

`xyz/test/data/core/weather/surface-based-observations/synop`

<img alt="minio-admin-create-new-path" src="../../assets/img/minio-admin-create-new-path.png" width="800">

Upload the file `aws-example.csv` to the directory you just created:

<img alt="minio-admin-uploaded-file" src="../../assets/img/minio-admin-uploaded-file.png" width="800">

!!! question "Exercise 1: check for errors"
    Do you see any errors reported on the Grafana dashboard?

??? success "Click to reveal answer"
    The 'wis2box ERRORs' displayed at the bottom of the Grafana home dashboard should report the following error:    
    
    * `ERROR - handle() error: Topic Hierarchy validation error: No plugins for http://minio:9000/wis2box-incoming/xyz/test/data/core/weather/surface-based-observations/synop/aws-example.csv in data mappings. Did not match any of the following: ...`

    Note, the `data` definition in `data-mappings.yml` uses `.` instead of `/` to separate the path elements.
    However the path using `.` in the `data-mappings.yml` and `/` in MinIO are equivalent.

    If there are no data mappings defined for the directory that received the data, wis2box will not initiate any workflow.

!!! question "Exercise 2: correct your input path and repeat the data ingest"

    Go back to MinIO to the root of the `wis2box-incoming` bucket. Then click 'Create new path' and define the correct path for wis2box. For example if your country code is `idn` and your centre-id is `bmkg`, you should create the following path:

    * `idn/bmkg/data/core/weather/surface-based-observations/synop`
    
    Now upload the sample data file `aws-example.csv` to the new path. Do you see any errors reported on the Grafana dashboard?

??? success "Click to reveal answer"
    The Grafana dashboard should report the following errors:

    * ... {/app/wis2box/data/csv2bufr.py:98} ERROR - Station 0-20000-0-60360 not in station list; skipping
    * ... {/app/wis2box/data/csv2bufr.py:98} ERROR - Station 0-20000-0-60355 not in station list; skipping
    * ... {/app/wis2box/data/csv2bufr.py:98} ERROR - Station 0-20000-0-60351 not in station list; skipping

    As the stations in the test data are not defined in your wis2box metadata, the data ingest workflow will not be triggered.

    If instead you again see the error `Topic Hierarchy validation error: No plugins for ... in data mappings`, check that you have defined the correct path in MinIO and repeat the data ingest.

!!! question "Exercise 3: add the test stations and repeat the data ingest"

    Add the following stations to your wis2box using the station editor in **wis2box-webapp**:

    - 0-20000-0-60351
    - 0-20000-0-60355
    - 0-20000-0-60360

    Now re-upload the sample data file `aws-example.csv` to the same path in MinIO you used in the previous exercise.

    Check the Grafana dashboard, are there any new errors ? How can you see that the test data was successfully ingested and published?

??? success "Click to reveal answer"

    If you were subscribed with MQTT Explorer to your **wis2box-broker**, you should have received notifications for the test data when the data was successfully published.

    You can also check the charts on the Grafana home dashboard to see if the test data was successfully ingested and published.

    <img alt="grafana_success" src="../../assets/img/grafana_success.png" width="800">

    The chart "Number of WIS2.0 notifications published by wis2box" indicates that notifications were successfully published on the MQTT broker in wis2box.

## Viewing the data you have published

You can use the **wis2box-webapp** to view the WIS2 notifications that have been published by your wis2box and inspect the content of the data that was published.

## Conclusion

!!! success "Congratulations!"
    In this practical session, you learned how to:

    - trigger wis2box workflow using different data ingest methods
    - monitor the status of your data ingest and publishing

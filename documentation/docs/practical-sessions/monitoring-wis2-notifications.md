---
title: Monitoring WIS2 Notifications
---

# Monitoring WIS2 Notifications 

!!! abstract "Learning outcomes"

    By the end of this practical session, you will be able to:
    
    - trigger the wis2box workflow by uploading data in MinIO
    - view warnings and errors displayed in the Grafana dashboard
    - check the content of the data being published

## Introduction

The **Grafana dashboard** uses data from Prometheus and Loki to display the status of your wis2box. Prometheus store time-series data from the metrics collected, while Loki store the logs from the containers running on your wis2box-instance. This data allows you to check how much data is received on MinIO and how many WIS2 notifications are published, and if there are any errors detected in the logs.

To see the content of the WIS2-notifications that are being published on different topics of your wis2box you can use the 'Monitor' tab in the **wis2box-webapp**.

## Preparation

This section will use the datasets previously created in the [Configuring datasets in wis2box](/practical-sessions/configuring-wis2box-datasets) practical session. 

Login to you student VM using your SSH client (PuTTY or other).

Make sure wis2box is up and running:

```bash
cd ~/wis2box-1.0b8/
python3 wis2box-ctl.py start
python3 wis2box-ctl.py status
```

Make sure your have MQTT Explorer running and connected to your instance.
If you are still connected from the previous session, clear any previous messages you may have received from the queue by disconnecting and reconnecting.

Make sure you have a web browser open with the Grafana dashboard for your instance by going to `http://<your-host>:3000`

<img alt="grafana-homepage" src="../../assets/img/grafana-homepage.png" width="800">

And make sure you have a second tab open with the MinIO user interface at `http://<your-host>:9001`. Remember you need to login with the `WIS2BOX_STORAGE_USER` and `WIS2BOX_STORAGE_PASSWORD` defined in your `wis2box.env` file:

<img alt="minio-second-tab" src="../../assets/img/minio-second-tab.png" width="800">

## Ingesting some data


Download the following sample data files to your local machine:

[aws-example.csv](/sample-data/aws-example.csv)

Access the MinIO console in your web browser and navigate to the `wis2box-incoming` bucket and click 'Create new path' to create the following directory:

`not-my-centre/data/core/weather/surface-based-observations/synop`

<img alt="minio-admin-create-new-path" src="../../assets/img/minio-admin-create-new-path.png" width="800">

Upload the file `aws-example.csv` to the directory you just created:

<img alt="minio-admin-uploaded-file" src="../../assets/img/minio-admin-uploaded-file.png" width="800">

!!! question "Exercise 1: check for errors"
    Do you see any errors reported on the Grafana dashboard?

??? success "Click to reveal answer"
    The 'wis2box ERRORs' displayed at the bottom of the Grafana home dashboard should report the following error:    
    
    * `ERROR - Path validation error: Could not match http://minio:9000/wis2box-incoming/not-my-centre/data/core/weather/surface-based-observations/synop/aws-example.csv to dataset, path should include one of the following:: ...`

    This error indicates that the wis2box-management container could not match the path of the uploaded file to a dataset configured in your wis2box-instance.

!!! question "Exercise 2: correct your input path and repeat the data ingest"

    Go back to MinIO to the root of the `wis2box-incoming` bucket. Then click 'Create new path' and define the correct path for wis2box by replacing 'not-my-centre' with the centre-id you used when creating the dataset in the previous practical session. For example, if your centre-id is `fr-meteofrance`, the path should be:

    * `fr-meteofrance/data/core/weather/surface-based-observations/synop`
    
    Now upload the sample data file `aws-example.csv` to the new path. Do you see any errors reported on the Grafana dashboard?

??? success "Click to reveal answer"
    The Grafana dashboard should report the following warnings:

    * ... WARNING - input=aws-example.csv warning=Station 0-20000-0-60360 not in station list; skipping
    * ... WARNING - input=aws-example.csv warning=Station 0-20000-0-60355 not in station list; skipping
    * ... WARNING - input=aws-example.csv warning=Station 0-20000-0-60351 not in station list; skipping

    As the stations in the test data are not defined in your wis2box metadata, the data ingest workflow will not be triggered.

    If instead you still see the error `ERROR - Path validation error: Could not match ...`, check that you have defined the correct path in MinIO and repeat the data ingest until you see the warnings above.

!!! question "Exercise 3: add the test stations and repeat the data ingest"

    Add the following stations to your wis2box using the station editor in **wis2box-webapp**:

    - 0-20000-0-60351
    - 0-20000-0-60355
    - 0-20000-0-60360

    And associate them with the topic for your dataset.

    Now re-upload the sample data file `aws-example.csv` to the same path in MinIO you used in the previous exercise.

    Check the Grafana dashboard, are there any new errors or warnings ? How can you see that the test data was successfully ingested and published?

??? success "Click to reveal answer"

    You can check the charts on the Grafana home dashboard to see if the test data was successfully ingested and published.

    <img alt="grafana_success" src="../../assets/img/grafana_success.png" width="800">

    The chart "Number of WIS2.0 notifications published by wis2box" indicates that notifications were successfully published on the MQTT broker in wis2box.

    Also, if you were subscribed with MQTT Explorer to your **wis2box-broker**, you should have received WIS2 notifications for the test data when the data was successfully published.

## Viewing the data content you have published

You can use the **wis2box-webapp** to view the content of the WIS2 data notifications that have been published by your wis2box.

Open the **wis2box-webapp** in your browser by navigating to `http://<your-host>/wis2box-webapp` and select the 'Monitor' tab:

<img alt="wis2box-webapp-monitor" src="../../assets/img/wis2box-webapp-monitor.png" width="220">

In the monitoring-tab select to the topic hierarchy for your dataset and click "UPDATE"

??? question "Exercise 4: view the WIS2 notifications"
    
    How many WIS2 data notifications were published by your wis2box? 

    What is the air-temperature that was measured at the station with the WIGOS-identifier=0-20000-0-60351?

??? success "Click to reveal answer"

    If you have successfully ingested the test data, you should see 3 WIS2 data notifications published by your wis2box.

    To see the air-temperature measured for the station with WIGOS-identifier=0-20000-0-60351, click on the "INSPECT"-button next to the file for that station to open a pop-up window displaying the parsed content of the data file. The air-temperature measured at this station was 25.0 degrees Celsius.

## Conclusion

!!! success "Congratulations!"
    In this practical session, you learned how to:

    - view the WIS2 notifications published by your wis2box
    - check the content of the data being published

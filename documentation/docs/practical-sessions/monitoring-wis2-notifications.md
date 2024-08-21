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

This section will use the "surface-based-observations/synop" dataset previously created in the [Configuring datasets in wis2box](/practical-sessions/configuring-wis2box-datasets) practical session. 

Login to you student VM using your SSH client (PuTTY or other).

Make sure wis2box is up and running:

```bash
cd ~/wis2box-1.0b8/
python3 wis2box-ctl.py start
python3 wis2box-ctl.py status
```

Make sure your have MQTT Explorer running and connected to your instance using the public credentials `everyone/everyone` with a subscription to the topic `origin/a/wis2/#`.

Make sure you have a web browser open with the Grafana dashboard for your instance by going to `http://<your-host>:3000`

<img alt="grafana-homepage" src="../../assets/img/grafana-homepage.png" width="800">

## Ingesting some data

Copy the sample data file `aws-example.csv` to the the directory you defined as the WI2BOX_HOST_DATADIR in your `wis2box.env` file.

```bash
cp ~/exercise-materials/monitoring-exercise/aws-example.csv ~/wis2box-data
```

Make sure you are in the `wis2box-1.0b8` directory and login to the **wis2box-management** container:

```bash
cd ~/wis2box-1.0b8
python3 wis2box-ctl.py login
```

From the wis2box command line we can ingest the sample data file `aws-example.csv` into a specific dataset as follows:

```bash
wis2box data ingest -p /data/wis2box/aws-example.csv --metadata-identifier urn:wmo:md:not-my-centre:surface-based-observations.synop
```

!!! note
    The `WIS2BOX_HOST_DATADIR` is mounted as `/data/wis2box/` inside the wis2box-management container by the docker-compose.yml file included in the wis2box-1.0b8 directory.
    
    This allows you to share data between the host and the container.

Go to the Grafana dashboard in your browser and check the status of the data ingest.

!!! question "Exercise 1: check for errors"
    Do you see any errors reported on the Grafana dashboard?

??? success "Click to reveal answer"
    The 'wis2box ERRORs' displayed at the bottom of the Grafana home dashboard should report the following error:    
    
    * `ERROR - Path validation error: Could not match http://minio:9000/wis2box-incoming/urn:wmo:md:not-my-centre:surface-based-observations.synop/aws-example.csv to dataset, path should include one of the following:: ...`

    This error indicates that the wis2box-management container could not match the path of the uploaded file to a dataset configured in your wis2box-instance.

!!! question "Exercise 2: correct your input path and repeat the data ingest"

    Find the correct metadata identifier for the dataset you created in the previous practical session and repeat the data ingest command with the correct path.

??? success "Click to reveal answer"

    If you provided the correct metadata identifier for the dataset you created in the previous practical session, the Grafana dashboard should report the following warnings:

    * ... WARNING - input=aws-example.csv warning=Station 0-20000-0-60360 not in station list; skipping
    * ... WARNING - input=aws-example.csv warning=Station 0-20000-0-60355 not in station list; skipping
    * ... WARNING - input=aws-example.csv warning=Station 0-20000-0-60351 not in station list; skipping

    As the stations in the test data are not defined in your wis2box metadata, the data ingest workflow will not be triggered.

    If instead you still see the error `ERROR - Path validation error: Could not match ...`, check that you have defined the correct metadata identifier and repeat the data ingest command.

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

!!! question "Exercise 4: check the MQTT broker for WIS2 notifications"
    
    Go to the MQTT Explorer and check if you can see the WIS2 Notification Message for the data you just ingested.
    
    How many WIS2 data notifications were published by your wis2box?
    
    How do you access the content of the data being published?

??? success "Click to reveal answer"

    You should see 3 WIS2 data notifications published by your wis2box.

    To access the content of the data being published, you can expand the topic structure to see the different levels of the message until you reach the last level and review message content of one of the messages.

    The message content has a "links" section with a "rel" key of "canonical" and a "href" key with the URL to download the data. The URL will be in the format `http://<your-host>/data/...`. 
    
    The web-proxy service in the wis2box-stack has proxied '/data' to the "wis2box-public" bucket in MinIO, providing a public HTTP endpoint to download the data.

## Viewing the data content you have published

You can use the **wis2box-webapp** to view the content of the WIS2 data notifications that have been published by your wis2box.

Open the **wis2box-webapp** in your browser by navigating to `http://<your-host>/wis2box-webapp` and select the 'Monitor' tab:

<img alt="wis2box-webapp-monitor" src="../../assets/img/wis2box-webapp-monitor.png" width="220">

In the monitoring-tab select to the topic hierarchy for your dataset and click "UPDATE"

??? question "Exercise 5: view the WIS2 notifications in the wis2box-webapp"
    
    How many WIS2 data notifications were published by your wis2box? 

    What is the air-temperature that was measured at the station with the WIGOS-identifier=0-20000-0-60351?

??? success "Click to reveal answer"

    If you have successfully ingested the test data, you should see 3 WIS2 data notifications published by your wis2box.

    To see the air-temperature measured for the station with WIGOS-identifier=0-20000-0-60351, click on the "INSPECT"-button next to the file for that station to open a pop-up window displaying the parsed content of the data file. The air-temperature measured at this station was 25.0 degrees Celsius.

!!! Note
    The wis2box-api container includes tools to parse BUFR files and display the content in a human-readable format. This is a not a core requirements for the WIS2.0 implementation, but was included in the wis2box to aid data-publishers in checking the content of the data they are publishing.

## Conclusion

!!! success "Congratulations!"
    In this practical session, you learned how to:

    - view the WIS2 notifications published by your wis2box
    - check the content of the data being published

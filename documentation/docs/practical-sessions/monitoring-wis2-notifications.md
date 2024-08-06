---
title: Monitoring WIS2 Notifications
---

# Monitoring WIS2 Notifications

!!! abstract "Learning outcomes"

    By the end of this practical session, you will be able to:
    
    - view the WIS2 notifications published by your wis2box
    - check the content of the data being published

## Introduction

The Grafana dashboard uses data from Prometheus and Loki to display the status of your wis2box. Prometheus store time-series data from the metrics collected, while Loki store the logs from the containers running on your wis2box-instance. This data allows you to check how much data is received on MinIO and how many WIS2 notifications are published, and if there are any errors detected in the logs.

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
If you are still connected from the previous session, clear any previous messages you may have received from the queue.
This can be done by either by disconnecting and reconnecting or by clicking the trash can for the topic.

Make sure you have a web browser open with the Grafana dashboard for your instance by going to `http://<your-host>:3000`

<img alt="grafana-homepage" src="../../assets/img/grafana-homepage.png" width="800">

And make sure you have a second tab open with the MinIO user interface at `http://<your-host>:9001`. Remember you need to login with the `WIS2BOX_STORAGE_USER` and `WIS2BOX_STORAGE_PASSWORD` defined in your `wis2box.env` file:

<img alt="minio-second-tab" src="../../assets/img/minio-second-tab.png" width="800">

## Ingesting some data

work-in-progress, not sure if data ingest is needed for this practical session or we can re-use the data from the previous practical session.

## Viewing the data you have published

You can use the **wis2box-webapp** to view the WIS2 notifications that have been published by your wis2box and inspect the content of the data that was published.

## Conclusion

!!! success "Congratulations!"
    In this practical session, you learned how to:

    - view the WIS2 notifications published by your wis2box
    - check the content of the data being published

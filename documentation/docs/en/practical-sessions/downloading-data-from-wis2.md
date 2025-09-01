---
title: Downloading data from WIS2 using wis2downloader
---

# Downloading data from WIS2 using wis2downloader

!!! abstract "Learning outcomes!"

    By the end of this practical session, you will be able to:

    - use the "wis2downloader" to subscribe to WIS2 data notifications and download data to your local system
    - view the status of the downloads in the Grafana dashboard
    - learn how to configure the wis2downloader to subscribe to a non-default broker

## Introduction

In this session you will learn how to setup a subscription to a WIS2 Broker and automatically download data to your local system using the "wis2downloader"-service included in the wis2box. 

!!! note "About wis2downloader"
     
     The wis2downloader is also available as a standalone service that can be run on a different system from the one that is publishing the WIS2 notifications. See [wis2downloader](https://pypi.org/project/wis2downloader/) for more information for using the wis2downloader as a standalone service.

     If you like to develop your own service for subscribing to WIS2 notifications and downloading data, you can use the [wis2downloader source code](https://github.com/World-Meteorological-Organization/wis2downloader) as a reference.

## Preparation

Before starting please login to your student VM and ensure your wis2box instance is up and running.


## wis2downloader basics

The wis2downloader is included as a separate container in wis2box as defined in the Docker Compose files. The Prometheus container in wis2box is configured to scrape metrics from the wis2downloader container and these metrics can be visualized by a dashboard in Grafana.

### Viewing the wis2downloader dashboard in Grafana

Open a web browser and navigate to the Grafana dashboard for your wis2box instance by going to `http://YOUR-HOST:3000`.

Click on dashboards in the left-hand menu, and then select the **wis2downloader dashboard**.

You should see the following dashboard:

![wis2downloader dashboard](../assets/img/wis2downloader-dashboard.png)

This dashboard is based on metrics published by the wis2downloader service and will show you the status of the downloads that are currently in progress.

On the top left corner you can see the subscriptions that are currently active.

Keep this dashboard open as you will use it to monitor the download progress in the next exercise.

### Reviewing the wis2downloader configuration

The wis2downloader service in wis2box can be configured using the environment variables defined in your `wis2box.env` file.

The following environment variables are used by the wis2downloader:

    - DOWNLOAD_BROKER_HOST: The hostname of the MQTT broker to connect to. Defaults to globalbroker.meteo.fr
    - DOWNLOAD_BROKER_PORT: The port of the MQTT broker to connect to. Defaults to 443 (HTTPS for websockets)
    - DOWNLOAD_BROKER_USERNAME: The username to use to connect to the MQTT broker. Defaults to everyone
    - DOWNLOAD_BROKER_PASSWORD: The password to use to connect to the MQTT broker. Defaults to everyone
    - DOWNLOAD_BROKER_TRANSPORT: websockets or tcp, the transport-mechanism to use to connect to the MQTT broker. Defaults to websockets,
    - DOWNLOAD_RETENTION_PERIOD_HOURS: The retention period in hours for the downloaded data. Defaults to 24
    - DOWNLOAD_WORKERS: The number of download workers to use. Defaults to 8. Determines the number of parallel downloads.
    - DOWNLOAD_MIN_FREE_SPACE_GB: The minimum free space in GB to keep on the volume hosting the downloads. Defaults to 1.

To review the current configuration of the wis2downloader, you can use the following command:

```bash
cat ~/wis2box/wis2box.env | grep DOWNLOAD
```

!!! question "Review the configuration of the wis2downloader"
    
    What is the default MQTT broker that the wis2downloader connects to?

    What is the default retention period for the downloaded data?

??? success "Click to reveal answer"

    The default MQTT broker that the wis2downloader connects to is `globalbroker.meteo.fr`.

    The default retention period for the downloaded data is 24 hours.

!!! note "Updating the configuration of the wis2downloader"

    To update the configuration of the wis2downloader, you can edit the wis2box.env file. To apply the changes you can re-run the start command for the wis2box-stack:

    ```bash
    python3 wis2box-ctl.py start
    ```

    And you will see the wis2downloader service restart with the new configuration.

You can keep the default configuration for the next exercise.

### wis2downloader command line interface

To access the command line interface of the wis2downloader within wis2box, you can login to the **wis2downloader** container using the following command:

```bash
python3 wis2box-ctl.py login wis2downloader
```

Use the following command to list the subscriptions that are currently active:

```bash
wis2downloader list-subscriptions
```

This command returns an empty list, as there are no subscriptions setup yet.

## Download GTS-data using a WIS2 Global Broker

If you kept the default configuration of the wis2downloader, it is currently connected to the WIS2 Global Broker hosted by Météo-France.

### Setup the subscription

Use the following command `cache/a/wis2/de-dwd-gts-to-wis2/#`, to subscribe to data published by the GTS-to-WIS2 gateway hosted by DWD, made available through the Global Caches:

```bash
wis2downloader add-subscription --topic cache/a/wis2/de-dwd-gts-to-wis2/#
```

Then exit the **wis2downloader** container by typing `exit`:

```bash
exit
```

### Check the downloaded data

Check the wis2downloader dashboard in Grafana to see the new subscription added. Wait a few minutes and you should see the first downloads starting. Go to the next exercise once you have confirmed that the downloads are starting.

The wis2downloader service in wis2box downloads the data in the 'downloads' directory in the directory you defined as the `WIS2BOX_HOST_DATADIR` in your `wis2box.env` file. To view the contents of the downloads directory, use the following command:

```bash
ls -R ~/wis2box-data/downloads
```

Note that the downloaded data is stored in directories named after the topic the WIS2 Notification was published on.

!!! question "Viewing the downloaded data"

    What directories do you see in the downloads directory?

    Can you see any downloaded files in these directories?

??? success "Click to reveal answer"
    You should see a directory structure starting with `cache/a/wis2/de-dwd-gts-to-wis2/` underneath which you will see more directories named after the GTS-bulletin headers of the downloaded data.

    Depending on when you started the subscription, you may or may not see any downloaded files in this directory yet. If you do not see any files yet, wait a few more minutes and check again.

Let's cleanup the subscription and the downloaded data before moving to the next exercise.

Log back in to the wis2downloader container:

```bash
python3 wis2box-ctl.py login wis2downloader
```

and remove the subscription you made from the wis2downloader, using the following command:

```bash
wis2downloader remove-subscription --topic cache/a/wis2/de-dwd-gts-to-wis2/#
```

Remove the downloaded data using the following command:

```bash
rm -rf /wis2box-data/downloads/cache/*
```

And exit the wis2downloader container by typing `exit`:
    
```bash
exit
```

Check the wis2downloader dashboard in Grafana to see the subscription removed. You should see the downloads stopping.

!!! note "About GTS-to-WIS2 gateways"
    There are currently two GTS-to-WIS2 gateways currently publishing data through the WIS2 Global Broker and the Global Caches:

    - DWD (Germany): centre-id=*de-dwd-gts-to-wis2*
    - JMA (Japan): centre-id=*jp-jma-gts-to-wis2*
    
    If in the previous exercise you replace `de-dwd-gts-to-wis2` with `jp-jma-gts-to-wis2`, you would receive the notifications and data published by the JMA GTS-to-WIS2 gateway.

!!! note "Origin vs cache topics"

    When subscribing to a topic starting with `origin/`, you will receive notifications with a canonical URL that points to a data server provided by the WIS Centre publishing the data.

    When subscribing to a topic starting with `cache/`, you will receive multiple notifications for the same data, one for each Global Cache. Each notification will contain a canonical URL that points to the data server of the respective Global Cache. The wis2downloader will download the data from the first canonical URL it can reach.

## Download example data from the WIS2 Training Broker

In this exercise, you will subscribe to the WIS2 Training Broker which is publishing example data for training purposes. 

### Change the wis2downloader configuration

This demonstrates how to subscribe to a broker that is not the default broker and will allow you to download some data published from the WIS2 Training Broker.

Edit the `wis2box.env` file and change `DOWNLOAD_BROKER_HOST` to `wis2training-broker.wis2dev.io`, `DOWNLOAD_BROKER_PORT` to `1883` and `DOWNLOAD_BROKER_TRANSPORT` to `tcp`:

```copy
# downloader settings
DOWNLOAD_BROKER_HOST=wis2training-broker.wis2dev.io
DOWNLOAD_BROKER_PORT=1883
DOWNLOAD_BROKER_USERNAME=everyone
DOWNLOAD_BROKER_PASSWORD=everyone
# download transport mechanism (tcp or websockets)
DOWNLOAD_BROKER_TRANSPORT=tcp
```

Then run the 'start' command again to apply the changes:

```bash
python3 wis2box-ctl.py start
```

Check the logs of the wis2downloader to see if the connection to the new broker was successful:

```bash
docker logs wis2downloader
```

You should see the following log message:

```copy
...
INFO - Connecting...
INFO - Host: wis2training-broker.wis2dev.io, port: 1883
INFO - Connected successfully
```

### Setup new subscriptions

Now we will setup a new subscription to the topic to downloaded cyclone track data from the WIS2 Training Broker.

Login to the **wis2downloader** container:

```bash
python3 wis2box-ctl.py login wis2downloader
```

And execute the following command (copy-paste this to avoid typos):

```bash
wis2downloader add-subscription --topic origin/a/wis2/int-wis2-training/data/core/weather/prediction/forecast/medium-range/probabilistic/trajectory
```

Exit the **wis2downloader** container by typing `exit`.

### Check the downloaded data

Wait until you see the downloads starting in the wis2downloader dashboard in Grafana.

Check that the data was downloaded by checking the wis2downloader logs again with:

```bash
docker logs wis2downloader
```

You should see a log message similar to the following:

```copy
[...] INFO - Message received under topic origin/a/wis2/int-wis2-training/data/core/weather/prediction/forecast/medium-range/probabilistic/trajectory
[...] INFO - Downloaded A_JSXX05ECEP020000_C_ECMP_...
```

Check the contents of the downloads directory again:

```bash
ls -R ~/wis2box-data/downloads
```

You should see a new directory named `origin/a/wis2/int-wis2-training/data/core/weather/prediction/forecast/medium-range/probabilistic/trajectory` containing the downloaded data.

!!! question "Review the downloaded data"
    
    What is the file format of the downloaded data?

??? success "Click to reveal answer"

    The downloaded data is in BUFR format as indicated by the `.bufr` file extension. 

Next try to add another two subscriptions to download monthly surface temperature anomalies and global ensemble forecast data from the following topics:

- `origin/a/wis2/int-wis2-training/data/core/weather/prediction/forecast/medium-range/probabilistic/global`
- `origin/a/wis2/int-wis2-training/data/core/climate/experimental/anomalies/monthly/surface-temperature`

Wait until you see the downloads starting in the wis2downloader dashboard in Grafana.

Check the contents of the downloads directory again:

```bash
ls -R ~/wis2box-data/downloads
```

You should see two new directories named `origin/a/wis2/int-wis2-training/data/core/weather/prediction/forecast/medium-range/probabilistic/global` and `origin/a/wis2/int-wis2-training/data/core/climate/experimental/anomalies/monthly/surface-temperature` containing the downloaded data.

!!! question "Review the downloaded data for the two new topics"
    
    What is the file format of the downloaded data for the `../prediction/forecast/medium-range/probabilistic/global` topic?

    What is the file format of the downloaded data for the `../climate/experimental/anomalies/monthly/surface-temperature` topic?

??? success "Click to reveal answer"

    The downloaded data for the `../prediction/forecast/medium-range/probabilistic/global` topic is in GRIB2 format as indicated by the `.grib2` file extension. 

    The downloaded data for the `../climate/experimental/anomalies/monthly/surface-temperature` topic is in NetCDF format as indicated by the `.nc` file extension.

## Conclusion

!!! success "Congratulations!"

    In this practical session, you learned how to:

    - use the 'wis2downloader' to subscribe to a WIS2 Broker and download data to your local system
    - view the status of the downloads in the Grafana dashboard
    - how to change the default configuration of the wis2downloader to subscribe to a different broker
    - how to view the downloaded data on your local system

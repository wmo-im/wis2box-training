---
title: Downloading data from WIS2 notifications
---

# Downloading data from WIS2 notifications

!!! abstract "Learning outcomes!"

    By the end of this practical session, you will be able to:

    - use the "wis2downloader" to subscribe to WIS2 data notifications and download data to your local system.

## Introduction

In this session you will learn how to setup a subscription to a WIS2 Broker and automatically download data to your local system using the "wis2downloader"-service included in the wis2box. 

!!! note "About wis2downlaoder"
     
     The wis2downloader is also available as a standalone service that can be run on a different system from the one that is publishing the WIS2 notifications. See [wis2downloader](https://pypi.org/project/wis2downloader/) for more information for using the wis2downloader as a standalone service.

## Preparation

Before starting please login to your student VM and ensure your wis2box instance is up and running.

## Exercise 1: viewing the wis2download dashboard in Grafana

Open a web browser and navigate to the Grafana dashboard for your wis2box instance by going to `http://<your-host>:3000`.

Click on dashboards in the left-hand menu, and then select the **wis2downloader dashboard**.

You should see the following dashboard:

![wis2downloader dashboard](../assets/img/wis2downloader-dashboard.png)

This dashboard is based on metrics published by the wis2downloader service and will show you the status of the downloads that are currently in progress.

On the top left corner you can see the subscriptions that are currently active.

Keep this dashboard open as you will use it to monitor the download progress in the next exercise.

## Exercise 2: reviewing the wis2downloader configuration

The wis2downloader-service started by the wis2box-stack can be configured using the environment variables defined in your wis2box.env file.

The following environment variables are used by the wis2downloader:

    - DOWNLOAD_BROKER_HOST: The hostname of the MQTT-broker to connect to. Defaults to globalbroker.meteo.fr
    - DOWNLOAD_BROKER_PORT: The port of the MQTT-broker to connect to. Defaults to 443 (HTTPS for websockets)
    - DOWNLOAD_BROKER_USERNAME: The username to use to connect to the MQTT-broker. Defaults to everyone
    - DOWNLOAD_BROKER_PASSWORD: The password to use to connect to the MQTT-broker. Defaults to everyone
    - DOWNLOAD_BROKER_TRANSPORT: websockets or tcp, the transport-mechanism to use to connect to the MQTT-broker. Defaults to websockets,
    - DOWNLOAD_RETENTION_PERIOD_HOURS: The retention period in hours for the downloaded data. Defaults to 24
    - DOWNLOAD_WORKERS: The number of download workers to use. Defaults to 8. Determines the number of parallel downloads.
    - DOWNLOAD_MIN_FREE_SPACE_GB: The minimum free space in GB to keep on the volume hosting the downloads. Defaults to 1.

To review the current configuration of the wis2downloader, you can use the following command:

```bash
cat ~/wis2box-1.0b8/wis2box.env | grep DOWNLOAD
```

??? question "Review the configuration of the wis2downloader"
    
    What is the default MQTT-broker that the wis2downloader connects to?

    What is the default retention period for the downloaded data?

!!! success "Click to reveal the answers"

    The default MQTT-broker that the wis2downloader connects to is `globalbroker.meteo.fr`.

    The default retention period for the downloaded data is 24 hours.

!!! note "Updating the configuration of the wis2downloader"

    To update the configuration of the wis2downloader, you can edit the wis2box.env file. To apply the changes you can re-run the start command for the wis2box-stack:

    ```bash
    python3 wis2box-ctl.py start
    ```

    And you will see the wis2downloader service restart with the new configuration.

You can keep the default configuration for the purpose of this exercise.

## Exercise 3: adding subscriptions to the wis2downloader

Inside the **wis2downloader** container, you can use the command line to list, add and delete subscriptions.

To login to the **wis2downloader** container, use the following command:

```bash
python3 wis2box-ctl.py login wis2downloader
```

Then use the following command to list the subscriptions that are currently active:

```bash
wis2downloader subscriptions list
```

This command returns an empty list since no subscriptions are currently active.

For the purpose of this exercise, we will subscribe to the following topic `cache/a/wis2/de-dwd-gts-to-wis2/#`, to subscribe to data published by the DWD-hosted GTS-to-WIS2 gateway and downloading notifications from the Global Cache.

To add this subscription, use the following command:

```bash
wis2downloader subscriptions add --topic cache/a/wis2/de-dwd-gts-to-wis2/#
```

Check the wis2downloader dashboard in Grafana to see the new subscription added. Wait a few minutes and you should see the first downloads starting. Go to he next exercise once you have confirmed that the downloads are starting.

## Exercise 4: viewing the downloaded data

The wis2downloader-service in the wis2box-stack downloads the data in the 'downloads' directory in the directory you defined as the WIS2BOX_HOST_DATADIR in your wis2box.env file. To view the contents of the downloads directory, you can use the following command:

```bash
ls -l ~/wis2box-data/downloads
```

## Exercise 5: removing subscriptions from the wis2downloader

To remove a subscription from the wis2downloader, you can use the following command:

```bash
wis2downloader subscriptions remove --topic cache/a/wis2/de-dwd-gts-to-wis2/#
```

Check the wis2downloader dashboard in Grafana to see the subscription removed. 

## Conclusion

!!! success "Congratulations!"

    In this practical session, you learned how to:

    - use the 'wis2downloader' to subscribe to a WIS2 Broker and download data to your local system
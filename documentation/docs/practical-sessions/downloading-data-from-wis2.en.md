---
title: Downloading data from WIS2 notifications
---

# Downloading data from WIS2 notifications

!!! abstract "Learning outcomes!"

    By the end of this practical session, you will be able to:

    - use the "wis2downloader" to subscribe to WIS2 data notifications and download data to your local system.

## Introduction

In this session you will learn how to setup a subscription to a WIS2 Broker and automatically download data to your local system using the "wis2downloader"-service included in the wis2box. 

!!! note "About wis2downloader"
     
     The wis2downloader is also available as a standalone service that can be run on a different system from the one that is publishing the WIS2 notifications. See [wis2downloader](https://pypi.org/project/wis2downloader/) for more information for using the wis2downloader as a standalone service.

     If you like to develop your own service for subscribing to WIS2 notifications and downloading data, you can use the [wis2downloader source code](https://github.com/wmo-im/wis2downloader) as a reference.

!!! Other tools for accessing WIS2 data

    The following tools can also be used to discover and access data from WIS2:

    - [pywiscat](https://github.com/wmo-im/pywiscat) provides search capability atop the WIS2 Global Discovery Catalogue in support of reporting and analysis of the WIS2 Catalogue and its associated discovery metadata
    - [pywis-pubsub](https://github.com/wmo-im/pywis-pubsub) provides subscription and download capability of WMO data from WIS2 infrastructure services

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
cat ~/wis2box-1.0b8/wis2box.env | grep DOWNLOAD
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

You can keep the default configuration for the purpose of this exercise.

## Exercise 3: adding subscriptions to the wis2downloader

Inside the **wis2downloader** container, you can use the command line to list, add and delete subscriptions.

To login to the **wis2downloader** container, use the following command:

```bash
python3 wis2box-ctl.py login wis2downloader
```

Then use the following command to list the subscriptions that are currently active:

```bash
wis2downloader list-subscriptions
```

This command returns an empty list since no subscriptions are currently active.

For the purpose of this exercise, we will subscribe to the following topic `cache/a/wis2/de-dwd-gts-to-wis2/#`, to subscribe to data published by the DWD-hosted GTS-to-WIS2 gateway and downloading notifications from the Global Cache.

To add this subscription, use the following command:

```bash
wis2downloader add-subscription --topic cache/a/wis2/de-dwd-gts-to-wis2/#
```

Then exit the **wis2downloader** container by typing `exit`.

Check the wis2downloader dashboard in Grafana to see the new subscription added. Wait a few minutes and you should see the first downloads starting. Go to he next exercise once you have confirmed that the downloads are starting.

## Exercise 4: viewing the downloaded data

The wis2downloader-service in the wis2box-stack downloads the data in the 'downloads' directory in the directory you defined as the WIS2BOX_HOST_DATADIR in your wis2box.env file. To view the contents of the downloads directory, you can use the following command:

```bash
ls -R ~/wis2box-data/downloads
```

Note that the downloaded data is stored in directories named after the topic the WIS2 Notification was published on.

## Exercise 5: removing subscriptions from the wis2downloader

Next, the remove the subscription you made from the wis2downloader, using the following command:

```bash
wis2downloader remove-subscription --topic cache/a/wis2/de-dwd-gts-to-wis2/#
```

Check the wis2downloader dashboard in Grafana to see the subscription removed. You should see the downloads stopping.

## Exercise 6: subscribe to the wis2training-broker and setup a new subscription

For the next exercise we will subscribe to the wis2training-broker.

This demonstrates how to subscribe to a broker that is not the default broker and will allow you to download some data published from the WIS2 Training Broker.

Edit the wis2box.env file and change the DOWNLOAD_BROKER_HOST to `wis2training-broker.wis2dev.io`.

```copy
DOWNLOAD_BROKER_HOST=wis2training-broker.wis2dev.io
```

Then restart the wis2downloader service to apply the changes:

```bash
python3 wis2box-ctl.py restart wis2downloader
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

Now we will setup a new subscription to the topic to downloaded cyclone-track data from the WIS2 Training Broker.

Login to the **wis2downloader** container:

```bash
python3 wis2box-ctl.py login wis2downloader
```

Then add the subscription to the topic `origin/a/wis2/int-wis2-training/data/core/weather/prediction/forecast/medium-range/deterministic/trajectory`:

```bash
wis2downloader add-subscription --topic origin/a/wis2/int-wis2-training/data/core/weather/prediction/forecast/medium-range/deterministic/trajectory
```

Exit the **wis2downloader** container by typing `exit`.

Wait until you see the downloads starting in the wis2downloader dashboard in Grafana.

!!! note "Downloading data from the WIS2 Training Broker"

    The WIS2 Training Broker is a test broker that is used for training purposes and may not publish data all the time.

    During the in-person training sessions, the local training will publish data to the WIS2 Training Broker for you to download.

    If you are doing this exercise outside of a training session, you may not see any data being downloaded.

Check that the data was downloaded by listing the contents of the downloads directory:

```bash
ls -R ~/wis2box-data/downloads
```

## Exercise 7: decoded the downloaded data

In order to demonstrate how you can decode the downloaded data, we will start a new container using 'decode-bufr-jupyter' image.

This container will be start Jupiter notebook server on your instance that include the eccodes library that you can use to decode the downloaded data.

We will the example notebooks included in `~/exercise-materials/notebook-examples` to decode the downloaded data for the cyclone tracks.

To start the container, use the following command:

```bash
docker run -d --name decode-bufr-jupyter -v ~/wis2box-data/downloads:/root/downloads \
    -v ~/exercise-materials/notebook-examples:/root/notebooks \
    -p 8888:8888 \
    -e JUPYTER_TOKEN=dataismagic! \
    mlimper/decode-bufr-jupyter
```

!!! note "About the decode-bufr-jupyter container"

    The `decode-bufr-jupyter` container is a custom container that includes the eccodes library and Jupyter notebook server. The container is based on a image that includes the `eccodes` library for decoding BUFR data, along

    The container is started with two volumes mounted:

    - The `~/wis2box-data/downloads` directory is mounted to `/root/downloads` in the container. This is where the downloaded data is stored.
    - The `~/exercise-materials/notebook-examples` directory is mounted to `/root/notebooks` in the container. This is where the example notebooks are stored.

    The container is started with the Jupyter notebook server listening on port 8888 and the token `dataismagic!` is used to authenticate to the server.

Then open a web browser and navigate to `http://<your-host>:8888` to access the Jupyter notebook server.


## Conclusion

!!! success "Congratulations!"

    In this practical session, you learned how to:

    - use the 'wis2downloader' to subscribe to a WIS2 Broker and download data to your local system

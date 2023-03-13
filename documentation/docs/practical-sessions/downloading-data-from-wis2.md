---
title: Downloading data from WIS2
---

# Downloading data from WIS2

## Introduction

In this session you will learn how to download data from a WIS2 Global Broker.

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

## Working with pywis-pubsub

The [first practical session](../connecting-to-mqtt) used MQTT Explorer to connect to the  Météo-France Global Broker.

Let's use the [pywis-pubsub](https://github.com/wmo-im/pywis-pubsub) to subscribe using a command line tool.

```bash
pywis-pubsub subscribe --help
```

Update the sample configuration to connect to the Météo-France Global Broker:

```bash
vi ~/exercise-materials/wis2box-setup/examples/config/pywis-pubsub.yml
```

Update the following values in the configuration:

- **broker**
    - username: everyone
    - password: everyone
    - host: globalbroker.meteo.fr
    - port: 8883
- **subscribe_topics**: `origin/#` `cache/#`

Run the `pywis-pubsub` command:

```bash
pywis-pubsub subscribe -c exercise-materials/wis2box-setup/examples/config/pywis-pubsub.yml   
```

!!! question

    What is the format of the data notifications that are displayed on the screen?

!!! question

    How can we run the `pywis-pubsub` command to be able to download the data (hint: review the options when running the `pywis-pubsub subscribe --help` command)?

Stop the `pywis-pubsub` command (CTRL-C) and update the configuration to be able to download the data
to `/tmp/wis2-data`.


## Conclusion

!!! success "Congratulations!"

    In this practical session, you learned how to:

    - use pywis-pubsub to subscribe to a Global Broker and download data to your local system

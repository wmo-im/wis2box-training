---
title: wis2box environment variables
---

#  wis2box environment variables

## Introduction

In this session you will customize your wis2box environment variables and re-initialize your wis2box.

### Preparation

Login to your student VM using WinSCP (using SCP-protocol) and PuTTY.

## re-initialize wis2box

Stop your wis2box:

```bash
cd ~/wis2box-1.0b4/
python3 wis2box-ctl.py stop
```

Stop the wis2box-ftp service:
```bash
docker-compose -f docker-compose.wis2box-ftp.yml down
```

Check that there are no longer any Docker-containers running on your system:
```bash
docker ps -a
```

Check that you still have Docker volumes remaining on your system:
```bash
docker volume ls
```

To delete all Docker volumes that are not associated to a Docker Container, run the following command:
```bash
docker volume prune
```

Check that your docker volumes are removed:

```bash
docker volume ls
```

!!! note "wis2box and Docker volumes"
    Note that deleting the Docker volumes is a quick way to re-initialize wis2box.
    
    It will also delete all information stored in the ElasticSearch API backend (i.e. discovery metadata, station metadata, data notifications, and previously ingested observation data).
    
    **Do NOT delete the `es-data`-volume if you want preserve previously ingested observation data.**

## Configure your own `dev.env`

The wis2box setup reads environment variables from `dev.env`. 

Make sure you are in the wis2box-directory and the check the current content of your `dev.env`.

```bash
cd ~/wis2box-1.0b4/
cat dev.env
```

This is the minimum setup that enabled you to run your wis2box in the previous exercises. 

This setup was using the pre-defined configuration stored in `~/exercise-materials/wis2box-test-data` as defined `WIS2BOX_HOST_DATADIR`.

!!! note "WIS2BOX_URL and WIS2BOX_API_URL"
    Note the current values of "WIS2BOX_URL" and "WIS2BOX_API_URL" are referring to your student-VM. 
    
    Make sure you keep these values when editing your `dev.env`

In the next few steps we will review how to update some of key environment variables used in wis2box by editing `dev.env` in the directory `wis2box-1.0b4`.

You can use WinSCP to connect to your instance and edit this file or you can edit the file from the command line using PuTTY.

## define your own wis2box-data directory

Using the SSH client connected to your student VM, use the following command to create a new directory on your instance:
```bash
mkdir -p ~/wis2box-data
```

Inside this directory create the following directory structure for your discovery metadata and station metadata:

```bash
mkdir -p ~/wis2box-data/metadata/discovery
mkdir -p ~/wis2box-data/metadata/station
```

### create an (empty) `data-mappings.yml`

The wis2box requires the file `data-mappings.yml` stored in your wis2box data directory. 

Use the following commands to create an (empty) `data-mappings.yml` that you will populate at a later step. 
```bash
echo "data:" > ~/wis2box-data/data-mappings.yml
```

### create an (empty) `station-list.csv`

The wis2box requires the file `metadata/station/station_list.csv` store in your wis2box data directory.

Use the following commands to create `metadata/station/station_list.csv` (headers only):

```bash
echo "station_name,wigos_station_identifier,traditional_station_identifier,facility_type,latitude,longitude,elevation,territory_name,wmo_region" > ~/wis2box-data/metadata/station/station_list.csv
```

Edit `dev.env` (using WinSCP or from the command line):

Comment out the original `WIS2BOX_HOST_DATADIR` :
 
 `# WIS2BOX_HOST_DATADIR=/home/<your-username>/exercise-materials/wis2box-test-data` 
 
And add the following to point to your new directory:

 `WIS2BOX_HOST_DATADIR=/home/<your-username>/wis2box-data`

### define custom credentials for your broker and storage

Edit the file `dev.env` and add the following to customize the default broker credentials (replace `XXXXXXXX` with your own password):

```bash
# broker credentials
WIS2BOX_BROKER_USERNAME=wis2box
WIS2BOX_BROKER_PASSWORD=XXXXXXXX
```

And the following content to `dev.env` to set the storage credentials (replace XXXXXXXX with your own password)

```bash
# storage credentials
WIS2BOX_STORAGE_USERNAME=minio
WIS2BOX_STORAGE_PASSWORD=XXXXXXXX
```

!!!note "storage credentials requirements"
    Username should be 3 or more characters

    Password should be 8 or more characters

Finally, add the following block to your `dev.env` to ensure the credentials are propagated across all services:

```bash
# wis2box-public-broker
WIS2BOX_BROKER_PUBLIC=mqtt://${WIS2BOX_BROKER_USERNAME}:${WIS2BOX_BROKER_PASSWORD}@mosquitto:1883
# minio-setup
MINIO_ROOT_USER=${WIS2BOX_STORAGE_USERNAME}
MINIO_ROOT_PASSWORD=${WIS2BOX_STORAGE_PASSWORD}
MINIO_NOTIFY_MQTT_USERNAME_WIS2BOX=${WIS2BOX_BROKER_USERNAME}
MINIO_NOTIFY_MQTT_PASSWORD_WIS2BOX=${WIS2BOX_BROKER_PASSWORD}
```

The content of you `dev.env` should now look as follows (except for your own passwords and URLs):

<img alt="winscp_devdotenv" src="../../assets/img/winscp_devdotenv.png" width="800">

## Restart wis2box

Start the wis2box and check the status:
```bash
python3 wis2box-ctl.py start
python3 wis2box-ctl.py status
```

### Check /data/wis2box in wis2box-management

Login to the **wis2box-management** container using the following command:

```bash
python3 wis2box-ctl.py login
```

Run the following command to view the environment variable `WIS2BOX_HOST_DATADIR`:

```bash
echo $WIS2BOX_HOST_DATADIR
```

returns:

```console
/home/<your-username>/wis2box-data/
```

And check the content of `/data/wis2box` inside the **wis2box-management** container:

```bash
ls /data/wis2box/
```

returns:

```console
data-mappings.yml metadata
```

!!! note
    The directory defined by `$WIS2BOX_HOST_DATADIR` gets mounted as `/data/wis2box` inside the **wis2box-management** container.

### Re-connect to MQTT-explorer

Try to reconnect to MQTT Explorer using the values you defined for `WIS2BOX_BROKER_USERNAME` and `WIS2BOX_BROKER_PASSWORD`

### Access the MinIO user interface

Access the MinIO UI at `http://<your-host-name>:9001` using the values you defined for `WIS2BOX_STORAGE_USERNAME` and `WIS2BOX_STORAGE_PASSWORD`

## Conclusion

!!! success "Congratulations!"
    In this practical session, you learned how to:

    - reinitialize wis2box services
    - set the wis2box data directory
    - set custom passwords for your broker and storage

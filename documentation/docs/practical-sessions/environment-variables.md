---
title: wis2box environment variables
---

#  wis2box environment variables

## Introduction

In this session you will customize your wis2box environment variables and restart your wis2box.

### Preparation

Login to your student VM.

## re-initialize wis2box

Stop your wis2box:

```bash
cd ~/wis2box-1.0b3/
python3 wis2box-ctl.py stop
```

Stop your wis2box-ftp:
```bash
docker-compose -f docker-compose.wis2box-ftp.yml down
```

Check that there are no longer any Docker-containers running on your system:
```bash
docker ps -a
```

Note that though you have no Docker-containers you still have docker volumes remaining on your system:
```bash
docker volume ls
```

To delete all docker volumes that are not associated to a docker-container run the following command:
```bash
docker volume prune
```

Check that your docker volumes are gone:
```bash
docker volume ls
```

!!! note 
    Note that deleting the docker volumes is a quick way to re-initialize the wis2box.
    It will also delete all information stored in the ElasticSearch-backend: the discovery metadata and previously ingested observation data. 
    Do NOT delete your `es-data`-volume if you want preserve previously ingested observation data.

## Configure your own `dev.env`

The wis2box setup reads environment variables from `dev.env`. 

Make sure you are in the wis2box-directory and the check the current content of your `dev.env`.

```bash
cd ~/wis2box-1.0b3/
cat dev.env
```

This is the minimum setup that enabled you to run your wis2box in the previous practical exercises, using the pre-defined configuration stored in `~/exercise-materials/wis2box-test-data`.

!!! note "WIS2BOX_URL and WIS2BOX_API_URL"
    Note the current values of "WIS2BOX_URL" and "WIS2BOX_API_URL" make sure you keep these values in the new version of your `dev.env`

Let's create a new empty version in ~/wis2box-1.0b3/ :
```bash
mv dev.env dev.env_old
touch dev.env
```

You can use WinSCP to connect to your instance and edit this file or edit the file from the command-line when connected over SSH.

### define your own wis2box-data directory

Create a new directory on your instance to store the files you will share with the wis2box-management container:
```bash
mkdir -p ~/wis2box-data
```

Inside this directory create the following directory structure for your discovery-metadata and station-metadata:
```bash
mkdir -p ~/wis2box-data/metadata/discovery
mkdir -p ~/wis2box-data/metadata/station
```

### create an (empty) data-mappings.yml

The wis2box requires a data-mappings.yml in your wis2box-data-directory, use the following commands to create an (empty) data-mappings.yml that you will populate later. 
```bash
echo "data > ~/wis2box-data/data-mappings.yml
```

### create an (empty) station-list.csv

The wis2box requires a station_list.csv, stored in metadata/station/, use the following commands to create metadata/station/station_list.csv (headers-only):
```bash
echo "station_name,wigos_station_identifier,traditional_station_identifier,facility_type,latitude,longitude,elevation,territory_name,wmo_region
" > ~/wis2box-data/metadata/station/station_list.csv
```

Define WIS2BOX_HOST_DATADIR=/home/**username**/wis2box-data

For example from the command-line:
```bash
echo "''" > ~/wis2box-1.0b3/dev.env
```
Or open `dev.env` and use the internal editor in WinSCP

### define your WIS2BOX_URL and WIS2BOX_API_URL

Add WIS2BOX_URL and WIS2BOX_API_URL to your dev.env 

### define your WIS2BOX_BROKER_USERNAME and WIS2BOX_BROKER_PASSWORD

TBD

### define your WIS2BOX_STORAGE_USERNAME and WIS2BOX_STORAGE_USERNAME

TBD

## Review your new setup

Start the wis2box and check the status:
```bash
python3 wis2box-ctl.py start
```

Login to the **wis2box-management** container using the following command:

```bash
python3 wis2box-ctl.py login
```

Run the following command to view the environment variables used by your wis2box:

```bash
wis2box environment show
```

Note the variables you have set for `WIS2BOX_HOST_DATADIR`, `WIS2BOX_URL` and `WIS2BOX_API_URL`, etc.

Review that your **wis2box-broker** and MinIO storage passwords have been updated.

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

## Conclusion

!!! success "Congratulations!"
    In this practical session, you learned how to:

    - reinitialize wis2box services
    - set the wis2box data directory
    - set the logging level for the wis2box services   
    - set custom passwords for your broker and storage

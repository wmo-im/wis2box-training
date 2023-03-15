---
title: Configuring station metadata
---

# Configuring station metadata

## Introduction

wis2box requires station metadata to be able to process and publish observations to WIS2.
This session will walk you through creating and publishing station metadata from wis2box
from a configuration file.  wis2box uses a fixed station metadata list that is used as
part of its runtime operation.

## Preparation

!!! note
    Ensure you are logged into the **wis2box-management** container on your student VM: 

    ```bash
    cd ~/exercise-materials/wis2box-setup
    python3 wis2box-ctl.py login
    ```

## Creating station metadata

Update the file `~/exercises-metadata/test-data/metadata/station/station_list.csv`, adding your new station:

```bash
vi ~/exercises-metadata/test-data/metadata/station/station_list.csv
```

For each new station, add a row to the end of the file with the following values:

- `station_name`: the human readable name of the station
- `wigos_station_identifier`: the WSI issued for the station
- `traditional_station_identifier`: the traditional station identifier if a WSI does not exist
- `facility_type`: the station/platform type (use **Land (fixed)** for land stations)
- `latitude`: the latitude, in decimal degrees
- `longitude`: the longitude, in decimal degrees
- `elevation`: station elevation, in metres above sea level
- `territory_name`: the human readable country name
- `wmo_region`: the Roman numeral of your country based on WMO Regional Associations

!!! tip
    You can also derive your station information from the [WMO OSCAR/Surface](https://oscar.wmo.int/surface) system.

!!! tip
    Ensure that latitude and longitude values are correctly signed (for example, use the minus sign [`-`] for southern or western hemispheres.

## Publishing station metadata

Run the following command to publish your station metadata:

```bash
wis2box metadata station discovery publish-collection
```

Ensure that your new station metadata was published to the API, by navigating to `http://<your-host>/oapi/collections/stations`.

!!! question
    Do you see your new station metadata?

Click on your station metadata record and inspect the content, noting how it relates to the station list configuration updated earlier in this session.

## Conclusion

!!! success "Congratulations!"
    In this practical session, you learned how to:

    - update station metadata
    - publish station metadata

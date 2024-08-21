---
title: Adding GTS headers to WIS2 notifications
---

# Adding GTS headers to WIS2 notifications

!!! abstract "Learning outcomes"

    By the end of this practical session, you will be able to:
    
    - configure a mapping between filename and GTS headers
    - ingest data with a filename that matches the GTS headers
    - view the GTS headers in the WIS2 notifications

## Introduction

WMO Members wishing to stop their data-transmission on GTS during the transition phase to WIS2, will need to add GTS-headers to their WIS2-notifications. These headers enable the WIS2-to-GTS gateway to forward the data to the GTS network.

This allows Members having migrated to using a WIS2 node for data publication to disable their MSS system and ensure that their data is still available to Members not yet migrated to WIS2.

The GTS property in the WIS2 Notification Message needs to be added as an additional property to the WIS2 Notification Message. The GTS property is a JSON object that contains the GTS headers that are required for the data to be forwarded to the GTS network.

```json
{
  "gts": {
    "ttaaii": "FTAE31",
    "cccc": "VTBB"
  }
}
```

Within wis2box you can add this to WIS2 Notifications automatically by providing an additional file "gts_headers_mappings.csv" that contains the required information to map the GTS headers to the incoming filenames.

This file should be placed in the directory defined by WIS2BOX_HOST_DATADIR in your wis2box.env and should have the following columns:

- string_in_filepath: a string that is part of the filename that will be used to match the GTS headers
- TTAAii: the TTAAii header to be added to the WIS2 notification
- CCCC: the CCCC header to be added to the WIS2 notification

## Preparation

Ensure you have SSH access to your student VM and that your wis2box instance is up and running.

Make sure that you are connected to the MQTT-broker of your wis2box-instance using MQTT Explorer. You can use the public credentials `everyone/everyone` to connect to the broker.

Make sure you have a web browser open with the Grafana dashboard for your instance by going to `http://<your-host>:3000`

## creating gts_headers_mappings.csv

To add GTS headers to your WIS2 notifications, a CSV file is required that maps GTS headers to incoming filenames.

The CSV file should be named (exactly) "gts_headers_mapping.csv" and should be placed in the directory defined by WIS2BOX_HOST_DATADIR in your wis2box.env. 

## Exercise 1: providing a gts_headers_mapping.csv file
    
Copy the file `exercise-materials/gts-headers-exercises/gts_headers_mappings.csv` to your wis2box instance and place it in the directory defined by WIS2BOX_HOST_DATADIR in your wis2box.env.


```bash
cp exercise-materials/gts-headers-exercises/gts_headers_mappings.csv ~/wis2box-data
```

Then restart the wis2box stack to apply the changes:

```bash
python3 wis2box-ctl.py restart
```

## Exercise 2: Ingesting data with GTS headers

Copy the file `exercise-materials/gts-headers-exercises/FTAE31_VTBB_20220101T000000Z.csv` to the directory defined by WIS2BOX_HOST_DATADIR in your wis2box.env:

```bash
cp exercise-materials/gts-headers-exercises/FTAE31_VTBB_20220101T000000Z.csv ~/wis2box-data
```

Then login to the **wis2box-management** container:

```bash
cd ~/wis2box-1.0b8
python3 wis2box-ctl.py login
```

From the wis2box command line we can ingest the sample data file `FTAE31_VTBB_20220101T000000Z.csv` into a specific dataset as follows:

```bash
wis2box data ingest -p /data/wis2box/FTAE31_VTBB_20220101T000000Z.csv --metadata-identifier urn:wmo:md:not-my-centre:surface-based-observations.synop
```

Make sure to replace the metadata-identifier with the correct identifier for your dataset.

## Exercise 3: Viewing the GTS headers in the WIS2 Notification

Go to the MQTT Explorer and check if you can see the WIS2 Notification Message for the data you just ingested.

The WIS2 Notification Message should contain the GTS headers you provided in the gts_headers_mapping.csv file.

## Conclusion

!!! success "Congratulations!"
    In this practical session, you learned how to:

    - add GTS-headers to your WIS2-notifications

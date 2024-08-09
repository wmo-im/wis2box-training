---
title: Configuring station metadata
---

# Configuring station metadata

!!! abstract "Learning outcomes"

    By the end of this practical session, you will be able to:

    - create an authorization token for the `collections/stations` endpoint
    - add station metadata to wis2box
    - review stations associated to datasets in the **wis2box-ui**
    - update/delete station metadata using the **wis2box-webapp**

## Introduction

For sharing data internationally between WMO Members, it is important to have a common understanding of the stations that are producing the data. The WMO Integrated Global Observing System (WIGOS) provides a framework for the integration of observing systems and data management systems. The **WIGOS Station Identifier (WSI)** is used as the unique reference of the station which produced a specific set of observation data.

wis2box has a collection of station metadata that is used to describe the stations that are producing the observation data and should be retrieved from the **OSCAR/Surface** database. The station metadata in wis2box is used by the BUFR-transformation tools to check input data contains a WIGOS Station Identifier (WSI) and to provide a mapping between the WSI and the station metadata.

## Create an authorization token for collections/stations

To edit stations via the **wis2box-webapp** you will first to need create an authorization token.

Login to your student VM and ensure you are in the `wis2box-1.0b8` directory:

```bash
cd ~/wis2box-1.0b8
```

Then login into the **wis2box-management** container with the following command:

```bash
python3 wis2box-ctl.py login
```

Within the **wis2box-management** container your can create an authorization token for a specific endpoint using the command: `wis2box auth add-token --path <my-endpoint>`.

For example, to use a random automatically generated token for the `collections/stations` endpoint:

```{.copy}
wis2box auth add-token --path collections/stations
```	

The output will look like this:

```{.copy}
Continue with token: 7ca20386a131f0de384e6ffa288eb1ae385364b3694e47e3b451598c82e899d1 [y/N]? y
Token successfully created
```

Or, if you want to define your own token for the `collections/stations` endpoint, you can use the following example:

```{.copy}
wis2box auth add-token --path collections/stations DataIsMagic
```

Output:
    
```{.copy}
Continue with token: DataIsMagic [y/N]? y
Token successfully created
```

Please create an authorization token for the `collections/stations` endpoint using the instructions above.

## add station metadata using the **wis2box-webapp**

The **wis2box-webapp** provides a graphical user interface to edit station metadata.

Open the **wis2box-webapp** in your browser by navigating to `http://<your-host>/wis2box-webapp`:

<img alt="wis2box-webapp" src="../../assets/img/wis2box-webapp.png" width="800">

And select stations:

<img alt="wis2box-webapp-select-stations" src="../../assets/img/wis2box-webapp-select-stations.png" width="250">

When you click add 'add new station' you are asked to provide the WIGOS station identifier for the station you want to add:

<img alt="wis2box-webapp-import-station-from-oscar" src="../../assets/img/wis2box-webapp-import-station-from-oscar.png" width="800">

!!! note "Add station metadata for 3 or more stations"
    Please add three or more stations to the wis2box station metadata collection of your wis2box. 
      
    Please use stations from your country if possible, especially if you brought your own data.
      
    If your country does not have any stations in OSCAR/Surface, you can use the following stations for the purpose of this exercise:

      - 0-20000-0-91334
      - 0-20000-0-96323 (note missing station elevation in OSCAR)
      - 0-20000-0-96749 (note missing station elevation in OSCAR)

When you click search the station data is retrieved from OSCAR/Surface, please note that this can take a few seconds.

Review the data returned by OSCAR/Surface and add missing data where required. Select a topic for the station and provide your authorization token for the `collections/stations` endpoint and click 'save':

<img alt="wis2box-webapp-create-station-save" src="../../assets/img/wis2box-webapp-create-station-save.png" width="800">

<img alt="wis2box-webapp-create-station-success" src="../../assets/img/wis2box-webapp-create-station-success.png" width="500">

Go back to the station list and you will see the station you added:

<img alt="wis2box-webapp-stations-with-one-station" src="../../assets/img/wis2box-webapp-stations-with-one-station.png" width="800">

Repeat this process until you have at least 3 stations configured.

!!! tip "Deriving missing elevation information"

    If your station elevation is missing, there are online services to help lookup the elevation using open elevation data. One such example is the [Open Topo Data API](https://www.opentopodata.org).

    For example, to get the elevation at latitude -6.15558 and longitude 106.84204, you can copy-paste the following URL in a new browser-tab:

    ```copy
    https://api.opentopodata.org/v1/aster30m?locations=-6.15558,106.84204
    ```

    Output:

    ```{.copy}
    {
      "results": [
        {
          "dataset": "aster30m", 
          "elevation": 7.0, 
          "location": {
            "lat": -6.15558, 
            "lng": 106.84204
          }
        }
      ], 
      "status": "OK"
    }
    ```

## Review your station metadata

The station metadata is stored in the backend of wis2box and made available via the **wis2box-api**. 

If you open a browser and navigate to `http://<your-host>/oapi/collections/stations/items` you will see the station metadata you added:

<img alt="wis2box-api-stations" src="../../assets/img/wis2box-api-stations.png" width="800">

You can also visit the **wis2box-ui** at `http://<your-host>` and select "EXPLORE" on your dataset and you will see the stations you added:

<img alt="wis2box-ui-explore-stations" src="../../assets/img/wis2box-ui-explore-stations.png" width="800">

!!! note "Review your station metadata"

    Verify the stations you added are associated to your dataset by visiting the **wis2box-api** and **wis2box-ui** endpoints for your host in your browser.

You also have the option to view/update/delete the station in the **wis2box-webapp**. Note that you are required to provide your authorization token for the `collections/stations` endpoint to update/delete the station.

!!! note "Update/delete station metadata"

    Try and see if you can update/delete the station metadata for one of the stations you added using the **wis2box-webapp**.

## Bulk station metadata upload

Note that wis2box also has the ability to perform "bulk" loading of station metadata from a CSV file using command line tools provided in the **wis2box-management** container. See the official [wis2box documentation](https://docs.wis2box.wis.wmo.int) for more information on how to use this feature.

## Conclusion

!!! success "Congratulations!"
    In this practical session, you learned how to:

    - create an authorization token for the `collections/stations` endpoint
    - add station metadata to wis2box
    - review stations associated to datasets in the **wis2box-ui**
    - update/delete station metadata using the **wis2box-webapp**

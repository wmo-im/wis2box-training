---
title: Querying data using the wis2box API
---

# Querying data using the wis2box API

!!! abstract "Learning outcomes"
    By the end of this practical session, you will be able to:

    - use the wis2box API to query and filter your stations
    - use the wis2box API to query and filter your data

## Introduction

The wis2box API provides discovery and query access in a machine readable manner to the data that has been ingested in wis2box. The API is based on the OGC API - Features standard and is implemented using [pygeoapi](https://pygeoapi.io).

The wis2box API provides access to the following collections:

- Stations
- Discovery metadata
- Data notifications
- plus one collection per dataset configured, which stores the output from bufr2geojson (the plugin `bufr2geojson` needs to be enabled in the data mappings configuration to fill the items in the dataset collection).

In this practical session you will learn how to use the data API to browse and query data that has been ingested in wis2box.

## Preparation

!!! note
    Navigate to the wis2box API landing page in your web browser:

    `http://YOUR-HOST/oapi`

<img alt="wis2box-api-landing-page" src="../../assets/img/wis2box-api-landing-page.png" width="600">

## Inspecting collections

From the landing page, click on the 'Collections' link.

!!! question
    How many dataset collections do you see on the resulting page? What do you think each collection represents?

??? success "Click to reveal answer"
    There should be 4 collections displayed, including "Stations", "Discovery metadata", and "Data notifications"

## Inspecting stations

From the landing page, click on the 'Collections' link, then click on the 'Stations' link.

<img alt="wis2box-api-collections-stations" src="../../assets/img/wis2box-api-collections-stations.png" width="600">

Click on the 'Browse' link, then click on the 'json' link.

!!! question
    How many stations are returned? Compare this number to the station list in `http://YOUR-HOST/wis2box-webapp/station`

??? success "Click to reveal answer"
    The number of stations from the API should be equal to the number of stations you see in the wis2box webapp.

!!! question
    How can we query for a single station (e.g. `Balaka`)?

??? success "Click to reveal answer"
    Query the API with `http://YOUR-HOST/oapi/collections/stations/items?q=Balaka`.

!!! note
    The above example is based on the Malawi test data.  Try testing against the stations your have ingested as part of the previous exercises.

## Inspecting observations

!!! note
    The above example is based on the Malawi test data.  Try testing against the observation your have ingested as part of the exercises.

From the landing page, click on the 'Collections' link, then click on the 'Surface weather observations from Malawi' link.

<img alt="wis2box-api-collections-malawi-obs" src="../../assets/img/wis2box-api-collections-malawi-obs.png" width="600">

Click on the 'Queryables' link.

<img alt="wis2box-api-collections-malawi-obs-queryables" src="../../assets/img/wis2box-api-collections-malawi-obs-queryables.png" width="600">

!!! question
    Which queryable would be used to filter by station identifier?

??? success "Click to reveal answer"
    The `wigos_station_identifer` is the correct queryable.

Navigate to the previous page (i.e. `http://YOUR-HOST/oapi/collections/urn:wmo:md:mwi:mwi_met_centre:surface-weather-observations`)

Click on the 'Browse' link.

!!! question
    How can we visualize the JSON response?

??? success "Click to reveal answer"
    By clicking on the 'JSON' link at the top right of the page, of by adding `f=json` to the API request on the web browser.

Inspect the JSON response of the observations.

!!! question
    How many records are returned?

!!! question
    How can we limit the response to 3 observations?

??? success "Click to reveal answer"
    Add `limit=3` to the API request.

!!! question
    How can we sort the response by the latest observations?

??? success "Click to reveal answer"
    Add `sortby=-resultTime` to the API request (notice the `-` sign to denote descending sort order).  For sorting by the earliest observations, update the request to include `sortby=resultTime`.

!!! question
    How can we filter the observations by a single station?

??? success "Click to reveal answer"
    Add `wigos_station_identifier=<WSI>` to the API request.

!!! question
    How can we receive the observations as a CSV?

??? success "Click to reveal answer"
    Add `f=csv` to the API request.

!!! question
    How can we show a single observation (id)?

??? success "Click to reveal answer"
    Using the feature identifier from an API request against the observations, query the API for `http://YOUR-HOST/oapi/collections/{collectionId}/items/{featureId}`, where `{collectionId}` is the name of your observations collection and `{itemId}` is the identifier of the single observation of interest.

## Conclusion

!!! success "Congratulations!"
    In this practical session, you learned how to:

    - use the wis2box API to query and filter your stations
    - use the wis2box API to query and filter your data

---
title: Data API usage and queries
---

# Data API usage and queries

## Introduction

The wis2box API provides discovery and query access in a machine readable manager, which includes the wis2box UI.

In this practical session you will learn how to use the data API to discovery, browse and query data that has been ingested in wis2box.

## Preparation

!!! note
    Navigate to the wis2box API landing page in your web browser:

    `http://<your-host>/oapi`

<img alt="wis2box-api-landing-page" src="../../assets/img/wis2box-api-landing-page.png" width="600">

## Inspecting collections

From the landing page, click on the 'Collections' link.

!!! question
    How many dataset collections do you see on the resulting page? What do you think each collection represents?

## Inspecting stations

From the landing page, click on the 'Collections' link, then click on the 'Stations' link.

<img alt="wis2box-api-collections-stations" src="../../assets/img/wis2box-api-collections-stations.png" width="600">

Click on the 'Browse' link, then click on the 'json' link.

!!! question
    How many stations are returned? Compare this number to the station list in `/data/wis2box/metadata/station/station_list.csv` file when logged into wis2box (`python3 wis2box-ctl.py login`).

!!! question
    How can we query for a single station (e.g. `Balaka`)?

!!! note
    The above example is based on the Malawi test data.  Try testing against the stations your have ingested as part of the exercises.

## Inspecting observations

!!! note
    The above example is based on the Malawi test data.  Try testing against the observation your have ingested as part of the exercises.

From the landing page, click on the 'Collections' link, then click on the 'Surface weather observations from Malawi' link.

<img alt="wis2box-api-collections-malawi-obs" src="../../assets/img/wis2box-api-collections-malawi-obs.png" width="600">

Click on the 'Queryables' link.

<img alt="wis2box-api-collections-malawi-obs-queryables" src="../../assets/img/wis2box-api-collections-malawi-obs-queryables.png" width="600">

!!! question
    Which queryable would be used to filter by station identifier?

Navigate to the previous page (i.e. `http://localhost/oapi/collections/urn:x-wmo:md:mwi:mwi_met_centre:surface-weather-observations`)

Click on the 'Browse' link.

!!! question
    How can we visualize the JSON response?

Inspect the JSON response of the observations.

!!! question
    How many records are returned?

!!! question
    How can we limit the response to 3 observations?

!!! question
    How can we sort the response by the latest observations?

!!! question
    How can we filter the observations by a single station?

!!! question
    How can we receive the observations as a CSV?

!!! question
    How can we show a single observation (id)?

## Conclusion

!!! success "Congratulations!"
    In this practical session, you learned how to:

    - use the wis2box API to query and filter your stations
    - use the wis2box API to query and filter your data

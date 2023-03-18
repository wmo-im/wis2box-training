---
title: Configuring WIS2 discovery metadata
---

# Configuring WIS2 discovery metadata

## Introduction

As described in the [overviews](../../overviews), WIS2 requires discovery metadata to be provided describing
your data to be shared to WIS2 Global Services.  This session will walk you through creating and publishing
discovery metadata from wis2box from a configuration file.

## Preparation

!!! note
    Ensure you are running MQTT Explorer and you are connected to the broker on your student VM before continuing.

!!! note
    Ensure you are logged into the **wis2box-management** container on your student VM: 

    ```bash
    cd ~/exercise-materials/wis2box-setup
    python3 wis2box-ctl.py login
    ```

## Creating discovery metadata

Copy the test discovery metadata into your own file (you may name the file whatever you wish):

```bash
cp ~/exercise-materials/wis2box-setup/test-data/mwi-surface-weather-observations.yml ~/my-discovery-metadata.yml
```

Inspect the sample discovery metadata:

```bash
more ~/my-discovery-metadata.yml
```

!!! note
    All values in the discovery metadata configuration are required and should be included.

!!! question
    How does line 3 of your discovery metadata file relate to the new data mapping in the previous session?

Update the following values in the discovery metadata configuration:

- `wis2box.topic_hierarchy`: the topic hierarchy that categorizes the data (this value should be the same as the definition in your newly created data mapping).
- `wis2box.country`: 3-letter country code in lower case
- `wis2box.centre_id`: your centre id as defined in the previous exercise
- `metadata.identifier`: a unique identifier consisting of `urn:x-wmo:md:[country]:[centre_id]:[dataset_name]`, where `[dataset-name]` can be any name of your choosing.  Remember this value for API validation later on in this exercise
- `identification.title`: a human readable title describing your data
- `identification.abstract`: a human readable description describing your data
- `identification.dates.creation`: when the discovery metadata was created (today's date)
- `identification.extents.spatial (bbox)`: the bounding box coordinates of your data (minimum longitude, minimum latitude, maximum longitude, maximum latitude), in decimal degrees
- `identification.extents.temporal (begin)`: the begin and end time of your data (keeping the end time to `null` is suitable to ongoing observations)
- `contact.pointOfContact`: your organization's point of contact information

!!! tip
    The configuration is based on the YAML format.  Consult the [YAML cheatsheet](../cheatsheets/yaml.md) for more information.

!!! tip
    Ensure that bbox values are correctly signed (for example, use the minus sign [`-`] for southern or western hemispheres.

## Publishing discovery metadata

Run the following command to publish your discovery metadata:

```bash
wis2box metadata discovery publish ~/my-discovery-metadata.yml
```

Ensure that your discovery metadata was published to the API, by navigating to `http://<your-host>/oapi/collections/discovery-metadata`.

Ensure that your discovery metadata was also published to the broker, by looking for a new metadata message in MQTT Explorer.

!!! question
    Do you see your new discovery metadata in the API?

Click on your discovery metadata record and inspect the content, noting how it relates to the discovery metadata configuration created earlier in this session.

Update the title of your discovery metadata, and re-publish:

```bash
vi ~/my-discovery-metadata.yml
wis2box metadata discovery publish ~/my-discovery-metadata.yml
```

Ensure that your discovery metadata updates were published to the API, by refreshing the page to your discovery metadata.

!!! question
    Are you able to see the updates you made in the configuration?

Feel free to update additional values and re-publishing your discovery metadata to get a better idea of how and where discovery metadata content is updated.

## Publishing your dataset to the API

Run the below command to add the data to the API:

```bash
wis2box data add-collection ~/my-discovery-metadata.yml
```

Ensure that your dataset was published to the API, by navigating to `http://<your-host>/oapi/collections/<metadata.identifier>`.

!!! question
    Do you see your new dataset in the API?

!!! question
    Do you see any data coming from your new dataset in the API?  If not, why not?

## Conclusion

!!! success "Congratulations!"
    In this practical session, you learned how to:

    - create discovery metadata
    - publish discovery metadata
    - update and re-publish discovery metadata

---
title: Configuring WIS2 discovery metadata
---

# Configuring WIS2 discovery metadata

!!! abstract "Learning outcomes"
    By the end of this practical session, you will be able to:

    - create discovery metadata
    - publish discovery metadata
    - update and re-publish discovery metadata

## Introduction

WIS2 requires discovery metadata to be provided describing
your data to be shared to WIS2 Global Services.  This session will walk you through creating and publishing
discovery metadata from wis2box from a configuration file.

!!! note
    While this practical session uses discovery metadata to publish SYNOP, feel free to use another dataset (such as TEMP).

    The discovery metadata configuration file for TEMP can be found in `~/wis2box-data/metadata/discovery/metadata-temp.yml`.


## Preparation

Ensure you are running MQTT Explorer and you are connected to the broker on your student VM before continuing.

Login to your student VM using your SSH-client.

## Creating discovery metadata

Let's start by using the file generated during the [Initializing wis2box](../initializing-wis2box) practical session.

Inspect the sample SYNOP discovery metadata:

```bash
more ~/wis2box-data/metadata/discovery/metadata-synop.yml
```

!!! note
    All values in the discovery metadata configuration are required and should be included.

!!! question
    How does line 3 of your discovery metadata file relate to the new data mapping in the previous session?

??? success "Click to reveal answer"
    Line 3 of the discovery metadata configuration file should be equal to one of the data mappings defined in `data-mappings.yml`.

Update the following values in the discovery metadata configuration:

- `identification.title`: a human readable title describing your data
- `identification.abstract`: a human readable description describing your data
- `identification.extents.temporal (begin)`: the begin (`BEGIN_DATE`) (`YYYY-MM-DD`) and end time of your data (keeping the end time to `null` is suitable to ongoing observations)
- `contact.pointOfContact`: your organization's point of contact information

!!! note
    Many values have been pre-populated as part of the [Initializing wis2box](../initializing-wis2box) practical session, however you will want to ensure they are correct / accurate for your dataset.

!!! tip
    The configuration is based on the YAML format.  Consult the [YAML cheatsheet](../cheatsheets/yaml.md) for more information.

!!! tip
    As the `identification.extents.spatial.bbox` coordinates are pre-populated, you may want to update the coordinates if the dataset coordinates are not based on your country's administrative boundaries.  Feel free to update this value accordingly, ensuring that values are correctly signed (for example, use the minus sign [`-`] for southern or western hemispheres.

    The following tools can be valuable for deriving your `identification.extents.spatial.bbox`:

    - [https://gist.github.com/graydon/11198540](https://gist.github.com/graydon/11198540)
    - [http://bboxfinder.com](http://bboxfinder.com)
    - [https://boundingbox.klokantech.com](https://boundingbox.klokantech.com)

## Publishing discovery metadata

First login to the **wis2box-management** container:

```bash
python3 wis2box-ctl.py login
```

Run the following command to publish your discovery metadata:

```bash
wis2box metadata discovery publish /data/metadata/discovery/metadata-synop.yml
```

Ensure that your discovery metadata was published to the API, by navigating to `http://<your-host>/oapi/collections/discovery-metadata`.

Ensure that your discovery metadata was also published to the broker, by looking for a new metadata message in MQTT Explorer.

!!! question
    Do you see your new discovery metadata in the API?

??? success "Click to reveal answer"
    You should see your published discovery metadata in the API, under the `http://<your-host>/oapi/collections/discovery-metadata/items` link.

Click on your discovery metadata record and inspect the content, noting how it relates to the discovery metadata configuration created earlier in this session.

Update the title of your discovery metadata:

```bash
vi ~/wis2box-data/metadata/discovery/metadata-temp.yml
```

!!! tip
    You can also use WinSCP to connect to your instance and edit this file.

Now re-publish (from inside the **wis2box-management** container):

```bash
wis2box metadata discovery publish /data/metadata/discovery/metadata-synop.yml
```

Ensure that your discovery metadata updates were published to the API, by refreshing the page to your discovery metadata.

!!! question
    Are you able to see the updates you made in the configuration?

??? success "Click to reveal answer"
    You should see your published discovery metadata update in the API, under the `http://<your-host>/oapi/collections/discovery-metadata/items` link.

Feel free to update additional values and re-publishing your discovery metadata to get a better idea of how and where discovery metadata content is updated.

## Publishing your dataset to the API

Run the below command to add the data to the API:

```bash
wis2box data add-collection /data/metadata/discovery/metadata-synop.yml
```

Ensure that your dataset was published to the API, by navigating to `http://<your-host>/oapi/collections/<metadata.identifier>`.

!!! question
    Do you see your new dataset in the API?

??? success "Click to reveal answer"
    You should see the new dataset published to the API.

!!! question
    Do you see any data coming from your new dataset in the API?  If not, why not?

??? success "Click to reveal answer"
    If you do not see new data, this means that data has not been ingested yet against your new dataset.

## Conclusion

!!! success "Congratulations!"
    In this practical session, you learned how to:

    - create discovery metadata
    - publish discovery metadata
    - update and re-publish discovery metadata

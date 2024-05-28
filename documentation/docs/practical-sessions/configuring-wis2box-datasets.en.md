---
title: Configuring datasets in wis2box
---

# Configuring datasets in wis2box

!!! abstract "Learning outcomes"
    By the end of this practical session, you will be able to:

    - create a new dataset
    - create discovery metadata for a dataset
    - configure data mappings for a dataset
    - publish a WIS2 notifications with a WCMP2 record
    - update and re-publish your dataset

## Introduction

The wis2box uses datasets that are associated with discovery metadata and data mappings.

The discovery metadata is used to create a WCMP2 record that is shared using a WIS2 notification published on your wis2box-broker.

The data mappings are used to associate a data plugin to your input data, allowing your data to be transformed prior to being published using the WIS2 notification.

This session will walk you through creating a new dataset, creating discovery metadata, and configuring data mappings. You will inspect your dataset in the wis2box-api and review the WIS2 notification for your discovery metadata.

## Preparation

Ensure you are running MQTT Explorer and you are connected to the broker on your student VM before continuing.

Open a browser and open a page to `http://<your-host>/wis2box-webapp`. Make sure you are logged in and can access the 'dataset editor' page.

## Creating a new dataset

Use the wis2box-webapp to create a new dataset.

## Reviewing the WIS2-notification for your discovery metadata

Review the WIS2-notification for the discovery metadata you received when you published your data.

## Reviewing your dataset in the wis2box-api

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

---
title: Setting up a recommended dataset with access control
---

# Setting up a recommended dataset with access control

!!! abstract "Learning outcomes"
    By the end of this practical session, you will be able to:

    - create a new dataset with data-policy 'recommended'
    - add an access token to the dataset
    - validate the dataset can not be accessed without the access token
    - add the access token to HTTP headers to access the dataset

## Introduction

Datasets that are not considered 'core' dataset in WMO can optionally be configured with an access control policy. The wis2box provides a mechanism to add an access token to a dataset which will prevent users from downloading data unless they supply the access token in the HTTP headers.

## Preparation

Ensure you have SSH access to your student VM and that your wis2box instance is up and running.

Make sure that you are connected to the MQTT-broker of your wis2box-instance using MQTT Explorer. You can use the public credentials `everyone/everyone` to connect to the broker.

Ensure you have a web browser open with the wis2box-webapp for your instance by going to `http://<your-host>/wis2box-webapp`.

## create a new dataset with data-policy 'recommended'

Go to the 'dataset editor' page in the wis2box-webapp and create a new dataset. Use the same centre-id as in the previous practical sessions and use the template='surface-weather-observations/synop'. 

In the dataset editor, set the data-policy to 'recommended' and fill all the required fields.

Ensure the dataset is published and the WIS2 Notification Message announcing the new Discovery Metadata record is published.

Add the following stations to your "recommended" dataset to ensure the test data can be ingested and published:

- 0-20000-0-60351
- 0-20000-0-60355
- 0-20000-0-60360

## add an access token to the dataset

Login to the wis2box-management container and add an access token to the dataset.

```bash
docker exec -it wis2box-management bash
```

```bash
wis2box auth add-token --mdi urn:md:wmo:mydataset --token S3cr3tT0k3n
```

## publish some data to the dataset

Publish to the test-data to the new recommended dataset.

Check the canonical-link in the WIS2 Notification Message and copy-paste the link to the browser.

You should see a 403 Forbidden error.

## add the access token to HTTP headers to access the dataset

In order to demonstrate that the access token is required to access the dataset we will reproduce the error you saw in the browser using the command line function `wget`.

From the command line in your student VM, use the `wget` command with the canonical-link you copied from the WIS2 Notification Message.

```bash
wget <canonical-link>
```

You should see a 403 Forbidden error.

Now add the access token to the HTTP headers to access the dataset.

```bash
wget --header="Authorization: Bearer S3cr3tT0k3n" <canonical-link>
```

You should see the data being downloaded.

## clean up

Delete the dataset using the dataset editor.

## Conclusion

!!! success "Congratulations!"
    In this practical session, you learned how to:

    - create a new dataset with data-policy 'recommended'
    - add an access token to the dataset
    - validate the dataset can not be accessed without the access token
    - add the access token to HTTP headers to access the dataset

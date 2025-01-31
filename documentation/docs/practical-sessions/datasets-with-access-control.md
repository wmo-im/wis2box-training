---
title: Setting up a recommended dataset with access control
---

# Setting up a recommended dataset with access control

!!! abstract "Learning outcomes"
    By the end of this practical session, you will be able to:

    - create a new dataset with data policy 'recommended'
    - add an access token to the dataset
    - validate the dataset can not be accessed without the access token
    - add the access token to HTTP headers to access the dataset

## Introduction

Datasets that are not considered 'core' dataset in WMO can optionally be configured with an access control policy. wis2box provides a mechanism to add an access token to a dataset which will prevent users from downloading data unless they supply the access token in the HTTP headers.

## Preparation

Ensure you have SSH access to your student VM and that your wis2box instance is up and running.

Make sure you are connected to the MQTT broker of your wis2box instance using MQTT Explorer. You can use the public credentials `everyone/everyone` to connect to the broker.

Ensure you have a web browser open with the wis2box-webapp for your instance by going to `http://<your-host>/wis2box-webapp`.

## Exercise 1: create a new dataset with data policy 'recommended'

Go to the 'dataset editor' page in the wis2box-webapp and create a new dataset. Use the same centre-id as in the previous practical sessions and use the template='surface-weather-observations/synop'. 

Click 'OK' to proceed.

In the dataset editor, set the data policy to 'recommended' (note that changing the data-policy will update the 'Topic Hierarchy').
Replace the auto-generated 'Local ID' with a descriptive name for the dataset, e.g. 'recommended-data-with-access-control':

<img alt="create-dataset-recommended" src="../../assets/img/create-dataset-recommended.png" width="800">

Continue to fill the required fields for Spatial Properties and Contact Information, and 'Validate form' to check for any errors.

Finally submit the dataset, using the previously create authentication token, and check that the new dataset is created in the wis2box-webapp.

Check MQTT-explorer to see that you receive the WIS2 Notification Message announcing the new Discovery Metadata record on the topic `origin/a/wis2/<your-centre-id>/metadata`.	

## Exercise 2: add an access token to the dataset

Login to the wis2box-management container,

```bash
cd ~/wis2box-1.0.0rc1
python3 wis2box-ctl.py login
```

From command line inside the container you can secure a dataset using the `wis2box auth add-token` command, using the flag `--metadata-id` to specify the metadata-identifier of the dataset and the access token as an argument.

For example, to add the access token `S3cr3tT0k3n` to the dataset with metadata-identifier `urn:wmo:md:not-my-centre:core.surface-based-observations.synop`:	

```bash
wis2box auth add-token --metadata-id urn:wmo:md:not-my-centre:reco.surface-based-observations.synop S3cr3tT0k3n
```

Exit the wis2box-management container:

```bash
exit
```

## Exercise 3: publish some data to the dataset

Copy the file `exercise-materials/access-control-exercises/aws-example2.csv` to the directory defined by `WIS2BOX_HOST_DATADIR` in your `wis2box.env`:

```bash
cp ~/exercise-materials/access-control-exercises/aws-example2.csv ~/wis2box-data
```

Then use WinSCP or a command line editor to edit the file `aws-example2.csv` and update the WIGOS-station-identifiers in the input-data to match the stations you have in your wis2box instance. 

Next, go to the station-editor in the wis2box-webapp. For each station you used in `aws-example2.csv`, update the 'topic' field to match the 'topic' of the dataset you created in the previous exercise.

This station will now be associated to 2 topics, one for the 'core' dataset and one for the 'recommended' dataset:

<img alt="edit-stations-add-topics" src="../../assets/img/edit-stations-add-topics.png" width="600">

You will need to use your token for `collections/stations` to save the updated station data.

Next, login to the wis2box-management container:

```bash
cd ~/wis2box-1.0.0rc1
python3 wis2box-ctl.py login
```

From the wis2box command line we can ingest the sample data file `aws-example2.csv` into a specific dataset as follows:

```bash
wis2box data ingest -p /data/wis2box/aws-example2.csv --metadata-id urn:wmo:md:not-my-centre:reco.surface-based-observations.synop
```

Make sure to provide the correct metadata-identifier for your dataset and **check that you receive WIS2 data-notifications in MQTT Explorer**, on the topic `origin/a/wis2/<your-centre-id>/data/recommended/surface-based-observations/synop`.

Check the canonical link in the WIS2 Notification Message and copy/paste the link to the browser to try and download the data.

You should see a 403 Forbidden error.

## Exercise 4: add the access token to HTTP headers to access the dataset

In order to demonstrate that the access token is required to access the dataset we will reproduce the error you saw in the browser using the command line function `wget`.

From the command line in your student VM, use the `wget` command with the canonical-link you copied from the WIS2 Notification Message.

```bash
wget <canonical-link>
```

You should see that the HTTP request returns with *401 Unauthorized* and the data is not downloaded.

Now add the access token to the HTTP headers to access the dataset.

```bash
wget --header="Authorization: Bearer S3cr3tT0k3n" <canonical-link>
```

Now the data should be downloaded successfully.

## Conclusion

!!! success "Congratulations!"
    In this practical session, you learned how to:

    - create a new dataset with data policy 'recommended'
    - add an access token to the dataset
    - validate the dataset can not be accessed without the access token
    - add the access token to HTTP headers to access the dataset

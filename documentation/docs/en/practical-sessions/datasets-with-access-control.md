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
    - add a custom license file hosted on your wis2box instance

## Introduction

Data are shared on WIS2 in accordance with the WMO Unified Data Policy which describes two categories of data:

- **core** : data that is provided on a free and unrestricted basis, without charge and with no conditions on use.
- **recommended** : data that may be provided with conditions on use and/or subject to a license.

Data that are shared as recommended:

- May be subject to conditions on use and reuse;
- May have access controls applied to the data;
- Are not cached within WIS2 by the Global Caches;
- Must have a link to a license specifying the conditions of use of the data included in the discovery metadata.

The dataset-editor in the wis2box-webapp will require you to provide a license URL when you select the data policy 'recommended'. Optionally, you can add an access token to such a dataset to restrict access to the data. 

In this practical session, you will create a new dataset with data policy 'recommended' and learn how to add access control.
It will also guide you through the steps to add a custom license file to your wis2box instance.

## Preparation

Ensure you have SSH access to your student VM and that your wis2box instance is up and running.

Make sure you are connected to the MQTT broker of your wis2box instance using MQTT Explorer. You can use the public credentials `everyone/everyone` to connect to the broker.

Ensure you have a web browser open with the wis2box-webapp for your instance by going to `http://YOUR-HOST/wis2box-webapp`.

## Create a new dataset with data policy 'recommended'

Go to the 'dataset editor' page in the wis2box-webapp and create a new dataset. Select the Data Type = 'weather/surface-weather-observations/synop'. 

<img alt="create-dataset-recommended" src="/../assets/img/create-dataset-template.png" width="800">

For "Centre ID", use the same as you used in the previous practical sessions.

Click 'CONTINUE TO FORM' to proceed.

Replace the auto-generated 'Local ID' with a descriptive name for the dataset, e.g. 'recommended-data-with-access-control', and update the 'Title' and 'Description' fields:

<img alt="create-dataset-recommended" src="/../assets/img/create-dataset-recommended.png" width="800">

Change the WMO data policy to 'recommended' and you will see that the form added a new input-field for a URL providing the License information for the dataset:

<img alt="create-dataset-license" src="/../assets/img/create-dataset-license.png" width="800">

You have the option to provide a URL to a license that describes the terms of use for the dataset. For example you could use
`https://creativecommons.org/licenses/by/4.0/`
to point to the Creative Commons Attribution 4.0 International (CC BY 4.0) license.

Or you can use `WIS2BOX_URL/data/license.txt` to point to a custom license file you hosted on your own webserver, where `WIS2BOX_URL` is the URL your defined in the wis2box.env file:

<img alt="create-dataset-license-url" src="/../assets/img/create-dataset-license-custom.png" width="800">

Continue to fill the required fields for Spatial Properties and Contact Information, and 'Validate form' to check for any errors.

Finally submit the dataset, using the previously created authentication token, and check that the new dataset is created in the wis2box-webapp.

Check MQTT Explorer to see that you receive the WIS2 Notification Message announcing the new Discovery Metadata record on the topic `origin/a/wis2/<your-centre-id>/metadata`.	

## Review your new dataset in the wis2box-api

View the list of datasets in the wis2box-api by opening the URL `WIS2BOX_URL/oapi/collections/discovery-metadata/items` in your web browser, replacing `WIS2BOX_URL` with the URL of your wis2box instance.

Open the link of the dataset you just created and scroll down to the 'links' section of the JSON response:

<img alt="wis2box-api-recommended-dataset-links" src="/../assets/img/wis2box-api-recommended-dataset-links.png" width="600">

You should see a link for "License for this dataset" pointing to the URL you provided in the dataset editor.

If you used `http://YOUR-HOST/data/license.txt` as the license URL, the link will currently not work, because we have not yet added a license file to the wis2box instance.

If time permits, you can add a custom license file to your wis2box instance at the end of this practical session. First, we will continue with adding an access token to the dataset.

## Add an access token to the dataset

Log in to the wis2box-management container,

```bash
cd ~/wis2box
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

## Publish some data to the dataset

Copy the file `exercise-materials/access-control-exercises/aws-example.csv` to the directory defined by `WIS2BOX_HOST_DATADIR` in your `wis2box.env`:

```bash
cp ~/exercise-materials/access-control-exercises/aws-example.csv ~/wis2box-data
```

Then use WinSCP or a command line editor to edit the file `aws-example.csv` and update the WIGOS-station-identifiers in the input-data to match the stations you have in your wis2box instance. 

Next, go to the station-editor in the wis2box-webapp. For each station you used in `aws-example.csv`, update the 'topic' field to match the 'topic' of the dataset you created in the previous exercise.

This station will now be associated to 2 topics, one for the 'core' dataset and one for the 'recommended' dataset:

<img alt="edit-stations-add-topics" src="/../assets/img/edit-stations-add-topics.png" width="600">

You will need to use your token for `collections/stations` to save the updated station data.

Next, log in to the wis2box-management container:

```bash
cd ~/wis2box
python3 wis2box-ctl.py login
```

From the wis2box command line we can ingest the sample data file `aws-example.csv` into a specific dataset as follows:

```bash
wis2box data ingest -p /data/wis2box/aws-example.csv --metadata-id urn:wmo:md:not-my-centre:reco.surface-based-observations.synop
```

Make sure to provide the correct metadata-identifier for your dataset and **check that you receive WIS2 data-notifications in MQTT Explorer**, on the topic `origin/a/wis2/<your-centre-id>/data/recommended/surface-based-observations/synop`.

Check the canonical link in the WIS2 Notification Message and copy/paste the link to the browser to try and download the data.

You should see a *401 Authorization Required*.

## Add the access token to HTTP headers to access the dataset

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

## Add a custom license file to your wis2box instance (optional)

Create a text file on your local machine using your favorite text editor and add some license information to the file, such as:

*This is a custom license file for the recommended dataset with access control.
You are free to use this data, but please acknowledge the data provider.*

To upload a locally created file license.txt, use the MinIO Console available at port 9001 of the wis2box instance, by going to a web browser and visiting `http://YOUR-HOST:9001`

The credentials to access the MinIO Console in the wis2box.env file are defined by `WIS2BOX_STORAGE_USERNAME` and `WIS2BOX_STORAGE_PASSWORD` environment variables.
You can find these in the wis2box.env file as follows:

```bash
cat wis2box.env | grep WIS2BOX_STORAGE_USERNAME
cat wis2box.env | grep WIS2BOX_STORAGE_PASSWORD
```

Once you have logged in to the MinIO Console, you can upload the license file into base path of the **wis2box-public** bucket using the “Upload” button:

<img alt="minio-upload-license" src="/../assets/img/minio-upload-license.png" width="800">

After uploading the license file, check if the file is accessible by visiting `WIS2BOX_URL/data/license.txt` in your web browser, replacing `WIS2BOX_URL` with the URL of your wis2box instance. 

!!! note

    The web-proxy in wis2box proxies all files stored in the "wis2box-public" bucket under the path `WIS2BOX_URL/data/`

The link for "License for this dataset" included in the metadata of your recommended dataset should now work.

## Conclusion

!!! success "Congratulations!"
    In this practical session, you learned how to:

    - create a new dataset with data policy 'recommended'
    - add an access token to the dataset
    - validate the dataset can not be accessed without the access token
    - add the access token to HTTP headers to access the dataset
    - add a custom license file to your wis2box instance

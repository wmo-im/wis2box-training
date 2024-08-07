---
title: Configuring datasets in wis2box
---

# Configuring datasets in wis2box

!!! abstract "Learning outcomes"
    By the end of this practical session, you will be able to:

    - create a new dataset
    - create discovery metadata for a dataset
    - configure data mappings for a dataset
    - publish a WIS2 notification with a WCMP2 record
    - update and re-publish your dataset

## Introduction

The wis2box uses datasets that are associated with discovery metadata and data mappings.

The discovery metadata is used to create a WCMP2 record that is shared using a WIS2 notification published on your wis2box-broker.

The data mappings are used to associate a data plugin to your input data, allowing your data to be transformed prior to being published using the WIS2 notification.

This session will walk you through creating a new dataset, creating discovery metadata, and configuring data mappings. You will inspect your dataset in the wis2box-api and review the WIS2 notification for your discovery metadata.

## Preparation

Connect to your broker using MQTT Explorer. Instead of using your internal broker credentials, use the public credentials `everyone/everyone`:

<img alt="MQTT Explorer: Connect to broker" src="../../assets/img/mqtt-explorer-wis2box-broker-everyone-everyone.png" width="800">

!!! Note

    The `everyone/everyone` credentials enable read-only access on the topic 'origin/a/wis2/#'. This is the topic where the WIS2 notifications are published. The Global Broker can subscribe with these public credentials to receive the notifications. The 'everyone' user will not see internal topics or be able to publish messages.

Open a browser and open a page to `http://<your-host>/wis2box-webapp`. Make sure you are logged in and can access the 'dataset editor' page.

See the section on [Initializing wis2box](/practical-sessions/initializing-wis2box)
if you need to remember how to connect to the broker or access the wis2box-webapp.

You will need an authorization token for the 'processes/wis2box' endpoint to publish your dataset. 

To create an authorization token first login to the wis2box-management container:

```bash
cd ~/wis2box-1.0b8
python3 wis2box-ctl.py login
```

Then run the following command to create an authorization token for the 'processes/wis2box' endpoint:

```bash
wis2box auth add-token --path processes/wis2box
```

Then exit the container:

```bash
exit
```

## Initializing the dataset editor form using a template

On the 'dataset editor' page, under the 'Datasets' tab, click on "Create New ...":

<img alt="Create New Dataset" src="../../assets/img/wis2box-create-new-dataset.png" width="800">

A pop-up window will appear, asking you to provide:

- `Centre Id' : this is the agency acronym (in lower case and no spaces), as specified by the WMO Member, that identifies the data centre responsible for publishing the data.
- Data Type: The type of data you are creating metadata for. You can choose between using a predefined template or selecting 'other'.  If 'other' is selected, more fields will have to be manually filled.

!!! Note

    Your centre-id should start with the ccTLD of your country, followed by a - and an abbreviated name of your organization, for example fr-meteofrance. The centre-id has to be lowercase and use alphanumeric characters only. The dropdown list shows all currently registered centre-ids on WIS2 as well as any centre-id you have already created in wis2box.

Please choose a centre-id appropriate for your organization. For 'Data Type', select 'weather/surface-based-observations/synop':

<img alt="Create New Dataset Form: Initial information" src="../../assets/img/wis2box-create-new-dataset-form-initial.png" width="800">

Click 'continue to form' to proceed, you will now be presented with the 'Dataset Editor Form'.

## Creating discovery metadata

The 'Dataset Editor Form' allows you to provide the Discovery Metadata for your dataset that the wis2box-management container will use to publish a WCMP2 record.

Since you have selected the 'weather/surface-based-observations/synop' data type, the form will be pre-populated with some default values.

Review the title, description, and keywords, and update them as necessary:

<img alt="Metadata Editor: title, description, keywords" src=""../../assets/img/wis2box-metadata-editor-part1.png" width="800">

Note there are options to change the 'WMO Data Policy' from 'core' to 'recommended' or to modify your default Metadata Identifier, please leave these as they are.

Next, review the section defining your 'Temporal Properties' and 'Spatial Properties'. You can adjust the bounding box by updating the 'North Latitude', 'South Latitude', 'East Longitude', and 'West Longitude' fields:

<img alt="Metadata Editor: temporal properties, spatial properties" src="../../assets/img/wis2box-metadata-editor-part2.png" width="800">

Next, fill out the section defining the 'Contact Information of the Data Provider':

<img alt="Metadata Editor: contact information" src="../../assets/img/wis2box-metadata-editor-part3.png" width="800">

Finally, fill out the section defining the 'Data Quality Information':

Once you are done filling out all the sections, click 'VALIDATE FORM' and check the form for any errors:

<img alt="Metadata Editor: validation" src="../../assets/img/wis2box-metadata-validation-error.png" width="800">

Making sure you have no errors and that you get a pop-up indication your form has been validated:

<img alt="Metadata Editor: validation success" src="../../assets/img/wis2box-metadata-validation-success.png" width="800">

This finishes the creation of the discovery metadata for your dataset. Next you will configure the data mappings.

## Configuring data mappings

Since you used a template to create your dataset, several data mappings have already been created for you:

<img alt="Data Mappings: update plugin" src="../../assets/img/wis2box-data-mappings.png" width="800">

You can click on the "update"-button to change settings for the plugin such as file-extension and the file-pattern.

You can leave the default settings for now. 

## Submitting your dataset

Finally, you can click 'submit' to publish your dataset. 

You will need to provide the authorization token for 'processes/wis2box' that you created earlier.

Check that you get the following message after submitting your dataset, indicating that the dataset was successfully submitted:

<img alt="Submit Dataset Success" src="../../assets/img/wis2box-submit-dataset-success.png" width="400">

After you click 'OK', you are redirected to the Dataset Editor home page. Now if you click on the 'Dataset' tab, you should see your new dataset listed:

<img alt="Dataset Editor: new dataset" src="../../assets/img/wis2box-dataset-editor-new-dataset.png" width="800">

## Reviewing the WIS2-notification for your discovery metadata

Go to MQTT-explorer, if you were connected to the broker, you should see a new WIS2 notification published on the topic 'origin/a/wis2/<your-centre-id>/metadata':

<img alt="MQTT Explorer: WIS2 notification" src="../../assets/img/mqtt-explorer-wis2-notification-metadata.png" width="800">

Inspect the content of the WIS2 notification you published. You should see a JSON with a structure corresponding to the WIS Notification Message (WNM) format.

!!! question
    
    Try to find the title, description and keywords you provided in the discovery metadata in the WIS2 notification.  Can you find them?

??? success "Click to reveal answer"

    The title, description, and keywords you provided in the discovery metadata are not present in the WIS2 notification !
    
    The WIS2 notification contains a canonical link to the WCMP2 record that was published. If you copy-paste this link into a browser, you will download the WCMP2 record and see the title, description, and keywords you provided.

## Reviewing your dataset in the wis2box-ui

Navigate to `http://<your-host>` you should now see some new content:

<img alt="wis2box-ui: new dataset" src="../../assets/img/wis2box-ui-new-dataset.png" width="800">

If you click on "discovery metadata" a new page will open showing the metadata you provided in the wis2box-api:

<img alt="wis2box-ui: discovery metadata" src="../../assets/img/wis2box-api-discovery-metadata.png" width="800">

Note that the "explore"-option or clicking on the map will lead to an error being shown, as there are no stations associated with this dataset yet.

## Conclusion

!!! success "Congratulations!"
    In this practical session, you learned how to:

    - create a new dataset
    - define your discovery metadata
    - review your data mappings
    - publish discovery metadata
    - review the WIS2 notification for your discovery metadata

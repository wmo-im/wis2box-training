---
title: Configuring datasets in wis2box
---

# Configuring datasets in wis2box

!!! abstract "Learning outcomes"
    By the end of this practical session, you will be able to:

    - use the wis2box-webapp dataset editor
    - create new datasets using Template=*weather/surface-based-observations/synop* and Template=*other*
    - define your discovery metadata
    - review your data mappings
    - publish a WIS2 notification for your discovery metadata

## Introduction

wis2box uses **datasets** that are associated with **discovery metadata** and **data mappings**.

**Discovery metadata** is used to create a WCMP2 (WMO Core Metadata Profile 2) record that is shared using a WIS2 notification published on your wis2box-broker.

**Data mappings** are used to associate data plugins to your input data, allowing your data to be transformed prior to being published on WIS2.

In this practical session, you will learn how to create and configure datasets using the **wis2box-webapp dataset editor**.
 
!!! note "Configuring datasets without using the wis2box-webapp"

    wis2box also supports configuring datasets using the [metadata control file (MCF)](https://geopython.github.io/pygeometa/reference/mcf) format.
    
    Using MCF allows you more flexibility and control but can be more error-prone as you need to ensure that the MCF is correctly formatted and adheres to the required schema.
    
    MCF-files can be published from the command line in the wis2box-management container. See the [wis2box documentation](https://docs.wis2box.wis.wmo.int/en/latest/reference/running/discovery-metadata.html) for more information.

## Preparation

Connect to your broker using MQTT Explorer. 

Instead of using your internal broker credentials, use the public credentials `everyone/everyone`:

<img alt="MQTT Explorer: Connect to broker" src="/../assets/img/mqtt-explorer-wis2box-broker-everyone-everyone.png" width="800">

!!! Note

    You never need to share the credentials of your internal broker with external users. The 'everyone' user is a public user to enable sharing of WIS2 notifications.

    The `everyone/everyone` credentials have read-only access on the topic 'origin/a/wis2/#'. This is the topic where the WIS2 notifications are published. The Global Broker can subscribe with these public credentials to receive the notifications.
    
    The 'everyone' user will not see internal topics or be able to publish messages.
    
Open a browser and go to `http://YOUR-HOST/wis2box-webapp`. Make sure you are logged in and can access the 'dataset editor' page.

See the section on [Initializing wis2box](./initializing-wis2box.md) if you need to remember how to connect to the broker or access the wis2box-webapp.

## Create an authorization token for processes/wis2box

You will need an authorization token for the 'processes/wis2box' endpoint to publish your dataset. 

To create an authorization token, access your training VM over SSH and use the following commands:

```bash
cd ~/wis2box
python3 wis2box-ctl.py login
```

Then run the following command to create a randomly generated authorization token for the 'processes/wis2box' endpoint:

```bash
wis2box auth add-token --path processes/wis2box
```

You can also create a token with a specific value by providing the token as an argument to the command:

```bash
wis2box auth add-token --path processes/wis2box MyS3cretToken
```

Make sure to copy the token value and store it on your local machine, as you will need it later.

Once you have your token, you can exit the wis2box-management container:

```bash
exit
```

## The wis2box-webapp dataset editor

Navigate to the 'dataset editor' page in the wis2box-webapp of your wis2box instance by going to `http://YOUR-HOST/wis2box-webapp` and selecting 'dataset editor' from the menu on the left-hand side.

On the 'dataset editor' page, under the 'Datasets' tab, click on "Create New ...":

<img alt="Create New Dataset" src="/../assets/img/wis2box-create-new-dataset.png" width="800">

A pop-up window will appear, asking you to provide:

- **Centre ID**: this is the agency acronym (in lower case and no spaces), as specified by the WMO Member, that identifies the data centre responsible for publishing the data.
- **Template**: The type of data you are creating metadata for. You can choose between using a predefined template or selecting *other*.

<img alt="Create New Dataset pop up" src="/../assets/img/wis2box-create-new-dataset-pop-up.png" width="600">

!!! Note "Centre ID"

    Your Centre ID should start with the TLD of your country, followed by a dash (`-`) and an abbreviated name of your organization (for example `fr-meteofrance`). The Centre ID must be lowercase and use alphanumeric characters only. The dropdown list shows all currently registered Centre IDs on WIS2 as well as any Centre ID you have already created in wis2box. Please choose a Centre ID appropriate for your organization.

!!! Note "Template"

    The *Template* field allows you to select from a list of templates available in the wis2box-webapp dataset editor. A template will pre-populate the form with suggested default values appropriate for the data type. This includes suggested title and keywords for the metadata and pre-configured data plugins. 
    
    The topic is automatically set to the default topic linked to the selected template unless you select *other*. If you select *other*, the topic can be defined from a dropdown list based on the [WIS2 Topic Hierarchy](https://codes.wmo.int/wis/topic-hierarchy/_earth-system-discipline).

For the purpose of the training, you will create two datasets:
    
- A dataset using Template=*weather/surface-based-observations/synop*, which includes data plugins that transform the data into BUFR format before publication.
- A dataset using Template=*other*, where you are responsible for defining the WIS2 Topic and where you will use the "Universal" plugin to publish the data without transformation.

## Template=weather/surface-based-observations/synop

For **Template**, select **weather/surface-based-observations/synop**:

<img alt="Create New Dataset Form: Initial information" src="/../assets/img/wis2box-create-new-dataset-form-initial.png" width="450">

Click *continue to form* to proceed. You will now be presented with the **Dataset Editor Form**.

Since you selected the **weather/surface-based-observations/synop** template, the form will be pre-populated with some initial values related to this data type.

### Creating discovery metadata

The Dataset Editor Form allows you to provide the Discovery Metadata for your dataset that the wis2box-management container will use to publish a WCMP2 record.

Since you have selected the 'weather/surface-based-observations/synop' template, the form will be pre-populated with some default values.

Please make sure to replace the auto-generated 'Local ID' with a descriptive name for your dataset, e.g., 'synop-dataset-wis2training':

<img alt="Metadata Editor: title, description, keywords" src="/../assets/img/wis2box-metadata-editor-part1.png" width="800">

Review the title and keywords, update them as necessary, and provide a description for your dataset.

Note, there are options to change the 'WMO Data Policy' from 'core' to 'recommended' or to modify your default Metadata Identifier. Please keep data policy as 'core' and use the default Metadata Identifier.

Next, review the section defining your 'Temporal Properties' and 'Spatial Properties'. You can adjust the bounding box by updating the 'North Latitude', 'South Latitude', 'East Longitude', and 'West Longitude' fields:

<img alt="Metadata Editor: temporal properties, spatial properties" src="/../assets/img/wis2box-metadata-editor-part2.png" width="800">

Next, fill out the section defining the 'Contact Information of the Data Provider':

<img alt="Metadata Editor: contact information" src="/../assets/img/wis2box-metadata-editor-part3.png" width="800">

Finally, fill out the section defining the 'Data Quality Information':

Once you are done filling out all the sections, click 'VALIDATE FORM' and check the form for any errors:

<img alt="Metadata Editor: validation" src="/../assets/img/wis2box-metadata-validation-error.png" width="800">

If there are any errors, correct them and click 'VALIDATE FORM' again.

Make sure you have no errors and that you get a pop-up indicating your form has been validated:

<img alt="Metadata Editor: validation success" src="/../assets/img/wis2box-metadata-validation-success.png" width="800">

Next, before submitting your dataset, review the data mappings for your dataset.

### Configuring data mappings

Since you used a template to create your dataset, the dataset mappings have been pre-populated with the default plugins for the 'weather/surface-based-observations/synop' template. Data plugins are used in the wis2box to transform data before it is published using the WIS2 notification.

<img alt="Data Mappings: update plugin" src="/../assets/img/wis2box-data-mappings.png" width="800">

Note that you can click on the "Update" button to change settings for the plugin such as file extension and the file pattern. You can leave the default settings for now.

### Submitting your dataset

Finally, you can click 'submit' to publish your dataset. 

You will need to provide the authorization token for 'processes/wis2box' that you created earlier. If you have not done so, you can create a new token by following the instructions in the preparation section.

Check that you get the following message after submitting your dataset, indicating that the dataset was successfully submitted:

<img alt="Submit Dataset Success" src="/../assets/img/wis2box-submit-dataset-success.png" width="400">

After you click 'OK', you are redirected to the Dataset Editor home page. Now if you click on the 'Dataset' tab, you should see your new dataset listed:

<img alt="Dataset Editor: new dataset" src="/../assets/img/wis2box-dataset-editor-new-dataset.png" width="800">

### Reviewing the WIS2 notification for your discovery metadata

Go to MQTT Explorer. If you were connected to the broker, you should see a new WIS2 notification published on the topic `origin/a/wis2/<your-centre-id>/metadata`:

<img alt="MQTT Explorer: WIS2 notification" src="/../assets/img/mqtt-explorer-wis2-notification-metadata.png" width="800">

Inspect the content of the WIS2 notification you published. You should see a JSON with a structure corresponding to the WIS Notification Message (WNM) format.

!!! question

    On what topic is the WIS2 notification published?

??? success "Click to reveal answer"

    The WIS2 notification is published on the topic `origin/a/wis2/<your-centre-id>/metadata`.

!!! question
    
    Try to find the title, description, and keywords you provided in the discovery metadata in the WIS2 notification. Can you find them?

??? success "Click to reveal answer"

    **The title, description, and keywords you provided in the discovery metadata are not present in the WIS2 notification payload!** 
    
    Instead, try to look for the canonical link in the "links" section in the WIS2 notification:

    <img alt="WIS2 notification for metadata, links sections" src="/../assets/img/wis2-notification-metadata-links.png" width="800">

    **The WIS2 notification contains a canonical link to the WCMP2 record that was published.** 
    
    Copy-paste this canonical link into your browser to access the WCMP2 record. Depending on your browser settings, you may be prompted to download the file or it may be displayed directly in your browser.

    You will find the title, description, and keywords you provided inside the WCMP2 record.

wis2box provides only a limited number of predefined templates. These templates are designed for common types of datasets, but they may not always match specialized data. For all other types of datasets, you can create your dataset by selecting Template=*other*.

## Template=other

Next, we will create a 2nd dataset using Template=*other*.

Click on "Create New ..." again to create a new dataset. Use the same centre-id you used before, it should be available in the dropdown list. For **Template**, select **other**:

<img alt="Create New Dataset Form: Initial information" src="/../assets/img/wis2box-create-new-dataset-form-initial-other.png" width="450">

Click *continue to form* to proceed, you will now be presented with the **Dataset Editor Form** again.

### Creating discovery metadata

Provide your own values for the 'Title' and 'Description' fields and make sure to replace the auto-generated 'Local ID' with a descriptive name for your dataset:

<img alt="Metadata Editor: title, description, keywords" src="/../assets/img/wis2box-metadata-editor-part1-other.png" width="800">

Note that since you selected Template=*other* it is up to you to define the WIS2 Topic Hierarchy using the dropdown lists for 'Discipline' and 'Sub-Discipline'.

For this exercise please select Sub-Discipline Topic "prediction/analysis/medium-range/deterministic/global":

<img alt="Metadata Editor: title, description, keywords" src="/../assets/img/wis2box-metadata-editor-part1-other-topic.png" width="800">

Since you used Template=*other*, no keywords were predefined. Make sure you add at least 3 keywords of your own choice:

<img alt="Metadata Editor: title, description, keywords" src="/../assets/img/wis2box-metadata-editor-part1-other-2.png" width="800">

After filling out the required fields, fill out the remaining sections of the form, including 'Temporal Properties', 'Spatial Properties' and 'Contact Information of the Data Provider' and make sure to validate the form.

### Configuring data mappings

When Template=other is used, no default data mappings are provided. As a result, the Dataset Mappings Editor will be empty and users must configure the mappings according to their specific requirements.

<img alt="Data Mappings: update plugin" src="/../assets/img/wis2box-data-mappings-other1.png" width="800">

Click "ADD A PLUGIN +" to add a data plugin to your dataset.

Select the plugin with name **"Universal data without conversion"**. This plugin is designed to publish data without applying any transformation.

When adding this plugin, you will need to specify the **File Extension** and a **File Pattern** (defined by a regular expression) that matches the naming pattern of your data files. In the case of the "Universal"-plugin, the File Pattern is also used to determine "datetime"-property for the data.

!!! Note "Parsing datetime from filename"

    The "Universal"-plugin assumes that the first group in the regular expression corresponds to the datetime of the data. 

    The default File Pattern is `^.*?_(\d{8}).*?\..*$` which matches on 8-digits preceded by an underscore and followed by any characters and a dot before the file extension. For example:

    - `mydata_20250101.txt` will match and extract 25th January 2025 as the datetime-property for the data
    - `mydata_2025010112.txt` will not match, as there are 10 digits instead of 8
    - `mydata-20250101.txt` will not match, as there is a hyphen instead of an underscore before the date

    When ingesting data using the "Universal"-plugin either rename your files to match the default or update the File Pattern ensuring that the first group in the regular expression corresponds to the datetime.

Keep the default values for "File Name" a for now as they match the data you will ingest in the next practical session:

<img alt="Data Mappings: update plugin" src="/../assets/img/wis2box-data-mappings-other2.png" width="800">

Click "SAVE" to save the plugin settings and verify you now see the plugin listed in the Dataset Mappings Editor:

<img alt="Data Mappings: update plugin" src="/../assets/img/wis2box-data-mappings-other3.png" width="800">

Note that when you will ingest data the File extension and File Pattern of the filename must match the settings you have provided here, otherwise the data will not be processed and the wis2box-management container will log ERROR messages.

### Submit and review the result

Finally provide the authorization token for 'processes/wis2box' that you created earlier and click 'submit' to publish your dataset.

After a successful submission, your new dataset will appear in the Dataset tab:

<img alt="Dataset Editor: new dataset" src="/../assets/img/wis2box-dataset-editor-new-dataset-other.png" width="800">

Go to MQTT Explorer, if you were connected to your broker, you should see another new WIS2 notification published on the topic `origin/a/wis2/<your-centre-id>/metadata`.

!!! question
    
    Visit the wis2box-UI at `http://YOUR-HOST`.
    
    How many datasets do you see listed? How can you view the WIS2 Topic Hierarchy used for each dataset and how can you see the description of each dataset?

??? success "Click to reveal answer"

    By opening the wis2box UI at `http://YOUR-HOST` you should see 2 datasets listed along with their WIS2 Topic Hierarchy. To see the description of each dataset you can click on "metadata" which will redirect to the corresponding 'discovery-metadata'-item as served by the wis2box-api.

!!! question

    Try to update the description of the last dataset you created. After updating the description, do you see a new WIS2 notification published on the topic `origin/a/wis2/<your-centre-id>/metadata`? What is the difference between the new notification and the previous one?

??? success "Click to reveal answer"

    You should see a new data notification message being sent after updating your dataset on the topic `origin/a/wis2/<your-centre-id>/metadata`.
    
    In the message, the value of *"rel": "canonical"* will change to *"rel": "update"*, indicating that previously published data has been modified. To view the updated description, copy-paste the URL into your browser and you should see the updated description.

!!! question

    Try to update the Topic Hierarchy of the last dataset you created by changing the selection in "Sub-Discipline Topics". Do you see a new WIS2 notification published on the topic `origin/a/wis2/<your-centre-id>/metadata`?

??? success "Click to reveal answer"

    You are **not** able to update the Topic Hierarchy of an existing dataset. The Topic Hierarchy field is disabled in the Dataset Editor Form after the dataset has been created. If you want to use a different Topic Hierarchy, first delete the existing dataset and then create a new dataset with the desired Topic Hierarchy.

## Conclusion

!!! success "Congratulations!"
    In this practical session, you learned how to:

    - use the wis2box-webapp dataset editor
    - create new datasets using Template=*weather/surface-based-observations/synop* and Template=*other*
    - define your discovery metadata
    - review your data mappings
    - publish discovery metadata and review the WIS2 notification

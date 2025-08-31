---
title: Configuring datasets in wis2box
---

# Configuring datasets in wis2box

!!! abstract "Learning outcomes"
    By the end of this practical session, you will be able to:

    - Create new datasets using the default template and your customized template
    - create discovery metadata for your dataset
    - configure data mappings for your dataset
    - publish a WIS2 notification with a WCMP2 record
    - update and re-publish your dataset

## Introduction

wis2box uses datasets that are associated with discovery metadata and data mappings.

Discovery metadata is used to create a WCMP2 (WMO Core Metadata Profile 2) record that is shared using a WIS2 notification published on your wis2box-broker.

The data mappings are used to associate a data plugin to your input data, allowing your data to be transformed prior to being published using the WIS2 notification.

This session will walk you through create new datasets using the default template and your customized template, creating discovery metadata, and configuring data mappings. You will inspect your datasets in the wis2box-api and review the WIS2 notification for your discovery metadata.

## Preparation

Connect to your broker using MQTT Explorer. 

Instead of using your internal broker credentials, use the public credentials `everyone/everyone`:

<img alt="MQTT Explorer: Connect to broker" src="/../assets/img/mqtt-explorer-wis2box-broker-everyone-everyone.png" width="800">

!!! Note

    You never need to share the credentials of your internal broker with external users. The 'everyone' user is a public user to enable sharing of WIS2 notifications.

    The `everyone/everyone` credentials has read-only access on the topic 'origin/a/wis2/#'. This is the topic where the WIS2 notifications are published. The Global Broker can subscribe with these public credentials to receive the notifications.
    
    The 'everyone' user will not see internal topics or be able to publish messages.
    
Open a browser and open a page to `http://YOUR-HOST/wis2box-webapp`. Make sure you are logged in and can access the 'dataset editor' page.

See the section on [Initializing wis2box](./initializing-wis2box.md) if you need to remember how to connect to the broker or access the wis2box-webapp.

## Create an authorization token for processes/wis2box

You will need an authorization token for the 'processes/wis2box' endpoint to publish your dataset. 

To create an authorization token, access your training VM over SSH and use the following commands to login to the wis2box-management container:

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

## Creating new datasets in the wis2box-webapp

Navigate to the 'dataset editor' page in the wis2box-webapp of your wis2box instance by going to `http://YOUR-HOST/wis2box-webapp` and selecting 'dataset editor' from the menu on the left hand side.

On the 'dataset editor' page, under the 'Datasets' tab, click on "Create New ...":

<img alt="Create New Dataset" src="/../assets/img/wis2box-create-new-dataset.png" width="800">

A pop-up window will appear, asking you to provide:

- **Centre ID** : this is the agency acronym (in lower case and no spaces), as specified by the WMO Member, that identifies the data centre responsible for publishing the data.
- **Template**: The template corresponding to the type of data you are creating metadata for. You can choose between using a predefined template or selecting 'other'.  If 'other' is selected, it means you want to define a custom template, and therefore additional fields must be filled in manually. 

<img alt="Create New Dataset pop up" src="/../assets/img/wis2box-create-new-dataset-pop-up.png" width="600">

!!! Note "Centre ID"

    Your centre-id should start with the TLD of your country, followed by a dash (`-`) and an abbreviated name of your organization (for example `fr-meteofrance`). The centre-id must be lowercase and use alphanumeric characters only. The dropdown list shows all currently registered centre-ids on WIS2 as well as any centre-id you have already created in wis2box. Please choose a centre-id appropriate for your organization.

!!! Note "Template"

    The *Template* field allows you to select from a list of templates available in the wis2box-webapp dataset editor. A template will pre-populate the form with suggested default values appropriate for the data type. This includes suggested title and keywords for the metadata and pre-configured data plugins. The topic is automatically set to the default topic linked to the selected template.

    For the purpose of the training，we will work with two options when creating new datasets:
    
    1. The predefined *weather/surface-based-observations/synop* template, which includes data plugins that transform the data into BUFR format before publication;
    2. The *other* template, which allows you to define your own custom template by manually filling in the required fields.

    If you want to publish CAP alerts using wis2box, use the template *weather/advisories-warnings*. This template includes a data plugin that verifies the input data is a valid CAP alert before publishing. To create CAP alerts and publish them via wis2box you can use the [WMO CAP Composer](https://github.com/World-Meteorological-Organization/cap-composer) or forward the CAP XML from your own system into the wis2box-incoming bucket.

Now, let’s create a new dataset by using predefined template.

## Create a new dataset by using predefined template

For **Template**, select **weather/surface-based-observations/synop**:

<img alt="Create New Dataset Form: Initial information" src="/../assets/img/wis2box-create-new-dataset-form-initial.png" width="450">

Click *continue to form* to proceed, you will now be presented with the **Dataset Editor Form**.

Since you selected the **weather/surface-based-observations/synop** template, the form will be pre-populated with some initial values related to this data type.

### Creating discovery metadata

The Dataset Editor Form allows you to provide the Discovery Metadata for your dataset that the wis2box-management container will use to publish a WCMP2 record.

Since you have selected the 'weather/surface-based-observations/synop' template, the form will be pre-populated with some default values.

Please make sure to replace the auto-generated 'Local ID' with a descriptive name for your dataset, e.g. 'synop-dataset-wis2training':

<img alt="Metadata Editor: title, description, keywords" src="/../assets/img/wis2box-metadata-editor-part1.png" width="800">

Review the title and keywords, and update them as necessary, and provide a description for your dataset.

Note there are options to change the 'WMO Data Policy' from 'core' to 'recommended' or to modify your default Metadata Identifier, please keep data-policy as 'core' and use the default Metadata Identifier.

Next, review the section defining your 'Temporal Properties' and 'Spatial Properties'. You can adjust the bounding box by updating the 'North Latitude', 'South Latitude', 'East Longitude', and 'West Longitude' fields:

<img alt="Metadata Editor: temporal properties, spatial properties" src="/../assets/img/wis2box-metadata-editor-part2.png" width="800">

Next, fill out the section defining the 'Contact Information of the Data Provider':

<img alt="Metadata Editor: contact information" src="/../assets/img/wis2box-metadata-editor-part3.png" width="800">

Finally, fill out the section defining the 'Data Quality Information':

Once you are done filling out all the sections, click 'VALIDATE FORM' and check the form for any errors:

<img alt="Metadata Editor: validation" src="/../assets/img/wis2box-metadata-validation-error.png" width="800">

If there are any errors, correct them and click 'VALIDATE FORM' again.

Making sure you have no errors and that you get a pop-up indication your form has been validated:

<img alt="Metadata Editor: validation success" src="/../assets/img/wis2box-metadata-validation-success.png" width="800">

Next, before submitting your dataset, review the data mappings for your dataset.

### Configuring data mappings

Since you used a template to create your dataset, the dataset mappings have been pre-populated with the defaults plugins for the 'weather/surface-based-observations/synop' template. Data plugins are used in the wis2box to transform data before it is published using the WIS2 notification.

<img alt="Data Mappings: update plugin" src="/../assets/img/wis2box-data-mappings.png" width="800">

Note that you can click on the "update"-button to change settings for the plugin such as file-extension and the file-pattern, you can leave the default settings for now. This will be explained in more detail later when creating a custom dataset.

### Submitting your dataset

Finally, you can click 'submit' to publish your dataset. 

You will need to provide the authorization token for 'processes/wis2box' that you created earlier. If you have not done so, you can create a new token by following the instructions in the preparation section.

Check that you get the following message after submitting your dataset, indicating that the dataset was successfully submitted:

<img alt="Submit Dataset Success" src="/../assets/img/wis2box-submit-dataset-success.png" width="400">

After you click 'OK', you are redirected to the Dataset Editor home page. Now if you click on the 'Dataset' tab, you should see your new dataset listed:

<img alt="Dataset Editor: new dataset" src="/../assets/img/wis2box-dataset-editor-new-dataset.png" width="800">

### Reviewing the WIS2-notification for your discovery metadata

Go to MQTT Explorer, if you were connected to the broker, you should see a new WIS2 notification published on the topic `origin/a/wis2/<your-centre-id>/metadata`:

<img alt="MQTT Explorer: WIS2 notification" src="/../assets/img/mqtt-explorer-wis2-notification-metadata.png" width="800">

Inspect the content of the WIS2 notification you published. You should see a JSON with a structure corresponding to the WIS Notification Message (WNM) format.

!!! question

    On what topic is the WIS2 notification published?

??? success "Click to reveal answer"

    The WIS2 notification is published on the topic `origin/a/wis2/<your-centre-id>/metadata`.

!!! question
    
    Try to find the title, description and keywords you provided in the discovery metadata in the WIS2 notification.  Can you find them?

??? success "Click to reveal answer"

    **The title, description, and keywords you provided in the discovery metadata are not present in the WIS2 notification payload!** 
    
    Instead, try to look for the canonical link  in the "links"-section in the WIS2 notification:

    <img alt="WIS2 notification for metadata, links sections" src="/../assets/img/wis2-notification-metadata-links.png" width="800">

    **The WIS2 notification contains a canonical link to the WCMP2 record that was published.** 
    
    Copy-paste this canonical link into your browser to access the WCMP2 record, depending on your browser settings, you may be prompted to download the file or it may be displayed directly in your browser.

    You will find the title, description, and keywords your provided inside the WCMP2 record.

wis2box provides only a limited number of predefined templates. These templates are designed for common types of datasets, but they may not always match specialized data. When predefined templates are not suitable, a custom template can be created. This allows users to define the required metadata fields according to their dataset.

In the next section, we will create a new dataset and show how to configure it using a custom template.

## Create a new dataset by configuring your customized template

For **Template**, select **other**:

<img alt="Create New Dataset Form: Initial information" src="/../assets/img/wis2box-create-new-dataset-form-initial-other.png" width="450">

Click *continue to form* to proceed, you will now be presented with the **Dataset Editor Form**.

Since the *other* template was selected, the next step is to click *Continue* to form to proceed. You will now be presented with the Dataset Editor Form. Within this form, key fields such as Title, Description, Sub-discipline topics, and Keywords must be completed or reviewed by the user. The Experimental (free text topic) option controls how Sub-discipline topics are defined: if this option is selected, Sub-discipline topics can be entered as free text, allowing the user to define a custom topic. If the option is not selected, Sub-discipline topics is presented as a drop-down list, and one of the predefined options must be chosen.

### Creating customized discovery metadata

At this stage, you will need to complete the required fields in the Dataset Editor Form, including Title, Description, Local ID, Sub-discipline topics, and Keywords. 

For the purpose of this training, we will complete these fields using a customized Global Ensemble Prediction System (GEPS) dataset template as an example. This example serves only as a reference — in real WIS2 operations, users should customize the metadata fields according to the requirements of their own datasets.

<img alt="Metadata Editor: title, description, keywords" src="/../assets/img/wis2box-metadata-editor-part1-other.png" width="800">

<img alt="Metadata Editor: title, description, keywords" src="/../assets/img/wis2box-metadata-editor-part1-other-2.png" width="800">

The subsequent steps are the same as when creating a dataset with the predefined synop template. For detailed instructions, please refer to the *Creating discovery metadata* section under *Create a new dataset by using a predefined template*. 

### Configuring customized data mappings

When a custom template is used, no default data mappings are provided. As a result, the Dataset Mappings Editor will be empty and users must configure the mappings according to their specific requirements.

<img alt="Data Mappings: update plugin" src="/../assets/img/wis2box-data-mappings-other1.png" width="800">

In this training, we will customize a GEPS dataset and use the universal data without conversion plugin as an example. This plugin is designed to publish data without applying any transformation. Since GEPS data is delivered in GRIB2 format, the file extension must be set to .grib2; otherwise, the data cannot be published successfully.

Special attention should be given to the Regex field, as it directly affects data ingestion. If the regular expression does not match the naming pattern of the data files, publishing errors will occur. To avoid this, either update the regex to match your dataset naming convention, or leave the default regex unchanged and ensure that your data files are renamed accordingly.

<img alt="Data Mappings: update plugin" src="/../assets/img/wis2box-data-mappings-other2.png" width="800">

In actual WIS2 operations, users may choose different plugins depending on their requirements; here we use the universal data without conversion plugin only as an example.

If you want to publish other types and formats of data, you can click on the "update" button to change settings such as the file-extension and file-pattern.

<img alt="Data Mappings: update plugin" src="/../assets/img/wis2box-data-mappings-other3.png" width="800">

### Submitting your customized dataset

The submission process is the same as described in the *Submitting your dataset* section under *Create a new dataset by using a predefined template*. Please refer to that section for detailed instructions.

After a successful submission, your new dataset will appear in the Dataset tab:

<img alt="Dataset Editor: new dataset" src="/../assets/img/wis2box-dataset-editor-new-dataset-other.png" width="800">

### Reviewing the WIS2-notification for your discovery metadata

Go to MQTT Explorer, if you were connected to the broker, you should see a new WIS2 notification published on the topic `origin/a/wis2/<your-centre-id>/metadata`:

<img alt="MQTT Explorer: WIS2 notification" src="/../assets/img/mqtt-explorer-wis2-notification-metadata-other.png" width="800">

!!! question
    
    What is the Metadata Identifier of the customized GEPS dataset you created?

??? success "Click to reveal answer"

    By opening the wis2box UI, you can view the customized GEPS dataset. The Metadata Identifier is:

    *urn:wmo:md:nl-knmi-test:customized-geps-dataset-wis2-training*

!!! question

    If we modify a dataset, will a new data notification message be sent? What changes can be expected?

??? success "Click to reveal answer"

    Yes. A new data notification message will be sent. In the message, the value of "rel": "canonical" within the "links" element will change to "rel": "update", indicating that the dataset has been modified.

!!! question
    
    If we delete a dataset, will a new data notification message be sent? What changes can be expected?

??? success "Click to reveal answer"

    Yes. A new data notification message will be sent. In the message, the value of "rel": "canonical" within the "links" element will change to "rel": "deletion", indicating that the dataset has been removed.

## Conclusion

!!! success "Congratulations!"
    In this practical session, you learned how to:

    - Create new datasets using the default template and your customized template
    - define your discovery metadata
    - review your data mappings
    - publish discovery metadata
    - review the WIS2 notification for your discovery metadata

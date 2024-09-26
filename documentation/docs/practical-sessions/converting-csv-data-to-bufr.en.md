---
title: Converting CSV data to BUFR
---

# Converting CSV data to BUFR

!!! abstract "Learning outcomes"
    By the end of this practical session, you will be able to:

    - use the **MinIO UI** to upload input CSV data files and monitor the result
    - know the format for CSV data for use with the default automatic weather station BUFR template
    - use the dataset editor in the **wis2box webapp** to create a dataset for publishing DAYCLI messages
    - know the format for CSV data for use with the DAYCLI BUFR template
    - use **wis2box webapp** to validate and convert sample data for AWS stations to BUFR (optional)

## Introduction

Comma-separated values (CSV) data files are often used for recording observational and other data in a tabular format. 
Most data loggers used to record sensor output are able to export the observations in delimited files, including in CSV.
Similarly, when data are ingested into a database it is easy to export the required data in CSV formatted files. 
To aid the exchange of data originally stored in tabular data formats a CSV to BUFR converted has been implemented in 
the wis2box using the same software as for SYNOP to BUFR.

In this session you will learn about using csv2bufr converter in the wis2box for the following built-in templates:

- **AWS** (aws-template.json) : Mapping template for converting CSV data from simplified automatic weather station file to BUFR sequence 301150, 307096"
- **DayCLI** (daycli-template.json) : Mapping template for converting daily climate CSV data to BUFR sequence 307075

## Preparation

Make sure the wis2box-stack has been started with `python3 wis2box.py start`

Make sure that you have a web browser open with the MinIO UI for your instance by going to `http://<your-host>:9000`
If you don't remember your MinIO credentials, you can find them in the `wis2box.env` file in the `wis2box-1.0b8` directory on your student VM.

Make sure that you have MQTT Explorer open and connected to your broker using the credentials `everyone/everyone`.

## Exercise 1: Using csv2bufr with the 'AWS' template

The 'AWS' template provides a predefined mapping template to convert CSV data from AWS stations in support of the GBON reporting requirements. 

The full list of columns used in the AWS template is described in this file: [aws-full.csv](/assets/tables/aws-full.csv)

### Review the aws-example input data

Download the example for this exercise from the link below:

[csv2bufr-ex1.csv](/sample-data/aws-example.csv)

Open the file you downloaded in an editor and inspect the content:

!!! question
    Examining the date, time and identify fields (WIGOS and traditional identifiers) what do
    you notice? How would today's date be represented?

??? success "Click to reveal answer"
    Each column contains a single piece of information. For example the date is split into
    year, month and day, mirroring how the data are stored in BUFR. Todays date would be 
    split across the columns "year", "month" and "day". Similarly, the time needs to be
    split into "hour" and "minute" and the WIGOS station identifier into its respective components.

!!! question
    Looking at the data file how are missing data encoded?
    
??? success "Click to reveal answer"
    Missing data within the file are represented by empty cells. In a CSV file this would be
    encoded by ``,,``. Note that this is an empty cell and not encoded as a zero length string, 
    e.g. ``,"",``.

!!! hint "Missing data"
    It is recognized that data may be missing for a variety of reasons, whether due to sensor 
    failure or the parameter not being observed. In these cases missing data can be encoded
    as per the above answer, the other data in the report remain valid.

### Upload the data to MinIO and check the result

Navigate to the MinIO UI and log in using the credentials from the `wis2box.env` file.

Create a new folder in the MinIO bucket that matches the dataset-id for the dataset you created with the template='weather/surface-weather-observations/synop':

<center><img alt="Image showing MinIO UI with the create folder button highlighted" src="../../assets/img/minio-create-folder.png"/></center>

Upload the example file you downloaded to the folder you created in the MinIO bucket:

<center><img alt="Image showing MinIO UI with the upload button highlighted" src="../../assets/img/minio-upload.png"/></center>

Check the Grafana dashboard to see if there are any WARNINGS or ERRORS. If you see any, try to fix them and repeat the exercise.

Check the MQTT Explorer to see if the data has been published to the broker.

Check the Monitoring page in the wis2box web-application to see if you can find the notification you have just published. Try to 'Inspect' the notification to see the content of the BUFR data.

## Exercise 2 - Using the 'DayCLI' template

In the previous exercise we used the dataset you created with Data-type='weather/surface-weather-observations/synop', which has pre-configured the CSV to BUFR conversion template to the AWS template.

In the next exercise we will use the 'DayCLI' template to convert daily climate data to BUFR. The table below lists the parameters included in the format:

{{ read_csv('docs/assets/tables/daycli-minimal.csv') }}

### Creating a wis2box dataset of publishing DAYCLI messages

Go to the dataset editor in the wis2box-webapp and create a new dataset. Use the same centre-id as in the previous practical sessions and use the template='climate/daily-climate-observations/daycli'.

### Review the daycli-example input data

Download the example for this exercise from the link below:

[daycli.csv](/sample-data/daycli-example.csv)

Open the file you downloaded in an editor and inspect the content:

!!! question
    What weather variables are included in the daycli template?

??? success "Click to reveal answer"
    The daycli template includes fields for the maximum and minimum temperature, the precipitation 
    and the snow depth.



## Exercise 3 - uploading and converting the data using the CSV-form in wis2box-webapp (optional)

The wis2box web-application provides an interface for uploading CSV data and converting it to BUFR before publishing it to the WIS2, using the AWS template.

The use of this form is intended for debugging and validation purposes, the recommended submission method for publishing data from Automated Weather Stations is to a setup a process that automatically uploads the data to the MinIO bucket.

### Using the CSV Form in the wis2box web-application

Navigate to CSV Form on the the wis2box web-application 
(``http://<your-host-name>/wis2box-webapp/csv2bufr_form``).
Click the entry box or drag and drop the test file you have downloaded to the entry box. 
You should now be able to click next to preview and validate the file.

<center><img alt="Image showing CSV to BUFR upload screen" src="../../assets/img/csv2bufr-ex1.png"/></center>

Clicking the next button loads the file into the browser and validates the contents against a predefined schema. 
No data has yet been converted or published.  On the preview / validate tab you should be presented with a list of warnings 
about missing data but in this exercise these can be ignored. 

<center><img alt="Image showing CSV to BUFR example validation page with warnings" src="../../assets/img/csv2bufr-warnings.png"/></center>

Click *next* to proceed and you will be asked to provide a dataset-id for the data to be published. Select the dataset-id you create previously and click *next*.

You should now be on an authorization page where you will be asked to enter the ``processes/wis2box`` 
token you have previously created. Enter this token and click the "Publish on WIS2" toggle to ensure 
"Publish to WIS2" is selected (see screenshot below).

<center><img alt="csv2bufr auth and publish screen" src="../../assets/img/csv2bufr-toggle-publish.png"/></center>

Click next to transform to BUFR and publish, you should then see the following screen:

<center><img alt="Image showing CSV to BUFR example success screen" src="../../assets/img/csv2bufr-success.png"/></center>

Clicking the down arrow tn the right of  ``Output BUFR files`` should reveal the ``Download`` and ``Inspect`` buttons.
Click inspect to view the data and confirm the values are as expected.

<center><img alt="Image showing CSV to BUFR inspect output" src="../../assets/img/csv2bufr-inspect.png"/></center>

As a final step navigate to the monitoring page from the left menu.

<center><img alt="Image showing monitoring tab in on the left menu" src="../../assets/img/csv2bufr-monitoring.png"/></center>

Select the dataset-id you have been publishing on from the dropdown menu and click update, you should see the message 
you have just published (and possibly notifications from the synop2bufr session). An example screenshot is shown below:

<center><img alt="Image showing notifications published over the last 24 hours" src="../../assets/img/csv2bufr-monitoring2.png"/></center>

You should also be able to see these notifications in MQTT Explorer.

### Debugging invalid input data

In this exercise we will examine what happens with invalid input data. Download the next example file by clicking the 
link below. This contains the same data as the first file but with the empty columns removed.
Examine the file and confirm which columns have been removed and then follow the same process to convert the data to BUFR.

[csv2bufr-ex3a.csv](/sample-data/csv2bufr-ex3a.csv)

!!! question
    With the columns missing from the file were you able to convert the data to BUFR?
    Did you notice any change to the warnings on the validation page?

??? success "Click to reveal answer"
    You should have still been able to convert the data to BUFR but the warning messages will have been updated
    to indicate that the columns were missing completely rather than containing a missing value.

In this next example an additional column has been added to the CSV file.

[csv2bufr-ex3b.csv](/sample-data/csv2bufr-ex3b.csv)

!!! question
    Without uploading or submitting the file can you predict what will happen when you do?

Now upload and confirm whether your prediction was correct.

??? success "Click to reveal answer"
    When the file is validated you should now receive a warning that the column ``index``
    is not found in the schema and that the data will be skipped. You should be able to click
    through and convert to BUFR as with the previous example.

In the final example in this exercise the data has been modified. Examine the contents of the CSV file.

[csv2bufr-ex3c.csv](/sample-data/csv2bufr-ex3c.csv)

!!! question
    What has changed in the file and what do you think will happen?

Now upload the file and confirm whether you were correct.

??? warning "Click to real answer"
    The pressure fields have been converted from Pa to hPa in the input data. However, the CSV to BUFR
    converter expects the same units as BUFR (Pa) and, as a result, these fields fail the validation due to being
    out of range. You should be able to edit the CSV to correct the issue and to resubmit the data by
    returning to the first screen and re-uploading.

!!! hint
    The wis2box web-application can be used to test and validate sample data for the automated workflow. This will identify
    some common issues, such as the incorrect units (hPa vs Pa and C vs K) and missing columns. Care should be taken 
    that the units in the CSV data match those indicated above.

!!! bug
    Please note, due to a bug in the current version of the web-application you may need to reload the page before resubmitting
    the data.

## Conclusion

!!! success "Congratulations"
    In this practical session you have learned:

    - how to format a CSV file for use with wis2box web-application
    - and how to validate a sample CSV file and to correct for common issues.  

!!! info "Next steps"
    The csv2bufr converter used in the wis2box has been designed to be configurable for use with any row based 
    tabular data. The column names, delimiters, quotation style and limited quality control can all be configured
    according to user needs. In this session you have used the built-in AWS and daycli templates but you can develop
    your own templates for other data types as required.

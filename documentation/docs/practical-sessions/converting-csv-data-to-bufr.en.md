---
title: Converting CSV data to BUFR
---

# Converting CSV data to BUFR

!!! abstract "Learning outcomes"
    By the end of this practical session, you will be able to:

    - format CSV data for use with the default automatic weather station BUFR template
    - use **wis2box webapp** to validate and convert sample data for AWS stations to BUFR
    - use the MinIO UI to upload input CSV data files
    - use the dataset editor to use a different template for CSV to BUFR conversion

## Introduction

Comma-separated values (CSV) data files are often used for recording observational and other data in a tabular format. 
Most data loggers used to record sensor output are able to export the observations in delimited files, including in CSV.
Similarly, when data are ingested into a database it is easy to export the required data in CSV formatted files. 
To aid the exchange of data originally stored in tabular data formats a CSV to BUFR converted has been implemented in 
the wis2box using the same software as for SYNOP to BUFR. In this session you will learn about using this tool
through the wis2box web-application. Command line usage and customisation will be covered in a later session.

## Preparation

!!! warning "Prerequisites"
    - Ensure that your wis2box has been configured and started, including the setting execution tokens 
      for the ``processes/wis2box`` and ``collections/stations``paths. Confirm the status by visiting 
      the wis2box API (``http://<your-host-name>/oapi``) and verifying that the API is running.
    - The tokens can be checked by logging in to the wis2box management container and entering the 
      command: ``wis2box auth has-access-path --path processes/wis2box <your-token>`` where 
      ``<your-token>`` is the token you entered.
    - If the tokens are missing they can be generated with the following commands:
    
        ```{.copy}
        wis2box auth add-token --path processes/wis2box <token>
        wis2box auth add-token --path collections/stations <token>
        ```
      where token is the value of the token. This can be left blank to automatically generate
      a random token (recommended).
    - Make sure that you have MQTT Explorer open and connected to your broker.
    

## Inspecting CSV data and BUFR conversion

### Exercise 1 - the basics

The csv2bufr converter used in the wis2box can be configured to map between various tabulated input files, including CSV.
However, to facilitate and make the use of this tool easier a standardised CSV format has been developed, targeted
at data from AWS stations and in support of the GBON reporting requirements. The table below lists the parameters 
included in the format:

{{ read_csv('docs/assets/tables/aws-minimal.csv') }}

The full file can be downloaded from: [aws-full.csv](/assets/tables/aws-full.csv)

Now download the example for this exercise from the link below:

[csv2bufr-ex1.csv](/sample-data/csv2bufr-ex1.csv)

Inspect the expected columns from the table above and compare to the example data file.

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

### Exercise 2 - converting your first message

Now that you have familiarized yourself with the input data file and specified CSV format you will convert this example file to BUFR using the wis2box web-application. 

First you need to register the station referred to in the input-data in your wis2box-instance. However, if you try to import *0-20000-0-99100* from OSCAR/Surface using the wis2box web-app you will find that the station does not exist:

<center><img alt="Image showing station not found in OSCAR/Surface" src="../../assets/img/csv2bufr-station-not-found.png"/></center>

Click the button 'CREATE NEW STATION' and you will be allowed to enter the station details manually.

Enter the fictional station details, suggested details are below:

| Field | Value           |
| ----- |-----------------|
 | Station name | Monte Genuardo  |
| WIGOS station identifier | 0-20000-0-99100 |
| Traditional identifier | 99100           |
| Longitude | 13.12425        |
| Latitude | 37.7            |
| Station elevation | 552             |
| Facility type | Land (fixed)    |
| Barometer height above sea level | 553             |
| WMO Region | VI              |
| Territory or member operating the station | Italy           |
| Operating status | operational     |

Select the appropriate topic, enter the ``collections/stations`` token previously created and click save. 

You are now ready to process data from this station.

Navigate to CSV to BUFR submission page on the the wis2box web-application 
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

Select the topic you have been publishing on from the dropdown menu and click update, you should see the message 
you have just published (and possibly notifications from the synop2bufr session). An example screenshot is shown below:

<center><img alt="Image showing notifications published over the last 24 hours" src="../../assets/img/csv2bufr-monitoring2.png"/></center>

!!! success
    Congratulations you have published you first csv data converted to BUFR via the wis2box.

You should also be able to see these notifications in MQTT Explorer.


### Exercise 3 - debugging the input data

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

### Exercise 4 - potential web-application and API issues

Before the web-application can be used to submit data the topic hierarchy, on which to publish, the authorisation
token and the stations need to be configured. This can be demonstrated with several simple exercises.

For the first example in this exercise download the example file via the link below and publish using the web-application.

[csv2bufr-ex4a.csv](/sample-data/csv2bufr-ex4a.csv)

!!! question
    What result do you receive on the "Review page"?

??? success "Click to reveal answer"
    The second row in the file contains data from a station (again fictional) that has not been registered
    in the wis2box. As a result a warning is given that the station has not been found and that the data
    have not been published.

    <center><img alt="Image showing CSV to BUFR invalid WSi warning" src="../../assets/img/csv2bufr-skip-wsi.png"/></center>

For the next  example, try submitting the data but without selecting a topic hierarchy on which to publish.

[csv2bufr-ex4b.csv](/sample-data/csv2bufr-ex4b.csv)

!!! question
    What happens when you try and click next?

??? warning "Click to reveal answer"
    You should find the next button greyed out until a valid topic is selected. The options for the topic hierarchy
    are set based on the discovery metadata registered within the box

For the final example, try entering a token that has not been registered and observe what happens when you click next.

!!! question
    What do you expect will happen if you enter an invalid token?

??? warning "Click to reveal answer"
    When you click next you should be taken to the Review page but receive a message that the token is invalid. 
    Navigate to the previous step, enter a valid token and try again.

## Housekeeping

As with the FM-12 SYNOP to BUFR exercise you will have registered some new stations within the wis2box. Navigate to the
station list and delete those stations as they are no longer required.

## Conclusion

!!! success "Congratulations"
    In this practical session you have learned:

    - how to format a CSV file for use with wis2box web-application
    - and how to validate a sample CSV file and to correct for common issues.  

!!! info "Next steps"
    The csv2bufr converter used in the wis2box has been designed to be configurable for use with any row based 
    tabular data. The column names, delimiters, quotation style and limited quality control can all be configured
    according to user needs. In this page only the basics have been covered, with a standardised CSV template
    developed based on user feedback. Advanced configuration will be covered as part of the BUFR command line tools
    session.

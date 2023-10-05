---
title: Converting SYNOP data to BUFR
---

# Converting SYNOP data to BUFR

!!! abstract "Learning outcomes"
    By the end of this practical session, you will be able to:

    - submit valid FM-12 SYNOP bulletins via the wis2box web application for conversion to BUFR and exchange over the WIS2.0
    - validate, diagnose and fix simple coding errors in an FM-12 SYNOP bulletin prior to format conversion and exchange
    - ensure that the required station metadata is available in the wis2box
    - confirm and inspect successfully converted bulletins

## Introduction

Surface weather reports from land surface stations have historically been reported hourly or at the main 
(00, 06, 12 and 18 UTC) and intermediate (03, 09, 15, 21 UTC) synoptic hours. Prior to the migration
to BUFR these reports were encoded in the plain text FM-12 SYNOP code form. Whilst the migration to BUFR
was scheduled to be complete by 2012 a large number of reports are still exchanged in the legacy 
FM-12 SYNOP format. 

To aid with completing migration to BUFR some tools have been developed for
encoding FM-12 SYNOP reports to BUFR, in this session you will learn how to use these tools as well
as the relationship between the information contained in the FM-12 SYNOP reports and BUFR messages.

## Preparation

!!! warning "Prerequisites"

    - Ensure that your wis2box has been configured and started.
    - Confirm the status by visiting the wis2box API (``http://<your-host-name>/oapi``) and verifying that the API is running.
    - Make sure that you have MQTT Explorer open and connected to your broker.

In order to submit data to be processed in the wis2box-webapp you will need an auth token for "processes/wis2box".

You can generate this token by logging in to the wis2box management container and using the `wis2box auth add-token` command:

```bash
cd ~/wis2box-1.0b5
python3 wis2box-ctl.py login
wis2box auth add-token --path processes/wis2box
```

Or if you want to define your own token:

```bash
wis2box auth add-token --path processes/wis2box DataIsMagic
```

Please record the token that is generated, you will need this later in the session.

For practical purposes the exercises in this session use data from Romania, import the station ``0-20000-0-15015`` into your station list and associate it with the topic for your "Surface weather observations collection". You can remove this station at the end of the session.

If you have forgotten your auth token for "collections/stations" you can create a new one with:

```bash
wis2box auth add-token --path collections/stations
```

## Inspecting SYNOP data and BUFR conversion

### Exercise 1 - the basics

Review the FM-12 SYNOP message below:

``` {.copy}
AAXX 21121
15015 02999 02501 10103 21090 39765 42952 57020 60001=
``` 

Identify the key components of the FM-12 SYNOP message and confirm that the station(s) is (are) registered
within the wis2box. The station(s) should be discoverable via the station list page
(``http://<your-host-name>/wis2box-webapp/station``) or via the API directly
(``http://<your-host-name>/oapi/collections/stations``). 

!!! hint
    The traditional station identifier (2 digit block number and 3 digit station number) are included
    in the FM-12 SYNOP report. These can be used to find the station.

!!! question
    What is the traditional station identifier of the station included in the message and 
    where is the station located?

??? success "Click to reveal answer"
    The five digit group, ``15015``, gives the 5 digit traditional station identifier. In 
    this case for the station "OCNA SUGATAG" located in Romania.


Identify the number of weather reports in the message.

!!! question
    How many weather reports are in the message?

??? success "Click to reveal answer"
    One, the report contains a single message.
    
    The first line ``AAXX 21121`` indicates that this is an FM-12 SYNOP message (``AAXX``), 
    the 2112 indicates that the weather observation was made on the 21st day of the month at 12 UTC.
    The final digit of the row, ``1``, indicates the source and units of the wind speed. The second line
    contains a single weather report, beginning with the 5 digit group ``15015`` and ending with 
    the ``=`` symbol.

### Exercise 2 - converting your first message

Now that you have reviewed the message, you are ready to convert the data to BUFR.

Copy the message you have just reviewed:
    
``` {.copy}
AAXX 21121
15015 02999 02501 10103 21090 39765 42952 57020 60001=
``` 

Open the wis2box web application and navigate to the synop2bufr page using the left navigation drawer and proceed as follows:

- Paste the content you have copied in the text entry box.
- Select the month and year using the date picker, assume the current month for this exercise.
- Select a topic from the drop down menu (the options are based on the metadata configured in the wis2box)
- Enter the "processes/wis2box" auth token you generated earlier
- Ensure "Publish on WIS2" is toggled ON
- Click "SUBMIT"

<center><img alt="Dialog showing synop2bufr page, including toggle button" src="../../assets/img/synop2bufr-toggle.png"></center>

Click submit. The data will now be converted to BUFR and the result returned to the web application.

Click on "Output BUFR files" to see a list of the files that have been generated.

??? tip
    The result section of the page should show a single converted BUFR message with zero warnings 
    or errors. The download button allows the BUFR data to be downloaded directly to your computer.
    Click the down arrow / chevron to reveal download and inspect buttons. 
    The inspect button runs a process to convert and extract the data from BUFR.

    <center><img alt="Dialog showing result of successfully submitting a message"
         src="../../assets/img/synop2bufr-ex2-success.png"></center>

!!! question
    The FM-12 SYNOP format does not include the station location, elevation or barometer height. 
    Confirm that these are in the output BUFR data, where do these come from?

??? success "Click to reveal answer"
    Clicking the inspect button should bring up a dialog like that shown below.

    <center><img alt="Results of the inspect button showing the basic station metadata, the station location and the observed properties"
         src="../../assets/img/synop2bufr-ex2.png"></center>

    This includes the station location shown on a map and basic metadata, as well as the observations in the message.
    
    As part of the transformation from FM-12 SYNOP to BUFR, additional metadata was added to the BUFR file.
    
    The BUFR file can also be inspected by downloading the file and validating using a tool such as as the ECMWF ecCodes BUFR validator.

As a final step navigate to the monitoring page from the left menu and confirm that the data have been published.

<center><img alt="Image showing monitoring tab in on the left menu" src="../../assets/img/csv2bufr-monitoring.png"/></center>

<center><img alt="Image showing monitoring page and published data" src="../../assets/img/synop2bufr-monitoring.png"/></center>

You should also be able to see these notifications in MQTT Explorer.

### Exercise 3 - understanding the station list

For this next exercise you will convert a file containing multiple reports, see the data below:

``` {.copy}
AAXX 21121
15015 02999 02501 10103 21090 39765 42952 57020 60001=
15020 02997 23104 10130 21075 30177 40377 58020 60001 81041=
15090 02997 53102 10139 21075 30271 40364 58031 60001 82046=
```

!!! question
    Based on the prior exercise, look at the FM-12 SYNOP message and predict how many output BUFR
    messages will be generated. 
    
    Now copy paste this message into SYNOP form and submit the data.

    Did the number of messages generated match your expectation and if not, why not?

??? warning "Click to reveal answer"
    
    You might have expected three BUFR messages to be generated, one for each weather report. However, instead you got 2 warnings and only one BUFR file.
    
    In order for a weather report to be converted to BUFR the basic metadata contained in the 
    station list is required. Whilst the above example includes three weather reports, two of the
    three stations reporting were not registered in your wis2box. 
    
    As a result, only one of the three weather report resulted in a BUFR file being generated and WIS2 notification being published. The other two weather reports were ignored and warnings were generated.

!!! hint
    Take note of the relationship between the WIGOS Identifier and the traditional station 
    identifier included in the BUFR output. In many cases, for stations listed in WMO-No. 9
    Volume A at the time of migrating to WIGOS station identifiers, the WIGOS station
    identifier is given by the traditional station identifier with ``0-20000-0`` prepended,
    e.g. ``15015`` has become ``0-20000-0-15015``.

Using the station list page from the web application import the missing stations from OSCAR/Surface 
into the wis2box and repeat the exercise. 

Three BUFR files should be generated and there should be no warnings or errors listed in the web application. 

In addition to the basic station information, additional metadata such as the station elevation above sea level and the
barometer height above sea level are required for encoding to BUFR. The fields are included in the station list and station editor pages.
    
### Excercise 4 - debugging

In this final exercise you will identify and correct two of the most common problems encountered when
using this tool to convert FM-12 SYNOP to BUFR. 

Example data is shown in the box below, examine the data and try and resolve any issues that there 
may be prior to submitting the data through the web application. 

!!! hint
    You can edit the data in the entry box on the web application page. If you miss any issues 
    these should be detected and highlighted as a warning or error once the submit button 
    has been clicked.

``` {.copy}
AAXX 21121
15015 02999 02501 10103 21090 39765 42952 57020 60001
15020 02997 23104 10130 21075 30177 40377 58020 60001 81041=
15090 02997 53102 10139 21075 30271 40364 58031 60001 82046
```

!!! question
    What issues did you expect to encounter when converting the data to BUFR and how did you
    overcome them? Where there any issues you were not expecting?

??? success "Click to reveal answer"
    In this first example the "end of text" symbol (=), or record delimiter, is missing between the
    first and second weather reports. Consequently, lines 2 and 3 are treated as a single report, 
    leading to errors in the parsing of the message.

The second example below contains several common issue found in FM-12 SYNOP reports. Examine the
data and try to identify the issues and then submit the corrected data through the web application.

```{.copy}
AAXX 21121
15020 02997 23104 10/30 21075 30177 40377 580200 60001 81041=
```

!!! question
    What issues did you find and how did you resolve these?

??? success "Click to reveal answer"
    There are two issues in the weather report. 
    
    The first, in the signed air temperature group, has the tens character set to missing (/), 
    leading to an invalid group. In this example we know that the temperature is 13.0 degrees 
    Celsius (from the above examples) and so this issue can be corrected. Operationally, the 
    correct value would need to be confirmed with the observer.

    The second issue occurs in group 5 where there is an additional character, with the final 
    character duplicated. This issue can be fixed by removing the extra character.

## Housekeeping

During the exercises in this session you will have imported several files into your station list. Navigate to the 
station list page and click the trash can icons to delete the stations. You may need to refresh the page to have
the stations removed from the list after deleting.

<center><img alt="Station metadata viewer"
         src="../../assets/img/synop2bufr-trash.png" width="600"></center>

You can also delete the file used in the final exercise as this will no longer be required.

## Conclusion

!!! success "Congratulations!"

    In this practical session, you learned:

    - how to submit a FM-12 SYNOP report through the web-app;
    - how to diagnose and correct simple errors in an FM-12SYNOP report;
    - the importance of registering stations in the wis2box (and OSCAR/Surface);
    - and how to use `bufr_dump` to inspect the content of BUFR data.


---
title: Converting SYNOP data to BUFR
---

# Converting SYNOP data to BUFR using the wis2box-webapp

!!! abstract "Learning outcomes"
    By the end of this practical session, you will be able to:

    - submit valid FM-12 SYNOP bulletins via the wis2box web application for conversion to BUFR and exchange over the WIS2.0
    - validate, diagnose and fix simple coding errors in an FM-12 SYNOP bulletin prior to format conversion and exchange
    - ensure that the required station metadata is available in the wis2box
    - confirm and inspect successfully converted bulletins

## Introduction

To allow manual observers to submit data directly to the WIS2.0, the wis2box-webapp has a form for converting FM-12 SYNOP bulletins to BUFR. The form also allows users to diagnose and fix simple coding errors in the FM-12 SYNOP bulletin prior to format conversion and exchange and inspect the resulting BUFR data.

## Preparation

!!! warning "Prerequisites"

    - Ensure that your wis2box has been configured and started.
    - Open a terminal and connect to your student VM using SSH.
    - Connect to the MQTT broker of your wis2box instance using MQTT Explorer.
    - Open the wis2box web application (``http://<your-host-name>/wis2box-webapp``) and ensure you are logged in.

## Using the wis2box-webapp to convert FM-12 SYNOP to BUFR

### Exercise 1 - using the wis2box-webapp to convert FM-12 SYNOP to BUFR

Make sure you have the auth token for "processes/wis2box" that you generated in the previous exercise and that you are connected to your wis2box broker in MQTT Explorer.

Copy the following message:
    
``` {.copy}
AAXX 27031
15015 02999 02501 10103 21090 39765 42952 57020 60001=
``` 

Open the wis2box web application and navigate to the synop2bufr page using the left navigation drawer and proceed as follows:

- Paste the content you have copied in the text entry box.
- Select the month and year using the date picker, assume the current month for this exercise.
- Select a topic from the drop down menu (the options are based on the datasets configured in the wis2box).
- Enter the "processes/wis2box" auth token you generated earlier
- Ensure "Publish on WIS2" is toggled ON
- Click "SUBMIT"

<center><img alt="Dialog showing synop2bufr page, including toggle button" src="../../assets/img/synop2bufr-toggle.png"></center>

Click submit. You will receive an warning message as the station is not registered in the wis2box. Go to the station-editor and import the following station:

``` {.copy}
0-20000-0-15015
```

Ensure the station is associated with the topic you selected in the previous step and then return to the synop2bufr page and repeat the process with the same data as before. 

!!! question
    How can you see the result of the conversion from FM-12 SYNOP to BUFR?

??? success "Click to reveal answer"
    The result section of the page shows Warnings, Errors and Output BUFR files.

    Click on "Output BUFR files" to see a list of the files that have been generated. You should see one file listed.

    The download button allows the BUFR data to be downloaded directly to your computer.

    The inspect button runs a process to convert and extract the data from BUFR.

    <center><img alt="Dialog showing result of successfully submitting a message"
         src="../../assets/img/synop2bufr-ex2-success.png"></center>

!!! question
    The FM-12 SYNOP input data did not include the station location, elevation or barometer height. 
    Confirm that these are in the output BUFR data, where do these come from?

??? success "Click to reveal answer"
    Clicking the inspect button should bring up a dialog like that shown below.

    <center><img alt="Results of the inspect button showing the basic station metadata, the station location and the observed properties"
         src="../../assets/img/synop2bufr-ex2.png"></center>

    This includes the station location shown on a map and basic metadata, as well as the observations in the message.
    
    As part of the transformation from FM-12 SYNOP to BUFR, additional metadata was added to the BUFR file.
    
    The BUFR file can also be inspected by downloading the file and validating using a tool such as as the ECMWF ecCodes BUFR validator.

Go to MQTT Explorer and check the WIS2 notifications topic to see the WIS2 notifications that have been published.

### Exercise 2 - understanding the station list

For this next exercise you will convert a file containing multiple reports, see the data below:

``` {.copy}
AAXX 27031
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

Using the station list page, import the following stations:

``` {.copy}
0-20000-0-15020
0-20000-0-15090
```

Ensure that the stations are associated with the topic you selected in the previous exercise and then return to the synop2bufr page and repeat the process.

Three BUFR files should now be generated and there should be no warnings or errors listed in the web application. 

In addition to the basic station information, additional metadata such as the station elevation above sea level and the
barometer height above sea level are required for encoding to BUFR. The fields are included in the station list and station editor pages.
    
### Exercise 3 - debugging

In this final exercise you will identify and correct two of the most common problems encountered when
using this tool to convert FM-12 SYNOP to BUFR. 

Example data is shown in the box below, examine the data and try and resolve any issues that there 
may be prior to submitting the data through the web application. 

!!! hint
    You can edit the data in the entry box on the web application page. If you miss any issues 
    these should be detected and highlighted as a warning or error once the submit button 
    has been clicked.

``` {.copy}
AAXX 27031
15015 02999 02501 10103 21090 39765 42952 57020 60001
15020 02997 23104 10130 21075 30177 40377 58020 60001 81041=
15090 02997 53102 10139 21075 30271 40364 58031 60001 82046=
```

!!! question
    What issues did you expect to encounter when converting the data to BUFR and how did you
    overcome them? Where there any issues you were not expecting?

??? success "Click to reveal answer"
    In this first example the "end of text" symbol (=), or record delimiter, is missing between the
    first and second weather reports. Consequently, lines 2 and 3 are treated as a single report, 
    leading to errors in the parsing of the message.

The second example below contains several common issues found in FM-12 SYNOP reports. Examine the
data and try to identify the issues and then submit the corrected data through the web application.

```{.copy}
AAXX 27031
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

## Conclusion

!!! success "Congratulations!"

    In this practical session, you learned:

    - how the synop2bufr tool can be used to convert FM-12 SYNOP reports to BUFR;
    - how to submit a FM-12 SYNOP report through the web-app;
    - how to diagnose and correct simple errors in an FM-12 SYNOP report;
    - the importance of registering stations in the wis2box (and OSCAR/Surface);
    - and the use of the inspect button to view the content of BUFR data.


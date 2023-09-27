---
title: Converting SYNOP data to BUFR
---

# Converting SYNOP data to BUFR

!!! abstract Learning outcomes
    By the end of this session you will be able to:

    - Submit valid FM-12 SYNOP bulletins via the WIS2box web app for conversion to BUFR and exchange over the WIS2.0.
    - Validate, diagnose and fix simple coding errors in an FM-12 SYNOP bulletin prior to format conversion and exchange.
    - Ensure that the required station metadata is available in the WIS2box.
    - Confirm and inspect successfully converted bulletins.

## Introduction

Surface weather reports from land surface stations have historically been reported hourly or at the main 
(00, 06, 12 and 18 UTC) and intermediate (03, 09, 15, 21 UTC) synoptic hours. Prior to the migration
to BUFR these reports were encoded in the FM-12 SYNOP code form. Whilst the migration to BUFR
was scheduled to be complete by 2012 a large number of reports are still exchanged in the legacy 
FM-12 SYNOP format. 

To aid with completing migration to BUFR some tools have been developed for
encoding FM-12 SYNOP reports to BUFR, in this session you will learn how to use these tools as well
as the relationship between the information contained in the FM-12 SYNOP reports and BUFR messages.

## Preparation

!!! warning
    - Ensure that your WIS2box has been configured and started, including the setting execution tokens 
      for the ``processes/wis2box`` and ``collections/stations``paths. Confirm the status by visiting 
      the WIS2box API (``http://<your-host-name>/oapi``) and verifying that the API is running.
    - Ensure that you are able to access the MinIO admin interface at: ``http://<your-host-name>:9001``

## Inspecting SYNOP data and BUFR conversion

### Exercise 1 - the basics

Review the FM-12 SYNOP message below:

``` {.copy}
AAXX 21121
15015 02999 02501 10103 21090 39765 42952 57020 60001=
``` 

Identify the key components of the FM-12 SYNOP message and confirm that the station(s) is (are) registered
within the WIS2box. The station(s) should be discoverable via the station list page
(``http://<your-host-name>/wis2box-webapp/station``) or via the API directly
(``http://<your-host-name>/oapi/collections/stations``). 

!!! hint
    The traditional station identifier (2 digit block number and 3 digit station number) are included
    in the FM-12 SYNOP report. These can be used to find the station.

!!! question
    What is the traditional station identifier of the station included in the message and 
    where is the station located?

??? success "Click to reveal the answer"
    The five digit group, ``15015``, gives the 5 digit traditional station identifier. In 
    this case for the station "OCNA SUGATAG" located in Romania.


Identify the number of weather reports in the message.

!!! question
    How many weather reports are in the message?

??? success "Click to reveal the answer"
    One, the report contains a single message.
    
    The first line ``AAXX 21121`` indicates that this is an FM-12 SYNOP message (``AAXX``), 
    the 2112 indicates that the weather observation was made on the 21st day of the month at 12 UTC.
    The final digit of the row, ``1``, indicates the source and units of the wind speed. The second line
    contains a single weather report, beginning with the 5 digit group ``15015`` and ending with 
    the ``=`` symbol.

!!! question "Bonus question"
    What is the WIGOS identifier for the station and what topics have been configured?

??? success "Click to reveal the answer"
    The WIGOS identifier of the station can be found via the station list. The screen shot
    below shows an example of the station information.

    <center><img alt="Station metadata viewer"
         src="../../assets/img/synop2bufr-ex1.png" width="600"></center>

    In this example, the WIGOS identifier for the station "OCNA SUGATAG" is 0-20000-0-15015. 
    Further information can be found by scrolling down the station page, the station
    is configured to publish on topic  ``origin/a/wis2/rou/rnimh/data/core/weather/surface-based-observations/synop``.

### Exercise 2 - converting your first message
Now that you have confirmed that there is one weather report in the file and that the station
is registered in the WIS2box you are ready to convert the data to BUFR.

Open the WIS2box web app and navigate to the synop2bufr page using the left navigation drawer. 
Select the date using the date picker and copy and paste the FM-12 SYNOP message into the text 
entry box. Assume today's date for demonstration purposes. Once the message has been copied, select 
the appropriate topic to publish the data on, enter the "processes/wis2box" token and select submit.
The data will now be converted to BUFR and the result returned to the web app.

??? tip
    The result section of the page should show a single converted BUFR message with zero warnings 
    or errors. The download button allows the BUFR data to be downloaded directly to your computer.
    The inspect button runs a process to convert and extract the data from BUFR.

    <center><img alt="Dialog showing result of successfully submitting a message"
         src="../../assets/img/synop2bufr-ex2-success.png" width="600"></center>

!!! question
    The FM-12 SYNOP format does not include the station location, elevation or barometer height. 
    Confirm that these are in the output BUFR data, where do these come from?

??? success "Click to reveal the answer"
    Clicking the inspect button should bring up a dialog like that shown below.

    <center><img alt="Results of the inspect button showing the basic station metadata, the station location and the observed properteis"
         src="../../assets/img/synop2bufr-ex2.png" width="600"></center>

    This includes the station location shown on a map and basic metadata, as well as the observations, 
    extracted from the BUFR message. As part of the transformation from FM-12 SYNOP to BUFR this information
    is merged from the station metadata. The BUFR file can also be inspected by downloading the file
    and validating using a tool as as the ECMWF ecCodes BUFR validator.

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
    messages will be generated. Does the number match your expection, and if not, why not?

??? warning "Click to reveal the answer"
    In order for a weather report to be converted to BUFR the basic metadata contained in the 
    station list is required. Whilst the above example includes three weather reports two of the
    three stations reporting have not been registered in the WIS2box. As a result, only one
    weather report has been converted two BUFR.

!!! hint
    Take note of the relationship between the WIGOS Identifier and the traditional station 
    identifier included in the BUFR output. In many cases, for stations listed in WMO-No. 9
    Volume A at the time of migrating to WIGOS identifiers, the WIGOS station
    identifier is given by the traditional station identifier with ``0-20000-0`` prepended,
    e.g. ``15015`` has become ``0-20000-0-15015``.

Using the station list page from the web app import the missing stations from OSCAR/Surface 
into the WIS2box and repeat the exercise. Three BUFR files should be generated and there 
should be no warnings or errors listed in the web app. In addition to the basic station
information additional metadata such as the station elevation above sea level and the
barometer height above sea level are required for encoding to BUFR. The fields are included
in the station list and station editor pages.
    
### Excercise 4 - debugging

In this final exercise you will identify and correct two of the most common problems encountered when
using this tool to convert FM-12 SYNOP to BUFR. 

Example data is shown in the box below, examine the data and try and resolve any issues that there 
may be prior to submitting the data through the web app. 

!!! hint
    You can edit the data in the entry box on the web app page. If you miss any issues 
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

??? success "Click to reveal the answer"
    In this first example the "end of text" symbol (=), or record delimiter, is missing between the
    first and second weather reports. Consequently, lines 2 and 3 are treated as a single report, 
    leading to errors in the parsing of the message. The final line is also missing the end of 
    text symbol but the wis2box is able to handle this case.

    The station 15090 should have been registered as part of the previous exercise. If not you will
    also receive a warning that the station can not be found.  If this is the case, register the
    station in the WIS2box and repeat the exercise.

The second example below contains several common issue found in FM-12 SYNOP reports. Examine the
data and try to identify the issues and then submit the corrected data through the web app.

```{.copy}
AAXX 21121
15020 02997 23104 10/30 21075 30177 40377 580200 60001 81041=
```

!!! question
    What issues did you find and how did you resolve these?

??? success "Click to reveal the answer"
    There are two issues in the weather report. 
    
    The first, in the signed air temperature group, has the tens character set to missing (/), 
    leading to an invalid group. In this example we know that the temperature is 13.0 degrees 
    Celsius (from the above examples) and so this issue can be corrected. Operationally, the 
    correct value would need to be confirmed with the observer.

    The second issue occurs in group 5 where there is an additional character, with the final 
    character duplicated. This issue can be fixed by removing the extra character.


### Exercise 5 - command line tools
In addition to the web app, the WIS2box management container includes command lines tools for working with BUFR.
The first of these, `bufr_bump` from the ECMWF ecCodes software, allows the contents of a BUFR file to be decoded
and inspected. In this exercise we will use this tool and the wis2box management container (on day 2 you should 
have configured a WIS2box and have been able to log in).

Before starting the exercise we need to transfer some data to the wis2box. Download one of the BUFR files
you created in the previous exercise and save this to a MinIO bucket. 

!!! hint
    Create a new bucket, e.g. synop2bufr-exercise, through the MinIO admin interface and save to this location.
    The admin interface can be found at ``http://<your-host-name>:9001``.

You are now ready to begin the exercise, start by logging in to the wis2box management container and navigate
to the wis2box data directory:

!!! example
    ``` {.copy}
    cd /data/wis2box/synop2bufr
    ```

Confirm that ecCodes and bufr_dump are available, these will have been automatically installed as part of the
wis2box configuration process.

!!! example
    commands to follow ...

Now experiment using ``bufr_dump`` to decode and extract data from the file. Some examples are given below, you will
need to update the filename to that of the file saved to the MinIO bucket.

```bash
bufr_dump -p my_bufr.bufr4
```

This will display BUFR content to your screen.  If you are interested in the values taken by a variable in 
particular, use the `egrep` command:

```bash
bufr_dump -p my_bufr.bufr4 | egrep -i temperature
```

This will display variables related to temperature in your BUFR data. If you want to do this for multiple types of variables, filter the output using a pipe (`|`):

```bash
bufr_dump -p my_bufr.bufr4 | egrep -i 'temperature|wind'
```

## Conclusion

!!! success "Congratulations!"

    In this practical session, you learned:

    - how to submit a FM-12 SYNOP report through the web-app;
    - how to diagnose and correct simple errors in an FM-12SYNOP report;
    - the importance of registering stations in the wis2box (and OSCAR/Surface);
    - and how to use `bufr_dump` to inspect the content of BUFR data.
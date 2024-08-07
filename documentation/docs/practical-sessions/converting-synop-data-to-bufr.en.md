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
FM-12 SYNOP format. Further information on the FM-12 SYNOP format can be found in the WMO Manual on Codes, 
Volume I.1 (WMO-No. 306, Volume I.1).

[WMO Manual on Codes, Volume I.1](https://library.wmo.int/records/item/35713-manual-on-codes-international-codes-volume-i-1)

To aid with completing migration to BUFR some tools have been developed for
encoding FM-12 SYNOP reports to BUFR, in this session you will learn how to use these tools as well
as the relationship between the information contained in the FM-12 SYNOP reports and BUFR messages.

## Preparation

!!! warning "Prerequisites"

    - Ensure that your wis2box has been configured and started.
    - Confirm the status by visiting the wis2box API (``http://<your-host-name>/oapi``) and verifying that the API is running.

## synop2bufr primer

Below are essential `synop2bufr` commands and configurations:

### transform
The `transform` function converts a SYNOP message to BUFR:

```bash
synop2bufr data transform --metadata my_file.csv --output-dir ./my_directory --year message_year --month message_month my_SYNOP.txt
```

Note that if the metadata, output directory, year and month options are not specified, they will assume their default values:

| Option      | Default |
| ----------- | ----------- |
| --metadata | station_list.csv |
| --output-dir | The current working directory. |
| --year | The current year. |
| --month | The current month. |

!!! note
    One must be cautious using the default year and month, as the day of the month specified in the report may not correspond (e.g. June does not have 31 days).

In the examples, the year and month are not given, so feel free to specify a date yourself or use the default values.

## ecCodes primer

ecCodes provides both command line tools and can be embedded in your own applications.  Below are some useful command
line utilities to work with BUFR data.

### bufr_dump

The `bufr_dump` command is a generic BUFR information tool.  It has many options, but the following will be the most applicable to the exercises:

```bash
bufr_dump -p my_bufr.bufr4
```

This will display BUFR content to your screen.  If you are interested in the values taken by a variable in particular, use the `egrep` command:

```bash
bufr_dump -p my_bufr.bufr4 | egrep -i temperature
```

This will display variables related to temperature in your BUFR data. If you want to do this for multiple types of variables, filter the output using a pipe (`|`):

```bash
bufr_dump -p my_bufr.bufr4 | egrep -i 'temperature|wind'
```

## Converting FM-12 SYNOP to BUFR using synop2bufr from the command line

The eccodes library and synop2bufr module are installed in the wis2box-api container. In order to do the next few exercises we will copy the synop2bufr-exercises directory to the wis2box-api container and run the exercises from there.

```bash
docker cp ~/exercise-materials/synop2bufr-exercises wis2box-api:/root
```

Now we can enter the container and run the exercises:

```bash
docker exec -it wis2box-api /bin/bash
```

### Exercise 1
Navigate to the `/root/synop2bufr-exercises/ex_1` directory and inspect the SYNOP message file message.txt:

```bash
cd /root/synop2bufr-exercises/ex_1
more message.txt
```

!!! question

    How many SYNOP reports are in this file?

Inspect the station list:

```bash
more station_list.csv
```

!!! question

    How many stations are listed in the station list?

!!! question
    Convert `message.txt` to BUFR format.

!!! tip

    See the [synop2bufr primer](#synop2bufr-primer) section.

Inspect the resulting BUFR data using `bufr_dump`.
!!! question
     Compare the latitude and longitude values to those in the station list.

!!! tip

    See the [ecCodes primer](#eccodes-primer) section.

### Exercise 2
Navigate to the `exercise-materials/synop2bufr-exercises/ex_2` directory and inspect the SYNOP message file message.txt:

```bash
cd /root/synop2bufr-exercises/ex_2
more message.txt
```

!!! question

    How many SYNOP reports are in this file?

Inspect the station list:

```bash
more station_list.csv
```

!!! question

    How many stations are listed in the station list?

!!! question
    Convert `message.txt` to BUFR format.

!!! question

    Based on the results of the exercises in this and the previous exercise, how would you predict the number of
    resulting BUFR files based upon the number of SYNOP reports and stations listed in the station metadata file?

Inspect the resulting BUFR data using `bufr_dump`.

!!! question
    Check each of the output BUFR files contain different WIGOS Station Identifiers (WSI).

### Exercise 3
Navigate to the `exercise-materials/synop2bufr-exercises/ex_3` directory and inspect the SYNOP message file message.txt:

```bash
cd /root/synop2bufr-exercises/ex_3
more message.txt
```

This SYNOP message only contains one longer report with more sections.

Inspect the station list:


```bash
more station_list.csv
```

!!! question

    Is it problematic that this file contains more stations than there are reports in the SYNOP message?

!!! note

    The station list file is a source of metadata for `synop2bufr` to provide the information missing in the alphanumeric SYNOP report and required in the BUFR SYNOP.

!!! question
    Convert `message.txt` to BUFR format.

Inspect the resulting BUFR data using `bufr_dump`.

!!! question

    Find the following variables:

    - Air temperature (K) of the report
    - Total cloud cover (%) of the report
    - Total period of sunshine (mins) of the report
    - Wind speed (m/s) of the report

!!! tip

    You may find the last command of the [ecCodes primer](#eccodes-primer) section useful.


### Exercise 4
Navigate to the `exercise-materials/synop2bufr-exercises/ex_4` directory and inspect the SYNOP message file message.txt:

```bash
cd /root/synop2bufr-exercises/ex_4
more message_incorrect.txt
```

!!! question

    What is incorrect about this SYNOP file?

Attempt to convert `message_incorrect.txt` using `station_list.csv`

!!! question

    What problem(s) did you encounter with this conversion?

### Exercise 5
Navigate to the `exercise-materials/synop2bufr-exercises/ex_5` directory and inspect the SYNOP message file message.txt:

```bash
cd /root/synop2bufr-exercises/ex_5
more message.txt
```

Attempt to convert `message.txt` to BUFR format using `station_list_incorrect.csv` 

!!! question

    What problem(s) did you encounter with this conversion?  
    Considering the error presented, justify the number of BUFR files produced.

## Using the wis2box-webapp to convert FM-12 SYNOP to BUFR

### Exercise 1 - Creating an auth token for the wis2box-webapp

In order to submit data to be processed in the wis2box-webapp you will need an auth token for "processes/wis2box".

You can generate this token by logging in to the wis2box management container and using the `wis2box auth add-token` command:

```bash
cd ~/wis2box-1.0b8
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

### Exercise 2 - using the wis2box-webapp to convert FM-12 SYNOP to BUFR

Make sure you have the auth token for "processes/wis2box" that you generated in the previous exercise and that you are connected to your wis2box broker in MQTT Explorer.

Copy the following message:
    
``` {.copy}
AAXX 21121
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

Click submit. You will receive an error message as the station is not registered in the wis2box. Go to the station-editor and import the following station:

``` {.copy}
0-20000-0-15015
```

Ensure the station is associated with the topic you selected in the previous step and then return to the synop2bufr page and repeat the process.

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

Using the station list page, import the following stations:

``` {.copy}
0-20000-0-15020
0-20000-0-15090
```

Ensure that the stations are associated with the topic you selected in the previous exercise and then return to the synop2bufr page and repeat the process.

Three BUFR files should now be generated and there should be no warnings or errors listed in the web application. 

In addition to the basic station information, additional metadata such as the station elevation above sea level and the
barometer height above sea level are required for encoding to BUFR. The fields are included in the station list and station editor pages.
    
### Exercise 4 - debugging

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

## Conclusion

!!! success "Congratulations!"

    In this practical session, you learned:

    - how the synop2bufr tool can be used to convert FM-12 SYNOP reports to BUFR;
    - how to submit a FM-12 SYNOP report through the web-app;
    - how to diagnose and correct simple errors in an FM-12 SYNOP report;
    - the importance of registering stations in the wis2box (and OSCAR/Surface);
    - and the use of the inspect button to view the content of BUFR data.


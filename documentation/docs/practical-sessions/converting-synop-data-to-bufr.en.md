---
title: Converting SYNOP data to BUFR
---

# Converting SYNOP data to BUFR from the command line

!!! abstract "Learning outcomes"
    By the end of this practical session, you will be able to:

    - use the synop2bufr tool to convert FM-12 SYNOP reports to BUFR;
    - diagnose and fix simple coding errors in FM-12 SYNOP reports prior to format conversion;

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
    - Make sure to read the **synop2bufr primer** and **ecCodes primer** sections before starting the exercises.

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


## Conclusion

!!! success "Congratulations!"

    In this practical session, you learned:

    - how the synop2bufr tool can be used to convert FM-12 SYNOP reports to BUFR;
    - how to diagnose and fix simple coding errors in FM-12 SYNOP reports prior to format conversion;



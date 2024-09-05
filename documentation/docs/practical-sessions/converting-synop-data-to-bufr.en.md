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

??? success "Click to reveal answer"
    
    There is 1 SYNOP report, as there is only 1 delimiter (=) at the end of the message.

Inspect the station list:

```bash
more station_list.csv
```

!!! question

    How many stations are listed in the station list?

??? success "Click to reveal answer"

    There is 1 station, the station_list.csv contains one row of station metadata.

!!! question
    Try to convert `message.txt` to BUFR format.

??? success "Click to reveal answer"

    To convert the SYNOP message to BUFR format, use the following command:

    ```bash
    synop2bufr data transform --metadata station_list.csv --output-dir ./ --year 2024 --month 09 message.txt
    ```

!!! tip

    See the [synop2bufr primer](#synop2bufr-primer) section.

Inspect the resulting BUFR data using `bufr_dump`.

!!! question
     Find how to compare the latitude and longitude values to those in the station list.

??? success "Click to reveal answer"

    To compare the latitude and longitude values in the BUFR data to those in the station list, use the following command:

    ```bash
    bufr_dump -p WIGOS_0-20000-0-15015_20240921T120000.bufr4 | egrep -i 'latitude|longitude'
    ```

    This will display the latitude and longitude values in the BUFR data.

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

??? success "Click to reveal answer"

    There are 3 SYNOP reports, as there are 3 delimiters (=) at the end of the message.

Inspect the station list:

```bash
more station_list.csv
```

!!! question

    How many stations are listed in the station list?

??? success "Click to reveal answer"

    There are 3 stations, the station_list.csv contains three rows of station metadata.

!!! question
    Convert `message.txt` to BUFR format.

??? success "Click to reveal answer"

    To convert the SYNOP message to BUFR format, use the following command:

    ```bash
    synop2bufr data transform --metadata station_list.csv --output-dir ./ --year 2024 --month 09 message.txt
    ```

!!! question

    Based on the results of the exercises in this and the previous exercise, how would you predict the number of
    resulting BUFR files based upon the number of SYNOP reports and stations listed in the station metadata file?

??? success "Click to reveal answer"

    To see the produced BUFR-files run the following command:

    ```bash
    ls -l *.bufr4
    ```

    The number of BUFR files produced will be equal to the number of SYNOP reports in the message file.

Inspect the resulting BUFR data using `bufr_dump`.

!!! question
    How can you check the WIGOS Station ID encoded inside the BUFR data of each file produced?

??? success "Click to reveal answer"

    This can be done using the following commands:

    ```bash
    bufr_dump -p WIGOS_0-20000-0-15015_20240921T120000.bufr4 | egrep -i 'wigos'
    ```

    ```bash
    bufr_dump -p WIGOS_0-20000-0-15020_20240921T120000.bufr4 | egrep -i 'wigos'
    ```

    ```bash
    bufr_dump -p WIGOS_0-20000-0-15090_20240921T120000.bufr4 | egrep -i 'wigos'
    ```

    Note that if you have a directory with just these 3 BUFR files, you can use Linux wildcards as follows:

    ```bash
    bufr_dump -p *.bufr4 | egrep -i 'wigos'
    ```

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

??? success "Click to reveal answer"

    No, this is not a problem provided that there exists a row in the station list file with a station TSI matching that of the SYNOP report we are trying to convert.

!!! note

    The station list file is a source of metadata for `synop2bufr` to provide the information missing in the alphanumeric SYNOP report and required in the BUFR SYNOP.

!!! question
    Convert `message.txt` to BUFR format.

??? success "Click to reveal answer"

    This is done using the `transform` command, for example:

    ```bash
    synop2bufr data transform --metadata station_list.csv --output-dir ./ --year 2024 --month 09 message.txt
    ```

Inspect the resulting BUFR data using `bufr_dump`.

!!! question

    Find the following variables:

    - Air temperature (K) of the report
    - Total cloud cover (%) of the report
    - Total period of sunshine (mins) of the report
    - Wind speed (m/s) of the report

??? success "Click to reveal answer"

    To find the variables by keyword in the BUFR data, you can use the following commands:

    ```bash
    bufr_dump -p WIGOS_0-20000-0-15260_20240921T115500.bufr4 | egrep -i 'temperature'
    ```

    You can use the following command to search for multiple keywords:

    ```bash
    bufr_dump -p WIGOS_0-20000-0-15260_20240921T115500.bufr4 | egrep -i 'temperature|cover|sunshine|wind'
    ```

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

??? success "Click to reveal answer"

    The SYNOP report for 15015 is missing the delimiter (`=`) that allows `synop2bufr` to distinguish this report from the next.

Attempt to convert `message_incorrect.txt` using `station_list.csv`

!!! question

    What problem(s) did you encounter with this conversion?

??? success "Click to reveal answer"

    To convert the SYNOP message to BUFR format, use the following command:

    ```bash
    synop2bufr data transform --metadata station_list.csv --output-dir ./ --year 2024 --month 09 message_incorrect.txt
    ```

    Attempting to convert should raise the following errors:
    
    - `[ERROR] Unable to decode the SYNOP message`
    - `[ERROR] Error parsing SYNOP report: AAXX 21121 15015 02999 02501 10103 21090 39765 42952 57020 60001 15020 02997 23104 10130 21075 30177 40377 58020 60001 81041. 10130 is not a valid group!`

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

??? success "Click to reveal answer"

    To convert the SYNOP message to BUFR format, use the following command:

    ```bash
    synop2bufr data transform --metadata station_list_incorrect.csv --output-dir ./ --year 2024 --month 09 message.txt
    ```

    One of the station TSIs (`15015`) has no corresponding metadata in the station-list, which will prohibit synop2bufr from accessing additional necessary metadata to convert the first SYNOP report to BUFR.

    You will see the following warning:

    - `[WARNING] Station 15015 not found in station file`

    You can see the number of BUFR files produced by running the following command:

    ```bash
    ls -l *.bufr4
    ```

    There are 3 SYNOP reports in message.txt but only 2 BUFR files have been produced. This is because one of the SYNOP reports lacked the necessary metadata as mentioned above.

## Conclusion

!!! success "Congratulations!"

    In this practical session, you learned:

    - how the synop2bufr tool can be used to convert FM-12 SYNOP reports to BUFR;
    - how to diagnose and fix simple coding errors in FM-12 SYNOP reports prior to format conversion;



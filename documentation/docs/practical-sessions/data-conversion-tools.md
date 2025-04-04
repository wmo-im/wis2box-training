---
title: Data Conversion Tools
---

# Data Conversion Tools

!!! abstract "Learning Outcomes"
    By the end of this practical session, you will be able to:

    - Access ecCodes command-line tools within the wis2box-api container.
    - Use the synop2bufr tool to convert FM-12 SYNOP reports to BUFR from the command line.
    - Trigger synop2bufr conversion via the wis2box-webapp.
    - Use the csv2bufr tool to convert CSV data to BUFR from the command line.

## Introduction

Data published on WIS2 should use a standard format to ensure interoperability. To lower the barriers to data publication for land-based surface observations, the wis2box provides tools to convert data to BUFR format. These tools are available via the wis2box-api container and can be used from the command line to test the data conversion process.

The main conversions currently supported by wis2box are FM-12 SYNOP reports to BUFR and CSV data to BUFR. FM-12 data is supported as it is still widely used and exchanged in the WMO community, while CSV data is supported to allow the mapping of data produced by automatic weather stations to BUFR format.

### About FM-12 SYNOP

Surface weather reports from land surface stations have historically been reported hourly or at the main (00, 06, 12, and 18 UTC) and intermediate (03, 09, 15, 21 UTC) synoptic hours. Prior to the migration to BUFR, these reports were encoded in the plain text FM-12 SYNOP code form. While the migration to BUFR was scheduled to be complete by 2012, a large number of reports are still exchanged in the legacy FM-12 SYNOP format. Further information on the FM-12 SYNOP format can be found in the WMO Manual on Codes, Volume I.1 (WMO-No. 306, Volume I.1).

### About ecCodes

The ecCodes library is a set of software libraries and utilities designed to decode and encode meteorological data in the GRIB and BUFR formats. It is developed by the European Centre for Medium-Range Weather Forecasts (ECMWF) and documented here: https://confluence.ecmwf.int/display/ECC/ecCodes+documentation.

The wis2box software includes the ecCodes library in the base image of the wis2box-api container. This allows users to access the command-line tools and libraries from within the container. The ecCodes library is used within the wis2box-stack to decode and encode BUFR messages.

### About csv2bufr and synop2bufr

In addition to ecCodes, the wis2box uses the following Python modules that work with ecCodes to convert data to BUFR format:

- **csv2bufr**: https://github.com/World-Meteorological-Organization/csv2bufr
- **synop2bufr**: https://github.com/World-Meteorological-Organization/synop2bufr

These modules can be used standalone or as part of the wis2box-stack. The modules are used to convert CSV and FM-12 SYNOP data to BUFR format. The modules are installed in the wis2box-api container and can be used from the command line.

## Preparation

!!! warning "Prerequisites"

    - Ensure that your wis2box has been configured and started.
    - Ensure you have set up a dataset and configured at least one station in your wis2box.
    - Connect to the MQTT broker of your wis2box instance using MQTT Explorer.
    - Open the wis2box web application (`http://<your-host-name>/wis2box-webapp`) and ensure you are logged in.
    - Open the Grafana dashboard for your instance by going to `http://YOUR-HOST:3000`.

To use the BUFR command-line tools, you will need to be logged in to the wis2box-api container. Unless specified otherwise, all commands should be run on this container. You will also need to have MQTT Explorer open and connected to your broker.

First, connect to your student VM via your SSH client and copy the exercise materials to the wis2box-api container:

```bash
docker cp ~/exercise-materials/data-conversion-exercises wis2box-api:/root
```

Then log in to the wis2box-api container and change to the directory where the exercise materials are located:

```bash
cd ~/wis2box-1.0.0rc1
python3 wis2box-ctl.py login wis2box-api
cd /root/data-conversions-exercises
```

Confirm that the tools are available, starting with ecCodes:

```bash
bufr_dump -V
```

You should get the following response:

```
ecCodes Version 2.36.0
```

Next, check the synop2bufr version:

```bash
synop2bufr --version
```

You should get the following response:

```
synop2bufr, version 0.7.0
```

Next, check csv2bufr:

```bash
csv2bufr --version
```

You should get the following response:

```
csv2bufr, version 0.8.5
```

## Using the BUFR Command-Line Tools

### bufr_ls

In this first exercise, you will use the `bufr_ls` command to inspect the headers of a BUFR file and determine the type of the contents of the file.

Now use the following command to run `bufr_ls` on the file `bufr-cli-ex1.bufr4`:

```bash
bufr_ls bufr-cli-ex1.bufr4
```

You should see the following output:

```bash
bufr-cli-ex1.bufr4
centre                     masterTablesVersionNumber  localTablesVersionNumber   typicalDate                typicalTime                numberOfSubsets
cnmc                       29                         0                          20231002                   000000                     1
1 of 1 messages in bufr-cli-ex1.bufr4

1 of 1 total messages in 1 file
```

Various options can be passed to `bufr_ls` to change both the format and header fields printed.

!!! question
     
    What would be the command to list the previous output in JSON format?

    You can run the command `bufr_ls` with the `-h` flag to see the available options.

??? success "Click to Reveal Answer"
    You can change the output format to JSON using the `-j` flag, i.e.
    ```bash
    bufr_ls -j bufr-cli-ex1.bufr4
    ```

    When run, this should give you the following output:
    ```
    { "messages" : [
      {
        "centre": "cnmc",
        "masterTablesVersionNumber": 29,
        "localTablesVersionNumber": 0,
        "typicalDate": 20231002,
        "typicalTime": "000000",
        "numberOfSubsets": 1
      }
    ]}
    ```

The output printed represents the values of some of the header keys in the BUFR file.

On its own, this information is not very informative, with only limited information on the file contents provided.

When examining a BUFR file, we often want to determine the type of data contained in the file and the typical date/time of the data in the file. This information can be listed using the `-p` flag to select the headers to output. Multiple headers can be included using a comma-separated list.

You can use the following command to list the data category, sub-category, typical date, and time:
    
```bash
bufr_ls -p dataCategory,internationalDataSubCategory,typicalDate,typicalTime -j bufr-cli-ex1.bufr4
```

!!! question

    Execute the previous command and interpret the output using [Common Code Table C-13](https://github.com/wmo-im/CCT/blob/master/C13.csv) to determine the data category and sub-category.

    What type of data (data category and sub-category) is contained in the file? What is the typical date and time for the data?

??? success "Click to Reveal Answer"
    
    ```
    { "messages" : [
      {
        "dataCategory": 2,
        "internationalDataSubCategory": 4,
        "typicalDate": 20231002,
        "typicalTime": "000000"
      }
    ]}
    ```

    From this, we see that:

    - The data category is 2, indicating **"Vertical soundings (other than satellite)"** data.
    - The international sub-category is 4, indicating **"Upper-level temperature/humidity/wind reports from fixed-land stations (TEMP)"** data.
    - The typical date and time are 2023-10-02 and 00:00:00z, respectively.

### bufr_dump

The `bufr_dump` command can be used to list and examine the contents of a BUFR file, including the data itself.

In this exercise we will use a BUFR file that is the same as your created during the initial csv2bufr practical session using the wis2box-webapp.

Download the sample-file to the wis2box management container directly with the following command:

``` {.copy}
curl https://training.wis2box.wis.wmo.int/sample-data/bufr-cli-ex2.bufr4 --output bufr-cli-ex2.bufr4
```

Now run the `bufr_dump` command on the file, using the `-p` flag to output the data in plain text (key=value format):

```{.copy}
bufr_dump -p bufr-cli-ex2.bufr4
```

You should see around 240 keys output, many of which are missing. This is typical with real world data as not all the eccodes keys are populated with reported data.

!!! hint
    The missing values can be filtered using tools such as `grep`:
    ```{.copy}
    bufr_dump -p bufr-cli-ex2.bufr4 | grep -v MISSING
    ```
## synop2bufr conversion

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

??? success "Click to reveal answer"

    You will 
    
    If you successfully ingested and published the last data sample, you should have received 10 new notifications on the wis2box MQTT broker. Each notification correspond to data for one station for one observation timestamp.

    The plugin `wis2box.data.bufr4.ObservationDataBUFR` splits the BUFR file into individual BUFR messages and publishes one message for each station and observation timestamp.

## csv2bufr conversion

Please download the CSV example file into your current location as follows:

```{.copy}
curl https://training.wis2box.wis.wmo.int/sample-data/aws-example.csv --output aws-example.csv
```

And display the content of the file with:

```{.copy}
cat csv2bufr-ex1.csv
```

Let's attempt to convert the file to BUFR format using the `csv2bufr` command:

```{.copy}
csv2bufr data transform --bufr-template aws-template ./aws-example.csv
```

## Conclusion

!!! success "Congratulations"
    In this practical session you have learned:

    - how to use some of the BUFR command line tools available in the wis2box management container;
    - how to use syn2bufr, csv2bufr and bufr2bufr to convert data to BUFR format;


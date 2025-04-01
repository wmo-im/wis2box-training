---
title: Data conversion tools
---

# Data conversion tools

!!! abstract "Learning outcomes"
    By the end of this practical session, you will be able to:

    - access eccodes command line tools within the wis2box-api container
    - use the synop2bufr tool to convert FM-12 SYNOP reports to BUFR from the command line
    - trigger synop2bufr conversion via the wis2box-webapp
    - use the csv2bufr tool to convert CSV data to BUFR from the command line

## Introduction

Data published on WIS2 should use a standard format to ensure interoperability. To lower the barriers to data publication for land-based surface observations, the wis2box provides tools to convert data to BUFR format. These tools are available via the wis2box-api container and can be used from the command line to test the data conversion process. 

The main conversions currently supported by wis2box are FM-12 SYNOP reports to BUFR and CSV data to BUFR. FM-12 data is supported as it is still widely used and exchanged in the WMO community, while CSV data is supported to allow the mapping of data produces by automatic weather stations to BUFR format.

### About FM-12 SYNOP

Surface weather reports from land surface stations have historically been reported hourly or at the main (00, 06, 12 and 18 UTC) and intermediate (03, 09, 15, 21 UTC) synoptic hours. Prior to the migration to BUFR these reports were encoded in the plain text FM-12 SYNOP code form. Whilst the migration to BUFR was scheduled to be complete by 2012 a large number of reports are still exchanged in the legacy FM-12 SYNOP format. Further information on the FM-12 SYNOP format can be found in the WMO Manual on Codes, Volume I.1 (WMO-No. 306, Volume I.1).

## Preparation

!!! warning "Prerequisites"

    - Ensure that your wis2box has been configured and started.
    - Ensure you have setup a dataset and configured at least one station in your wis2box
    - Connect to the MQTT broker of your wis2box instance using MQTT Explorer.
    - Open the wis2box web application (`http://<your-host-name>/wis2box-webapp`) and ensure you are logged in.
    - Open the Grafana dashboard for your instance by going to `http://<your-host>:3000`

## Preparation

In order to use the BUFR command line tools you will need to be logged in to the wis2box-api container
and unless specified otherwise all commands should be run on this container. You will also need to have
MQTT Explorer open and connected to your broker.

First connect to your student VM via your ssh client and then log in the to wis2box-api container: 

```{.copy}
cd ~/wis2box-1.0.0rc1
python3 wis2box-ctl.py login wis2box-api
```

Confirm the that tools are available, starting with ecCodes:

``` {.copy}
bufr_dump -V
```
You should get the following response:

```
ecCodes Version 2.28.0
```

Next check csv2bufr:

```{.copy}
csv2bufr --version
```

You should get the following response:

```
csv2bufr, version 0.7.4
```

Finally, create a working directory to work in:

```{.copy}
cd /data/wis2box
mkdir -p working/bufr-cli
cd working/bufr-cli
```

You are now ready to start using the BUFR tools.

## Using the BUFR command line tools

### bufr_ls
In this first exercise you will use the `bufr_ls` command to inspect the headers of a BUFR file and to determine the 
contents of the file. The following headers are included in a BUFR file:

| header                            | ecCodes key                  | description                                                                                                                                           |
|-----------------------------------|------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------|
| originating/generating centre     | centre                       | The originating / generating centre for the data                                                                                                      |
| originating/generating sub-centre | bufrHeaderSubCentre          | The originating / generating sub centre for the data                                                                                                  | 
| Update sequence number            | updateSequenceNumber         | Whether this is the first version of the data (0) or an update (>0)                                                                                   |               
| Data category                     | dataCategory                 | The type of data contained in the BUFR message, e.g. suface data. See [BUFR Table A](https://github.com/wmo-im/BUFR4/blob/master/BUFR_TableA_en.csv)  |
| International data sub-category   | internationalDataSubCategory | The sub-type of data contained in the BUFR message, e.g. suface data. See [Common Code Table C-13](https://github.com/wmo-im/CCT/blob/master/C13.csv) |
| Year                              | typicalYear (typicalDate)    | Most typical time for the BUFR message contents                                                                                                       |
| Month                             | typicalMonth (typicalDate)   | Most typical time for the BUFR message contents                                                                                                       |
| Day                               | typicalDay (typicalDate)     | Most typical time for the BUFR message contents                                                                                                       |
| Hour                              | typicalHour (typicalTime)    | Most typical time for the BUFR message contents                                                                                                       |
| Minute                            | typicalMinute (typicalTime)  | Most typical time for the BUFR message contents                                                                                                       |
| BUFR descriptors                  | unexpandedDescriptors        | List of one, or more, BUFR descriptors defining the data contained in the file                                                                        |

Download the example file directly into the wis2box-management container using the following command:

``` {.copy}
curl https://training.wis2box.wis.wmo.int/sample-data/bufr-cli-ex1.bufr4 --output bufr-cli-ex1.bufr4
```

Now use the following command to run `bufr_ls` on this file:

```bash
bufr_ls bufr-cli-ex1.bufr4
```

You should see the following output:

```bash
bufr-cli-ex1.bufr4
centre                     masterTablesVersionNumber  localTablesVersionNumber   typicalDate                typicalTime                numberOfSubsets
cnmc                       29                         0                          20231002                   000000                     1
1 of 1 messages in bufr-cli-ex1.bufr4

1 of 1 total messages in 1 files
```

On its own this information is not very informative, with only limited information on the file contents provided. 

The default output does not provide information on the observation, or data, type and is in a format that is not
very easy to read. However, various options can be passed to `bufr_ls` to change both the format and header fields 
printed.  

Use `bufr_ls` without any arguments to view the options:

```{.copy}
bufr_ls
```

You should see the following output:

```
NAME    bufr_ls

DESCRIPTION
        List content of BUFR files printing values of some header keys.
        Only scalar keys can be printed.
        It does not fail when a key is not found.

USAGE
        bufr_ls [options] bufr_file bufr_file ...

OPTIONS
        -p key[:{s|d|i}],key[:{s|d|i}],...
                Declaration of keys to print.
                For each key a string (key:s), a double (key:d) or an integer (key:i)
                type can be requested. Default type is string.
        -F format
                C style format for floating-point values.
        -P key[:{s|d|i}],key[:{s|d|i}],...
                As -p adding the declared keys to the default list.
        -w key[:{s|d|i}]{=|!=}value,key[:{s|d|i}]{=|!=}value,...
                Where clause.
                Messages are processed only if they match all the key/value constraints.
                A valid constraint is of type key=value or key!=value.
                For each key a string (key:s), a double (key:d) or an integer (key:i)
                type can be specified. Default type is string.
                In the value you can also use the forward-slash character '/' to specify an OR condition (i.e. a logical disjunction)
                Note: only one -w clause is allowed.
        -j      JSON output
        -s key[:{s|d|i}]=value,key[:{s|d|i}]=value,...
                Key/values to set.
                For each key a string (key:s), a double (key:d) or an integer (key:i)
                type can be defined. By default the native type is set.
        -n namespace
                All the keys belonging to the given namespace are printed.
        -m      Mars keys are printed.
        -V      Version.
        -W width
                Minimum width of each column in output. Default is 10.
        -g      Copy GTS header.
        -7      Does not fail when the message has wrong length

SEE ALSO
        Full documentation and examples at:
        <https://confluence.ecmwf.int/display/ECC/bufr_ls>
```

Now run the same command on the example file but output the information in JSON.

!!! question
    What flag do you pass to the `bufr_ls` command to view the output in JSON format?

??? success "Click to reveal answer"
    You can change the output format to json using the `-j` flag, i.e.
    `bufr_ls -j <input-file>`. This can be more readable than the default output format. See the example output below:

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

When examining a BUFR file we often want to determine the type of data contained in the file and the typical date / time
of the data in the file. This information can be listed using the `-p` flag to select the headers to output. Multiple
headers can be included using a comma separated list. 

Using the `bufr_ls` command inspect the test file and identify the type of data contained in the file and the typical date and time for that data.

??? hint
    The ecCodes keys are given in the table above. We can use the following to list the dataCategory and
    internationalDataSubCategory of the BUFR data:

    ```
    bufr_ls -p dataCategory,internationalDataSubCategory bufr-cli-ex1.bufr4
    ```

    Additional keys can be added as required.

!!! question
    What type of data (date category and sub category) are contained in the file? What is the typical date and time
    for the data?

??? success "Click to reveal answer"
    The command you need to run should have been similar to:
    
    ```
    bufr_ls -p dataCategory,internationalDataSubCategory,typicalDate,typicalTime -j bufr-cli-ex1.bufr4
    ```

    You may have additional keys, or listed the year, month, day etc individually. The output should
    be similar to below, depending on whether you selected JSON or default output.

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

    From this we see that:

    - The data category is 2, from [BUFR Table A](https://github.com/wmo-im/BUFR4/blob/master/BUFR_TableA_en.csv)
      we can see that this file contains "Vertical soundings (other than satellite)" data.
    - The international sub category is 4, indicating 
      "Upper-level temperature/humidity/wind reports from fixed-land stations (TEMP)" data. This information can be looked
      up in [Common Code Table C-13](https://github.com/wmo-im/CCT/blob/master/C13.csv) (row 33). Note the combination
      of category and sub category.
    - The typical date and time are 2023/10/02 and 00:00:00z respectively.

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
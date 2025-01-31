---
title: Working with BUFR data
---

# Working with BUFR data

!!! abstract "Learning outcomes"
    In this practical session you will be introduced to some of the BUFR tools included in the **wis2box-api** container that are used to transform data to BUFR format and to read the content encoded in BUFR.
    
    You will learn:

    - how to inspect the headers in the BUFR file using the `bufr_ls` command
    - how to extract and inspect the data within a bufr file using `bufr_dump`
    - the basic structure of the bufr templates used in csv2bufr and how to use the command line tool
    - and how to make basic changes to the bufr templates and how to update the wis2box to use the revised
      version

## Introduction

The plugins that produces notifications with BUFR data use processes in the wis2box-api to work with BUFR data, for example to transform the data from CSV to BUFR or from BUFR to geojson.

The wis2box-api container includes a number of tools to work with BUFR data.

These include the tools developed by ECMWF and included in the ecCodes software, more information on these can be 
found on the [ecCodes website](https://confluence.ecmwf.int/display/ECC/BUFR+tools). 

In this session you will be introduced to the `bufr_ls` and `bufr_dump` from the ecCodes software package and advanced configuration of the csv2bufr tool.

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

### Exercise 1 - bufr_ls
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

    

### Exercise 2 - bufr_dump

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

The example BUFR file for this exercise comes from the csv2bufr practical session. Please download the original CSV file into your current location as follows:

```{.copy}
curl https://training.wis2box.wis.wmo.int/sample-data/csv2bufr-ex1.csv --output csv2bufr-ex1.csv
```

And display the content of the file with:

```{.copy}
more csv2bufr-ex1.csv
```

!!! question
    Use the following command to display column 18 in the CSV file and you will find the reported mean sea level pressure (msl_pressure):

    ```{.copy}
    more csv2bufr-ex1.csv | cut -d ',' -f 18
    ```
    
    Which key in the BUFR output corresponds to the mean sea level pressure ?

??? hint
    Tools such as `grep` can be used in combination with `bufr_dump`. For example:
    
    ```{.copy}
    bufr_dump -p bufr-cli-ex2.bufr4 | grep -i "pressure"
    ```
    
    would filter the contents of `bufr_dump`to only those lines containing the word pressure. Alternatively, 
    the output could be filtered on a value.

??? success "Click to reveal answer"
    The key "pressureReducedToMeanSeaLevel" corresponds to the msl_pressure column in the input CSV file.

Spend a few minutes examining the rest of the output, comparing to the input CSV file before moving on to the next
exercise. For example, you can try to find the keys in the BUFR output that correspond to relative humidity (column 23 in the CSV file) and air temperature (column 21 in the CSV file).

### Exercise 3 - csv2bufr mapping files

The csv2bufr tool can be configured to process tabular data with different columns and BUFR sequences. 

This is done by the way of a configuration file written in the JSON format. 

Like BUFR data itself, the JSON file contains a header section and a data section, with these broadly corresponding to the same sections in BUFR. 

Additionally, some formatting options are specified within the JSON file. 

The JSON file for the default mapping can be view via the link below (right-click and open in new tab):

[aws-template.json](https://raw.githubusercontent.com/wmo-im/csv2bufr/main/csv2bufr/templates/resources/aws-template.json)

Examine the `header` section of the mapping file (shown below) and compare to the table from exercise 1 (ecCodes key column):

```
"header":[
    {"eccodes_key": "edition", "value": "const:4"},
    {"eccodes_key": "masterTableNumber", "value": "const:0"},
    {"eccodes_key": "bufrHeaderCentre", "value": "const:0"},
    {"eccodes_key": "bufrHeaderSubCentre", "value": "const:0"},
    {"eccodes_key": "updateSequenceNumber", "value": "const:0"},
    {"eccodes_key": "dataCategory", "value": "const:0"},
    {"eccodes_key": "internationalDataSubCategory", "value": "const:2"},
    {"eccodes_key": "masterTablesVersionNumber", "value": "const:30"},
    {"eccodes_key": "numberOfSubsets", "value": "const:1"},
    {"eccodes_key": "observedData", "value": "const:1"},
    {"eccodes_key": "compressedData", "value": "const:0"},
    {"eccodes_key": "typicalYear", "value": "data:year"},
    {"eccodes_key": "typicalMonth", "value": "data:month"},
    {"eccodes_key": "typicalDay", "value": "data:day"},
    {"eccodes_key": "typicalHour", "value": "data:hour"},
    {"eccodes_key": "typicalMinute", "value": "data:minute"},
    {"eccodes_key": "unexpandedDescriptors", "value":"array:301150, 307096"}
],
```

Here you can see the same headers as available in the output from the `bufr_ls` command. In the mapping file the value 
for these can be set to a column from the CSV input file, a constant value or an array of constant values.

!!! question
    Look at the example header section above. How would you specify a constant value, a value from the input CSV data
    file and an array of constants?

??? success "Click to reveal answer"
    - Constant values can be set by setting the `value` property to `"value": "const:<your-constant>"`.
    - Values can be set to a column from the input CSV by setting the `value` property to `"value": "data:<your-column>"`.
    - Arrays can be set by setting the `value` property to `"value": "array:<comma-seperated-values>"`.

Now examine the data section of the JSON mapping file (note, the output has been truncated):

```
    "data": [
        {"eccodes_key": "#1#wigosIdentifierSeries", "value":"data:wsi_series", "valid_min": "const:0", "valid_max": "const:0"},
        {"eccodes_key": "#1#wigosIssuerOfIdentifier", "value":"data:wsi_issuer", "valid_min": "const:0", "valid_max": "const:65534"},
        {"eccodes_key": "#1#wigosIssueNumber", "value":"data:wsi_issue_number", "valid_min": "const:0", "valid_max": "const:65534"},
        {"eccodes_key": "#1#wigosLocalIdentifierCharacter", "value":"data:wsi_local"},
        {"eccodes_key": "#1#latitude", "value": "data:latitude", "valid_min": "const:-90.0", "valid_max": "const:90.0"},
        {"eccodes_key": "#1#longitude", "value": "data:longitude", "valid_min": "const:-180.0", "valid_max": "const:180.0"},
        {"eccodes_key": "#1#heightOfStationGroundAboveMeanSeaLevel", "value":"data:station_height_above_msl", "valid_min": "const:-400", "valid_max": "const:9000"},
        {"eccodes_key": "#1#heightOfBarometerAboveMeanSeaLevel", "value":"data:barometer_height_above_msl", "valid_min": "const:-400", "valid_max": "const:9000"},
        {"eccodes_key": "#1#blockNumber", "value": "data:wmo_block_number", "valid_min": "const:0", "valid_max": "const:99"},
        {"eccodes_key": "#1#stationNumber", "value": "data:wmo_station_number", "valid_min": "const:0", "valid_max": "const:999"},
        {"eccodes_key": "#1#stationType", "value": "data:station_type", "valid_min": "const:0", "valid_max": "const:3"},
        {"eccodes_key": "#1#year", "value": "data:year", "valid_min": "const:1600", "valid_max": "const:2200"},
        {"eccodes_key": "#1#month", "value": "data:month", "valid_min": "const:1", "valid_max": "const:12"},
        {"eccodes_key": "#1#day", "value": "data:day", "valid_min": "const:1", "valid_max": "const:31"},
        {"eccodes_key": "#1#hour", "value": "data:hour", "valid_min": "const:0", "valid_max": "const:23"},
        {"eccodes_key": "#1#minute", "value": "data:minute", "valid_min": "const:0", "valid_max": "const:59"},
        {"eccodes_key": "#1#nonCoordinatePressure", "value": "data:station_pressure", "valid_min": "const:50000", "valid_max": "const:150000"},
        {"eccodes_key": "#1#pressureReducedToMeanSeaLevel", "value": "data:msl_pressure", "valid_min": "const:50000", "valid_max": "const:150000"},
        {"eccodes_key": "#1#nonCoordinateGeopotentialHeight", "value": "data:geopotential_height", "valid_min": "const:-1000", "valid_max": "const:130071"},
        ...
    ]
```

Refer back to exercise 2 in this practical session and the task identifying the ecCodes key corresponding to the
mean sea level pressure.

!!! question
    Can you identify the row in the data section that performs the mapping between the CSV input file and ecCodes key
    used to encode the mean sea level pressure data?

??? success "Click to reveal answer"
    You will have hopefully identified the line below:
    
    ```
    {"eccodes_key": "#1#pressureReducedToMeanSeaLevel", "value": "data:msl_pressure", "valid_min": "const:50000", "valid_max": "const:150000"},
    ```
    
    This instructs the csv2bufr tool to map the data from the `msl_pressure` column to the `#1#pressureReducedToMeanSeaLevel` element in BUFR.

!!! question "Bonus question"
    Can you guess what the `valid_min` and `valid_max` properties do?
 
??? success "Click to reveal answer" 
    These specify the valid minimum and maximum values for the different elements. Values falling outside of the 
    range specified will result in a warning message and the data set to missing in the output BUFR file.

Download the csv2bufr mapping file to the wis2box management container:

``` {.copy}
curl https://raw.githubusercontent.com/wmo-im/csv2bufr/main/csv2bufr/templates/resources/aws-template.json --output aws-template.json 
```

Now modify the file to change the limits for air temperature, for example set to realistic limits but in degrees Celsius:

```
        {"eccodes_key": "#1#airTemperature", "value": "data:air_temperature", "valid_min": "const:-60", "valid_max": "const:60"},
```

Now use `csv2bufr` to transform the example CSV data file to BUFR using the modified mapping file:

```{.copy}
csv2bufr data transform --bufr-template aws-template.json csv2bufr-ex1.csv
```

You should see the following output:

```
CLI:    ... Transforming ex1.csv to BUFR ...
CLI:    ... Processing subsets:
#1#airTemperature: Value (301.25) out of valid range (-60 - 60).; Element set to missing
CLI:    ..... 384 bytes written to ./WIGOS_0-20000-0-99100_20230929T090000.bufr4
CLI:    End of processing, exiting.
```

This suggests a mismatch between the units in the input data and that expected by the mapping file.

Use the `bufr_dump` command to confirm that the first air temperature value has been set to missing in the file that was produced:

```{.copy}
bufr_dump -p WIGOS_0-20000-0-99100_20230929T090000.bufr4 | grep airTemperature
```

!!! note
    Note that the units used in BUFR are fixed, Kelvin for temperature, Pascals for pressure etc. However,
    csv2bufr can perform simple unit conversions by scaling and adding an offset.

As the final part of this exercise, edit the the mapping file again and add a scale and offset to the 
airTemperature line.

```json
        {"eccodes_key": "#1#airTemperature", "value": "data:air_temperature", "valid_min": "const:-60", "valid_max": "const:60", "scale": "const:0", "offset":"const:273.15"},
```

And edit  the air_temperature column in the 'csv2bufr-ex1.csv' to be in Celsius rather than Kelvin: 301.25 K = 28.1 degrees C.

Rerun the conversion:

```{.copy}
csv2bufr data transform --bufr-template aws-template.json csv2bufr-ex1.csv
```
 
Run BUFR dump and confirm that the airTemperature is correctly encoded.
    
```{.copy}
bufr_dump -p WIGOS_0-20000-0-99100_20230929T090000.bufr4 | grep airTemperature
```

You should see the following output:

```
#1#airTemperature=301.25
#2#airTemperature=MISSING
```

### Exercise 4 - installing new csv2bufr templates

The `bufr-template` used by csv2bufr can be specified by providing a filename to the command, as per the above example,
or by setting a search path with an environment variable and by specifying the template name. The template name must match
the filename but without the extension, with the file located on the search path. 

!!! bug
    Currently, the default mapping file used in the csv2bufr automated workflow sets the originating centre
    header to indicate that the data have originating with the WMO Secretariat, see the JSON snippet 
    from the default `bufr-template` below:

    ```
        {"eccodes_key": "bufrHeaderCentre", "value": "const:0"}, 
    ```

In this final exercise you will download the template used, correct with the appropriate centre code and install 
in the wis2box management container. Suggested originating centre codes are listed below, these will need to be
confirmed with your WIS focal points prior to data exchange.

| Centre                         | Code |
|--------------------------------|------|
| Melbourne (RSMC), Australia    | 67   |
| Brasilia (RSMC), Brazil        | 43   |
| Beijing (RSMC), China          | 38   |
| New Delhi (RSMC), India        | 28   |
| Indonesia (NMC)                | 195  |
| Malaysia (NMC)                 | 73   |
| Federated States of Micronesia | 197  |
| Wellington (RSMC), New Zealand | 69   |
| Oman (NMC)                     | 127  |
| Philippines (NMC)              | 201  |
| Seoul, Republic of Korea       | 40   |
| Dili (NMC), Timor-Leste        | TBC  |

For this exercise, first create a directory in which to store the mappings:

```{.copy}
cd /data/wis2box
mkdir bufr-templates
```

Navigate to the directory and download the default bufr-template:

```{.copy}
cd bufr-templates
curl https://raw.githubusercontent.com/wmo-im/csv2bufr/main/csv2bufr/templates/resources/aws-template.json \
    --output aws-template-custom.json
```

Make sure the file 'aws-template-custom.json' is in the directory '/data/wis2box/bufr-templates':

```{.copy}
ls /data/wis2box/bufr-templates
```

Edit the file using `vi` or your favourite text editor and update the value of the `bufrHeaderCentre`.

Now try the commands from the block below:

```{.copy}
curl https://training.wis2box.wis.wmo.int/sample-data/csv2bufr-ex1.csv --output csv2bufr-ex1.csv
export CSV2BUFR_TEMPLATES=/data/wis2box/bufr-templates
csv2bufr data transform --bufr-template aws-template-custom csv2bufr-ex1.csv
```

Inspect the output file using `bufr_ls` and confirm that the originating centre in the headers is updated.

## Housekeeping

Clean up your working directory by removing files you no longer need and clean up your station list to remove any
example stations you may have created and that are no longer needed.

## Conclusion

!!! success "Congratulations"
    In this practical session you have learned:

    - how to use some of the BUFR command line tools available in the wis2box management container;
    - how to make basic changes to the mapping file used in the csv2bufr tool;
    - and how to install new csv2bufr mappping templates in wis2box.

!!! info "Next steps"
        
    In this session we have covered only a small part of the csv2bufr and ecCodes BUFR tools functionality. 
    For example, the csv2bufr tool includes the ability to create new 'bufr-template' files provided different BUFR 
    sequences. As an example, the template for BUFR sequence (301150, 307096), used by the default 
    `aws-template`, can be generated with the command:
    
    ```{.copy}
    csv2bufr mappings create 301150 307096 > bufr-template.json
    ```
    
    This file can be modified to add and map additional variables from the CSV data file, use different quality 
    control values (valid_min and valid_max) and perform some basic (linear) unit conversions. Further information
    is available via the csv2bufr documentation pages: 

    [https://csv2bufr.readthedocs.io/en/latest/](https://csv2bufr.readthedocs.io/en/latest/).

    Further information on the ecCodes BUFR tools can be found at: 

    [https://confluence.ecmwf.int/display/ECC/BUFR+tools](https://confluence.ecmwf.int/display/ECC/BUFR+tools).
    

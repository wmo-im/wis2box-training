---
title: BUFR command line tools
---

# BUFR command line tools and configuring csv2bufr

!!! abstract
    In this session you will be introduced to some of the BUFR command line tools included in the wis2box
    management container.

## Introduction

The wis2box management container contains some tools for working with BUFR files from the command line. 
These include the tools developed by ECMWF and included in the ecCodes software, more information on these can be 
found on the [ecCodes website](https://confluence.ecmwf.int/display/ECC/BUFR+tools). Other tools include those
developed as part of the wis2box development, including csv2bufr and synop2bufr that you have previously used
but via the wis2box web-application. In this session you will be introduced to the `bufr_ls` and `bufr_dump` from
the ecCodes software package and advanced configuration of the csv2bufr tool.

## Preparation

In order to use the BUFR command line tools you will need to be logged in to the wis2box management container. 
First connect to your student VM via your ssh client and then log in the to management container: 

```{.copy}
cd ~/wis2box-1.0b5
python3 wis2box-ctl.py login
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

Download the example file from the link below and copy the file to your student VM: 

Example file: [bufr-cli-ex1.bufr4](/sample-data/bufr-cli-ex1.bufr4)

!!! hint
    You can also download the file directly on your student VM. Log in to the wis2box management container, navigate to 
    your working directory and use `curl`, e.g. 
    
    ``` {.copy}
    curl https://training.wis2box.wis.wmo.int/sample-data/bufr-cli-ex1.bufr4 --output bufr-cli-ex1.bufr4
    ```

Now run the command `bufr_ls` on the file.

```{.copy}
bufr_ls bufr-cli-ex1.bufr4
```
You should see the following output:

Various options can be passed to `bufr_ls`, use `bufr_ls` without and arguments to view the options. Now run the same
command to output the information in JSON.

!!! question
    What flag do you pass to the `bufr_ls` command to view the output in JSON format?

??? success "Click to reveal answer"
    You can change the output format to json using the `-j` flag, i.e.
    `bufr_ls -j <input-file>`. This can be more readable than the default output format.

When examining a BUFR file we often want to determine the type of data contained in the file and the typical date / time
of the data in the file. This information can be listed using the `-p` flag to select the headers to output. Multiple
headers can be included using a comma separated list. Using the `bufr_ls` command inspect the test file and identify
the type of data contained in the file and the typical date and time for that data.

??? hint
    The ecCodes keys are given in the table above.

!!! question
    What type of data (date category and sub category) are contained in the file? What is the typical date and time
    for the data?

??? success "Click to reveal the answer"
    answer to follow

### Exercise 2 - bufr_dump

The `bufr_dump` command can be used to list and examine the contents of a BUFR file, including the data itself.
Use the second file from the previous exercise and list the contents using:

```{.copy}
bufr_dump -p bufr-cli-ex1b.bufr4
```

The `-p` flag instructs bufr_dump to output the decoded values in plain text and as a list of key / value pairs,
with one key/value pair per line. The example BUFR file for this exercise comes from the csv2bufr practical session,
the input file can be downloaded from the link below. After downloading, examine the input files and how they compare
to the data in the BUFR file.

!!! question
    Which key in the BUFR output corresponds to the mean sea level pressure (msl_pressure) in the CSV file?

??? hint
    Tools such as `grep` can be used in combination with `bufr_dump`. For example:
    
    ```{.copy}
    bufr_dump -p bufr-cli-ex1b.bufr4 | grep -i "pressure"
    ```
    
    would filter the contents of `bufr_dump`to only those lines containing the word pressure. Alternatively, 
    the output could be filtered on a value.

??? success "Click to reveal the answer"
    The key "pressureReducedToMeanSeaLevel" corresponds to the msl_pressure column in the input CSV file.

Spend a few minutes examing the rest of the output, comparing to the input CSV file before moving on to the next
exercise.

### Exercise 3 - csv2bufr mapping files

The csv2bufr tool can be configured to process tabular data with different columns and BUFR sequences. This is done by
the way of a configuration file written in the JSON format. Like BUFR data itself, the JSON file contains a header section
and a data section, with these broadly corresponding to the same sections in BUFR. Additionally, some formatting options
are specified within the JSON file. 




### Exercise 4 - debugging

---
title: Converting SYNOP data to BUFR
---

# Converting SYNOP data to BUFR

## Introduction

Surface synoptic observations (SYNOP) data are used to report weather observations from surface
stations (manned or automated).  [synop2bufr](https://github.com/wmo-im/synop2bufr) is a tool to
help convert SYNOP to BUFR data.  [ecCodes](https://confluence.ecmwf.int/display/ECC/ecCodes+Home)
is a package to reading and writing GRIB and BUFR formats.

In this session you will learn about converting a SYNOP report into the WMO BUFR format using the
above mentioned tools, as well as the relationship between SYNOP reports and BUFR messages.

!!! note

    The argument `-v ~/exercise-materials/synop2bufr-exercises:/exercises` ensures that the directory 'synop2bufr-exercises' on your student VM is accessible as '/exercises' inside your container.

## synop2bufr primer

Below are essential `synop2bufr` commands and configurations:

### transform
The `transform` function converts a SYNOP message to BUFR:

```bash
synop2bufr transform --metadata my_file.csv --output-dir ./my_folder --year message_year --month message_month my_SYNOP.txt
```

Note that if the metadata, output directory, year and month options are not specified, they will assume their default values:

| Option      | Default |
| ----------- | ----------- |
| --metadata | metadata.csv |
| --output-dir | The current working directory. |
| --year | The current year. |
| --month | The current month. |

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

## Preparation

!!! note

    Ensure that you are logged into your student VM. Ensure you have the exercise-materials downloaded in your home-directory as detailed [previously](https://wmo-im.github.io/wis2box-training/practical-sessions/access-your-student-vm/#download-the-exercise-materials).

Launch the **synop2bufr** image as an interactive Docker container using the following command:

```bash
docker run -it -v ~/exercise-materials/synop2bufr-exercises:/exercises --userwmoim/synop2bufr
```

## Inspecting SYNOP data and BUFR conversion

To begin with the exercises, login to your VM, and start the **synop2bufr** container with the following command:

```bash
docker run -it -v ~/exercise-materials/synop2bufr-exercises:/exercises:rw synop2bufr
```

!!! note

    Ensure that you are logged in the docker container started in the [preparation step](#Preparation). If needed consult the [Docker cheatsheet](../cheatsheets/docker.md).

### Exercise 1
Navigate to the `ex_1` directory and inspect a SYNOP message:

```bash
cd /exercises/ex_1
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

Convert `message.txt` to BUFR format.

!!! tip

    See the [synop2bufr primer](#synop2bufr-primer) section.

!!! note

    BUFR files have no set file extension, however it is recommended to use `bufr4`.

Inspect the resulting BUFR data and compare the latitude and longitude values to those in the station list.

!!! tip

    See the [ecCodes primer](#eccodes-primer) section.

### Exercise 2
Navigate to the `ex_2` directory and inspect another SYNOP message:

```bash
cd ../ex_2
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

Convert `message.txt` to BUFR format.

!!! question

    Based on the results of the exercises in this and the previous exercise, how would you predict the number of
    resulting BUFR files based upon the number of SYNOP reports and stations listed in the station metadata file?

Use bufr_dump to check each of the output BUFR files contain different WIGOS Station Identifiers (WSI).

### Exercise 3
Navigate to the `ex_3` directory and inspect the SYNOP message:

```bash
cd ../ex_3
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

Convert `message.txt` to BUFR format.

Use bufr_dump to find the following:

- Air temperature (K) of the report
- Total cloud cover (%) of the report
- Total period of sunshine (mins) of the report
- Wind speed (m/s) of the report

### Exercise 4
Navigate to the `ex_4` directory and inspect the SYNOP message:

```bash
cd ../ex_4
more message.txt
```

!!! question

    What is incorrect about this SYNOP file?

Convert `message.txt` using `station_list.csv`

!!! question

    What problem(s) did you encounter with this conversion?

### Exercise 5
Navigate to the `ex_5` directory and inspect the SYNOP message:

```bash
cd ../ex_5
more message.txt
```

Convert `message.txt` to BUFR format.

!!! question

    What problem(s) did you encounter with this conversion?  
    Considering the error presented, justify the number of BUFR files produced.


## Conclusion

!!! success "Congratulations!"

    In this practical session, you learned:

    - the principles of SYNOP data reporting
    - how to use `synop2bufr` to convert SYNOP data to BUFR format
    - how to use `bufr_dump` to inspect the content of BUFR data

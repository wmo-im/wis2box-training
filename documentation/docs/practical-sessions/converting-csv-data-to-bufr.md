---
title: Converting CSV data to BUFR
---

# Converting CSV data to BUFR

## Introduction

CSV data is a commonly used format for recording tabular data.  `csv2bufr` is a tool to help
convert CSV to BUFR data.

In this session you will learn to create BUFR data from CSV, using custom and flexible
configuration (mappings) in support of meeting WMO GBON requirements.

## Preparation
!!! warning
    Ensure that you are logged into your student VM.
    Ensure you have the exercise-materials downloaded in your home-directory as detailed [previously](accessing-your-student-vm.md#download-the-exercise-materials).

Navigate to the `exercise-materials/csv2bufr-exercises` directory and make sure that the exercises directories are there.

```bash
cd ~/exercise-materials/csv2bufr-exercises
ls
```

!!! tip
    You shuld be able to see the following directories `BUFR_tables answers  ex_1  ex_2  ex_3  ex_4  ex_5 ex_6`


## csv2bufr primer

Below are essential `csv2bufr` commands and configurations:

### mappings Create

The `mappings create` command creates an empty BUFR mapping template JSON file, which maps CSV column headers to their corresponding ecCodes element:

```bash
csv2bufr mappings create <BUFR descriptors> --output <my_template.json>
```

For more information, see the following [example](https://csv2bufr.readthedocs.io/en/latest/example.html#creating-a-new-mapping-file).

### data transform

The `data transform` command converts a CSV file to BUFR format:

```bash
csv2bufr data transform --bufr-template <my_template.json> --output-dir <./my_folder> <my_data.csv>
```

## ecCodes BUFR refresher

### bufr_dump

The `bufr_dump` function will allow you to inspect the BUFR files created from the conversion.  It has numerous options;, the following will be most applicable to the exercises:

```bash
bufr_dump -p <my_bufr.bufr4>
```

This will display the content of your BUFR on screen.  If you are interested in the values taken by a variable in particular, use the `egrep` command:

```bash
bufr_dump -p <my_bufr.bufr4> | egrep -i temperature
```

This will display the variables related to temperature in your BUFR data.  If you want to do this for multiple types of variables, filter the output using a pipe (`|`):

```bash
bufr_dump -p <my_bufr.bufr4> | egrep -i 'temperature|wind'
```

## Inspecting CSV data and BUFR conversion

### Exercise 1: mapping BUFR elements

Navigate to the `ex_1` directory and create a mapping file:

```bash
cd ~/exercise-materials/csv2bufr-exercises/ex_1
```

!!! note

    csv2bufr mappings files have no set file extension, however it recommended to use `.json`.

Using the [ecCodes WMO element table page](https://confluence.ecmwf.int/display/ECC/WMO%3D38+element+table), create a mapping file of the following variables:

- WIGOS Station Identifier (series, issuer, issue number, local identifier)
- Date (Year, month, day)
- Time (Hour, minute)
- Location (Latitude, longitude)
- Barometer height above sea level
- Station level pressure
- Air temperature
- Relative humidity

Use the `csv2bufr` `data transform` command to convert the file `ex_1.csv` to BUFR format.

!!! tip

    See the [csv2bufr primer](#csv2bufr-primer) section.

Use bufr_dump to find the latitude and longitude value stored in the output BUFR file. Verify these values using the CSV file.

!!! tip

    See the [BUFR primer](../converting-synop-data-to-bufr#bufr_dump) section.

### Exercise 2: Mapping BUFR sequences

Navigate to the `ex_2` directory:

```bash
cd ~/exercise-materials/csv2bufr-exercises/ex_2
```

!!! question

    Repeat the previous steps, replacing the following elements with their respective BUFR sequences (which have the form **3XXYYY**):

* WIGOS Station Identifier (series, issuer, issue number, local identifier)
* Date (Year, month, day)
* Time (Hour, minute)
* Location (Latitude, longitude)

The `BUFR_TableD_en.csv` file from the `BUFR_tables` directory contains the defined BUFR sequences as per the official WMO BUFR code tables.

The first few columns of this file are as follows (important columns are in **bold**):

- BUFR category (numeric)
- BUFR category (name)
- **BUFR sequence number**
- **BUFR sequence name**
- BUFR sequence subtitle
- **Included BUFR element number**
- **Included BUFR element name**

A given sequence will appear multiple times, once for each BUFR element it contains.

!!! tip

    Search for the corresponding 6 digit codes found in the previous exercise, and find the corresponding sequence in the 3rd column. For example, the BUFR elements **005002** (Latitude) and **006002** (Longitude) can be replaced with sequence **301023** (Latitude/longitude (coarse accuracy)).

### Exercise 3: Adapting the mapping file to your input CSV data (column names)

Navigate to the `ex_3` directory, and inspect file `ex_3.csv`.

!!! question

    Compare this file to `ex_2.csv`:

```bash
cd ~/exercise-materials/csv2bufr-exercises/ex_3
more ex_3.csv
more ../ex_2/ex_2.csv
```

You should notice that the data is the same, however the column names are different.

!!! question

    With this in mind, create a mapping template file for the `ex_3.csv` file. 
    
Open the mapping file generated:

```bash
nano <my_mapping.json>
```

!!! question

    Change the `"value"` items to correctly correspond to each column in `ex_3.csv`.

!!! tip

    In the first column, `"eccodes_key": "#1#wigosIdentifierSeries"` should now be paired with `"value": "data:wigos_identifier_series"`.

!!! question
    Use the csv2bufr `data transform` function to convert `ex_3.csv` to BUFR format.

!!! question
    Check that the data stored in the output BUFR is the same as that in the CSV that is was converted from.

### Exercise 4: Adapting the mapping file to your input CSV data (units)
Navigate to the `ex_4` directory and edit the file `ex_4.csv`:

```bash
cd ~/exercise-materials/csv2bufr-exercises/ex_4
vi ex_4.csv
```

This file contains the same data and column names as `ex_2.csv`, but uses different units:

- `heightOfBarometerAboveMeanSeaLevel` is given in **cm**
- `nonCoordinatePressure` is given in **hPA**
- `airTemperature` is given in **&deg;C**

!!! question

    Using the [ecCodes WMO element table page](https://confluence.ecmwf.int/display/ECC/WMO%3D38+element+table), find the correct units for these three variables.

!!! question

    Find the scale (*x*, for a multiplication by *10<sup>x</sup>*) and offset (addition of a constant *c*) required for each of these conversions.

!!! tip

    As 1cm = 1m x 10<sup>-2</sup>, the first conversion requires a scale of *x=-2* and an offset of *c=0*.

Open the mapping file `mapping_4.json`:

```bash
nano mapping_4.json
```

!!! tip
    To edit the mapping_4.json file you can use nano, vi, vim or emacs.

This is the same mapping file as you generated and modified a couple of exercises ago.  Using your answers in the previous question, convert the units using the `scale` and `offset` keys.

!!! question

    Convert the file `ex_4.csv` to BUFR format.

### Exercise 5: Create mappings for hourly synop with WIGOS Station Identifier
Navigate to the `ex_5` directory:

```bash
cd ~/exercise-materials/csv2bufr-exercises/ex_5
```

Here, you are free to either work with your own synoptic CSV data, or use the file `ex_5_hourly.csv`.

!!! question

    Noting that a SYNOP report cannot contain the WIGOS station identifier, creating a mappings template which contains the mappings for both the WIGOS station identifier and the hourly synoptic data.

!!! question

    Just like previous exercises, edit element names in the mapping file according to the CSV data.

!!! note

    Make sure that `number_header_rows` and `column_names_row` are correct.

Convert the CSV data data to BUFR format.

### Exercise 6
Navigate to the `ex_6` directory and edit the file `ex_6.csv`:

```bash
cd ~/exercise-materials/csv2bufr-exercises/ex_6
vi ex_6.csv
```

!!! question

    Notice that this time the `relative_humidity` column contains an incorrect value.  Why is this value incorrect?

!!! tip

    Think of valid minimum and maximum values for relative humidity.

!!! question

    By adjusting the `valid_min` and `valid_max` keys of the `relativeHumidity` element in the mapping file `mapping_6.json`, enforce a quality control measure which prevents this value from being written to BUFR.

!!! question

    Add more valid minimum and maximum values to the mappings file according to your own preference.

!!! note

    The minimum and maximum values must have the **same units** as your **original** input data, not the converted values discussed in the previous exercise.

!!! question

    Convert the file `ex_6.csv` to BUFR format, and use `bufr_dump` to verify that this variable has no value in the resulting BUFR.

## Conclusion

!!! success "Congratulations!"

    In this practical session, you learned:

    - the basic usage of `csv2bufr`
    - how to create and update a simple csv2bufr mapping file for a variety of scenarios, including for GBON requirements, unit conversion, and quality control/range checking
    - how to `csv2bufr` on a test data file and convert to BUFR format
    - how to lookup the BUFR element number for a parameter to be encoded
    - how to encode BUFR data for the example input data and inspect the resulting output data
    - about the sequence for hourly climate data
    - about the BUFR Manual on Codes requirements on the units of variables, e.g. Celsius -> Kelvin.

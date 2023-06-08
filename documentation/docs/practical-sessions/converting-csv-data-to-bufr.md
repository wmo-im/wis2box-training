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

Navigate to the `exercise-materials/csv2bufr-exercises` directory and make sure that the exercises directories are there.

```bash
cd ~/exercise-materials/csv2bufr-exercises
ls
```

!!! tip
    You should be able to see the following directories `answers  ex_1  ex_2  ex_3  ex_4  ex_5`


## csv2bufr primer

### Necessary CSV data

There are some requirements on the data that must be present in the CSV file:

- WIGOS Station Identifier, either in 1 column or split over 4 columns for each component as follows:
- Observation year
- Observation month
- Observation day
- Observation hour
- Observation minute
- Latitude
- Longitude
- Station height
- Barometer height

!!! note
    Notice that the datetime of the observation is split into 5 different columns (from most to least significant).

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
csv2bufr data transform --bufr-template <my_template.json> --output-dir <./my_directory> <my_data.csv>
```

!!! note
    The output directory is not required, and by default is the current working directory.


## ecCodes BUFR refresher

### bufr_dump

The `bufr_dump` function will allow you to inspect the BUFR files created from the conversion. It has numerous options, the following will be most applicable to the exercises:

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

### Exercise 1: Converting a CSV file to BUFR
In this exercise we will look at a pre-configured mapping file for the CSV data, and will use this to convert the data to BUFR.

Navigate to the `ex_1` directory:

```bash
cd ~/exercise-materials/csv2bufr-exercises/ex_1
```

and open the CSV data `ex_1.csv`.

1. How many header rows are there in this data?
2. Which row contains the column names?

Now open the mappings file `mappings_1.json`.

!!! note

    csv2bufr mappings files have no set file extension, however it recommended to use `.json`.

3. Verify that `"number_header_rows"` and `"column_names_row"` are the same as your answers above.

4. Locate each of the CSV column names in this mappings file.

5. By the `data transform` command, use the mappings file to convert this CSV data to BUFR.

6. Use bufr_dump to find the latitude and longitude value stored in the output BUFR file. Verify these values using the CSV file.

### Exercise 2: Correcting the datetime format
In this exercise we will investigate the correct format to present the datetime of an observation in the CSV file.

Navigate to the `ex_2` directory:

```bash
cd ~/exercise-materials/csv2bufr-exercises/ex_2
```

and open the CSV data `ex_2.csv`.

1. What are the differences in the way that the datetime is represented in this CSV file compared to the previous one?

Now open the mappings file `mappings_2.json`. By looking at the eccodes keys related to dates and times, it should seem clear that it is not possible to map the datetime with the CSV in its current state.

2. Create new columns in the CSV file for each component of the datetime: `Year`, `Month`, `Day`, `Hour`, `Minute`.

3. By the `data transform` command, use the mappings file to convert this CSV data to BUFR.

### Exercise 3: Handling changes to the CSV data
In this exercise we consider the following scenario: given the same CSV data but with different column names, how can we adjust the mappings file to convert this data to BUFR? For simplicity, we will only look at one column name change.

Navigate to the `ex_3` directory

```bash
cd ~/exercise-materials/csv2bufr-exercises/ex_3
```

1. By the `data transform` command, attempt to convert the CSV data to BUFR. What error appears?

Open the CSV data `ex_3.csv`.

2. What column name has been changed?

Open the mappings file `mappings_3.json`.

3. Find the original column name in this mapping file, and change it to the new name.
4. By the `data transform` command, use the mappings file to convert this CSV data to BUFR.
5. Use `bufr_dump` to verify that `relativeHumidity` has the same value as the CSV data.

### Exercise 4: Unit conversion
In this exercise, we expand on the work above by not only handling changes to column names, but also the units of the data. We achieve this by using `offset` and `scale` in the mappings file.

Navigate to the `ex_4` directory:

```bash
cd ~/exercise-materials/csv2bufr-exercises/ex_4
```

and open the CSV data `ex_4.csv`.

1. Which row are the units of the variables written?

You should notice that `BP` now has units hPa instead of Pa. Moreover, the air temperature and dewpoint temperature now have column names `AirTempC` and `DewPointTempC`, with units C instead of K.

2. What power of 10 is needed to convert hPa to Pa?
3. What constant must be added to convert degrees C to K?

Open the mappings file `mappings_4.json`. Find the lines corresponding to the variables above.

4. Convert `BP` to Pa by adding the following line to the right of `"data:BP"`:

    ```bash
    "offset": "const:0", "scale": "const:x"
    ```

    where `x` is your answer in part 3.

5. Change the column names of air temperature and dewpoint temperature in the mappings file to match that of the CSV file, as you did in the previous exercise.

6. Convert `AirTempC` to K by adding the following line to the right of `"data:AirTempC"`:

    ```bash
    "offset": "const:y", "scale": "const:0"
    ```

    where `y` is your answer in part 4.

7. Convert `DewPointTempC` to K by adding the following line to the right of `"data:DewPointTempC"`:

    ```bash
    "offset": "const:y", "scale": "const:0"
    ```

    where `y` is your answer in part 4.

8. By running the `csv2bufr data transform` command, use the mappings file to convert this CSV data to BUFR.

9. Use the `bufr_dump` command to verify that `nonCoordinatePressure`, `airTemperature` and `dewpointTemperature` have the values you would expect after conversion.

### Exercise 5: Implementing quality control
In this exercise, we will implement some minimum and maximum tolerable values to prevent data of certain variables from being encoded into BUFR. To do this, we will use `valid_min` and `valid_max` in the mappings file.

Navigate to the `ex_5` directory:

```bash
cd ~/exercise-materials/csv2bufr-exercises/ex_5
```

1. By running the `csv2bufr data transform` command, use the mappings file to convert this CSV data to BUFR. What error occurs? Is a BUFR file created?

2. Use the `bufr_dump` command to check the values of `pressureReducedToMeanSeaLevel`, `airTemperature` and `dewpointTemperature`. Which variables are missing, and why?

Open the mappings file `mappings_5.json`. Find the lines corresponding to the variables above. You will find the following on these lines:

```bash
"valid_min": "const:a", "valid_max": "const:b"
```

where `a` and `b` are values. These values represent the minimum and maximum tolerable extremes for encoding into BUFR. 

3. Change `a` and `b` on each line to form a less tight range of tolerance for these variables.

    !!! note
    The valid minimum and maximum values should take the same units as the CSV data.

4. By running the `csv2bufr data transform` command, use this mappings file to convert this CSV data to BUFR again. Do you notice any errors this time?

## Conclusion

!!! success "Congratulations!"

    In this practical session, you learned:

    - The basic usage of `csv2bufr`
    - The required structure of CSV data for conversion to BUFR
    - How to update a simple csv2bufr mapping file for a variety of scenarios, including for GBON requirements, unit conversion, and quality control/range checking
    - How to use `csv2bufr` on a test data file and convert to BUFR format
    - How to use `bufr_dump` to verify the values of BUFR encoded variables

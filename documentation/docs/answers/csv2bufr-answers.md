---
title: Converting CSV data to BUFR answers
---

# Converting CSV data to BUFR answers

## Exercise 1

1. There are 4 header rows.
2. Row 2 contains the column names.
3. Found by checking the lines 6 and 7 in the mapping file.
4. These are found in the `data:` lines of the mapping file.
5. The CSV data is converted to BUFR using the following command:
    ```bash
    csv2bufr data transform ex_1.csv --bufr-template mappings_1.json
    ```
6. The latitude and longitude can be verified using the following command:
    ```bash
    bufr_dump -p WIGOS_0-454-2-AWSMULANJE_20230526T005500.bufr4 | egrep -i 'latitude|longitude'
    ```

## Exercise 2

1. In the previous CSV file, the datetime was split into six columns representing the year, month, day, hour, minute, and second of the observation. In this CSV file, the datetime is stored in a single column.

2. This is done by recreating the six columns of the previous CSV file, and deleting the new datetime column.

3. The CSV data is written to BUFR using:
    ```bash
    csv2bufr data transform ex_2.csv --bufr-template mappings_2.json
    ```

## Exercise 3

1. When running:
    ```bash
    csv2bufr data transform ex_3.csv --bufr-template mappings_3.json
    ```

    You should see the following error:

    ```bash
    Column RH not found in input data
    ```

    followed by the input data dictionary.

2. The relative humidity column now has name `RelativeHumidity` instead of `RH`.

3. We do this by changing the line:

    ```bash
    {"eccodes_key": "#1#relativeHumidity", "value":"data:RH"}
    ```

    to:

    ```bash
    {"eccodes_key": "#1#relativeHumidity", "value":"data:RelativeHumidity"}
    ```

4. The CSV data is written to BUFR by re-using:

    ```bash
    csv2bufr data transform ex_3.csv --bufr-template mappings_3.json
    ```

5. The relative humidity can be verified using:

    ```bash
    bufr_dump -p WIGOS_0-454-2-AWSMULANJE_20230526T005500.bufr4 | egrep -i relativeHumidity
    ```

    which should give a value of `54`.

    !!! note
        The value returned is not the same exact value as what is present in the CSV file: 54.09.
        This is because some variables (such as relative humidity) in BUFR are always integers, hence are rounded.


## Exercise 4

1. The units are found in row 3.
2. 2, as 1hPa = 100Pa.
3. 273.15, as 0 degrees C = 273.15 K
4. You should have the following line in your mapppings file:

    ```bash
    {"eccodes_key": "#1#nonCoordinatePressure", "value":"data:BP", "offset": "const:0", "scale": "const:2"}
    ```

5. You should have the following line in your mappings file:

    ```bash
    {"eccodes_key": "#1#airTemperature", "value":"data:AirTempC"}
    {"eccodes_key": "#1#dewpointTemperature", "value":"data:DewPointTempC"}
    ```

6. ```bash
    {"eccodes_key": "#1#airTemperature", "value":"data:AirTempC", "offset": "const:273.15", "scale": "const:0"}
    ```

7. ```bash
    {"eccodes_key": "#1#dewpointTemperature", "value":"data:DewPointTempC", "offset": "const:273.15", "scale": "const:0"}
    ```

8. The CSV data is written to BUFR by re-using:

    ```bash
    csv2bufr data transform ex_4.csv --bufr-template mappings_4.json
    ```

9. The converted variables can be verified using:

    ```bash
    bufr_dump -p WIGOS_0-454-2-AWSMULANJE_20230526T005500.bufr4 | egrep -i 'nonCoordinatePressure|airTemperature|dewpointTemperature'
    ```

## Exercise 5

1. When converting `ex_5.csv` to BUFR, we come across the following error:

    ```bash
    #1#pressureReducedToMeanSeaLevel: Value (102043.2) out of valid range (50000 - 100000).; Element set to missing
    #1#airTemperature: Value (25.85) out of valid range (-10 - 25).; Element set to missing
    ```

2. By using the following command:

    ```bash
    bufr_dump -p WIGOS_0-454-2-AWSMULANJE_20230526T005500.bufr4 | egrep -i 'pressureReducedToMeanSeaLevel|airTemperature|dewpointTemperature'
    ```

    which gives output:

    ```bash
    pressureReducedToMeanSeaLevel=MISSING
    airTemperature=MISSING
    dewpointTemperature=289.1
    ```

    We find that the pressure and air temperature variables are missing because, from the error found in part 1, these variables are outside of the valid range.

3. This is personal preference.

4. Provided the values of `QNH`, `AirTempC`, and `DewPointTempC` are within the ranges set in the previous part, the CSV file should convert to BUFR without any errors.


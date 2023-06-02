---
title: Converting CSV data to BUFR answers
---

# Converting CSV data to BUFR answers

## Exercise 1

1. There are 4 header rows.
2. Row 2 contains the column names.
3. Found by checking the lines 6 and 7 in the mapping file.
4. These are found in the `"data:` lines of the mapping file.
5. The CSV data is written to BUFR using:
    ```bash
    csv2bufr data transform ex_1.csv --bufr-template mappings_1.json
    ```
6. The latitude and longitude can be verified using:
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

    You should see the error:

    ```bash
    Column RH not found in input data
    ```

    followed by the input data dictionary.

2. The relative humidity column now has name `RelativeHumidity` instead of `RH`.

3. We do this by changing line:

    ```bash
    {"eccodes_key": "#1#relativeHumidity", "value":"data:RH"}
    ```

    to line:

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
        This is because this particular ecCode is always an integer, so is rounded.


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

1. Non coordinate pressure (QNH) takes a negative value and the air temperature is too high.

2. This will vary from person to person, but here is an example:

    | Variable        | Minimum | Maximum |
    |-----------------|---------|---------|
    | Pressure (Pa)   | 0       | 150000  |
    | Temperature (C) | -20     | 50      |

3. You should have the following line in your mappings file:

    ```bash
    {"eccodes_key": "#1#pressureReducedToMeanSeaLevel", "value":"data:QNH", "valid_min": "const:0", "valid_max": "const:150000"}
    ```

    ```bash
    {"eccodes_key": "#1#airTemperature", "value":"data:AirTempC", "valid_min": "const:-20", "valid_max": "const:50", "offset": "const:273.15", "scale": "const:0"},
    {"eccodes_key": "#1#dewpointTemperature", "value":"data:DewPointTempC", "valid_min": "const:-20", "valid_max": "const:50", "offset": "const:273.15", "scale": "const:0"}
    ```

    !!! note
    The valid minimum and maximum values should take the same units as the CSV data.

4. You will see the following error:

    ```bash
    ECCODES ERROR   :  encode_double_value: pressureReducedToMeanSeaLevel (010051). Value (-102043) out of range (minAllowed=0, maxAllowed=163830).
    ECCODES ERROR   :  Cannot encode pressureReducedToMeanSeaLevel=-102043 (subset=1)
    error calling codes_set(49887440, 'pack', True): Value out of coding range
    ```

    and no BUFR file is written. This is because the pressure reduced to sea level variable is out of the range of minimum and maximum valid values.

    !!! note
    There will be no error for the air temperature being out of range. This is because once one value out of range error occurs, the csv2bufr process is halted.
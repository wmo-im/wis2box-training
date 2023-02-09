# Instructions
1. Read the docs:
   - <a href="https://csv2bufr.readthedocs.io/en/latest/quickstart.html" target="_blank">csv2bufr quickstart</a>
   - <a href="https://csv2bufr.readthedocs.io/en/latest/example.html" target="_blank">csv2bufr example</a>
1. Using the information available from the <a href="https://confluence.ecmwf.int/display/ECC/WMO%3D38+element+table" target="_blank">ECMWF eccodes website</a>
create a mapping file with the csv2bufr command line tool for the data shown below (Table 1). The following elements should be included:

- WIGOS station identifier (series, issuer, issue number, local identifier)
- Date (Year, month, day)
- Time (Hour, minute)
- Location (Latitude, longitude)
- Barometer height above sea level
- Station level pressure
- Air temperature
- Relative humidity

NOTE:     The BUFR tables can also be found locally at the following path:

        ${ECCODES_DIR}/share/eccodes/definitions/bufr/tables/0/wmo/39//element.table

3. Instructions on the ``csv2bufr`` template creation tool can be found at: <a href="https://csv2bufr.readthedocs.io/en/latest/example.html#creating-a-new-mapping-file" target="_blank">csv2bufr mappings create ...</a>
4. Edit the mapping file to remove the unused elements (where "value": "")
3. Verify the mapping file by running ``csv2bufr`` on the example data file ``example1.csv``
1. Examine the contents of the output BUFR file using the ``bufr_dump`` tool from eccodes.

_Table 1. Example data to encode to BUFR_ 

| parameter/variable                     | value    |
|----------------------------------------|----------|
| wigosIdentifierSeries                  | 0        |
| wigosIssuerOfIdentifier                | 20000    |
| wigosIssueNumber                       | 0        |
| wigosLocalIdentifierCharacter          | MYWSI001 | 
| year (UTC)                             | 2023     |
| month (UTC)                            | 02       |
| day (UTC)                              | 03       |
| hour (UTC)                             | 12       |
| minute (UTC)                           | 02       |
| latitude (coarse, 2decimal places)     | 47.59    |
| longitude (coarse, 2dp)                | 10.54    |
| heightOfBarometerAboveMeanSeaLevel (m) | 15       | 
| nonCoordinatePressure (Pa)             | 102310   |
| airTemperature (K, 2dp)                | 281.35   |
| relativeHumidity (%, 1dp)              | 45.2     |

This data is included in the ``./data/exercise-1.csv`` file.

# Expected results
- JSON file containing the mappings for the above parameters from the file ``exercise-1.csv``.
- BUFR output file containng the encoded data.

# Learning outcomes
- Understand the basic usage of CSV2BUR
  - generate simple BUFR mapping file
  - run csv2bufr on a test data file and convert to BUFR
- Ability to lookup up the BUFR element number for a parameter to be encoded
- Create a basic BUFR mapping file
- Encode BUFR data for the example input data and inspect the data
 
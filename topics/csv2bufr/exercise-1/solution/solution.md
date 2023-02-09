# Solution and expected output

- Use the following command to generate the json file

``
csv2bufr mappings create 001125 001126 001127 001128 004001 004002 004003 004004 004005 005002 006002 007031 010004 012101 013009 --output example1.json
``

The 6 digit numbers correspond to the following (identified by either the local BUFR tables or by looking up on the ECMWF website).

| parameter/variable                       | 6 digit code (FXXYYY) |
|------------------------------------------|-----------------------|
| wigosIdentifierSeries                    | 001125                |
| wigosIssuerOfIdentifier                  | 001126                |
| wigosIssueNumber                         | 001127                |
| wigosLocalIdentifierCharacter            | 001128                | 
| year (UTC)                               | 004001                |
| month (UTC)                              | 004002                |
| day (UTC)                                | 004003                |
| hour (UTC)                               | 004004                |
| minute (UTC)                             | 004005                |
| latitude (coarse, 2dp)                   | 005002                |
| longitude (coarse, 2dp)                  | 006002                |
| heightOfBarometerAboveMeanSeaLevel (m)   | 007031                | 
| nonCoordinatePressure (Pa)               | 010004                |
| airTemperature (K, 2dp)                  | 012101                |
| relativeHumidity (%, 1dp)                | 013009                |

- Run the following to convert to BUFR.

``
csv2bufr data transform --bufr-template example1.json --output-dir . example1.csv
``

This should create the following file: ``WIGOS_0-20000-0-MYWSI001_20230203T120200.bufr4``

- Use the ``bufr_compare`` tool to verify the result:

``
bufr_compare WIGOS_0-20000-0-MYWSI001_20230203T120200.bufr4 ./solution/output/sample.bufr4
``

No differences should be listed.
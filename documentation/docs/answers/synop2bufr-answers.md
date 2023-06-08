---
title: Converting SYNOP data to BUFR answers
---

# Converting SYNOP data to BUFR answers

## Exercise 1

1. There is 1 SYNOP report, as there is only 1 delimiter (=)
1. There is 1 station
1. This is done using the `transform` command, for example:

    ```bash
    synop2bufr transform --metadata station_list.csv --output-dir . message.txt
    ```

1. This can be done using the following command:

    ```bash
    bufr_dump -p <file.bufr4> | egrep -i 'latitude|longitude'
    ```

## Exercise 2

1. There are 3 SYNOP reports, as there are 3 delimiters (=)
1. There are 3 stations
1. This is done using the `transform` command, for example:

    ```bash
    synop2bufr transform --metadata station_list.csv --output-dir . message.txt
    ```

1. The number of BUFR files output is determined by the number of valid SYNOP reports in the text file, provided the station TSI of each report can be found in the station list file with a corresponding WSI
1. This can be done using the following commands:

    ```bash
    bufr_dump -p <file.bufr4> | egrep -i 'wigos'
    ```

    ```bash
    bufr_dump -p <file.bufr4> | egrep -i 'wigos'
    ```

    ```bash
    bufr_dump -p <file.bufr4> | egrep -i 'wigos'
    ```

    Note that if you have a directory with just these 3 BUFR files, you can use Linux wildcards as follows:

    ```bash
    bufr_dump -p *.bufr4 | egrep -i 'wigos'
    ```

## Exercise 3

1. No, this is not a problem provided that there exists a row in the station list file with a station TSI matching that of the SYNOP report we are trying to convert
1. This is done using the `transform` command, for example:

    ```bash
    synop2bufr transform --metadata station_list.csv --output-dir . message.txt
    ```

1. This can be done in one command:

    ```bash
    bufr_dump -p <file.bufr4> | egrep -i 'temperature|cover|sunshine|wind'
    ```

Of course a command for each variable can also be used.

## Exercise 4

1. The SYNOP reports are missing the delimiter (`=`) that allows `synop2bufr` to distinguish one report from another
1. Attempting to convert should raise the following error: `ERROR:synop2bufr:Delimiters (=) are not present in the string, thus unable to identify separate SYNOP reports.`

## Exercise 5

1. One of the station TSIs (`15015`) has no corresponding metadata in the file, which will prohibit synop2bufr from accessing additional necessary metadata to convert the first SYNOP report to BUFR
1. The error is: `ERROR:synop2bufr:Missing WSI for station 15015`
1. There are 3 SYNOP reports but only 2 BUFR files have been produced. This is because one of the SYNOP reports lacked the necessary metadata as mentioned above

---
title: "WIS2 Training Day 3"
date: "22/02/2023"
...

# Answers

## Ex. 1

1. There is 1 SYNOP report, as there is only 1 delimiter (=).
1. There is 1 station.
1. This is done using the `transform` command, for example:

    ```console
    synop2bufr transform --metadata station_list.csv --output-dir . message.txt
    ```

1. This can be done using the following command:

    ```console
    bufr_dump -p WIGOS_0-20000-0-15015_20230221T120000.bufr4 |grep -i 'latitude\|longitude'
    ```

## Ex. 2

1. There are 3 SYNOP reports, as there are 3 delimiters (=).
1. There are 3 stations.
1. This is done using the `transform` command, for example:

    ```console
    synop2bufr transform --metadata station_list.csv --output-dir . message.txt
    ```

1. The number of BUFR files output is determined by the number of valid SYNOP reports in the text file, provided the station TSI of each report can be found in the station list file with a corresponding WSI.
1. This can be done using the following commands:

    ```console
    bufr_dump -p WIGOS_0-20000-0-15015_20230221T120000.bufr4 |grep -i 'wigos'
    ```

    ```console
    bufr_dump -p WIGOS_0-20000-0-15020_20230221T120000.bufr4 |grep -i 'wigos'
    ```

    ```console
    bufr_dump -p WIGOS_0-20000-0-15090_20230221T120000.bufr4 |grep -i 'wigos'
    ```

    Note that if you have a folder with just these 3 BUFR files, you can use the **shorter command**:

    ```console
    bufr_dump -p *.bufr4 |grep -i 'wigos'
    ```

## Ex. 3

1. No, this is not a problem provided that there exists a row in the station list file with a station TSI matching that of the SYNOP report we're trying to convert.
1. This is done using the `transform` command, for example:

    ```console
    synop2bufr transform --metadata station_list.csv --output-dir . message.txt
    ```

1. This can be done in one command:

    ```console
    bufr_dump -p WIGOS_0-20000-0-15260_20230221T115500.bufr4 |grep -i 'temperature\|cover\|sunshine\|wind'
    ```

Of course a command for each variable can be used too.

## Ex. 4

1. The SYNOP reports are missing the delimiter (=) that allows SYNOP2BUFR to distinguish one report from another.
1. Attempting to convert should raise error: `ERROR:synop2bufr:Delimiters (=) are not present in the string, thus unable to identify separate SYNOP reports.`

## Ex. 5

1. One of the station TSIs (`15015`) has no corresponding metadata in the file, which will prohibit SYNOP2BUFR from accessing additional necessary metadata to convert the first SYNOP report to BUFR.
1. The error is: `ERROR:synop2bufr:Missing WSI for station 15015`.
1. There are 3 SYNOP reports but only 2 BUFR files have been produced. This is because one of the SYNOP reports lacked the necessary metadata as mentioned above.

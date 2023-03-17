---
title: Converting DAYCLI data to BUFR
---

# Converting DAYCLI data to BUFR

## Introduction

Daily climate reports (DAYCLI) are a requirement for daily climate observations to monitor extremes, such as daily maximum and minimum temperature, daily total precipitation, and more. 

This session will focus on understanding the structure of a typical DAYCLI CSV file, converting it to BUFR format, and inspecting the resulting contents.

If this data is recorded in CSV format, we can use [csv2bufr](https://github.com/wmo-im/csv2bufr) to convert this data to BUFR.  Moreover, if the structure of the CSV file is correct, then one does **not need to configure** a mappings file for the conversion to BUFR, as a DAYCLI mapping template comes included with csv2bufr to manage such data.

## Preparation
!!! warning
    Ensure that you are logged into your student VM.
    Ensure you have the exercise-materials downloaded in your home-directory as detailed [previously](accessing-your-student-vm.md#download-the-exercise-materials).

Navigate to the `exercise-materials/daycli-exercises` directory.

```bash
cd ~/exercise-materials/daycli-exercises
```

## Exercise

Edit the file `daycli.csv`.  Compare the column structure to that of the final slides of the presentation we just viewed.

Convert this CSV file to BUFR using the built-in daycli mapping file:

```bash
csv2bufr data transform --bufr-template daycli --output-dir ./ daycli.csv
```

Inspect the output BUFR files using `bufr_dump` and verify the data is the same as the original DAYCLI CSV file.

## Conclusion

!!! success "Congratulations!"

    In this practical session, you learned how to:

    - verify the structure of a typical DAYCLI CSV file
    - convert this DAYCLI CSV file into BUFR using csv2bufr and the built-in daycli mapping template
    - inspect the contents of the DAYCLI BUFR files created

---
title: DAYCLI Template
---

# csv2bufr template for daily climate data (DAYCLI)

The **DAYCLI** template provides a standardized CSV format for converting daily climate data to BUFR sequence 307075.

The format is intended for use with Climate Data Management Systems to publish data on WIS2, in support of reporting requirements for daily climate observations.

This templates maps daily observations of:

 - Minimum, maximum and average temperature over 24 hours period
 - Total accumulated precipitation over 24 hours period
 - Total snow depth at time of observation
 - Depth of fresh snow over 24 hours period

This template requires additional metadata with respect to the simplified AWS-template: method of calculating average temperature; sensor and station heights; exposure and measurement quality classification.

!!! Note "About the DAYCLI template"
    Please note that the DAYCLI BUFR sequence will be updated during 2025 to include additional information and revised QC flags. The DAYCLI template included the wis2box will be updated to reflect these changes. WMO will communicate when the wis2box-software is updated to include the new DAYCLI template, to allow users to update their systems accordingly.

## CSV columns and description

{{ read_csv("docs/assets/tables/daycli-table.csv") }}

## Averaging method

{{ read_csv("docs/assets/tables/averaging-method-table.csv") }}

## Quality flag

{{ read_csv("docs/assets/tables/quality_flag.csv") }}

## References for siting classification

[Reference for "temperature_siting_classification"](https://library.wmo.int/idviewer/35625/839).

[Reference for "precipitation_siting_classification"](https://library.wmo.int/idviewer/35625/840).

## Example

Example CSV file that conforms to the DAYCLI template: [daycli-example.csv](../../sample-data/daycli-example.csv).

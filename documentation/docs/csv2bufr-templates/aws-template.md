---
title: AWS Template
---

# csv2bufr template for Automated Weather Stations reporting hourly GBON data

The **AWS Template** uses a standardized CSV format to ingest data from Automatic Weather Stations in support of GBON reporting requirements. This mapping template converts CSV data to BUFR sequence 301150, 307096.

The format is intended for use with automatic weather stations reporting a minimum number of parameters, including pressure, air temperature and humidity, wind speed and direction and precipitation on an hourly basis.

## CSV columns and description

{{ read_csv("docs/assets/tables/aws-minimal.csv") }}

## Example

Example CSV file that conforms to the AWS template: [aws-example.csv](/sample-data/aws-example.csv).

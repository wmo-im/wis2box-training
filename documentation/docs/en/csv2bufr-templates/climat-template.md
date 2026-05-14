---
title: CLIMAT Template
---

# csv2bufr template for daily climate data (CLIMAT)

**CLIMAT** messages report monthly climate summaries compiled from daily observations at synoptic and climatological stations, to support climate monitoring, research, and archiving.

The CLIMAT template provides a standardized CSV format to produce CLIMAT messages encoded in BUFR format for sequence 301150,307073.

## CSV columns and description

{{ read_csv("docs/assets/tables/climat-table.csv") }}

## Example

Example CSV file that conforms to the CLIMAT template: [climat-example.csv](../../sample-data/climat-example.csv).
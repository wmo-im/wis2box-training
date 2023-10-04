---
title: Configuring data mappings
---

# Configuring data mappings

!!! abstract "Learning outcomes"
    By the end of this this practical session, you will be able to:

    - inspect the live wis2box data mappings
    - add a new data mapping
    - update the `country` and `centre_id` values add a new data mapping
    - update the `file-pattern` value to match your data filename convention

## Introduction

wis2box uses a number of configuration files to allow for a simple setup of the system.  At the heart of wis2box
is data ingest and publishing, which are driven by wis2box data mappings.  The basic concept of data mappings
is configuring a WIS2 topic to a defined ingest and publish workflow and files/templates.  In this session, you
will work on adding to the data mappings in support of publishing your data via wis2box.

## Preparation

Login to your student VM

### Add CSV data

Here's how to add data mapping for wis2box to process CSV data.  Inspect the contents of the sample SYNOP CSV data mapping:

```bash
cat ~/wis2box-1.0b5/synop-csv-mappings.yml
```

!!! question
    What topic is defined in this mapping?  What values of the topic are placeholders to be updated later in this session?

Copy and paste the above file contents into your file `~/wis2box-data/data-mappings.yml`

Update the `[country]` and `[centre_id]` values in your new/added data mapping.  Use your username as the `centre_id` topic.

!!! tip
    The `country` value should match one of the countries in the [country list of the WIS2 Topic Hierarchy](https://github.com/wmo-im/wis2-topic-hierarchy/blob/main/topic-hierarchy/country.csv).

!!! note
    Centre ids will be officially managed and introduced as part of the WIS2 Topic Hierarchy throughout the WIS2 Pilot Phase, at which point each centre's id will be in the [centre_id list of the WIS2 Topic Hierarchy](https://github.com/wmo-im/wis2-topic-hierarchy/blob/main/topic-hierarchy/centre-id.csv).  `centre_id` values should be lower case and contain no accents or special characters. Dashes should be used instead of underscores.

!!! note
    The `file-pattern` values throughout the data mapping provide a [regular expression](https://www.regular-expressions.info) to be able to match filenames.  Ensure your filenames are formatted as per the regular expression in the new data mapping, to include `WIGOS_` as a fixed value, followed by the WIGOS Station Identifier (WSI), followed by an underscore (`_`), as well as any other information (i.e. datestamp).  Ensure the file extension is `.csv`.  A real world example would be `WIGOS_0-454-2-AWSBALAKA_2021-11-18T0955.csv`.


!!! tip

    Remember your dataset topic for the [WIS2 discovery metadata](configuring-wis2-discovery-metadata.md) exercise.

## Restart wis2box

In order for data mappings to take effect, restart wis2box as follows:

```bash
python3 wis2box-ctl.py restart
``` 

## Conclusion

!!! success "Congratulations!"
    In this practical session, you learned how to:

    - inspect the live wis2box data mappings
    - add a new data mapping
    - update the `country` and `centre_id` values add a new data mapping
    - update the `file-pattern` value to match your data filename convention


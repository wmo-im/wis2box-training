---
title: Configuring data mappings
---

# Introduction

wis2box uses a number of configuration files to allow for a simple setup of the system.  At the heart of wis2box
is data ingest and publishing, which are driven by wis2box data mappings.  The basic concept of data mappings
is configuring a WIS2 topic to a defined ingest and publish workflow and files/templates.  In this session, you
will work on adding to the data mappings in support of publishing your data via wis2box.

## Preparation

!!! note
    Ensure you are logged into the **wis2box-management** container on your student VM: 

    ```bash
    cd ~/exercise-materials/wis2box-setup
    python3 wis2box-ctl.py login
    ```

## Configure a data mapping

!!! note
    Ensure you are logged into the **wis2box-management** container before continuing.

Inspect the wis2box environment to locate the data mappings in use by the system, as defined by the `WIS2BOX_DATA_MAPPINGS` environment variable:

```bash
wis2box environment show | grep WIS2BOX_DATA_MAPPINGS
```

!!! question
    Where are the live data mappings located?

!!! question
    How can using the `$WIS2BOX_DATA_MAPPINGS` environment variable be valuable, as compared to `/data/wis2box/data-mappings.yml`?

### Add CSV data

Let's add a data mapping for wis2box to process CSV data.  Inspect the contents of the sample SYNOP CSV data mapping:

```bash
cat ~/exercise-materials/wis2box-setup/synop-csv-mappings.yml
```

!!! question
    What topic is defined in this mapping?  What values of the topic are placeholders to be updated later in this session?

Copy and paste the above file contents into the `$WIS2BOX_DATA_MAPPINGS` file (either manually or via the command below)::

```bash
tail -n +2 exercise-materials/wis2box-setup/test-data/data-mappings.yml >> $WIS2BOX_DATA_MAPPINGS
```

!!! tip
    Be sure that the first `data:` line from the above file is omitted when copying/pasting into the `$WIS2BOX_DATA_MAPPINGS` file.

Open the data mappings file:

```bash
vi $WIS2BOX_DATA_MAPPINGS
```

Verify that the file you copied from `~/exercise-materials/wis2box-setup/synop-csv-mappings.yml` is now part of the live data mappings file.

Update the `[country]` and `[centre_id]` values in your new/added data mapping.

!!! tip
    The `country` value should match one of the countries in the [country list of the WIS2 Topic Hierarchy](https://github.com/wmo-im/wis2-topic-hierarchy/blob/main/topic-hierarchy/country.csv).

!!! tip
    The `centre_id` value should match one of the countries in the [country list of the WIS2 Topic Hierarchy](https://github.com/wmo-im/wis2-topic-hierarchy/blob/main/topic-hierarchy/country.csv) and `centre_id` values should be lower case and contain no accents or special characters. Dashes should be used instead of underscores.

!!! note
    The `file-pattern` values throughout the data mapping provide a [regular expression](https://www.regular-expressions.info) to be able to match filenames.  Ensure your filenames are formatted as per the regular expression in the new data mapping, to include `WIGOS_` as a fixed value, followed by the WIGOS Station Identifier (WSI), followed by an underscore (`_`), as well as any other information (i.e. datestamp).  Ensure the file extension is `.csv`.  An real world example would be `WIGOS_0-454-2-AWSBALAKA_2021-11-18T0955.csv`.

!!! note
    centre id's will officially managed and introduced as part of the WIS2 Topic Hierarchy throughout the WIS2 Pilot Phase.

## Conclusion

!!! success "Congratulations!"
    In this practical session, you learned how to:

    - inspect the live wis2box data mappings
    - add a new data mapping
    - update the `country` and `centre_id` values add a new data mapping
    - update the `file-pattern` value to match your data filename convention


---
title: Downloading and finding data from WIS2
---

# Downloading and finding data from WIS2

!!! abstract "Learning outcomes!"

    By the end of this practical session, you will be able to:

    - use pywis-pubsub to subscribe to a Global Broker and download data to your local system
    - use pywiscat to discover datasets from the Global Discovery Catalogue

## Introduction

In this session you will learn how to discover data from the WIS2 Global Discovery Catalogue (GDC) and download data from a WIS2 Global Broker (GB).

## Preparation

!!! note
    Before starting please login to your student VM.

## Downloading data with pywis-pubsub

The [first practical session](../connecting-to-mqtt) used MQTT Explorer to connect to the Météo-France Global Broker.

Let's use the [pywis-pubsub](https://github.com/wmo-im/pywis-pubsub) to subscribe using a command line tool.

```bash
pywis-pubsub subscribe --help
```

!!! note
    pywis-pubsub is pre-installed on the local training environment, but can be installed from anywhere with `pip3 pywis-pubsub`

Update the sample configuration (see the sections marked **TBD**) to connect to the Météo-France Global Broker:

```bash
vi ~/exercise-materials/pywis-pubsub-exercises/config.yml
```

Open MQTT Explorer and connect to the Météo-France Global Broker.

Update the following values in the configuration:

- **broker**: `mqtts://everyone:everyone@globalbroker.meteo.fr:8883`
- **subscribe_topics**: fill in one to many topics `origin/#` and `cache/#` (on separate lines)
- **storage.option.path**: add a directory to where data should be downloaded

Run the `pywis-pubsub` command:

```bash
pywis-pubsub subscribe -c ~/exercise-materials/pywis-pubsub-exercises/config.yml --verbosity DEBUG -d
```

At this point you should see a number of ongoing messages on your screen.  Hit `Crtl-C` to stop messages from arriving/download to help analyze the content.

!!! note

    The above command will download data to your local system for demo purposes.  For operational environments
    you will need to consider and manage diskspace requirements as part of your workflow.

!!! question

    What is the format of the data notifications that are displayed on the screen?

??? success "Click to reveal answer"
    The format is GeoJSON

!!! question

    Is there data being downloaded?  How can we run the `pywis-pubsub` command to be able to download the data (hint: review the options when running the `pywis-pubsub subscribe --help` command)?

??? success "Click to reveal answer"
    Add the `-d` or `--download` flag to the `pywis-pubsub` command

Stop the `pywis-pubsub` command (CTRL-C) and update the configuration to be able to download the data
to `/tmp/wis2-data`.

Try spatial filtering with a bounding box:

```bash
pywis-pubsub subscribe -c ~/exercise-materials/pywis-pubsub-exercises/config.yml --verbosity INFO -d -b -142,42,-52,84
```

!!! note

    Try using your own bounding box (format is `west,south,east,north`, in decimal degrees).

## Finding data with pywiscat

Let's use [pywiscat](https://github.com/wmo-im/pywiscat) to query the GDC

```bash
pywiscat wis2 search --help
```

!!! note
    pywiscat is pre-installed on the local training environment, but can be installed from anywhere with `pip3 install pywiscat`

```bash
pywiscat wis2 search
```

!!! question

    How many records are returned from the search?

??? success "Click to reveal answer"
    There should be 40 records returned

    ```
    Querying WIS2 GDC 🗃️ ...

    Results: 40 records
    ...
    ```

Let's try querying the GDC with a keyword:

```bash
pywiscat wis2 search -q observations
```

!!! question

    What is the data policy of the results?

??? success "Click to reveal answer"
    All data returned should specify "core" data

    ```
    +---------------------------------------------------------------------------+------------------------------+-------------------------------------------------------+-------------+
    | id                                                                        | centre                       | title                                                 | data policy |
    +---------------------------------------------------------------------------+------------------------------+-------------------------------------------------------+-------------+
    | urn:x-wmo:md:dma:dominica_met_wis2node:surface-weather-observations       | dominica_met_wis2node        | Surface weather observations from Dominica Meteoro... | core        |
    | urn:x-wmo:md:gin:conakry_met_centre:surface-weather-observations          | conakry_met_centre           | Surface weather observations from gin.conakry_met_... | core        |
    | urn:x-wmo:md:atg:antigua_met_wis2node:surface-weather-observations        | antigua_met_wis2node         | Surface weather observations from Antigua and Barb... | core        |
    | urn:x-wmo:md:bfa:ouagadougou_met_centre:surface-weather-observations      | ouagadougou_met_centre       | Surface weather observations from bfa.ouagadougou_... | core        |
    ...
    ```

Try additional queries with `-q`

!!! tip

    The `-q` flag allows for the following syntax:

    - `-q synop`: find all records with the word "synop"
    - `-q temp`: find all records with the word "temp"
    - `-q "observations AND malawi"`: find all records with the words "observations" and "malawi"
    - `-q "observations NOT malawi"`: find all records that contain the word "observations" but not the word "malawi"
    - `-q "synop OR temp"`: find all records with both "synop" or "temp"
    - `-q "obs~"`: fuzzy search

    When searching for terms with spaces, enclose in double quotes.

Let's get more details on a specific search result that we are interested in:

```bash
pywiscat wis2 get <id>
```

!!! tip

    Use the `id` value from the previous search.


## Conclusion

!!! success "Congratulations!"

    In this practical session, you learned how to:

    - use pywis-pubsub to subscribe to a Global Broker and download data to your local system
    - use pywiscat to discover datasets from the Global Discovery Catalogue

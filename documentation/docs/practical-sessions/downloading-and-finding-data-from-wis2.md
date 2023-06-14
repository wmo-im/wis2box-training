---
title: Downloading and finding data from WIS2
---

# Downloading and finding data from WIS2

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
pywis-pubsub subscribe -c ~/exercise-materials/pywis-pubsub-exercises/config.yml
```

!!! question

    What is the format of the data notifications that are displayed on the screen?

!!! question

    Is there data being downloaded?  How can we run the `pywis-pubsub` command to be able to download the data (hint: review the options when running the `pywis-pubsub subscribe --help` command)?

Stop the `pywis-pubsub` command (CTRL-C) and update the configuration to be able to download the data
to `/tmp/wis2-data`.

## Finding data with pywiscat

Let's use [pywiscat](https://github.com/wmo-im/pywiscat) to query the GDC

```bash
pywiscat wis2 search
```

!!! question

    How many records are returned from the search?


Let's try querying the GDC with a keyword:

```bash
pywiscat wis2 search -q radar
```

!!! question

    What is the data policy of the results?

Try additional queries with `-q`

!!! tip

    The `-q` flag allows for the following syntax:

    - `-q sea`: find all records with the word "sea"
    - `-q "NOT sea"`: find all records that do not contain the word "sea"
    - `-q "sea AND ice"`: find all records with both "sea" and "ice"
    - `-q "sea OR ice"`: find all records with both "sea" and "ice"
    - `-q "sea NOT ice"`: find all records with "sea" but not "ice"
    - `-q "sea~"`: fuzzy search

    If searching for terms with spaces, enclose in double quotes.

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

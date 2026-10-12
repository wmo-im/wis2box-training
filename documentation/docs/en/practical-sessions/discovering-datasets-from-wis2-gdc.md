---
title: Discovering datasets from the WIS2 Global Discovery Catalogue
---

# Discovering datasets from the WIS2 Global Discovery Catalogue

!!! abstract "Learning outcomes!"

    By the end of this practical session, you will be able to:

    - use pywmocat to discover datasets from the Global Discovery Catalogue (GDC)

## Introduction

In this session you will learn how to discover data from the WIS2 Global Discovery Catalogue (GDC) using [pywmocat](https://github.com/wmo-im/pywmocat), a command line tool to search and retrieve metadata from a WIS2 GDC.

At the moment, the following GDCs are available:

- Environment and Climate Change Canada, Meteorological Service of Canada: <https://wis2-gdc.weather.gc.ca/collections/wis2-discovery-metadata>
- China Meteorological Administration: <https://gdc.wis.cma.cn/collections/wis2-discovery-metadata>
- Deutscher Wetterdienst: <https://wis2.dwd.de/gdc/collections/wis2-discovery-metadata>


During local training sessions, a local GDC is set up to allow participants to query the GDC for the metadata they published from their wis2box-instances. In this case the trainers will provide the URL to the local GDC.

## Preparation

!!! note
    Before starting please login to your student VM.

## Installing pywmocat

Use the `pip3` Python package installer to install pywmocat on your VM:
```bash
pip3 install pywmocat
```

!!! note

    If you encounter the following error:

    ```
    WARNING: The script pywmocat is installed in '/home/username/.local/bin' which is not on PATH.
    Consider adding this directory to PATH or, if you prefer to suppress this warning, use --no-warn-script-location.
    ```

    Then run the following command:

    ```bash
    export PATH=$PATH:/home/$USER/.local/bin
    ```

    ...where `$USER` is your username on your VM.

Verify that the installation was successful:

```bash
pywmocat --version
```

## Finding data with pywmocat

By default, pywsicat connects to Global Discovery Catalogue (GDC) hosted by Environment and Climate Change Canada (ECCC).

!!! note "Changing the GDC URL"
    If you are doing this exercise during a local training session, you can configure pywmocat to query the local GDC by setting the `PYWISCAT_GDC_URL` environment variable:

    ```bash
    export PYWMOCAT_WIS2_GDC_URL=http://gdc.training.wis2dev.io/collections/wis2-discovery-metadata
    ```

To see the available options, run:

```bash
pywmocat wis2-gdc search --help
```

You can search the GDC for all records:

```bash
pywmocat wis2-gdc search
```

!!! question

    How many records are returned from the search?

??? success "Click to reveal answer"
    The number of records depends on the GDC you are querying. When using the local training GDC, you should see that the number of records is equal to the number of datasets that have been ingested into the GDC during the other practical sessions.

Let's try querying the GDC with a keyword:

```bash
pywmocat wis2-gdc search -q observations
```

!!! question

    What is the data policy of the results?

??? success "Click to reveal answer"
    All data returned should specify "core" data

Try additional queries with `-q`

!!! tip

    The `-q` flag allows for the following syntax:

    - `-q synop`: find all records with the word "synop"
    - `-q temp`: find all records with the word "temp"
    - `-q "observations AND oman"`: find all records with the words "observations" and "oman"
    - `-q "observations NOT oman"`: find all records that contain the word "observations" but not the word "oman"
    - `-q "synop OR temp"`: find all records with both "synop" or "temp"
    - `-q "obs*"`: fuzzy search

    When searching for terms with spaces, enclose in double quotes.

Let's get more details on a specific search result that we are interested in:

```bash
pywmocat wis2-gdc get <id>
```

!!! tip

    Use the `id` value from the previous search.


## Conclusion

!!! success "Congratulations!"

    In this practical session, you learned how to:

    - use pywmocat to discover datasets from the WIS2 Global Discovery Catalogue


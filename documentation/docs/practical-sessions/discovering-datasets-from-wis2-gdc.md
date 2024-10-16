---
title: Discovering datasets from the WIS2 Global Discovery Catalogue
---

# Discovering datasets from the WIS2 Global Discovery Catalogue

!!! abstract "Learning outcomes!"

    By the end of this practical session, you will be able to:

    - use pywiscat to discover datasets from the Global Discovery Catalogue (GDC)

## Introduction

In this session you will learn how to discover data from the WIS2 Global Discovery Catalogue (GDC).

At the moment, the following GDCs are available:

- Environment and Climate Change Canada, Meteorological Service of Canada: <https://wis2-gdc.weather.gc.ca>
- China Meteorological Administration: <https://gdc.wis.cma.cn/api>
- Deutscher Wetterdienst: <https://wis2.dwd.de/gdc>


During local training sessions, a local GDC is set up to allow participants to query the GDC for the metadata they published from their wis2box-instances. In this case the trainers will provide the URL to the local GDC.

## Preparation

!!! note
    Before starting please login to your student VM.

## Installing pywiscat

Use the `pip3` Python package installer to install pywiscat on your VM:
```bash
pip3 install pywiscat
```

!!! note

    If you encounter the following error:

    ```
    WARNING: The script pywiscat is installed in '/home/username/.local/bin' which is not on PATH.
    Consider adding this directory to PATH or, if you prefer to suppress this warning, use --no-warn-script-location.
    ```

    Then run the following command:

    ```bash
    export PATH=$PATH:/home/$USER/.local/bin
    ```

    ...where `$USER` is your username on your VM.

Verify that the installation was successful:

```bash
pywiscat --version
```

## Finding data with pywiscat

By default, pywiscat connects to Canada's Global Discovery Catalogue.  Let's configure pywiscat to query the training GDC by setting the `PYWISCAT_GDC_URL` environment variable:

```bash
export PYWISCAT_GDC_URL=http://<local-gdc-host-or-ip>
```

Let's use [pywiscat](https://github.com/wmo-im/pywiscat) to query the GDC setup as part of the training.

```bash
pywiscat search --help
```

Now search the GDC for all records:

```bash
pywiscat search
```

!!! question

    How many records are returned from the search?

??? success "Click to reveal answer"
    The number of records depends on the GDC you are querying. When using the local training GDC, you should see that the number of records is equal to the number of datasets that have been ingested into the GDC during the other practical sessions.

Let's try querying the GDC with a keyword:

```bash
pywiscat search -q observations
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
    - `-q "observations AND fiji"`: find all records with the words "observations" and "fiji"
    - `-q "observations NOT fiji"`: find all records that contain the word "observations" but not the word "fiji"
    - `-q "synop OR temp"`: find all records with both "synop" or "temp"
    - `-q "obs~"`: fuzzy search

    When searching for terms with spaces, enclose in double quotes.

Let's get more details on a specific search result that we are interested in:

```bash
pywiscat get <id>
```

!!! tip

    Use the `id` value from the previous search.


## Conclusion

!!! success "Congratulations!"

    In this practical session, you learned how to:

    - use pywiscat to discover datasets from the WIS2 Global Discovery Catalogue


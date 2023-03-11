---
title: WIS2 in a box cheatsheet
---

# WIS2 in a box cheatsheet

## Overview

wis2box runs as a suite of Docker Compose commands.  The ``wis2box-ctl.py`` command is a utility
(written in Python) to run Docker Compose commands easily.

## wis2box command essentials

### Building

* Build all of wis2box:

```bash
python3 wis2box-ctl.py build
```

* Build a specific wis2box Docker image:

```bash
python3 wis2box-ctl.py build wis2box-management
```

* Update wis2box:

```bash
python3 wis2box-ctl.py update
```

### Starting and stopping

* Start wis2box:

```bash
python3 wis2box-ctl.py start
```

* Stop wis2box:

```bash
python3 wis2box-ctl.py stop
```

* Verify all wis2box containers are running:

```bash
python3 wis2box-ctl.py status
```

* Login to a wis2box container (*wis2box-management* by default):

```bash
python3 wis2box-ctl.py login
```

* Login to a specific wis2box container:

```bash
python3 wis2box-ctl.py login wis2box-api
```

### Design time commands (metadata management and publishing)

!!! note

    You must be logged into the **wis2box-management** container to run the below commands

* Publish discovery metadata:

```bash
wis2box metadata discovery publish /path/to/discovery-metadata-file.yml
```

* Publish station metadata:

```bash
wis2box metadata station publish-collection
```

* Add a dataset of observation collections from discovery metadata:

```bash
wis2box data add-collection /path/to/discovery-metadata-file.yml
```

* Ingest data into the **wis2box-incoming** bucket to trigger processing and publishing:

```bash
wis2box data ingest --topic-hierarchy topic.hierarchy.path --path /path/to/directory/of/data/files
```

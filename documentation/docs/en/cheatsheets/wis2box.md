---
title: WIS2 in a box cheatsheet
---

# WIS2 in a box cheatsheet

## Overview

wis2box runs as a suite of Docker Compose commands.  The ``wis2box-ctl.py`` command is a utility
(written in Python) to run Docker Compose commands easily.

## wis2box command essentials

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

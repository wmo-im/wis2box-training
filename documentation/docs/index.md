---
title: Home
---

<img alt="WMO logo" src="assets/img/wmo-logo.png" width="200">
# WIS2 in a box training

WIS2 in a box ([wis2box](https://docs.wis2box.wis.wmo.int)) is a Free and Open Source (FOSS) Reference Implementation of a WMO WIS2 node. The project provides a plug and play toolset to ingest, process, and publish weather/climate/water data using standards-based approaches in alignment with the WIS2 principles. wis2box also provides access to all data in the WIS2 network. wis2box is designed to have a low barrier to entry for data providers, providing enabling infrastructure and services for data discovery, access, and visualization.

This training provides step-by-step explanations of various aspects of the wis2box project as well as a number of exercises
to help you publish and download data from WIS2.  The training is provided in the form of overview presentations as well as
hands-on practical exercises.

Particpants will be able to work with sample test data and metadata, as well as integrate their own data and metadata.

This training covers a wide range of topics (install/setup/configuration, publishing/downloading data, etc.).

Please see the left hand navigation for the table of contents.

## Prerequisites

### Knowledge

- Basic Linux commands (see the [cheatsheet](cheatsheets/linux.md))
- Basic knowledge of networking and Internet protocols

### Software

This training requires the following tools:

- Console/terminal to be able to run various command line tools
- MQTT Explorer
- WinSCP

## Goals and learning outcomes

The goals of this training are to become familiar with the following:

- WIS2 concepts and core functions and components
- Required and optional functions of a WIS2 Node
- WIS2 in a box architecture and environment
- data and metadata formats used in WIS2 for discovery and access
- wis2box core functions:
    - sending data
    - registering as a WIS2 Node
    - downloading data from broker
    - monitoring operations


## Conventions

Exercises are indicated as follows:

!!! question "Example exercise"

    A section marked like this indicates that you can try out the exercise.

Also you will notice tips and notes sections within the text:

!!! tip

    Tips share additional help on how to best achieve tasks

Examples are indicated as follows:

Code
``` {.html linenums="1"}
<html>
    <head>
        <title>This is an HTML sample</title>
    </head>
</html>
```

Configuration
``` {.yaml linenums="1"}
my-collection:
    type: collection
    title: my cool collection title
    description: my cool collection description
```

Snippets which need to be typed in a on a terminal/console are indicated as:

<div class="termy">
```bash
echo 'Hello world'
```
</div>

## Training location and materials

This training is always provided live at [https://training.wis2box.wis.wmo.int](https://training.wis2box.wis.wmo.int).

The training contents, wiki and issue tracker are managed on GitHub at [https://github.com/wmo-im/wis2box-training](https://github.com/wmo-im/wis2box-training).

## Printing the material

This training can be exported to PDF.  To save or print this training material, go to the [print page](print_page), and select
File > Print > Save as PDF.

## Test data for exercises

Test data can be downloaded from the [exercises.zip](https://wmo-im.github.io/wis2box-training/exercises.zip) zipfile.


## Support

For issues/bugs/suggestions or improvements/contributions to this training, please use the [GitHub issue tracker](https://github.com/wmo-im/wis2box-training/issues).

All wis2box bugs, enhancements and issues can be reported on [GitHub](https://github.com/wmo-im/wis2box/issues).

For additional support of questions, please contact wis@wmo.int.

As always, wis2box core documentation can always be found at [https://docs.wis2box.wis.wmo.int](https://docs.wis2box.wis.wmo.int).

Contributions are always enncouraged and welcome!

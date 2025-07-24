---
title: Home
---

<img alt="WMO logo" src="/assets/img/wmo-logo.png" width="200">
# WIS2 in a box training

WIS2 in a box ([wis2box](https://docs.wis2box.wis.wmo.int)) is a Free and Open Source (FOSS) Reference Implementation of a WMO WIS2 Node. The project provides a plug and play toolset to ingest, process, and publish weather/climate/water data using standards-based approaches in alignment with the WIS2 principles. wis2box also provides access to all data in the WIS2 network. wis2box is designed to have a low barrier to entry for data providers, providing enabling infrastructure and services for data discovery, access, and visualization.

This training provides step-by-step explanations of various aspects of the wis2box project as well as a number of exercises
to help you publish and download data from WIS2.  The training is provided in the form of overview presentations as well as
hands-on practical exercises.

Participants will be able to work with sample test data and metadata, as well as integrate their own data and metadata.

This training covers a wide range of topics (install/setup/configuration, publishing/downloading data, etc.). 

## Goals and learning outcomes

The goals of this training are to become familiar with the following:

- WIS2 architecture core concepts and components
- data and metadata formats used in WIS2 for discovery and access
- wis2box architecture and environment
- wis2box core functions:
    - metadata management
    - data ingest and transformation to BUFR format
    - MQTT broker for WIS2 message publishing
    - HTTP endpoint for data download
    - API endpoint for programmatic access to data

## Navigation

The left hand navigation provides a table of contents for the entire training.

The right hand navigation provides a table of contents for a specific page.

## Prerequisites

### Knowledge

- Basic Linux commands (see the [cheatsheet](./cheatsheets/linux.md))
- Basic knowledge of networking and Internet protocols

### Software

This training requires the following tools:

- An instance running Ubuntu OS (provided by WMO trainers during local training sessions) see [Accessing your student VM](./practical-sessions/accessing-your-student-vm.md#introduction)
- SSH client to access your instance
- MQTT Explorer on your local machine
- SCP and SFTP client to copy files from your local machine

## Conventions

!!! question

    A section marked like this invites you to answer a question.

Also you will notice tips and notes sections within the text:

!!! tip

    Tips share help on how to best achieve tasks.

!!! note

    Notes provide additional information on the topic covered by the practical session, as well as how to best achieve tasks.

Examples are indicated as follows:

Configuration
``` {.yaml linenums="1"}
my-collection-defined-in-yaml:
    type: collection
    title: my title defined as a yaml attribute named title
    description: my description as a yaml attribute named description
```

Snippets which need to be typed in a on a terminal/console are indicated as:

```bash
echo 'Hello world'
```

Container names (running images) are denoted in **bold**.

## Training location and materials

The training contents, wiki and issue tracker are managed on GitHub at [https://github.com/wmo-im/wis2box-training](https://github.com/wmo-im/wis2box-training).

## Exercise materials

Exercise materials can be downloaded from the [exercise-materials.zip](/exercise-materials.zip) zipfile.

## Support

For issues/bugs/suggestions or improvements/contributions to this training, please use the [GitHub issue tracker](https://github.com/World-Meteorological-Organization/wis2box-training/issues).

All wis2box bugs, enhancements and issues can be reported on [GitHub](https://github.com/World-Meteorological-Organization/wis2box/issues).

For additional support of questions, please contact wis2-support@wmo.int.

As always, wis2box core documentation can always be found at [https://docs.wis2box.wis.wmo.int](https://docs.wis2box.wis.wmo.int).

Contributions are always encouraged and welcome!

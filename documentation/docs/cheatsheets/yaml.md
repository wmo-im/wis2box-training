---
title: YAML cheatsheet
---

# YAML cheatsheet

## Overview

Many wis2box configuration files are managed in [YAML (YAML Ain't Markup Language)](https://yaml.org)
format.  YAML allows for flexible configurations using indentation to do grouping and nesting.


## Indentation

YAML is characterized by indentatation.  It is important to ensure consistet indentatation in a YAML
fileiont.

It is recommended to use **4 spaces** for a default indentation level.

It is also strongly recommended to **NOT** use tabs for indentation.

## A simple YAML file:

```yaml
my-configuration:  # <- this is a section
    # this is a comment
    # you can add comments in this manner as you wish
    section:  # <- this is nested section
        subsection:  # <- this is another nested section
            value1: 123  # an integer
            value2: 1.23  # a float
            value3: '123'  # a number forced into a string
            value4: my value  # a string (does not need quoting)
            value4: [1, 2, 3, 4]  # an array/list

    # lists can contain any data type, including more lists or sections
    my-list:  # another list, same result as value4 above
        - item 1
        - item 2
        - item 3
```             

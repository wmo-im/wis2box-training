---
title: WIS2box environment variables
---

#  WIS2box environment variables

## Introduction

In this session you will customize your wis2box environment variables and restart your wis2box anew.

### preparation

Login to your VM

Stop wis2box, and use docker commands to remove volumes 

### dev.env

The wis2box setup reads environment variables from `dev.env`. A basic example is provided by `test.env` in your current directory.

## review your new setup

Login to the **wis2box-management** container using the following command:

```bash
python3 wis2box-ctl.py login
```

Run the following command to see the environment variables used by your wis2box:

```bash
wis2box environment show
```

Note the variables you have set for `WIS2BOX_HOST_DATADIR`, `WIS2BOX_URL` and `WIS2BOX_API_URL` etc.

Review that your wis2box-broker and MinIO-storage passwords have been updated.

Run the following command to see the environment variable WIS2BOX_HOST_DATADIR

```bash
echo $WIS2BOX_HOST_DATADIR
```
returns
```console
/home/<your-username>/wis2box-data/
```

And check the content of /data/wis2box inside the wis2box-management container:

```bash
ls /data/wis2box/
```
returns:
```console
data-mappings.yml  metadata
```

!!! note
    The directory defined by `$WIS2BOX_HOST_DATADIR` gets mounted as /data/wis2box inside the wis2box-management container.

## Conclusion

!!! success "Congratulations!"
    In this practical session, you learned how to:

    - reinitialize wis2box-services
    - set the wis2box-data-directory
    - set the logging level for the wis2box-services   
    - set custom passwords for your broker and storage
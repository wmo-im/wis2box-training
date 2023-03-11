---
title: Downloading data from WIS2
---

# Downloading data from WIS2

In this session you will learn various ways to ingest data into your wis2box and learn how you can monitor if your data is being ingested without errors.

Note that the starting point for wis2box workflow is the MinIO container publishing a message on the `wisbox-storage/#` topic on the local broker.

## Preparation

!!! note
    Before starting please login to your student VM and ensure your wis2box is started and all services are up:

    ```bash
    python3 wis2box-ctl.py start
    python3 wis2box-ctl.py status
    ```

    Ensure you are logged into the wis2box-management container on your student VM:

    ```bash
    python3 wis2box-ctl.py login
    ```

## Conclusion

!!! success "Congratulations!"
    In this practical session, you learned how to:

    - prepare and verify your data mappings, dicovery metadta, and station metadata
    - ingest and publish your data
    - monitoring the status of your data ingest and publishing
    - visualize your data on the wis2box API


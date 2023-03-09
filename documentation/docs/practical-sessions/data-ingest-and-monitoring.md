---
title: Data ingest and monitoring
---

# Data ingest and monitoring

In this session you will learn various ways to ingest data into your WIS2-in-a-box and learn how you can monitor if your data is being ingested without errors. 

Note that the starting point for the WIS2-in-a-box workflow is the MinIO-container publishing a message on the 'wisbox-storage/#'-topic on the local broker. 

## Preparation

!!! note
    Before starting please login to your student-VM and ensure your wis2box is started and all services are UP: 

    ```bash
    python3 wis2box-ctl.py start
    python3 wis2box-ctl.py status
    ```

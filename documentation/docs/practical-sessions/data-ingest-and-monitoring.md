---
title: Data ingest and monitoring
---

# Data ingest and monitoring

In this session you will learn various ways to ingest data into your wis2box and learn how you can monitor if your data is being ingested without errors.

The wis2box workflow is automatically initiated when new data is received on the storage-service provided by the MinIO-container. This session introduces various ways to upload data into MinIO.

In this session participants will be asked to complete the data ingest methods introduced below using your own data-sample (or a test-data-sample from the previous csv2bufr/synop2bufr practicals).

## Preparation

!!! note
    Before starting please login to your student-VM and ensure your wis2box is started and all services are up:

    ```bash
    cd ~/exercise-materials/wis2box-setup
    python3 wis2box-ctl.py start
    python3 wis2box-ctl.py status
    ```

## Ingest data using the command line

Login to the wis2box and ingest the locally create file 'hello-world.txt' using the command line inside the 'wis2box-management'-container.

```bash
python3 wis2box-ctl.py login
echo 'hello world!' > /data/wis2box/hello_world.txt
wis2box data ingest -th cmd_line/test -p /data/wis2box/hello_world.txt
exit
```

!!! Question
    Login to the MinIO-UI accessible on http://<your-host>:9001. 
    (Default username/password is minio/minio123)
    Browse the content of the bucket 'wis2box-incoming'. What is the path for the file you just ingested ? 

!!! Question
    View your monitoring dashboard accessible on http://<your-host>:3000. 
    Did ingesting the file result in any new WIS 2.0 notifications published by your local broker? If not, why not?

!!! note
    Using 'wis2box data ingest -th' allows you to specify the topic used to publish your data. 
    The directory structure inside the MinIO-bucket reflects the topic that will be used to publish the data.

!!! note
    The 'wis2box data ingest'-command is useful to test you have correctly prepared the configuration for your wis2box.

    The Grafana dashboard will display errors indicating when a file is not successfully ingested.

**Now please prepare an actual data-sample and publish it using the correct WIS2 topic structure. Please use the country-code for your member-country and your lastname for the centre-id.**

You can use your own data-sample if you have any, or you can attempt a SYNOP or CSV data-sample from the previous exercises. 

Continue to use 'wis2box data ingest'-command until you can publish a WIS2-message on your wis2box-broker using the data-mappings.yml and station_list.csv provided in previous exercises. 

## Ingesting data using python

This will be an example of how to ingest data using python. A sample-script will be provided to push 'hello_world.txt' into the non-existing topic 'python/test' and the participant is required to correctly define the path for their data, the topic, and the wis2box connection details.

## Ingesting data using the optional FTP-server

This will be an example of how to start the optional wis2box-ftp service. The participant will need to start the service and define the correct directory-structure on their ftp-server for their data to successfully ingest data. 

An example will be provided to create the directory structure 'ftp/test' and uploading the file hello_world.txt

## Conclusion

!!! success "Congratulations!"
    In this practical session, you learned how to:

    - how to access the MinIO-UI to view the content in the MinIO-buckets
    - how to ingest data using the command line to test your wis2box configuration
    - how to ingest data programmatically in python
    - how to ingest data using the optional wis2box-ftp service
    - how to monitor the status of your data-ingestion actions using the Grafana dashboard



---
title: WIS2 in a box cheatsheet
---

# WIS2 in a box Cheatsheet

### Installing
* Build the WIS2Box: 

    ```console
    python3 wis2box-ctl.py build
    ```

* Update the WIS2Box: 
    
    ```console
    python3 wis2box-ctl.py update
    ```

* Start the WIS2Box: 
    
    ```console
    python3 wis2box-ctl.py start
    ```

* Login to the *wis2box-management* container: 

    ```console
    python3 wis2box-ctl.py login
    ```

* Verify all containers are running: 

    ```console
    python3 wis2box-ctl.py status
    ```

### Metadata and Observations
* Publish discovery metadata: 

    ```console
    wis2box metadata discovery publish <discovery_metadata_dir.yml>
    ```

* Add observation collections from discovery metadata: 

    ```console
    wis2box data add-collection <discovery_metadata_dir.yml>
    ```

* Ingest data into the *wis2box-incoming* bucket: 

    ```console
    wis2box data ingest --topic-hierarchy <topic.hierarchy> --path <observation_dir>
    ```

* Publish stations: 

    ```console
    wis2box metadata station publish-collection
    ```
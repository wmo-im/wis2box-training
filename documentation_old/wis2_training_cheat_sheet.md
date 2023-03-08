---
title: "WIS2 Training"
date: "20/02/2023"
...

# WIS2 Training Cheat Sheet

The following cheat sheet will attempt to provide you with all the basic commands you may need when using the WIS2Box.

## Student VM Access
You can access your dedicated VM on the local WIS2-training network using an **SSH-client** such as PuTTy.

* Host:
* Username:
* Password: 

## Docker
### Using a New Image
* Building the image:

    ```bash
    docker build -t <image_name> <dir_of_dockerfile>
    ```

    **Note**: If you are in the directory of the Docker file already, this is more simply:

    ```bash
    docker build -t <image_name> .
    ```


### Volume Management
* Create a volume: 

    ```bash
    docker volume create <volume_name>
    ```

* List all created volumes: 

    ```bash
    docker volume ls
    ```

* Display detailed information on a volume: 

    ```bash
    docker volume inspect <volume_name>
    ```

* Remove a volume: 

    ```bash
    docker volume rm <volume_name>
    ```

* Remove all unused volumes:

    ```bash
    docker volume prune
    ```

### Container Management
* Create a container from an image, with an interactive terminal (`it`) and a mounted volume (`v`): 

    ```bash
    docker run -it -v ${pwd}:/app <image_name>
    ```

* Display a list of currently running containers:
    
    ```bash
    docker ps
    ```

    ...or a list of all containers:
    
    ```bash
    docker ps -a
    ```

* Start a stopped container: 

    ```bash
    docker start <container_name>
    ```

* Enter the interactive terminal of a running container: 

    ```bash
    docker exec -it <container_name> bash
    ```

* Remove a container 

    ```bash
    docker rm <container_name>
    ```

* Remove a running container: 

    ```bash
    docker rm -f <container_name>
    ```

## Bash
### Directory Navigation
* Entering a true directory: 

    ```bash
    cd /folder_1/folder_2
    ```

* Entering a local directory: 

    ```bash
    cd ./folder
    ```

* Move one directory upwards: 

    ```bash
    cd ..
    ```
* Move to the previously used directory: 

    ```bash
    cd -
    ```

### File Management
* Listing files present in a directory: 

    ```bash
    ls
    ```

* Create a file: 

    ```bash
    touch <file_name>
    ```

* Copy one file to another: 

    ```bash
    cat <file_1> >> <file_2>
    ```

    **or** 
    
    ```bash
    cp <file_1> <file_2>
    ```

* Delete a file: 

    ```bash
    rm <file_name>
    ```
* Delete all files with the same file extension: 

    ```bash
    rm *.<file_extension>
    ```
* Create a folder 

    ```bash
    mkdir <folder_name>
    ```

### Connecting Commands
This routes the output of one command to another command, and is done using the pipe `|` symbol: 

```bash
command_1 |command_2
```

* Restrict outputs to those containing keyword: 

    ```bash
    command |grep <keyWord>
    ```

    * Ignoring case: 
    
        ```bash
        command |grep -i <keyword>
        ```

    * Count matching lines: 
    
        ```bash
        command |grep -c <keyWord>
        ```

    * Return outputs not containing keyword: 
    
        ```bash
        command |grep -v <keyWord>
        ```

* Display output one screen at a time: 

    ```bash
    command |more
    ```
    
    ...with controls:
    * Scroll down line by line: *enter*
    * Go to next page: *space bar*
    * Go back one page: *b*

### ecCodes Commands

* Display the data contained in a BUFR file: 
    
    ```bash
    bufr_dump -p my_bufr
    ```

* Compare the differences between two BUFR files: 

    ```bash
    bufr_compare <bufr_1> <bufr_2>
    ```

    * Ignore/blacklist keys from the comparison: 
    
        ```bash
        bufr_compare -b <key_1,key_2,key_3> <bufr_1> <bufr_2>
        ```

### Performing Multiple Commands (One-Liners)

Multiple commands can be ran in sequential order from the same line using the semi-colon `;` symbol: 

```bash
command_1; command_2; command_3
```

___

## WIS2Box

### Installing
* Build the WIS2Box: 

    ```bash
    python3 wis2box-ctl.py build
    ```

* Update the WIS2Box: 
    
    ```bash
    python3 wis2box-ctl.py update
    ```

* Start the WIS2Box: 
    
    ```bash
    python3 wis2box-ctl.py start
    ```

* Login to the *wis2box-management* container: 

    ```bash
    python3 wis2box-ctl.py login
    ```

* Verify all containers are running: 

    ```bash
    python3 wis2box-ctl.py status
    ```

### Metadata and Observations
* Publish discovery metadata: 

    ```bash
    wis2box metadata discovery publish <discovery_metadata_dir.yml>
    ```

* Add observation collections from discovery metadata: 

    ```bash
    wis2box data add-collection <discovery_metadata_dir.yml>
    ```

* Ingest data into the *wis2box-incoming* bucket: 

    ```bash
    wis2box data ingest --topic-hierarchy <topic.hierarchy> --path <observation_dir>
    ```

* Publish stations: 

    ```bash
    wis2box metadata station publish-collection
    ```

_____

## SYNOP2BUFR
* Convert a SYNOP message to BUFR: 

    ```bash
    synop2bufr transform --metadata <my_file.csv> --output-dir <./my_folder> --year <message_year> --month <message_month> <SYNOP_file_dir.txt>
    ```
    
    **Note**: The options for this command are not required, and if not specified take the following default values: 

    | Option      | Default |
    | ----------- | ----------- |
    | --metadata | metadata.csv |
    | --output-dir | The current working directory. |
    | --year | The current year. |
    | --month | The current month. |

## CSV2BUFR
* Create a template mappings file: 

    ```bash
    csv2bufr mappings create <BUFR descriptors> --output <output_dir>
    ```

* Convert a CSV file to BUFR: 

    ```bash
    csv2bufr data transform --bufr-template <my_template.json> --output-dir <./my_folder> <CSV_file_dir.csv>
    ```

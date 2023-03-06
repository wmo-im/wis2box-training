---
title: Linux cheatsheet
---

# Linux Cheatsheet

## Bash
### Directory Navigation
* Entering a true directory: 

    ```console
    cd /folder_1/folder_2
    ```

* Entering a local directory: 

    ```console
    cd ./folder
    ```

* Move one directory upwards: 

    ```console
    cd ..
    ```
* Move to the previously used directory: 

    ```console
    cd -
    ```

### File Management
* Listing files present in a directory: 

    ```console
    ls
    ```

* Create a file: 

    ```console
    touch <file_name>
    ```

* Copy one file to another: 

    ```console
    cat <file_1> >> <file_2>
    ```

    **or** 
    
    ```console
    cp <file_1> <file_2>
    ```

* Delete a file: 

    ```console
    rm <file_name>
    ```
* Delete all files with the same file extension: 

    ```console
    rm *.<file_extension>
    ```
* Create a folder 

    ```console
    mkdir <folder_name>
    ```

### Connecting Commands
This routes the output of one command to another command, and is done using the pipe `|` symbol: 

```console
command_1 |command_2
```

* Restrict outputs to those containing keyword: 

    ```console
    command |grep <keyWord>
    ```

    * Ignoring case: 
    
        ```console
        command |grep -i <keyword>
        ```

    * Count matching lines: 
    
        ```console
        command |grep -c <keyWord>
        ```

    * Return outputs not containing keyword: 
    
        ```console
        command |grep -v <keyWord>
        ```

* Display output one screen at a time: 

    ```console
    command |more
    ```
    
    ...with controls:
    * Scroll down line by line: *enter*
    * Go to next page: *space bar*
    * Go back one page: *b*
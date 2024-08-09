---
title: Initializing wis2box
---

#  Initializing wis2box

!!! abstract "Learning outcomes"

    By the end of this practical session, you will be able to:

    - run the `wis2box-create-config.py` script to create the initial configuration
    - start wis2box and check the status of its components
    - access the **wis2box-webapp**, API, MinIO UI and Grafana dashboard in a browser
    - connect to the local **wis2box-broker** using MQTT Explorer

!!! note

    The current training materials are using wis2box-1.0b8. 
    
    See [accessing-your-student-vm](accessing-your-student-vm.md) for instructions on how to download and install the wis2box software stack if you are running this training outside of a local training session.

## Preparation

Login to your designated VM with your username and password and ensure you are in the `wis2box-1.0b8` directory:

```bash
cd ~/wis2box-1.0b8
```

## creating the initial configuration

The initial configuration for the wis2box requires:

- an environment file `wis2box.env` containing the configuration parameters
- a directory on the host-machine to share between the host machine and the wis2box containers defined by the `WIS2BOX_HOST_DATADIR` environment variable

The `wis2box-create-config.py` script can be used to create the initial configuration of your wis2box. 

It will ask you a set of question to help setup your configuration.

You will be able to review and update the configuration files after the script has completed.

Run the script as follows:

```bash
python3 wis2box-create-config.py
```

### wis2box-data directory

The script will ask you to enter the directory to be used for the `WIS2BOX_HOST_DATADIR` environment variable.

Note that you need to define the full path to this directory.

For example if your username is `mlimper`, the full path to the directory is `/home/mlimper/wis2box-data`:

```{.copy}
mlimper@student-vm-mlimper:~/wis2box-1.0b8$ python3 wis2box-create-config.py
Please enter the directory on the host to be used for WIS2BOX_HOST_DATADIR:
/home/mlimper/wis2box-data
Configuration-files will be stored in the following directory:
    /home/mlimper/wis2box-data
Is this correct? (y/n/exit)
y
The directory /home/mlimper/wis2box-data has been created.
```

### wis2box URL

Next, you will be asked to enter the URL for your wis2box. This is the URL that will be used to access the wis2box web application, API and UI.

Please use `http://<your-hostname>` as the URL. Remember that your hostname is defined by your `username.wis2.training`

```{.copy}
Please enter the URL of the wis2box:
 For local testing the URL is http://localhost
 To enable remote access, the URL should point to the public IP address or domain name of the server hosting the wis2box.
http://mlimper.wis2.training
The URL of the wis2box will be set to:
  http://mlimper.wis2.training
Is this correct? (y/n/exit)
```

### WEBAPP, STORAGE and BROKER passwords

You can use the option of random password generation when prompted for and `WIS2BOX_WEBAPP_PASSWORD`, `WIS2BOX_STORAGE_PASSWORD`, `WIS2BOX_BROKER_PASSWORD` and define your own.

Don't worry about remembering these passwords, they will be stored in the `wis2box.env` file in your wis2box-1.0b8 directory.

### review configuration

Once the scripts is completed check the contents of the `wis2box.env` file in your current directory:

```bash
cat ~/wis2box-1.0b8/wis2box.env
```

Or check the content of the file via WinSCP.

!!! question 

    What is the value of the WIS2BOX_STORAGE_DATA_RETENTION_DAYS environment variable in the wis2box.env file?

??? success "Click to reveal answer"

    The default value for WIS2BOX_STORAGE_DATA_RETENTION_DAYS is 30 days. You can change this value to a different number of days if you wish.
    
    The wis2box-management container runs a cronjob on a daily basis to remove data older than the number of days defined by WIS2BOX_STORAGE_DATA_RETENTION_DAYS from the `wis2box-public` bucket and the API backend:
    
    ```{.copy}
    0 0 * * * su wis2box -c "wis2box data clean --days=$WIS2BOX_STORAGE_DATA_RETENTION_DAYS"
    ```

!!! note

    The `wis2box.env` file contains environment variables defining the configuration of your wis2box. For more information consult the [wis2box-documentation](https://docs.wis2box.wis.wmo.int/en/latest/reference/configuration.html)


## wis2box start and status

Ensure you are in the directory containing the wis2box software stack:

```{.copy}
cd ~/wis2box-1.0b8
```

Start wis2box with the following command:

```{.copy}
python3 wis2box-ctl.py start
```

Inspect the status with the following command:

```{.copy}
python3 wis2box-ctl.py status
```

Repeat this command until all services are up and running.

!!! note "wis2box and Docker"
    wis2box runs as a set of Docker containers managed by docker-compose.
    
    The services are defined in the various `docker-compose*.yml` which can be found in the `~/wis2box-1.0b8/` directory.
    
    The Python script `wis2box-ctl.py` is used to run the underlying Docker Compose commands that control the wis2box services.

To login to the wis2box-management container, use the following command:

```{.copy}
python3 wis2box-ctl.py login
```

Inside the wis2box-management container you can run various commands to manage your wis2box, such as:

- `wis2box auth add-token --path processes/wis2box` : to create an authorization token for the `processes/wis2box` endpoint
- `wis2box data clean --days=<number-of-days>` : to clean up data older than a certain number of days from the `wis2box-public` bucket

To exit the container and go back to the host machine, use the following command:

```{.copy}
exit
```

## wis2box UI

Open a web browser and visit the page `http://<your-host>`:

<img alt="wis2box-ui.png" src="../../assets/img/wis2box-ui-empty.png" width="600">

The wis2box UI will display your configured datasets. The UI is currently empty, as datasets have not yet been configured.

## wis2box API

Open a new tab and navigate to the page `http://<your-host>/oapi`.

<img alt="wis2box-api.png" src="../../assets/img/wis2box-api.png" width="800">

This is the wis2box API (running via the **wis2box-api** container).

!!! question
     
     What collections are currently available?

??? success "Click to reveal answer"
    
    To view collections currently available through the API, click `View the collections in this service`:

    <img alt="wis2box-api-collections.png" src="../../assets/img/wis2box-api-collections.png" width="600">

    The following collections are currently available:

    - Discovery metadata
    - Station metadata
    - Data notifications

!!! question

    How many data notifications have been published?

??? success "Click to reveal answer"

    Click on "Data notifications", then click on `Browse through the items of "Data Notifications"`. 
    
    You will note that the page says "No items" as no Data notifications have been published yet.

## wis2box webapp

Open a web browser and visit the page `http://<your-host>/wis2box-webapp`.

You will see a pop-up asking for your username and password. Use the default username `wis2box-user` and the `WIS2BOX_WEBAPP_PASSWORD` defined in the `wis2box.env` file and click "Sign in":

!!! note 

    Check you wis2box.env for the value of your WIS2BOX_WEBAPP_PASSWORD. You can use the following command to check the value of this environment variable:

    ```{.copy}
    cat ~/wis2box-1.0b8/wis2box.env | grep WIS2BOX_WEBAPP_PASSWORD
    ```

Once logged in, you move your mouse to the menu on the left to see the options available in the wis2box web application:

<img alt="wis2box-webapp-menu.png" src="../../assets/img/wis2box-webapp-menu.png" width="400">

This is the wis2box web application to enable you to interact with your wis2box:

- create and manage datasets
- update/review your station metadata
- ingest ASCII and CSV data
- monitor notifications published on your wis2box-broker

We will use this web application in a later session.

## wis2box-broker

Open the MQTT Explorer on your computer and prepare a new connection to connect to your broker (running via the **wis2box-broker** container).

Click `+` to add a new connection:

<img alt="mqtt-explorer-new-connection.png" src="../../assets/img/mqtt-explorer-new-connection.png" width="300">

You can click on the 'ADVANCED' button and verify you have subscriptions to the the following topics:

- `#`
- `$SYS/#`

<img alt="mqtt-explorer-topics.png" src="../../assets/img/mqtt-explorer-topics.png" width="550">

!!! note

    The `#` topic is a wildcard subscription that will subscribe to all topics published on the broker.

    The messages published under the `$SYS` topic are system messages published by the mosquitto service itself.

Use the following connection details, making sure to replace the value of `<your-host>` with your hostname and `<WIS2BOX_BROKER_PASSWORD>` with the value from your `wis2box.env` file:

- **Protocol: mqtt://**
- **Host: `<your-host>`**
- **Port: 1883**
- **Username: wis2box**
- **Password: `<WIS2BOX_BROKER_PASSWORD>`**

!!! note 

    You can check your wis2box.env for the value of your WIS2BOX_BROKER_PASSWORD. You can use the following command to check the value of this environment variable:

    ```{.copy}
    cat ~/wis2box-1.0b8/wis2box.env | grep WIS2BOX_BROKER_PASSWORD
    ```

    Note that this your **internal** broker password, the Global Broker will use different (read-only) credentials to subscribe to your broker. Never share this password with anyone.

Make sure to click "SAVE" to store your connection details.

Then click "CONNECT" to connect to your **wis2box-broker**.

<img alt="mqtt-explorer-wis2box-broker.png" src="../../assets/img/mqtt-explorer-wis2box-broker.png" width="600">

Once you are connected, you should see statistics being published by your broker on the `$SYS/#`.

Keep the MQTT Explorer open, as we will use it to monitor the messages published on the broker.

## MinIO UI

Open a web browser and visit the page `http://<your-host>:9001`:

<img alt="minio-ui.png" src="../../assets/img/minio-ui.png" width="600">

This is the MinIO UI (running via the **wis2box-storage** container).

The username and password are defined in the `wis2box.env` file in your wis2box data directory by the environment variables `WIS2BOX_STORAGE_USERNAME` and `WIS2BOX_STORAGE_PASSWORD`. The default username is `wis2box`.

!!! note 

    You can check your wis2box.env for the value of your WIS2BOX_STORAGE_PASSWORD. You can use the following command to check the value of this environment variable:

    ```{.copy}
    cat ~/wis2box-1.0b8/wis2box.env | grep WIS2BOX_STORAGE_PASSWORD
    ```

    Note that these are the read-write credentials for your MinIO instance. Never share these credentials with anyone. The Global Services can only download data from your MinIO instance using the web-proxy on the wis2box-public bucket.

Try to login to your MinIO UI. You will see that there 3 buckets already defined:

- `wis2box-incoming`: used to receive incoming data
- `wis2box-public`: used to store data that is made available in the WIS2 notifications, the content of this bucket is proxied as `/data` on your `WIS2BOX_URL` via the nginx container
- `wis2box-archive`: used to archive data from `wis2box-incoming` on a daily basis

<img alt="minio-ui-buckets.png" src="../../assets/img/wis2box-minio-buckets.png" width="600">

!!! note

    The **wis2box-storage** container (provided by MinIO) will send a notification on the **wis2box-broker** when data is received. The **wis2box-management** container is subscribed to all messages on `wis2box/#` and will receive these notifications, triggering the data pipelines defined in your `data-mappings.yml`.

### Using the MinIO UI to test data ingestion

First click on "browse" for the `wis2box-incoming` bucket, then click on "Create new path" and enter the path `/testing/upload/`:

<img alt="minio-ui-create-path.png" src="../../assets/img/minio-ui-create-path.png" width="600">

Then click on "Upload" and select a file from your local machine to upload to the `wis2box-incoming` bucket

You should now see the file in the `wis2box-incoming` bucket:

<img alt="minio-ui-upload-file.png" src="../../assets/img/minio-ui-upload-file.png" width="600">

!!! question

    Did you see a message published on your MQTT-broker in MQTT Explorer?

??? success "Click to reveal answer"

    If you are connected to your wis2box-broker, you should note that a message has been published on the `wis2box/storage` topic. This is how MinIO informs the wis2box-management service that there is new data to process. Note that this is *not* a WIS2 notification, but an internal message between components within the wis2box software stack.

The wis2box is not yet configured to process any files you upload, so the file will not be processed and no WIS2 notification will be published

We will check the error message produced by the wis2box-management container in the Grafana dashboard in the next step.

## Grafana UI

Open a web browser and visit the page `http://<your-host>:3000`:

<img alt="wis2box-grafana-ui.png" src="../../assets/img/wis2box-grafana-ui.png" width="600">

This is the Grafana UI, where you can view the wis2box workflow monitoring dashboard. You can also access the logs of the various containers in the wis2box software stack via the 'Explore' option in the menu.

!!! question

    Are there any errors or warnings displayed in the your dashboard ?

??? success "Click to reveal answer"

    You will see an error message indicating that the wis2box could not process the file you uploaded.

    This is expected as we have not yet configured any datasets in the wis2box, you will learn how to do this in the next practical session.

## Conclusion

!!! success "Congratulations!"
    In this practical session, you learned how to:

    - run the `wis2box-create-config.py` script to create the initial configuration
    - start wis2box and check the status of its components
    - connect to the **wis2box-broker** using MQTT Explorer
    - access the wis2box-UI, wis2box-webapp and wis2box-API in a browser
    - upload a file to the `wis2box-incoming` bucket in the MinIO UI
    - view the Grafana dashboard to monitor the wis2box workflow

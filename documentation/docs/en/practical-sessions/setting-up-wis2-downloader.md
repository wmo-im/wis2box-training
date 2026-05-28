---
title: Set up WIS2 Downloader on your student VM
---

# Set up WIS2 Downloader on your student VM

!!! abstract "Learning outcomes!"

    By the end of this practical session, you will be able to:

    - set up your own "WIS2 Downloader" instance and manage the specific configurations required
    - navigate through the instance to make use of it's different capabilities 

## Introduction

In this session you will learn how to set up a WIS2 Downloader instance on the provided student VM and how to navigate thorugh it's different services.

!!! note "About WIS2 Downloader"
     
     The WIS2 Downloader is available as a standalone Docker Compose project and is recommended to be ran on a separate server from the wis2box, so as to not have the downloads interfering with the publication of messages.

     If you would like to develop your own service for subscribing to WIS2 notifications and downloading data, you can use the [WIS2 Downloader source code](https://github.com/World-Meteorological-Organization/wis2downloader) as a reference.

## Preparation and requirements

!!! note "If not during the training"

    The following steps are only to be applied if the mentioned ports are unavailable by default on the server. In any configuration, these are the only ports needed  to be accessed in order to use the full capabilities of the WIS2 Downloader stack.    

Before starting please log in to your student VM making sure to tunnel via SSH the following ports:

- `5002 (API)`
- `8080 (UI)`
- `3000 (Grafana)`

To do this you can change the settings of your connection in Putty:

![access putty tunnel settings](../assets/img/putty-tunnel-settings.png)

Then add the 3 ports mapping to ports on your own pc(localhost):

![adding tunnels in putty](../assets/img/putty-add-tunnel.png)


## WIS2 Downloader installation

Download the latest release tarball from GitHub and extract it on your student VM:

```bash
wget https://github.com/World-Meteorological-Organization/wis2downloader/releases/latest/download/wis2downloader-latest.tar.gz
tar -xzf wis2downloader-latest.tar.gz
cd wis2downloader-*
```

Run the setup script to generate your configuration file:

```bash
bash setup.sh
```

This creates a `.env` file from the defaults and generates random values for `FLASK_SECRET_KEY` and `REDIS_PASSWORD`. You can review the file with `cat .env` — the defaults are suitable for a single-machine deployment.

Install the Loki Docker plugin used for log shipping:

```bash
ARCH=$(uname -m | sed 's/x86_64/amd64/;s/aarch64/arm64/')
docker plugin install grafana/loki-docker-driver:3.6.7-${ARCH} --alias loki --grant-all-permissions
```

Verify the plugin is enabled:

```bash
docker plugin ls
```

You should see `loki:latest` listed with `ENABLED` set to `true`.

Create a dedicated `wis2` group, add your user to it, and configure the `.env` file and downloads directory accordingly:

```bash
sudo groupadd wis2
sudo usermod -aG wis2 $USER
sed -i "s/^UID=.*/UID=$(id -u)/" .env
sed -i "s/^GID=.*/GID=$(getent group wis2 | cut -d: -f3)/" .env
mkdir -p downloads
sudo chown $(id -un):wis2 downloads
chmod 775 downloads
```

!!! note "Re-login required"
    The group membership change only takes effect after you log out and back in to your SSH session.

Start the full service stack:

```bash
docker compose up -d
```

Wait about 30 seconds for the health checks to pass, then confirm the subscription manager is ready:

```bash
curl http://localhost:5002/health
```

!!! note "Checking the running containers"
    You can verify all containers started successfully with:
    ```bash
    docker compose ps
    ```
    You should see services for the subscription manager, MQTT subscribers, UI, Celery workers, Redis, Prometheus, Grafana, and Loki.

### Accesing the WIS2 Downloader UI

Open a web browser and navigate to the UI for your WIS2 Downloader instance by going to `http://localhost:8080`.

You will find yourself in the landing page which is set to the `Help` section by default showing the documentation.

![WIS2 Downloader Landing Page](../assets/img/wis2-downloader-landing-page.png)

In the left sidebar menu you'll be able to navigate through all the different sections of the UI.

The main sections available are:

- **Dashboard** — an embedded Grafana dashboard showing download activity, queue status, and metrics for the running service. Also available at `http://localhost:3000`.
- **Catalogue View** — browse available WIS2 datasets by searching or filtering the global catalogue. Select a topic and a save directory, then click *Subscribe* to start downloading.
- **Tree View** — navigate the WIS2 topic hierarchy as a collapsible tree. Useful for exploring what topics are available before subscribing.
- **Manual Subscription** — create a subscription by entering a topic and broker details directly, without relying on the Global Discovery Catalogues. Useful for subscribing to topics from specific WIS2 Nodes or private brokers.
- **Subscriptions** — view and manage all active subscriptions. From here you can see which topics are being monitored and remove any you no longer need.
- **Settings** — currently allows you to reload the dataset catalogue from the Global Discovery Catalogues. This section will be expanded in future releases to cover general configuration and management of the WIS2 Downloader.
- **Help** — the default landing page, showing the built-in documentation for the WIS2 Downloader.

### Reviewing the WIS2 Downloader configuration

The WIS2 Downloader instance can be configured using the environment variables defined in your `.env` file.

You may check a breakdown of the environment variables in the [WIS2 Downloader Admin Guide Section 2.1](https://world-meteorological-organization.github.io/wis2downloader/en/admin-guide.html)

To review the current configuration of the WIS2 Downloader, you can use the following command:

```bash
cat .env
```

!!! question "Review the configuration of the WIS2 Downloader"

    What is the default retention period for the downloaded data?

    Which port does the subscription manager API listen on?

??? success "Click to reveal answer"

    The default retention period for the downloaded data is `30` days, as set by `DOWNLOAD_RETENTION_PERIOD`.

    The subscription manager API listens on port `5002`, as defined in `WIS2DOWNLOADER_SUBSCRIPTION_MANAGER_URL`.

!!! note "Updating the configuration of the WIS2 Downloader"

    To update the configuration, edit the `.env` file and restart the stack to apply the changes:

    ```bash
    docker compose up -d
    ```

You can keep the default configuration for the next exercises.

### WIS2 Downloader API

The WIS2 Downloader exposes a REST API at `<WIS2DOWNLOADER_BASE_URL>:5002/api`. Confirm the service is ready:

```bash
curl <WIS2DOWNLOADER_BASE_URL>:5002/api/health
```

You should see:

```json
{"status": "healthy"}
```

To create a subscription, send a `POST` request with the MQTT `topic` and an optional `target` subdirectory where files will be saved:

```bash
curl -s -X POST <WIS2DOWNLOADER_BASE_URL>:5002/api/subscriptions \
  -H "Content-Type: application/json" \
  -d '{"topic": "cache/a/wis2/+/data/core/weather/surface-based-observations/#", "target": "surface-obs"}'
```

The response includes the UUID assigned to the new subscription. Use it to delete the subscription when no longer needed:

```bash
curl -X DELETE <WIS2DOWNLOADER_BASE_URL>:5002/api/subscriptions/{id}
```

For the full list of available endpoints (list, get, update subscriptions and more), refer to the interactive Swagger documentation available at `<WIS2DOWNLOADER_BASE_URL>:5002/api/openapi`.


## Conclusion

!!! success "Congratulations!"

    In this practical session, you learned how to:

    - install WIS2 Downloader on your local system and change the default configurations
    - interact with the UI to create and remove subscriptions
    - manage subscriptions using the API
    - view the downloaded data on your local system

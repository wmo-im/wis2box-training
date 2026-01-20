---
title: 初始化 wis2box
---

# 初始化 wis2box

!!! abstract "学习目标"

    在本次实践课程结束时，您将能够：

    - 运行 `wis2box-create-config.py` 脚本以创建初始配置
    - 启动 wis2box 并检查其组件的状态
    - 查看 **wis2box-api** 的内容
    - 访问 **wis2box-webapp**
    - 使用 MQTT Explorer 连接到本地 **wis2box-broker**

!!! note

    当前的培训材料基于 wis2box-release 1.2.0。

    如果您在本地培训课程之外运行本次培训，请参阅 [accessing-your-student-vm](./accessing-your-student-vm.md) 以获取有关如何下载和安装 wis2box 软件栈的说明。

## 准备工作

使用您的用户名和密码登录到指定的虚拟机，并确保您位于 `wis2box` 目录中：

```bash
cd ~/wis2box
```

## 创建初始配置

wis2box 的初始配置需要以下内容：

- 一个包含配置参数的环境文件 `wis2box.env`
- 主机与 wis2box 容器之间共享的一个目录，该目录由环境变量 `WIS2BOX_HOST_DATADIR` 定义

可以使用 `wis2box-create-config.py` 脚本来创建 wis2box 的初始配置。

脚本会向您提出一系列问题以帮助设置配置。

在脚本完成后，您可以查看并更新配置文件。

按以下方式运行脚本：

```bash
python3 wis2box-create-config.py
```

### wis2box-host-data 目录

脚本会要求您输入用于 `WIS2BOX_HOST_DATADIR` 环境变量的目录。

请注意，您需要定义该目录的完整路径。

例如，如果您的用户名是 `username`，目录的完整路径为 `/home/username/wis2box-data`：

```{.copy}
username@student-vm-username:~/wis2box$ python3 wis2box-create-config.py
Please enter the directory to be used for WIS2BOX_HOST_DATADIR:
/home/username/wis2box-data
The directory to be used for WIS2BOX_HOST_DATADIR will be set to:
    /home/username/wis2box-data
Is this correct? (y/n/exit)
y
The directory /home/username/wis2box-data has been created.
```

### wis2box URL

接下来，您将被要求输入 wis2box 的 URL。此 URL 将用于访问 wis2box 的 Web 应用程序、API 和用户界面。

请使用 `http://<your-hostname-or-ip>` 作为 URL。

```{.copy}
Please enter the URL of the wis2box:
 For local testing the URL is http://localhost
 To enable remote access, the URL should point to the public IP address or domain name of the server hosting the wis2box.
http://username.wis2.training
The URL of the wis2box will be set to:
  http://username.wis2.training
Is this correct? (y/n/exit)
```

### WEBAPP、STORAGE 和 BROKER 密码

当提示输入 `WIS2BOX_WEBAPP_PASSWORD`、`WIS2BOX_STORAGE_PASSWORD` 和 `WIS2BOX_BROKER_PASSWORD` 时，您可以选择随机生成密码或自行定义。

无需担心记住这些密码，它们会存储在 `wis2box` 目录中的 `wis2box.env` 文件中。

### 检查 `wis2box.env`

脚本完成后，检查当前目录中 `wis2box.env` 文件的内容：

```bash
cat ~/wis2box/wis2box.env
```

或者通过 WinSCP 检查文件内容。

!!! question

    `wis2box.env` 文件中 WISBOX_BASEMAP_URL 的值是什么？

??? success "点击查看答案"

    WIS2BOX_BASEMAP_URL 的默认值是 `https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png`。

    此 URL 指向 OpenStreetMap 的瓦片服务器。如果您希望使用其他地图提供商，可以将此 URL 更改为指向其他瓦片服务器。

!!! question 

    `wis2box.env` 文件中 WIS2BOX_STORAGE_DATA_RETENTION_DAYS 环境变量的值是什么？

??? success "点击查看答案"

    WIS2BOX_STORAGE_DATA_RETENTION_DAYS 的默认值是 30 天。如果需要，您可以将此值更改为其他天数。

    wis2box-management 容器每天运行一个 cronjob，从 `wis2box-public` 存储桶和 API 后端中删除超过 WIS2BOX_STORAGE_DATA_RETENTION_DAYS 定义天数的数据：

    ```{.copy}
    0 0 * * * su wis2box -c "wis2box data clean --days=$WIS2BOX_STORAGE_DATA_RETENTION_DAYS"
    ```

!!! note

    `wis2box.env` 文件包含定义 wis2box 配置的环境变量。有关更多信息，请参阅 [wis2box-documentation](https://docs.wis2box.wis.wmo.int/en/latest/reference/configuration.html)。

    除非您确定所做更改，否则不要编辑 `wis2box.env` 文件。不正确的更改可能导致 wis2box 无法正常工作。

    请勿与他人共享 `wis2box.env` 文件的内容，因为其中包含密码等敏感信息。

## 启动 wis2box

确保您位于包含 wis2box 软件栈定义文件的目录中：

```{.copy}
cd ~/wis2box
```

通过以下命令启动 wis2box：

```{.copy}
python3 wis2box-ctl.py start
```

首次运行此命令时，您将看到以下输出：

```
No docker-compose.images-*.yml files found, creating one
Current version=Undefined, latest version=1.2.0
Would you like to update ? (y/n/exit)
```

选择 ``y``，脚本将创建文件 ``docker-compose.images-1.2.0.yml``，下载所需的 Docker 镜像并启动服务。

根据您的网络连接速度，下载镜像可能需要一些时间。此步骤仅在首次启动 wis2box 时需要。

通过以下命令检查状态：

```{.copy}
python3 wis2box-ctl.py status
```

重复运行此命令，直到所有服务都启动并运行。

!!! note "wis2box 和 Docker"
    wis2box 作为一组由 docker-compose 管理的 Docker 容器运行。
    
    服务定义在 `~/wis2box/` 目录中的各种 `docker-compose*.yml` 文件中。
    
    Python 脚本 `wis2box-ctl.py` 用于运行控制 wis2box 服务的底层 Docker Compose 命令。

    您无需了解 Docker 容器的详细信息即可运行 wis2box 软件栈，但您可以查看 `docker-compose*.yml` 文件以了解服务的定义。如果您有兴趣了解更多关于 Docker 的信息，可以参考 [Docker 文档](https://docs.docker.com/)。

要登录到 wis2box-management 容器，请使用以下命令：

```{.copy}
python3 wis2box-ctl.py login
```

注意，登录后，您的提示符会发生变化，表明您现在位于 wis2box-management 容器内：

```{bash}
root@025381da3c40:/home/wis2box#
```

在 wis2box-management 容器内，您可以运行各种命令来管理您的 wis2box，例如：

- `wis2box auth add-token --path processes/wis2box`：为 *processes/wis2box* 端点创建授权令牌
- `wis2box data clean --days=<number-of-days>`：清理 *wis2box-public* 存储桶中超过指定天数的数据

要退出容器并返回主机，请使用以下命令：

```{.copy}
exit
```

运行以下命令查看主机上运行的 Docker 容器：

```{.copy}
docker ps --format "table {{.Names}} \t{{.Status}} \t{{.Image}}"
```

您应该会看到以下容器正在运行：

```{bash}
NAMES                     STATUS                   IMAGE
elasticsearch            docker.elastic.co/elasticsearch/elasticsearch:8.6.2                              "/bin/tini -- /usr/l…"   elasticsearch            大约一分钟前   正在运行 (健康)     9200/tcp, 9300/tcp
elasticsearch-exporter   quay.io/prometheuscommunity/elasticsearch-exporter:latest                        "/bin/elasticsearch_…"   elasticsearch-exporter   大约一分钟前   正在运行               7979/tcp
grafana                  grafana/grafana-oss:9.0.3                                                        "/run.sh"                grafana                  大约一分钟前   正在运行               0.0.0.0:3000->3000/tcp
loki                     grafana/loki:2.4.1                                                               "/usr/bin/loki -conf…"   loki                     大约一分钟前   正在运行               3100/tcp
mosquitto                ghcr.io/world-meteorological-organization/wis2box-broker:1.2.0                   "/docker-entrypoint.…"   mosquitto                大约一分钟前   正在运行               0.0.0.0:1883->1883/tcp, 0.0.0.0:8884->8884/tcp
mqtt_metrics_collector   ghcr.io/world-meteorological-organization/wis2box-mqtt-metrics-collector:1.2.0   "python3 -u mqtt_met…"   mqtt_metrics_collector   大约一分钟前   正在运行 10 秒                   8000/tcp, 0.0.0.0:8001->8001/tcp
nginx                    nginx:alpine                                                                     "/docker-entrypoint.…"   web-proxy                大约一分钟前   正在运行 9 秒                    0.0.0.0:80->80/tcp
prometheus               prom/prometheus:v2.37.0                                                          "/bin/prometheus --c…"   prometheus               大约一分钟前   正在运行               9090/tcp
wis2box-api              ghcr.io/world-meteorological-organization/wis2box-api:1.2.0                      "/app/docker/es-entr…"   wis2box-api              大约一分钟前   正在运行 36 秒 (健康)         
wis2box-auth             ghcr.io/world-meteorological-organization/wis2box-auth:1.2.0                     "/entrypoint.sh"         wis2box-auth             大约一分钟前   正在运行 10 秒                   
wis2box-management       ghcr.io/world-meteorological-organization/wis2box-management:1.2.0               "/home/wis2box/entry…"   wis2box-management       大约一分钟前   正在运行 12 秒                   
wis2box-minio            minio/minio:RELEASE.2024-08-03T04-33-23Z-cpuv1                                   "/usr/bin/docker-ent…"   minio                    大约一分钟前   正在运行 (健康)     0.0.0.0:8022->8022/tcp, 0.0.0.0:9000-9001->9000-9001/tcp
wis2box-ui               ghcr.io/world-meteorological-organization/wis2box-ui:1.2.0                       "/docker-entrypoint.…"   wis2box-ui               大约一分钟前   正在运行 35 秒                   0.0.0.0:9999->80/tcp
wis2box-webapp           ghcr.io/world-meteorological-organization/wis2box-webapp:1.2.0                   "sh /wis2box-webapp/…"   wis2box-webapp           大约一分钟前   正在运行 (不健康)   4173/tcp
wis2downloader           ghcr.io/wmo-im/wis2downloader:v0.3.2                                             "/home/wis2downloade…"   wis2downloader           大约一分钟前   正在运行 (健康)

```

这些容器是 wis2box 软件栈的一部分，提供运行 wis2box 所需的各种服务。

运行以下命令以查看主机上运行的 Docker 卷：

```{.copy}
docker volume ls
```

您应该会看到以下卷：

- wis2box_project_auth-data
- wis2box_project_es-data
- wis2box_project_minio-data
- wis2box_project_prometheus-data
- wis2box_project_loki-data
- wis2box_project_mosquitto-config

以及一些由不同容器使用的匿名卷。

以 `wis2box_project_` 开头的卷用于存储 wis2box 软件栈中各种服务的持久数据。

## wis2box API

wis2box 包含一个 API（应用程序编程接口），提供数据访问和处理功能，用于交互式可视化、数据转换和发布。

打开一个新标签页，导航到页面 `http://YOUR-HOST/oapi`。

<img alt="wis2box-api.png" src="/../assets/img/wis2box-api.png" width="800">

这是 wis2box API 的登录页面（通过 **wis2box-api** 容器运行）。

!!! question
     
     当前有哪些集合可用？

??? success "点击查看答案"
    
    要查看 API 当前可用的集合，请点击 `View the collections in this service`：

    <img alt="wis2box-api-collections.png" src="/../assets/img/wis2box-api-collections.png" width="600">

    当前可用的集合包括：

    - Stations
    - Data notifications
    - Discovery metadata


!!! question

    已发布了多少条数据通知？

??? success "点击查看答案"

    点击 "Data notifications"，然后点击 `Browse through the items of "Data Notifications"`。 
    
    您会注意到页面显示 "No items"，因为尚未发布任何数据通知。

## wis2box webapp

打开一个网页浏览器，访问页面 `http://YOUR-HOST/wis2box-webapp`。

您将看到一个弹窗，要求输入用户名和密码。使用默认用户名 `wis2box-user` 和在 `wis2box.env` 文件中定义的 `WIS2BOX_WEBAPP_PASSWORD`，然后点击 "Sign in"：

!!! note 

    检查您的 wis2box.env 文件以获取 WIS2BOX_WEBAPP_PASSWORD 的值。您可以使用以下命令检查此环境变量的值：

    ```{.copy}
    cat ~/wis2box/wis2box.env | grep WIS2BOX_WEBAPP_PASSWORD
    ```

登录后，将鼠标移到左侧菜单以查看 wis2box Web 应用程序中的可用选项：

<img alt="wis2box-webapp-menu.png" src="/../assets/img/wis2box-webapp-menu.png" width="400">

这是 wis2box Web 应用程序，您可以通过它与您的 wis2box 进行交互：

- 创建和管理数据集
- 更新/查看站点元数据
- 使用 FM-12 synop 表单上传手动观测数据
- 监控在您的 wis2box-broker 上发布的通知

我们将在后续课程中使用此 Web 应用程序。

## wis2box-broker

在您的计算机上打开 MQTT Explorer，并准备一个新连接以连接到您的代理（通过 **wis2box-broker** 容器运行）。

点击 `+` 添加新连接：

<img alt="mqtt-explorer-new-connection.png" src="/../assets/img/mqtt-explorer-new-connection.png" width="300">

您可以点击 'ADVANCED' 按钮，并验证您是否订阅了以下主题：

- `#`
- `$SYS/#`

<img alt="mqtt-explorer-topics.png" src="/../assets/img/mqtt-explorer-topics.png" width="550">

!!! note

    `#` 主题是一个通配符订阅，它将订阅代理上发布的所有主题。

    发布在 `$SYS` 主题下的消息是由 mosquitto 服务本身发布的系统消息。

使用以下连接详细信息，确保将 `<your-host>` 的值替换为您的主机名，将 `<WIS2BOX_BROKER_PASSWORD>` 的值替换为您 `wis2box.env` 文件中的值：

- **Protocol: mqtt://**
- **Host: `<your-host>`**
- **Port: 1883**
- **Username: wis2box**
- **Password: `<WIS2BOX_BROKER_PASSWORD>`**

!!! note 

    您可以检查您的 wis2box.env 文件以获取 WIS2BOX_BROKER_PASSWORD 的值。您可以使用以下命令检查此环境变量的值：

    ```{.copy}
    cat ~/wis2box/wis2box.env | grep WIS2BOX_BROKER_PASSWORD
    ```

    请注意，这是您的 **内部** 代理密码，Global Broker 将使用不同的（只读）凭据订阅您的代理。切勿与他人共享此密码。

确保点击 "SAVE" 保存您的连接详细信息。

然后点击 "CONNECT" 连接到您的 **wis2box-broker**。

<img alt="mqtt-explorer-wis2box-broker.png" src="/../assets/img/mqtt-explorer-wis2box-broker.png" width="600">

一旦连接成功，验证您的代理是否在 `$SYS` 主题下发布了内部 mosquitto 统计信息：

<img alt="mqtt-explorer-sys-topic.png" src="/../assets/img/mqtt-explorer-sys-topic.png" width="400">

保持 MQTT Explorer 打开状态，因为我们将使用它来监控代理上发布的消息。

## 结论

!!! success "恭喜！"
    在本次实践课程中，您学习了如何：

    - 运行 `wis2box-create-config.py` 脚本以创建初始配置
    - 启动 wis2box 并检查其组件的状态
    - 在浏览器中访问 wis2box-webapp 和 wis2box-API
    - 使用 MQTT Explorer 连接到学生虚拟机上的 MQTT 代理
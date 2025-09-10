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

    当前的培训材料基于 wis2box-release 1.1.0。

    如果您在本地培训课程之外运行本次培训，请参阅 [accessing-your-student-vm](./accessing-your-student-vm.md) 了解如何下载和安装 wis2box 软件栈的说明。

## 准备工作

使用您的用户名和密码登录到指定的虚拟机，并确保您处于 `wis2box` 目录中：

```bash
cd ~/wis2box
```

## 创建初始配置

wis2box 的初始配置需要以下内容：

- 一个包含配置参数的环境文件 `wis2box.env`
- 主机上的一个目录，用于在主机和 wis2box 容器之间共享，该目录由环境变量 `WIS2BOX_HOST_DATADIR` 定义

可以使用 `wis2box-create-config.py` 脚本来创建 wis2box 的初始配置。

该脚本会向您提出一系列问题，以帮助设置配置。

在脚本完成后，您可以查看并更新配置文件。

运行以下命令启动脚本：

```bash
python3 wis2box-create-config.py
```

### wis2box-host-data 目录

脚本会要求您输入用于 `WIS2BOX_HOST_DATADIR` 环境变量的目录。

请注意，您需要定义该目录的完整路径。

例如，如果您的用户名是 `username`，则目录的完整路径为 `/home/username/wis2box-data`：

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

接下来，您将被要求输入 wis2box 的 URL。这是用于访问 wis2box Web 应用程序、API 和 UI 的 URL。

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

当提示输入 `WIS2BOX_WEBAPP_PASSWORD`、`WIS2BOX_STORAGE_PASSWORD` 和 `WIS2BOX_BROKER_PASSWORD` 时，您可以选择随机生成密码，也可以自行定义。

无需担心记住这些密码，它们会存储在 `wis2box.env` 文件中，该文件位于您的 wis2box 目录中。

### 检查 `wis2box.env`

脚本完成后，检查当前目录中的 `wis2box.env` 文件内容：

```bash
cat ~/wis2box/wis2box.env
```

或者通过 WinSCP 检查文件内容。

!!! question

    `wis2box.env` 文件中 WISBOX_BASEMAP_URL 的值是什么？

??? success "点击查看答案"

    WIS2BOX_BASEMAP_URL 的默认值是 `https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png`。

    该 URL 指向 OpenStreetMap 瓦片服务器。如果您想使用其他地图提供商，可以将此 URL 更改为指向其他瓦片服务器的地址。

!!! question 

    `wis2box.env` 文件中 WIS2BOX_STORAGE_DATA_RETENTION_DAYS 环境变量的值是什么？

??? success "点击查看答案"

    WIS2BOX_STORAGE_DATA_RETENTION_DAYS 的默认值是 30 天。如果需要，您可以将此值更改为其他天数。

    wis2box-management 容器每天会运行一个 cronjob，删除 `wis2box-public` 存储桶和 API 后端中超过 WIS2BOX_STORAGE_DATA_RETENTION_DAYS 定义天数的数据：

    ```{.copy}
    0 0 * * * su wis2box -c "wis2box data clean --days=$WIS2BOX_STORAGE_DATA_RETENTION_DAYS"
    ```

!!! note

    `wis2box.env` 文件包含定义 wis2box 配置的环境变量。有关更多信息，请参考 [wis2box-documentation](https://docs.wis2box.wis.wmo.int/en/latest/reference/configuration.html)。

    除非您确定更改内容，否则不要编辑 `wis2box.env` 文件。不正确的更改可能会导致 wis2box 无法正常工作。

    请勿与他人共享 `wis2box.env` 文件的内容，因为其中包含密码等敏感信息。

## 启动 wis2box

确保您位于包含 wis2box 软件栈定义文件的目录中：

```{.copy}
cd ~/wis2box
```

使用以下命令启动 wis2box：

```{.copy}
python3 wis2box-ctl.py start
```

首次运行此命令时，您将看到以下输出：

```
No docker-compose.images-*.yml files found, creating one
Current version=Undefined, latest version=1.1.0
Would you like to update ? (y/n/exit)
```

选择 ``y``，脚本将创建文件 ``docker-compose.images-1.1.0.yml``，下载所需的 Docker 镜像并启动服务。

根据您的网络连接速度，下载镜像可能需要一些时间。此步骤仅在首次启动 wis2box 时需要完成。

使用以下命令检查状态：

```{.copy}
python3 wis2box-ctl.py status
```

重复运行此命令，直到所有服务都启动并运行。

!!! note "wis2box 和 Docker"
    wis2box 作为一组由 docker-compose 管理的 Docker 容器运行。
    
    服务定义在 `~/wis2box/` 目录中的各种 `docker-compose*.yml` 文件中。
    
    Python 脚本 `wis2box-ctl.py` 用于运行控制 wis2box 服务的底层 Docker Compose 命令。

    您无需了解 Docker 容器的详细信息即可运行 wis2box 软件栈，但您可以查看 `docker-compose*.yml` 文件，了解服务的定义。如果您有兴趣了解更多关于 Docker 的信息，可以参考 [Docker 文档](https://docs.docker.com/)。

要登录到 wis2box-management 容器，请使用以下命令：

```{.copy}
python3 wis2box-ctl.py login
```

登录后，您的提示符将发生变化，表明您现在位于 wis2box-management 容器中：

```{bash}
root@025381da3c40:/home/wis2box#
```

在 wis2box-management 容器中，您可以运行各种命令来管理您的 wis2box，例如：

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
nginx                     Up About a minute         nginx:alpine
wis2box-auth              Up About a minute         ghcr.io/world-meteorological-organization/wis2box-auth:1.1.0
mqtt_metrics_collector    Up About a minute         ghcr.io/world-meteorological-organization/wis2box-mqtt-metrics-collector:1.1.0
wis2box-ui                Up 3 minutes              ghcr.io/world-meteorological-organization/wis2box-ui:1.1.0
wis2box-management        Up About a minute         ghcr.io/world-meteorological-organization/wis2box-management:1.1.1
wis2box-minio             Up 4 minutes (healthy)    minio/minio:RELEASE.2024-08-03T04-33-23Z-cpuv1
wis2box-api               Up 3 minutes (healthy)    ghcr.io/world-meteorological-organization/wis2box-api:1.1.0
wis2box-webapp            Up 4 minutes (healthy)    ghcr.io/world-meteorological-organization/wis2box-webapp:1.1.0
elasticsearch             Up 4 minutes (healthy)    docker.elastic.co/elasticsearch/elasticsearch:8.6.2
mosquitto                 Up 4 minutes              ghcr.io/world-meteorological-organization/wis2box-broker:1.1.0
grafana                   Up 4 minutes              grafana/grafana-oss:9.0.3
elasticsearch-exporter    Up 4 minutes              quay.io/prometheuscommunity/elasticsearch-exporter:latest
wis2downloader            Up 4 minutes (healthy)    ghcr.io/wmo-im/wis2downloader:v0.3.2
prometheus                Up 4 minutes              prom/prometheus:v2.37.0
loki                      Up 4 minutes              grafana/loki:2.4.1

```

这些容器是 wis2box 软件栈的一部分，提供运行 wis2box 所需的各种服务。

运行以下命令查看主机上运行的 Docker 卷：

```{.copy}
docker volume ls
```

您应该会看到以下卷：

- wis2box_project_auth-data
- wis2box_project_es-data
- wis2box_project_htpasswd
- wis2box_project_minio-data
- wis2box_project_prometheus-data
- wis2box_project_loki-data
- wis2box_project_mosquitto-config

以及一些由各种容器使用的匿名卷。

以 `wis2box_project_` 开头的卷用于存储 wis2box 软件栈中各服务的持久化数据。

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

打开一个浏览器，访问页面 `http://YOUR-HOST/wis2box-webapp`。

您会看到一个弹窗，要求输入用户名和密码。使用默认用户名 `wis2box-user` 和在 `wis2box.env` 文件中定义的 `WIS2BOX_WEBAPP_PASSWORD`，然后点击 "Sign in"：

!!! note 

    检查您的 wis2box.env 文件以获取 WIS2BOX_WEBAPP_PASSWORD 的值。您可以使用以下命令检查此环境变量的值：

    ```{.copy}
    cat ~/wis2box/wis2box.env | grep WIS2BOX_WEBAPP_PASSWORD
    ```

登录后，将鼠标移动到左侧菜单以查看 wis2box Web 应用程序中的可用选项：

<img alt="wis2box-webapp-menu.png" src="/../assets/img/wis2box-webapp-menu.png" width="400">

这是 wis2box Web 应用程序，您可以通过它与您的 wis2box 交互：

- 创建和管理数据集
- 更新/查看您的站点元数据
- 使用 FM-12 synop 表单上传手动观测数据
- 监控在您的 wis2box-broker 上发布的通知

我们将在后续课程中使用此 Web 应用程序。

## wis2box-broker

在您的计算机上打开 MQTT Explorer，并准备一个新连接以连接到您的 broker（通过 **wis2box-broker** 容器运行）。

点击 `+` 添加一个新连接：

<img alt="mqtt-explorer-new-connection.png" src="/../assets/img/mqtt-explorer-new-connection.png" width="300">

您可以点击 'ADVANCED' 按钮，验证您已订阅以下主题：

- `#`
- `$SYS/#`

<img alt="mqtt-explorer-topics.png" src="/../assets/img/mqtt-explorer-topics.png" width="550">

!!! note

    `#` 主题是一个通配符订阅，将订阅 broker 上发布的所有主题。

    发布在 `$SYS` 主题下的消息是由 mosquitto 服务本身发布的系统消息。

使用以下连接详细信息，确保将 `<your-host>` 替换为您的主机名，将 `<WIS2BOX_BROKER_PASSWORD>` 替换为 `wis2box.env` 文件中的值：

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

    请注意，这是您的 **内部** broker 密码，Global Broker 将使用不同的（只读）凭据订阅您的 broker。切勿与任何人共享此密码。

确保点击 "SAVE" 保存您的连接详细信息。

然后点击 "CONNECT" 连接到您的 **wis2box-broker**。

<img alt="mqtt-explorer-wis2box-broker.png" src="/../assets/img/mqtt-explorer-wis2box-broker.png" width="600">

连接后，验证您的 broker 是否正在 `$SYS` 主题下发布内部 mosquitto 统计信息：

<img alt="mqtt-explorer-sys-topic.png" src="/../assets/img/mqtt-explorer-sys-topic.png" width="400">

保持 MQTT Explorer 打开状态，我们将使用它来监控 broker 上发布的消息。

## 总结

!!! success "恭喜！"
    在本次实践课程中，您学习了如何：

    - 运行 `wis2box-create-config.py` 脚本以创建初始配置
    - 启动 wis2box 并检查其组件状态
    - 在浏览器中访问 wis2box-webapp 和 wis2box-API
    - 使用 MQTT Explorer 连接到学生虚拟机上的 MQTT broker
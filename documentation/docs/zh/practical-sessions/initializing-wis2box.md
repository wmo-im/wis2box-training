---
title: 初始化 wis2box
---

# 初始化 wis2box

!!! abstract "学习成果"

    在本实践课程结束时，您将能够：

    - 运行 `wis2box-create-config.py` 脚本创建初始配置
    - 启动 wis2box 并检查其组件的状态
    - 查看 **wis2box-api** 的内容
    - 访问 **wis2box-webapp**
    - 使用 MQTT Explorer 连接到本地的 **wis2box-broker**

!!! note

    当前的培训材料基于 wis2box-release 1.0.0。
    
    如果您在本地培训会议之外运行此培训，请参阅 [accessing-your-student-vm](./accessing-your-student-vm.md) 了解如何下载和安装 wis2box 软件栈的指南。

## 准备工作

使用您的用户名和密码登录到指定的 VM，并确保您位于 `wis2box` 目录中：

```bash
cd ~/wis2box
```

## 创建初始配置

wis2box 的初始配置需要：

- 一个包含配置参数的环境文件 `wis2box.env`
- 由环境变量 `WIS2BOX_HOST_DATADIR` 定义的，用于主机和 wis2box 容器之间共享的主机上的目录

可以使用 `wis2box-create-config.py` 脚本来创建您的 wis2box 的初始配置。

它将询问您一系列问题以帮助设置您的配置。

脚本完成后，您将能够审查和更新配置文件。

按以下方式运行脚本：

```bash
python3 wis2box-create-config.py
```

### wis2box-host-data 目录

脚本将要求您输入用于 `WIS2BOX_HOST_DATADIR` 环境变量的目录。

请注意，您需要定义此目录的完整路径。

例如，如果您的用户名是 `username`，目录的完整路径是 `/home/username/wis2box-data`：

```{.copy}
username@student-vm-username:~/wis2box$ python3 wis2box-create-config.py
请输入用于 WIS2BOX_HOST_DATADIR 的目录：
/home/username/wis2box-data
将设置用于 WIS2BOX_HOST_DATADIR 的目录为：
    /home/username/wis2box-data
这样设置是否正确？(y/n/exit)
y
目录 /home/username/wis2box-data 已创建。
```

### wis2box URL

接下来，您将被要求输入您的 wis2box 的 URL。这是用来访问 wis2box 网页应用、API 和 UI 的 URL。

请使用 `http://<your-hostname-or-ip>` 作为 URL。

```{.copy}
请输入 wis2box 的 URL：
 对于本地测试，URL 是 http://localhost
 若要启用远程访问，URL 应指向托管 wis2box 的服务器的公共 IP 地址或域名。
http://username.wis2.training
将设置 wis2box 的 URL 为：
  http://username.wis2.training
这样设置是否正确？(y/n/exit)
```

### WEBAPP、STORAGE 和 BROKER 密码

在提示输入 `WIS2BOX_WEBAPP_PASSWORD`、`WIS2BOX_STORAGE_PASSWORD`、`WIS2BOX_BROKER_PASSWORD` 时，您可以选择生成随机密码，并定义自己的密码。

不用担心记住这些密码，它们将被存储在您的 wis2box 目录中的 `wis2box.env` 文件中。

### 审查 `wis2box.env`

脚本完成后检查当前目录中 `wis2box.env` 文件的内容：

```bash
cat ~/wis2box/wis2box.env
```

或通过 WinSCP 检查文件内容。

!!! question

    wis2box.env 文件中 WISBOX_BASEMAP_URL 的值是什么？

??? success "点击以显示答案"

    WIS2BOX_BASEMAP_URL 的默认值是 `https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png`。

    此 URL 指向 OpenStreetMap 瓦片服务器。如果您想使用不同的地图提供商，可以将此 URL 更改为指向不同的瓦片服务器。

!!! question 

    wis2box.env 文件中 WIS2BOX_STORAGE_DATA_RETENTION_DAYS 环境变量的值是多少？

??? success "点击以显示答案"

    WIS2BOX_STORAGE_DATA_RETENTION_DAYS 的默认值是 30 天。如果您希望，可以将此值更改为不同的天数。
    
    wis2box-management 容器每天运行一次 cronjob，从 `wis2box-public` 存储桶和 API 后端删除超过 WIS2BOX_STORAGE_DATA_RETENTION_DAYS 定义的天数的数据：
    
    ```{.copy}
    0 0 * * * su wis2box -c "wis2box data clean --days=$WIS2BOX_STORAGE_DATA_RETENTION_DAYS"
    ```

!!! note

    `wis2box.env` 文件包含定义您的 wis2box 配置的环境变量。有关更多信息，请参阅 [wis2box-documentation](https://docs.wis2box.wis.wmo.int/en/latest/reference/configuration.html)。

    除非您确定所做的更改，请不要编辑 `wis2box.env` 文件。不正确的更改可能导致您的 wis2box 停止工作。

    不要与任何人分享您的 `wis2box.env` 文件的内容，因为它包含敏感信息，如密码。

## 启动 wis2box

确保您位于包含 wis2box 软件栈定义文件的目录中：

```{.copy}
cd ~/wis2box
```

使用以下命令启动 wis2box：

```{.copy}
python3 wis2box-ctl.py start
```

当您第一次运行此命令时，您将看到以下输出：

```
未找到 docker-compose.images-*.yml 文件，正在创建一个
当前版本=Undefined，最新版本=1.0.0
您想要更新吗？ (y/n/exit)
```

选择 ``y``，脚本将创建文件 ``docker-compose.images-1.0.0.yml``，下载所需的 Docker 镜像并启动服务。

下载镜像可能需要一些时间，这取决于您的互联网连接速度。这一步只在您第一次启动 wis2box 时需要。

使用以下命令检查状态：

```{.copy}
python3 wis2box-ctl.py status
```

重复此命令直到所有服务都在运行。

!!! note "wis2box 和 Docker"
    wis2box 作为一组由 docker-compose 管理的 Docker 容器运行。
    
    服务在各种 `docker-compose*.yml` 中定义，这些文件可以在 `~/wis2box/` 目录中找到。
    
    Python 脚本 `wis2box-ctl.py` 用于运行控制 wis2box 服务的底层 Docker Compose 命令。

    您不需要了解 Docker 容器的细节来运行 wis2box 软件栈，但您可以查看 `docker-compose*.yml` 和文件以了解服务是如何定义的。如果您有兴趣了解更多关于 Docker 的信息，可以在 [Docker documentation](https://docs.docker.com/) 中找到更多信息。

要登录到 wis2box-management 容器，请使用以下命令：

```{.copy}
python3 wis2box-ctl.py login
```

在 wis2box-management 容器内部，您可以运行各种命令来管理您的 wis2box，例如：

- `wis2box auth add-token --path processes/wis2box` : 为 `processes/wis2box` 端点创建授权令牌
- `wis2box data clean --days=<number-of-days>` : 清理 `wis2box-public` 存储桶中超过一定天数的数据

要退出容器并返回到主机，请使用以下命令：

```{.copy}
exit
```

运行以下命令查看您的主机上运行的 docker 容器：

```{.copy}
docker ps
```

您应该看到以下容器在运行：

- wis2box-management
- wis2box-api
- wis2box-minio
- wis2box-webapp
- wis2box-auth
- wis2box-ui
- wis2downloader
- elasticsearch
- elasticsearch-exporter
- nginx
- mosquitto
- prometheus
- grafana
- loki

这些容器是 wis2box 软件栈的一部分，提供运行 wis2box 所需的各种服务。

运行以下命令查看您的主机上运行的 docker 卷：

```{.copy}
docker volume ls
```

您应该看到以下卷：

- wis2box_project_auth-data
- wis2box_project_es-data

- wis2box_project_htpasswd
- wis2box_project_minio-data
- wis2box_project_prometheus-data
- wis2box_project_loki-data
- wis2box_project_mosquitto-config

以及一些由各种容器使用的匿名卷。

以 `wis2box_project_` 开头的卷用于存储 wis2box 软件堆栈中各种服务的持久数据。

## wis2box API

wis2box 包含一个 API（应用程序编程接口），提供数据访问和用于交互式可视化、数据转换和发布的流程。

打开一个新标签页并导航到页面 `http://YOUR-HOST/oapi`。

<img alt="wis2box-api.png" src="/../assets/img/wis2box-api.png" width="800">

这是 wis2box API 的登录页面（通过 **wis2box-api** 容器运行）。

!!! question
     
     当前有哪些集合可用？

??? success "点击以显示答案"
    
    要查看通过 API 当前可用的集合，请点击 `查看此服务中的集合`：

    <img alt="wis2box-api-collections.png" src="/../assets/img/wis2box-api-collections.png" width="600">

    当前可用的集合包括：

    - 站点
    - 数据通知
    - 发现元数据


!!! question

    已发布多少数据通知？

??? success "点击以显示答案"

    点击“数据通知”，然后点击 `浏览“数据通知”的项目`。
    
    您将注意到页面显示“无项目”，因为尚未发布任何数据通知。

## wis2box webapp

在浏览器中打开 `http://YOUR-HOST/wis2box-webapp`。

您将看到一个弹出窗口，要求您输入用户名和密码。使用默认用户名 `wis2box-user` 和 `wis2box.env` 文件中定义的 `WIS2BOX_WEBAPP_PASSWORD`，然后点击“登录”：

!!! note 

    检查您的 wis2box.env 以获取 WIS2BOX_WEBAPP_PASSWORD 的值。您可以使用以下命令检查此环境变量的值：

    ```{.copy}
    cat ~/wis2box/wis2box.env | grep WIS2BOX_WEBAPP_PASSWORD
    ```

登录后，将鼠标移动到左侧菜单以查看 wis2box web 应用中的可用选项：

<img alt="wis2box-webapp-menu.png" src="/../assets/img/wis2box-webapp-menu.png" width="400">

这是 wis2box web 应用，使您能够与您的 wis2box 互动：

- 创建和管理数据集
- 更新/审查您的站点元数据
- 使用 FM-12 synop 表格上传手动观测数据
- 监控在您的 wis2box-broker 上发布的通知

我们将在后续会议中使用此 web 应用。

## wis2box-broker

在您的计算机上打开 MQTT Explorer 并准备一个新连接以连接到您的 broker（通过 **wis2box-broker** 容器运行）。

点击 `+` 添加新连接：

<img alt="mqtt-explorer-new-connection.png" src="/../assets/img/mqtt-explorer-new-connection.png" width="300">

您可以点击 'ADVANCED' 按钮并验证您已订阅以下主题：

- `#`
- `$SYS/#`

<img alt="mqtt-explorer-topics.png" src="/../assets/img/mqtt-explorer-topics.png" width="550">

!!! note

    主题 `#` 是一个通配符订阅，将订阅在 broker 上发布的所有主题。

    在 `$SYS` 主题下发布的消息是 mosquitto 服务本身发布的系统消息。

使用以下连接详情，确保将 `<your-host>` 的值替换为您的主机名，将 `<WIS2BOX_BROKER_PASSWORD>` 的值替换为您的 `wis2box.env` 文件中的值：

- **Protocol: mqtt://**
- **Host: `<your-host>`**
- **Port: 1883**
- **Username: wis2box**
- **Password: `<WIS2BOX_BROKER_PASSWORD>`**

!!! note 

    您可以检查您的 wis2box.env 以获取 WIS2BOX_BROKER_PASSWORD 的值。您可以使用以下命令检查此环境变量的值：

    ```{.copy}
    cat ~/wis2box/wis2box.env | grep WIS2BOX_BROKER_PASSWORD
    ```

    请注意，这是您的**内部** broker 密码，Global Broker 将使用不同的（只读）凭据来订阅您的 broker。切勿与任何人分享此密码。

确保点击“保存”以存储您的连接详情。

然后点击“连接”以连接到您的 **wis2box-broker**。

<img alt="mqtt-explorer-wis2box-broker.png" src="/../assets/img/mqtt-explorer-wis2box-broker.png" width="600">

连接后，验证您的 broker 在 `$SYS` 主题下发布的内部 mosquitto 统计信息：

<img alt="mqtt-explorer-sys-topic.png" src="/../assets/img/mqtt-explorer-sys-topic.png" width="400">

保持 MQTT Explorer 打开，因为我们将使用它来监控在 broker 上发布的消息。

## 结论

!!! success "恭喜！"
    在这个实践课程中，您学习了如何：

    - 运行 `wis2box-create-config.py` 脚本以创建初始配置
    - 启动 wis2box 并检查其组件的状态
    - 在浏览器中访问 wis2box-webapp 和 wis2box-API
    - 使用 MQTT Explorer 在您的学生 VM 上连接到 MQTT broker
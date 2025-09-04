---
title: 发布数据的摄取
---

# 发布数据的摄取

!!! abstract "学习目标"

    在本次实践课程结束时，您将能够：
    
    - 通过使用 MinIO 网页界面、SFTP 或 Python 脚本上传数据，触发 wis2box 工作流。
    - 访问 Grafana 仪表板以监控数据摄取状态并查看您的 wis2box 实例的日志。
    - 使用 MQTT Explorer 查看由您的 wis2box 发布的 WIS2 数据通知。

## 简介

在 WIS2 中，数据通过 WIS2 数据通知实时共享，这些通知包含一个“规范”链接，可用于下载数据。

要使用 wis2box 软件在 WIS2 Node 中触发数据工作流，必须将数据上传到 **MinIO** 中的 **wis2box-incoming** 存储桶，这将启动 wis2box 工作流。此过程会通过 WIS2 数据通知发布数据。根据您在 wis2box 实例中配置的数据映射，数据可能会在发布之前转换为 BUFR 格式。

在本次练习中，我们将使用示例数据文件触发 wis2box 工作流，并为您在之前实践课程中配置的数据集**发布 WIS2 数据通知**。

在练习过程中，我们将使用 **Grafana 仪表板** 和 **MQTT Explorer** 监控数据摄取的状态。Grafana 仪表板使用来自 Prometheus 和 Loki 的数据显示您的 wis2box 状态，而 MQTT Explorer 允许您查看由您的 wis2box 实例发布的 WIS2 数据通知。

请注意，根据数据集中预先配置的数据映射，wis2box 会在将示例数据发布到 MQTT broker 之前将其转换为 BUFR 格式。在本次练习中，我们将重点关注将数据上传到您的 wis2box 实例的不同方法，并验证摄取和发布是否成功。数据转换将在 [数据转换工具](./data-conversion-tools.md) 实践课程中进一步讲解。

## 准备工作

本节使用在 [配置 wis2box 数据集](./configuring-wis2box-datasets.md) 实践课程中创建的 "surface-based-observations/synop" 和 "other" 数据集。

此外，还需要了解如何在 **wis2box-webapp** 中配置站点元数据，如 [配置站点元数据](./configuring-station-metadata.md) 实践课程中所述。

确保您可以使用 SSH 客户端（例如 PuTTY）登录到您的学生虚拟机。

确保 wis2box 正在运行：

```bash
cd ~/wis2box/
python3 wis2box-ctl.py start
python3 wis2box-ctl.py status
```

确保 MQTT Explorer 正在运行并使用公共凭据 `everyone/everyone` 连接到您的实例，并订阅主题 `origin/a/wis2/#`。

确保您已打开一个 Web 浏览器，并通过导航到 `http://YOUR-HOST:3000` 访问您的实例的 Grafana 仪表板。

### 准备示例数据

将目录 `exercise-materials/data-ingest-exercises` 复制到您在 `wis2box.env` 文件中定义的 `WIS2BOX_HOST_DATADIR` 目录中：

```bash
cp -r ~/exercise-materials/data-ingest-exercises ~/wis2box-data/
```

!!! note
    `WIS2BOX_HOST_DATADIR` 由 `wis2box` 目录中 `docker-compose.yml` 文件挂载为 wis2box-management 容器内的 `/data/wis2box/`。
    
    这允许您在主机和容器之间共享数据。

## 使用 MinIO 界面摄取数据

首先，我们将使用 MinIO 网页界面，该界面允许您通过 Web 浏览器下载和上传数据到 MinIO。

### 访问 MinIO 界面

打开 MinIO 网页界面（通常可通过 http://your-localhost:9001 访问）。

WIS2BOX_STORAGE_USERNAME 和 WIS2BOX_STORAGE_PASSWORD 凭据可以在 wis2box.env 文件中找到。

### 使用 Universal 插件摄取和发布

从以下链接下载本次练习的通用示例数据到本地环境：
[sample-data-for-universal-plugin](../sample-data/Z_NAFP_C_BABJ_20250818000000_P_CMA-GEPS-GLB-024.grib2)

选择存储桶 wis2box-incoming 并点击“Create new path”。目录名称必须与您在 [配置 wis2box 数据集](./configuring-wis2box-datasets.md) 实践课程中创建的 "other" 数据集的元数据标识符相对应。因此，在本例中，请创建目录：

```bash
urn:wmo:md:nl-knmi-test:customized-geps-dataset-wis2-training
```

进入新创建的目录，点击“Upload”，并选择您之前下载到本地的 [sample-data-for-universal-plugin](../sample-data/Z_NAFP_C_BABJ_20250818000000_P_CMA-GEPS-GLB-024.grib2)。

上传后，使用 MQTT Explorer 检查数据是否成功发布。

<img alt="Metadata Editor: title, description, keywords" src="/../assets/img/mqtt-explorer-wis2-notification-geps-sample.png" width="800">

!!! question "将文件重命名为 sample-geps-data.grib2"

    使用网页界面将重命名的文件上传到 MinIO 中与之前文件相同的路径。

    重命名的文件会成功发布吗？为什么？

??? success "点击查看答案"

    不会，因为当您将数据名称更改为 "sample-geps-data.grib2" 时，它将不符合正则表达式规则。

    <img alt="Metadata Editor: title, description, keywords" src="/../assets/img/mqtt-explorer-wis2-notification-geps-regex-error.png" width="800">
    
    上传数据时，文件名必须符合由正则表达式定义的命名约定：

    ```bash
    ^.*?_(\d{8}).*?\..*$
    ```

    此模式要求每个文件名包含：

    一个下划线 (_)，紧接着是一个格式为 YYYYMMDD 的 8 位数字日期字符串（例如，20250904）。

    例如，以下名称是有效的：

    1. *Z_NAFP_C_BABJ_20250904_P_CMA-GEPS-GLB-024.grib2*

    2. *forecast_20250904.grib2*

    3. *sample-geps_20250101_data.grib2*

    像 sample-geps-data.grib2 这样的名称将不被接受，因为它不包含所需的 8 位数字日期。

!!! question "将文件扩展名从 .grib2 更改为 .bufr4（不更改文件的内部内容）"

    使用网页界面将重命名的文件上传到 MinIO 中与之前文件相同的路径。

    重命名的文件会成功发布吗？为什么？

??? success "点击查看答案"

    不会，因为当您将数据格式从 "grib2" 更改为 "bufr4" 时，它将不符合您在创建数据集时定义的文件扩展名规则。

    <img alt="Metadata Editor: title, description, keywords" src="/../assets/img/mqtt-explorer-wis2-notification-geps-file-extension-error.png" width="800">
    
    使用 Universal 插件上传数据时，文件必须具有与数据集配置中定义的文件扩展名一致的正确扩展名。此要求确保摄取过程能够正确识别和处理文件格式。例如，如果数据集配置为 grib2 文件，则只有以 .grib2 结尾的文件会被接受。使用不正确的扩展名（例如 .txt 或 .bin）将导致文件被拒绝且无法发布。

!!! question "使用 MinIO 网页界面重新上传数据"

    在浏览器中打开 MinIO 网页界面并浏览到 `wis2box-incoming` 存储桶。您将看到之前练习中上传的文件 `Z_NAFP_C_BABJ_20250818000000_P_CMA-GEPS-GLB-024.grib2`。

    点击文件，您将看到下载选项：

    <img alt="minio-wis2box-incoming-dataset-folder" src="/../assets/img/minio-download.png" width="800">

    您可以下载此文件并将其重新上传到 MinIO 中的相同路径，以重新触发 wis2box 工作流。

    检查 Grafana 仪表板和 MQTT Explorer，查看数据是否成功摄取和发布。

??? success "点击查看答案"

    您将看到一条消息，表明 wis2box 已经发布了此数据：

    ```bash
    ERROR - Data already published for Z_NAFP_C_BABJ_20250818000000_P_CMA-GEPS-GLB-024-grib2; not publishing
    ``` 
    
    这表明数据工作流已被触发，但数据未重新发布。wis2box 不会重复发布相同的数据。

### 使用 synop2bufr-plugin 摄取和发布数据

下载练习所需的 synop 示例数据 [synop_202502040900.txt](../sample-data/synop_202502040900.txt) 到本地环境：

选择存储桶 `wis2box-incoming` 并点击“Create new path”。目录名称必须与您在 [Configuring Datasets in wis2box](./configuring-wis2box-datasets.md) 实践环节中创建的 "surface-based-observations/synop" 数据集的元数据标识符一致。因此，在本例中，请创建以下目录：

```bash
urn:wmo:md:nl-knmi-test:synop-dataset-wis2-training
```

进入新创建的目录，点击“Upload”，选择之前下载到本地的 [synop_202502040900.txt](../sample-data/synop_202502040900.txt) 文件并上传。

!!! question "您是否收到一条新通知，表明数据已发布？为什么？"

??? success "点击查看答案"

    没有。在 Grafana 仪表板中，您会看到一条错误信息，表明数据摄取失败：

    <img alt="grafana_data_ingest" src="/../assets/img/grafana_data-ingest-error.png" width="800"> 

    使用默认 synop 插件（支持 CSV、TXT 和 BUFR SYNOP 数据）的 synop 数据集模板时，每条记录必须包含有效的站点标识符。如果站点未在您的 `wis2box` 实例中定义，数据摄取将失败。因此，您必须先添加站点，然后再发布 SYNOP 数据。

    现在，让我们为本次练习添加一个测试站点。

    使用 `wis2box-webapp` 中的站点编辑器，将 WIGOS 标识符为 `0-20000-0-64400` 的站点添加到您的 `wis2box` 实例中。

    从 OSCAR 检索站点信息：

    <img alt="oscar-station" src="/../assets/img/webapp-test-station-oscar-search.png" width="600">

    将站点添加到您为 "../surface-based-observations/synop" 数据集创建的发布路径中，并使用您的身份验证令牌保存更改：

    <img alt="webapp-test-station" src="/../assets/img/webapp-test-station-save.png" width="800">

    请注意，您可以在实践环节结束后从数据集中移除此站点。

完成站点元数据配置后，使用 MQTT Explorer 检查数据是否成功发布。如果您看到以下通知，则说明您已成功发布 synop 示例数据。

<img alt="webapp-test-station" src="/../assets/img/mqtt-explorer-wis2box-notification-synop-sample.png" width="800">

## 使用 Python 摄取数据（可选）

在本次练习中，我们将使用 MinIO 的 Python 客户端将数据复制到 MinIO。

MinIO 提供了一个 Python 客户端，可以通过以下命令安装：

```bash
pip3 install minio
```

在您的学生虚拟机上，Python 的 `minio` 包已经安装。

在 `exercise-materials/data-ingest-exercises` 目录中，您会找到一个示例脚本 `copy_file_to_incoming.py`，可用于将文件复制到 MinIO。

尝试运行脚本，将示例数据文件 `synop_202501030900.txt` 复制到 MinIO 的 `wis2box-incoming` 存储桶中：

```bash
cd ~/wis2box-data/data-ingest-exercises
python3 copy_file_to_incoming.py synop_202501030900.txt
```

!!! note

    您会收到一个错误提示，因为脚本尚未配置为访问您的 `wis2box` 上的 MinIO 端点。

脚本需要知道访问 `wis2box` 上 MinIO 的正确端点。如果 `wis2box` 运行在您的主机上，MinIO 端点可通过 `http://YOUR-HOST:9000` 访问。脚本还需要更新您的存储密码以及 MinIO 存储桶中存储数据的路径。

!!! question "更新脚本并摄取 CSV 数据"
    
    编辑脚本 `copy_file_to_incoming.py` 以解决错误，可以使用以下方法之一：
    - 从命令行：使用 `nano` 或 `vim` 文本编辑器编辑脚本。
    - 使用 WinSCP：启动一个新的连接，选择文件协议 `SCP`，并使用与 SSH 客户端相同的凭据。导航到目录 `wis2box-data/data-ingest-exercises` 并使用内置文本编辑器编辑 `copy_file_to_incoming.py`。

    确保您：

    - 定义主机的正确 MinIO 端点。
    - 提供 MinIO 实例的正确存储密码。
    - 提供 MinIO 存储桶中存储数据的正确路径。

    重新运行脚本，将示例数据文件 `synop_202501030900.txt` 摄取到 MinIO：

    ```bash
    python3 ~/wis2box-data/ ~/wis2box-data/synop_202501030900.txt
    ```

    确保错误已解决。

当您成功运行脚本后，您会看到一条消息，表明文件已复制到 MinIO，您还应在 MQTT Explorer 中看到您的 `wis2box` 实例发布的数据通知。

您还可以检查 Grafana 仪表板，查看数据是否成功摄取并发布。

现在脚本已正常工作，您可以尝试使用相同的脚本将其他文件复制到 MinIO。

!!! question "摄取 BUFR 格式的二进制数据"

    运行以下命令，将二进制数据文件 `bufr-example.bin` 复制到 MinIO 的 `wis2box-incoming` 存储桶中：

    ```bash
    python3 copy_file_to_incoming.py bufr-example.bin
    ```

检查 Grafana 仪表板和 MQTT Explorer，查看测试数据是否成功摄取并发布。如果出现任何错误，请尝试解决。

!!! question "验证数据摄取"

    此数据样本发布到 MQTT broker 的消息数量是多少？

??? success "点击查看答案"

    您会在 Grafana 中看到错误报告，因为 BUFR 文件中的站点未在您的 `wis2box` 实例的站点列表中定义。

    如果 BUFR 文件中使用的所有站点都已在您的 `wis2box` 实例中定义，您应该会看到 10 条消息发布到 MQTT broker。每条通知对应一个站点的一个观测时间戳的数据。

    插件 `wis2box.data.bufr4.ObservationDataBUFR` 会将 BUFR 文件拆分为单独的 BUFR 消息，并为每个站点和观测时间戳发布一条消息。

## 通过 SFTP 摄取数据（可选）

`wis2box` 中的 MinIO 服务还可以通过 SFTP 访问。MinIO 的 SFTP 服务器绑定到主机的 8022 端口（22 端口用于 SSH）。

在本次练习中，我们将演示如何使用 WinSCP 通过 SFTP 将数据上传到 MinIO。

您可以按照以下截图设置一个新的 WinSCP 连接：

<img alt="winscp-sftp-connection" src="/../assets/img/winscp-sftp-login.png" width="400">

SFTP 连接的凭据由 `wis2box.env` 文件中的 `WIS2BOX_STORAGE_USERNAME` 和 `WIS2BOX_STORAGE_PASSWORD` 定义，与您用于连接 MinIO UI 的凭据相同。

登录后，您将看到 `wis2box` 在 MinIO 中使用的存储桶：

<img alt="winscp-sftp-bucket" src="/../assets/img/winscp-buckets.png" width="600">

您可以导航到 `wis2box-incoming` 存储桶，然后进入您的数据集文件夹。您会看到之前练习中上传的文件：

<img alt="winscp-sftp-incoming-path" src="/../assets/img/winscp-incoming-data-path.png" width="600">

!!! question "使用 SFTP 上传数据"

    下载此示例文件到本地计算机：

    [synop_202503030900.txt](./../sample-data/synop_202503030900.txt)（右键单击并选择“另存为”下载文件）。

    然后使用 WinSCP 的 SFTP 会话将其上传到 MinIO 的 incoming 数据集路径中。

    检查 Grafana 仪表板和 MQTT Explorer，查看数据是否成功摄取并发布。

??? success "点击查看答案"

    您应该会看到一条新的 WIS2 数据通知，表明测试站点 `0-20000-0-64400` 的数据已成功摄取并发布。

    <img alt="grafana_data_ingest" src="/../assets/img/grafana_data-ingest-test3.png" width="400"> 

    如果路径错误，您将在日志中看到错误消息。

## 总结

!!! success "恭喜！"
    在本次实践中，您学习了如何：

    - 通过多种方法将数据上传到 MinIO 以触发 `wis2box` 工作流。
    - 使用 Grafana 仪表板和 `wis2box` 实例的日志调试数据摄取过程中的常见错误。
    - 在 Grafana 仪表板和 MQTT Explorer 中监控由 `wis2box` 发布的 WIS2 数据通知。
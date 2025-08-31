---
title: 数据发布的接收与处理
---

# 数据发布的接收与处理

!!! abstract "学习目标"

    通过本次实践课程，您将能够：
    
    - 使用命令行、MinIO Web 界面、SFTP 或 Python 脚本将数据上传到 MinIO，从而触发 wis2box 工作流。
    - 访问 Grafana 仪表板，监控数据接收状态并查看您的 wis2box 实例的日志。
    - 使用 MQTT Explorer 查看由您的 wis2box 发布的 WIS2 数据通知。

## 介绍

在 WIS2 中，数据通过 WIS2 数据通知实时共享，这些通知包含一个“规范”链接，可用于下载数据。

要使用 wis2box 软件在 WIS2 Node 中触发数据工作流，必须将数据上传到 **MinIO** 中的 **wis2box-incoming** 存储桶，这将启动 wis2box 工作流。此过程会通过 WIS2 数据通知发布数据。根据您在 wis2box 实例中配置的数据映射，数据可能会在发布之前转换为 BUFR 格式。

在本次练习中，我们将使用示例数据文件触发 wis2box 工作流，并为您在上一实践课程中配置的数据集**发布 WIS2 数据通知**。

在练习过程中，我们将使用 **Grafana 仪表板** 和 **MQTT Explorer** 监控数据接收状态。Grafana 仪表板使用来自 Prometheus 和 Loki 的数据显示您的 wis2box 状态，而 MQTT Explorer 允许您查看由您的 wis2box 实例发布的 WIS2 数据通知。

请注意，根据数据集中预先配置的数据映射，wis2box 会在发布到 MQTT broker 之前将示例数据转换为 BUFR 格式。在本次练习中，我们将重点关注将数据上传到您的 wis2box 实例的不同方法，并验证接收和发布是否成功。数据转换将在 [数据转换工具](./data-conversion-tools.md) 实践课程中进一步讲解。

## 准备工作

本节使用在 wis2box 配置数据集实践课程中准备的两个数据集：

1. 预定义的 weather/surface-based-observations/synop 数据集。

2. 使用 Other 模板创建的自定义数据集（GEPS 示例）。

接收 **weather/surface-based-observations/synop** 数据需要在 wis2box-webapp 中配置站点元数据，具体操作请参考 [配置站点元数据](./configuring-station-metadata.md) 实践课程。

对于本次培训中使用的 **other** 数据集，选择了通用数据无转换插件以发布未转换的 GRIB2 文件。由于该培训数据集不代表站点观测数据，因此无需配置站点。请确保文件扩展名设置为 .grib2，并且文件模式正则表达式与您的数据文件名匹配。

在实际的 WIS2 操作中，如果使用 **other** 模板创建的数据集旨在发布基于站点的观测数据，则必须以与 *surface-based-observations/synop* 相同的方式创建和配置站点元数据。

确保您可以使用 SSH 客户端（例如 PuTTY）登录到您的学生虚拟机。

确保 wis2box 正在运行：

```bash
cd ~/wis2box/
python3 wis2box-ctl.py start
python3 wis2box-ctl.py status
```

确保 MQTT Explorer 正在运行，并使用公共凭据 `everyone/everyone` 连接到您的实例，并订阅主题 `origin/a/wis2/#`。

确保您已打开浏览器，并通过访问 `http://YOUR-HOST:3000` 打开实例的 Grafana 仪表板。

## 准备示例数据

将目录 `exercise-materials/data-ingest-exercises` 复制到您在 `wis2box.env` 文件中定义为 `WIS2BOX_HOST_DATADIR` 的目录中：

```bash
cp -r ~/exercise-materials/data-ingest-exercises ~/wis2box-data/
```

!!! note
    `WIS2BOX_HOST_DATADIR` 由 `wis2box` 目录中包含的 `docker-compose.yml` 文件挂载为 wis2box-management 容器内的 `/data/wis2box/`。
    
    这允许您在主机和容器之间共享数据。

## 添加测试站点（仅适用于基于站点的观测数据）

让我们使用在 [配置 wis2box 数据集](./configuring-wis2box-datasdets.md) 实践课程中创建的预定义 weather/surface-based-observations/synop 数据集，这是一个基于真实站点观测的良好示例。

使用 wis2box-webapp 中的站点编辑器，将 WIGOS 标识符为 `0-20000-0-64400` 的站点添加到您的 wis2box 实例。

从 OSCAR 检索站点：

<img alt="oscar-station" src="/../assets/img/webapp-test-station-oscar-search.png" width="600">

将站点添加到您为 "../surface-based-observations/synop" 发布创建的数据集中，并使用您的身份验证令牌保存更改：

<img alt="webapp-test-station" src="/../assets/img/webapp-test-station-save.png" width="800">

请注意，您可以在实践课程结束后从数据集中移除此站点。

## 从命令行测试数据接收

在本次练习中，我们将使用 `wis2box data ingest` 命令将数据上传到 MinIO。

确保您位于 `wis2box` 目录中，并登录到 **wis2box-management** 容器：

```bash
cd ~/wis2box
python3 wis2box-ctl.py login
```

验证以下示例数据是否存在于 **wis2box-management** 容器内的 `/data/wis2box/` 目录中：

```bash
ls -lh /data/wis2box/data-ingest-exercises/synop_202412030900.txt
```

!!! question "使用 `wis2box data ingest` 接收数据"

    执行以下命令，将示例数据文件接收到您的 wis2box 实例中：

    ```bash
    wis2box data ingest -p /data/wis2box/data-ingest-exercises/synop_202412030900.txt --metadata-id urn:wmo:md:not-my-centre:synop-test
    ```

    数据是否成功接收？如果没有，错误信息是什么？您如何解决？

??? success "点击查看答案"

    数据**未**成功接收。您应该会看到以下内容：

    ```bash
    Error: metadata_id=urn:wmo:md:not-my-centre:synop-test not found in data mappings
    ```

    错误信息表明您提供的元数据标识符与您的 wis2box 实例中配置的任何数据集都不匹配。

    提供与您在上一实践课程中创建的数据集匹配的正确元数据 ID，并重复数据接收命令，直到看到以下输出：

    ```bash 
    Processing /data/wis2box/data-ingest-exercises/synop_202412030900.txt
    Done
    ```

转到浏览器中的 MinIO 控制台，检查文件 `synop_202412030900.txt` 是否已上传到 `wis2box-incoming` 存储桶。您应该会看到一个以您在 `--metadata-id` 选项中提供的数据集名称命名的新目录，在该目录中可以找到文件 `synop_202412030900.txt`：

<img alt="minio-wis2box-incoming-dataset-folder" src="/../assets/img/minio-data-ingest-test-data.png" width="800">

!!! note
    `wis2box data ingest` 命令将文件上传到 MinIO 中的 `wis2box-incoming` 存储桶，并存储在以您提供的元数据标识符命名的目录中。

转到浏览器中的 Grafana 仪表板，检查数据接收状态。

!!! question "在 Grafana 上检查数据接收状态"
    
    在浏览器中转到 Grafana 仪表板（**http://your-host:3000**），检查数据接收状态。
    
    您如何判断数据是否成功接收和发布？

??? success "点击查看答案"
    
    如果数据成功接收，您应该会看到以下内容：
    
    <img alt="grafana_data_ingest" src="/../assets/img/grafana_data-ingest-test.png" width="400">  
    
    如果未看到此内容，请检查仪表板底部显示的 WARNING 或 ERROR 消息，并尝试解决问题。

!!! question "检查 MQTT Broker 中的 WIS2 通知"
    
    打开 MQTT Explorer，检查是否可以看到您刚接收的数据的 WIS2 通知消息。
    
    您的 wis2box 发布了多少条 WIS2 数据通知？
    
    您如何访问正在发布的数据内容？

??? success "点击查看答案"

    您应该会看到 1 条由您的 wis2box 发布的 WIS2 数据通知。

    要访问正在发布的数据内容，您可以展开主题结构，查看消息的不同层级，直到最后一层，并查看消息内容。

消息内容包含一个 "links" 部分，其中有一个 "rel" 键值为 "canonical"，以及一个 "href" 键值为数据下载的 URL。URL 的格式为 `http://YOUR-HOST/data/...`。

请注意，数据格式为 BUFR，您需要一个 BUFR 解析器来查看数据内容。BUFR 格式是一种由气象服务用于交换数据的二进制格式。`wis2box` 内部的数据插件会在发布数据之前将其转换为 BUFR 格式。

完成此练习后，退出 **wis2box-management** 容器：

```bash
exit
```

## 使用 SFTP 上传数据（可选）

`wis2box` 中的 MinIO 服务也可以通过 SFTP 访问。MinIO 的 SFTP 服务器绑定到主机的 8022 端口（22 端口用于 SSH）。

在本练习中，我们将演示如何使用 WinSCP 通过 SFTP 将数据上传到 MinIO。

您可以按照以下截图设置一个新的 WinSCP 连接：

<img alt="winscp-sftp-connection" src="/../assets/img/winscp-sftp-login.png" width="400">

SFTP 连接的凭据由 `wis2box.env` 文件中的 `WIS2BOX_STORAGE_USERNAME` 和 `WIS2BOX_STORAGE_PASSWORD` 定义，与您用于连接 MinIO UI 的凭据相同。

登录后，您将看到 MinIO 中 `wis2box` 使用的存储桶：

<img alt="winscp-sftp-bucket" src="/../assets/img/winscp-buckets.png" width="600">

您可以导航到 `wis2box-incoming` 存储桶，然后进入您的数据集文件夹。您将看到之前练习中上传的文件：

<img alt="winscp-sftp-incoming-path" src="/../assets/img/winscp-incoming-data-path.png" width="600">

!!! question "使用 SFTP 上传数据"

    下载此示例文件到您的本地计算机：

    [synop_202503030900.txt](./../sample-data/synop_202503030900.txt)（右键单击并选择“另存为”下载文件）。

    然后使用 WinSCP 的 SFTP 会话将其上传到 MinIO 的 `incoming` 数据集路径。

    检查 Grafana 仪表板和 MQTT Explorer，确认数据是否成功被摄取和发布。

??? success "点击查看答案"

    您应该会看到一个新的 WIS2 数据通知，发布到测试站点 `0-20000-0-64400`，表明数据已成功被摄取和发布。

    <img alt="grafana_data_ingest" src="/../assets/img/grafana_data-ingest-test3.png" width="400"> 

    如果路径错误，您将在日志中看到错误消息。

## 使用 Python 脚本上传数据（可选）

在本练习中，我们将使用 MinIO 的 Python 客户端将数据复制到 MinIO。

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

    您会遇到一个错误，因为脚本尚未配置为访问 `wis2box` 上的 MinIO 端点。

脚本需要知道访问 `wis2box` 上 MinIO 的正确端点。如果 `wis2box` 运行在您的主机上，MinIO 端点可通过 `http://YOUR-HOST:9000` 访问。脚本还需要更新您的存储密码以及 MinIO 存储桶中存储数据的路径。

!!! question "更新脚本并摄取 CSV 数据"
    
    编辑脚本 `copy_file_to_incoming.py` 以解决错误，可以通过以下方法之一完成：
    - 从命令行：使用 `nano` 或 `vim` 文本编辑器编辑脚本。
    - 使用 WinSCP：启动一个新的连接，使用文件协议 `SCP` 和与您的 SSH 客户端相同的凭据。导航到目录 `wis2box-data/data-ingest-exercises` 并使用内置文本编辑器编辑 `copy_file_to_incoming.py`。

    确保您：

    - 定义主机的正确 MinIO 端点。
    - 提供 MinIO 实例的正确存储密码。
    - 提供 MinIO 存储桶中存储数据的正确路径。

    重新运行脚本，将示例数据文件 `synop_202501030900.txt` 摄取到 MinIO：

    ```bash
    python3 ~/wis2box-data/ ~/wis2box-data/synop_202501030900.txt
    ```

    确保错误已解决。

一旦您成功运行脚本，您将看到一条消息，指示文件已复制到 MinIO，并且您应该在 MQTT Explorer 中看到由 `wis2box` 实例发布的数据通知。

您还可以检查 Grafana 仪表板，确认数据是否成功被摄取和发布。

现在脚本已正常工作，您可以尝试使用相同的脚本将其他文件复制到 MinIO。

!!! question "摄取 BUFR 格式的二进制数据"

    运行以下命令，将二进制数据文件 `bufr-example.bin` 复制到 MinIO 的 `wis2box-incoming` 存储桶中：

    ```bash
    python3 copy_file_to_incoming.py bufr-example.bin
    ```

检查 Grafana 仪表板和 MQTT Explorer，确认测试数据是否成功被摄取和发布。如果看到任何错误，请尝试解决。

!!! question "验证数据摄取"

    此数据样本发布到 MQTT broker 的消息数量是多少？

??? success "点击查看答案"

    您将在 Grafana 中看到错误报告，因为 BUFR 文件中的站点未在您的 `wis2box` 实例的站点列表中定义。
    
    如果 BUFR 文件中使用的所有站点都已在 `wis2box` 实例中定义，您应该会看到 10 条消息发布到 MQTT broker。每条通知对应一个站点的一个观测时间戳的数据。

    插件 `wis2box.data.bufr4.ObservationDataBUFR` 将 BUFR 文件拆分为单独的 BUFR 消息，并为每个站点和观测时间戳发布一条消息。

## 使用 MinIO Web 界面上传数据

在前三种摄取方法中，我们始终使用基于站点的数据集（synop）及其相关的观测数据。在本节中，我们将介绍第四种方法——一种最常用的方法。这里，我们将处理 Other 数据集，并使用 MinIO Web 界面摄取 GEPS 数据，该界面允许通过 Web 浏览器直接上传和下载数据。

### 登录 MinIO 浏览器

打开 MinIO Web 界面（通常可通过 http://localhost:9001 访问）。

凭据 `WIS2BOX_STORAGE_USERNAME` 和 `WIS2BOX_STORAGE_PASSWORD` 可在 `wis2box.env` 文件中找到。

### 导航到 `wis2box-incoming` 存储桶

选择存储桶 `wis2box-incoming` 并点击“创建新路径”。
目录名称必须与您的数据集的元数据标识符相对应。
在本次培训中，我们使用之前创建的 GEPS 数据集，因此创建目录：

```bash
urn:wmo:md:nl-knmi-test:customized-geps-dataset-wis2-training
```

### 上传 GEPS 数据文件

进入新创建的目录，点击“上传”，并选择本地的 GEPS 数据文件进行上传。

<img alt="minio-incoming-path" src="/../assets/img/minio-incoming-data-GEPS.png" width="800">

### 使用 MQTT Explorer 验证上传成功

上传后，使用 MQTT Explorer 检查数据是否成功发布。

如果未成功，请检查以下内容：

1. 验证 GEPS 数据集配置的插件。文件名与配置的正则表达式不匹配可能会导致摄取失败。调整正则表达式或重命名数据文件以匹配。

2. 重启 `wis2box` 并重复上传过程。

一旦数据成功发布，您将看到类似以下的确认消息：

<img alt="minio-incoming-path" src="/../assets/img/minio-incoming-data-path-publish.png" width="800">

!!! question "使用 MinIO Web 界面重新上传数据"

    在浏览器中打开 MinIO Web 界面，浏览到 `wis2box-incoming` 存储桶。您将看到之前练习中上传的文件 `Z_NAFP_C_BABJ_20250818000000_P_CMA-GEPS-GLB-024`。

    点击文件，您将有选项下载它：

    <img alt="minio-wis2box-incoming-dataset-folder" src="/../assets/img/minio-download.png" width="800">

    您可以下载此文件并将其重新上传到 MinIO 的相同路径，以重新触发 `wis2box` 工作流。

检查 Grafana 仪表板和 MQTT Explorer，确认数据是否已成功摄取并发布。

??? success "点击查看答案"

您将看到一条消息，表明 wis2box 已经发布了该数据：

```bash
ERROR - Data already published for Z_NAFP_C_BABJ_20250818000000_P_CMA-GEPS-GLB-024-grib2; not publishing
``` 

这表明数据工作流已被触发，但数据未被重新发布。wis2box 不会重复发布相同的数据。

对于**其他**数据集：

## 结论

!!! success "恭喜！"
在本次实践课程中，您学会了：

- 通过多种方法将数据上传到 MinIO，从而触发 wis2box 工作流。
- 使用 Grafana 仪表板和您的 wis2box 实例日志，调试数据摄取过程中的常见错误。
- 在 Grafana 仪表板和 MQTT Explorer 中监控由您的 wis2box 发布的 WIS2 数据通知。
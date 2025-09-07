---
title: 数据发布的摄取
---

# 数据发布的摄取

!!! abstract "学习目标"

    在本次实践课程结束时，您将能够：
    
    - 通过使用 MinIO 网页界面、SFTP 或 Python 脚本上传数据到 MinIO，触发 wis2box 工作流。
    - 访问 Grafana 仪表板，监控数据摄取状态并查看您的 wis2box 实例的日志。
    - 使用 MQTT Explorer 查看由您的 wis2box 发布的 WIS2 数据通知。

## 介绍

在 WIS2 中，数据通过 WIS2 数据通知实时共享，这些通知包含一个“规范”链接，可用于下载数据。

要使用 wis2box 软件在 WIS2 Node 中触发数据工作流，必须将数据上传到 **MinIO** 中的 **wis2box-incoming** 存储桶，这将启动 wis2box 工作流。此过程会通过 WIS2 数据通知发布数据。根据您在 wis2box 实例中配置的数据映射，数据可能会在发布之前被转换为 BUFR 格式。

在本次练习中，我们将使用示例数据文件触发 wis2box 工作流，并为您在之前实践课程中配置的数据集**发布 WIS2 数据通知**。

在练习过程中，我们将使用 **Grafana 仪表板** 和 **MQTT Explorer** 监控数据摄取状态。Grafana 仪表板使用来自 Prometheus 和 Loki 的数据显示您的 wis2box 状态，而 MQTT Explorer 允许您查看由您的 wis2box 实例发布的 WIS2 数据通知。

在本次练习中，我们将重点介绍将数据上传到您的 wis2box 实例的不同方法，并验证摄取和发布是否成功。数据转换将在 [数据转换工具](./data-conversion-tools.md) 实践课程中进一步介绍。

## 准备工作

本节使用在 [配置 wis2box 数据集](./configuring-wis2box-datasets.md) 实践课程中创建的 "surface-based-observations/synop" 和 "other" 数据集。

还需要了解如何在 **wis2box-webapp** 中配置站点，如 [配置站点元数据](./configuring-station-metadata.md) 实践课程中所述。

确保您可以使用 SSH 客户端（例如 PuTTY）登录到您的学生虚拟机。

确保 wis2box 正在运行：

```bash
cd ~/wis2box/
python3 wis2box-ctl.py start
python3 wis2box-ctl.py status
```

确保 MQTT Explorer 正在运行，并使用公共凭据 `everyone/everyone` 连接到您的实例，并订阅主题 `origin/a/wis2/#`。

确保您已打开一个浏览器，并通过访问 `http://YOUR-HOST:3000` 打开您的实例的 Grafana 仪表板。

## 使用 MinIO 界面摄取数据

首先，我们将使用 MinIO 网页界面，该界面允许您通过浏览器下载和上传数据到 MinIO。

### 访问 MinIO 界面

打开 MinIO 网页界面，通常可以通过 `http://YOUR-HOST:9001` 访问。

<img alt="Minio UI: minio ui" src="/../assets/img/minio-ui.png" width="400">

WIS2BOX_STORAGE_USERNAME 和 WIS2BOX_STORAGE_PASSWORD 凭据可以在 wis2box.env 文件中找到。

如果您不确定这些值，请导航到您的 wis2box 根目录并运行以下命令，仅显示相关凭据：

```bash
grep -E '^(WIS2BOX_STORAGE_USERNAME|WIS2BOX_STORAGE_PASSWORD)=' wis2box.env
```

在登录 MinIO 时，使用 WIS2BOX_STORAGE_USERNAME 和 WIS2BOX_STORAGE_PASSWORD 的值作为用户名和密码。

### 使用 Universal 插件摄取和发布数据

下载 geps 示例数据 [geps_202508180000.grib2](../sample-data/geps_202508180000.grib2) 到您的本地环境：

选择存储桶 wis2box-incoming 并点击 `Create new path`。

<img alt="minio ui: create new path" src="/../assets/img/minio-create-new-path.png" width="800">

路径名称必须对应于您在 [配置 wis2box 数据集](./configuring-wis2box-datasets.md) 实践课程中创建的 "other" 数据集的元数据标识符。

<img alt="minio ui: create new path empty" src="/../assets/img/minio-ui-create-path-empty.png" width="700">

因此，在本例中，请创建以下目录：

```bash
urn:wmo:md:my-centre-id:my-other-dataset
```

进入新创建的目录，点击 `Upload`，找到您之前下载到本地的 [geps_202508180000.grib2](../sample-data/geps_202508180000.grib2)，并将此文件上传到 wis2box-incoming 存储桶。

<img alt="minio ui: upload your file" src="/../assets/img/minio-other-dataset-upload.png" width="650">

上传完成后，您将在 MinIO 的 wis2box-incoming 存储桶中看到此文件：

<img alt="minio ui: upload your file" src="/../assets/img/minio-geps-file-upload.png" width="650">

上传后，使用 MQTT Explorer 检查数据是否成功发布。

<img alt="Metadata Editor: title, description, keywords" src="/../assets/img/mqtt-explorer-wis2-notification-geps-sample.png" width="800">

接下来，下载具有不同文件扩展名的 geps 示例数据 [geps_202508180000.nc](../sample-data/geps_202508180000.nc) 到您的本地环境。将此文件上传到与之前练习相同的目录中。

!!! question "问题"

    您能否成功上传到 wis2box-incoming 存储桶？

??? success "点击查看答案"

    可以。
    <img alt="Minio ui: geps nc file" src="/../assets/img/minio-upload-geps-with-nc-extension.png" width="800">

!!! question "问题"

    您能否通过 MinIO 成功发布数据通知消息？ 
    检查 Grafana 仪表板和 MQTT Explorer，查看数据是否成功摄取和发布。

!!! hint

    在创建自定义数据集时，您使用了哪个插件？
    插件是否对文件格式有任何要求？这些要求在哪里指定？

??? success "点击查看答案"

    不可以。
    您将看到一条消息，指示存在未知文件类型错误。

    ```bash
    ERROR - Path validation error: Unknown file type (nc) for metadata_id=urn:wmo:md:nl-knmi-test:customized-geps-dataset-wis2-training. Did not match any of the following:grib2
    ``` 
    
    这表明数据工作流已被触发，但数据未被重新发布。如果文件扩展名不匹配 grib2，wis2box 将不会发布数据。

然后，下载重命名的 geps 示例数据 [geps_renamed_sample_data.grib2](../sample-data/geps_renamed_sample_data.grib2) 到您的本地环境。将此文件上传到与之前两个练习相同的目录中。

!!! question "问题"

    您能否成功上传到 wis2box-incoming 存储桶？

??? success "点击查看答案"

    可以。
    <img alt="Minio ui: geps nc file" src="/../assets/img/minio-upload-renamed-geps.png" width="800">

!!! question "问题"

    您能否通过 MinIO 成功发布数据通知消息？ 
    检查 Grafana 仪表板和 MQTT Explorer，查看数据是否成功摄取和发布。

!!! hint

    您使用的自定义插件是否对文件名有任何要求或限制？

??? success "点击查看答案"

    不可以。
    您将看到一条消息，指示数据未匹配正则表达式的错误。

    ```bash
    ERROR - ERROR - geps_renamed_sample_data.grib2 did not match ^.*?_(\d{8}).*?\..*$
    ``` 
    
    这表明数据工作流已被触发，但数据未被重新发布。如果文件名不匹配正则表达式 ^.*?_(\d{8}).*?\..*$，wis2box 将不会发布数据。

Universal 插件提供了一种通用机制，用于摄取和发布文件，而无需应用特定领域的解码。相反，它在发布 WIS2 通知之前执行一组基本检查：

`文件扩展名` – 文件必须使用数据集配置中允许的扩展名。

`文件名模式` – 文件名必须匹配数据集中定义的正则表达式。

如果两个条件都满足，文件将被摄取并发布通知。

将文件上传到 MinIO 只要用户有权限访问，总是可以成功的。然而，发布 WIS2 数据通知需要更严格的验证。不符合扩展名或文件名规则的文件会存储在 `incoming` 存储桶中，但 `Universal plugin` 不会为它们发布通知。这解释了为什么具有不支持的扩展名（例如 `geps_202508180000.nc`）或无效文件名（例如 `geps_renamed_sample_data.grib2`）的文件会被 MinIO 接受，但不会出现在 WIS2 中。

接下来，在浏览器中打开 MinIO 的 Web 界面，浏览到 `wis2box-incoming` 存储桶。您会看到在前面练习中上传的文件 `geps_202508180000.grib2`。

点击该文件，您将有下载选项：

<img alt="minio-wis2box-incoming-dataset-folder" src="/../assets/img/minio-download.png" width="800">

请下载此文件并将其重新上传到 MinIO 中的相同路径，以重新触发 wis2box 工作流。

!!! question "问题"

    您能通过 MinIO 成功重新发布数据通知消息吗？  
    检查 Grafana 仪表板和 MQTT Explorer，查看数据是否成功被摄取和发布。

??? success "点击查看答案"

    您会看到一条消息，表明 wis2box 已经发布了此数据：

    ```bash
    ERROR - Data already published for geps_202508180000-grib2; not publishing
    ``` 
    
    这表明数据工作流已被触发，但数据未被重新发布。wis2box 不会重复发布相同的数据。

### 使用 synop2bufr-plugin 进行数据摄取和发布

下载 synop 示例数据 [synop_202502040900.txt](../sample-data/synop_202502040900.txt) 到您的本地环境：

与之前的练习一样，在 `wis2box-incoming` 存储桶下创建一个与您的 surface-based-observations/synop 数据集的元数据标识符匹配的目录。

进入新创建的目录，点击 `Upload`，选择您之前下载到本地计算机的 [synop_202502040900.txt](../sample-data/synop_202502040900.txt)，然后上传。

!!! question "问题"

    您能通过 MinIO 成功发布数据通知消息吗？  
    检查 Grafana 仪表板和 MQTT Explorer，查看数据是否成功被摄取和发布。

??? success "点击查看答案"

    不能。  
    在 Grafana 仪表板中，您会看到一条警告，表明缺少站点 64400 的记录：

    ```bash
    WARNING - Station 64400 not found in station file
    ``` 
    
    这表明数据工作流已被触发，但需要特定的站点元数据。

在这种情况下，您正在使用 `FM-12 data converted to BUFR` 插件。

该插件的目的是处理以纯文本格式提供的 FM-12 数据并将其转换为二进制 BUFR。在此过程中，插件需要解析并映射数据中包含的站点信息。

如果缺少必要的站点元数据，插件将无法正确解析文件，转换将失败。

因此，在发布 SYNOP 数据之前，您必须确保已将相关站点元数据添加到 wis2box。

现在，为本次练习添加一个测试站点。

使用 wis2box-webapp 中的站点编辑器，将 WIGOS 标识符为 `0-20000-0-64400` 的站点添加到您的 wis2box 实例中。

从 OSCAR 检索站点：

<img alt="oscar-station" src="/../assets/img/webapp-test-station-oscar-search.png" width="600">

将站点添加到您为 "../surface-based-observations/synop" 发布创建的数据集中，并使用您的身份验证令牌保存更改：

<img alt="webapp-test-station" src="/../assets/img/webapp-test-station-save.png" width="800">

请注意，您可以在实践课程结束后从数据集中移除此站点。

完成站点元数据配置后，使用 MQTT Explorer 检查数据是否成功发布。如果您看到以下通知，则说明您已成功发布 synop 示例数据。

<img alt="webapp-test-station" src="/../assets/img/mqtt-explorer-wis2box-notification-synop-sample.png" width="800">

## 使用 Python 进行数据摄取（可选）

在本次练习中，我们将使用 MinIO 的 Python 客户端将数据复制到 MinIO。

MinIO 提供了一个 Python 客户端，可以通过以下方式安装：

```bash
pip3 install minio
```

在您的学生虚拟机上，Python 的 'minio' 包已经安装。

将目录 `exercise-materials/data-ingest-exercises` 复制到您在 `wis2box.env` 文件中定义为 `WIS2BOX_HOST_DATADIR` 的目录：

```bash
cp -r ~/exercise-materials/data-ingest-exercises ~/wis2box-data/
```

!!! note
    `WIS2BOX_HOST_DATADIR` 通过 `wis2box` 目录中包含的 `docker-compose.yml` 文件挂载为 wis2box-management 容器内的 `/data/wis2box/`。
    
    这允许您在主机和容器之间共享数据。

在 `exercise-materials/data-ingest-exercises` 目录中，您会找到一个示例脚本 `copy_file_to_incoming.py`，可用于将文件复制到 MinIO。

尝试运行脚本，将示例数据文件 `synop_202501030900.txt` 复制到 MinIO 的 `wis2box-incoming` 存储桶中：

```bash
cd ~/wis2box-data/data-ingest-exercises
python3 copy_file_to_incoming.py synop_202501030900.txt
```

!!! note

    您会收到一个错误，因为脚本尚未配置为访问您的 wis2box 上的 MinIO 端点。

脚本需要知道访问 wis2box 上 MinIO 的正确端点。如果 wis2box 运行在您的主机上，MinIO 端点可通过 `http://YOUR-HOST:9000` 访问。脚本还需要更新您的存储密码以及 MinIO 存储桶中存储数据的路径。

!!! question "更新脚本并摄取 CSV 数据"
    
    编辑脚本 `copy_file_to_incoming.py` 以解决错误，使用以下方法之一：
    - 从命令行：使用 `nano` 或 `vim` 文本编辑器编辑脚本。
    - 使用 WinSCP：使用与您的 SSH 客户端相同的凭据启动一个新的连接，文件协议选择 `SCP`。导航到目录 `wis2box-data/data-ingest-exercises` 并使用内置文本编辑器编辑 `copy_file_to_incoming.py`。
    
    确保您：

    - 定义主机的正确 MinIO 端点。
    - 提供 MinIO 实例的正确存储密码。
    - 提供 MinIO 存储桶中存储数据的正确路径。

    重新运行脚本，将示例数据文件 `synop_202501030900.txt` 摄取到 MinIO：

    ```bash
    python3 ~/wis2box-data/ ~/wis2box-data/synop_202501030900.txt
    ```

    确保错误已解决。

一旦您成功运行脚本，您将看到一条消息，表明文件已复制到 MinIO，并且您应该在 MQTT Explorer 中看到您的 wis2box 实例发布的数据通知。

您还可以检查 Grafana 仪表板，查看数据是否成功被摄取和发布。

现在脚本已正常工作，您可以尝试使用相同的脚本将其他文件复制到 MinIO。

!!! question "摄取 BUFR 格式的二进制数据"

    运行以下命令，将二进制数据文件 `bufr-example.bin` 复制到 MinIO 的 `wis2box-incoming` 存储桶中：

    ```bash
    python3 copy_file_to_incoming.py bufr-example.bin
    ```

检查 Grafana 仪表板和 MQTT Explorer，查看测试数据是否成功被摄取和发布。如果您看到任何错误，请尝试解决它们。

!!! question "验证数据摄取"

    对于此数据样本，发布到 MQTT broker 的消息数量是多少？

??? success "点击查看答案"

    您将在 Grafana 中看到错误报告，因为 BUFR 文件中的站点未在您的 wis2box 实例的站点列表中定义。 
    
    如果 BUFR 文件中使用的所有站点都在您的 wis2box 实例中定义，您应该会看到 10 条消息发布到 MQTT broker。每条通知对应一个站点的一个观测时间戳的数据。

    插件 `wis2box.data.bufr4.ObservationDataBUFR` 会将 BUFR 文件拆分为单独的 BUFR 消息，并为每个站点和观测时间戳发布一条消息。

## 通过 SFTP 摄取数据（可选）

wis2box 中的 MinIO 服务还可以通过 SFTP 访问。MinIO 的 SFTP 服务器绑定到主机的 8022 端口（22 端口用于 SSH）。

在本次练习中，我们将演示如何使用 WinSCP 通过 SFTP 将数据上传到 MinIO。

您可以按照以下截图设置一个新的 WinSCP 连接：

<img alt="winscp-sftp-connection" src="/../assets/img/winscp-sftp-login.png" width="400">

SFTP 连接的凭据由 `WIS2BOX_STORAGE_USERNAME` 和 `WIS2BOX_STORAGE_PASSWORD` 定义，这些变量存储在您的 `wis2box.env` 文件中，并且与您用于连接 MinIO UI 的凭据相同。

登录后，您将看到 wis2box 在 MinIO 中使用的存储桶：

<img alt="winscp-sftp-bucket" src="/../assets/img/winscp-buckets.png" width="600">

您可以导航到 `wis2box-incoming` 存储桶，然后进入您的数据集文件夹。您将看到在之前练习中上传的文件：

<img alt="winscp-sftp-incoming-path" src="/../assets/img/winscp-incoming-data-path.png" width="600">

!!! question "使用 SFTP 上传数据"

    下载此示例文件到您的本地计算机：

    [synop_202503030900.txt](./../sample-data/synop_202503030900.txt) （右键单击并选择“另存为”以下载文件）。

    然后使用 WinSCP 中的 SFTP 会话将其上传到 MinIO 的 incoming 数据集路径。

    在 Grafana 仪表板和 MQTT Explorer 中检查数据是否成功被摄取并发布。

??? success "点击查看答案"

    您应该会看到一个新的 WIS2 数据通知已为测试站点 `0-20000-0-64400` 发布，这表明数据已成功被摄取并发布。

    <img alt="grafana_data_ingest" src="/../assets/img/grafana_data-ingest-test3.png" width="400"> 

    如果您使用了错误的路径，您将在日志中看到一条错误消息。

## 结论

!!! success "恭喜！"
    在本次实践课程中，您学习了如何：

    - 通过多种方法将数据上传到 MinIO 来触发 wis2box 工作流。
    - 使用 Grafana 仪表板和 wis2box 实例的日志调试数据摄取过程中的常见错误。
    - 在 Grafana 仪表板和 MQTT Explorer 中监控由您的 wis2box 发布的 WIS2 数据通知。
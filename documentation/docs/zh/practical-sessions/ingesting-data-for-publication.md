---
title: 数据发布的摄取
---

# 数据发布的摄取

!!! abstract "学习目标"

    在本次实践课程结束时，您将能够：
    
    - 通过使用 MinIO Web 界面、SFTP 或 Python 脚本将数据上传到 MinIO 来触发 wis2box 工作流。
    - 访问 Grafana 仪表板以监控数据摄取状态并查看您的 wis2box 实例的日志。
    - 使用 MQTT Explorer 查看由您的 wis2box 发布的 WIS2 数据通知。

## 介绍

在 WIS2 中，数据通过包含“规范”链接的 WIS2 数据通知实时共享，用户可以通过该链接下载数据。

要使用 wis2box 软件在 WIS2 Node 中触发数据工作流，必须将数据上传到 **MinIO** 中的 **wis2box-incoming** 存储桶，这将启动 wis2box 数据工作流以处理并发布数据。

要监控 wis2box 数据工作流的状态，您可以使用 **Grafana 仪表板** 和 **MQTT Explorer**。Grafana 仪表板使用来自 Prometheus 和 Loki 的数据来显示您的 wis2box 状态，而 MQTT Explorer 允许您查看由您的 wis2box 实例发布的 WIS2 数据通知。

在本节中，我们将重点介绍如何将数据上传到您的 wis2box 实例并验证摄取和发布是否成功。数据转换将在 [数据转换工具](./data-conversion-tools.md) 实践课程中进一步讲解。

为了手动测试数据摄取过程，我们将使用 MinIO Web 界面，它允许您通过 Web 浏览器下载和上传数据到 MinIO。

在生产环境中，数据通常通过自动化流程摄取，例如通过 S3 或 SFTP 将数据转发到 MinIO 的脚本或应用程序。

## 准备工作

本节假设您已成功完成 [在 wis2box 中配置数据集](./configuring-wis2box-datasets.md) 的实践课程。如果您按照该课程中的说明操作，您应该有一个使用 `Universal` 插件的数据集，以及另一个使用 `FM-12 data converted to BUFR` 插件的数据集。

确保您可以使用 SSH 客户端（例如 PuTTY）登录到您的学生虚拟机。

确保 wis2box 正在运行：

```bash
cd ~/wis2box/
python3 wis2box-ctl.py start
python3 wis2box-ctl.py status
```

确保 MQTT Explorer 正在运行，并使用公共凭据 `everyone/everyone` 连接到您的实例，并订阅主题 `origin/a/wis2/#`。

## Grafana 仪表板

打开位于 `http://YOUR-HOST:3000` 的 Grafana 仪表板，您将看到 wis2box 数据发布仪表板：

<img alt="grafana_dashboard" src="/../assets/img/grafana-homepage.png" width="800">

保持 Grafana 仪表板在浏览器中打开，因为稍后我们将使用它来监控数据摄取的状态。

## 使用 MinIO Web 界面

打开位于 `http://YOUR-HOST:9001` 的 MinIO Web 界面，您将看到登录界面：

<img alt="Minio UI: minio ui" src="/../assets/img/minio-login.png" width="400">

要登录，您需要使用定义在 wis2box.env 文件中的 WIS2BOX_STORAGE_USERNAME 和 WIS2BOX_STORAGE_PASSWORD 凭据。
您可以通过在学生虚拟机上运行以下命令来检查这些变量的值：

```bash
cat wis2box.env | grep WIS2BOX_STORAGE_USERNAME
cat wis2box.env | grep WIS2BOX_STORAGE_PASSWORD
```

登录后，您将进入 MinIO 的对象浏览器视图。在这里，您可以看到 wis2box 使用的存储桶：

- *wis2box-incoming*: 这是您上传数据以触发 wis2box 工作流的存储桶。
- *wis2box-public*: 这是 wis2box 发布已成功摄取和处理数据的存储桶。

点击存储桶 *wis2box-incoming*。尝试通过点击 `Create new path` 定义一个新路径：

<img alt="minio ui: minio ui after login" src="/../assets/img/minio-incoming-create-new-path.png" width="800">

输入新文件夹路径 = *new-directory* 并上传此示例文件 [mydata.nc](./../sample-data/mydata.nc)（右键单击并选择“另存为”下载文件）。您可以使用 MinIO 中的“Upload”按钮将文件上传到新目录中：

<img alt="minio ui: create new path" src="/../assets/img/minio-initial-example-upload.png" width="800">

!!! question "问题"

    上传文件后，如何查看 wis2box 中的数据工作流是否成功触发？

??? success "点击查看答案"

    您可以检查 Grafana 仪表板以查看数据是否成功摄取和发布。

    查看 Grafana 仪表板的底部面板，您将看到一个 **路径验证错误**，指示路径与任何已配置的数据集不匹配：

    ```bash
    ERROR - Path validation error: Could not match http://minio:9000/wis2box-incoming/new-directory/mydata.nc to dataset, path should include one of the following: ['urn:wmo:md:int-wmo-example:synop-dataset-wis2-training', 'urn:wmo:md:int-wmo-example:forecast-dataset' ...
    ``` 
    
## 摄取与发布："Universal"-插件

现在您已经知道如何将数据上传到 MinIO，让我们尝试为您在上一节中创建的使用 "Universal"-插件的预测数据集上传数据。

返回浏览器中的 MinIO Web 界面，选择存储桶 `wis2box-incoming`，然后点击 `Create new path`。

这次请确保**创建一个与您在上一节中创建的预测数据集的元数据标识符匹配的目录**：

<img alt="minio-filepath-forecast-dataset" src="/../assets/img/minio-filepath-forecast-dataset.png" width="800">

进入新创建的目录，点击 `Upload` 并将您之前使用的文件 *mydata.nc* 上传到新目录中。检查 Grafana 仪表板以查看数据是否成功摄取和发布。

您应该在 Grafana 仪表板中看到以下错误：

```bash
ERROR - Path validation error: Unknown file type (nc) for metadata_id=urn:wmo:md:int-wmo-example:forecast-dataset. Did not match any of the following:grib2
```

!!! question "问题"

    为什么数据未被摄取和发布？

??? success "点击查看答案"

    数据集被配置为仅处理扩展名为 `.grib2` 的文件。文件扩展名配置是您在上一节中定义的数据映射的一部分。

下载此文件 [GEPS_18August2025.grib2](../sample-data/GEPS_18August2025.grib2) 到您的本地计算机，并将其上传到您为预测数据集创建的目录中。检查 Grafana 仪表板和 MQTT Explorer 以查看数据是否成功摄取和发布。

您将在 Grafana 仪表板中看到以下错误：

```bash
ERROR - Failed to transform file http://minio:9000/wis2box-incoming/urn:wmo:md:int-wmo-example:forecast-dataset/GEPS_18August2025.grib2 : GEPS_18August2025.grib2 did not match ^.*?_(\d{8}).*?\..*$
```

!!! question "问题"

    如何解决此错误？

??? success "点击查看答案"

    文件名与您在数据集配置中定义的正则表达式不匹配。文件名必须匹配模式 `^.*?_(\d{8}).*?\..*$`，该模式要求文件名中包含一个 8 位日期（YYYYMMDD）。

    将文件重命名为 *GEPS_202508180000.grib2* 并再次上传到 MinIO 中的相同路径以重新触发 wis2box 工作流。（或者从这里下载重命名的文件：[GEPS_202508180000.grib2](../sample-data/GEPS_202508180000.grib2)）。

修复文件名问题后，检查 Grafana 仪表板和 MQTT Explorer 以查看数据是否成功摄取和发布。

您应该在 MQTT Explorer 中看到一个新的 WIS2 数据通知：

<img alt="mqtt explorer: message notification geps data" src="/../assets/img/mqtt-explorer-wis2-notification-geps-sample.png" width="800">

!!! note "关于 Universal 插件"

    "Universal"-插件允许您在不进行任何转换的情况下发布数据。这是一个*直通*插件，它摄取数据文件并按原样发布。为了将属性 "datetime" 添加到 WIS2 数据通知中，该插件依赖于文件模式中的第一个分组来匹配您正在发布的数据的日期。

!!! question "附加问题"

    尝试将相同的文件再次上传到 MinIO 中的相同路径。您是否会在 MQTT Explorer 中收到另一个通知？

??? success "点击查看答案"

    不会。
    在 Grafana 仪表板中，您将看到一个错误，指示数据已被发布：

```bash
ERROR - Data already published for GEPS_202508180000-grib2; not publishing
```

这表明数据工作流已被触发，但数据未被重新发布。wis2box 不会重复发布相同的数据。

如果您希望强制重新发送相同数据的通知，请在重新导入数据之前，从 'wis2box-public' 存储桶中删除该数据。

## 导入与发布："synop2bufr"-插件

接下来，您将使用 **Template='weather/surface-based-observations/synop'** 模板处理您在上一个实践环节中创建的数据集。该模板为您预先配置了以下数据插件：

<img alt="synop-dataset-plugins" src="/../assets/img/wis2box-data-mappings.png" width="1000">

请注意，其中一个插件是 **FM-12 数据转换为 BUFR**（synop2bufr），该插件被配置为处理文件扩展名为 **txt** 的文件。

下载此示例数据 [synop_202502040900.txt](../sample-data/synop_202502040900.txt)（右键单击并选择“另存为”以下载文件）到您的本地计算机。在 MinIO 中创建一个与 synop 数据集的元数据标识符匹配的新路径，并将示例数据上传到该路径。

检查 Grafana 仪表板和 MQTT Explorer，确认数据是否成功导入并发布。

!!! question "问题"

    为什么您没有在 MQTT Explorer 中收到通知？

??? success "点击查看答案"

    在 Grafana 仪表板中，您会看到以下警告：

    ```bash
    WARNING - Station 64400 not found in station file
    ```

    或者，如果主题中没有关联的站点，您会看到：

    ```bash
    ERROR - No stations found
    ```

    数据工作流已被触发，但由于缺少站点元数据，数据插件无法处理数据。

!!! note "关于 FM-12 数据转换为 BUFR 插件"

    此插件尝试将 FM-12 输入数据转换为 BUFR 格式。

    在转换过程中，插件会向输出数据添加缺失的元数据，例如 WIGOS 站点标识符、站点位置和气压计高度。为了添加这些元数据，插件会使用传统的（5 位）标识符（在本例中为 64400）在您的 wis2box 实例的站点列表中查找相关信息。

    如果在站点列表中找不到该站点，插件将无法添加缺失的元数据，也不会发布任何数据。

使用 wis2box-webapp 中的站点编辑器，将 WIGOS 标识符为 `0-20000-0-64400` 的站点添加到您的 wis2box 实例中，如您在 [配置站点元数据](./configuring-station-metadata.md) 实践环节中所学。

从 OSCAR 检索站点信息：

<img alt="oscar-station" src="/../assets/img/webapp-test-station-oscar-search.png" width="600">

将站点添加到 '../weather/surface-based-observations/synop' 的主题中，并使用您的身份验证令牌保存更改。

添加站点后，通过再次将示例数据文件 *synop_202502040900.txt* 上传到 MinIO 中的相同路径，重新触发 wis2box 工作流。

检查 Grafana 仪表板和 MQTT Explorer，确认数据是否成功发布。如果您看到以下通知，则说明您已成功发布 synop 示例数据：

<img alt="webapp-test-station" src="/../assets/img/mqtt-explorer-wis2box-notification-synop-sample.png" width="800">

!!! question "问题"

    在 WIS2 数据通知中发布的文件扩展名是什么？

??? success "点击查看答案"

    在 MQTT Explorer 的 WIS2 数据通知的 Links 部分中，您将看到规范链接：

    ```json
    {
      "rel": "canonical",
      "type": "application/bufr",
      "href": "http://example.wis2.training/data/2025-02-04/wis/urn:wmo:md:int-wmo-example:synop-dataset/WIGOS_0-20000-0-64400_20250204T090000.bufr4",
      "length": 387
    }
    ```

    文件扩展名为 `.bufr4`，表明数据已成功从 FM-12 格式转换为 BUFR 格式。

## 使用 Python 导入数据

使用 MinIO Web 界面是手动上传数据到 MinIO 进行测试的便捷方式。然而，在生产环境中，通常会使用自动化流程将数据上传到 MinIO，例如使用脚本或基于 MinIO S3 兼容 API 的应用程序。

在本练习中，我们将使用 MinIO 的 Python 客户端将数据复制到 MinIO 中。

MinIO 提供了一个 Python 客户端，可以通过以下方式安装：

```bash
pip3 install minio
```

在您的学生虚拟机上，Python 的 'minio' 包已经安装。

将目录 `exercise-materials/data-ingest-exercises` 复制到您在 `wis2box.env` 文件中定义的 `WIS2BOX_HOST_DATADIR` 目录中：

```bash
cp -r ~/exercise-materials/data-ingest-exercises ~/wis2box-data/
```

!!! note
    `WIS2BOX_HOST_DATADIR` 在 `docker-compose.yml` 文件中被挂载为 wis2box-management 容器内的 `/data/wis2box/`。

    这允许主机与容器之间共享数据。

在 `exercise-materials/data-ingest-exercises` 目录中，您会找到一个示例脚本 `copy_file_to_incoming.py`，可用于将文件复制到 MinIO。

尝试运行脚本，将示例数据文件 `synop_202501030900.txt` 复制到 MinIO 的 `wis2box-incoming` 存储桶中：

```bash
cd ~/wis2box-data/data-ingest-exercises
python3 copy_file_to_incoming.py synop_202501030900.txt
```

!!! note

    您会收到错误提示，因为脚本尚未配置为访问您的 wis2box 上的 MinIO 端点。

脚本需要知道访问 wis2box 上 MinIO 的正确端点。如果 wis2box 运行在您的主机上，MinIO 端点可通过 `http://YOUR-HOST:9000` 访问。脚本还需要更新您的存储密码以及 MinIO 存储桶中存储数据的路径。

!!! question "更新脚本并导入 CSV 数据"
    
    编辑脚本 `copy_file_to_incoming.py` 以解决错误，使用以下方法之一：
    - 从命令行：使用 `nano` 或 `vim` 文本编辑器编辑脚本。
    - 使用 WinSCP：启动一个新连接，使用文件协议 `SCP` 和与您的 SSH 客户端相同的凭据。导航到目录 `wis2box-data/data-ingest-exercises` 并使用内置文本编辑器编辑 `copy_file_to_incoming.py`。

    确保您：
    - 定义主机的正确 MinIO 端点。
    - 提供 MinIO 实例的正确存储密码。
    - 提供 MinIO 存储桶中存储数据的正确路径。

    重新运行脚本，将示例数据文件 `synop_202501030900.txt` 导入 MinIO：

    ```bash
    python3 ~/wis2box-data/ ~/wis2box-data/synop_202501030900.txt
    ```

    确保错误已解决。

一旦您成功运行脚本，您将看到一条消息，表明文件已复制到 MinIO，并且您应该在 MQTT Explorer 中看到您的 wis2box 实例发布的数据通知。

您还可以检查 Grafana 仪表板，确认数据是否成功导入并发布。

现在脚本已正常运行，您可以尝试使用相同的脚本将其他文件复制到 MinIO。

!!! question "导入 BUFR 格式的二进制数据"

    运行以下命令，将二进制数据文件 `bufr-example.bin` 复制到 MinIO 的 `wis2box-incoming` 存储桶中：

    ```bash
    python3 copy_file_to_incoming.py bufr-example.bin
    ```

检查 Grafana 仪表板和 MQTT Explorer，确认测试数据是否成功导入并发布。如果出现任何错误，请尝试解决。

!!! question "验证数据导入"

    对于此数据样本，MQTT broker 发布了多少条消息？

??? success "点击查看答案"

    您将在 Grafana 中看到错误报告，因为 BUFR 文件中的站点未在您的 wis2box 实例的站点列表中定义。

    如果 BUFR 文件中使用的所有站点都已在您的 wis2box 实例中定义，您应该会看到 10 条消息发布到 MQTT broker。每条通知对应一个站点的一个观测时间戳的数据。

    插件 `wis2box.data.bufr4.ObservationDataBUFR` 会将 BUFR 文件拆分为单独的 BUFR 消息，并为每个站点和观测时间戳发布一条消息。

## 使用 SFTP 导入数据
```

在 wis2box 中，MinIO 服务还可以通过 SFTP 进行访问。如果您有一个现有系统可以配置为通过 SFTP 转发数据，您可以使用这种方法作为自动化数据摄取的替代方式。

MinIO 的 SFTP 服务器绑定到主机的 8022 端口（22 端口用于 SSH）。

在本练习中，我们将演示如何使用 WinSCP 通过 SFTP 将数据上传到 MinIO。

您可以按照以下截图设置一个新的 WinSCP 连接：

<img alt="winscp-sftp-connection" src="/../assets/img/winscp-sftp-login.png" width="400">

SFTP 连接的凭据由 `WIS2BOX_STORAGE_USERNAME` 和 `WIS2BOX_STORAGE_PASSWORD` 定义，这些凭据存储在您的 `wis2box.env` 文件中，与您用于连接 MinIO UI 的凭据相同。

登录后，您将看到 wis2box 在 MinIO 中使用的存储桶：

<img alt="winscp-sftp-bucket" src="/../assets/img/winscp-buckets.png" width="600">

您可以导航到 `wis2box-incoming` 存储桶，然后进入您的数据集文件夹。您将看到在之前练习中上传的文件：

<img alt="winscp-sftp-incoming-path" src="/../assets/img/winscp-incoming-data-path.png" width="600">

!!! question "使用 SFTP 上传数据"

    下载此示例文件到您的本地计算机：

    [synop_202503030900.txt](./../sample-data/synop_202503030900.txt) （右键点击并选择“另存为”下载文件）。

    然后使用 WinSCP 中的 SFTP 会话将其上传到 MinIO 的 incoming 数据集路径。

    在 Grafana 仪表板和 MQTT Explorer 中检查数据是否成功被摄取并发布。

??? success "点击查看答案"

    您应该会看到一个新的 WIS2 数据通知已为测试站点 `0-20000-0-64400` 发布，表明数据已成功摄取并发布。

    <img alt="grafana_data_ingest" src="/../assets/img/grafana_data-ingest-test3.png" width="400"> 

    如果您使用了错误的路径，您将在日志中看到一条错误消息。

## 总结

!!! success "恭喜！"
    在本次实践中，您学会了：

    - 通过多种方法将数据上传到 MinIO 来触发 wis2box 工作流。
    - 使用 Grafana 仪表板和 wis2box 实例的日志调试数据摄取过程中的常见错误。
    - 在 Grafana 仪表板和 MQTT Explorer 中监控由您的 wis2box 发布的 WIS2 数据通知。
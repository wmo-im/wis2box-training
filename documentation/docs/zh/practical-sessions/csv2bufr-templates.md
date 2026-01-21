---
title: CSV-to-BUFR 映射模板
---

# CSV-to-BUFR 映射模板

!!! abstract "学习目标"
    在本次实践课程结束时，您将能够：

    - 为您的 CSV 数据创建一个新的 BUFR 映射模板
    - 从命令行编辑和调试自定义 BUFR 映射模板
    - 配置 CSV-to-BUFR 数据插件以使用自定义 BUFR 映射模板
    - 使用内置的 AWS 和 DAYCLI 模板将 CSV 数据转换为 BUFR

## 简介

逗号分隔值（CSV）数据文件通常用于以表格格式记录观测数据和其他数据。  
大多数用于记录传感器输出的数据记录器能够以分隔文件（包括 CSV 格式）导出观测数据。  
同样，当数据被导入数据库时，也可以很容易地以 CSV 格式的文件导出所需数据。

`wis2box csv2bufr` 模块提供了一个命令行工具，用于将 CSV 数据转换为 BUFR 格式。使用 `csv2bufr` 时，您需要提供一个 BUFR 映射模板，将 CSV 列映射到相应的 BUFR 元素。如果您不想创建自己的映射模板，可以使用内置的 AWS 和 DAYCLI 模板将 CSV 数据转换为 BUFR，但需要确保您使用的 CSV 数据格式与这些模板匹配。如果您需要解码 AWS 和 DAYCLI 模板中未包含的参数，则需要创建自己的映射模板。

在本次课程中，您将学习如何创建自己的映射模板以将 CSV 数据转换为 BUFR。您还将学习如何使用内置的 AWS 和 DAYCLI 模板将 CSV 数据转换为 BUFR。

## 准备工作

确保已使用以下命令启动 `wis2box-stack`：  
`python3 wis2box.py start`

确保已打开一个 Web 浏览器，并通过访问 `http://YOUR-HOST:9000` 打开您的实例的 MinIO UI。  
如果您不记得 MinIO 的凭据，可以在学生虚拟机的 `wis2box` 目录下的 `wis2box.env` 文件中找到。

确保已打开 MQTT Explorer，并使用凭据 `everyone/everyone` 连接到您的代理。

## 创建映射模板

`csv2bufr` 模块附带了一个命令行工具，可以使用一组 BUFR 序列和/或 BUFR 元素作为输入来创建自己的映射模板。

要查找特定的 BUFR 序列和元素，可以参考 BUFR 表：[https://confluence.ecmwf.int/display/ECC/BUFR+tables](https://confluence.ecmwf.int/display/ECC/BUFR+tables)。

### csv2bufr 映射命令行工具

要访问 `csv2bufr` 命令行工具，您需要登录到 `wis2box-api` 容器：

```bash
cd ~/wis2box
python3 wis2box-ctl.py login wis2box-api
```

打印 `csv2bufr mapping` 命令的帮助页面：

```bash
csv2bufr mappings --help
```

帮助页面显示了两个子命令：

- `csv2bufr mappings create`：创建一个新的映射模板
- `csv2bufr mappings list`：列出系统中可用的映射模板

!!! Note "csv2bufr mapping list"

    `csv2bufr mapping list` 命令将显示系统中可用的映射模板。  
    默认模板存储在容器中的目录 `/opt/wis2box/csv2bufr/templates` 中。

    要与系统共享自定义映射模板，可以将它们存储在由 `$CSV2BUFR_TEMPLATES` 定义的目录中，该目录在容器中默认设置为 `/data/wis2box/mappings`。由于容器中的目录 `/data/wis2box/mappings` 挂载到主机上的目录 `$WIS2BOX_HOST_DATADIR/mappings`，因此您将在主机上的目录 `$WIS2BOX_HOST_DATADIR/mappings` 中找到您的自定义映射模板。

让我们尝试使用 `csv2bufr mapping create` 命令创建一个新的自定义映射模板，输入 BUFR 序列 301150 和 BUFR 元素 012101：

```bash
csv2bufr mappings create 301150 012101 --output /data/wis2box/mappings/my_custom_template.json
```

您可以使用 `cat` 命令检查刚刚创建的映射模板的内容：

```bash
cat /data/wis2box/mappings/my_custom_template.json
```

!!! question "检查映射模板"

    有多少个 CSV 列被映射到 BUFR 元素？每个 BUFR 元素映射的 CSV 标题是什么？

??? success "点击查看答案"
    
    您创建的映射模板将 **5** 个 CSV 列映射到 BUFR 元素，即序列 301150 中的 4 个 BUFR 元素加上 BUFR 元素 012101。

    以下 CSV 列被映射到 BUFR 元素：

    - **wigosIdentifierSeries** 映射到 `"eccodes_key": "#1#wigosIdentifierSeries"`（BUFR 元素 001125）
    - **wigosIssuerOfIdentifier** 映射到 `"eccodes_key": "#1#wigosIssuerOfIdentifier`（BUFR 元素 001126）
    - **wigosIssueNumber** 映射到 `"eccodes_key": "#1#wigosIssueNumber"`（BUFR 元素 001127）
    - **wigosLocalIdentifierCharacter** 映射到 `"eccodes_key": "#1#wigosLocalIdentifierCharacter"`（BUFR 元素 001128）
    - **airTemperature** 映射到 `"eccodes_key": "#1#airTemperature"`（BUFR 元素 012101）

您创建的映射模板缺少关于观测的关键元数据，例如观测的日期和时间以及站点的经纬度。

接下来，我们将更新映射模板并添加以下序列：

- **301011**：日期（年、月、日）
- **301012**：时间（小时、分钟）
- **301023**：位置（经纬度，粗精度）

以及以下元素：

- **010004**：气压
- **007031**：气压计高度（相对于平均海平面）

执行以下命令更新映射模板：

```bash
csv2bufr mappings create 301150 301011 301012 301023 007031 012101 010004  --output /data/wis2box/mappings/my_custom_template.json
```

再次检查映射模板的内容：

```bash
cat /data/wis2box/mappings/my_custom_template.json
```

!!! question "检查更新后的映射模板"

    现在有多少个 CSV 列被映射到 BUFR 元素？每个 BUFR 元素映射的 CSV 标题是什么？

??? success "点击查看答案"
    
    您创建的映射模板现在将 **18** 个 CSV 列映射到 BUFR 元素：
    - 来自 BUFR 序列 301150 的 4 个 BUFR 元素
    - 来自 BUFR 序列 301011 的 3 个 BUFR 元素
    - 来自 BUFR 序列 301012 的 2 个 BUFR 元素
    - 来自 BUFR 序列 301023 的 2 个 BUFR 元素
    - BUFR 元素 007031
    - BUFR 元素 012101

    以下 CSV 列被映射到 BUFR 元素：

    - **wigosIdentifierSeries** 映射到 `"eccodes_key": "#1#wigosIdentifierSeries"`（BUFR 元素 001125）
    - **wigosIssuerOfIdentifier** 映射到 `"eccodes_key": "#1#wigosIssuerOfIdentifier`（BUFR 元素 001126）
    - **wigosIssueNumber** 映射到 `"eccodes_key": "#1#wigosIssueNumber"`（BUFR 元素 001127）
    - **wigosLocalIdentifierCharacter** 映射到 `"eccodes_key": "#1#wigosLocalIdentifierCharacter"`（BUFR 元素 001128）
    - **year** 映射到 `"eccodes_key": "#1#year"`（BUFR 元素 004001）
    - **month** 映射到 `"eccodes_key": "#1#month"`（BUFR 元素 004002）
    - **day** 映射到 `"eccodes_key": "#1#day"`（BUFR 元素 004003）
    - **hour** 映射到 `"eccodes_key": "#1#hour"`（BUFR 元素 004004）
    - **minute** 映射到 `"eccodes_key": "#1#minute"`（BUFR 元素 004005）
    - **latitude** 映射到 `"eccodes_key": "#1#latitude"`（BUFR 元素 005002）
    - **longitude** 映射到 `"eccodes_key": "#1#longitude"`（BUFR 元素 006002）
    - **heightOfBarometerAboveMeanSeaLevel** 映射到 `"eccodes_key": "#1#heightOfBarometerAboveMeanSeaLevel"`（BUFR 元素 007031）
    - **airTemperature** 映射到 `"eccodes_key": "#1#airTemperature"`（BUFR 元素 012101）
    - **nonCoordinatePressure** 映射到 `"eccodes_key": "#1#nonCoordinatePressure"`（BUFR 元素 010004）

检查目录 `/wis2box-api/data-conversion-exercises` 中文件 `custom_template_data.csv` 的内容：

```bash
cd /wis2box-api/data-conversion-exercises
cat custom_template_data.csv
```

请注意，此 CSV 文件的表头与您创建的映射模板中的表头相同。

为了测试数据转换，我们可以使用 `csv2bufr` 命令行工具，通过我们创建的映射模板将 CSV 文件转换为 BUFR：

```bash
csv2bufr data transform --bufr-template my_custom_template /wis2box-api/data-conversion-exercises/custom_template_data.csv
```

您应该会看到以下输出：

```bash
CLI:    ... Transforming /wis2box-api/data-conversion-exercises/custom_template_data.csv to BUFR ...
CLI:    ... Processing subsets:
CLI:    ..... 94 bytes written to ./WIGOS_0-20000-0-15015_20250412T210000.bufr4
CLI:    End of processing, exiting.
```

!!! question "检查 BUFR 文件的内容"
    
    您如何检查刚刚创建的 BUFR 文件的内容，并验证它是否正确编码了数据？

??? success "点击查看答案"

    您可以使用 `bufr_dump -p` 命令检查刚刚创建的 BUFR 文件的内容。
    该命令将以人类可读的格式显示 BUFR 文件的内容。

    ```bash
    bufr_dump -p ./WIGOS_0-20000-0-15015_20250412T210000.bufr4
    ```

    在输出中，您将看到映射模板中定义的 BUFR 元素的值，例如 "airTemperature" 将显示为：
    
    ```bash
    airTemperature=298.15
    ```

您现在可以退出容器：

```bash
exit
```

### 在 wis2box 中使用映射模板

为了确保 wis2box-api 容器能够识别新的映射模板，您需要重启该容器：

```bash
docker restart wis2box-api
```

现在，您可以在 wis2box-webapp 中配置您的数据集，以使用 CSV 到 BUFR 转换插件的自定义映射模板。

wis2box-webapp 将自动检测您创建的映射模板，并在 CSV 到 BUFR 转换插件的模板列表中提供该模板。

点击您在之前实践课程中创建的数据集，然后点击插件名称为 "CSV data converted to BUFR" 旁边的 "UPDATE" 按钮：

<img alt="显示 wis2box-webapp 数据集编辑器的图像" src="/../assets/img/wis2box-webapp-data-mapping-update-csv2bufr.png"/>

您应该会在可用模板列表中看到您创建的新模板：

<img alt="显示 wis2box-webapp 中 csv2bufr 模板的图像" src="/../assets/img/wis2box-webapp-csv2bufr-templates.png"/>

!!! hint

    如果您没有看到新创建的模板，请尝试刷新页面或在新的隐身窗口中打开页面。

目前，请保持 AWS 模板的默认选择（点击右上角关闭插件配置）。

## 使用 'AWS' 模板

'AWS' 模板提供了将 CSV 数据映射到 BUFR 序列 301150 和 307096 的模板，以支持最低 GBON 要求。

AWS 模板的描述可以在此处找到 [aws-template](./../csv2bufr-templates/aws-template.md)。

### 查看 aws-example 输入数据

从以下链接下载本次练习的示例文件：

[aws-example.csv](./../sample-data/aws-example.csv)

在编辑器中打开您下载的文件并检查内容：

!!! question
    检查日期、时间和标识字段（WIGOS 和传统标识符），您注意到了什么？今天的日期将如何表示？

??? success "点击查看答案"
    每列包含一条信息。例如，日期被分为年、月和日，这与数据在 BUFR 中的存储方式一致。今天的日期将分布在 "year"、"month" 和 "day" 列中。同样，时间需要分为 "hour" 和 "minute"，WIGOS 站点标识符需要分为其各自的组件。

!!! question
    查看数据文件，缺失数据是如何编码的？
    
??? success "点击查看答案"
    文件中的缺失数据通过空单元格表示。在 CSV 文件中，这将被编码为 ``,,``。请注意，这是一个空单元格，而不是编码为零长度字符串，例如 ``,"",``。

!!! hint "缺失数据"
    需要注意的是，数据可能由于多种原因缺失，例如传感器故障或参数未被观测。在这些情况下，缺失数据可以按照上述答案进行编码，报告中的其他数据仍然有效。

### 更新示例文件

更新您下载的示例文件以使用今天的日期和时间，并将 WIGOS 站点标识符更改为您在 wis2box-webapp 中注册的站点。

### 上传数据到 MinIO 并检查结果

进入 MinIO UI，并使用 `wis2box.env` 文件中的凭据登录。

导航到 **wis2box-incoming** 并点击 "Create new path" 按钮：

<img alt="显示 MinIO UI 中创建新路径按钮的图像" src="/../assets/img/minio-create-new-path.png"/>

在 MinIO 存储桶中创建一个新文件夹，该文件夹与您使用模板='weather/surface-weather-observations/synop' 创建的数据集的 dataset-id 匹配：

<img alt="显示 MinIO UI 中创建新路径的图像" src="/../assets/img/minio-create-new-path-metadata_id.png"/>

将您下载的示例文件上传到您在 MinIO 存储桶中创建的文件夹中：

<img alt="显示 MinIO UI 中上传 aws-example 的图像" src="/../assets/img/minio-upload-aws-example.png"/></center>

检查 Grafana 仪表板 `http://YOUR-HOST:3000`，查看是否有任何 WARNINGS 或 ERRORS。如果有，请尝试修复并重复练习。

检查 MQTT Explorer，查看是否接收到 WIS2 数据通知。

如果您成功导入了数据，您应该会在 MQTT Explorer 中的主题 `origin/a/wis2/<centre-id>/data/weather/surface-weather-observations/synop` 下看到 3 条通知，这些通知对应于您报告数据的 3 个站点：

<img width="450" alt="显示上传 AWS 后 MQTT Explorer 的图像" src="/../assets/img/mqtt-explorer-aws-upload.png"/>

## 使用 'DayCLI' 模板

**DayCLI** 模板提供了将每日气候 CSV 数据映射到 BUFR 序列 307075 的模板，以支持每日气候数据的报告。

DAYCLI 模板的描述可以在此处找到 [daycli-template](./../csv2bufr-templates/daycli-template.md)。

要在 WIS2 上共享此数据，您需要在 wis2box-webapp 中创建一个新数据集，该数据集具有正确的 WIS2 主题层次结构，并使用 DAYCLI 模板将 CSV 数据转换为 BUFR。

### 为发布 DAYCLI 消息创建 wis2box 数据集

进入 wis2box-webapp 的数据集编辑器并创建一个新数据集。使用与之前实践课程中相同的 centre-id，并选择 **Data Type='climate/surface-based-observations/daily'**：

<img alt="在 wis2box-webapp 中为 DAYCLI 创建新数据集" src="/../assets/img/wis2box-webapp-create-dataset-daycli.png"/>

点击 "CONTINUE TO FORM"，为您的数据集添加描述，设置边界框，并提供数据集的联系信息。完成所有部分后，点击 'VALIDATE FORM' 并检查表单。

查看数据集的数据插件。点击插件名称为 "CSV data converted to BUFR" 旁边的 "UPDATE" 按钮，您将看到模板设置为 **DayCLI**：

<img alt="将数据插件更新为使用 DAYCLI 模板" src="/../assets/img/wis2box-webapp-update-data-plugin-daycli.png"/>

关闭插件配置，并使用您在之前实践课程中创建的身份验证令牌提交表单。

现在，您应该在 wis2box-webapp 中有第二个数据集，该数据集配置为使用 DAYCLI 模板将 CSV 数据转换为 BUFR。

### 查看 daycli-example 输入数据

从以下链接下载本次练习的示例文件：

[daycli-example.csv](./../sample-data/daycli-example.csv)

在编辑器中打开您下载的文件并检查内容：

!!! question
    daycli 模板中包含了哪些额外变量？

??? success "点击查看答案"
    daycli 模板包含了关于温度和湿度的仪器位置和测量质量分类的重要元数据、质量控制标志以及关于如何计算每日平均温度的信息。

### 更新示例文件

示例文件包含一个月中每天的数据行，并报告一个站点的数据。更新您下载的示例文件以使用今天的日期和时间，并将 WIGOS 站点标识符更改为您在 wis2box-webapp 中注册的站点。

### 上传数据到 MinIO 并检查结果

如前所述，您需要将数据上传到 MinIO 中的 'wis2box-incoming' 存储桶，以便通过 csv2bufr 转换器进行处理。这次，您需要在 MinIO 存储桶中创建一个新文件夹，该文件夹名称需与您使用模板 `climate/surface-based-observations/daily` 创建的数据集的 dataset-id 匹配，该 dataset-id 将与您在之前练习中使用的 dataset-id 不同：

<img alt="Image showing MinIO UI with DAYCLI-example uploaded" src="/../assets/img/minio-upload-daycli-example.png"/></center>

上传数据后，请检查 Grafana 仪表板中是否没有 WARNINGS 或 ERRORS，并检查 MQTT Explorer 是否接收到 WIS2 数据通知。

如果您成功导入了数据，您应该会在 MQTT Explorer 中的主题 `origin/a/wis2/<centre-id>/data/climate/surface-based-observations/daily` 上看到 30 条通知，表示您报告的月份中有 30 天的数据：

<img width="450" alt="Image showing MQTT explorer after uploading DAYCLI" src="/../assets/img/mqtt-daycli-template-success.png"/>

## 结论

!!! success "恭喜"
    在本次实践课程中，您学到了：

    - 如何创建自定义映射模板，将 CSV 数据转换为 BUFR
    - 如何使用内置的 AWS 和 DAYCLI 模板，将 CSV 数据转换为 BUFR
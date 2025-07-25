---
title: CSV至BUFR映射模板
---

# CSV至BUFR映射模板

!!! abstract "学习成果"
    通过本实践课程，您将能够：

    - 为您的CSV数据创建一个新的BUFR映射模板
    - 从命令行编辑和调试您的自定义BUFR映射模板
    - 配置CSV至BUFR数据插件以使用自定义BUFR映射模板
    - 使用内置的AWS和DAYCLI模板将CSV数据转换为BUFR

## 引言

逗号分隔值（CSV）数据文件通常用于以表格格式记录观测数据和其他数据。
大多数用于记录传感器输出的数据记录器能够导出观测结果为分隔文件，包括CSV格式。
同样，当数据被摄入数据库时，很容易以CSV格式导出所需数据。

wis2box的csv2bufr模块提供了一个命令行工具，用于将CSV数据转换为BUFR格式。使用csv2bufr时，您需要提供一个BUFR映射模板，该模板将CSV列映射到相应的BUFR元素。如果您不想创建自己的映射模板，您可以使用内置的AWS和DAYCLI模板将CSV数据转换为BUFR，但您需要确保所使用的CSV数据格式适用于这些模板。如果您想解码AWS和DAYCLI模板中未包含的参数，您将需要创建自己的映射模板。

在本课程中，您将学习如何为将CSV数据转换为BUFR创建自己的映射模板。您还将学习如何使用内置的AWS和DAYCLI模板将CSV数据转换为BUFR。

## 准备工作

确保已使用`python3 wis2box.py start`启动wis2box堆栈

确保您的浏览器已打开并通过访问`http://YOUR-HOST:9000`连接到您实例的MinIO UI。
如果您忘记了MinIO凭据，可以在学生VM的`wis2box`目录中的`wis2box.env`文件中找到它们。

确保您已打开MQTT Explorer并使用凭据`everyone/everyone`连接到您的broker。

## 创建映射模板

csv2bufr模块附带一个命令行工具，使用一组BUFR序列和/或BUFR元素作为输入来创建您自己的映射模板。

要查找特定的BUFR序列和元素，您可以参考BUFR表格网址[https://confluence.ecmwf.int/display/ECC/BUFR+tables](https://confluence.ecmwf.int/display/ECC/BUFR+tables)。

### csv2bufr映射命令行工具

要访问csv2bufr命令行工具，您需要登录到wis2box-api容器：

```bash
cd ~/wis2box
python3 wis2box-ctl.py login wis2box-api
```

要打印命令`csv2bufr mapping`的帮助页面：

```bash
csv2bufr mappings --help
```

帮助页面显示2个子命令：

- `csv2bufr mappings create`：创建一个新的映射模板
- `csv2bufr mappings list`：列出系统中可用的映射模板

!!! Note "csv2bufr mapping list"

    `csv2bufr mapping list`命令将显示系统中可用的映射模板。
    默认模板存储在容器中的目录`/opt/wis2box/csv2bufr/templates`中。

    要与系统共享自定义映射模板，您可以将它们存储在由`$CSV2BUFR_TEMPLATES`定义的目录中，该目录在容器中默认设置为`/data/wis2box/mappings`。由于容器中的目录`/data/wis2box/mappings`挂载到主机上的目录`$WIS2BOX_HOST_DATADIR/mappings`，您将在主机上的目录`$WIS2BOX_HOST_DATADIR/mappings`中找到您的自定义映射模板。

让我们尝试使用命令`csv2bufr mapping create`创建一个新的自定义映射模板，输入BUFR序列301150加BUFR元素012101。

```bash
csv2bufr mappings create 301150 012101 --output /data/wis2box/mappings/my_custom_template.json
```

您可以使用`cat`命令检查您刚创建的映射模板的内容：

```bash
cat /data/wis2box/mappings/my_custom_template.json
```

!!! question "检查映射模板"

    有多少CSV列被映射到BUFR元素？每个BUFR元素的CSV标题是什么？

??? success "点击显示答案"
    
    您创建的映射模板将**5**个CSV列映射到BUFR元素，即序列301150中的4个BUFR元素加上BUFR元素012101。

    以下CSV列被映射到BUFR元素：

    - **wigosIdentifierSeries** 映射到 `"eccodes_key": "#1#wigosIdentifierSeries"` (BUFR元素001125)
    - **wigosIssuerOfIdentifier** 映射到 `"eccodes_key": "#1#wigosIssuerOfIdentifier` (BUFR元素001126)
    - **wigosIssueNumber** 映射到 `"eccodes_key": "#1#wigosIssueNumber"` (BUFR元素001127)
    - **wigosLocalIdentifierCharacter** 映射到 `"eccodes_key": "#1#wigosLocalIdentifierCharacter"` (BUFR元素001128)
    - **airTemperature** 映射到 `"eccodes_key": "#1#airTemperature"` (BUFR元素012101)

您创建的映射模板缺少有关观测的重要元数据，观测的日期和时间，以及站点的纬度和经度。

接下来我们将更新映射模板并添加以下序列：

- **301011** 用于日期（年、月、日）
- **301012** 用于时间（小时、分钟）
- **301023** 用于位置（粗略精度的纬度/经度）

以及以下元素：

- **010004** 用于气压
- **007031** 用于海平面上方的气压计高度

执行以下命令以更新映射模板：

```bash
csv2bufr mappings create 301150 301011 301012 301023 007031 012101 010004  --output /data/wis2box/mappings/my_custom_template.json
```

并再次检查映射模板的内容：

```bash
cat /data/wis2box/mappings/my_custom_template.json
```

!!! question "检查更新后的映射模板"

    现在有多少CSV列被映射到BUFR元素？每个BUFR元素的CSV标题是什么？

??? success "点击显示答案"
    
    您创建的映射模板现在将**18**个CSV列映射到BUFR元素：
    - 来自BUFR序列301150的4个BUFR元素
    - 来自BUFR序列301011的3个BUFR元素
    - 来自BUFR序列301012的2个BUFR元素
    - 来自BUFR序列301023的2个BUFR元素
    - BUFR元素007031
    - BUFR元素012101

    以下CSV列被映射到BUFR元素：

    - **wigosIdentifierSeries** 映射到 `"eccodes_key": "#1#wigosIdentifierSeries"` (BUFR元素001125)
    - **wigosIssuerOfIdentifier** 映射到 `"eccodes_key": "#1#wigosIssuerOfIdentifier` (BUFR元素001126)
    - **wigosIssueNumber** 映射到 `"eccodes_key": "#1#wigosIssueNumber"` (BUFR元素001127)
    - **wigosLocalIdentifierCharacter** 映射到 `"eccodes_key": "#1#wigosLocalIdentifierCharacter"` (BUFR元素001128)
    - **year** 映射到 `"eccodes_key": "#1#year"` (BUFR元素004001)
    - **month** 映射到 `"eccodes_key": "#1#month"` (BUFR元素004002)
    - **day** 映射到 `"eccodes_key": "#1#day"` (BUFR元素004003)
    - **hour** 映射到 `"eccodes_key": "#1#hour"` (BUFR元素004004)
    - **minute** 映射到 `"eccodes_key": "#1#minute"` (BUFR元素004005)
    - **latitude** 映射到 `"eccodes_key": "#1#latitude"` (BUFR元素005002)
    - **longitude** 映射到 `"eccodes_key": "#1#longitude"` (BUFR元素006002)
    - **heightOfBarometerAboveMeanSeaLevel"** 映射到 `"eccodes_key": "#1#heightOfBarometerAboveMeanSeaLevel"` (BUFR元素007031)
    - **airTemperature** 映射到 `"eccodes_key": "#1#airTemperature"` (BUFR元素012101)
    - **nonCoordinatePressure** 映射到 `"eccodes_key": "#1#nonCoordinatePressure"` (BUFR元素010004)

检查文件夹`/root/data-conversion-exercises`中的文件`custom_template_data.csv`的内容：

```bash
cat /root/data-conversion-exercises/custom_template_data.csv
```

注意，此CSV文件的标题与您创建的映射模板中的CSV标题相同。

为了测试数据转换，我们可以使用`csv2bufr`命令行工具使用我们创建的映射模板将CSV文件转换为BUFR：

```bash
csv2bufr data transform --bufr-template my_custom_template /root/data-conversion-exercises/custom_template_data.csv
```

您应该看到以下输出：

```bash
CLI:    ... Transforming /root/data-conversion-exercises/custom_template_data.csv to BUFR ...
CLI:    ... Processing subsets:
CLI:    ..... 94 bytes written to ./WIGOS_0-20000-0-15015_20250412T210000.bufr4
CLI:    End of processing, exiting.
```

!!! question "检查BUFR文件的内容"
    
    您如何检查您刚创建的BUFR文件的内容并验证其是否正确编码了数据？

??? success "点击显示答案"

    您可以使用`bufr_dump -p`命令检查您刚创建的BUFR文件的内容。
    该命令将以人类可读的格式显示BUFR文件的内容。

    ```bash
    bufr_dump -p ./WIGOS_0-20000-0-15015_20250412T210000.bufr4
    ```

    在输出中，您将看到您在模板中映射的BUFR元素的值，例如"airTemperature"将显示：
    
    ```bash
    airTemperature=298.15
    ```

现在您可以退出容器：

```bash
exit
```

### 在wis2box中使用映射模板

为确保新的映射模板被wis2box-api容器识别，您需要重启容器：

```bash
docker restart wis2box-api
```

您现在可以在wis2box-webapp中配置您的数据集，以使用自定义映射模板进行CSV至BUFR转换插件。

wis2box-webapp将自动检测您创建的映射模板，并在CSV至BUFR转换插件的模板列表中显示。

点击您在上一个实践课程中创建的数据集，然后点击名为"CSV data converted to BUFR"的插件旁边的"UPDATE"：

<img alt="Image showing the dataset editor in the wis2box-webapp" src="/../assets/img/wis2box-webapp-data-mapping-update-csv2bufr.png"/>

您应该在可用模板列表中看到您创建的新模板：

<img alt="Image showing the csv2bufr-templates in the wis2box-webapp" src="/../assets/img/wis2box-webapp-csv2bufr-templates.png"/>

!!! hint

    注意，如果您看不到您创建的新模板，请尝试刷新页面或在新的隐身窗口中打开。

现在保持AWS模板的默认选择（点击右上角关闭插件配置）。

## 使用'AWS'模板

'AWS'模板提供了将CSV数据转换为BUFR序列301150, 307096的映射模板，以支持最低GBON要求。

AWS模板的描述可以在此处找到 [aws-template](./../csv2bufr-templates/aws-template.md).

### 审查aws-example输入数据

从下面的链接下载本练习的示例：

[aws-example.csv](./../../sample-data/aws-example.csv)

打开您下载的文件并检查内容：

!!! question
    检查日期、时间和标识字段（WIGOS和传统标识符），您注意到了什么？今天的日期将如何表示？

??? success "点击显示答案"
    每列包含单一信息。例如，日期被分为年、月和日，反映了数据在BUFR中的存储方式。今天的日期将跨越"year", "month"和"day"列分开表示。同样，时间需要分为"hour"和"minute"，WIGOS站点标识符需要分解为其各个组成部分。

!!! question
    查看数据文件，缺失数据如何编码？
    
??? success "点击显示答案"

文件中缺失的数据由空单元格表示。在 CSV 文件中，这将被编码为 ``,,``。注意，这是一个空单元格，而不是编码为零长度字符串，例如 ``,"",``。

!!! hint "缺失数据"
    众所周知，数据可能因各种原因缺失，无论是由于传感器故障还是未观测到该参数。在这些情况下，可以按照上述答案编码缺失数据，报告中的其他数据仍然有效。

### 更新示例文件

更新您下载的示例文件，使用今天的日期和时间，并更改 WIGOS 站点标识符，以使用您在 wis2box-webapp 中注册的站点。

### 上传数据到 MinIO 并检查结果

导航到 MinIO UI 并使用 `wis2box.env` 文件中的凭据登录。

导航到 **wis2box-incoming** 并点击“创建新路径”按钮：

<img alt="Image showing MinIO UI with the create folder button highlighted" src="/../assets/img/minio-create-new-path.png"/>

在 MinIO 桶中创建一个与您使用模板创建的数据集的 dataset-id 匹配的新文件夹='weather/surface-weather-observations/synop':

<img alt="Image showing MinIO UI with the create folder button highlighted" src="/../assets/img/minio-create-new-path-metadata_id.png"/>

将您下载的示例文件上传到您在 MinIO 桶中创建的文件夹：

<img alt="Image showing MinIO UI with aws-example uploaded" src="/../assets/img/minio-upload-aws-example.png"/>

检查位于 `http://YOUR-HOST:3000` 的 Grafana 仪表板，查看是否有任何警告或错误。如果看到任何问题，请尝试修复它们并重复此练习。

检查 MQTT Explorer 以查看是否收到 WIS2 数据通知。

如果您成功摄取了数据，您应该在主题 `origin/a/wis2/<centre-id>/data/weather/surface-weather-observations/synop` 上的 MQTT explorer 中看到 3 个通知，这是您报告的 3 个站点的数据：

<img width="450" alt="Image showing MQTT explorer after uploading AWS" src="/../assets/img/mqtt-explorer-aws-upload.png"/>

## 使用 'DayCLI' 模板

**DayCLI** 模板提供了一个映射模板，用于将日常气候 CSV 数据转换为 BUFR 序列 307075，以支持报告日常气候数据。

DAYCLI 模板的描述可以在此处找到 [daycli-template](./../csv2bufr-templates/daycli-template.md)。

要在 WIS2 上共享此数据，您需要在 wis2box-webapp 中创建一个新的数据集，该数据集具有正确的 WIS2 主题层次结构，并使用 DAYCLI 模板将 CSV 数据转换为 BUFR。

### 为发布 DAYCLI 消息创建 wis2box 数据集

转到 wis2box-webapp 中的数据集编辑器并创建一个新数据集。使用与之前实践课程中相同的 centre-id，并选择 **Data Type='climate/surface-based-observations/daily'**：

<img alt="Create a new dataset in the wis2box-webapp for DAYCLI" src="/../assets/img/wis2box-webapp-create-dataset-daycli.png"/>

点击“继续填写表单”并为您的数据集添加描述，设置边界框并提供数据集的联系信息。填写完所有部分后，点击‘验证表单’并检查表单。

查看数据集的数据插件。点击名为“CSV 数据转换为 BUFR”的插件旁边的“更新”，您将看到模板设置为 **DayCLI**：

<img alt="Update the data plugin for the dataset to use the DAYCLI template" src="/../assets/img/wis2box-webapp-update-data-plugin-daycli.png"/>

关闭插件配置并使用您在上一个实践课程中创建的认证令牌提交表单。

您现在应该在 wis2box-webapp 中有第二个配置为使用 DAYCLI 模板将 CSV 数据转换为 BUFR 的数据集。

### 审查 daycli-example 输入数据

从下面的链接下载此练习的示例：

[daycli-example.csv](./../../sample-data/daycli-example.csv)

在编辑器中打开您下载的文件并检查内容：

!!! question
    daycli 模板中包含哪些额外的变量？

??? success "点击以显示答案"
    daycli 模板包括有关仪器放置和温度及湿度测量质量分类的重要元数据，质量控制标志以及如何计算日平均温度的信息。

### 更新示例文件

示例文件包含一个月中每天的一行数据，并报告一个站点的数据。更新您下载的示例文件，使用今天的日期和时间，并更改 WIGOS 站点标识符，以使用您在 wis2box-webapp 中注册的站点。

### 上传数据到 MinIO 并检查结果

与之前一样，您需要将数据上传到 MinIO 中的 'wis2box-incoming' 桶中，以便由 csv2bufr 转换器处理。这次您需要在 MinIO 桶中创建一个与您使用模板创建的数据集的 dataset-id 匹配的新文件夹='climate/surface-based-observations/daily'，这将与您在上一个练习中使用的 dataset-id 不同：

<img alt="Image showing MinIO UI with DAYCLI-example uploaded" src="/../assets/img/minio-upload-daycli-example.png"/>

上传数据后，在 Grafana 仪表板中检查是否有任何警告或错误，并检查 MQTT Explorer 以查看是否收到 WIS2 数据通知。

如果您成功摄取了数据，您应该在主题 `origin/a/wis2/<centre-id>/data/climate/surface-based-observations/daily` 上的 MQTT explorer 中看到 30 个通知，这是您报告的月份中 30 天的数据：

<img width="450" alt="Image showing MQTT explorer after uploading DAYCLI" src="/../assets/img/mqtt-daycli-template-success.png"/>

## 结论

!!! success "恭喜"
    在这个实践课程中，您已经学会了：

    - 如何创建自定义映射模板将 CSV 数据转换为 BUFR
    - 如何使用内置的 AWS 和 DAYCLI 模板将 CSV 数据转换为 BUFR
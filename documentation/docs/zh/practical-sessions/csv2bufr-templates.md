---
title: CSV 至 BUFR 映射模板
---

# CSV 至 BUFR 映射模板

!!! abstract "学习成果"
    通过本实践课程，您将能够：

    - 为您的 CSV 数据创建一个新的 BUFR 映射模板
    - 从命令行编辑和调试您的自定义 BUFR 映射模板
    - 配置 CSV 至 BUFR 数据插件以使用自定义 BUFR 映射模板
    - 使用内置的 AWS 和 DAYCLI 模板将 CSV 数据转换为 BUFR

## 引言

逗号分隔值（CSV）数据文件通常用于以表格格式记录观测数据和其他数据。
大多数用于记录传感器输出的数据记录器能够导出观测结果为分隔文件，包括 CSV 格式。
同样，当数据被摄入数据库时，很容易以 CSV 格式导出所需数据。

wis2box 的 csv2bufr 模块提供了一个命令行工具，用于将 CSV 数据转换为 BUFR 格式。使用 csv2bufr 时，您需要提供一个 BUFR 映射模板，该模板将 CSV 列映射到相应的 BUFR 元素。如果您不想创建自己的映射模板，您可以使用内置的 AWS 和 DAYCLI 模板将 CSV 数据转换为 BUFR，但您需要确保所使用的 CSV 数据格式正确适用于这些模板。如果您想解码 AWS 和 DAYCLI 模板中未包含的参数，您将需要创建自己的映射模板。

在本课程中，您将学习如何为将 CSV 数据转换为 BUFR 创建自己的映射模板。您还将学习如何使用内置的 AWS 和 DAYCLI 模板将 CSV 数据转换为 BUFR。

## 准备工作

确保已使用 `python3 wis2box.py start` 启动 wis2box-stack。

确保您的浏览器已打开并通过 `http://YOUR-HOST:9000` 访问您实例的 MinIO UI。
如果您忘记了 MinIO 凭据，可以在学生 VM 上的 `wis2box` 目录中的 `wis2box.env` 文件中找到它们。

确保您已打开 MQTT Explorer 并使用凭据 `everyone/everyone` 连接到您的 broker。

## 创建映射模板

csv2bufr 模块附带一个命令行工具，使用一组 BUFR 序列和/或 BUFR 元素作为输入来创建您自己的映射模板。

要查找特定的 BUFR 序列和元素，您可以参考 BUFR 表格网址 [https://confluence.ecmwf.int/display/ECC/BUFR+tables](https://confluence.ecmwf.int/display/ECC/BUFR+tables)。

### csv2bufr 映射命令行工具

要访问 csv2bufr 命令行工具，您需要登录到 wis2box-api 容器：

```bash
cd ~/wis2box
python3 wis2box-ctl.py login wis2box-api
```

要打印 `csv2bufr mapping` 命令的帮助页面：

```bash
csv2bufr mappings --help
```

帮助页面显示 2 个子命令：

- `csv2bufr mappings create`：创建一个新的映射模板
- `csv2bufr mappings list`：列出系统中可用的映射模板

!!! Note "csv2bufr mapping list"

    `csv2bufr mapping list` 命令将向您展示系统中可用的映射模板。
    默认模板存储在容器中的目录 `/opt/wis2box/csv2bufr/templates` 中。

    要将自定义映射模板与系统共享，您可以将它们存储在由 `$CSV2BUFR_TEMPLATES` 定义的目录中，该目录在容器中默认设置为 `/data/wis2box/mappings`。由于容器中的目录 `/data/wis2box/mappings` 被挂载到主机上的目录 `$WIS2BOX_HOST_DATADIR/mappings`，您将在主机上的目录 `$WIS2BOX_HOST_DATADIR/mappings` 中找到您的自定义映射模板。

让我们尝试使用 `csv2bufr mapping create` 命令创建一个新的自定义映射模板，输入 BUFR 序列 301150 加 BUFR 元素 012101。

```bash
csv2bufr mappings create 301150 012101 --output /data/wis2box/mappings/my_custom_template.json
```

您可以使用 `cat` 命令检查您刚刚创建的映射模板的内容：

```bash
cat /data/wis2box/mappings/my_custom_template.json
```

!!! question "检查映射模板"

    有多少 CSV 列被映射到 BUFR 元素？每个 BUFR 元素的 CSV 标题是什么？

??? success "点击以显示答案"
    
    您创建的映射模板将 **5** 个 CSV 列映射到 BUFR 元素，即序列 301150 中的 4 个 BUFR 元素加上 BUFR 元素 012101。 

    下列 CSV 列被映射到 BUFR 元素：

    - **wigosIdentifierSeries** 映射到 `"eccodes_key": "#1#wigosIdentifierSeries"` (BUFR 元素 001125)
    - **wigosIssuerOfIdentifier** 映射到 `"eccodes_key": "#1#wigosIssuerOfIdentifier` (BUFR 元素 001126)
    - **wigosIssueNumber** 映射到 `"eccodes_key": "#1#wigosIssueNumber"` (BUFR 元素 001127)
    - **wigosLocalIdentifierCharacter** 映射到 `"eccodes_key": "#1#wigosLocalIdentifierCharacter"` (BUFR 元素 001128)
    - **airTemperature** 映射到 `"eccodes_key": "#1#airTemperature"` (BUFR 元素 012101)

您创建的映射模板缺少有关观测的重要元数据，观测的日期和时间，以及站点的纬度和经度。

接下来我们将更新映射模板并添加以下序列：
    
- **301011** 用于日期（年、月、日）
- **301012** 用于时间（小时、分钟）
- **301023** 用于位置（粗略精度的纬度/经度）

以及以下元素：

- **010004** 用于气压
- **007031** 用于气压计高于平均海平面的高度

执行以下命令以更新映射模板：

```bash
csv2bufr mappings create 301150 301011 301012 301023 007031 012101 010004  --output /data/wis2box/mappings/my_custom_template.json
```

再次检查映射模板的内容：

```bash
cat /data/wis2box/mappings/my_custom_template.json
```

!!! question "检查更新后的映射模板"

    现在有多少 CSV 列被映射到 BUFR 元素？每个 BUFR 元素的 CSV 标题是什么？

??? success "点击以显示答案"
    
    您创建的映射模板现在将 **18** 个 CSV 列映射到 BUFR 元素：
    - 来自 BUFR 序列 301150 的 4 个 BUFR 元素
    - 来自 BUFR 序列 301011 的 3 个 BUFR 元素
    - 来自 BUFR 序列 301012 的 2 个 BUFR 元素
    - 来自 BUFR 序列 301023 的 2 个 BUFR 元素
    - BUFR 元素 007031
    - BUFR 元素 012101

    下列 CSV 列被映射到 BUFR 元素：

    - **wigosIdentifierSeries** 映射到 `"eccodes_key": "#1#wigosIdentifierSeries"` (BUFR 元素 001125)
    - **wigosIssuerOfIdentifier** 映射到 `"eccodes_key": "#1#wigosIssuerOfIdentifier` (BUFR 元素 001126)
    - **wigosIssueNumber** 映射到 `"eccodes_key": "#1#wigosIssueNumber"` (BUFR 元素 001127)
    - **wigosLocalIdentifierCharacter** 映射到 `"eccodes_key": "#1#wigosLocalIdentifierCharacter"` (BUFR 元素 001128)
    - **year** 映射到 `"eccodes_key": "#1#year"` (BUFR 元素 004001)
    - **month** 映射到 `"eccodes_key": "#1#month"` (BUFR 元素 004002)
    - **day** 映射到 `"eccodes_key": "#1#day"` (BUFR 元素 004003)
    - **hour** 映射到 `"eccodes_key": "#1#hour"` (BUFR 元素 004004)
    - **minute** 映射到 `"eccodes_key": "#1#minute"` (BUFR 元素 004005)
    - **latitude** 映射到 `"eccodes_key": "#1#latitude"` (BUFR 元素 005002)
    - **longitude** 映射到 `"eccodes_key": "#1#longitude"` (BUFR 元素 006002)
    - **heightOfBarometerAboveMeanSeaLevel"** 映射到 `"eccodes_key": "#1#heightOfBarometerAboveMeanSeaLevel"` (BUFR 元素 007031)
    - **airTemperature** 映射到 `"eccodes_key": "#1#airTemperature"` (BUFR 元素 012101)

- **nonCoordinatePressure** 映射到 `"eccodes_key": "#1#nonCoordinatePressure"`（BUFR 元素 010004）

检查目录 `/root/data-conversion-exercises` 中文件 `custom_template_data.csv` 的内容：

```bash
cat /root/data-conversion-exercises/custom_template_data.csv
```

请注意，此 CSV 文件的表头与您创建的映射模板中的 CSV 表头相同。

要测试数据转换，我们可以使用 `csv2bufr` 命令行工具，使用我们创建的映射模板将 CSV 文件转换为 BUFR：

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

!!! question "检查 BUFR 文件的内容"
    
    如何检查您刚创建的 BUFR 文件的内容，并验证其是否正确编码了数据？

??? success "点击查看答案"

    您可以使用 `bufr_dump -p` 命令来检查您刚创建的 BUFR 文件的内容。
    该命令将以人类可读的格式显示 BUFR 文件的内容。

    ```bash
    bufr_dump -p ./WIGOS_0-20000-0-15015_20250412T210000.bufr4
    ```

    在输出中，您将看到您在模板中映射的 BUFR 元素的值，例如 "airTemperature" 将显示：
    
    ```bash
    airTemperature=298.15
    ```

您现在可以退出容器：

```bash
exit
```

### 在 wis2box 中使用映射模板

为确保 wis2box-api 容器识别新的映射模板，您需要重启容器：

```bash
docker restart wis2box-api
```

您现在可以在 wis2box-webapp 中配置您的数据集，以使用 CSV 到 BUFR 转换插件的自定义映射模板。

wis2box-webapp 将自动检测到您创建的映射模板，并在 CSV 到 BUFR 转换插件的模板列表中提供。

点击您在上一个实践课程中创建的数据集，然后点击插件名称旁边的“更新”：

<img alt="显示 wis2box-webapp 中的数据集编辑器的图像" src="../../assets/img/wis2box-webapp-data-mapping-update-csv2bufr.png"/>

您应该在可用模板列表中看到您创建的新模板：

<img alt="显示 wis2box-webapp 中的 csv2bufr-templates 的图像" src="../../assets/img/wis2box-webapp-csv2bufr-templates.png"/>

!!! hint

    请注意，如果您看不到您创建的新模板，请尝试刷新页面或在新的隐身窗口中打开它。

daycli模板包括有关仪器安置和温湿度测量质量分类的重要元数据，质量控制标志以及如何计算日平均温度的信息。

### 更新示例文件

示例文件包含一个月中每天的一行数据，并报告一个站点的数据。更新您下载的示例文件，使用今天的日期和时间，并更改WIGOS站点标识符，使用您在wis2box-webapp中注册的站点。

### 将数据上传至MinIO并检查结果

与之前一样，您需要将数据上传到MinIO中的'wis2box-incoming'桶中，由csv2bufr转换器处理。这次您需要在MinIO桶中创建一个新文件夹，与您使用模板='climate/surface-based-observations/daily'创建的数据集的dataset-id匹配，这将与您在上一个练习中使用的dataset-id不同：

<img alt="显示MinIO UI与DAYCLI-example上传的图片" src="../../assets/img/minio-upload-daycli-example.png"/></center>

上传数据后，检查Grafana仪表板中是否有警告或错误，并检查MQTT Explorer以查看是否收到WIS2数据通知。

如果您成功摄取了数据，您应该在MQTT explorer上的主题`origin/a/wis2/<centre-id>/data/climate/surface-based-observations/daily`上看到30条通知，这些通知是您报告的月份中30天的数据：

<img width="450" alt="上传DAYCLI后显示MQTT explorer的图片" src="../../assets/img/mqtt-daycli-template-success.png"/>

## 结论

!!! success "恭喜"
    在这个实践环节中，您已经学会了：

    - 如何为将CSV数据转换为BUFR创建自定义映射模板
    - 如何使用内置的AWS和DAYCLI模板将CSV数据转换为BUFR
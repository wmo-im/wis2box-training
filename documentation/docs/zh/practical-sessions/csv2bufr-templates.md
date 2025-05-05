---
title: CSV转BUFR映射模板
---

# CSV转BUFR映射模板

!!! abstract "学习目标"
    完成本实践课程后,您将能够:

    - 为您的CSV数据创建新的BUFR映射模板
    - 从命令行编辑和调试自定义BUFR映射模板
    - 配置CSV转BUFR数据插件以使用自定义BUFR映射模板
    - 使用内置的AWS和DAYCLI模板将CSV数据转换为BUFR

## 简介

逗号分隔值(CSV)数据文件通常用于以表格格式记录观测和其他数据。
大多数用于记录传感器输出的数据记录器都能够以分隔文件格式导出观测数据,包括CSV格式。
同样,当数据被导入数据库时,也很容易将所需数据导出为CSV格式文件。

wis2box csv2bufr模块提供了一个命令行工具,可以将CSV数据转换为BUFR格式。使用csv2bufr时,您需要提供一个BUFR映射模板,将CSV列映射到相应的BUFR元素。如果您不想创建自己的映射模板,可以使用内置的AWS和DAYCLI模板将CSV数据转换为BUFR,但您需要确保使用的CSV数据格式符合这些模板的要求。如果您想解码AWS和DAYCLI模板中未包含的参数,则需要创建自己的映射模板。

在本课程中,您将学习如何创建自己的映射模板来将CSV数据转换为BUFR。您还将学习如何使用内置的AWS和DAYCLI模板将CSV数据转换为BUFR。

## 准备工作

确保已使用`python3 wis2box.py start`启动wis2box-stack

确保您已打开网络浏览器并通过访问`http://YOUR-HOST:9000`打开您实例的MinIO UI
如果您忘记了MinIO凭据,可以在学生VM上的`wis2box`目录中的`wis2box.env`文件中找到。

确保您已打开MQTT Explorer并使用凭据`everyone/everyone`连接到您的代理。

## 创建映射模板

csv2bufr模块提供了一个命令行工具,可以使用一组BUFR序列和/或BUFR元素作为输入来创建自己的映射模板。

要查找特定的BUFR序列和元素,您可以参考[https://confluence.ecmwf.int/display/ECC/BUFR+tables](https://confluence.ecmwf.int/display/ECC/BUFR+tables)上的BUFR表。

### csv2bufr映射命令行工具

要访问csv2bufr命令行工具,您需要登录到wis2box-api容器:

```bash
cd ~/wis2box
python3 wis2box-ctl.py login wis2box-api
```

要打印`csv2bufr mapping`命令的帮助页面:

```bash
csv2bufr mappings --help
```

帮助页面显示2个子命令:

- `csv2bufr mappings create` : 创建新的映射模板
- `csv2bufr mappings list` : 列出系统中可用的映射模板

!!! Note "csv2bufr mapping list"

    `csv2bufr mapping list`命令将显示系统中可用的映射模板。
    默认模板存储在容器中的`/opt/wis2box/csv2bufr/templates`目录中。

    要与系统共享自定义映射模板,您可以将它们存储在由`$CSV2BUFR_TEMPLATES`定义的目录中,该目录在容器中默认设置为`/data/wis2box/mappings`。由于容器中的`/data/wis2box/mappings`目录挂载到主机上的`$WIS2BOX_HOST_DATADIR/mappings`目录,您将在主机上的`$WIS2BOX_HOST_DATADIR/mappings`目录中找到您的自定义映射模板。

让我们尝试使用`csv2bufr mapping create`命令创建一个新的自定义映射模板,使用BUFR序列301150和BUFR元素012101作为输入。

```bash
csv2bufr mappings create 301150 012101 --output /data/wis2box/mappings/my_custom_template.json
```

您可以使用`cat`命令检查刚刚创建的映射模板的内容:

```bash
cat /data/wis2box/mappings/my_custom_template.json
```

!!! question "检查映射模板"

    有多少CSV列被映射到BUFR元素?每个被映射的BUFR元素的CSV标题是什么?

??? success "点击查看答案"
    
    您创建的映射模板将**5**个CSV列映射到BUFR元素,即序列301150中的4个BUFR元素加上BUFR元素012101。

    以下CSV列被映射到BUFR元素:

    - **wigosIdentifierSeries**映射到`"eccodes_key": "#1#wigosIdentifierSeries"`(BUFR元素001125)
    - **wigosIssuerOfIdentifier**映射到`"eccodes_key": "#1#wigosIssuerOfIdentifier`(BUFR元素001126)
    - **wigosIssueNumber**映射到`"eccodes_key": "#1#wigosIssueNumber"`(BUFR元素001127)
    - **wigosLocalIdentifierCharacter**映射到`"eccodes_key": "#1#wigosLocalIdentifierCharacter"`(BUFR元素001128)
    - **airTemperature**映射到`"eccodes_key": "#1#airTemperature"`(BUFR元素012101)

您创建的映射模板缺少关于观测的重要元数据、观测的日期和时间以及站点的纬度和经度。

接下来我们将更新映射模板并添加以下序列:
    
- **301011**用于日期(年、月、日)
- **301012**用于时间(小时、分钟)
- **301023**用于位置(纬度/经度(粗略精度))

以及以下元素:

- **010004**用于压力
- **007031**用于气压表高于平均海平面的高度

执行以下命令更新映射模板:

```bash
csv2bufr mappings create 301150 301011 301012 301023 007031 012101 010004  --output /data/wis2box/mappings/my_custom_template.json
```

再次检查映射模板的内容:

```bash
cat /data/wis2box/mappings/my_custom_template.json
```

!!! question "检查更新后的映射模板"

    现在有多少CSV列被映射到BUFR元素?每个被映射的BUFR元素的CSV标题是什么?

??? success "点击查看答案"
    
    您创建的映射模板现在将**18**个CSV列映射到BUFR元素:
    - BUFR序列301150中的4个BUFR元素
    - BUFR序列301011中的3个BUFR元素
    - BUFR序列301012中的2个BUFR元素
    - BUFR序列301023中的2个BUFR元素
    - BUFR元素007031
    - BUFR元素012101

    以下CSV列被映射到BUFR元素:

    - **wigosIdentifierSeries**映射到`"eccodes_key": "#1#wigosIdentifierSeries"`(BUFR元素001125)
    - **wigosIssuerOfIdentifier**映射到`"eccodes_key": "#1#wigosIssuerOfIdentifier`(BUFR元素001126)
    - **wigosIssueNumber**映射到`"eccodes_key": "#1#wigosIssueNumber"`(BUFR元素001127)
    - **wigosLocalIdentifierCharacter**映射到`"eccodes_key": "#1#wigosLocalIdentifierCharacter"`(BUFR元素001128)
    - **year**映射到`"eccodes_key": "#1#year"`(BUFR元素004001)
    - **month**映射到`"eccodes_key": "#1#month"`(BUFR元素004002)
    - **day**映射到`"eccodes_key": "#1#day"`(BUFR元素004003)
    - **hour**映射到`"eccodes_key": "#1#hour"`(BUFR元素004004)
    - **minute**映射到`"eccodes_key": "#1#minute"`(BUFR元素004005)
    - **latitude**映射到`"eccodes_key": "#1#latitude"`(BUFR元素005002)
    - **longitude**映射到`"eccodes_key": "#1#longitude"`(BUFR元素006002)
    - **heightOfBarometerAboveMeanSeaLevel"**映射到`"eccodes_key": "#1#heightOfBarometerAboveMeanSeaLevel"`(BUFR元素007031)
    - **airTemperature**映射到`"eccodes_key": "#1#airTemperature"`(BUFR元素012101)
    - **nonCoordinatePressure**映射到`"eccodes_key": "#1#nonCoordinatePressure"`(BUFR元素010004)

检查`/root/data-conversion-exercises`目录中`custom_template_data.csv`文件的内容:

```bash
cat /root/data-conversion-exercises/custom_template_data.csv
```

注意,此CSV文件的标题与您创建的映射模板中的CSV标题相同。

要测试数据转换,我们可以使用`csv2bufr`命令行工具使用我们创建的映射模板将CSV文件转换为BUFR:

```bash
csv2bufr data transform --bufr-template my_custom_template /root/data-conversion-exercises/custom_template_data.csv
```

您应该看到以下输出:

```bash
CLI:    ... Transforming /root/data-conversion-exercises/custom_template_data.csv to BUFR ...
CLI:    ... Processing subsets:
CLI:    ..... 94 bytes written to ./WIGOS_0-20000-0-15015_20250412T210000.bufr4
CLI:    End of processing, exiting.
```

!!! question "检查BUFR文件的内容"
    
    您如何检查刚刚创建的BUFR文件的内容并验证它是否正确编码了数据?

??? success "点击查看答案"

    您可以使用`bufr_dump -p`命令检查刚刚创建的BUFR文件的内容。
    该命令将以人类可读的格式显示BUFR文件的内容。

    ```bash
    bufr_dump -p ./WIGOS_0-20000-0-15015_20250412T210000.bufr4
    ```

    在输出中,您将看到您在模板中映射的BUFR元素的值,例如"airTemperature"将显示:
    
    ```bash
    airTemperature=298.15
    ```

现在您可以退出容器:

```bash
exit
```

### 在wis2box中使用映射模板

为确保wis2box-api容器识别新的映射模板,您需要重启容器:

```bash
docker restart wis2box-api
```

现在您可以在wis2box-webapp中配置您的数据集,以使用自定义映射模板进行CSV到BUFR的转换插件。

wis2box-webapp将自动检测您创建的映射模板,并在CSV到BUFR转换插件的模板列表中提供它。

点击您在上一个实践课程中创建的数据集,然后点击名为"CSV data converted to BUFR"的插件旁边的"UPDATE":

<img alt="显示wis2box-webapp中数据集编辑器的图片" src="../../assets/img/wis2box-webapp-data-mapping-update-csv2bufr.png"/>

您应该在可用模板列表中看到您创建的新模板:

<img alt="显示wis2box-webapp中csv2bufr模板的图片" src="../../assets/img/wis2box-webapp-csv2bufr-templates.png"/>

!!! hint

    注意,如果您看不到刚刚创建的新模板,请尝试刷新页面或在新的隐私窗口中打开它。

现在保持AWS模板的默认选择(点击右上角关闭插件配置)。

## 使用'AWS'模板

'AWS'模板提供了将CSV数据转换为BUFR序列301150、307096的映射模板,以支持最低GBON要求。

AWS模板的描述可以在这里找到[aws-template](/csv2bufr-templates/aws-template)。

### 查看aws-example输入数据

从以下链接下载此练习的示例:

[aws-example.csv](/sample-data/aws-example.csv)

在编辑器中打开下载的文件并检查内容:

!!! question
    检查日期、时间和标识字段(WIGOS和传统标识符)您注意到什么?今天的日期将如何表示?

??? success "点击查看答案"
    每列包含一条信息。例如,日期被分为年、月和日,反映了数据在BUFR中的存储方式。今天的日期将分布在"year"、"month"和"day"列中。同样,时间需要分为"hour"和"minute",WIGOS站点标识符需要分为其各个组成部分。

!!! question
    查看数据文件,缺失数据是如何编码的?
    
??? success "点击查看答案"
    文件中的缺失数据用空单元格表示。在CSV文件中,这将编码为``,,``。注意,这是一个空单元格,而不是编码为零长度字符串,例如``,"",``。

!!! hint "缺失数据"
    众所周知,由于各种原因可能会缺失数据,无论是由于传感器故障还是未
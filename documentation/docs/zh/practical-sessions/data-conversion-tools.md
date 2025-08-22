---
title: 数据转换工具
---

# 数据转换工具

!!! abstract "学习目标"
    在本次实践课程结束时，您将能够：

    - 在 wis2box-api 容器中访问 ecCodes 命令行工具
    - 使用 synop2bufr 工具从命令行将 FM-12 SYNOP 报告转换为 BUFR
    - 通过 wis2box-webapp 触发 synop2bufr 转换
    - 使用 csv2bufr 工具从命令行将 CSV 数据转换为 BUFR

## 简介

发布在 WIS2 上的数据应符合由各地球系统学科/领域专家社区定义的要求和标准。为了降低发布陆地表面观测数据的门槛，wis2box 提供了将数据转换为 BUFR 格式的工具。这些工具可以通过 wis2box-api 容器使用，并可从命令行测试数据转换过程。

目前 wis2box 主要支持的转换包括 FM-12 SYNOP 报告到 BUFR 和 CSV 数据到 BUFR。支持 FM-12 数据是因为它在 WMO 社区中仍被广泛使用和交换，而支持 CSV 数据是为了允许将自动气象站生成的数据映射到 BUFR 格式。

### 关于 FM-12 SYNOP

陆地表面站的地面气象报告历史上通常按整点或主要（00、06、12 和 18 UTC）和中间（03、09、15、21 UTC）时次进行报告。在迁移到 BUFR 之前，这些报告以纯文本的 FM-12 SYNOP 编码形式进行编码。尽管迁移到 BUFR 的计划应在 2012 年完成，但仍有大量报告以传统的 FM-12 SYNOP 格式交换。有关 FM-12 SYNOP 格式的更多信息，请参阅《WMO 编码手册》，第一卷（WMO-No. 306, Volume I.1）。

### 关于 ecCodes

ecCodes 是一组软件库和工具，旨在对 GRIB 和 BUFR 格式的气象数据进行解码和编码。它由欧洲中期天气预报中心（ECMWF）开发，更多信息请参阅 [ecCodes 文档](https://confluence.ecmwf.int/display/ECC/ecCodes+documentation)。

wis2box 软件在 wis2box-api 容器的基础镜像中包含了 ecCodes 库。这使用户能够从容器中访问命令行工具和库。ecCodes 库在 wis2box-stack 中被用于解码和编码 BUFR 消息。

### 关于 csv2bufr 和 synop2bufr

除了 ecCodes，wis2box 还使用以下与 ecCodes 配合的 Python 模块将数据转换为 BUFR 格式：

- **synop2bufr**：支持传统上由人工观测员使用的 FM-12 SYNOP 格式。synop2bufr 模块依赖额外的站点元数据来在 BUFR 文件中编码额外的参数。请参阅 [GitHub 上的 synop2bufr 仓库](https://github.com/World-Meteorological-Organization/synop2bufr)。
- **csv2bufr**：支持将自动气象站生成的 CSV 数据提取转换为 BUFR 格式。csv2bufr 模块使用映射模板将 CSV 数据映射到 BUFR 格式。请参阅 [GitHub 上的 csv2bufr 仓库](https://github.com/World-Meteorological-Organization/csv2bufr)。

这些模块既可以独立使用，也可以作为 wis2box 堆栈的一部分使用。

## 准备工作

!!! warning "前置条件"

    - 确保您的 wis2box 已配置并启动
    - 确保您已设置数据集并在 wis2box 中配置了至少一个站点
    - 使用 MQTT Explorer 连接到您的 wis2box 实例的 MQTT broker
    - 打开 wis2box Web 应用程序 (`http://YOUR-HOST/wis2box-webapp`)，并确保已登录
    - 通过访问 `http://YOUR-HOST:3000` 打开实例的 Grafana 仪表板

要使用 BUFR 命令行工具，您需要登录到 wis2box-api 容器。除非另有说明，所有命令均应在此容器中运行。您还需要打开 MQTT Explorer 并连接到您的 broker。

首先，通过 SSH 客户端连接到您的学生虚拟机，并将练习材料复制到 wis2box-api 容器中：

```bash
docker cp ~/exercise-materials/data-conversion-exercises wis2box-api:/root
```

然后登录到 wis2box-api 容器并切换到练习材料所在的目录：

```bash
cd ~/wis2box
python3 wis2box-ctl.py login wis2box-api
cd /root/data-conversion-exercises
```

确认工具是否可用，从 ecCodes 开始：

```bash
bufr_dump -V
```

您应该看到以下响应：

```
ecCodes Version 2.36.0
```

接下来，检查 synop2bufr 版本：

```bash
synop2bufr --version
```

您应该看到以下响应：

```
synop2bufr, version 0.7.0
```

然后检查 csv2bufr：

```bash
csv2bufr --version
```

您应该看到以下响应：

```
csv2bufr, version 0.8.6
```

## ecCodes 命令行工具

wis2box-api 容器中包含的 ecCodes 库提供了许多用于处理 BUFR 文件的命令行工具。
接下来的练习将演示如何使用 `bufr_ls` 和 `bufr_dump` 检查 BUFR 文件的内容。

### bufr_ls

在第一个练习中，您将使用 `bufr_ls` 命令检查 BUFR 文件的头部信息，并确定文件内容的类型。

使用以下命令运行 `bufr_ls` 检查文件 `bufr-cli-ex1.bufr4`：

```bash
bufr_ls bufr-cli-ex1.bufr4
```

您应该看到以下输出：

```bash
bufr-cli-ex1.bufr4
centre                     masterTablesVersionNumber  localTablesVersionNumber   typicalDate                typicalTime                numberOfSubsets
cnmc                       29                         0                          20231002                   000000                     1
1 of 1 messages in bufr-cli-ex1.bufr4

1 of 1 total messages in 1 file
```

可以通过向 `bufr_ls` 传递各种选项来更改输出的格式和打印的头部字段。

!!! question
     
    如何以 JSON 格式列出上述输出？

    您可以运行带有 `-h` 标志的 `bufr_ls` 命令来查看可用选项。

??? success "点击查看答案"
    您可以使用 `-j` 标志将输出格式更改为 JSON，例如：
    ```bash
    bufr_ls -j bufr-cli-ex1.bufr4
    ```

    运行后，您应该看到以下输出：
    ```
    { "messages" : [
      {
        "centre": "cnmc",
        "masterTablesVersionNumber": 29,
        "localTablesVersionNumber": 0,
        "typicalDate": 20231002,
        "typicalTime": "000000",
        "numberOfSubsets": 1
      }
    ]}
    ```

打印的输出表示 BUFR 文件中某些头部键的值。

单独来看，这些信息并不十分有用，仅提供了文件内容的有限信息。

在检查 BUFR 文件时，我们通常希望确定文件中包含的数据类型以及数据的典型日期/时间。这些信息可以通过使用 `-p` 标志选择要输出的头部字段来列出。可以使用逗号分隔的列表包含多个头部字段。

您可以使用以下命令列出数据类别、子类别、典型日期和时间：
    
```bash
bufr_ls -p dataCategory,internationalDataSubCategory,typicalDate,typicalTime -j bufr-cli-ex1.bufr4
```

!!! question

    执行上述命令，并使用 [公共代码表 C-13](https://github.com/wmo-im/CCT/blob/master/C13.csv) 解释输出以确定数据类别和子类别。

    文件中包含的数据类型（数据类别和子类别）是什么？数据的典型日期和时间是什么？

??? success "点击查看答案"
    
    ```
    { "messages" : [
      {
        "dataCategory": 2,
        "internationalDataSubCategory": 4,
        "typicalDate": 20231002,
        "typicalTime": "000000"
      }
    ]}
    ```

    从中可以看出：

- 数据类别为2，表示**“垂直探空（非卫星）”**数据。
- 国际子类别为4，表示**“固定陆地站点的高空温度/湿度/风报告（TEMP）”**数据。
- 典型日期和时间分别为2023-10-02和00:00:00z。

### bufr_dump

`bufr_dump`命令可用于列出并检查BUFR文件的内容，包括数据本身。

尝试对第二个示例文件`bufr-cli-ex2.bufr4`运行`bufr_dump`命令：

```{.copy}
bufr_dump bufr-cli-ex2.bufr4
```

这将生成一个JSON文件，可能难以解析。尝试使用`-p`标志以纯文本（key=value格式）输出数据：

```{.copy}
bufr_dump -p bufr-cli-ex2.bufr4
```

您将看到大量键作为输出，其中许多键缺失。这在实际数据中是典型现象，因为并非所有的eccodes键都填充了报告数据。

您可以使用`grep`命令过滤输出，仅显示未缺失的键。例如，要显示所有未缺失的键，可以使用以下命令：

```{.copy}
bufr_dump -p bufr-cli-ex2.bufr4 | grep -v MISSING
```

!!! question

    BUFR文件`bufr-cli-ex2.bufr4`中报告的海平面气压值是多少？

??? success "点击查看答案"

    使用以下命令：

    ```bash
    bufr_dump -p bufr-cli-ex2.bufr4 | grep -i 'pressureReducedToMeanSeaLevel'
    ```

    您应该看到以下输出：

    ```
    pressureReducedToMeanSeaLevel=105590
    ```
    这表明海平面气压值为105590 Pa（1055.90 hPa）。

!!! question

    BUFR文件`bufr-cli-ex2.bufr4`中报告数据的WIGOS站点标识符是什么？

??? success "点击查看答案"

    使用以下命令：

    ```bash
    bufr_dump -p bufr-cli-ex2.bufr4 | grep -i 'wigos'
    ```

    您应该看到以下输出：

    ```
    wigosIdentifierSeries=0
    wigosIssuerOfIdentifier=20000
    wigosIssueNumber=0
    wigosLocalIdentifierCharacter="99100"
    ```

    这表明WIGOS站点标识符为`0-20000-0-99100`。

## synop2bufr 转换

接下来，我们来看如何使用`synop2bufr`模块将FM-12 SYNOP数据转换为BUFR格式。`synop2bufr`模块用于将FM-12 SYNOP数据转换为BUFR格式。该模块安装在wis2box-api容器中，可以通过以下命令行使用：

```{.copy}
synop2bufr data transform \
    --metadata <station-metadata.csv> \
    --output-dir <output-directory-path> \
    --year <year-of-observation> \
    --month <month-of-observation> \
    <input-fm12.txt>
```

`--metadata`参数用于指定站点元数据文件，该文件提供要编码到BUFR文件中的附加信息。
`--output-dir`参数用于指定转换后的BUFR文件的写入目录。`--year`和`--month`参数用于指定观测的年份和月份。

`synop2bufr`模块还可在wis2box-webapp中使用基于Web的输入表单将FM-12 SYNOP数据转换为BUFR格式。

接下来的几个练习将演示`synop2bufr`模块的工作原理以及如何使用它将FM-12 SYNOP数据转换为BUFR格式。

### 检查示例SYNOP消息

检查本练习的示例SYNOP消息文件`synop_message.txt`：

```bash
cd /root/data-conversion-exercises
more synop_message.txt
```

!!! question

    此文件中有多少条SYNOP报告？

??? success "点击查看答案"
    
    输出显示如下：

    ```{.copy}
    AAXX 21121
    15015 02999 02501 10103 21090 39765 42952 57020 60001=
    15020 02997 23104 10130 21075 30177 40377 58020 60001 81041=
    15090 02997 53102 10139 21075 30271 40364 58031 60001 82046=
    ```

    文件中有3条SYNOP报告，分别对应3个不同的站点（由5位传统站点标识符标识：15015、15020和15090）。
    请注意，每条报告的末尾由`=`字符标记。

### 检查站点列表

`--metadata`参数需要一个使用预定义格式的CSV文件，工作示例在文件`station_list.csv`中提供：

使用以下命令检查`station_list.csv`文件的内容：

```bash
more station_list.csv
```

!!! question

    站点列表中列出了多少个站点？这些站点的WIGOS站点标识符是什么？

??? success "点击查看答案"

    输出显示如下：

    ```{.copy}
    station_name,wigos_station_identifier,traditional_station_identifier,facility_type,latitude,longitude,elevation,barometer_height,territory_name,wmo_region
    OCNA SUGATAG,0-20000-0-15015,15015,landFixed,47.7770616258,23.9404602638,503.0,504.0,ROU,europe
    BOTOSANI,0-20000-0-15020,15020,landFixed,47.7356532437,26.6455501701,161.0,162.1,ROU,europe
    ```

    这对应于2个站点的站点元数据：WIGOS站点标识符为`0-20000-0-15015`和`0-20000-0-15020`。

### 将SYNOP转换为BUFR

接下来，使用以下命令将FM-12 SYNOP消息转换为BUFR格式：

```bash
synop2bufr data transform --metadata station_list.csv --output-dir ./ --year 2024 --month 09 synop_message.txt
```

!!! question
    创建了多少个BUFR文件？输出中的WARNING消息是什么意思？

??? success "点击查看答案"
    输出显示如下：

    ```{.copy}
    [WARNING] Station 15090 not found in station file
    ```

    如果您使用`ls -lh`检查目录内容，您应该看到创建了2个新的BUFR文件：`WIGOS_0-20000-0-15015_20240921T120000.bufr4`和`WIGOS_0-20000-0-15020_20240921T120000.bufr4`。

    警告消息表明，传统站点标识符为`15090`的站点未在站点列表文件`station_list.csv`中找到。这意味着该站点的SYNOP报告未转换为BUFR格式。

!!! question
    使用`bufr_dump`命令检查BUFR文件`WIGOS_0-20000-0-15015_20240921T120000.bufr4`的内容。

    您能否验证`station_list.csv`文件中提供的信息是否存在于BUFR文件中？

??? success "点击查看答案"
    您可以使用以下命令检查BUFR文件的内容：

    ```bash
    bufr_dump -p WIGOS_0-20000-0-15015_20240921T120000.bufr4 | grep -v MISSING
    ```

    您将注意到以下输出：

    ```{.copy}
    wigosIdentifierSeries=0
    wigosIssuerOfIdentifier=20000
    wigosIssueNumber=0
    wigosLocalIdentifierCharacter="15015"
    blockNumber=15
    stationNumber=15
    stationOrSiteName="OCNA SUGATAG"
    stationType=1
    year=2024
    month=9
    day=21
    hour=12
    minute=0
    latitude=47.7771
    longitude=23.9405
    heightOfStationGroundAboveMeanSeaLevel=503
    heightOfBarometerAboveMeanSeaLevel=504
    ```

    请注意，这包括`station_list.csv`文件中提供的数据。

### wis2box-webapp中的SYNOP表单

`synop2bufr` 模块也被用于 `wis2box-webapp`，通过基于网页的输入表单将 FM-12 SYNOP 数据转换为 BUFR 格式。  
要测试此功能，请访问 `http://YOUR-HOST/wis2box-webapp` 并登录。

从左侧菜单中选择 `SYNOP Form`，然后将 `synop_message.txt` 文件的内容复制粘贴到表单中：

```{.copy}
AAXX 21121
15015 02999 02501 10103 21090 39765 42952 57020 60001=
15020 02997 23104 10130 21075 30177 40377 58020 60001 81041=
15090 02997 53102 10139 21075 30271 40364 58031 60001 82046=
```

粘贴到 `SYNOP message` 文本区域中：

<img alt="synop-form" src="/../assets/img/wis2box-webapp-synop-form.png" width="800">

!!! question
    您是否能够提交表单？结果是什么？

??? success "点击查看答案"

    您需要选择一个数据集，并提供在前一个练习中创建的 "processes/wis2box" 的令牌才能提交表单。

    如果您提供了无效的令牌，您将看到以下结果：
    
    - 结果：未授权，请提供有效的 'processes/wis2box' 令牌

    如果您提供了有效的令牌，您将看到 "WARNINGS: 3"。点击 "WARNINGS" 打开下拉菜单，显示以下内容：

    - Station 15015 not found in station file
    - Station 15020 not found in station file
    - Station 15090 not found in station file

    要将这些数据转换为 BUFR 格式，您需要在您的 wis2box 中配置相应的站点，并确保这些站点与您的数据集主题相关联。

!!! note

    在 [ingesting-data-for-publication](./ingesting-data-for-publication.md) 练习中，您导入了文件 "synop_202412030900.txt"，并通过 `synop2bufr` 模块将其转换为 BUFR 格式。

    在 wis2box 的自动化工作流中，年份和月份会从文件名中自动提取，并用于填充 `--year` 和 `--month` 参数，而站点元数据会从 wis2box 的站点配置中自动提取。

## csv2bufr 转换

!!! note
    确保您仍然登录到 `wis2box-api` 容器，并位于目录 `/root/data-conversion-exercises` 中。如果您在前一个练习中退出了容器，可以通过以下方式重新登录：

    ```bash
    cd ~/wis2box
    python3 wis2box-ctl.py login wis2box-api
    cd /root/data-conversion-exercises
    ```

现在我们来看如何使用 `csv2bufr` 模块将 CSV 数据转换为 BUFR 格式。该模块已安装在 `wis2box-api` 容器中，可以通过以下命令行使用：

```{.copy}
csv2bufr data transform \
    --bufr-template <bufr-mapping-template> \
    <input-csv-file>
```

`--bufr-template` 参数用于指定 BUFR 映射模板文件，该文件以 JSON 格式提供输入 CSV 数据与输出 BUFR 数据之间的映射关系。默认的映射模板安装在 `wis2box-api` 容器的目录 `/opt/csv2bufr/templates` 中。

### 查看示例 CSV 文件

查看示例 CSV 文件 `aws-example.csv` 的内容：

```bash
more aws-example.csv
```

!!! question
    CSV 文件中有多少行数据？CSV 文件中报告的站点的 WIGOS 站点标识符是什么？

??? question "点击查看答案"

    输出显示如下内容：

    ```{.copy}
    wsi_series,wsi_issuer,wsi_issue_number,wsi_local,wmo_block_number,wmo_station_number,station_type,year,month,day,hour,minute,latitude,longitude,station_height_above_msl,barometer_height_above_msl,station_pressure,msl_pressure,geopotential_height,thermometer_height,air_temperature,dewpoint_temperature,relative_humidity,method_of_ground_state_measurement,ground_state,method_of_snow_depth_measurement,snow_depth,precipitation_intensity,anemometer_height,time_period_of_wind,wind_direction,wind_speed,maximum_wind_gust_direction_10_minutes,maximum_wind_gust_speed_10_minutes,maximum_wind_gust_direction_1_hour,maximum_wind_gust_speed_1_hour,maximum_wind_gust_direction_3_hours,maximum_wind_gust_speed_3_hours,rain_sensor_height,total_precipitation_1_hour,total_precipitation_3_hours,total_precipitation_6_hours,total_precipitation_12_hours,total_precipitation_24_hours
    0,20000,0,60355,60,355,1,2024,3,31,1,0,47.77706163,23.94046026,503,504.43,100940,101040,1448,5,298.15,294.55,80,3,1,1,0,0.004,10,-10,30,3,30,5,40,9,20,11,2,4.7,5.3,7.9,9.5,11.4
    0,20000,0,60355,60,355,1,2024,3,31,2,0,47.77706163,23.94046026,503,504.43,100940,101040,1448,5,25.,294.55,80,3,1,1,0,0.004,10,-10,30,3,30,5,40,9,20,11,2,4.7,5.3,7.9,9.5,11.4
    0,20000,0,60355,60,355,1,2024,3,31,3,0,47.77706163,23.94046026,503,504.43,100940,101040,1448,5,298.15,294.55,80,3,1,1,0,0.004,10,-10,30,3,30,5,40,9,20,11,2,4.7,5.3,7.9,9.5,11.4
    ```

    CSV 文件的第一行是列标题，用于标识每列中的数据。

    标题行之后有 3 行数据，表示同一站点在三个不同时间点的 3 次气象观测，WIGOS 站点标识符为 `0-20000-0-60355`，时间戳分别为 `2024-03-31 01:00:00`、`2024-03-31 02:00:00` 和 `2024-03-31 03:00:00`。

### 查看 aws-template

`wis2box-api` 包含一组预定义的 BUFR 映射模板，这些模板安装在目录 `/opt/csv2bufr/templates` 中。

检查目录 `/opt/csv2bufr/templates` 的内容：

```bash
ls /opt/csv2bufr/templates
```

您应该看到以下输出：

```{.copy}
CampbellAfrica-v1-template.json  aws-template.json  daycli-template.json
```

查看 `aws-template.json` 文件的内容：

```bash
cat /opt/csv2bufr/templates/aws-template.json
```

这将返回一个较大的 JSON 文件，提供了 43 个 CSV 列的映射关系。

!!! question
    哪个 CSV 列映射到 eccodes 键 `airTemperature`？此键的有效最小值和最大值是多少？

??? success "点击查看答案"

    使用以下命令过滤输出：

    ```bash
    cat /opt/csv2bufr/templates/aws-template.json | grep -i airTemperature
    ```
    您应该看到以下输出：

    ```{.copy}
    {"eccodes_key": "#1#airTemperature", "value": "data:air_temperature", "valid_min": "const:193.15", "valid_max": "const:333.15"},
    ```

    对于 eccodes 键 `airTemperature`，其值将从 CSV 列 **air_temperature** 中提取。

    此键的最小值和最大值分别为 `193.15` 和 `333.15`。

!!! question

    哪个 CSV 列映射到 eccodes 键 `internationalDataSubCategory`？此键的值是多少？

??? success "点击查看答案"
    使用以下命令过滤输出：

    ```bash
    cat /opt/csv2bufr/templates/aws-template.json | grep -i internationalDataSubCategory
    ```
    您应该看到以下输出：

    ```{.copy}
    {"eccodes_key": "internationalDataSubCategory", "value": "const:2"},
    ```

**没有任何 CSV 列映射到 eccodes 键 `internationalDataSubCategory`**，而是使用了常量值 2，并将在使用此映射模板生成的所有 BUFR 文件中进行编码。

### 将 CSV 转换为 BUFR

让我们尝试使用 `csv2bufr` 命令将文件转换为 BUFR 格式：

```{.copy}
csv2bufr data transform --bufr-template aws-template ./aws-example.csv
```

!!! question
    创建了多少个 BUFR 文件？

??? success "点击查看答案"

    输出显示如下内容：

    ```{.copy}
    CLI:    ... Transforming ./aws-example.csv to BUFR ...
    CLI:    ... Processing subsets:
    CLI:    ..... 384 bytes written to ./WIGOS_0-20000-0-60355_20240331T010000.bufr4
    #1#airTemperature: Value (25.0) out of valid range (193.15 - 333.15).; Element set to missing
    CLI:    ..... 384 bytes written to ./WIGOS_0-20000-0-60355_20240331T020000.bufr4
    CLI:    ..... 384 bytes written to ./WIGOS_0-20000-0-60355_20240331T030000.bufr4
    CLI:    End of processing, exiting.
    ```

    输出表明创建了 3 个 BUFR 文件：`WIGOS_0-20000-0-60355_20240331T010000.bufr4`、`WIGOS_0-20000-0-60355_20240331T020000.bufr4` 和 `WIGOS_0-20000-0-60355_20240331T030000.bufr4`。

要检查 BUFR 文件的内容并忽略缺失值，可以使用以下命令：

```bash
bufr_dump -p WIGOS_0-20000-0-60355_20240331T010000.bufr4 | grep -v MISSING
```

!!! question
    在 BUFR 文件 `WIGOS_0-20000-0-60355_20240331T010000.bufr4` 中，eccodes 键 `airTemperature` 的值是多少？在 BUFR 文件 `WIGOS_0-20000-0-60355_20240331T020000.bufr4` 中呢？

??? success "点击查看答案"
    要过滤输出，可以使用以下命令：

    ```bash
    bufr_dump -p WIGOS_0-20000-0-60355_20240331T010000.bufr4 | grep -v MISSING | grep airTemperature
    ```
    你应该会看到以下输出：

    ```{.copy}
    #1#airTemperature=298.15
    ```

    而对于第二个文件：

    ```bash
    bufr_dump -p WIGOS_0-20000-0-60355_20240331T020000.bufr4 | grep -v MISSING | grep airTemperature
    ```

    你不会得到任何结果，这表明在 BUFR 文件 `WIGOS_0-20000-0-60355_20240331T020000.bufr4` 中，键 `airTemperature` 的值缺失。`csv2bufr` 拒绝对 CSV 数据中的值 `25.0` 进行编码，因为它超出了映射模板中定义的有效范围 `193.15` 和 `333.15`。

请注意，使用预定义的 BUFR 映射模板将 CSV 转换为 BUFR 存在以下限制：

- CSV 文件必须符合映射模板中定义的格式，即 CSV 列名必须与映射模板中定义的名称匹配
- 只能编码映射模板中定义的键
- 质量控制检查仅限于映射模板中定义的检查

有关如何创建和使用自定义 BUFR 映射模板的信息，请参阅下一个实践练习 [csv2bufr-templates](./csv2bufr-templates.md)。

## 结论

!!! success "恭喜！"
    在本次实践课程中，你学会了：

    - 如何在 wis2box-api 容器中访问 ecCodes 命令行工具
    - 如何使用 `synop2bufr` 从命令行将 FM-12 SYNOP 报告转换为 BUFR
    - 如何在 wis2box-webapp 的 SYNOP 表单中将 FM-12 SYNOP 报告转换为 BUFR
    - 如何使用 `csv2bufr` 从命令行将 CSV 数据转换为 BUFR
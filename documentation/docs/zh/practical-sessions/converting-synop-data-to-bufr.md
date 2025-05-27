---
title: 将SYNOP数据转换为BUFR
---

# 从命令行将SYNOP数据转换为BUFR

!!! abstract "学习成果"
    在本实践课程结束时，您将能够：

    - 使用synop2bufr工具将FM-12 SYNOP报告转换为BUFR；
    - 在格式转换之前诊断并修复FM-12 SYNOP报告中的简单编码错误；

## 引言

陆地表面站的地面天气报告历来每小时或在主要（00、06、12和18 UTC）和中间（03、09、15、21 UTC）天气时报告。在迁移到BUFR之前，这些报告是以纯文本FM-12 SYNOP代码形式编码的。尽管计划在2012年之前完成迁移到BUFR，但仍有大量报告以遗留的FM-12 SYNOP格式交换。有关FM-12 SYNOP格式的更多信息，请参阅WMO代码手册，第I.1卷（WMO-No. 306，第I.1卷）。

[WMO代码手册，第I.1卷](https://library.wmo.int/records/item/35713-manual-on-codes-international-codes-volume-i-1)

为了帮助完成迁移到BUFR，已经开发了一些工具用于将FM-12 SYNOP报告编码为BUFR，在本课程中您将学习如何使用这些工具以及FM-12 SYNOP报告中包含的信息与BUFR消息之间的关系。

## 准备工作

!!! warning "先决条件"

    - 确保您的wis2box已配置并启动。
    - 通过访问wis2box API（``http://<your-host-name>/oapi``）并验证API正在运行来确认状态。
    - 在开始练习之前，请确保阅读**synop2bufr入门**和**ecCodes入门**部分。

## synop2bufr入门

以下是基本的`synop2bufr`命令和配置：

### 转换
`transform`功能将SYNOP消息转换为BUFR：

```bash
synop2bufr data transform --metadata my_file.csv --output-dir ./my_directory --year message_year --month message_month my_SYNOP.txt
```

请注意，如果未指定元数据、输出目录、年份和月份选项，它们将采用其默认值：

| 选项        | 默认值 |
| ----------- | ----------- |
| --metadata | station_list.csv |
| --output-dir | 当前工作目录。 |
| --year | 当前年份。 |
| --month | 当前月份。 |

!!! note
    使用默认的年份和月份时必须小心，因为报告中指定的日期可能不对应（例如，六月没有31天）。

在示例中，没有给出年份和月份，所以可以自行指定日期或使用默认值。

## ecCodes入门

ecCodes提供了命令行工具，也可以嵌入到您自己的应用程序中。以下是一些与BUFR数据一起使用的有用命令行工具。

### bufr_dump

`bufr_dump`命令是一个通用的BUFR信息工具。它有许多选项，但以下将是最适用于练习的：

```bash
bufr_dump -p my_bufr.bufr4
```

这将显示BUFR内容到您的屏幕上。如果您对特定变量的值感兴趣，请使用`egrep`命令：

```bash
bufr_dump -p my_bufr.bufr4 | egrep -i temperature
```

这将显示您BUFR数据中与温度相关的变量。如果您想对多种类型的变量进行此操作，请使用管道(`|`)过滤输出：

```bash
bufr_dump -p my_bufr.bufr4 | egrep -i 'temperature|wind'
```

## 从命令行使用synop2bufr将FM-12 SYNOP转换为BUFR

eccodes库和synop2bufr模块已安装在wis2box-api容器中。为了进行接下来的几个练习，我们将synop2bufr-exercises目录复制到wis2box-api容器中并从那里运行练习：

```bash
docker cp ~/exercise-materials/synop2bufr-exercises wis2box-api:/root
```

现在我们可以进入容器并运行练习：

```bash
docker exec -it wis2box-api /bin/bash
```

### 练习1
导航到`/root/synop2bufr-exercises/ex_1`目录并检查SYNOP消息文件message.txt：

```bash
cd /root/synop2bufr-exercises/ex_1
more message.txt
```

!!! question

    这个文件中有多少个SYNOP报告？

??? success "点击查看答案"
    
    有1个SYNOP报告，因为在消息的结尾只有1个分隔符(=)。

检查站点列表：

```bash
more station_list.csv
```

!!! question

    站点列表中列出了多少个站点？

??? success "点击查看答案"

    有1个站点，station_list.csv包含一行站点元数据。

!!! question
    尝试将`message.txt`转换为BUFR格式。

??? success "点击查看答案"

    要将SYNOP消息转换为BUFR格式，请使用以下命令：

    ```bash
    synop2bufr data transform --metadata station_list.csv --output-dir ./ --year 2024 --month 09 message.txt
    ```

!!! tip

    请参阅[synop2bufr入门](#synop2bufr入门)部分。

使用`bufr_dump`检查生成的BUFR数据。

!!! question
     如何比较纬度和经度值与站点列表中的值？

??? success "点击查看答案"

    要比较BUFR数据中的纬度和经度值与站点列表中的值，请使用以下命令：

    ```bash
    bufr_dump -p WIGOS_0-20000-0-15015_20240921T120000.bufr4 | egrep -i 'latitude|longitude'
    ```

    这将显示BUFR数据中的纬度和经度值。

!!! tip

    请参阅[ecCodes入门](#eccodes入门)部分。

### 练习2
导航到`exercise-materials/synop2bufr-exercises/ex_2`目录并检查SYNOP消息文件message.txt：

```bash
cd /root/synop2bufr-exercises/ex_2
more message.txt
```

!!! question

    这个文件中有多少个SYNOP报告？

??? success "点击查看答案"

    有3个SYNOP报告，因为在消息的结尾有3个分隔符(=)。

检查站点列表：

```bash
more station_list.csv
```

!!! question

    站点列表中列出了多少个站点？

??? success "点击查看答案"

    有3个站点，station_list.csv包含三行站点元数据。

!!! question
    将`message.txt`转换为BUFR格式。

??? success "点击查看答案"

    要将SYNOP消息转换为BUFR格式，请使用以下命令：

    ```bash
    synop2bufr data transform --metadata station_list.csv --output-dir ./ --year 2024 --month 09 message.txt
    ```

!!! question

    根据这个和上一个练习的结果，您如何预测基于SYNOP报告数量和站点元数据文件中列出的站点数量的结果BUFR文件数量？

??? success "点击查看答案"

    要查看生成的BUFR文件，请运行以下命令：

    ```bash
    ls -l *.bufr4
    ```

    生成的BUFR文件数量将等于消息文件中的SYNOP报告数量。

使用`bufr_dump`检查生成的BUFR数据。

!!! question
    如何检查每个生成的文件中编码的WIGOS站点ID？

??? success "点击查看答案"

    这可以通过以下命令完成：

    ```bash
    bufr_dump -p WIGOS_0-20000-0-15015_20240921T120000.bufr4 | egrep -i 'wigos'
    ```

    ```bash
    bufr_dump -p WIGOS_0-20000-0-15020_20240921T120000.bufr4 | egrep -i 'wigos'
    ```

    ```bash
    bufr_dump -p WIGOS_0-20000-0-15090_20240921T120000.bufr4 | egrep -i 'wigos'
    ```

    注意，如果您的目录中只有这3个BUFR文件，您可以使用Linux通配符如下：

    ```bash
    bufr_dump -p *.bufr4 | egrep -i 'wigos'
    ```

### 练习3
导航到`exercise-materials/synop2bufr-exercises/ex_3`目录并检查SYNOP消息文件message.txt：

```bash
cd /root/synop2bufr-exercises/ex_3
more message.txt
```

这个SYNOP消息只包含一个更长的报告，有更多的部分。

检查站点列表：

```bash
more station_list.csv
```

!!! question

    这个文件包含的站点比SYNOP消息中的报告多，这有问题吗？

??? success "点击查看答案"

    没有问题，只要站点列表文件中存在与我们试图转换的SYNOP报告匹配的站点TSI的行。

!!! note

    站点列表文件是`synop2bufr`的元数据来源，为在BUFR SYNOP中提供字母数字SYNOP报告中缺失的信息。

!!! question
    将`message.txt`转换为BUFR格式。

??? success "点击查看答案"

    这是使用`transform`命令完成的，例如：

    ```bash
    synop2bufr data transform --metadata station_list.csv --output-dir ./ --year 2024 --month 09 message.txt
    ```

使用`bufr_dump`检查生成的BUFR数据。

!!! question

    查找以下变量：

    - 报告的空气温度（K）
    - 报告的总云量（%）
    - 报告的总日照时长（分钟）
    - 报告的风速（m/s）

??? success "点击查看答案"

    要通过关键字在BUFR数据中查找变量，您可以使用以下命令：

    ```bash
    bufr_dump -p WIGOS_0-20000-0-15260_20240921T115500.bufr4 | egrep -i 'temperature'
    ```

    您可以使用以下命令搜索多个关键字：

    ```bash
    bufr_dump -p WIGOS_0-20000-0-15260_20240921T115500.bufr4 | egrep -i 'temperature|cover|sunshine|wind'
    ```

!!! tip

    您可能会发现[ecCodes入门](#eccodes入门)部分的最后一个命令很有用。


### 练习4
导航到`exercise-materials/synop2bufr-exercises/ex_4`目录并检查SYNOP消息文件message.txt：

```bash
cd /root/synop2bufr-exercises/ex_4
more message_incorrect.txt
```

!!! question

    这个SYNOP文件有什么不正确的地方？

??? success "点击查看答案"

    15015的SYNOP报告缺少允许`synop2bufr`区分此报告与下一个报告的分隔符(`=`)。

尝试使用`station_list.csv`转换`message_incorrect.txt`

!!! question

    您在这次转换中遇到了什么问题？

??? success "点击查看答案"

    要将SYNOP消息转换为BUFR格式，请使用以下命令：

    ```bash
    synop2bufr data transform --metadata station_list.csv --output-dir ./ --year 2024 --month 09 message_incorrect.txt
    ```

    尝试转换应该会引发以下错误：
    
    - `[ERROR] 无法解码SYNOP消息`
    - `[ERROR] 解析SYNOP报告时出错：AAXX 21121 15015 02999 02501 10103 21090 39765 42952 57020 60001 15020 02997 23104 10130 21075 30177 40377 58020 60001 81041. 10130不是有效的组！`

### 练习5
导航到`exercise-materials/synop2bufr-exercises/ex_5`目录并检查SYNOP消息文件message.txt：

```bash
cd /root/synop2bufr-exercises/ex_5
more message.txt
```

尝试使用`station_list_incorrect.csv`将`message.txt`转换为BUFR格式

!!! question

    您在这次转换中遇到了什么问题？  
    考虑到呈现的错误，证明生成的BUFR文件数量。

??? success "点击查看答案"

    要将SYNOP消息转换为BUFR格式，请使用以下命令：

    ```bash
    synop2bufr data transform --metadata station_list_incorrect.csv --output-dir ./ --year 2024 --month 09 message.txt
    ```

    一个站点TSI（`15015`）在站点列表中没有相应的元数据，这将阻止synop2bufr访问将第一个SYNOP报告转换为BUFR所需的额外必要元数据。

    您将看到以下警告：

    - `[WARNING] 站点15015在站点文件中未找到`

    您可以通过运行以下命令查看生成的BUFR文件数量：

    ```bash
    ls -l *.bufr4
    ```

    message.txt中有3个SYNOP报告，但只生成了2个BUFR文件。这是因为上面提到的一个SYNOP报告缺乏必要的元数据。

## 结论

!!! success "恭喜！"

    在这个实践课程中，您学习了：

    - 如何使用synop2bufr工具将FM-12 SYNOP报告转换为BUFR；
    - 如何在格式转换之前诊断并修复FM-12 SYNOP报告中的简单编码错误；

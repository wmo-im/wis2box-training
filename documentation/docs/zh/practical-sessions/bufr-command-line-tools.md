---
title: 使用 BUFR 数据
---

# 使用 BUFR 数据

!!! abstract "学习成果"
    在这个实践课程中，您将了解 **wis2box-api** 容器中包含的一些 BUFR 工具，这些工具用于将数据转换为 BUFR 格式以及读取 BUFR 中编码的内容。
    
    您将学习：

    - 如何使用 `bufr_ls` 命令检查 BUFR 文件中的头部
    - 如何使用 `bufr_dump` 提取并检查 bufr 文件中的数据
    - csv2bufr 中使用的 bufr 模板的基本结构以及如何使用命令行工具
    - 如何对 bufr 模板进行基本更改以及如何更新 wis2box 以使用修订版

## 介绍

生成 BUFR 数据通知的插件使用 wis2box-api 中的过程来处理 BUFR 数据，例如将数据从 CSV 转换为 BUFR 或从 BUFR 转换为 geojson。

wis2box-api 容器包括许多处理 BUFR 数据的工具。

这些工具包括 ECMWF 开发并包含在 ecCodes 软件中的工具，更多信息可以在 [ecCodes 网站](https://confluence.ecmwf.int/display/ECC/BUFR+tools) 上找到。

在本课程中，您将被介绍到 ecCodes 软件包中的 `bufr_ls` 和 `bufr_dump`，以及 csv2bufr 工具的高级配置。

## 准备

为了使用 BUFR 命令行工具，您需要登录到 wis2box-api 容器
除非另有说明，否则所有命令都应在此容器上运行。您还需要打开 MQTT Explorer 并连接到您的代理。

首先通过您的 ssh 客户端连接到您的学生 VM，然后登录到 wis2box-api 容器：

```{.copy}
cd ~/wis2box-1.0.0rc1
python3 wis2box-ctl.py login wis2box-api
```

确认工具可用，从 ecCodes 开始：

``` {.copy}
bufr_dump -V
```
您应该得到以下响应：

```
ecCodes Version 2.28.0
```

接下来检查 csv2bufr：

```{.copy}
csv2bufr --version
```

您应该得到以下响应：

```
csv2bufr, version 0.7.4
```

最后，创建一个工作目录：

```{.copy}
cd /data/wis2box
mkdir -p working/bufr-cli
cd working/bufr-cli
```

您现在已经准备好开始使用 BUFR 工具了。


## 使用 BUFR 命令行工具

### 练习 1 - bufr_ls
在这个第一个练习中，您将使用 `bufr_ls` 命令检查 BUFR 文件的头部并确定文件的内容。BUFR 文件中包含以下头部：

| 头部                              | ecCodes 键                    | 描述                                                                                                                                           |
|-----------------------------------|------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------|
| 发起/生成中心                     | centre                       | 数据的发起/生成中心                                                                                                      |
| 发起/生成子中心                   | bufrHeaderSubCentre          | 数据的发起/生成子中心                                                                                                  | 
| 更新序列号                        | updateSequenceNumber         | 这是数据的第一个版本 (0) 还是更新 (>0)                                                                                   |               
| 数据类别                         | dataCategory                 | BUFR 消息中包含的数据类型，例如 suface 数据。参见 [BUFR 表 A](https://github.com/wmo-im/BUFR4/blob/master/BUFR_TableA_en.csv)  |
| 国际数据子类别                   | internationalDataSubCategory | BUFR 消息中包含的数据子类型，例如 suface 数据。参见 [公共代码表 C-13](https://github.com/wmo-im/CCT/blob/master/C13.csv) |
| 年                                | typicalYear (typicalDate)    | BUFR 消息内容的最典型时间                                                                                                       |
| 月                                | typicalMonth (typicalDate)   | BUFR 消息内容的最典型时间                                                                                                       |
| 日                                | typicalDay (typicalDate)     | BUFR 消息内容的最典型时间                                                                                                       |
| 小时                              | typicalHour (typicalTime)    | BUFR 消息内容的最典型时间                                                                                                       |
| 分钟                              | typicalMinute (typicalTime)  | BUFR 消息内容的最典型时间                                                                                                       |
| BUFR 描述符                      | unexpandedDescriptors        | 定义文件中包含的数据的一个或多个 BUFR 描述符的列表                                                                        |

使用以下命令直接下载示例文件到 wis2box-management 容器：

``` {.copy}
curl https://training.wis2box.wis.wmo.int/sample-data/bufr-cli-ex1.bufr4 --output bufr-cli-ex1.bufr4
```

现在使用以下命令在此文件上运行 `bufr_ls`：

```bash
bufr_ls bufr-cli-ex1.bufr4
```

您应该看到以下输出：

```bash
bufr-cli-ex1.bufr4
centre                     masterTablesVersionNumber  localTablesVersionNumber   typicalDate                typicalTime                numberOfSubsets
cnmc                       29                         0                          20231002                   000000                     1
1 of 1 messages in bufr-cli-ex1.bufr4

1 of 1 total messages in 1 files
```

单独这些信息并不是很有信息量，只提供了有限的文件内容信息。

默认输出没有提供观察或数据类型的信息，格式也不容易阅读。然而，可以传递各种选项给 `bufr_ls` 来更改格式和打印的头部字段。

使用 `bufr_ls` 不带任何参数来查看选项：

```{.copy}
bufr_ls
```

您应该看到以下输出：

```
NAME    bufr_ls

DESCRIPTION
        List content of BUFR files printing values of some header keys.
        Only scalar keys can be printed.
        It does not fail when a key is not found.

USAGE
        bufr_ls [options] bufr_file bufr_file ...

OPTIONS
        -p key[:{s|d|i}],key[:{s|d|i}],...
                Declaration of keys to print.
                For each key a string (key:s), a double (key:d) or an integer (key:i)
                type can be requested. Default type is string.
        -F format
                C style format for floating-point values.
        -P key[:{s|d|i}],key[:{s|d|i}],...
                As -p adding the declared keys to the default list.
        -w key[:{s|d|i}]{=|!=}value,key[:{s|d|i}]{=|!=}value,...
                Where clause.
                Messages are processed only if they match all the key/value constraints.
                A valid constraint is of type key=value or key!=value.
                For each key a string (key:s), a double (key:d) or an integer (key:i)
                type can be specified. Default type is string.
                In the value you can also use the forward-slash character '/' to specify an OR condition (i.e. a logical disjunction)
                Note: only one -w clause is allowed.
        -j      JSON output
        -s key[:{s|d|i}]=value,key[:{s|d|i}]=value,...
                Key/values to set.
                For each key a string (key:s), a double (key:d) or an integer (key:i)
                type can be defined. By default the native type is set.
        -n namespace
                All the keys belonging to the given namespace are printed.
        -m      Mars keys are printed.
        -V      Version.
        -W width
                Minimum width of each column in output. Default is 10.
        -g      Copy GTS header.
        -7      Does not fail when the message has wrong length

SEE ALSO
        Full documentation and examples at:
        <https://confluence.ecmwf.int/display/ECC/bufr_ls>
```

现在在示例文件上运行相同的命令，但以 JSON 格式输出信息。

!!! question
    您需要传递哪个标志给 `bufr_ls` 命令以查看 JSON 格式的输出？

??? success "点击以显示答案"
    您可以使用 `-j` 标志将输出格式更改为 json，例如
    `bufr_ls -j <input-file>`。这可能比默认输出格式更易读。请参见下面的示例输出：

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

当检查 BUFR 文件时，我们通常希望确定文件中包含的数据类型以及数据的典型日期/时间。可以使用 `-p` 标志选择要输出的头部。可以使用逗号分隔列表包括多个头部。

使用 `bufr_ls` 命令检查测试文件并确定文件中包含的数据类型以及该数据的典型日期和时间。

??? hint
    ecCodes 键在上表中给出。我们可以使用以下命令列出 BUFR 数据的 dataCategory 和 internationalDataSubCategory：

    ```
    bufr_ls -p dataCategory,internationalDataSubCategory bufr-cli-ex1.bufr4
    ```

    可以根据需要添加其他键。

!!! question
    文件中包含哪种类型的数据（日期类别和子类别）？数据的典型日期和时间是什么？

??? success "点击以显示答案"
    您需要运行的命令应类似于：
    
    ```
    bufr_ls -p dataCategory,internationalDataSubCategory,typicalDate,typicalTime -j bufr-cli-ex1.bufr4
    ```

    您可能有额外的键，或者单独列出了年、月、日等。输出应该类似于下面，具体取决于您是否选择了 JSON 或默认输出。

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

    从这里我们可以看到：

    - 数据类别是 2，从 [BUFR 表 A](https://github.com/wmo-im/BUFR4/blob/master/BUFR_TableA_en.csv)
      我们可以看到这个文件包含 "垂直探测（非卫星）" 数据。
    - 国际子类别是 4，表示
      "固定陆地站的高层温度/湿度/风报告（TEMP）" 数据。这些信息可以在 [公共代码表 C-13](https://github.com/wmo-im/CCT/blob/master/C13.csv)（第 33 行）中查找。注意类别和子类别的组合。
    - 典型日期和时间分别是 2023/10/02 和 00:00:00z。

### 练习 2 - bufr_dump

`bufr_dump` 命令可用于列出和检查 BUFR 文件的内容，包括数据本身。

在这个练习中，我们将使用一个与您在初始 csv2bufr 实践课程中创建的 BUFR 文件相同的文件。

使用以下命令直接下载示例文件到 wis2box 管理容器：

``` {.copy}
curl https://training.wis2box.wis.wmo.int/sample-data/bufr-cli-ex2.bufr4 --output bufr-cli-ex2.bufr4
```

现在在文件上运行 `bufr_dump` 命令，使用 `-p` 标志以纯文本输出数据（key=value 格式）：

```{.copy}
bufr_dump -p bufr-cli-ex2.bufr4
```

您应该看到大约 240 个键输出，其中许多是缺失的。这在实际数据中是典型的，因为并非所有的 eccodes 键都填充了报告数据。

!!! hint
    可以使用诸如 `grep` 之类的工具过滤缺失值：
    ```{.copy}
    bufr_dump -p bufr-cli-ex2.bufr4 | grep -v MISSING
    ```

这个示例 BUFR 文件来自 csv2bufr 实践课程。请按照以下方式下载原始 CSV 文件到您当前的位置：

```{.copy}
curl https://training.wis2box.wis.wmo.int/sample-data/csv2bufr-ex1.csv --output csv2bufr-ex1.csv
```

并使用以下命令显示文件内容：

```{.copy}
more csv2bufr-ex1.csv
```

!!! question
    使用以下命令显示 CSV 文件中的第 18 列，您将找到报告的平均海平面气压 (msl_pressure)：

    ```{.copy}
    more csv2bufr-ex1.csv | cut -d ',' -f 18
    ```
    
    BUFR 输出中哪个键对应于平均海平面气压？

??? hint
    可以将 `grep` 等工具与 `bufr_dump` 结合使用。例如：
    
    ```{.copy}
    bufr_dump -p bufr-cli-ex2.bufr4 | grep -i "pressure"
    ```
    
    将过滤 `bufr_dump` 的内容，只显示包含单词 pressure 的行。或者，输出可以根据值进行过滤。

??? success "点击以显示答案"
    键 "pressureReducedToMeanSeaLevel" 对应于输入 CSV 文件中的 msl_pressure 列。

花几分钟时间检查其余的输出，与输入 CSV 文件进行比较，然后继续下一个练习。例如，您可以尝试在 BUFR 输出中找到与相对湿度（CSV 文件中的第 23 列）和空气温度（CSV 文件中的第 21 列）对应的键。

### 练习 3 - csv2bufr 映射文件

csv2bufr 工具可以配置为处理具有不同列和 BUFR 序列的表格数据。

这是通过使用 JSON 格式编写的配置文件完成的。

与 BUFR 数据本身一样，JSON 文件包含一个头部部分和一个数据部分，这些大致对应于 BUFR 中的相同部分。

此外，JSON 文件中还指定了一些格式选项。

可以通过下面的链接查看默认映射的 JSON 文件（右键单击并在新标签页中打开）：

[aws-template.json](https://raw.githubusercontent.com/wmo-im/csv2bufr/main/csv2bufr/templates/resources/aws-template.json)

检查映射文件的 `header` 部分（如下所示）并与练习 1 中的表格（ecCodes 键列）进行比较：

```
"header":[
    {"eccodes_key": "edition", "value": "const:4"},
    {"eccodes_key": "masterTableNumber", "value": "const:0"},
    {"eccodes_key": "bufrHeaderCentre", "value": "const:0"},
    {"eccodes_key": "bufrHeaderSubCentre", "value": "const:0"},
    {"eccodes_key": "updateSequenceNumber", "value": "const:0"},
    {"eccodes_key": "dataCategory", "value": "const:0"},
    {"eccodes_key": "internationalDataSubCategory", "value": "const:2"},
    {"eccodes_key": "masterTablesVersionNumber", "value": "const:30"},
    {"eccodes_key": "numberOfSubsets", "value": "const:1"},
    {"eccodes_key": "observedData", "value": "const:1"},
    {"eccodes_key": "compressedData", "value": "const:0"},
    {"eccodes_key": "typicalYear", "value": "data:year"},
    {"eccodes_key": "typicalMonth", "value": "data:month"},
    {"eccodes_key": "typicalDay", "value": "data:day"},
    {"eccodes_key": "typicalHour", "value": "data:hour"},
    {"eccodes_key": "typicalMinute", "value": "data:minute"},
    {"eccodes_key": "unexpandedDescriptors", "value":"array:301150, 307096"}
],
```

在这里，您可以看到与 `bufr_ls` 命令输出中可用的相同头部。在
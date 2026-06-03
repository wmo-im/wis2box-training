---
title: 将 GTS 标头添加到 WIS2 通知
---

# 将 GTS 标头添加到 WIS2 通知

!!! abstract "学习目标"

    在本次实践课程结束时，您将能够：
    
    - 配置文件名与 GTS 标头之间的映射
    - 通过匹配 GTS 标头的文件名来摄取数据
    - 在 WIS2 通知中查看 GTS 标头
    - 使用 FM-12 SYNOP 表单手动将 GTS 标头添加到 WIS2 通知中

## 介绍

在向 WIS2 过渡阶段，计划停止通过 GTS 传输数据的 WMO 成员需要将 GTS 标头添加到其 WIS2 通知中。这些标头使 WIS2 到 GTS 网关能够将数据转发到 GTS 网络。

这使得已经迁移到使用 WIS2 节点发布数据的成员能够停用其 MSS 系统，同时确保其数据仍可供尚未迁移到 WIS2 的成员使用。

需要将 GTS 属性作为附加属性添加到 WIS2 通知消息中。GTS 属性是一个 JSON 对象，其中包含将数据转发到 GTS 网络所需的 GTS 标头。

```json
{
  "gts": {
    "ttaaii": "FTAE31",
    "cccc": "VTBB"
  }
}
```

在 wis2box 中，您可以通过提供一个名为 `gts_headers_mapping.csv` 的附加文件来自动将此内容添加到 WIS2 通知中，该文件包含将 GTS 标头映射到传入文件名所需的信息。

此文件应放置在您的 `wis2box.env` 中由 `WIS2BOX_HOST_DATADIR` 定义的目录中，并应包含以下列：

- `string_in_filepath`：文件名中的字符串，用于匹配 GTS 标头
- `TTAAii`：要添加到 WIS2 通知中的 TTAAii 标头
- `CCCC`：要添加到 WIS2 通知中的 CCCC 标头

从 wis2box-1.3.0 开始，数据发布者有两种选择（可选）将 GTS 属性添加到其通知中：

1. 对于上传到 MinIO 的文件，准备映射文件 `gts_headers_mappings.csv` 并包含所需属性。

2. 对于在 wis2box-webapp 中使用 FM-12 SYNOP 表单输入的数据，选择 `Add GTS headers` 并手动输入所需信息。

## 准备工作

确保您可以通过 SSH 访问您的学生虚拟机，并且您的 wis2box 实例已启动并运行。

确保您已使用 MQTT Explorer 连接到您的 wis2box 实例的 MQTT broker。您可以使用公共凭证 `everyone/everyone` 连接到 broker。

确保您已打开一个网页浏览器，并通过访问 `http://YOUR-HOST:3000` 查看您的实例的 Grafana 仪表板。

## 练习 1：为上传到 MinIO 的数据使用映射文件

第一个练习将演示如何使用名为 `gts_headers_mapping.csv` 的映射文件为上传到 MinIO 的数据添加 GTS 标头。

### 创建 `gts_headers_mapping.csv`

要将 GTS 标头添加到您的 WIS2 通知中，需要一个 CSV 文件将 GTS 标头映射到传入文件名。

CSV 文件的名称必须为（完全一致）`gts_headers_mapping.csv`，并且应放置在您的 `wis2box.env` 中由 `WIS2BOX_HOST_DATADIR` 定义的目录中。

将文件 `exercise-materials/gts-headers-exercises/gts_headers_mapping.csv` 复制到您的 wis2box 实例，并放置在您的 `wis2box.env` 中由 `WIS2BOX_HOST_DATADIR` 定义的目录中。

```bash
cp ~/exercise-materials/gts-headers-exercises/gts_headers_mapping.csv ~/wis2box-data
```

### 应用映射

创建 `gts_headers_mapping.csv` 文件后，您需要重新启动 wis2box-management 容器以应用更改。您可以通过在学生虚拟机中运行以下命令来完成此操作：

```bash
docker restart wis2box-management
```

### 使用 GTS 标头摄取数据

将文件 `exercise-materials/gts-headers-exercises/A_SMRO01YRBK171200_C_EDZW_20240717120502.txt` 复制到您的 `wis2box.env` 中由 `WIS2BOX_HOST_DATADIR` 定义的目录中：

```bash
cp ~/exercise-materials/gts-headers-exercises/A_SMRO01YRBK171200_C_EDZW_20240717120502.txt ~/wis2box-data
```

然后登录到 **wis2box-management** 容器：

```bash
cd ~/wis2box
python3 wis2box-ctl.py login
```

在 wis2box 命令行中，我们可以将示例数据文件 `A_SMRO01YRBK171200_C_EDZW_20240717120502.txt` 摄取到特定数据集，如下所示：

```bash
wis2box data ingest -p /data/wis2box/A_SMRO01YRBK171200_C_EDZW_20240717120502.txt --metadata-id urn:wmo:md:not-my-centre:core.surface-based-observations.synop
```

确保将 `metadata-id` 选项替换为您的数据集的正确标识符。

检查 Grafana 仪表板以查看数据是否正确摄取。如果看到任何警告或错误，请尝试修复并重复执行 `wis2box data ingest` 命令。

### 在 WIS2 通知中查看 GTS 标头

打开 MQTT Explorer，检查您刚刚摄取的数据的 WIS2 通知消息。

WIS2 通知消息应包含您在 `gts_headers_mapping.csv` 文件中提供的 GTS 标头。

## 练习 2：使用 FM-12 SYNOP 表单

在 wis2box-webapp 中使用 FM-12 SYNOP 表单时，您可以通过选择 "Add GTS headers" 选项并提供所需信息，手动将 GTS 标头添加到您的 WIS2 通知中。

对于此练习，您可以使用以下示例数据或提供您自己的数据：

FM-12 SYNOP 消息：

```{copy}
AAXX 03094
64400 42460 71004 10285 20245 30113 40133 8493/
    333 59005 83813 81930 87363 94966 95836=
```

GTS 标头：TTAAii=`ISIH01` 和 CCCC=`FCBB`

!!! note
    wis2box 中的 synop2bufr-plugin 会将 FM-12 SYNOP 消息转换为 BUFR，因此 TTAAii 应以 `IS` 开头：

    - I = 观测数据（以二进制编码）– BUFR
    - S = 地面/海平面

### 手动提交带有 GTS 标头的 FM-12 SYNOP 表单

进入 wis2box-webapp 中的 FM-12 SYNOP 表单，并使用上述示例数据或您自己的数据填写表单。

确保选择 "Add GTS headers" 选项并提供所需的 GTS 标头信息：

<img alt="fm-12-synop-form-gts-headers.png" src="/../assets/img/fm-12-synop-form-gts-headers.png" width="800">

提供所需的身份验证令牌并提交表单。

您可能会看到一条错误消息，因为该站点未在您的站点列表中。您需要将站点 "0-20000-0-64400" 添加到您的站点列表中，以便数据能够成功转换并发布。

### 在 WIS2 通知中查看 GTS 标头

打开 MQTT Explorer，检查您刚刚摄取的数据的 WIS2 通知消息，以查看通知中是否包含 GTS 标头。

## 结论

!!! success "恭喜！"
    在本次实践课程中，您学习了：
      - 如何将 GTS 标头添加到您的 WIS2 通知中
      - 验证 GTS 标头是否通过您的 wis2box 安装成功提供
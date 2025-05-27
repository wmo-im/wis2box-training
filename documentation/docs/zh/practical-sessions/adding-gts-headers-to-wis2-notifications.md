---
title: 为 WIS2 通知添加 GTS 头信息
---

# 为 WIS2 通知添加 GTS 头信息

!!! abstract "学习目标"

    完成本实践课程后，您将能够：
    
    - 配置文件名和 GTS 头信息之间的映射
    - 使用与 GTS 头信息匹配的文件名摄入数据
    - 在 WIS2 通知中查看 GTS 头信息

## 简介

在向 WIS2 过渡阶段，希望停止 GTS 数据传输的 WMO 成员需要在其 WIS2 通知中添加 GTS 头信息。这些头信息使 WIS2 到 GTS 网关能够将数据转发到 GTS 网络。

这使得已迁移到使用 WIS2 节点进行数据发布的成员可以禁用其 MSS 系统，同时确保其数据仍然可供尚未迁移到 WIS2 的成员使用。

GTS 属性需要作为附加属性添加到 WIS2 通知消息中。GTS 属性是一个 JSON 对象，其中包含将数据转发到 GTS 网络所需的 GTS 头信息。

```json
{
  "gts": {
    "ttaaii": "FTAE31",
    "cccc": "VTBB"
  }
}
```

在 wis2box 中，您可以通过提供一个名为 `gts_headers_mapping.csv` 的附加文件来自动将其添加到 WIS2 通知中，该文件包含将 GTS 头信息映射到传入文件名所需的信息。

该文件应放置在 `wis2box.env` 中由 `WIS2BOX_HOST_DATADIR` 定义的目录中，并应包含以下列：

- `string_in_filepath`：文件名中用于匹配 GTS 头信息的字符串部分
- `TTAAii`：要添加到 WIS2 通知的 TTAAii 头信息
- `CCCC`：要添加到 WIS2 通知的 CCCC 头信息

## 准备工作

确保您可以通过 SSH 访问您的学员虚拟机，并且您的 wis2box 实例正在运行。

确保您使用 MQTT Explorer 连接到 wis2box 实例的 MQTT 代理。您可以使用公共凭据 `everyone/everyone` 连接到代理。

确保您已打开网络浏览器，通过访问 `http://YOUR-HOST:3000` 查看实例的 Grafana 仪表板。

## 创建 `gts_headers_mapping.csv`

要向 WIS2 通知添加 GTS 头信息，需要一个将 GTS 头信息映射到传入文件名的 CSV 文件。

该 CSV 文件应准确命名为 `gts_headers_mapping.csv`，并应放置在 `wis2box.env` 中由 `WIS2BOX_HOST_DATADIR` 定义的目录中。

## 提供 `gts_headers_mapping.csv` 文件
    
将文件 `exercise-materials/gts-headers-exercises/gts_headers_mapping.csv` 复制到您的 wis2box 实例，并将其放置在 `wis2box.env` 中由 `WIS2BOX_HOST_DATADIR` 定义的目录中。

```bash
cp ~/exercise-materials/gts-headers-exercises/gts_headers_mapping.csv ~/wis2box-data
```

然后重启 wis2box-management 容器以应用更改：

```bash
docker restart wis2box-management
```

## 摄入带有 GTS 头信息的数据

将文件 `exercise-materials/gts-headers-exercises/A_SMRO01YRBK171200_C_EDZW_20240717120502.txt` 复制到 `wis2box.env` 中由 `WIS2BOX_HOST_DATADIR` 定义的目录：

```bash
cp ~/exercise-materials/gts-headers-exercises/A_SMRO01YRBK171200_C_EDZW_20240717120502.txt ~/wis2box-data
```

然后登录到 **wis2box-management** 容器：

```bash
cd ~/wis2box
python3 wis2box-ctl.py login
```

从 wis2box 命令行，我们可以按如下方式将示例数据文件 `A_SMRO01YRBK171200_C_EDZW_20240717120502.txt` 摄入到特定数据集：

```bash
wis2box data ingest -p /data/wis2box/A_SMRO01YRBK171200_C_EDZW_20240717120502.txt --metadata-id urn:wmo:md:not-my-centre:core.surface-based-observations.synop
```

确保使用正确的数据集标识符替换 `metadata-id` 选项。

检查 Grafana 仪表板，查看数据是否正确摄入。如果看到任何警告或错误，请尝试修复它们并重复执行 `wis2box data ingest` 命令。

## 在 WIS2 通知中查看 GTS 头信息

转到 MQTT Explorer 并检查您刚刚摄入的数据的 WIS2 通知消息。

WIS2 通知消息应包含您在 `gts_headers_mapping.csv` 文件中提供的 GTS 头信息。

## 结论

!!! success "恭喜！"
    在本实践课程中，您学会了如何：
      - 向 WIS2 通知添加 GTS 头信息
      - 验证 GTS 头信息是否通过您的 wis2box 安装可用
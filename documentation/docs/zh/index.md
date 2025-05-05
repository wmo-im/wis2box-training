---
title: 首页
---

<img alt="WMO logo" src="../assets/img/wmo-logo.png" width="200">
# WIS2 in a box 培训

WIS2 in a box ([wis2box](https://docs.wis2box.wis.wmo.int)) 是一个免费开源的 WMO WIS2 Node 参考实现。该项目提供了一套即插即用的工具集，用于按照 WIS2 原则，采用基于标准的方法来摄取、处理和发布天气/气候/水文数据。wis2box 还提供对 WIS2 网络中所有数据的访问。wis2box 的设计目标是降低数据提供者的使用门槛，为数据发现、访问和可视化提供基础设施和服务。

本培训通过一系列演示和实践练习，提供了有关 wis2box 项目各个方面的逐步说明，帮助您发布和下载 WIS2 中的数据。

参与者可以使用样本测试数据和元数据进行操作，也可以集成自己的数据和元数据。

本培训涵盖广泛的主题（安装/设置/配置、发布/下载数据等）。

## 目标和学习成果

本培训的目标是熟悉以下内容：

- WIS2 架构核心概念和组件
- WIS2 中用于发现和访问的数据和元数据格式
- wis2box 架构和环境
- wis2box 核心功能：
    - 元数据管理
    - 数据摄取和转换为 BUFR 格式
    - 用于 WIS2 消息发布的 MQTT 代理
    - 用于数据下载的 HTTP 端点
    - 用于程序化访问数据的 API 端点

## 导航

左侧导航提供整个培训的目录。

右侧导航提供特定页面的目录。

## 先决条件

### 知识要求

- 基本的 Linux 命令（参见[速查表](cheatsheets/linux.md)）
- 网络和互联网协议的基础知识

### 软件要求

本培训需要以下工具：

- 运行 Ubuntu 操作系统的实例（在本地培训课程中由 WMO 培训师提供）参见[访问您的学员虚拟机](practical-sessions/accessing-your-student-vm.md#introduction)
- SSH 客户端以访问您的实例
- 本地机器上的 MQTT Explorer
- SCP 和 SFTP 客户端用于从本地机器复制文件

## 约定

!!! question

    这样标记的部分邀请您回答问题。

您还会在文本中注意到提示和注释部分：

!!! tip

    提示分享如何最好地完成任务。

!!! note

    注释提供有关实践课程所涵盖主题的附加信息，以及如何最好地完成任务。

示例如下所示：

配置
``` {.yaml linenums="1"}
my-collection-defined-in-yaml:
    type: collection
    title: my title defined as a yaml attribute named title
    description: my description as a yaml attribute named description
```

需要在终端/控制台中输入的代码片段表示为：

```bash
echo 'Hello world'
```

容器名称（运行镜像）用**粗体**表示。

## 培训位置和材料

培训内容、维基和问题跟踪器在 GitHub 上管理，地址为 [https://github.com/World-Meteorological-Organization/wis2box-training](https://github.com/World-Meteorological-Organization/wis2box-training)。

## 打印材料

本培训可以导出为 PDF。要保存或打印本培训材料，请转到[打印页面](print_page)，然后选择文件 > 打印 > 保存为 PDF。

## 练习材料

练习材料可以从 [exercise-materials.zip](/exercise-materials.zip) 压缩文件下载。

## 支持

对于本培训的问题/错误/建议或改进/贡献，请使用 [GitHub 问题跟踪器](https://github.com/World-Meteorological-Organization/wis2box-training/issues)。

所有 wis2box 错误、增强和问题都可以在 [GitHub](https://github.com/World-Meteorological-Organization/wis2box/issues) 上报告。

如需额外支持或咨询，请联系 wis2-support@wmo.int。

wis2box 核心文档始终可以在 [https://docs.wis2box.wis.wmo.int](https://docs.wis2box.wis.wmo.int) 找到。

我们始终鼓励并欢迎贡献！
---
title: 首页
---

<img alt="WMO logo" src="/assets/img/wmo-logo.png" width="200">

# WIS2 in a box 培训

WIS2 in a box ([wis2box](https://docs.wis2box.wis.wmo.int)) 是一个免费的开源（FOSS）WMO WIS2 Node 参考实现。该项目提供了一套即插即用的工具集，用于通过基于标准的方法来摄取、处理和发布天气/气候/水文数据，符合 WIS2 原则。wis2box 还提供对 WIS2 网络中所有数据的访问。wis2box 的设计旨在降低数据提供者的使用门槛，提供支持数据发现、访问和可视化的基础设施和服务。

本次培训通过逐步讲解 wis2box 项目的各个方面，并提供一系列练习，帮助您从 WIS2 发布和下载数据。培训内容包括概述性演示以及动手实践练习。

参与者将能够使用示例测试数据和元数据，并可集成自己的数据和元数据。

本次培训涵盖广泛的主题（安装/设置/配置、数据发布/下载等）。

## 目标和学习成果

本次培训的目标是熟悉以下内容：

- WIS2 架构的核心概念和组件
- WIS2 中用于数据发现和访问的数据和元数据格式
- wis2box 的架构和环境
- wis2box 的核心功能：
    - 元数据管理
    - 数据摄取和转换为 BUFR 格式
    - 用于 WIS2 消息发布的 MQTT broker
    - 用于数据下载的 HTTP 端点
    - 用于程序化访问数据的 API 端点

## 导航

左侧导航提供了整个培训的目录。

右侧导航提供了特定页面的目录。

## 前提条件

### 知识

- 基本的 Linux 命令（参见 [cheatsheet](./cheatsheets/linux.md)）
- 基本的网络和互联网协议知识。

### 软件

本次培训需要以下工具：

- 一台运行 Ubuntu 操作系统的实例（由 WMO 培训师在本地培训期间提供），参见 [访问您的学生虚拟机](./practical-sessions/accessing-your-student-vm.md#introduction)
- 用于访问实例的 SSH 客户端
- 本地计算机上的 MQTT Explorer
- 用于从本地计算机复制文件的 SCP 和 SFTP 客户端

## 约定

!!! question

    标记为这样的问题部分邀请您回答问题。

此外，您会在文本中看到提示和注释部分：

!!! tip

    提示分享了如何最好地完成任务的帮助信息。

!!! note

    注释提供了关于实践课程所涵盖主题的附加信息，以及如何最好地完成任务。

示例如下所示：

配置
``` {.yaml linenums="1"}
my-collection-defined-in-yaml:
    type: collection
    title: my title defined as a yaml attribute named title
    description: my description as a yaml attribute named description
```

需要在终端/控制台中输入的代码片段如下表示：

```bash
echo 'Hello world'
```

容器名称（运行中的镜像）用 **加粗** 表示。

## 培训地点和材料

培训内容、wiki 和问题跟踪器托管在 GitHub 上：[https://github.com/wmo-im/wis2box-training](https://github.com/wmo-im/wis2box-training)。

## 练习材料

练习材料可以从 [exercise-materials.zip](/exercise-materials.zip) 压缩文件中下载。

## 支持

对于本次培训的任何问题/错误/建议或改进/贡献，请使用 [GitHub 问题跟踪器](https://github.com/World-Meteorological-Organization/wis2box-training/issues)。

所有 wis2box 的错误、增强和问题可以在 [GitHub](https://github.com/World-Meteorological-Organization/wis2box/issues) 上报告。

如需额外支持或有任何问题，请联系 wis2-support@wmo.int。

如往常一样，wis2box 的核心文档始终可在 [https://docs.wis2box.wis.wmo.int](https://docs.wis2box.wis.wmo.int) 找到。

我们始终鼓励并欢迎贡献！
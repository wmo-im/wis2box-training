---
title: 从 WIS2 全球发现目录中发现数据集
---

# 从 WIS2 全球发现目录中发现数据集

!!! abstract "学习目标！"

    在本次实践课程结束时，您将能够：

    - 使用 pywiscat 从全球发现目录 (GDC) 中发现数据集

## 介绍

在本课程中，您将学习如何使用 [pywiscat](https://github.com/wmo-im/pywiscat) 从 WIS2 全球发现目录 (GDC) 中发现数据。pywiscat 是一个命令行工具，用于从 WIS2 GDC 中搜索和检索元数据。

目前，可用的 GDC 包括：

- 加拿大环境与气候变化部，加拿大气象局：<https://wis2-gdc.weather.gc.ca>
- 中国气象局：<https://gdc.wis.cma.cn>
- 德国气象局：<https://wis2.dwd.de/gdc>

在本地培训课程中，会设置一个本地 GDC，允许参与者查询他们从各自的 wis2box 实例发布的元数据。在这种情况下，培训师会提供本地 GDC 的 URL。

## 准备工作

!!! note
    在开始之前，请登录到您的学生虚拟机 (VM)。

## 安装 pywiscat

使用 `pip3` Python 包管理工具在您的虚拟机上安装 pywiscat：

```bash
pip3 install pywiscat
```

!!! note

    如果您遇到以下错误：

    ```
    WARNING: The script pywiscat is installed in '/home/username/.local/bin' which is not on PATH.
    Consider adding this directory to PATH or, if you prefer to suppress this warning, use --no-warn-script-location.
    ```

    请运行以下命令：

    ```bash
    export PATH=$PATH:/home/$USER/.local/bin
    ```

    ...其中 `$USER` 是您在虚拟机上的用户名。

验证安装是否成功：

```bash
pywiscat --version
```

## 使用 pywiscat 查找数据

默认情况下，pywiscat 会连接到由加拿大环境与气候变化部 (ECCC) 托管的全球发现目录 (GDC)。

!!! note "更改 GDC URL"
    如果您在本地培训课程中进行此练习，可以通过设置 `PYWISCAT_GDC_URL` 环境变量来配置 pywiscat 查询本地 GDC：

    ```bash
    export PYWISCAT_GDC_URL=http://gdc.wis2.training:5002
    ```

查看可用选项，请运行：

```bash
pywiscat search --help
```

您可以搜索 GDC 中的所有记录：

```bash
pywiscat search
```

!!! question

    搜索返回了多少条记录？

??? success "点击查看答案"
    返回的记录数量取决于您查询的 GDC。当使用本地培训 GDC 时，您应该会看到记录数量等于其他实践课程中已导入 GDC 的数据集数量。

让我们尝试使用关键字查询 GDC：

```bash
pywiscat search -q observations
```

!!! question

    查询结果的数据政策是什么？

??? success "点击查看答案"
    所有返回的数据都应指定为“核心”数据。

尝试使用 `-q` 进行其他查询。

!!! tip

    `-q` 标志支持以下语法：

    - `-q synop`：查找包含“synop”一词的所有记录
    - `-q temp`：查找包含“temp”一词的所有记录
    - `-q "observations AND oman"`：查找包含“observations”和“oman”两个词的所有记录
    - `-q "observations NOT oman"`：查找包含“observations”但不包含“oman”的所有记录
    - `-q "synop OR temp"`：查找包含“synop”或“temp”的所有记录
    - `-q "obs*"`：模糊搜索

    当搜索包含空格的术语时，请使用双引号括起来。

让我们获取一个感兴趣的特定搜索结果的更多详细信息：

```bash
pywiscat get <id>
```

!!! tip

    使用上一条搜索结果中的 `id` 值。

## 总结

!!! success "恭喜！"

    在本次实践课程中，您学习了如何：

    - 使用 pywiscat 从 WIS2 全球发现目录中发现数据集
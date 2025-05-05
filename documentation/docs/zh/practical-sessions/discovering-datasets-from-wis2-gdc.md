---
title: 从WIS2全球发现目录中发现数据集
---

# 从WIS2全球发现目录中发现数据集

!!! abstract "学习目标!"

    完成本实践课程后，您将能够：

    - 使用pywiscat从Global Discovery Catalogue (GDC)中发现数据集

## 介绍

在本课程中，您将学习如何从WIS2 Global Discovery Catalogue (GDC)中发现数据。

目前，以下GDC可用：

- Environment and Climate Change Canada, Meteorological Service of Canada: <https://wis2-gdc.weather.gc.ca>
- China Meteorological Administration: <https://gdc.wis.cma.cn>
- Deutscher Wetterdienst: <https://wis2.dwd.de/gdc>

在本地培训课程中，会设置一个本地GDC，让参与者可以查询他们从wis2box实例发布的元数据。在这种情况下，培训师将提供本地GDC的URL。

## 准备工作

!!! note
    开始之前请登录您的学员虚拟机。

## 安装pywiscat

使用`pip3` Python包安装器在您的虚拟机上安装pywiscat：
```bash
pip3 install pywiscat
```

!!! note

    如果您遇到以下错误：

    ```
    WARNING: The script pywiscat is installed in '/home/username/.local/bin' which is not on PATH.
    Consider adding this directory to PATH or, if you prefer to suppress this warning, use --no-warn-script-location.
    ```

    那么运行以下命令：

    ```bash
    export PATH=$PATH:/home/$USER/.local/bin
    ```

    其中`$USER`是您在虚拟机上的用户名。

验证安装是否成功：

```bash
pywiscat --version
```

## 使用pywiscat查找数据

默认情况下，pywiscat连接到加拿大的Global Discovery Catalogue。让我们通过设置`PYWISCAT_GDC_URL`环境变量来配置pywiscat以查询培训GDC：

```bash
export PYWISCAT_GDC_URL=http://gdc.wis2.training:5002
```

让我们使用[pywiscat](https://github.com/wmo-im/pywiscat)来查询作为培训一部分设置的GDC。

```bash
pywiscat search --help
```

现在搜索GDC中的所有记录：

```bash
pywiscat search
```

!!! question

    搜索返回了多少条记录？

??? success "点击查看答案"
    记录数量取决于您查询的GDC。当使用本地培训GDC时，您应该看到记录数量等于在其他实践课程中已导入GDC的数据集数量。

让我们尝试使用关键词查询GDC：

```bash
pywiscat search -q observations
```

!!! question

    结果的数据政策是什么？

??? success "点击查看答案"
    所有返回的数据都应指定为"core"数据

尝试使用`-q`进行其他查询

!!! tip

    `-q`标志允许以下语法：

    - `-q synop`：查找所有包含"synop"这个词的记录
    - `-q temp`：查找所有包含"temp"这个词的记录
    - `-q "observations AND oman"`：查找所有包含"observations"和"oman"这两个词的记录
    - `-q "observations NOT oman"`：查找所有包含"observations"但不包含"oman"这个词的记录
    - `-q "synop OR temp"`：查找所有包含"synop"或"temp"的记录
    - `-q "obs*"`：模糊搜索

    当搜索包含空格的术语时，请用双引号括起来。

让我们获取我们感兴趣的特定搜索结果的更多详细信息：

```bash
pywiscat get <id>
```

!!! tip

    使用之前搜索中的`id`值。

## 结论

!!! success "恭喜！"

    在本实践课程中，您学会了如何：

    - 使用pywiscat从WIS2 Global Discovery Catalogue中发现数据集
---
title: 设置带访问控制的推荐数据集
---

# 设置带访问控制的推荐数据集

!!! abstract "学习目标"
    完成本实践课程后，您将能够：

    - 创建一个具有"推荐"数据策略的新数据集
    - 为数据集添加访问令牌
    - 验证没有访问令牌时无法访问数据集
    - 在 HTTP 头部添加访问令牌以访问数据集

## 简介

在 WMO 中不被视为"核心"数据集的数据集可以选择配置访问控制策略。wis2box 提供了一种机制，可以为数据集添加访问令牌，除非用户在 HTTP 头部提供访问令牌，否则将无法下载数据。

## 准备工作

确保您可以通过 SSH 访问您的学生虚拟机，并且您的 wis2box 实例正在运行。

确保使用 MQTT Explorer 连接到您的 wis2box 实例的 MQTT 代理。您可以使用公共凭据 `everyone/everyone` 连接到代理。

通过访问 `http://YOUR-HOST/wis2box-webapp` 确保您已在网络浏览器中打开了实例的 wis2box-webapp。

## 创建具有"推荐"数据策略的新数据集

转到 wis2box-webapp 中的"数据集编辑器"页面并创建新数据集。选择 Data Type = 'weather/surface-weather-observations/synop'。

<img alt="create-dataset-recommended" src="/../assets/img/create-dataset-template.png" width="800">

对于"Centre ID"，使用与之前实践课程中相同的 ID。

点击"CONTINUE To FORM"继续。

在数据集编辑器中，将数据策略设置为"recommended"（注意更改数据策略将更新"主题层次结构"）。
用描述性名称替换自动生成的"Local ID"，例如"recommended-data-with-access-control"：

<img alt="create-dataset-recommended" src="/../assets/img/create-dataset-recommended.png" width="800">

继续填写空间属性和联系信息的必填字段，并"验证表单"以检查是否有错误。

最后使用先前创建的身份验证令牌提交数据集，并检查新数据集是否在 wis2box-webapp 中创建。

检查 MQTT-explorer 以查看您是否在主题 `origin/a/wis2/<your-centre-id>/metadata` 上收到宣布新发现元数据记录的 WIS2 通知消息。

## 为数据集添加访问令牌

登录到 wis2box-management 容器，

```bash
cd ~/wis2box
python3 wis2box-ctl.py login
```

在容器内的命令行中，您可以使用 `wis2box auth add-token` 命令保护数据集，使用 `--metadata-id` 标志指定数据集的元数据标识符，并将访问令牌作为参数。

例如，要将访问令牌 `S3cr3tT0k3n` 添加到元数据标识符为 `urn:wmo:md:not-my-centre:core.surface-based-observations.synop` 的数据集：

```bash
wis2box auth add-token --metadata-id urn:wmo:md:not-my-centre:reco.surface-based-observations.synop S3cr3tT0k3n
```

退出 wis2box-management 容器：

```bash
exit
```

## 向数据集发布数据

将文件 `exercise-materials/access-control-exercises/aws-example.csv` 复制到您的 `wis2box.env` 中 `WIS2BOX_HOST_DATADIR` 定义的目录：

```bash
cp ~/exercise-materials/access-control-exercises/aws-example.csv ~/wis2box-data
```

然后使用 WinSCP 或命令行编辑器编辑文件 `aws-example.csv`，将输入数据中的 WIGOS-station-identifiers 更新为与您的 wis2box 实例中的站点相匹配。

接下来，转到 wis2box-webapp 中的站点编辑器。对于 `aws-example.csv` 中使用的每个站点，更新"主题"字段以匹配您在上一个练习中创建的数据集的"主题"。

此站点现在将关联到 2 个主题，一个用于"核心"数据集，另一个用于"推荐"数据集：

<img alt="edit-stations-add-topics" src="/../assets/img/edit-stations-add-topics.png" width="600">

您需要使用 `collections/stations` 的令牌来保存更新的站点数据。

接下来，登录到 wis2box-management 容器：

```bash
cd ~/wis2box
python3 wis2box-ctl.py login
```

从 wis2box 命令行，我们可以按如下方式将示例数据文件 `aws-example.csv` 导入特定数据集：

```bash
wis2box data ingest -p /data/wis2box/aws-example.csv --metadata-id urn:wmo:md:not-my-centre:reco.surface-based-observations.synop
```

确保提供正确的数据集元数据标识符，并**检查您是否在 MQTT Explorer 中收到 WIS2 数据通知**，主题为 `origin/a/wis2/<your-centre-id>/data/recommended/surface-based-observations/synop`。

检查 WIS2 通知消息中的规范链接，并将链接复制/粘贴到浏览器中尝试下载数据。

您应该看到 403 Forbidden 错误。

## 在 HTTP 头部添加访问令牌以访问数据集

为了演示访问数据集需要访问令牌，我们将使用命令行函数 `wget` 重现您在浏览器中看到的错误。

在您的学生虚拟机的命令行中，使用 `wget` 命令和您从 WIS2 通知消息中复制的规范链接。

```bash
wget <canonical-link>
```

您应该看到 HTTP 请求返回 *401 Unauthorized*，并且数据未被下载。

现在在 HTTP 头部添加访问令牌以访问数据集。

```bash
wget --header="Authorization: Bearer S3cr3tT0k3n" <canonical-link>
```

现在数据应该可以成功下载。

## 结论

!!! success "恭喜！"
    在本实践课程中，您学会了如何：

    - 创建一个具有"推荐"数据策略的新数据集
    - 为数据集添加访问令牌
    - 验证没有访问令牌时无法访问数据集
    - 在 HTTP 头部添加访问令牌以访问数据集
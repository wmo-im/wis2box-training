---
title: 设置推荐数据集
---

# 设置推荐数据集

!!! abstract "学习目标"
    在本次实践课程结束时，您将能够：

    - 创建一个数据策略为“推荐”的新数据集
    - 为数据集添加访问令牌
    - 验证在没有访问令牌的情况下无法访问数据集
    - 将访问令牌添加到 HTTP 头以访问数据集
    - 添加一个托管在您 wis2box 实例上的自定义许可证文件

## 介绍

根据 WMO 统一数据政策，数据在 WIS2 上共享，并定义了两类数据。

**核心**：免费且无条件使用的数据，无需付费且无使用限制。

**推荐**：可能附带使用条件和/或需要许可证的数据。

共享为推荐的数据：

- 可能附带使用和再使用的条件
- 可能对数据应用访问控制
- 不会被 WIS2 全局缓存缓存
- 必须包含一个包含许可证 URL 的元数据记录

!!! note "下载推荐数据"
    
    由于 WIS2 全局缓存不会缓存推荐数据，您将**不会**在主题 `cache/a/wis2/<centre-id>/data/recommended/..` 上看到通知。

    数据消费者必须使用主题 `origin/a/wis2/<centre-id>/data/recommended/...` 通知中提供的规范 URL，从数据提供者托管的数据服务器下载数据。

在本次实践课程中，您将使用 wis2box-webapp 中的数据集编辑器创建一个数据策略为“推荐”的新数据集。您还将学习如何提供一个自托管许可证以及如何选择性地添加访问控制。

!!! note "WIS2 中的航空数据"
    
    在本次练习中，您需要创建一个数据集以共享 METAR 数据，这是一种用于报告航空天气观测的标准格式。
    
    WIS2 中的航空数据应始终以“推荐”的形式共享，以符合国际民航组织 (ICAO) 规定的航空数据共享规则。

## 准备工作

确保您可以通过 SSH 访问您的学生虚拟机，并且您的 wis2box 实例已启动并运行。

确保您已使用 MQTT Explorer 连接到您的 wis2box 实例的 MQTT broker。您可以使用公共凭据 `everyone/everyone` 连接到 broker。

确保您已打开一个 Web 浏览器，并通过访问 `http://YOUR-HOST/wis2box-webapp` 打开您的 wis2box-webapp 实例。

## 创建一个数据策略为“推荐”的新数据集

进入 wis2box-webapp 的“数据集编辑器”页面并创建一个新数据集。

对于“Centre ID”，使用您在之前实践课程中使用的相同 ID。

选择 Template = 'other'，以表明您不会为数据集使用预定义模板：

<img alt="create-dataset-recommended" src="/../assets/img/create-dataset-template-other.png" width="500">

点击“CONTINUE TO FORM”继续。

在本次练习中，请创建一个用于航空 METAR 数据的数据集：

- 为数据集选择一个合适的“Local ID”，例如“aviation-metar”
- 为数据集提供一个标题和描述
- 选择 WMO 数据策略 = 'recommended'

<img alt="create-dataset-recommended" src="/../assets/img/create-dataset-aviation-metar-example.png" width="800">

请注意，当您选择 WMO 数据策略 = 'recommended' 时，数据集编辑器会自动添加一个“License URL”字段，这是推荐数据集的必填项。

接下来：

- 使用 `WIS2BOX_URL/data/aviation-license.html` 指向托管在您实例上的自定义许可证文件，将 `WIS2BOX_URL` 替换为您的 wis2box 实例的 URL。
- 选择 'Sub Disciple Topic' = 'aviation/metar' 以定义该数据集的正确主题。

![create-dataset-license-url](../assets/img/create-dataset-license-custom.png)

!!! note "关于许可证 URL"
    
    与推荐数据集关联的许可证 URL 告知数据消费者该数据集的使用条件。

    您可以使用指向托管在您 wis2box 实例上的许可证文件的 URL，或者使用指向托管在外部网站上的许可证文件的 URL。

    在本次练习中，我们将使用一个自托管的许可证文件。稍后您将把文件 'aviation-license.html' 添加到您的 wis2box 实例，以确保许可证 URL 有效。

由于您选择了 Template = 'other'，因此数据集未预填任何关键词。请为数据集添加至少 3 个相关关键词：

![create-dataset-metar-keywords](../assets/img/create-dataset-metar-keywords.png)

继续填写空间属性和联系信息的必填字段。点击“Validate form”检查所有必填字段是否已填写。

由于您选择了 Template = 'other'，因此未定义数据集映射。

请添加“Universal data without conversion”插件，并确保将文件扩展名设置为 `.txt`，以匹配您稍后将在本次实践课程中发布到该数据集的 METAR 数据文件：

![create-dataset-plugin-universal-txt](../assets/img/create-dataset-plugin-universal-txt.png)

提交数据集，使用之前创建的身份验证令牌，并检查新数据集是否已在 wis2box-webapp 中创建。

检查 MQTT Explorer，验证是否收到主题 `origin/a/wis2/<your-centre-id>/metadata` 上的新发现元数据记录的 WIS2 通知消息。

## 在 wis2box-api 中查看您的新数据集

通过在 Web 浏览器中打开 URL `WIS2BOX_URL/oapi/collections/discovery-metadata/items` 查看 wis2box-api 中的数据集列表，将 `WIS2BOX_URL` 替换为您的 wis2box 实例的 URL。

打开刚创建的数据集的链接，向下滚动到 JSON 响应的“links”部分：

<img alt="wis2box-api-recommended-dataset-links" src="/../assets/img/wis2box-api-recommended-dataset-links.png" width="600">

您应该会看到一个指向数据集编辑器中提供的 URL 的“License for this dataset”链接。

如果您点击该链接，由于许可证文件尚未添加到您的 wis2box 实例，您会收到一个错误。

## 将许可证文件添加到您的 wis2box 实例

确保推荐数据集元数据中的“License for this dataset”链接按预期工作。

下载此示例航空许可证文件：[aviation-license.html](./../../sample-data/aviation-license.html)

!!! note "关于示例航空许可证文件"

    这是一个航空数据的示例许可证文件。您可能需要编辑该文件以包含与您的组织相关的信息。

要上传此文件，请使用 wis2box 实例的 MinIO 控制台（可通过端口 9001 访问），在 Web 浏览器中访问 `http://YOUR-HOST:9001`

访问 MinIO 控制台的凭据在 wis2box.env 文件中由 `WIS2BOX_STORAGE_USERNAME` 和 `WIS2BOX_STORAGE_PASSWORD` 环境变量定义。

您可以通过以下方式在 `wis2box.env` 文件中找到这些变量：

```bash
cat wis2box.env | grep WIS2BOX_STORAGE_USERNAME
cat wis2box.env | grep WIS2BOX_STORAGE_PASSWORD
```

登录 MinIO 控制台后，使用“Upload”按钮将许可证文件上传到 **wis2box-public** bucket 的根路径：

<img alt="minio-upload-license" src="/../assets/img/minio-upload-license.png" width="800">

上传许可证文件后，通过访问 `WIS2BOX_URL/data/aviation-license.html` 检查文件是否可访问，将 `WIS2BOX_URL` 替换为您的 wis2box 实例的 URL。

!!! note

    wis2box 中的 web-proxy 会将存储在 "wis2box-public" bucket 中的所有文件代理到路径 `WIS2BOX_URL/data/`

推荐数据集元数据中包含的“License for this dataset”链接现在应按预期工作。

## 为数据集添加访问令牌

登录到 wis2box-management 容器，

```bash
cd ~/wis2box
python3 wis2box-ctl.py login
```

在容器内的命令行中，您可以使用 `wis2box auth add-token` 命令为数据集添加访问令牌，使用 `--metadata-id` 标志指定数据集的元数据标识符，并将访问令牌作为参数。

例如，为元数据标识符为 `urn:wmo:md:my-centre-id:core.surface-based-observations.synop` 的数据集添加访问令牌 `S3cr3tT0k3n`：

```bash
wis2box auth add-token --metadata-id urn:wmo:md:my-centre-id:aviation-metar S3cr3tT0k3n
```

退出 wis2box-management 容器：

```bash
exit
```

## 将数据发布到数据集

将以下示例 METAR 数据文件下载到您的本地计算机：

[A_SAKO31RKSL290000_C_RKSL_20250729000055.txt](../../sample-data/A_SAKO31RKSL290000_C_RKSL_20250729000055.txt)

然后使用 MinIO 控制台将此文件导入到您的数据集中。要访问 MinIO 控制台，请打开浏览器并访问 `http://YOUR-HOST:9001`，使用 `wis2box.env` 文件中由环境变量 `WIS2BOX_STORAGE_USERNAME` 和 `WIS2BOX_STORAGE_PASSWORD` 定义的凭据登录。

要将文件导入到您的数据集中，请进入 **wis2box-incoming** 存储桶，并创建一个与您的数据集元数据标识符相同名称的新文件夹，然后使用“Upload”按钮将示例 METAR 数据文件上传到此文件夹中：

![minio-wis2box-incoming-metar-data-uploaded](../assets/img/minio-wis2box-incoming-metar-data-uploaded.png)

确保文件夹名称与您的数据集的元数据标识符相同，并检查您是否在 MQTT Explorer 中的主题 `origin/a/wis2/<your-centre-id>/data/recommended/aviation/metar` 收到 WIS2 数据通知：

![mqtt-explorer-data-aviation-metar](../assets/img/mqtt-explorer-data-aviation-metar.png)

!!! note "故障排查"

    如果在上传数据后未收到通知，您可以检查 `wis2box-management` 容器的最近日志以排查问题：

    ```bash
    docker logs -n100 wis2box-management
    ```

将 WIS2 通知消息中的规范链接（canonical-link）的 URL 复制粘贴到您的浏览器中。URL 应类似于以下内容：

```
http://example.wis2.training/data/2025-07-29/wis/urn:wmo:md:int-wmo-example:aviation-metar/A_SAKO31RKSL290000_C_RKSL_20250729000055.txt
```

如果您正确地将访问令牌添加到数据集中，您应该**无法**在浏览器中访问数据，而是会看到一个错误 *401 Authorization Required*。

## 将访问令牌添加到 HTTP 头以访问数据集

为了演示访问数据集需要访问令牌，我们将使用命令行功能 `wget` 重现您在浏览器中看到的错误。

在学生虚拟机的命令行中，使用从 WIS2 通知消息中复制的规范链接运行 `wget` 命令。

```bash
wget http://example.wis2.training/data/2025-07-29/wis/urn:wmo:md:int-wmo-example:aviation-metar/A_SAKO31RKSL290000_C_RKSL_20250729000055.txt
```

您应该看到 HTTP 请求返回 *401 Unauthorized*，并且数据未下载。

现在将访问令牌添加到 HTTP 头以访问数据集。

```bash
wget --header="Authorization: Bearer S3cr3tT0k3n" <canonical-link>
```

现在数据应该能够成功下载。

## 从数据集中移除访问令牌

要从数据集中移除访问令牌，请登录到 wis2box-management 容器，

```bash
cd ~/wis2box
python3 wis2box-ctl.py login
```

并使用命令 `wis2box auth remove-token` 从数据集中移除访问令牌，使用标志 `--metadata-id` 指定数据集的元数据标识符，并将访问令牌作为参数：

```bash
wis2box auth remove-token --metadata-id urn:wmo:md:my-centre-id:aviation-metar S3cr3tT0k3n
```

确保将 `urn:wmo:md:my-centre-id:aviation-metar` 替换为您的数据集的元数据标识符。

退出 wis2box-management 容器：

```bash
exit
```

并通过尝试使用 HTTP 头中的访问令牌再次下载数据，或者尝试在浏览器中访问数据，验证访问令牌已被移除。

!!! note "访问控制是可选的，仅适用于推荐数据集"

    WIS2 规定推荐数据集*可以*对数据应用访问控制，但不是强制性的。您可以仅依赖许可证 URL 来告知数据消费者数据使用条件。如果您确实应用了访问控制，则您有责任将访问令牌分享给需要访问该数据的消费者。

    如果您对具有 WMO 数据政策“core”的数据集应用了 `wis2box auth add-token`，由于全球缓存无法下载数据，全球监控将报告错误，并且您的数据集将被视为*不符合* WIS2 技术法规。

## 总结

!!! success "恭喜！"
    在本次实践课程中，您学会了：

    - 创建具有“recommended”数据政策的新数据集
    - 为您的 wis2box 实例添加自定义许可证文件
    - 向数据集添加访问令牌
    - 验证在没有访问令牌的情况下无法访问数据集
    - 将访问令牌添加到 HTTP 头以访问数据集
---
title: 设置推荐数据集
---

# 设置推荐数据集

!!! abstract "学习成果"
    在本次实践课程结束时，您将能够：

    - 创建一个数据策略为“推荐”的新数据集
    - 为数据集添加访问令牌
    - 验证数据集无法在没有访问令牌的情况下访问
    - 将访问令牌添加到HTTP头以访问数据集
    - 在您的wis2box实例上托管自定义许可文件

## 简介

数据根据WMO统一数据政策在WIS2上共享，该政策定义了两类数据。

**核心**：免费且无限制提供的数据，无需付费且无使用条件。

**推荐**：可能附带使用条件和/或需遵守许可的数据。

共享为推荐的数据：

- 可能附带使用和重用条件
- 可能对数据应用访问控制
- 不会被WIS2全球缓存缓存
- 必须有一个包含许可URL的元数据记录

!!! note "下载推荐数据"
    
    由于WIS全球缓存不会缓存推荐数据，您将**不会**在主题`cache/a/wis2/<centre-id>/data/recommended/..`上看到通知。

    数据消费者必须通过数据提供者托管的数据服务器，从主题`origin/a/wis2/<centre-id>/data/recommended/...`的通知中提供的规范URL下载数据。

在本次实践课程中，您将使用wis2box-webapp中的数据集编辑器创建一个数据策略为“推荐”的新数据集。
您还将学习如何提供自托管许可以及如何选择性地添加访问控制。

!!! note "WIS2中的航空数据"
    
    在本次练习中，您需要创建一个数据集以共享METAR数据，这是一种用于报告航空气象观测的标准格式。

    由于航空气象数据受使用限制，适用**推荐**数据策略。

    更多信息请参阅[WIS2 Cookbook中关于发布航空气象数据的部分](https://wmo-im.github.io/wis2-cookbook/cookbook/latest/wis2-cookbook-STABLE.html#_publishing_aeronautical_meteorology_data_on_wis2)。

## 准备工作

确保您可以通过SSH访问您的学生虚拟机，并且您的wis2box实例正在运行。

确保您已使用MQTT Explorer连接到您的wis2box实例的MQTT代理。您可以使用公共凭证`everyone/everyone`连接到代理。

确保您已打开一个网页浏览器，并通过访问`http://YOUR-HOST/wis2box-webapp`进入您的实例的wis2box-webapp。

## 创建一个数据策略为“推荐”的新数据集

进入wis2box-webapp中的“数据集编辑器”页面并创建一个新数据集。

对于“Centre ID”，使用您在之前实践课程中使用的相同值。

选择模板 = 'other'，表示您不会为数据集使用预定义模板：

<img alt="create-dataset-recommended" src="/../assets/img/create-dataset-template-other.png" width="500">

点击“CONTINUE TO FORM”继续。

在本次练习中，请为航空METAR数据创建一个数据集：

- 为数据集选择一个合适的“Local ID”，例如“aviation-metar”
- 为数据集提供标题和描述
- 选择WMO数据策略 = 'recommended'

<img alt="create-dataset-recommended" src="/../assets/img/create-dataset-aviation-metar-example.png" width="800">

注意，当您选择WMO数据策略 = 'recommended'时，数据集编辑器会自动添加一个“License URL”字段，这是推荐数据集的必填项。

接下来：

- 使用`WIS2BOX_URL/data/aviation-license.html`指向托管在您的实例上的自定义许可文件，将`WIS2BOX_URL`替换为您的wis2box实例的URL。
- 选择“Sub Disciple Topic” = 'aviation/metar'以定义此数据集的正确主题。

![create-dataset-license-url](../assets/img/create-dataset-license-custom.png)

!!! note "关于许可URL"
    
    与推荐数据集相关联的许可URL向数据消费者告知此数据集的使用条件。

    您可以使用指向托管在您的wis2box实例上的许可文件的URL，也可以使用指向托管在外部网站上的许可文件的URL。

    在本次练习中，我们将使用自托管许可文件。稍后您将把文件“aviation-license.html”添加到您的wis2box实例中，以确保许可URL有效。

由于您选择了模板 = 'other'，数据集没有预填的关键词。请为数据集添加至少3个相关关键词：

![create-dataset-metar-keywords](../assets/img/create-dataset-metar-keywords.png)

继续填写空间属性和联系信息的必填字段。点击“Validate form”检查所有必填字段是否已填写。

由于您选择了模板 = 'other'，未定义数据集映射。

请添加“Universal data without conversion”插件，并确保将文件扩展名设置为`.txt`以匹配您稍后将在本次实践课程中发布到此数据集的METAR数据文件：

![create-dataset-plugin-universal-txt](../assets/img/create-dataset-plugin-universal-txt.png)

提交数据集，使用之前创建的认证令牌，并检查新数据集是否已在wis2box-webapp中创建。

检查MQTT Explorer以验证您是否收到主题`origin/a/wis2/<your-centre-id>/metadata`上的WIS2通知消息，宣布新的发现元数据记录。

## 在wis2box-api中查看您的新数据集

通过在网页浏览器中打开URL `WIS2BOX_URL/oapi/collections/discovery-metadata/items`查看wis2box-api中的数据集列表，将`WIS2BOX_URL`替换为您的wis2box实例的URL。

打开刚创建的数据集的链接并向下滚动到JSON响应的“links”部分：

<img alt="wis2box-api-recommended-dataset-links" src="/../assets/img/wis2box-api-recommended-dataset-links.png" width="600">

您应该看到一个指向数据集许可的链接，指向您在数据集编辑器中提供的URL。

如果您点击该链接，会出现错误，因为许可文件尚未添加到您的wis2box实例。

## 将许可文件添加到您的wis2box实例

确保推荐数据集元数据中的“License for this dataset”链接按预期工作。

下载此示例航空许可文件：[aviation-license.html](./../../sample-data/aviation-license.html)。 

!!! note "关于示例航空许可文件"

    这是航空数据的示例许可文件。您可能需要编辑文件以包含与您的组织相关的信息。

要上传此文件，请使用wis2box实例的MinIO控制台，该控制台可通过实例的9001端口访问，打开网页浏览器并访问`http://YOUR-HOST:9001`

访问MinIO控制台的凭证在wis2box.env文件中由环境变量`WIS2BOX_STORAGE_USERNAME`和`WIS2BOX_STORAGE_PASSWORD`定义。

您可以通过以下方式在`wis2box.env`文件中找到这些信息：

```bash
cat wis2box.env | grep WIS2BOX_STORAGE_USERNAME
cat wis2box.env | grep WIS2BOX_STORAGE_PASSWORD
```

登录MinIO控制台后，使用“Upload”按钮将许可文件上传到**wis2box-public**桶的基础路径：

<img alt="minio-upload-license" src="/../assets/img/minio-upload-license.png" width="800">

上传许可文件后，通过访问`WIS2BOX_URL/data/aviation-license.html`检查文件是否可访问，将`WIS2BOX_URL`替换为您的wis2box实例的URL。

!!! note

    wis2box中的web-proxy会代理存储在“wis2box-public”桶中的所有文件，并将其路径设置为`WIS2BOX_URL/data/`

推荐数据集元数据中包含的“License for this dataset”链接现在应该可以正常工作。

## 为数据集添加访问令牌

登录到wis2box-management容器，

```bash
cd ~/wis2box
python3 wis2box-ctl.py login
```

在容器内的命令行中，您可以使用`wis2box auth add-token`命令保护数据集，使用`--metadata-id`标志指定数据集的元数据标识符，并将访问令牌作为参数。

例如，要将访问令牌`S3cr3tT0k3n`添加到元数据标识符为`urn:wmo:md:my-centre-id:core.surface-based-observations.synop`的数据集：

```bash
wis2box auth add-token --metadata-id urn:wmo:md:my-centre-id:aviation-metar S3cr3tT0k3n
```

退出wis2box-management容器：

```bash
exit
```

## 将数据发布到数据集

下载以下示例METAR数据文件到您的本地机器：

[A_SAKO31RKSL290000_C_RKSL_20250729000055.txt](../../sample-data/A_SAKO31RKSL290000_C_RKSL_20250729000055.txt)

然后通过 MinIO 控制台将此文件导入到您的数据集中。要访问 MinIO 控制台，请打开网页浏览器并访问 `http://YOUR-HOST:9001`，使用 `wis2box.env` 文件中定义的环境变量 `WIS2BOX_STORAGE_USERNAME` 和 `WIS2BOX_STORAGE_PASSWORD` 登录。

要将文件导入到您的数据集中，请进入 **wis2box-incoming** 存储桶，并以您的数据集元数据标识符命名创建一个新文件夹，然后使用“上传”按钮将示例 METAR 数据文件上传到此文件夹中：

![minio-wis2box-incoming-metar-data-uploaded](../assets/img/minio-wis2box-incoming-metar-data-uploaded.png)

确保文件夹名称与您的数据集元数据标识符一致，并检查您是否在 MQTT Explorer 中收到 WIS2 数据通知，主题为 `origin/a/wis2/<your-centre-id>/data/recommended/aviation/metar`：

![mqtt-explorer-data-aviation-metar](../assets/img/mqtt-explorer-data-aviation-metar.png)

!!! note "故障排除"

    如果上传数据后未收到通知，可以检查 `wis2box-management` 容器的最近日志以排查问题：

    ```bash
    docker logs -n100 wis2box-management
    ```

将 WIS2 通知消息中的规范链接 URL 复制粘贴到您的网页浏览器中。URL 应类似于以下内容：

```
http://example.wis2.training/data/2025-07-29/wis/urn:wmo:md:int-wmo-example:aviation-metar/A_SAKO31RKSL290000_C_RKSL_20250729000055.txt
```

如果您正确地将访问令牌添加到数据集中，您应该**无法**在网页浏览器中访问数据，而是会看到错误 *401 Authorization Required*。

## 将访问令牌添加到 HTTP 头以访问数据集

为了演示访问数据集需要访问令牌，我们将使用命令行功能 `wget` 重现您在浏览器中看到的错误。

在您的学生虚拟机的命令行中，使用从 WIS2 通知消息中复制的规范链接运行 `wget` 命令。

```bash
wget http://example.wis2.training/data/2025-07-29/wis/urn:wmo:md:int-wmo-example:aviation-metar/A_SAKO31RKSL290000_C_RKSL_20250729000055.txt
```

您应该看到 HTTP 请求返回 *401 Unauthorized*，数据未被下载。

现在将访问令牌添加到 HTTP 头以访问数据集。

```bash
wget --header="Authorization: Bearer S3cr3tT0k3n" <canonical-link>
```

现在数据应该可以成功下载。

## 从数据集中移除访问令牌

要从数据集中移除访问令牌，请登录到 wis2box-management 容器，

```bash
cd ~/wis2box
python3 wis2box-ctl.py login
```

并使用命令 `wis2box auth remove-token` 移除数据集的访问令牌，使用标志 `--metadata-id` 指定数据集的元数据标识符，并将访问令牌作为参数：

```bash
wis2box auth remove-token --metadata-id urn:wmo:md:my-centre-id:aviation-metar S3cr3tT0k3n
```

确保将 `urn:wmo:md:my-centre-id:aviation-metar` 替换为您的数据集元数据标识符。

退出 wis2box-management 容器：

```bash
exit
```

并通过尝试使用 HTTP 头中的访问令牌下载数据或尝试在网页浏览器中访问数据来验证访问令牌已被移除。

!!! note "访问控制仅适用于推荐数据集"

    WIS2 规定推荐数据集*可以*对数据应用访问控制。这并不是强制性的，您可以仅依赖许可证 URL 来告知数据消费者数据使用条件。如果您确实应用了访问控制，您有责任将访问令牌分享给需要访问此数据的消费者。

    如果您对具有 WMO 数据政策“核心”的数据集应用了 `wis2box auth add-token`，Global Caches 将向 Global Monitoring 报告错误，因为它们无法下载数据，您的数据集将被视为*不符合* WIS2 技术法规。

## 结论

!!! success "恭喜！"
    在本次实践课程中，您学习了如何：

    - 创建具有数据政策“推荐”的新数据集
    - 向您的 wis2box 实例添加自定义许可证文件
    - 向数据集添加访问令牌
    - 验证数据集在没有访问令牌的情况下无法访问
    - 将访问令牌添加到 HTTP 头以访问数据集
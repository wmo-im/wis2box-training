---
title: 设置具有访问控制的推荐数据集
---

# 设置具有访问控制的推荐数据集

!!! abstract "学习目标"
    在本次实践课程结束时，您将能够：

    - 创建一个数据策略为“recommended”的新数据集
    - 为数据集添加访问令牌
    - 验证在没有访问令牌的情况下无法访问数据集
    - 将访问令牌添加到 HTTP 头以访问数据集
    - 在您的 wis2box 实例上添加一个自定义许可证文件

## 介绍

根据 WMO 统一数据政策，数据在 WIS2 上共享，该政策描述了两类数据：

- **core**：免费且无条件使用的数据，无需付费且对使用没有任何限制。
- **recommended**：可能附带使用条件和/或需要许可证的数据。

共享为 recommended 的数据：

- 可能附带使用和再使用的条件；
- 可能对数据应用访问控制；
- 不会被 Global Caches 缓存到 WIS2 中；
- 必须在发现元数据中包含指向数据使用条件的许可证链接。

在 wis2box-webapp 的 dataset-editor 中，当您选择数据策略为“recommended”时，系统将要求您提供许可证 URL。您还可以选择为此类数据集添加访问令牌以限制对数据的访问。

在本次实践课程中，您将创建一个数据策略为“recommended”的新数据集，并学习如何添加访问控制。
课程还将指导您如何将自定义许可证文件添加到您的 wis2box 实例。

## 准备工作

确保您可以通过 SSH 访问您的学生虚拟机，并且您的 wis2box 实例已启动并运行。

确保您已使用 MQTT Explorer 连接到您的 wis2box 实例的 MQTT broker。您可以使用公共凭据 `everyone/everyone` 连接到 broker。

确保您已打开一个 Web 浏览器，并通过访问 `http://YOUR-HOST/wis2box-webapp` 打开您的 wis2box 实例的 wis2box-webapp。

## 创建一个数据策略为“recommended”的新数据集

进入 wis2box-webapp 的 'dataset editor' 页面并创建一个新数据集。选择 Data Type = 'weather/surface-weather-observations/synop'。

<img alt="create-dataset-recommended" src="/../assets/img/create-dataset-template.png" width="800">

对于 "Centre ID"，使用您在之前实践课程中使用的相同值。

点击 'CONTINUE TO FORM' 继续。

将自动生成的 'Local ID' 替换为数据集的描述性名称，例如 'recommended-data-with-access-control'，并更新 'Title' 和 'Description' 字段：

<img alt="create-dataset-recommended" src="/../assets/img/create-dataset-recommended.png" width="800">

将 WMO 数据策略更改为“recommended”，您会看到表单中新增了一个输入字段，用于提供数据集许可证信息的 URL：

<img alt="create-dataset-license" src="/../assets/img/create-dataset-license.png" width="800">

您可以选择提供一个描述数据集使用条款的许可证 URL。例如，您可以使用  
`https://creativecommons.org/licenses/by/4.0/`  
指向 Creative Commons Attribution 4.0 International (CC BY 4.0) 许可证。

或者，您可以使用 `WIS2BOX_URL/data/license.txt` 指向您在自己的 Web 服务器上托管的自定义许可证文件，其中 `WIS2BOX_URL` 是您在 wis2box.env 文件中定义的 URL：

<img alt="create-dataset-license-url" src="/../assets/img/create-dataset-license-custom.png" width="800">

继续填写空间属性和联系信息的必填字段，并通过 'Validate form' 检查是否有任何错误。

最后，使用之前创建的身份验证令牌提交数据集，并检查新数据集是否已在 wis2box-webapp 中创建。

检查 MQTT Explorer，查看是否收到 WIS2 通知消息，宣布新发现元数据记录位于主题 `origin/a/wis2/<your-centre-id>/metadata`。

## 在 wis2box-api 中查看您的新数据集

通过在 Web 浏览器中打开 URL `WIS2BOX_URL/oapi/collections/discovery-metadata/items` 查看 wis2box-api 中的数据集列表，将 `WIS2BOX_URL` 替换为您的 wis2box 实例的 URL。

打开刚刚创建的数据集的链接，并向下滚动到 JSON 响应的 'links' 部分：

<img alt="wis2box-api-recommended-dataset-links" src="/../assets/img/wis2box-api-recommended-dataset-links.png" width="600">

您应该会看到一个指向您在数据集编辑器中提供的许可证 URL 的 "License for this dataset" 链接。

如果您使用了 `http://YOUR-HOST/data/license.txt` 作为许可证 URL，该链接目前将无法工作，因为我们尚未向 wis2box 实例添加许可证文件。

如果时间允许，您可以在本次实践课程结束时向您的 wis2box 实例添加自定义许可证文件。首先，我们将继续为数据集添加访问令牌。

## 为数据集添加访问令牌

登录到 wis2box-management 容器，

```bash
cd ~/wis2box
python3 wis2box-ctl.py login
```

在容器内的命令行中，您可以使用 `wis2box auth add-token` 命令为数据集添加安全性，使用 `--metadata-id` 标志指定数据集的元数据标识符，并将访问令牌作为参数。

例如，为元数据标识符为 `urn:wmo:md:not-my-centre:core.surface-based-observations.synop` 的数据集添加访问令牌 `S3cr3tT0k3n`：

```bash
wis2box auth add-token --metadata-id urn:wmo:md:not-my-centre:reco.surface-based-observations.synop S3cr3tT0k3n
```

退出 wis2box-management 容器：

```bash
exit
```

## 向数据集发布一些数据

将文件 `exercise-materials/access-control-exercises/aws-example.csv` 复制到 `wis2box.env` 中定义的 `WIS2BOX_HOST_DATADIR` 目录：

```bash
cp ~/exercise-materials/access-control-exercises/aws-example.csv ~/wis2box-data
```

然后使用 WinSCP 或命令行编辑器编辑文件 `aws-example.csv`，并将输入数据中的 WIGOS 站点标识符更新为与您的 wis2box 实例中的站点匹配。

接下来，进入 wis2box-webapp 的 station-editor。对于您在 `aws-example.csv` 中使用的每个站点，更新 'topic' 字段以匹配您在上一个练习中创建的数据集的 'topic'。

此站点现在将与两个主题相关联，一个用于 'core' 数据集，一个用于 'recommended' 数据集：

<img alt="edit-stations-add-topics" src="/../assets/img/edit-stations-add-topics.png" width="600">

您需要使用 `collections/stations` 的令牌保存更新的站点数据。

接下来，登录到 wis2box-management 容器：

```bash
cd ~/wis2box
python3 wis2box-ctl.py login
```

在 wis2box 命令行中，我们可以将示例数据文件 `aws-example.csv` 导入到特定数据集中，如下所示：

```bash
wis2box data ingest -p /data/wis2box/aws-example.csv --metadata-id urn:wmo:md:not-my-centre:reco.surface-based-observations.synop
```

确保为您的数据集提供正确的元数据标识符，并**检查您是否在 MQTT Explorer 中收到 WIS2 数据通知**，主题为 `origin/a/wis2/<your-centre-id>/data/recommended/surface-based-observations/synop`。

检查 WIS2 通知消息中的规范链接，并将链接复制/粘贴到浏览器中尝试下载数据。

您应该会看到 *401 Authorization Required*。

## 将访问令牌添加到 HTTP 头以访问数据集

为了演示访问数据集需要访问令牌，我们将使用命令行功能 `wget` 重现您在浏览器中看到的错误。

在学生虚拟机的命令行中，使用从 WIS2 通知消息中复制的规范链接运行 `wget` 命令。

```bash
wget <canonical-link>
```

您应该会看到 HTTP 请求返回 *401 Unauthorized*，数据未被下载。

现在将访问令牌添加到 HTTP 头以访问数据集。

```bash
wget --header="Authorization: Bearer S3cr3tT0k3n" <canonical-link>
```

现在数据应该会成功下载。

## 向您的 wis2box 实例添加自定义许可证文件

如果您希望提供由您的 wis2box 实例托管的自定义许可证，而不是使用外部许可证 URL，则需要执行此步骤。

使用您喜欢的文本编辑器在本地计算机上创建一个文本文件，并在文件中添加一些许可证信息，例如：

*这是一个具有访问控制的推荐数据集的自定义许可证文件。  
您可以自由使用此数据，但请注明数据提供者。*

要上传本地创建的文件 license.txt，请使用 wis2box 实例 9001 端口上的 MinIO Console，通过 Web 浏览器访问 `http://YOUR-HOST:9001`。

访问 MinIO Console 的凭据在 wis2box.env 文件中由 `WIS2BOX_STORAGE_USERNAME` 和 `WIS2BOX_STORAGE_PASSWORD` 环境变量定义。
您可以通过以下方式在 wis2box.env 文件中找到这些变量：

```bash
cat wis2box.env | grep WIS2BOX_STORAGE_USERNAME
cat wis2box.env | grep WIS2BOX_STORAGE_PASSWORD
```

登录到 MinIO Console 后，您可以使用“Upload”按钮将许可证文件上传到 **wis2box-public** bucket 的基本路径：

<img alt="minio-upload-license" src="/../assets/img/minio-upload-license.png" width="800">

上传许可证文件后，通过访问 `WIS2BOX_URL/data/license.txt` 检查文件是否可访问，将 `WIS2BOX_URL` 替换为您的 wis2box 实例的 URL。

!!! note

    wis2box 中的 Web 代理会将存储在 "wis2box-public" bucket 中的所有文件代理到路径 `WIS2BOX_URL/data/`

包含在推荐数据集元数据中的 "License for this dataset" 链接现在应该可以正常工作。

## 总结

!!! success "恭喜！"
    在本次实践课程中，您学习了如何：

    - 创建一个数据策略为“recommended”的新数据集
    - 为数据集添加访问令牌
    - 验证在没有访问令牌的情况下无法访问数据集
    - 将访问令牌添加到 HTTP 头以访问数据集
    - 向您的 wis2box 实例添加自定义许可证文件
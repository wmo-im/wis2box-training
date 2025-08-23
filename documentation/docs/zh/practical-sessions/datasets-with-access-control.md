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
    - 在您的 wis2box 实例中添加一个自定义许可文件

## 介绍

根据 WMO 统一数据政策，WIS2 上的数据共享分为两类：

- **core**：免费且无条件限制使用的数据，无需付费，且对使用没有任何限制
- **recommended**：可能附带使用条件和/或需要许可的数据

共享为“recommended”的数据：

- 可能附带使用和再使用的条件
- 可能对数据应用访问控制
- 不会被 WIS2 Global Cache Services 缓存
- 必须在发现元数据中包含指向数据使用条件许可的链接

在 wis2box-webapp 的数据集编辑器中，当您选择数据策略为“recommended”时，系统将要求您提供许可 URL。此外，您可以选择为数据集添加访问令牌，以限制数据访问。

在本次实践课程中，您将创建一个数据策略为“recommended”的新数据集，并学习如何添加访问控制。

本课程还将指导您如何在您的 wis2box 实例中添加自定义许可文件。

## 准备工作

确保您可以通过 SSH 访问您的学生虚拟机，并且您的 wis2box 实例已启动并运行。

确保您已使用 MQTT Explorer 连接到您的 wis2box 实例的 MQTT broker。您可以使用公共凭据 `everyone/everyone` 连接到 broker。

确保您已在浏览器中打开了您的 wis2box 实例的 wis2box-webapp，访问地址为 `http://YOUR-HOST/wis2box-webapp`。

## 创建一个数据策略为“recommended”的新数据集

进入 wis2box-webapp 的“dataset editor”页面，创建一个新数据集。选择 Data Type = 'weather/surface-weather-observations/synop'。

<img alt="create-dataset-recommended" src="/../assets/img/create-dataset-template.png" width="800">

对于“Centre ID”，使用您在之前实践课程中使用的相同值。

点击“CONTINUE TO FORM”继续。

将自动生成的“Local ID”替换为数据集的描述性名称，例如“recommended-data-with-access-control”，并更新“Title”和“Description”字段：

<img alt="create-dataset-recommended" src="/../assets/img/create-dataset-recommended.png" width="800">

将 WMO 数据策略更改为“recommended”，您会看到表单中新增了一个输入字段，用于提供数据集许可信息的 URL：

<img alt="create-dataset-license" src="/../assets/img/create-dataset-license.png" width="800">

您可以选择提供一个许可 URL 来描述数据集的使用条款。例如，使用 `https://creativecommons.org/licenses/by/4.0/` 指向 Creative Commons Attribution 4.0 International (CC BY 4.0) 许可。

或者使用 `WIS2BOX_URL/data/license.txt` 指向您自己托管在 web 服务器上的自定义许可文件，其中 `WIS2BOX_URL` 是您在 `wis2box.env` 文件中定义的 URL：

<img alt="create-dataset-license-url" src="/../assets/img/create-dataset-license-custom.png" width="800">

继续填写空间属性和联系信息的必填字段。点击“Validate form”检查是否有错误。

最后，使用之前创建的认证令牌提交数据集，并检查新数据集是否已在 wis2box-webapp 中创建。

使用 MQTT Explorer 验证您是否收到了 WIS2 通知消息，通知主题为 `origin/a/wis2/<your-centre-id>/metadata`。

## 在 wis2box-api 中查看您的新数据集

通过在浏览器中打开 URL `WIS2BOX_URL/oapi/collections/discovery-metadata/items` 查看 wis2box-api 中的数据集列表，将 `WIS2BOX_URL` 替换为您的 wis2box 实例的 URL。

打开刚刚创建的数据集的链接，向下滚动到 JSON 响应的“links”部分：

<img alt="wis2box-api-recommended-dataset-links" src="/../assets/img/wis2box-api-recommended-dataset-links.png" width="600">

您应该会看到一个指向数据集许可的链接，该链接指向您在数据集编辑器中提供的 URL。

如果您使用了 `http://YOUR-HOST/data/license.txt` 作为许可 URL，则该链接目前无法工作，因为我们尚未向 wis2box 实例添加许可文件。

如果时间允许，您可以在本次实践课程结束时向您的 wis2box 实例添加自定义许可文件。接下来，我们将继续为数据集添加访问令牌。

## 为数据集添加访问令牌

登录到 wis2box-management 容器，

```bash
cd ~/wis2box
python3 wis2box-ctl.py login
```

在容器内的命令行中，您可以使用 `wis2box auth add-token` 命令为数据集添加访问令牌，使用 `--metadata-id` 标志指定数据集的元数据标识符，并将访问令牌作为参数。

例如，为元数据标识符为 `urn:wmo:md:not-my-centre:core.surface-based-observations.synop` 的数据集添加访问令牌 `S3cr3tT0k3n`：

```bash
wis2box auth add-token --metadata-id urn:wmo:md:not-my-centre:reco.surface-based-observations.synop S3cr3tT0k3n
```

退出 wis2box-management 容器：

```bash
exit
```

## 发布一些数据到数据集

将文件 `exercise-materials/access-control-exercises/aws-example.csv` 复制到 `wis2box.env` 中定义的 `WIS2BOX_HOST_DATADIR` 目录：

```bash
cp ~/exercise-materials/access-control-exercises/aws-example.csv ~/wis2box-data
```

然后使用 WinSCP 或命令行编辑器编辑文件 `aws-example.csv`，将输入数据中的 WIGOS 站点标识符更新为与您的 wis2box 实例中的站点匹配。

接下来，进入 wis2box-webapp 的 station-editor。对于您在 `aws-example.csv` 中使用的每个站点，更新“topic”字段以匹配您在上一个练习中创建的数据集的“topic”。

此站点现在将与两个主题相关联，一个用于“core”数据集，另一个用于“recommended”数据集：

<img alt="edit-stations-add-topics" src="/../assets/img/edit-stations-add-topics.png" width="600">

您需要使用 `collections/stations` 的令牌保存更新的站点数据。

接下来，登录到 wis2box-management 容器：

```bash
cd ~/wis2box
python3 wis2box-ctl.py login
```

从 wis2box 命令行中，我们可以将示例数据文件 `aws-example.csv` 导入到特定数据集中，如下所示：

```bash
wis2box data ingest -p /data/wis2box/aws-example.csv --metadata-id urn:wmo:md:not-my-centre:reco.surface-based-observations.synop
```

确保提供正确的数据集元数据标识符，并**检查您是否在 MQTT Explorer 中收到 WIS2 数据通知**，通知主题为 `origin/a/wis2/<your-centre-id>/data/recommended/surface-based-observations/synop`。

检查 WIS2 通知消息中的规范链接，将链接复制并粘贴到浏览器中尝试下载数据。

您应该看到 *401 Authorization Required*。

## 将访问令牌添加到 HTTP 头以访问数据集

为了演示访问令牌是访问数据集所必需的，我们将使用命令行功能 `wget` 重现您在浏览器中看到的错误。

在学生虚拟机的命令行中，使用从 WIS2 通知消息中复制的规范链接运行 `wget` 命令。

```bash
wget <canonical-link>
```

您应该看到 HTTP 请求返回 *401 Unauthorized*，数据未被下载。

现在将访问令牌添加到 HTTP 头以访问数据集。

```bash
wget --header="Authorization: Bearer S3cr3tT0k3n" <canonical-link>
```

现在数据应该可以成功下载。

## 向您的 wis2box 实例添加自定义许可文件

如果您希望提供由您的 wis2box 实例托管的自定义许可，而不是使用外部许可 URL，则需要完成此步骤。

使用您喜欢的文本编辑器在本地机器上创建一个文本文件，并在文件中添加一些许可信息，例如：

*这是一个具有访问控制的推荐数据集的自定义许可文件。
您可以自由使用这些数据，但请注明数据提供者。*

要上传本地创建的名为 `license.txt` 的文件，请使用 wis2box 实例的 MinIO 控制台，该控制台可通过实例的 9001 端口访问，浏览器访问 `http://YOUR-HOST:9001`。

访问 MinIO 控制台的凭据由 `wis2box.env` 文件中的 `WIS2BOX_STORAGE_USERNAME` 和 `WIS2BOX_STORAGE_PASSWORD` 环境变量定义。

您可以通过以下方式在 `wis2box.env` 文件中找到这些变量：

```bash
cat wis2box.env | grep WIS2BOX_STORAGE_USERNAME
cat wis2box.env | grep WIS2BOX_STORAGE_PASSWORD
```

登录到 MinIO 控制台后，使用“Upload”按钮将许可文件上传到 **wis2box-public** bucket 的根路径：

<img alt="minio-upload-license" src="/../assets/img/minio-upload-license.png" width="800">

上传许可文件后，访问 `WIS2BOX_URL/data/license.txt` 检查文件是否可访问，将 `WIS2BOX_URL` 替换为您的 wis2box 实例的 URL。

!!! note

    wis2box 的 web-proxy 会将存储在 "wis2box-public" bucket 中的所有文件代理到路径 `WIS2BOX_URL/data/`

您推荐数据集元数据中包含的“License for this dataset”链接现在应该可以正常工作。

## 总结

!!! success "恭喜！"
    在本次实践课程中，您学习了如何：

    - 创建一个数据策略为“recommended”的新数据集
    - 为数据集添加访问令牌
    - 验证在没有访问令牌的情况下无法访问数据集
    - 将访问令牌添加到 HTTP 头以访问数据集
    - 向您的 wis2box 实例添加自定义许可文件
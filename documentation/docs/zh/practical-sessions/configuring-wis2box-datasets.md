---
title: 在 wis2box 中配置数据集
---

# 在 wis2box 中配置数据集

!!! abstract "学习目标"
    在本次实践课程结束时，您将能够：

    - 使用默认模板和自定义模板创建新数据集
    - 为您的数据集创建发现元数据
    - 配置数据集的数据映射
    - 使用 WCMP2 记录发布 WIS2 通知
    - 更新并重新发布您的数据集

## 介绍

wis2box 使用与发现元数据和数据映射相关联的数据集。

发现元数据用于创建一个 WCMP2（WMO 核心元数据配置文件 2）记录，该记录通过发布在您的 wis2box-broker 上的 WIS2 通知进行共享。

数据映射用于将数据插件与输入数据关联，从而在数据通过 WIS2 通知发布之前对其进行转换。

本课程将指导您使用默认模板和自定义模板创建新数据集，创建发现元数据，以及配置数据映射。您将通过 wis2box-api 检查您的数据集，并查看发现元数据的 WIS2 通知。

## 准备工作

使用 MQTT Explorer 连接到您的 broker。

请使用公共凭据 `everyone/everyone`，而不是内部 broker 的凭据：

<img alt="MQTT Explorer: Connect to broker" src="/../assets/img/mqtt-explorer-wis2box-broker-everyone-everyone.png" width="800">

!!! 注意

    您永远不需要与外部用户共享内部 broker 的凭据。'everyone' 用户是一个公共用户，用于共享 WIS2 通知。

    `everyone/everyone` 凭据对主题 'origin/a/wis2/#' 具有只读访问权限。这是发布 WIS2 通知的主题。Global Broker 可以使用这些公共凭据订阅以接收通知。
    
    'everyone' 用户无法查看内部主题或发布消息。
    
打开浏览器，访问 `http://YOUR-HOST/wis2box-webapp` 页面。确保您已登录并可以访问 'dataset editor' 页面。

如果您需要回忆如何连接到 broker 或访问 wis2box-webapp，请参阅 [初始化 wis2box](./initializing-wis2box.md) 部分。

## 为 processes/wis2box 创建授权令牌

您需要为 'processes/wis2box' 端点创建一个授权令牌以发布您的数据集。

要创建授权令牌，请通过 SSH 访问您的训练虚拟机，并使用以下命令登录到 wis2box-management 容器：

```bash
cd ~/wis2box
python3 wis2box-ctl.py login
```

然后运行以下命令，为 'processes/wis2box' 端点创建一个随机生成的授权令牌：

```bash
wis2box auth add-token --path processes/wis2box
```

您也可以通过将令牌作为参数提供给命令来创建具有特定值的令牌：

```bash
wis2box auth add-token --path processes/wis2box MyS3cretToken
```

确保复制令牌值并将其存储在本地计算机上，因为稍后您将需要它。

获得令牌后，您可以退出 wis2box-management 容器：

```bash
exit
```

## 在 wis2box-webapp 中创建新数据集

导航到您的 wis2box 实例的 wis2box-webapp 中的 'dataset editor' 页面，访问 `http://YOUR-HOST/wis2box-webapp`，然后从左侧菜单中选择 'dataset editor'。

在 'dataset editor' 页面中，点击 'Datasets' 标签下的 "Create New ...":

<img alt="Create New Dataset" src="/../assets/img/wis2box-create-new-dataset.png" width="800">

弹出窗口将要求您提供以下信息：

- **Centre ID**：这是由 WMO 成员指定的机构缩写（小写且无空格），用于标识负责发布数据的数据中心。
- **Template**：与您正在创建元数据的数据类型对应的模板。您可以选择使用预定义模板或选择 'other'。如果选择 'other'，则需要手动填写其他字段以定义自定义模板。

<img alt="Create New Dataset pop up" src="/../assets/img/wis2box-create-new-dataset-pop-up.png" width="600">

!!! 注意 "Centre ID"

    您的 centre-id 应以您国家的顶级域名（TLD）开头，后跟一个短横线 (`-`) 和您组织的缩写名称（例如 `fr-meteofrance`）。centre-id 必须为小写并仅使用字母数字字符。下拉列表显示了 WIS2 上当前注册的所有 centre-id 以及您已在 wis2box 中创建的任何 centre-id。请选择适合您组织的 centre-id。

!!! 注意 "Template"

    *Template* 字段允许您从 wis2box-webapp 数据集编辑器中提供的模板列表中进行选择。模板将预填充表单，提供与数据类型相关的默认建议值。这包括元数据的建议标题和关键字以及预配置的数据插件。主题会自动设置为与所选模板关联的默认主题。

    在本次培训中，我们将在创建新数据集时使用以下两种选项：
    
    1. 预定义的 *weather/surface-based-observations/synop* 模板，其中包含将数据转换为 BUFR 格式后发布的数据插件；
    2. *other* 模板，允许您通过手动填写所需字段来定义自己的自定义模板。

    如果您想使用 wis2box 发布 CAP 警报，请使用模板 *weather/advisories-warnings*。此模板包含一个数据插件，用于验证输入数据是否为有效的 CAP 警报后再发布。要创建 CAP 警报并通过 wis2box 发布，您可以使用 [WMO CAP Composer](https://github.com/World-Meteorological-Organization/cap-composer) 或将 CAP XML 从您自己的系统转发到 wis2box-incoming bucket。

现在，让我们通过使用预定义模板创建一个新数据集。

## 使用预定义模板创建新数据集

对于 **Template**，选择 **weather/surface-based-observations/synop**：

<img alt="Create New Dataset Form: Initial information" src="/../assets/img/wis2box-create-new-dataset-form-initial.png" width="450">

点击 *continue to form* 继续，您将看到 **Dataset Editor Form**。

由于您选择了 **weather/surface-based-observations/synop** 模板，表单将预填充与此数据类型相关的一些初始值。

### 创建发现元数据

Dataset Editor Form 允许您为数据集提供发现元数据，wis2box-management 容器将使用这些元数据发布 WCMP2 记录。

由于您选择了 'weather/surface-based-observations/synop' 模板，表单将预填充一些默认值。

请确保将自动生成的 'Local ID' 替换为数据集的描述性名称，例如 'synop-dataset-wis2training'：

<img alt="Metadata Editor: title, description, keywords" src="/../assets/img/wis2box-metadata-editor-part1.png" width="800">

检查标题和关键字，并根据需要更新它们，同时为您的数据集提供描述。

请注意，可以将 'WMO Data Policy' 从 'core' 更改为 'recommended'，或者修改默认的 Metadata Identifier，请保持数据策略为 'core' 并使用默认的 Metadata Identifier。

接下来，检查定义 'Temporal Properties' 和 'Spatial Properties' 的部分。您可以通过更新 'North Latitude'、'South Latitude'、'East Longitude' 和 'West Longitude' 字段来调整边界框：

<img alt="Metadata Editor: temporal properties, spatial properties" src="/../assets/img/wis2box-metadata-editor-part2.png" width="800">

接下来，填写定义 '数据提供者联系信息' 的部分：

<img alt="Metadata Editor: contact information" src="/../assets/img/wis2box-metadata-editor-part3.png" width="800">

最后，填写定义 '数据质量信息' 的部分：

完成所有部分后，点击 'VALIDATE FORM' 并检查表单是否有任何错误：

<img alt="Metadata Editor: validation" src="/../assets/img/wis2box-metadata-validation-error.png" width="800">

如果有任何错误，请更正并再次点击 'VALIDATE FORM'。

确保没有错误，并且您收到一个弹出窗口，指示表单已验证成功：

<img alt="Metadata Editor: validation success" src="/../assets/img/wis2box-metadata-validation-success.png" width="800">

接下来，在提交数据集之前，请检查数据集的数据映射。

### 配置数据映射

由于您使用模板创建了数据集，因此数据集映射已预填充为 'weather/surface-based-observations/synop' 模板的默认插件。数据插件在 wis2box 中用于在数据通过 WIS2 通知发布之前对其进行转换。

<img alt="Data Mappings: update plugin" src="/../assets/img/wis2box-data-mappings.png" width="800">

请注意，您可以点击“update”按钮更改插件的设置，例如文件扩展名和文件模式，目前可以保留默认设置。稍后在创建自定义数据集时会更详细地解释这些内容。

### 提交您的数据集

最后，您可以点击“submit”按钮发布您的数据集。

您需要提供之前为 'processes/wis2box' 创建的授权令牌。如果尚未创建，可以按照准备部分的说明创建一个新的令牌。

提交数据集后，请检查是否收到以下消息，表明数据集已成功提交：

<img alt="Submit Dataset Success" src="/../assets/img/wis2box-submit-dataset-success.png" width="400">

点击“OK”后，您将被重定向到数据集编辑器主页。现在，如果您点击“Dataset”选项卡，应该会看到您的新数据集已列出：

<img alt="Dataset Editor: new dataset" src="/../assets/img/wis2box-dataset-editor-new-dataset.png" width="800">

### 查看您的发现元数据的 WIS2 通知

打开 MQTT Explorer，如果您已连接到代理，应该会看到一个新的 WIS2 通知发布在主题 `origin/a/wis2/<your-centre-id>/metadata` 上：

<img alt="MQTT Explorer: WIS2 notification" src="/../assets/img/mqtt-explorer-wis2-notification-metadata.png" width="800">

检查您发布的 WIS2 通知的内容。您应该会看到一个符合 WIS 通知消息（WNM）格式的 JSON 结构。

!!! question

    WIS2 通知发布在哪个主题上？

??? success "点击查看答案"

    WIS2 通知发布在主题 `origin/a/wis2/<your-centre-id>/metadata` 上。

!!! question
    
    尝试在 WIS2 通知中找到您在发现元数据中提供的标题、描述和关键词。您能找到它们吗？

??? success "点击查看答案"

    **您在发现元数据中提供的标题、描述和关键词并未出现在 WIS2 通知的有效负载中！**

    相反，请尝试在 WIS2 通知的“links”部分中查找规范链接：

    <img alt="WIS2 notification for metadata, links sections" src="/../assets/img/wis2-notification-metadata-links.png" width="800">

    **WIS2 通知包含一个指向已发布 WCMP2 记录的规范链接。**

    将此规范链接复制粘贴到浏览器中以访问 WCMP2 记录。根据您的浏览器设置，可能会提示您下载文件，或者文件可能会直接显示在浏览器中。

    您将在 WCMP2 记录中找到您提供的标题、描述和关键词。

wis2box 仅提供有限数量的预定义模板。这些模板是为常见类型的数据集设计的，但可能并不总是适合于特殊数据。当预定义模板不适用时，可以创建自定义模板。这允许用户根据其数据集定义所需的元数据字段。

在下一部分中，我们将创建一个新数据集，并展示如何使用自定义模板进行配置。

## 通过配置自定义模板创建新数据集

对于 **Template**，选择 **other**：

<img alt="Create New Dataset Form: Initial information" src="/../assets/img/wis2box-create-new-dataset-form-initial-other.png" width="450">

点击 *continue to form* 继续，您现在将看到 **Dataset Editor Form**。

由于选择了 *other* 模板，下一步是点击 *Continue* 继续，您现在将看到数据集编辑器表单。在此表单中，用户必须填写或审核关键字段，例如标题、描述、子学科主题和关键词。实验性（自由文本主题）选项控制子学科主题的定义方式：如果选择此选项，子学科主题可以作为自由文本输入，允许用户定义自定义主题。如果未选择此选项，子学科主题将以下拉列表的形式呈现，必须选择预定义选项之一。

### 创建自定义发现元数据

在此阶段，您需要完成数据集编辑器表单中的必填字段，包括标题、描述、本地 ID、子学科主题和关键词。

在本次培训中，我们将使用自定义的全球集合预报系统（GEPS）数据集模板作为示例来完成这些字段。此示例仅供参考——在实际的 WIS2 操作中，用户应根据其自身数据集的要求自定义元数据字段。

<img alt="Metadata Editor: title, description, keywords" src="/../assets/img/wis2box-metadata-editor-part1-other.png" width="800">

<img alt="Metadata Editor: title, description, keywords" src="/../assets/img/wis2box-metadata-editor-part1-other-2.png" width="800">

后续步骤与使用预定义 synop 模板创建数据集时相同。有关详细说明，请参阅 *Create a new dataset by using a predefined template* 下的 *Creating discovery metadata* 部分。

### 配置自定义数据映射

当使用自定义模板时，不会提供默认数据映射。因此，数据集映射编辑器将为空，用户必须根据其具体需求配置映射。

<img alt="Data Mappings: update plugin" src="/../assets/img/wis2box-data-mappings-other1.png" width="800">

在本次培训中，我们将自定义一个 GEPS 数据集，并以通用数据无转换插件为例。此插件旨在发布数据而不应用任何转换。由于 GEPS 数据以 GRIB2 格式交付，因此文件扩展名必须设置为 .grib2；否则，数据无法成功发布。

需要特别注意 Regex 字段，因为它直接影响数据的摄取。如果正则表达式与数据文件的命名模式不匹配，将会发生发布错误。为避免这种情况，可以更新正则表达式以匹配您的数据集命名约定，或者保持默认正则表达式不变，并确保您的数据文件已相应重命名。

<img alt="Data Mappings: update plugin" src="/../assets/img/wis2box-data-mappings-other2.png" width="800">

在实际的 WIS2 操作中，用户可以根据需求选择不同的插件；这里我们仅以通用数据无转换插件为例。

如果您想发布其他类型和格式的数据，可以点击“update”按钮更改设置，例如文件扩展名和文件模式。

<img alt="Data Mappings: update plugin" src="/../assets/img/wis2box-data-mappings-other3.png" width="800">

### 提交您的自定义数据集

提交过程与 *Create a new dataset by using a predefined template* 下的 *Submitting your dataset* 部分中描述的相同。有关详细说明，请参阅该部分。

成功提交后，您的新数据集将出现在 Dataset 选项卡中：

<img alt="Dataset Editor: new dataset" src="/../assets/img/wis2box-dataset-editor-new-dataset-other.png" width="800">

### 查看您的发现元数据的 WIS2 通知

打开 MQTT Explorer，如果您已连接到代理，应该会看到一个新的 WIS2 通知发布在主题 `origin/a/wis2/<your-centre-id>/metadata` 上：

<img alt="MQTT Explorer: WIS2 notification" src="/../assets/img/mqtt-explorer-wis2-notification-metadata-other.png" width="800">

!!! question
    
    您创建的自定义 GEPS 数据集的元数据标识符是什么？

??? success "点击查看答案"

    打开 wis2box UI，您可以查看自定义 GEPS 数据集。元数据标识符是：

    *urn:wmo:md:nl-knmi-test:customized-geps-dataset-wis2-training*

!!! question

    如果我们修改一个数据集，会发送新的数据通知消息吗？会发生什么变化？

??? success "点击查看答案"

    会发送新的数据通知消息。在消息中，“links”元素中的 "rel": "canonical" 值将更改为 "rel": "update"，表明数据集已被修改。

!!! question
    
    如果我们删除一个数据集，会发送新的数据通知消息吗？会发生什么变化？

??? success "点击查看答案"

    会发送新的数据通知消息。在消息中，“links”元素中的 "rel": "canonical" 值将更改为 "rel": "deletion"，表明数据集已被删除。

## 总结

!!! success "恭喜！"
    在本次实践课程中，您学习了如何：

    - 使用默认模板和自定义模板创建新数据集
    - 定义您的发现元数据
    - 审核您的数据映射
    - 发布发现元数据
    - 查看您的发现元数据的 WIS2 通知
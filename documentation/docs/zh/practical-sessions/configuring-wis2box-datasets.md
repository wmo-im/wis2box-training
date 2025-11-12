---
title: 在 wis2box 中配置数据集
---

# 在 wis2box 中配置数据集

!!! abstract "学习目标"
    在本次实践课程结束时，您将能够：

    - 使用 wis2box-webapp 数据集编辑器
    - 使用模板=*weather/surface-based-observations/synop* 和模板=*other* 创建新的数据集
    - 定义您的发现元数据
    - 审核您的数据映射
    - 为您的发现元数据发布 WIS2 通知

## 简介

wis2box 使用与**发现元数据**和**数据映射**相关联的**数据集**。

**发现元数据**用于创建一个 WMO 核心元数据配置文件 (WCMP2) 记录，该记录通过在您的 wis2box broker 上发布的 WIS2 通知进行共享。

**数据映射**用于将数据插件与您的输入数据关联，使您的数据在发布到 WIS2 之前能够进行转换。

在本次实践课程中，您将学习如何使用 **wis2box-webapp 数据集编辑器**创建和配置数据集。

!!! note "不使用 wis2box-webapp 配置数据集"

    wis2box 还支持使用 [元数据控制文件 (MCF)](https://geopython.github.io/pygeometa/reference/mcf) 格式配置数据集，该格式由 [pygeometa](https://geopython.github.io/pygeometa) 工具定义。
    
    使用 MCF 提供了更多的灵活性和控制，但需要精确编写，因为您需要确保 MCF 格式和缩进正确，符合所需的架构。
    
    MCF 文件可以通过 wis2box-management 容器中的命令行发布。有关更多信息，请参阅 [wis2box 文档](https://docs.wis2box.wis.wmo.int/en/latest/reference/running/discovery-metadata.html)。

## 准备工作

使用 MQTT Explorer 连接到您的 broker。

不要使用您的内部 broker 凭据，而是使用公共凭据 `everyone/everyone`：

<img alt="MQTT Explorer: Connect to broker" src="/../assets/img/mqtt-explorer-wis2box-broker-everyone-everyone.png" width="800">

!!! 注意

    您永远不需要与外部用户共享您的内部 broker 的凭据。'everyone' 用户是一个公共用户，用于共享 WIS2 通知。

    `everyone/everyone` 凭据对主题 'origin/a/wis2/#' 具有只读访问权限。此主题是发布 WIS2 通知的地方。Global Broker 可以使用这些公共凭据订阅以接收通知。
    
    'everyone' 用户无法查看内部主题或发布消息。
    
打开浏览器并访问 `http://YOUR-HOST/wis2box-webapp`。确保您已登录并可以访问 'dataset editor' 页面。

如果您需要回忆如何连接到 broker 或访问 wis2box-webapp，请参阅 [初始化 wis2box](./initializing-wis2box.md) 部分。

## 为 processes/wis2box 创建授权令牌

您将需要为 'processes/wis2box' 端点创建一个授权令牌以发布您的数据集。

要创建授权令牌，请通过 SSH 访问您的培训虚拟机，并使用以下命令：

```bash
cd ~/wis2box
python3 wis2box-ctl.py login
```

然后运行以下命令，为 'processes/wis2box' 端点创建一个随机生成的授权令牌：

```bash
wis2box auth add-token --path processes/wis2box
```

您还可以通过将令牌作为命令的参数提供，创建具有特定值的令牌：

```bash
wis2box auth add-token --path processes/wis2box MyS3cretToken
```

请确保复制令牌值并将其存储在您的本地计算机上，因为稍后您将需要它。

获得令牌后，您可以退出 wis2box-management 容器：

```bash
exit
```

## wis2box-webapp 数据集编辑器

通过浏览器访问您的 wis2box 实例中的 wis2box-webapp 的 'dataset editor' 页面，网址为 `http://YOUR-HOST/wis2box-webapp`，然后从左侧菜单中选择 'dataset editor'。

在 'dataset editor' 页面中，点击 'Datasets' 标签下的 "Create New ...":

<img alt="Create New Dataset" src="/../assets/img/wis2box-create-new-dataset.png" width="800">

一个弹窗将出现，要求您提供以下信息：

- **Centre ID**：这是由 WMO 成员指定的负责发布数据的数据中心的机构缩写（小写且无空格）。
- **Template**：您正在为其创建元数据的数据类型。您可以选择使用预定义模板或选择 *other*。

<img alt="Create New Dataset pop up" src="/../assets/img/wis2box-create-new-dataset-pop-up.png" width="600">

!!! 注意 "Centre ID"

    您的 Centre ID 应以您国家的顶级域名 (TLD) 开头，后跟一个短横线 (`-`) 和您组织的缩写名称（例如 `fr-meteofrance`）。Centre ID 必须是小写，并且仅使用字母数字字符。下拉列表显示了 WIS2 上当前注册的所有 Centre ID，以及您已在 wis2box 中创建的任何 Centre ID。请选择适合您组织的 Centre ID。

!!! 注意 "Template"

    *Template* 字段允许您从 wis2box-webapp 数据集编辑器中提供的模板列表中选择。模板将使用适合数据类型的建议默认值预填表单。这包括建议的元数据标题和关键字，以及预配置的数据插件。
    
    主题会自动设置为与所选模板链接的默认主题，除非您选择 *other*。如果您选择 *other*，则可以从基于 [WIS2 主题层次结构](https://codes.wmo.int/wis/topic-hierarchy/_earth-system-discipline) 的下拉列表中定义主题。

在培训过程中，您将创建两个数据集：
    
- 使用模板=*weather/surface-based-observations/synop* 的数据集，其中包括将数据转换为 BUFR 格式后发布的数据插件。
- 使用模板=*other* 的数据集，您需要定义 WIS2 主题，并使用 "Universal" 插件在不进行转换的情况下发布数据。

## Template=weather/surface-based-observations/synop

对于 **Template**，选择 **weather/surface-based-observations/synop**：

<img alt="Create New Dataset Form: Initial information" src="/../assets/img/wis2box-create-new-dataset-form-initial.png" width="450">

点击 *continue to form* 继续。您现在将看到 **Dataset Editor Form**。

由于您选择了 **weather/surface-based-observations/synop** 模板，表单将预填与此数据类型相关的一些初始值。

### 创建发现元数据

Dataset Editor Form 允许您为您的数据集提供发现元数据，wis2box-management 容器将使用这些元数据发布 WCMP2 记录。

由于您选择了 'weather/surface-based-observations/synop' 模板，表单将预填一些默认值。

请确保将自动生成的 'Local ID' 替换为数据集的描述性名称，例如 'synop-dataset-wis2training'：

<img alt="Metadata Editor: title, description, keywords" src="/../assets/img/wis2box-metadata-editor-part1.png" width="800">

审核标题和关键字，根据需要进行更新，并为您的数据集提供描述。

注意，可以将 'WMO Data Policy' 从 'core' 更改为 'recommended'，或者修改默认的 Metadata Identifier。请保持数据政策为 'core' 并使用默认的 Metadata Identifier。

接下来，审核定义 'Temporal Properties' 和 'Spatial Properties' 的部分。您可以通过更新 'North Latitude'、'South Latitude'、'East Longitude' 和 'West Longitude' 字段来调整边界框：

<img alt="Metadata Editor: temporal properties, spatial properties" src="/../assets/img/wis2box-metadata-editor-part2.png" width="800">

接下来，填写定义 '数据提供者联系信息' 的部分：

<img alt="Metadata Editor: contact information" src="/../assets/img/wis2box-metadata-editor-part3.png" width="800">

最后，填写定义 '数据质量信息' 的部分：

完成所有部分后，点击 'VALIDATE FORM' 并检查表单是否有错误：

<img alt="Metadata Editor: validation" src="/../assets/img/wis2box-metadata-validation-error.png" width="800">

如果有任何错误，请进行修正，然后再次点击 'VALIDATE FORM'。

确保没有错误，并且您收到一个弹窗，指示您的表单已验证成功：

<img alt="Metadata Editor: validation success" src="/../assets/img/wis2box-metadata-validation-success.png" width="800">

接下来，在提交数据集之前，请审核您的数据集的数据映射。

### 配置数据映射

由于您使用模板创建了数据集，因此数据集映射已预先填充了适用于 'weather/surface-based-observations/synop' 模板的默认插件。数据插件用于在数据发布到 WIS2 通知之前对数据进行转换。

<img alt="Data Mappings: update plugin" src="/../assets/img/wis2box-data-mappings.png" width="800">

请注意，您可以点击“Update”按钮更改插件的设置，例如文件扩展名和文件模式。您现在可以保留默认设置。

### 提交您的数据集

最后，您可以点击“submit”来发布您的数据集。

您需要提供之前创建的 'processes/wis2box' 的授权令牌。如果尚未创建，可以按照准备部分的说明创建新的令牌。

提交数据集后，请检查是否收到以下消息，表明数据集已成功提交：

<img alt="Submit Dataset Success" src="/../assets/img/wis2box-submit-dataset-success.png" width="400">

点击“OK”后，您将被重定向到数据集编辑器主页。如果您点击“Dataset”标签，应该可以看到您的新数据集已列出：

<img alt="Dataset Editor: new dataset" src="/../assets/img/wis2box-dataset-editor-new-dataset.png" width="800">

### 审查发现元数据的 WIS2 通知

打开 MQTT Explorer。如果您已连接到代理，应该会看到一个新的 WIS2 通知发布到主题 `origin/a/wis2/<your-centre-id>/metadata`：

<img alt="MQTT Explorer: WIS2 notification" src="/../assets/img/mqtt-explorer-wis2-notification-metadata.png" width="800">

!!! note "触发发现元数据的重新发布"
    WIS2 通知会在发现元数据成功提交后立即发布。如果您没有看到通知，可能是因为发布时您未连接到代理。
    
    如果您没有看到 WIS2 通知，可以使用以下命令手动触发发现元数据的重新发布：
    
    ```bash
    python3 wis2box-ctl.py execute wis2box metadata discovery republish
    ```

检查您发布的 WIS2 通知内容。您应该会看到一个 JSON，其结构符合 WIS 通知消息 (WNM) 格式。

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

    **WIS2 通知包含已发布的 WCMP2 记录的规范链接。**
    
    将此规范链接复制并粘贴到浏览器中以访问 WCMP2 记录。根据您的浏览器设置，可能会提示您下载文件，也可能直接在浏览器中显示。

    您将在 WCMP2 记录中找到您提供的标题、描述和关键词。

wis2box 仅提供有限数量的预定义模板。这些模板是为常见类型的数据集设计的，但可能并不总是适用于专业数据。对于所有其他类型的数据集，您可以通过选择 Template=*other* 来创建数据集。

## Template=other

接下来，我们将使用 Template=*other* 创建第二个数据集。

再次点击“Create New ...”以创建新的数据集。使用您之前使用的相同 centre-id，它应该在下拉列表中可用。对于 **Template**，选择 **other**：

<img alt="Create New Dataset Form: Initial information" src="/../assets/img/wis2box-create-new-dataset-form-initial-other.png" width="450">

点击 *continue to form* 继续，您将再次看到 **Dataset Editor Form**。

### 创建发现元数据

为“Title”和“Description”字段提供您自己的值，并确保将自动生成的“Local ID”替换为数据集的描述性名称：

<img alt="Metadata Editor: title, description, keywords" src="/../assets/img/wis2box-metadata-editor-part1-other.png" width="800">

请注意，由于您选择了 Template=*other*，需要您使用下拉列表为“Discipline”和“Sub-Discipline”定义 WIS2 主题层次结构。

在本练习中，请选择子学科主题 "prediction/analysis/medium-range/deterministic/global"：

<img alt="Metadata Editor: title, description, keywords" src="/../assets/img/wis2box-metadata-editor-part1-other-topic.png" width="800">

由于您使用了 Template=*other*，没有预定义的关键词。请确保添加至少 3 个您自己选择的关键词：

<img alt="Metadata Editor: title, description, keywords" src="/../assets/img/wis2box-metadata-editor-part1-other-2.png" width="800">

填写必填字段后，完成表单的其余部分，包括“Temporal Properties”、“Spatial Properties”和“Contact Information of the Data Provider”，并确保验证表单。

### 配置数据映射

使用 Template=other 时，没有默认数据映射。因此，数据集映射编辑器将为空，用户必须根据具体需求配置映射。

<img alt="Data Mappings: update plugin" src="/../assets/img/wis2box-data-mappings-other1.png" width="800">

点击“ADD A PLUGIN +”以向数据集添加数据插件。

选择名称为 **"Universal data without conversion"** 的插件。此插件旨在发布数据而不进行任何转换。

添加此插件时，您需要指定 **File Extension** 和 **File Pattern**（由正则表达式定义），以匹配数据文件的命名模式。对于 "Universal"-插件，File Pattern 还用于确定数据的 "datetime"-属性。

!!! Note "从文件名解析日期时间"

    "Universal"-插件假定正则表达式中的第一个分组对应于数据的日期时间。

    默认 File Pattern 是 `^.*?_(\d{8}).*?\..*$`，匹配下划线后跟 8 位数字，再后跟任意字符和文件扩展名前的点。例如：

    - `mydata_20250101.txt` 将匹配并提取 2025 年 1 月 25 日作为数据的日期时间属性
    - `mydata_2025010112.txt` 将不匹配，因为有 10 位数字而不是 8 位
    - `mydata-20250101.txt` 将不匹配，因为日期前是连字符而不是下划线

    使用 "Universal"-插件时，可以将文件重命名为匹配默认值，或者更新 File Pattern，确保正则表达式中的第一个分组对应于日期时间。

暂时保留 "File Name" 的默认值，因为它们与您将在下一个实践环节中导入的数据匹配：

<img alt="Data Mappings: update plugin" src="/../assets/img/wis2box-data-mappings-other2.png" width="800">

点击“SAVE”以保存插件设置，并验证您现在可以在数据集映射编辑器中看到插件已列出：

<img alt="Data Mappings: update plugin" src="/../assets/img/wis2box-data-mappings-other3.png" width="800">

请注意，当您导入数据时，文件扩展名和文件名的 File Pattern 必须与您在此处提供的设置匹配，否则数据将无法处理，wis2box-management 容器将记录 ERROR 消息。

### 提交并查看结果

最后，提供之前创建的 'processes/wis2box' 的授权令牌并点击“submit”以发布您的数据集。

成功提交后，您的新数据集将出现在 Dataset 标签中：

<img alt="Dataset Editor: new dataset" src="/../assets/img/wis2box-dataset-editor-new-dataset-other.png" width="800">

打开 MQTT Explorer，如果您已连接到代理，应该会看到另一个新的 WIS2 通知发布到主题 `origin/a/wis2/<your-centre-id>/metadata`。

!!! question
    
    访问 wis2box-UI，地址为 `http://YOUR-HOST`。
    
    您看到列出了多少个数据集？如何查看每个数据集使用的 WIS2 主题层次结构以及如何查看每个数据集的描述？

??? success "点击查看答案"

通过打开 `http://YOUR-HOST` 上的 wis2box UI，您应该会看到列出的两个数据集及其 WIS2 主题层次结构。要查看每个数据集的描述，您可以点击“metadata”，它将重定向到由 wis2box-api 提供的相应 'discovery-metadata'-项。

!!! question

尝试更新您创建的最后一个数据集的描述。在更新描述后，您是否看到一个新的 WIS2 通知发布在主题 `origin/a/wis2/<your-centre-id>/metadata` 上？新的通知与之前的通知有什么不同？

??? success "点击查看答案"

您应该会看到在主题 `origin/a/wis2/<your-centre-id>/metadata` 上发送了一条新的数据通知消息，表明您的数据集已更新。

在消息中，*"rel": "canonical"* 的值将更改为 *"rel": "update"*，表示之前发布的数据已被修改。要查看更新后的描述，请将 URL 复制并粘贴到浏览器中，您应该会看到更新后的描述。

!!! question

尝试通过更改“Sub-Discipline Topics”中的选择来更新您创建的最后一个数据集的主题层次结构。您是否看到一个新的 WIS2 通知发布在主题 `origin/a/wis2/<your-centre-id>/metadata` 上？

??? success "点击查看答案"

您**无法**更新现有数据集的主题层次结构。在数据集创建后，数据集编辑表单中的主题层次结构字段将被禁用。如果您想使用不同的主题层次结构，请先删除现有数据集，然后使用所需的主题层次结构创建一个新的数据集。

## 结论

!!! success "恭喜！"
在本次实践课程中，您学习了如何：

- 使用 wis2box-webapp 数据集编辑器
- 使用 Template=*weather/surface-based-observations/synop* 和 Template=*other* 创建新数据集
- 定义您的 discovery metadata
- 审核您的数据映射
- 发布 discovery metadata 并查看 WIS2 通知
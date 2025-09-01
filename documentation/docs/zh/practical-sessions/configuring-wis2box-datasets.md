---
title: 在 wis2box 中配置数据集
---

# 在 wis2box 中配置数据集

!!! abstract "学习目标"
    在本次实践课程结束时，您将能够：

    - 使用 wis2box-webapp 数据集编辑器
    - 使用 Template=*weather/surface-based-observations/synop* 和 Template=*other* 创建新数据集
    - 定义您的发现元数据
    - 审查数据映射
    - 为您的发现元数据发布 WIS2 通知
    - 审查您的发现元数据的 WIS2 通知

## 简介

wis2box 使用与发现元数据和数据映射相关联的数据集。

发现元数据用于创建 WCMP2 (WMO Core Metadata Profile 2) 记录，该记录通过在您的 wis2box-broker 上发布的 WIS2 通知进行共享。

数据映射用于将数据插件与输入数据关联，从而在通过 WIS2 通知发布之前对数据进行转换。

本课程将指导您使用默认模板和自定义模板创建新数据集，创建发现元数据，并配置数据映射。您将通过 wis2box-api 检查您的数据集，并审查发现元数据的 WIS2 通知。

## 准备工作

使用 MQTT Explorer 连接到您的 broker。

请使用公共凭据 `everyone/everyone`，而不是使用内部 broker 凭据：

<img alt="MQTT Explorer: 连接到 broker" src="/../assets/img/mqtt-explorer-wis2box-broker-everyone-everyone.png" width="800">

!!! Note

    您永远不需要与外部用户共享内部 broker 的凭据。'everyone' 用户是一个公共用户，用于启用 WIS2 通知的共享。

    `everyone/everyone` 凭据对主题 'origin/a/wis2/#' 具有只读访问权限。WIS2 通知会发布到该主题。Global Broker 可以使用这些公共凭据订阅以接收通知。
    
    'everyone' 用户无法查看内部主题或发布消息。
    
打开浏览器并访问 `http://YOUR-HOST/wis2box-webapp`。确保您已登录并可以访问 'dataset editor' 页面。

如果您需要回忆如何连接到 broker 或访问 wis2box-webapp，请参阅 [初始化 wis2box](./initializing-wis2box.md) 部分。

## 为 processes/wis2box 创建授权令牌

您需要为 'processes/wis2box' 端点创建授权令牌以发布您的数据集。

要创建授权令牌，请通过 SSH 访问您的训练虚拟机，并使用以下命令登录到 wis2box-management 容器：

```bash
cd ~/wis2box
python3 wis2box-ctl.py login
```

然后运行以下命令，为 'processes/wis2box' 端点创建一个随机生成的授权令牌：

```bash
wis2box auth add-token --path processes/wis2box
```

您还可以通过将令牌作为参数提供给命令来创建具有特定值的令牌：

```bash
wis2box auth add-token --path processes/wis2box MyS3cretToken
```

请确保复制令牌值并将其存储在本地计算机上，因为稍后您将需要它。

获得令牌后，您可以退出 wis2box-management 容器：

```bash
exit
```

## 使用数据集编辑器

通过访问 `http://YOUR-HOST/wis2box-webapp` 并从左侧菜单中选择 'dataset editor'，导航到您的 wis2box 实例中的 'dataset editor' 页面。

在 'dataset editor' 页面上的 'Datasets' 选项卡下，点击 "Create New ...":

<img alt="创建新数据集" src="/../assets/img/wis2box-create-new-dataset.png" width="800">

将弹出一个窗口，要求您提供以下信息：

- **Centre ID**：这是由 WMO 成员指定的机构缩写（小写且无空格），用于标识负责发布数据的数据中心。
- **Template**：您正在为其创建元数据的数据类型。您可以选择使用预定义模板或选择 *other*。

<img alt="创建新数据集弹出窗口" src="/../assets/img/wis2box-create-new-dataset-pop-up.png" width="600">

!!! Note "Centre ID"

    您的 centre-id 应以您国家的顶级域名（TLD）开头，后跟一个短横线 (`-`) 和您组织的缩写名称（例如 `fr-meteofrance`）。centre-id 必须为小写，仅使用字母数字字符。下拉列表显示了 WIS2 上当前注册的所有 centre-id 以及您已在 wis2box 中创建的任何 centre-id。请选择适合您组织的 centre-id。

!!! Note "Template"

    *Template* 字段允许您从 wis2box-webapp 数据集编辑器中可用的模板列表中进行选择。模板将使用适合数据类型的建议默认值预填充表单。这包括元数据的建议标题和关键字以及预配置的数据插件。
    
    除非您选择 *other*，否则主题会自动设置为与所选模板关联的默认主题。如果选择 *other*，则可以从基于 [WIS2 主题层次结构](https://codes.wmo.int/wis/topic-hierarchy/_earth-system-discipline) 的下拉列表中定义主题。

在本次培训中，您将创建两个数据集：
    
- 使用 Template=*weather/surface-based-observations/synop* 的数据集，其中包括在发布前将数据转换为 BUFR 格式的数据插件；
- 使用 Template=*Other* 的数据集，您需要定义 WIS2 主题，并使用 "Universal"-plugin 在不进行转换的情况下发布数据。

## Template=weather/surface-based-observations/synop

对于 **Template**，选择 **weather/surface-based-observations/synop**：

<img alt="创建新数据集表单：初始信息" src="/../assets/img/wis2box-create-new-dataset-form-initial.png" width="450">

点击 *continue to form* 继续，您将看到 **Dataset Editor Form**。

由于您选择了 **weather/surface-based-observations/synop** 模板，表单将预填充与此数据类型相关的一些初始值。

### 创建发现元数据

Dataset Editor Form 允许您为数据集提供发现元数据，wis2box-management 容器将使用这些元数据发布 WCMP2 记录。

由于您选择了 'weather/surface-based-observations/synop' 模板，表单将预填充一些默认值。

请确保将自动生成的 'Local ID' 替换为数据集的描述性名称，例如 'synop-dataset-wis2training'：

<img alt="元数据编辑器：标题、描述、关键字" src="/../assets/img/wis2box-metadata-editor-part1.png" width="800">

审查标题和关键字，并根据需要更新它们，同时为您的数据集提供描述。

请注意，可以将 'WMO Data Policy' 从 'core' 更改为 'recommended'，或修改默认的 Metadata Identifier，请保持数据策略为 'core' 并使用默认的 Metadata Identifier。

接下来，审查定义 'Temporal Properties' 和 'Spatial Properties' 的部分。您可以通过更新 'North Latitude'、'South Latitude'、'East Longitude' 和 'West Longitude' 字段来调整边界框：

<img alt="元数据编辑器：时间属性、空间属性" src="/../assets/img/wis2box-metadata-editor-part2.png" width="800">

接下来，填写定义 '数据提供者联系信息' 的部分：

<img alt="元数据编辑器：联系信息" src="/../assets/img/wis2box-metadata-editor-part3.png" width="800">

最后，填写定义 '数据质量信息' 的部分：

完成所有部分后，点击 'VALIDATE FORM' 并检查表单是否有任何错误：

<img alt="元数据编辑器：验证" src="/../assets/img/wis2box-metadata-validation-error.png" width="800">

如果有任何错误，请更正并再次点击 'VALIDATE FORM'。

确保没有错误并且弹出窗口显示表单已验证成功：

<img alt="元数据编辑器：验证成功" src="/../assets/img/wis2box-metadata-validation-success.png" width="800">

接下来，在提交数据集之前，审查数据集的数据映射。

### 配置数据映射

由于您使用模板创建数据集，数据集映射已使用 'weather/surface-based-observations/synop' 模板的默认插件预填充。数据插件在 wis2box 中用于在通过 WIS2 通知发布之前转换数据。

<img alt="数据映射：更新插件" src="/../assets/img/wis2box-data-mappings.png" width="800">

请注意，您可以点击 "update" 按钮更改插件的设置，例如文件扩展名和文件模式，目前可以保留默认设置。稍后在创建自定义数据集时将详细解释这一点。

### 提交数据集

最后，您可以点击 'submit' 发布您的数据集。

您需要提供之前创建的 'processes/wis2box' 的授权令牌。如果尚未创建，可以按照准备部分的说明创建一个新的令牌。

提交数据集后，请检查是否收到以下消息，表明数据集已成功提交：

<img alt="Submit Dataset Success" src="/../assets/img/wis2box-submit-dataset-success.png" width="400">

点击 'OK' 后，您将被重定向到数据集编辑器主页。现在，如果点击 'Dataset' 标签，您应该会看到新创建的数据集已列出：

<img alt="Dataset Editor: new dataset" src="/../assets/img/wis2box-dataset-editor-new-dataset.png" width="800">

### 审查发现元数据的 WIS2 通知

打开 MQTT Explorer，如果您已连接到代理，应该会看到一个新的 WIS2 通知发布在主题 `origin/a/wis2/<your-centre-id>/metadata` 上：

<img alt="MQTT Explorer: WIS2 notification" src="/../assets/img/mqtt-explorer-wis2-notification-metadata.png" width="800">

检查您发布的 WIS2 通知的内容。您应该会看到一个符合 WIS Notification Message (WNM) 格式的 JSON 结构。

!!! question

    WIS2 通知发布在哪个主题上？

??? success "点击查看答案"

    WIS2 通知发布在主题 `origin/a/wis2/<your-centre-id>/metadata` 上。

!!! question
    
    尝试在 WIS2 通知中找到您在发现元数据中提供的标题、描述和关键词。您能找到它们吗？

??? success "点击查看答案"

    **您在发现元数据中提供的标题、描述和关键词并未出现在 WIS2 通知的有效负载中！** 
    
    相反，请尝试在 WIS2 通知的 "links" 部分中查找规范链接：

    <img alt="WIS2 notification for metadata, links sections" src="/../assets/img/wis2-notification-metadata-links.png" width="800">

    **WIS2 通知包含指向已发布 WCMP2 记录的规范链接。** 
    
    将此规范链接复制并粘贴到浏览器中以访问 WCMP2 记录。根据您的浏览器设置，可能会提示您下载文件，或者直接在浏览器中显示。

    您将在 WCMP2 记录中找到您提供的标题、描述和关键词。

wis2box 仅提供有限数量的预定义模板。这些模板是为常见类型的数据集设计的，但可能无法始终匹配特定数据。对于所有其他类型的数据集，您可以通过选择 Template=*other* 来创建数据集。

## Template=other

接下来，我们将使用 Template=*other* 创建第二个数据集。

再次点击 "Create New ..." 来创建一个新数据集。使用之前使用的相同 centre-id，它应该可以在下拉列表中找到。对于 **Template**，选择 **other**：

<img alt="Create New Dataset Form: Initial information" src="/../assets/img/wis2box-create-new-dataset-form-initial-other.png" width="450">

点击 *continue to form* 继续，您现在将看到一个与之前略有不同的数据集编辑器表单。

### 创建发现元数据

与之前一样，您需要在数据集编辑器表单中填写必填字段，包括标题、描述和本地 ID：

<img alt="Metadata Editor: title, description, keywords" src="/../assets/img/wis2box-metadata-editor-part1-other.png" width="800">

请注意，由于您选择了 Template=*other*，因此需要您自行定义 WIS2 主题层级，可以使用 'Discipline' 和 'Sub-Discipline' 的下拉列表进行选择。

在本练习中，请选择子学科主题 "prediction/analysis/medium-range/deterministic/global"：

<img alt="Metadata Editor: title, description, keywords" src="/../assets/img/wis2box-metadata-editor-part1-other-topic.png" width="800">

由于您使用了 Template=*other*，因此没有预定义的关键词。请确保添加至少 3 个您自己选择的关键词：

<img alt="Metadata Editor: title, description, keywords" src="/../assets/img/wis2box-metadata-editor-part1-other-2.png" width="800">

填写完必填字段后，继续填写表单的其余部分，包括 'Temporal Properties'、'Spatial Properties' 和 'Contact Information of the Data Provider'，并确保验证表单。

### 配置数据映射

当使用自定义模板时，不会提供默认数据映射。因此，数据集映射编辑器将为空，用户必须根据具体需求配置映射。

<img alt="Data Mappings: update plugin" src="/../assets/img/wis2box-data-mappings-other1.png" width="800">

点击 "ADD A PLUGIN +" 为数据集添加数据插件。

选择名称为 **"Universal data without conversion"** 的插件。此插件旨在发布数据而不进行任何转换。

添加此插件时，您需要指定 **File Extension** 和 **File Pattern**（由正则表达式定义），以匹配数据文件的命名模式。对于 "Universal"-插件，File Pattern 还用于确定数据的 "datetime" 属性。

!!! Note "从文件名解析日期时间"

    "Universal"-插件假设正则表达式中的第一个分组对应于数据的日期时间。

    默认的 File Pattern 是 `^.*?_(\d{8}).*?\..*$`，它匹配以下模式：下划线后跟 8 位数字，再跟随任意字符和点以及文件扩展名。例如：

    - `mydata_20250101.txt` 将匹配并提取 2025 年 1 月 25 日作为数据的日期时间属性
    - `mydata_2025010112.txt` 不会匹配，因为有 10 位数字而不是 8 位
    - `mydata-20250101.txt` 不会匹配，因为日期前是连字符而不是下划线

    在使用 "Universal"-插件导入数据时，可以将文件重命名为匹配默认模式，或者更新 File Pattern，确保正则表达式中的第一个分组对应于日期时间。

暂时保留 "File Name" 的默认值，因为它们与您将在下一个实践环节中导入的数据匹配：

<img alt="Data Mappings: update plugin" src="/../assets/img/wis2box-data-mappings-other2.png" width="800">

点击 "SAVE" 保存插件设置，并验证您现在可以在数据集映射编辑器中看到插件已列出：

<img alt="Data Mappings: update plugin" src="/../assets/img/wis2box-data-mappings-other3.png" width="800">

请注意，当您导入数据时，文件扩展名和文件名模式必须与您在此处提供的设置匹配，否则数据将无法被处理，并且 wis2box-management 容器会记录错误消息。

### 提交并检查结果

最后，提供之前创建的 'processes/wis2box' 的授权令牌，然后点击 'submit' 发布您的数据集。

成功提交后，您的新数据集将出现在 Dataset 标签中：

<img alt="Dataset Editor: new dataset" src="/../assets/img/wis2box-dataset-editor-new-dataset-other.png" width="800">

打开 MQTT Explorer，如果您已连接到代理，应该会看到另一个新的 WIS2 通知发布在主题 `origin/a/wis2/<your-centre-id>/metadata` 上。

!!! question
    
    访问 `http://YOUR-HOST` 上的 wis2box-UI，您看到列出了多少个数据集？如何查看每个数据集使用的 WIS2 主题层级以及每个数据集的描述？

??? success "点击查看答案"

    打开 `http://YOUR-HOST` 上的 wis2box UI，您应该会看到列出了 2 个数据集及其 WIS2 主题层级。要查看每个数据集的描述，您可以点击 "metadata"，这将重定向到由 wis2box-api 提供的相应 'discovery-metadata' 项目。

!!! question

    尝试更新您最后创建的数据集的描述。更新描述后，您是否看到一个新的 WIS2 通知发布在主题 `origin/a/wis2/<your-centre-id>/metadata` 上？新通知与之前的通知有什么区别？

??? success "点击查看答案"

    在更新数据集后，您应该会看到一个新的数据通知消息发布在主题 `origin/a/wis2/<your-centre-id>/metadata` 上。
    
    在消息中，*"rel": "canonical"* 的值将更改为 *"rel": "update"*，表明之前发布的数据已被修改。要查看更新后的描述，请将 URL 复制粘贴到浏览器中，您应该会看到更新后的描述。

!!! question

    尝试通过更改 "Sub-Discipline Topics" 的选择来更新您最后创建的数据集的主题层级。您是否看到一个新的 WIS2 通知发布在主题 `origin/a/wis2/<your-centre-id>/metadata` 上？

??? success "点击查看答案"

您**无法**更新现有数据集的主题层级。在数据集创建后，数据集编辑表单中的主题层级字段将被禁用。如果您想使用不同的主题层级，请先删除现有数据集，然后使用所需的主题层级创建一个新数据集。

## 结论

!!! success "恭喜！"
    在本次实践课程中，您学会了如何：

    - 使用 wis2box-webapp 数据集编辑器
    - 使用模板 *weather/surface-based-observations/synop* 和模板 *other* 创建新数据集
    - 定义您的发现元数据
    - 审核您的数据映射
    - 发布发现元数据
    - 查看发现元数据的 WIS2 通知
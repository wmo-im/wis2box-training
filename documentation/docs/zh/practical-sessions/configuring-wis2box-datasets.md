---
title: 在wis2box中配置数据集
---

# 在wis2box中配置数据集

!!! abstract "学习目标"
    完成本实践课程后，您将能够：

    - 创建新的数据集
    - 为数据集创建发现元数据
    - 为数据集配置数据映射
    - 使用WCMP2记录发布WIS2通知
    - 更新并重新发布您的数据集

## 简介

wis2box使用与发现元数据和数据映射相关联的数据集。

发现元数据用于创建WCMP2（WMO核心元数据配置2）记录，该记录通过您的wis2box-broker发布的WIS2通知进行共享。

数据映射用于将数据插件与您的输入数据关联，允许在使用WIS2通知发布数据之前对数据进行转换。

本课程将指导您创建新的数据集、创建发现元数据和配置数据映射。您将在wis2box-api中检查您的数据集并查看发现元数据的WIS2通知。

## 准备工作

使用MQTT Explorer连接到您的代理。

不要使用您的内部代理凭据，而是使用公共凭据`everyone/everyone`：

<img alt="MQTT Explorer: Connect to broker" src="/../assets/img/mqtt-explorer-wis2box-broker-everyone-everyone.png" width="800">

!!! Note

    您永远不需要与外部用户共享内部代理的凭据。'everyone'用户是一个公共用户，用于启用WIS2通知的共享。

    `everyone/everyone`凭据在主题'origin/a/wis2/#'上具有只读访问权限。这是发布WIS2通知的主题。Global Broker可以使用这些公共凭据订阅以接收通知。
    
    'everyone'用户将看不到内部主题，也无法发布消息。
    
打开浏览器并打开页面`http://YOUR-HOST/wis2box-webapp`。确保您已登录并可以访问"数据集编辑器"页面。

如果您需要回顾如何连接到代理或访问wis2box-webapp，请参阅[初始化wis2box](./initializing-wis2box.md)部分。

## 为processes/wis2box创建授权令牌

您需要'processes/wis2box'端点的授权令牌来发布您的数据集。

要创建授权令牌，通过SSH访问您的培训虚拟机，并使用以下命令登录到wis2box-management容器：

```bash
cd ~/wis2box
python3 wis2box-ctl.py login
```

然后运行以下命令为'processes/wis2box'端点创建随机生成的授权令牌：

```bash
wis2box auth add-token --path processes/wis2box
```

您也可以通过向命令提供令牌作为参数来创建具有特定值的令牌：

```bash
wis2box auth add-token --path processes/wis2box MyS3cretToken
```

确保复制令牌值并将其存储在本地机器上，因为稍后您会需要它。

获得令牌后，您可以退出wis2box-management容器：

```bash
exit
```

## 在wis2box-webapp中创建新数据集

通过访问`http://YOUR-HOST/wis2box-webapp`并从左侧菜单中选择"数据集编辑器"，导航到wis2box实例中的"数据集编辑器"页面。

在"数据集编辑器"页面的"数据集"标签下，点击"创建新..."：

<img alt="Create New Dataset" src="/../assets/img/wis2box-create-new-dataset.png" width="800">

将出现一个弹出窗口，要求您提供：

- **Centre ID**：这是WMO成员指定的机构缩写（小写且无空格），用于标识负责发布数据的数据中心。
- **Data Type**：您正在创建元数据的数据类型。您可以选择使用预定义模板或选择"其他"。如果选择"其他"，将需要手动填写更多字段。

!!! Note "Centre ID"

    您的centre-id应该以您所在国家的TLD开头，后跟破折号（`-`）和您组织的缩写名称（例如`fr-meteofrance`）。centre-id必须是小写的，并且只使用字母数字字符。下拉列表显示了当前在WIS2上注册的所有centre-id以及您已经在wis2box中创建的任何centre-id。

!!! Note "数据类型模板"

    *Data Type*字段允许您从wis2box-webapp数据集编辑器中可用的模板列表中进行选择。模板将使用适合该数据类型的建议默认值预填充表单。这包括元数据的建议标题和关键词以及预配置的数据插件。主题将固定为该数据类型的默认主题。

    出于培训目的，我们将使用*weather/surface-based-observations/synop*数据类型，该类型包括确保数据在发布前转换为BUFR格式的数据插件。

    如果您想使用wis2box发布CAP警报，请使用*weather/advisories-warnings*模板。此模板包括一个数据插件，在发布前验证输入数据是否为有效的CAP警报。要创建CAP警报并通过wis2box发布，您可以使用[CAP Composer](https://github.com/wmo-raf/cap-composer)。

请为您的组织选择适当的centre-id。

对于**Data Type**，选择**weather/surface-based-observations/synop**：

<img alt="Create New Dataset Form: Initial information" src="/../assets/img/wis2box-create-new-dataset-form-initial.png" width="450">

点击*继续填写表单*以继续，您现在将看到**数据集编辑器表单**。

由于您选择了**weather/surface-based-observations/synop**数据类型，表单将预填充一些与该数据类型相关的初始值。

## 创建发现元数据

数据集编辑器表单允许您提供数据集的发现元数据，wis2box-management容器将使用这些元数据来发布WCMP2记录。

由于您选择了'weather/surface-based-observations/synop'数据类型，表单将预填充一些默认值。

请确保将自动生成的'Local ID'替换为您数据集的描述性名称，例如'synop-dataset-wis2training'：

<img alt="Metadata Editor: title, description, keywords" src="/../assets/img/wis2box-metadata-editor-part1.png" width="800">

检查标题和关键词，根据需要更新它们，并为您的数据集提供描述。

请注意，有选项可以将'WMO数据政策'从'core'更改为'recommended'，或修改您的默认元数据标识符，请保持数据政策为'core'并使用默认元数据标识符。

接下来，检查定义'时间属性'和'空间属性'的部分。您可以通过更新'北纬'、'南纬'、'东经'和'西经'字段来调整边界框：

<img alt="Metadata Editor: temporal properties, spatial properties" src="/../assets/img/wis2box-metadata-editor-part2.png" width="800">

接下来，填写定义'数据提供者联系信息'的部分：

<img alt="Metadata Editor: contact information" src="/../assets/img/wis2box-metadata-editor-part3.png" width="800">

最后，填写定义'数据质量信息'的部分：

填写完所有部分后，点击'验证表单'并检查表单是否有错误：

<img alt="Metadata Editor: validation" src="/../assets/img/wis2box-metadata-validation-error.png" width="800">

如果有任何错误，请更正它们并再次点击'验证表单'。

确保没有错误，并且您会看到一个弹出提示，表明您的表单已通过验证：

<img alt="Metadata Editor: validation success" src="/../assets/img/wis2box-metadata-validation-success.png" width="800">

接下来，在提交数据集之前，检查数据集的数据映射。

## 配置数据映射

由于您使用模板创建数据集，数据集映射已预填充了'weather/surface-based-observations/synop'数据类型的默认插件。数据插件在wis2box中用于在使用WIS2通知发布数据之前转换数据。

<img alt="Data Mappings: update plugin" src="/../assets/img/wis2box-data-mappings.png" width="800">

请注意，您可以点击"更新"按钮来更改插件的设置，如文件扩展名和文件模式，现在您可以保留默认设置。在后面的课程中，您将了解更多关于BUFR和数据转换为BUFR格式的内容。

## 提交您的数据集

最后，您可以点击'提交'来发布您的数据集。

您需要提供之前创建的'processes/wis2box'的授权令牌。如果您还没有创建令牌，可以按照准备部分的说明创建新令牌。

提交数据集后，检查是否收到以下消息，表明数据集已成功提交：

<img alt="Submit Dataset Success" src="/../assets/img/wis2box-submit-dataset-success.png" width="400">

点击'确定'后，您将被重定向到数据集编辑器主页。现在如果您点击'数据集'标签，应该能看到您的新数据集列表：

<img alt="Dataset Editor: new dataset" src="/../assets/img/wis2box-dataset-editor-new-dataset.png" width="800">

## 查看发现元数据的WIS2通知

转到MQTT Explorer，如果您已连接到代理，应该能看到在主题`origin/a/wis2/<your-centre-id>/metadata`上发布的新WIS2通知：

<img alt="MQTT Explorer: WIS2 notification" src="/../assets/img/mqtt-explorer-wis2-notification-metadata.png" width="800">

检查您发布的WIS2通知的内容。您应该看到一个符合WIS通知消息（WNM）格式的JSON结构。

!!! question

    WIS2通知发布在什么主题上？

??? success "点击查看答案"

    WIS2通知发布在主题`origin/a/wis2/<your-centre-id>/metadata`上。

!!! question
    
    尝试在WIS2通知中找到您在发现元数据中提供的标题、描述和关键词。您能找到它们吗？

??? success "点击查看答案"

    **您在发现元数据中提供的标题、描述和关键词不在WIS2通知负载中！**
    
    相反，请尝试在WIS2通知的"links"部分中查找规范链接：

    <img alt="WIS2 notification for metadata, links sections" src="/../assets/img/wis2-notification-metadata-links.png" width="800">

    **WIS2通知包含指向已发布WCMP2记录的规范链接。**
    
    将此规范链接复制粘贴到您的浏览器中以访问WCMP2记录，根据您的浏览器设置，您可能会被提示下载文件或直接在浏览器中显示。

    您将在WCMP2记录中找到您提供的标题、描述和关键词。

## 结论

!!! success "恭喜！"
    在本实践课程中，您学会了如何：

    - 创建新的数据集
    - 定义您的发现元数据
    - 检查您的数据映射
    - 发布发现元数据
    - 查看发现元数据的WIS2通知
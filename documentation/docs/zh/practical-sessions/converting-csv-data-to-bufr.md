---
title: 将 CSV 数据转换为 BUFR
---

# 将 CSV 数据转换为 BUFR

!!! abstract "学习成果"
    在本实践课程结束时，您将能够：

    - 使用 **MinIO UI** 上传输入的 CSV 数据文件并监控结果
    - 了解与默认自动气象站 BUFR 模板一起使用的 CSV 数据格式
    - 在 **wis2box webapp** 中使用数据集编辑器创建用于发布 DAYCLI 消息的数据集
    - 了解与 DAYCLI BUFR 模板一起使用的 CSV 数据格式
    - 使用 **wis2box webapp** 验证并转换 AWS 站点的样本数据为 BUFR（可选）

## 引言

逗号分隔值（CSV）数据文件常用于以表格格式记录观测数据和其他数据。
大多数用于记录传感器输出的数据记录器能够导出观测数据到分隔文件，包括 CSV 文件。
同样，当数据被摄取到数据库中时，很容易以 CSV 格式导出所需的数据。
为了帮助交换原始存储在表格数据格式中的数据，wis2box 实现了 CSV 到 BUFR 的转换，使用的软件与 SYNOP 到 BUFR 相同。

在本课程中，您将学习在 wis2box 中使用 csv2bufr 转换器的以下内置模板：

- **AWS** (aws-template.json)：转换简化自动气象站文件中的 CSV 数据到 BUFR 序列 301150, 307096 的映射模板
- **DayCLI** (daycli-template.json)：转换日常气候 CSV 数据到 BUFR 序列 307075 的映射模板

## 准备工作

确保已使用 `python3 wis2box.py start` 启动 wis2box-stack。

确保您的浏览器已打开并通过 `http://<your-host>:9000` 访问您实例的 MinIO UI。
如果您忘记了 MinIO 凭据，可以在学生 VM 上的 `wis2box-1.0.0rc1` 目录中的 `wis2box.env` 文件中找到它们。

确保您已打开 MQTT Explorer 并使用凭据 `everyone/everyone` 连接到您的代理。

## 练习 1：使用带有 'AWS' 模板的 csv2bufr

'AWS' 模板提供了一个预定义的映射模板，用于转换 AWS 站点的 CSV 数据，以支持 GBON 报告要求。

可以在此处找到 AWS 模板的描述：

[aws-template](./../csv2bufr-templates/aws-template.md)

### 审查 aws-example 输入数据

从下面的链接下载本练习的示例：

[aws-example.csv](./../sample-data/aws-example.csv)

打开您下载的文件，并检查内容：

!!! question
    检查日期、时间和标识字段（WIGOS 和传统标识符），您注意到了什么？今天的日期应该如何表示？

??? success "点击以显示答案"
    每列包含单独的信息。例如，日期被分为年、月和日，反映了数据在 BUFR 中的存储方式。同样，时间需要分为“小时”和“分钟”，WIGOS 站点标识符需要分解为其各自的组成部分。

!!! question
    查看数据文件，缺失数据是如何编码的？

??? success "点击以显示答案"
    文件中的缺失数据由空单元格表示。在 CSV 文件中，这将被编码为 ``,,``。注意，这是一个空单元格，而不是编码为零长度字符串，例如 ``,"",``。

!!! hint "缺失数据"
    由于传感器故障或未观测到参数等各种原因，数据可能会缺失。在这些情况下，可以按照上述答案编码缺失数据，报告中的其他数据仍然有效。

!!! question
    示例文件中报告数据的站点的 WIGOS 站点标识符是什么？它在输入文件中是如何定义的？

??? success "点击以显示答案"

    WIGOS 站点标识符由文件中的 4 个单独列定义：

    - **wsi_series**：WIGOS 标识符系列
    - **wsi_issuer**：WIGOS 标识符发行者
    - **wsi_issue_number**：WIGOS 发行编号
    - **wsi_local**：WIGOS 本地标识符

    示例文件中使用的 WIGOS 站点标识符是 `0-20000-0-60351`、`0-20000-0-60355` 和 `0-20000-0-60360`。

### 更新示例文件

更新您下载的示例文件，使用今天的日期和时间，并更改 WIGOS 站点标识符以使用您在 wis2box-webapp 中注册的站点。

### 上传数据到 MinIO 并检查结果

导航到 MinIO UI 并使用 `wis2box.env` 文件中的凭据登录。

导航到 **wis2box-incoming** 并点击“创建新路径”按钮：

<img alt="显示 MinIO UI 的图像，其中突出显示了创建文件夹按钮" src="/../assets/img/minio-create-new-path.png"/>

在 MinIO 存储桶中创建一个与您使用 template='weather/surface-weather-observations/synop' 创建的数据集 id 匹配的新文件夹：

<img alt="显示 MinIO UI 的图像，其中突出显示了创建文件夹按钮" src="/../assets/img/minio-create-new-path-metadata_id.png"/>

将您下载的示例文件上传到您在 MinIO 存储桶中创建的文件夹：

<img alt="显示 MinIO UI 的图像，其中 aws-example 已上传" src="/../assets/img/minio-upload-aws-example.png"/></center>

检查 `http://<your-host>:3000` 的 Grafana 仪表板，查看是否有任何警告或错误。如果看到任何问题，请尝试修复它们并重复练习。

检查 MQTT Explorer，看是否收到 WIS2 数据通知。

如果您成功摄取了数据，您应该在主题 `origin/a/wis2/<centre-id>/data/weather/surface-weather-observations/synop` 上的 MQTT explorer 中看到 3 个站点的 3 个通知：

<img width="450" alt="在上传 AWS 后显示 MQTT explorer 的图像" src="/../assets/img/mqtt-explorer-aws-upload.png"/>

## 练习 2 - 使用 'DayCLI' 模板

在上一个练习中，我们使用了您创建的数据类型为 'weather/surface-weather-observations/synop' 的数据集，该数据集已预配置了 CSV 到 BUFR 转换模板为 AWS 模板。

在下一个练习中，我们将使用 'DayCLI' 模板将日常气候数据转换为 BUFR。

可以在此处找到 DAYCLI 模板的描述：

[daycli-template](./../csv2bufr-templates/daycli-template.md)

!!! Note "关于 DAYCLI 模板"
    请注意，DAYCLI BUFR 序列将在 2025 年更新，以包括额外的信息和修订的 QC 标志。wis2box 将更新 DAYCLI 模板以反映这些变化。WMO 将通知何时更新 wis2box 软件以包括新的 DAYCLI 模板，以便用户相应更新其系统。

### 创建用于发布 DAYCLI 消息的 wis2box 数据集

转到 wis2box-webapp 中的数据集编辑器并创建一个新数据集。使用与之前实践课程相同的中心 ID，并选择 **Data Type='climate/surface-based-observations/daily'**：

<img alt="在 wis2box-webapp 中为 DAYCLI 创建一个新数据集" src="/../assets/img/wis2box-webapp-create-dataset-daycli.png"/>

点击“继续到表单”，为您的数据集添加描述，设置边界框并提供数据集的联系信息。填写完所有部分后，点击 'VALIDATE FORM' 并检查表单。

查看数据集的数据插件。点击名称为“CSV 数据转换为 BUFR”的插件旁边的“更新”，您将看到模板设置为 **DayCLI**：

<img alt="更新数据集的数据插件以使用 DAYCLI 模板" src="/../assets/img/wis2box-webapp-update-data-plugin-daycli.png"/>

关闭插件配置并使用您在上一个实践课程中创建的认证令牌提交表单。

您现在应该在 wis2box-webapp 中有第二个配置为使用 DAYCLI 模板将 CSV 数据转换为 BUFR 的数据集。

### 审查 daycli-example 输入数据

从下面的链接下载本练习的示例：

[daycli-example.csv](./../../sample-data/daycli-example.csv)

打开您下载的文件，并检查内容：

!!! question
    daycli 模板中包含了哪些额外的变量？

??? success "点击以显示答案"
    daycli 模板包括有关仪器放置和温度及湿度测量质量分类的重要元数据、质量控制标志以及如何计算日平均温度的信息。

### 更新示例文件

示例文件包含一个月中每天的一行数据，并为一个站点报告数据。更新您下载的示例文件，使用今天的日期和时间，并更改 WIGOS 站点标识符以使用您在 wis2box-webapp 中注册的站点。

### 上传数据到 MinIO 并检查结果

与之前一样，您需要将数据上传到 MinIO 中的 'wis2box-incoming' 存储桶中，以便由 csv2bufr 转换器处理。这次您需要在 MinIO 存储桶中创建一个新文件夹，该文件夹的数据集 ID 与您使用 template='climate/surface-based-observations/daily' 创建的数据集 ID 匹配，这与您在上一个练习中使用的数据集 ID 不同：

<img alt="显示 MinIO UI 的图像，其中 DAYCLI-example 已上传" src="/../assets/img/minio-upload-daycli-example.png"/></center>

上传数据后，在 Grafana 仪表板中检查是否有任何警告或错误，并检查 MQTT Explorer，看是否收到 WIS2 数据通知。

如果您成功摄取了数据，您应该在主题 `origin/a/wis2/<centre-id>/data/climate/surface-based-observations/daily` 上的 MQTT explorer 中看到您报告的月份中 30 天的 30 个通知：

<img width="450" alt="在上传 DAYCLI 后显示 MQTT explorer 的图像" src="/../assets/img/mqtt-daycli-template-success.png"/>

## 练习 3 - 使用 wis2box-webapp 中的 CSV 表单（可选）

wis2box Web 应用程序提供了一个界面，用于上传 CSV 数据并在发布到 WIS2 之前将其转换为 BUFR，使用 AWS 模板。

使用此表单的目的是用于调试和验证，推荐的自动气象站数据发布方法是设置一个自动上传数据到 MinIO 存储桶的过程。

### 在 wis2box web 应用程序中使用 CSV 表单

导航到 wis2box web 应用程序上的 CSV 表单
(``http://<your-host-name>/wis2box-webapp/csv2bufr_form``)。
在本练习中使用文件 [aws-example.csv](../sample-data/aws-example.csv)。
您现在应该能够点击下一步以预览并验证文件。

<center><img alt="显示 CSV 到 BUFR 上传屏幕的图像" src="/../assets/img/csv2bufr-ex1.png"/></center>

点击下一步按钮将文件加载到浏览器并根据预定义的模式验证内容。
数据尚未转换或发布。在预览/验证标签页上，您应该会看到关于缺失数据的警告列表，但在本练习中这些可以忽略。

<center><img alt="显示 CSV 到 BUFR 示例验证页面的警告的图像" src="/../assets/img/csv2bufr-warnings.png"/></center>

点击 *next* 继续，您将被要求提供数据发布的数据集 ID。选择您之前创建的数据集 ID 并点击 *next*。

您现在应该在授权页面上，您将被要求输入您之前创建的 ``processes/wis2box`` 令牌。输入此令牌并点击 "Publish on WIS2" 开关以确保选择了 "Publish to WIS2"（见下面的屏幕截图）。

<center><img alt="csv2bufr 授权和发布屏幕" src="/../assets/img/csv2bufr-toggle-publish.png"/></center>

点击下一步以转换为 BUFR 并发布，您应该会看到以下屏幕：

<center><img alt="显示 CSV 到 BUFR 示例成功屏幕的图像" src="/../assets/img/csv2bufr-success.png"/></center>

点击右侧的 ``Output BUFR files`` 下的向下箭头应该会显示 ``Download`` 和 ``Inspect`` 按钮。
点击 inspect 查看数据并确认值是否符合预期。

<center><img alt="显示 CSV 到 BUFR 检查输出的图像" src="/../assets/img/csv2bufr-inspect.png"/></center>

### 调试无效输入数据

在这个练习中，我们将检查输入无效数据时会发生什么。通过点击下面的链接下载下一个示例文件。这包含与第一个文件相同的数据，但已删除空列。
检查文件并确认已删除哪些列，然后按照相同的过程将数据转换为 BUFR。

[csv2bufr-ex3a.csv](./../../sample-data/csv2bufr-ex3a.csv)

!!! question
    由于文件中缺少列，您是否能够将数据转换为 BUFR？
    您是否注意到验证页面上的警告有什么变化？

??? success "点击以显示答案"
    您应该仍然能够将数据转换为 BUFR，但警告消息将更新为完全缺少列而不是包含缺失值。

在下一个示例中，CSV 文件中添加了一个额外的列。

[csv2bufr-ex3b.csv](./../../sample-data/csv2bufr-ex3b.csv)

!!! question
    在上传或提交文件之前，您能预测会发生什么吗？

现在上传并确认您的预测是否正确。

??? success "点击以显示答案"
    当文件被验证时，您应该会收到一个警告，指出列 ``index`` 在模式中未找到，数据将被跳过。您应该能够像之前的示例一样点击并转换为 BUFR。

在这个练习的最后一个示例中，数据已被修改。检查 CSV 文件的内容。

[csv2bufr-ex3c.csv](./../../sample-data/csv2bufr-ex3c.csv)

!!! question
    文件中发生了什么变化，您认为会发生什么？

现在上传文件并确认您是否正确。

??? warning "点击以显示答案"
    输入数据中的压力字段已从 Pa 转换为 hPa。然而，CSV 到 BUFR 转换器期望与 BUFR 相同的单位（Pa），结果，这些字段由于超出范围而未通过验证。您应该能够编辑 CSV 以纠正问题，并通过返回第一个屏幕并重新上传数据来重新提交。

!!! hint
    wis2box web 应用程序可用于测试和验证自动化工作流程的样本数据。这将识别一些常见问题，例如单位不正确（hPa 与 Pa 以及 C 与 K）和缺少列。应注意 CSV 数据中的单位与上述指示的单位相匹配。

## 结论

!!! success "恭喜"
    在这个实践课程中，您已经学到了：

    - 关
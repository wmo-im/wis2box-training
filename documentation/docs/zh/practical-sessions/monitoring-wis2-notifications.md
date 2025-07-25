---
title: 监控 WIS2 通知
---

# 监控 WIS2 通知

!!! abstract "学习成果"

    通过本实践课程，您将能够：
    
    - 通过使用 `wis2box data ingest` 命令在 MinIO 中上传数据来触发 wis2box 工作流
    - 查看 Grafana 仪表板中显示的警告和错误
    - 检查正在发布的数据内容

## 引言

**Grafana 仪表板** 使用来自 Prometheus 和 Loki 的数据来显示您的 wis2box 的状态。Prometheus 存储从收集的指标中获得的时间序列数据，而 Loki 存储在您的 wis2box 实例上运行的容器的日志。这些数据允许您检查 MinIO 上接收到的数据量、发布了多少 WIS2 通知，以及日志中是否检测到任何错误。

要查看在您的 wis2box 的不同主题上发布的 WIS2 通知的内容，您可以使用 **wis2box-webapp** 中的 'Monitor' 标签。

## 准备

本节将使用之前在 [配置 wis2box 数据集](/practical-sessions/configuring-wis2box-datasets) 实践课程中创建的 "surface-based-observations/synop" 数据集。

使用 SSH 客户端（PuTTY 或其他）登录到您的学生 VM。

确保 wis2box 正在运行：

```bash
cd ~/wis2box-1.0.0rc1/
python3 wis2box-ctl.py start
python3 wis2box-ctl.py status
```

确保您的 MQTT Explorer 正在运行并使用公共凭据 `everyone/everyone` 连接到您的实例，并订阅主题 `origin/a/wis2/#`。

确保您可以通过访问 `http://<your-host>:9000` 并登录（使用您的 `wis2box.env` 文件中的 `WIS2BOX_STORAGE_USERNAME` 和 `WIS2BOX_STORAGE_PASSWORD`）来访问 MinIO 网页界面。

确保您的网页浏览器已打开并显示您实例的 Grafana 仪表板，通过访问 `http://<your-host>:3000`。

## 导入一些数据

请从您的 SSH 客户端会话执行以下命令：

将样本数据文件 `aws-example.csv` 复制到您在 `wis2box.env` 文件中定义的 `WI2BOX_HOST_DATADIR` 目录中。

```bash
cp ~/exercise-materials/monitoring-exercises/aws-example.csv ~/wis2box-data/
```

确保您位于 `wis2box-1.0.0rc1` 目录中并登录到 **wis2box-management** 容器：

```bash
cd ~/wis2box-1.0.0rc1
python3 wis2box-ctl.py login
```

验证样本数据是否可在 **wis2box-management** 容器内的 `/data/wis2box/` 目录中找到：

```bash
ls -lh /data/wis2box/aws-example.csv
```

!!! note
    `WIS2BOX_HOST_DATADIR` 在 `wis2box-management` 容器中被挂载为 `/data/wis2box/`，通过 `wis2box-1.0.0rc1` 目录中包含的 `docker-compose.yml` 文件。
    
    这允许您在主机和容器之间共享数据。

!!! question "练习 1: 使用 `wis2box data ingest` 导入数据"

    执行以下命令将样本数据文件 `aws-example.csv` 导入到您的 wis2box 实例：

    ```bash
    wis2box data ingest -p /data/wis2box/aws-example.csv --metadata-id urn:wmo:md:not-my-centre:core.surface-based-observations.synop
    ```

    数据是否成功导入？如果没有，错误消息是什么，您应该如何解决？

??? success "点击查看答案"

    您将看到以下输出：

    ```bash
    Error: metadata_id=urn:wmo:md:not-my-centre:core.surface-based-observations.synop not found in data mappings
    ```

    错误消息表明您提供的元数据标识符与您的 wis2box 实例中配置的任何数据集都不匹配。

    提供与您在上一个实践课程中创建的数据集匹配的正确元数据标识符，并重复数据导入命令，直到您看到以下输出：

    ```bash 
    Processing /data/wis2box/aws-example.csv
    Done
    ```

转到您的浏览器中的 MinIO 控制台并检查 `aws-example.csv` 文件是否已上传到 `wis2box-incoming` 存储桶。您应该看到一个以您在 `--metadata-id` 选项中提供的数据集名称命名的新目录：

<img alt="minio-wis2box-incoming-dataset-folder" src="/../assets/img/minio-wis2box-incoming-dataset-folder.png" width="800">

!!! note
    `wis2box data ingest` 命令将文件上传到 MinIO 中名为您提供的元数据标识符的 `wis2box-incoming` 存储桶中的目录。

转到您的浏览器中的 Grafana 仪表板并检查数据导入的状态。

!!! question "练习 2: 检查数据导入的状态"
    
    转到您的浏览器中的 Grafana 仪表板并检查数据导入的状态。
    
    数据是否成功导入？

??? success "点击查看答案"
    Grafana 主页仪表板底部的面板报告以下警告：    
    
    `WARNING - input=aws-example.csv warning=Station 0-20000-0-60355 not in station list; skipping`
    `WARNING - input=aws-example.csv warning=Station 0-20000-0-60360 not in station list; skipping`

    此警告表明这些站点未在您的 wis2box 的站点列表中定义。在您将其添加到站点列表并将其与您的数据集的主题关联之前，不会为此站点发布任何 WIS2 通知。

!!! question "练习 3: 添加测试站点并重复数据导入"

    使用 **wis2box-webapp** 中的站点编辑器添加站点到您的 wis2box，并将站点与您的数据集的主题关联。

    现在重新上传样本数据文件 `aws-example.csv` 到您在上一个练习中使用的 MinIO 中的相同路径。

    检查 Grafana 仪表板，有没有新的错误或警告？您如何知道测试数据已成功导入并发布？

??? success "点击查看答案"

    您可以检查 Grafana 主页仪表板上的图表，看看测试数据是否已成功导入并发布。
    
    如果成功，您应该看到以下内容：

    <img alt="grafana_success" src="/../assets/img/grafana_success.png" width="800">

!!! question "练习 4: 检查 MQTT 代理以获取 WIS2 通知"
    
    转到 MQTT Explorer 并检查您是否可以看到您刚刚导入的数据的 WIS2 通知消息。
    
    您的 wis2box 发布了多少条 WIS2 数据通知？
    
    您如何访问正在发布的数据内容？

??? success "点击查看答案"

    您应该看到您的 wis2box 发布了 6 条 WIS2 数据通知。

    要访问正在发布的数据内容，您可以展开主题结构以查看消息的不同级别，直到您到达最后一级并查看其中一条消息的消息内容。

    消息内容中有一个 "links" 部分，其中包含 "rel" 键为 "canonical" 和 "href" 键，带有下载数据的 URL。URL 的格式为 `http://<your-host>/data/...`。
    
    请注意，数据格式为 BUFR，您将需要一个 BUFR 解析器来查看数据内容。BUFR 格式是气象服务用来交换数据的二进制格式。wis2box 内的数据插件在发布之前将数据从 CSV 转换为 BUFR。

## 查看您已发布的数据内容

您可以使用 **wis2box-webapp** 查看您的 wis2box 发布的 WIS2 数据通知的内容。

通过在浏览器中导航到 `http://<your-host>/wis2box-webapp` 并选择 **Monitoring** 标签来打开 **wis2box-webapp**：

<img alt="wis2box-webapp-monitor" src="/../assets/img/wis2box-webapp-monitor.png" width="220">

在监控标签中选择您的数据集 ID 并点击 "UPDATE"

??? question "练习 5: 在 wis2box-webapp 中查看 WIS2 通知"
    
    您的 wis2box 发布了多少条 WIS2 数据通知？

    在 WIGOS 标识符为 0-20000-0-60355 的站点中，最后一条通知中报告的气温是多少？

??? success "点击查看答案"

    如果您已成功导入测试数据，您应该看到您的 wis2box 发布了 6 条 WIS2 数据通知。

    要查看 WIGOS 标识符为 0-20000-0-60355 的站点测量的气温，请点击该站点文件旁边的 "INSPECT" 按钮，打开一个弹出窗口显示数据文件的解析内容。此站点测量的气温为 25.0 摄氏度。

!!! Note
    wis2box-api 容器包括解析 BUFR 文件并以人类可读格式显示内容的工具。这不是 WIS2.0 实施的核心要求，但已包含在 wis2box 中，以帮助数据发布者检查他们正在发布的数据内容。

## 结论

!!! success "恭喜！"
    在本实践课程中，您学会了如何：

    - 通过在 MinIO 中上传数据使用 `wis2box data ingest` 命令触发 wis2box 工作流
    - 在 Grafana 仪表板和 MQTT Explorer 中查看您的 wis2box 发布的 WIS2 通知
    - 使用 **wis2box-webapp** 检查正在发布的数据内容
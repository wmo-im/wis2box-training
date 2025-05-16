---
title: 发布数据的摄入
---

# 发布数据的摄入

!!! abstract "学习成果"

    在本实践课程结束时，您将能够：
    
    - 使用命令行、MinIO网页界面、SFTP或Python脚本上传数据到MinIO，触发wis2box工作流。
    - 访问Grafana仪表板以监控数据摄入状态并查看您的wis2box实例的日志。
    - 使用MQTT Explorer查看您的wis2box发布的WIS2数据通知。

## 引言

在WIS2中，数据通过包含“规范”链接的WIS2数据通知实时共享，从该链接可以下载数据。

要在WIS2 Node中使用wis2box软件触发数据工作流，必须将数据上传到**MinIO**中的**wis2box-incoming**桶，这将启动wis2box工作流。此过程将通过WIS2数据通知发布数据。根据您的wis2box实例中配置的数据映射，数据可能在发布前转换为BUFR格式。

在本练习中，我们将使用示例数据文件触发wis2box工作流并**发布WIS2数据通知**，用于您在上一个实践课程中配置的数据集。

在练习过程中，我们将使用**Grafana仪表板**和**MQTT Explorer**监控数据摄入的状态。Grafana仪表板使用来自Prometheus和Loki的数据显示您的wis2box的状态，而MQTT Explorer允许您查看您的wis2box实例发布的WIS2数据通知。

请注意，wis2box将在发布到MQTT代理之前将示例数据转换为BUFR格式，这是根据您的数据集中预配置的数据映射进行的。对于本练习，我们将重点关注上传数据到您的wis2box实例的不同方法，并验证成功的摄入和发布。数据转换将在[数据转换工具](./data-conversion-tools)实践课程中后续讨论。

## 准备

本节使用在[配置wis2box数据集](/practical-sessions/configuring-wis2box-datasets)实践课程中之前创建的“地面观测/synop”数据集。它还需要配置**wis2box-webapp**中的站点的知识，如[配置站点元数据](/practical-sessions/configuring-station-metadata)实践课程中所述。

确保您可以使用SSH客户端（例如PuTTY）登录到您的学生VM。

确保wis2box正在运行：

```bash
cd ~/wis2box/
python3 wis2box-ctl.py start
python3 wis2box-ctl.py status
```

确保MQTT Explorer正在运行并使用公共凭据`everyone/everyone`连接到您的实例，订阅主题`origin/a/wis2/#`。

确保您的浏览器已打开并导航到`http://YOUR-HOST:3000`，以访问您实例的Grafana仪表板。

### 准备示例数据

将目录`exercise-materials/data-ingest-exercises`复制到您在`wis2box.env`文件中定义为`WIS2BOX_HOST_DATADIR`的目录：

```bash
cp -r ~/exercise-materials/data-ingest-exercises ~/wis2box-data/
```

!!! note
    `WIS2BOX_HOST_DATADIR`通过`wis2box`目录中包含的`docker-compose.yml`文件挂载为wis2box-management容器内的`/data/wis2box/`。
    
    这允许您在主机和容器之间共享数据。

### 添加测试站点

使用wis2box-webapp中的站点编辑器添加WIGOS标识符为`0-20000-0-64400`的站点到您的wis2box实例。

从OSCAR检索站点：

<img alt="oscar-station" src="/../assets/img/webapp-test-station-oscar-search.png" width="600">

将站点添加到您为“../surface-based-observations/synop”发布创建的数据集中，并使用您的认证令牌保存更改：

<img alt="webapp-test-station" src="/../assets/img/webapp-test-station-save.png" width="800">

请注意，您可以在实践课程后从您的数据集中删除此站点。

## 从命令行测试数据摄入

在本练习中，我们将使用`wis2box data ingest`命令将数据上传到MinIO。

确保您位于`wis2box`目录并登录到**wis2box-management**容器：

```bash
cd ~/wis2box
python3 wis2box-ctl.py login
```

验证以下示例数据是否在**wis2box-management**容器内的`/data/wis2box/`目录中可用：

```bash
ls -lh /data/wis2box/data-ingest-exercises/synop_202412030900.txt
```

!!! question "使用`wis2box data ingest`摄入数据"

    执行以下命令将示例数据文件摄入到您的wis2box实例：

    ```bash
    wis2box data ingest -p /data/wis2box/data-ingest-exercises/synop_202412030900.txt --metadata-id urn:wmo:md:not-my-centre:synop-test
    ```

    数据是否成功摄入？如果没有，错误消息是什么，您应该如何解决？

??? success "点击以显示答案"

    数据**未**成功摄入。您应该看到以下内容：

    ```bash
    Error: metadata_id=urn:wmo:md:not-my-centre:synop-test not found in data mappings
    ```

    错误消息表明您提供的元数据标识符与您在wis2box实例中配置的任何数据集都不匹配。

    提供与您在上一个实践课程中创建的数据集匹配的正确元数据ID，并重复数据摄入命令，直到您看到以下输出：

    ```bash 
    Processing /data/wis2box/data-ingest-exercises/synop_202412030900.txt
    Done
    ```

转到您的浏览器中的MinIO控制台，检查文件`synop_202412030900.txt`是否已上传到`wis2box-incoming`桶。您应该看到一个以您在`--metadata-id`选项中提供的数据集名称命名的新目录，在这个目录中，您将找到文件`synop_202412030900.txt`：

<img alt="minio-wis2box-incoming-dataset-folder" src="/../assets/img/minio-data-ingest-test-data.png" width="800">

!!! note
    `wis2box data ingest`命令将文件上传到MinIO中名为您提供的元数据标识符的`wis2box-incoming`桶中的目录。

转到您的浏览器中的Grafana仪表板，检查数据摄入的状态。

!!! question "在Grafana上检查数据摄入的状态"
    
    在浏览器中转到**http://your-host:3000**的Grafana仪表板，检查数据摄入的状态。
    
    您如何知道数据是否成功摄入并发布？

??? success "点击以显示答案"
    
    如果您成功摄入数据，您应该看到以下内容：
    
    <img alt="grafana_data_ingest" src="/../assets/img/grafana_data-ingest-test.png" width="400">  
    
    如果您没有看到这个，请检查仪表板底部显示的WARNING或ERROR消息，并尝试解决它们。

!!! question "检查MQTT代理以获取WIS2通知"
    
    转到MQTT Explorer并检查您是否可以看到您刚刚摄入的数据的WIS2通知消息。
    
    您的wis2box发布了多少个WIS2数据通知？
    
    您如何访问正在发布的数据内容？

??? success "点击以显示答案"

    您应该看到您的wis2box发布了1个WIS2数据通知。

    要访问正在发布的数据内容，您可以展开主题结构以查看消息的不同级别，直到您到达最后一级并查看消息内容。

    消息内容中有一个“links”部分，其中包含一个“rel”键为“canonical”和一个“href”键，带有下载数据的URL。URL的格式为`http://YOUR-HOST/data/...`。
    
    请注意，数据格式为BUFR，您将需要一个BUFR解析器来查看数据内容。BUFR格式是气象服务用来交换数据的二进制格式。wis2box内的数据插件在发布前将数据转换为BUFR。

完成此练习后，退出**wis2box-management**容器：

```bash
exit
```

## 使用MinIO网页界面上传数据

在之前的练习中，您使用`wis2box data ingest`命令将wis2box主机上的数据上传到MinIO。

接下来，我们将使用 MinIO 网页界面，该界面允许您使用网页浏览器下载和上传数据到 MinIO。

!!! question "使用 MinIO 网页界面重新上传数据"

    在浏览器中打开 MinIO 网页界面，浏览到 `wis2box-incoming` 存储桶。您将看到您在之前的练习中上传的文件 `synop_202412030900.txt`。

    点击该文件，您将有下载它的选项：

    <img alt="minio-wis2box-incoming-dataset-folder" src="/../assets/img/minio-download.png" width="800">

    您可以下载此文件并重新上传到 MinIO 中相同的路径，以重新触发 wis2box 工作流。

    检查 Grafana 仪表板和 MQTT Explorer，看看数据是否成功摄取和发布。

??? success "点击以显示答案"

    您将看到一条消息，表明 wis2box 已经发布了这些数据：

    ```bash
    ERROR - Data already published for WIGOS_0-20000-0-64400_20241203T090000-bufr4; not publishing
    ``` 
    
    这表明数据工作流被触发，但数据没有被重新发布。wis2box 不会发布相同的数据两次。
    
!!! question "使用 MinIO 网页界面上传新数据"
    
    下载此示例文件 [synop_202502040900.txt](../sample-data/synop_202502040900.txt)（右键点击并选择“另存为”下载文件）。
    
    使用网页界面上传您下载的文件到 MinIO 中与之前文件相同的路径。

    数据是否成功摄取和发布？

??? success "点击以显示答案"

    前往 Grafana 仪表板，检查数据是否成功摄取和发布。

    如果您使用错误的路径，您将在日志中看到错误消息。

    如果您使用正确的路径，您将看到为测试站点 `0-20000-0-64400` 发布了一条更多的 WIS2 数据通知，表明数据已成功摄取和发布。

    <img alt="grafana_data_ingest" src="/../assets/img/grafana_data-ingest-test2.png" width="400"> 

## 使用 SFTP 上传数据

wis2box 中的 MinIO 服务也可以通过 SFTP 访问。MinIO 的 SFTP 服务器绑定在主机的 8022 端口上（端口 22 用于 SSH）。

在这个练习中，我们将演示如何使用 WinSCP 通过 SFTP 将数据上传到 MinIO。

您可以按照此屏幕截图设置新的 WinSCP 连接：

<img alt="winscp-sftp-connection" src="/../assets/img/winscp-sftp-login.png" width="400">

SFTP 连接的凭据由 `WIS2BOX_STORAGE_USERNAME` 和 `WIS2BOX_STORAGE_PASSWORD` 在您的 `wis2box.env` 文件中定义，并且与您用于连接 MinIO UI 的凭据相同。

登录后，您将看到 wis2box 在 MinIO 中使用的存储桶：

<img alt="winscp-sftp-bucket" src="/../assets/img/winscp-buckets.png" width="600">

您可以导航到 `wis2box-incoming` 存储桶，然后到您数据集的文件夹。您将看到您在之前的练习中上传的文件：

<img alt="winscp-sftp-incoming-path" src="/../assets/img/winscp-incoming-data-path.png" width="600">

!!! question "使用 SFTP 上传数据"

    将此示例文件下载到您的本地计算机：

    [synop_202503030900.txt](./../../sample-data/synop_202503030900.txt)（右键点击并选择“另存为”下载文件）。

    然后使用您在 WinSCP 中的 SFTP 会话将其上传到 MinIO 中的 incoming 数据集路径。

    检查 Grafana 仪表板和 MQTT Explorer，看看数据是否成功摄取和发布。

??? success "点击以显示答案"

    您应该看到为测试站点 `0-20000-0-64400` 发布了一条新的 WIS2 数据通知，表明数据已成功摄取和发布。

    <img alt="grafana_data_ingest" src="/../assets/img/grafana_data-ingest-test3.png" width="400"> 

    如果您使用错误的路径，您将在日志中看到错误消息。

## 使用 Python 脚本上传数据

在这个练习中，我们将使用 MinIO 的 Python 客户端将数据复制到 MinIO。

MinIO 提供了一个 Python 客户端，可以按照以下方式安装：

```bash
pip3 install minio
```

在您的学生 VM 上，Python 的 'minio' 包已经安装好了。

在 `exercise-materials/data-ingest-exercises` 目录中，您将找到一个示例脚本 `copy_file_to_incoming.py`，可以用来将文件复制到 MinIO。

尝试运行脚本将示例数据文件 `synop_202501030900.txt` 复制到 MinIO 中的 `wis2box-incoming` 存储桶，如下所示：

```bash
cd ~/wis2box-data/data-ingest-exercises
python3 copy_file_to_incoming.py synop_202501030900.txt
```

!!! note

    您将收到一个错误，因为脚本尚未配置为访问您的 wis2box 上的 MinIO 端点。

脚本需要知道正确的端点以在您的 wis2box 上访问 MinIO。如果 wis2box 在您的主机上运行，MinIO 端点可在 `http://YOUR-HOST:9000` 访问。脚本还需要更新您的存储密码和 MinIO 存储桶中存储数据的路径。

!!! question "更新脚本并摄取 CSV 数据"
    
    编辑脚本 `copy_file_to_incoming.py` 以解决错误，使用以下方法之一：
    - 从命令行：使用 `nano` 或 `vim` 文本编辑器编辑脚本。
    - 使用 WinSCP：使用与您的 SSH 客户端相同的凭据启动一个新连接，使用文件协议 `SCP`。导航到目录 `wis2box-data/data-ingest-exercises` 并使用内置文本编辑器编辑 `copy_file_to_incoming.py`。
    
    确保您：

    - 定义了您主机的正确 MinIO 端点。
    - 提供了您 MinIO 实例的正确存储密码。
    - 提供了 MinIO 存储桶中存储数据的正确路径。

    重新运行脚本将示例数据文件 `synop_202501030900.txt` 摄取到 MinIO：

    ```bash
    python3 ~/wis2box-data/ ~/wis2box-data/synop_202501030900.txt
    ```

    确保错误已解决。

一旦您成功运行脚本，您将看到一条消息表明文件已复制到 MinIO，您应该在 MQTT Explorer 中看到您的 wis2box 实例发布的数据通知。

您还可以检查 Grafana 仪表板，看看数据是否成功摄取和发布。

现在脚本工作正常，您可以尝试使用相同的脚本将其他文件复制到 MinIO。

!!! question "摄取 BUFR 格式的二进制数据"

    运行以下命令将二进制数据文件 `bufr-example.bin` 复制到 MinIO 中的 `wis2box-incoming` 存储桶：

    ```bash
    python3 copy_file_to_incoming.py bufr-example.bin
    ```

检查 Grafana 仪表板和 MQTT Explorer，看看测试数据是否成功摄取和发布。如果您看到任何错误，请尝试解决它们。

!!! question "验证数据摄取"

    这个数据样本发布到 MQTT 代理的消息有多少条？

??? success "点击以显示答案"

    您将在 Grafana 中看到错误报告，因为 BUFR 文件中的站点未在您的 wis2box 实例的站点列表中定义。
    
    如果 BUFR 文件中使用的所有站点都在您的 wis2box 实例中定义，您应该看到 10 条消息发布到 MQTT 代理。每个通知对应于一个站点的一次观测时间戳的数据。

    插件 `wis2box.data.bufr4.ObservationDataBUFR` 将 BUFR 文件分割为单个 BUFR 消息，并为每个站点和观测时间戳发布一条消息。

## 结论

!!! success "恭喜！"
    在这个实践课程中，您学习了如何：

    - 通过使用各种方法将数据上传到 MinIO 来触发 wis2box 工作流。
    - 使用 Grafana 仪表板和您的 wis2box 实例的日志调试数据摄取过程中的常见错误。
    - 监控您的 wis2box 在 Grafana 仪表板和 MQTT Explorer 中发布的 WIS2 数据通知。
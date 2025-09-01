---
title: 使用 wis2downloader 从 WIS2 下载数据
---

# 使用 wis2downloader 从 WIS2 下载数据

!!! abstract "学习目标！"

    在本次实践课程结束时，您将能够：

    - 使用 "wis2downloader" 订阅 WIS2 数据通知并将数据下载到本地系统
    - 在 Grafana 仪表板中查看下载状态
    - 学习如何配置 wis2downloader 以订阅非默认的 Broker

## 介绍

在本次课程中，您将学习如何设置对 WIS2 Broker 的订阅，并使用 wis2box 中包含的 "wis2downloader" 服务自动将数据下载到本地系统。

!!! note "关于 wis2downloader"
     
     wis2downloader 也可以作为独立服务运行，可以在发布 WIS2 通知的系统之外运行。有关将 wis2downloader 作为独立服务使用的更多信息，请参阅 [wis2downloader](https://pypi.org/project/wis2downloader/)。

     如果您希望开发自己的服务来订阅 WIS2 通知并下载数据，可以参考 [wis2downloader 源代码](https://github.com/World-Meteorological-Organization/wis2downloader)。

## 准备工作

在开始之前，请登录到您的学生虚拟机，并确保您的 wis2box 实例已启动并运行。

## wis2downloader 基础知识

wis2downloader 作为 wis2box-stack 中的一个独立容器包含在 docker compose 文件中定义的堆栈中。wis2box-stack 中的 prometheus 容器被配置为从 wis2downloader 容器中抓取指标，这些指标可以通过 Grafana 仪表板进行可视化。

### 在 Grafana 中查看 wis2downloader 仪表板

打开一个网页浏览器，导航到您的 wis2box 实例的 Grafana 仪表板，网址为 `http://YOUR-HOST:3000`。

点击左侧菜单中的仪表板，然后选择 **wis2downloader 仪表板**。

您应该会看到以下仪表板：

![wis2downloader 仪表板](../assets/img/wis2downloader-dashboard.png)

此仪表板基于 wis2downloader 服务发布的指标，显示当前正在进行的下载状态。

在左上角，您可以看到当前活动的订阅。

保持此仪表板打开，您将在下一个练习中使用它来监控下载进度。

### 查看 wis2downloader 配置

wis2box-stack 中的 wis2downloader 服务可以通过定义在 wis2box.env 文件中的环境变量进行配置。

以下是 wis2downloader 使用的环境变量：

- DOWNLOAD_BROKER_HOST: 要连接的 MQTT Broker 的主机名。默认为 globalbroker.meteo.fr
- DOWNLOAD_BROKER_PORT: 要连接的 MQTT Broker 的端口。默认为 443（用于 websockets 的 HTTPS）
- DOWNLOAD_BROKER_USERNAME: 连接 MQTT Broker 时使用的用户名。默认为 everyone
- DOWNLOAD_BROKER_PASSWORD: 连接 MQTT Broker 时使用的密码。默认为 everyone
- DOWNLOAD_BROKER_TRANSPORT: websockets 或 tcp，用于连接 MQTT Broker 的传输机制。默认为 websockets
- DOWNLOAD_RETENTION_PERIOD_HOURS: 下载数据的保留时间（小时）。默认为 24
- DOWNLOAD_WORKERS: 使用的下载工作线程数。默认为 8，决定并行下载的数量。
- DOWNLOAD_MIN_FREE_SPACE_GB: 保留在存储下载的卷上的最小空闲空间（GB）。默认为 1。

要查看当前的 wis2downloader 配置，可以使用以下命令：

```bash
cat ~/wis2box/wis2box.env | grep DOWNLOAD
```

!!! question "查看 wis2downloader 配置"
    
    wis2downloader 默认连接的 MQTT Broker 是什么？

    下载数据的默认保留时间是多少？

??? success "点击查看答案"

    wis2downloader 默认连接的 MQTT Broker 是 `globalbroker.meteo.fr`。

    下载数据的默认保留时间是 24 小时。

!!! note "更新 wis2downloader 配置"

    要更新 wis2downloader 的配置，您可以编辑 wis2box.env 文件。要应用更改，可以重新运行 wis2box-stack 的启动命令：

    ```bash
    python3 wis2box-ctl.py start
    ```

    您将看到 wis2downloader 服务以新配置重新启动。

您可以在下一个练习中保持默认配置。

### wis2downloader 命令行界面

要访问 wis2box-stack 中 wis2downloader 的命令行界面，您可以使用以下命令登录到 **wis2downloader** 容器：

```bash
python3 wis2box-ctl.py login wis2downloader
```

使用以下命令列出当前活动的订阅：

```bash
wis2downloader list-subscriptions
```

此命令返回一个空列表，因为尚未设置任何订阅。

## 使用 WIS2 Global Broker 下载 GTS 数据

如果您保持 wis2downloader 的默认配置，它当前连接到由 Météo-France 托管的 WIS2 Global Broker。

### 设置订阅

使用以下命令 `cache/a/wis2/de-dwd-gts-to-wis2/#` 订阅由 DWD 托管的 GTS-to-WIS2 网关通过 Global Caches 发布的数据：

```bash
wis2downloader add-subscription --topic cache/a/wis2/de-dwd-gts-to-wis2/#
```

然后通过输入 `exit` 退出 **wis2downloader** 容器：

```bash
exit
```

### 检查下载的数据

检查 Grafana 中的 wis2downloader 仪表板，查看新添加的订阅。等待几分钟，您应该会看到开始下载的第一批数据。确认下载开始后，进入下一个练习。

wis2box-stack 中的 wis2downloader 服务将数据下载到您在 wis2box.env 文件中定义的 WIS2BOX_HOST_DATADIR 目录中的 'downloads' 目录。要查看 downloads 目录的内容，可以使用以下命令：

```bash
ls -R ~/wis2box-data/downloads
```

请注意，下载的数据存储在以 WIS2 通知发布的主题命名的目录中。

!!! question "查看下载的数据"

    您在 downloads 目录中看到了哪些目录？

    您能在这些目录中看到任何下载的文件吗？

??? success "点击查看答案"
    您应该会看到一个目录结构，以 `cache/a/wis2/de-dwd-gts-to-wis2/` 开头，在其下方会有更多以下载数据的 GTS 公报头命名的目录。

    根据您开始订阅的时间，您可能会或可能不会在此目录中看到任何下载的文件。如果您尚未看到任何文件，请再等待几分钟并再次检查。

在进入下一个练习之前，让我们清理订阅和下载的数据。

重新登录到 wis2downloader 容器：

```bash
python3 wis2box-ctl.py login wis2downloader
```

并使用以下命令从 wis2downloader 中删除您创建的订阅：

```bash
wis2downloader remove-subscription --topic cache/a/wis2/de-dwd-gts-to-wis2/#
```

使用以下命令删除下载的数据：

```bash
rm -rf /wis2box-data/downloads/cache/*
```

然后通过输入 `exit` 退出 wis2downloader 容器：
    
```bash
exit
```

检查 Grafana 中的 wis2downloader 仪表板，查看订阅是否已删除。您应该会看到下载停止。

!!! note "关于 GTS-to-WIS2 网关"
    当前有两个 GTS-to-WIS2 网关通过 WIS2 Global Broker 和 Global Caches 发布数据：

    - DWD（德国）：centre-id=*de-dwd-gts-to-wis2*
    - JMA（日本）：centre-id=*jp-jma-gts-to-wis2*
    
    如果在上一个练习中将 `de-dwd-gts-to-wis2` 替换为 `jp-jma-gts-to-wis2`，您将收到由 JMA GTS-to-WIS2 网关发布的通知和数据。

!!! note "origin 与 cache 主题"

    当您订阅以 `origin/` 开头的主题时，您将收到带有指向由 WIS Centre 提供的数据服务器的规范 URL 的通知。

    当您订阅以 `cache/` 开头的主题时，您将为同一数据接收到多个通知，每个 Global Cache 都会发送一个通知。每个通知都包含指向相应 Global Cache 数据服务器的规范 URL。wis2downloader 将从它能够访问的第一个规范 URL 下载数据。

## 从 WIS2 Training Broker 下载示例数据

在本练习中，您将订阅发布示例数据用于培训目的的 WIS2 Training Broker。

### 更改 wis2downloader 配置

此示例演示了如何订阅一个非默认的代理，并下载由 WIS2 Training Broker 发布的一些数据。

编辑 `wis2box.env` 文件，将 `DOWNLOAD_BROKER_HOST` 修改为 `wis2training-broker.wis2dev.io`，将 `DOWNLOAD_BROKER_PORT` 修改为 `1883`，并将 `DOWNLOAD_BROKER_TRANSPORT` 修改为 `tcp`：

```copy
# downloader settings
DOWNLOAD_BROKER_HOST=wis2training-broker.wis2dev.io
DOWNLOAD_BROKER_PORT=1883
DOWNLOAD_BROKER_USERNAME=everyone
DOWNLOAD_BROKER_PASSWORD=everyone
# download transport mechanism (tcp or websockets)
DOWNLOAD_BROKER_TRANSPORT=tcp
```

然后再次运行 `start` 命令以应用更改：

```bash
python3 wis2box-ctl.py start
```

检查 `wis2downloader` 的日志，查看是否成功连接到新的代理：

```bash
docker logs wis2downloader
```

你应该会看到以下日志信息：

```copy
...
INFO - Connecting...
INFO - Host: wis2training-broker.wis2dev.io, port: 1883
INFO - Connected successfully
```

### 设置新的订阅

现在我们将设置一个新的订阅，订阅从 WIS2 Training Broker 下载的气旋轨迹数据。

登录到 **wis2downloader** 容器：

```bash
python3 wis2box-ctl.py login wis2downloader
```

然后执行以下命令（复制粘贴以避免输入错误）：

```bash
wis2downloader add-subscription --topic origin/a/wis2/int-wis2-training/data/core/weather/prediction/forecast/medium-range/probabilistic/trajectory
```

通过输入 `exit` 退出 **wis2downloader** 容器。

### 检查下载的数据

等待直到在 Grafana 的 `wis2downloader` 仪表板中看到下载开始。

再次检查 `wis2downloader` 的日志，确认数据是否已下载：

```bash
docker logs wis2downloader
```

你应该会看到类似以下的日志信息：

```copy
[...] INFO - Message received under topic origin/a/wis2/int-wis2-training/data/core/weather/prediction/forecast/medium-range/probabilistic/trajectory
[...] INFO - Downloaded A_JSXX05ECEP020000_C_ECMP_...
```

再次检查下载目录的内容：

```bash
ls -R ~/wis2box-data/downloads
```

你应该会看到一个名为 `origin/a/wis2/int-wis2-training/data/core/weather/prediction/forecast/medium-range/probabilistic/trajectory` 的新目录，其中包含下载的数据。

!!! question "检查下载的数据"
    
    下载的数据是什么文件格式？

??? success "点击查看答案"

    下载的数据是 BUFR 格式，文件扩展名为 `.bufr`。

接下来，尝试添加另外两个订阅，分别下载月度地表温度异常数据和全球集合预报数据，订阅以下主题：
- `origin/a/wis2/int-wis2-training/data/core/weather/prediction/forecast/medium-range/probabilistic/global`
- `origin/a/wis2/int-wis2-training/data/core/climate/experimental/anomalies/monthly/surface-temperature`

等待直到在 Grafana 的 `wis2downloader` 仪表板中看到下载开始。

再次检查下载目录的内容：

```bash
ls -R ~/wis2box-data/downloads
```

你应该会看到两个新目录，分别为 `origin/a/wis2/int-wis2-training/data/core/weather/prediction/forecast/medium-range/probabilistic/global` 和 `origin/a/wis2/int-wis2-training/data/core/climate/experimental/anomalies/monthly/surface-temperature`，其中包含下载的数据。

!!! question "检查两个新主题的下载数据"
    
    `../prediction/forecast/medium-range/probabilistic/global` 主题的下载数据是什么文件格式？

    `../climate/experimental/anomalies/monthly/surface-temperature` 主题的下载数据是什么文件格式？

??? success "点击查看答案"

    `../prediction/forecast/medium-range/probabilistic/global` 主题的下载数据是 GRIB2 格式，文件扩展名为 `.grib2`。

    `../climate/experimental/anomalies/monthly/surface-temperature` 主题的下载数据是 NetCDF 格式，文件扩展名为 `.nc`。

## 结论

!!! success "恭喜！"

    在本次实践中，你学会了：

    - 使用 `wis2downloader` 订阅 WIS2 Broker 并将数据下载到本地系统
    - 在 Grafana 仪表板中查看下载状态
    - 如何更改 `wis2downloader` 的默认配置以订阅不同的代理
    - 如何在本地系统上查看下载的数据
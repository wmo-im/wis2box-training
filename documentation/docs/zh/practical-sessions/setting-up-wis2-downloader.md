---
title: 在学生虚拟机上设置 WIS2 Downloader
---

# 在学生虚拟机上设置 WIS2 Downloader

!!! abstract "学习目标！"

    在本次实践课程结束时，您将能够：

    - 设置自己的 "WIS2 Downloader" 实例并管理所需的特定配置
    - 浏览实例并设置订阅
    - 删除订阅并找到下载的数据

## 简介

在本次课程中，您将学习如何在提供的学生虚拟机上设置 WIS2 Downloader 实例，以及如何浏览其不同的服务。

!!! note "关于 WIS2 Downloader"
     
     WIS2 Downloader 是一个独立的 Docker Compose 项目。建议将其运行在与 wis2box 实例不同的服务器或虚拟机上，以避免下载过程干扰消息发布。

     如果您希望开发自己的服务来订阅 WIS2 通知并下载数据，可以参考 [WIS2 Downloader 源代码](https://github.com/World-Meteorological-Organization/wis2downloader)。

     如果需要一个同时支持发布和下载 WIS2 消息的轻量级替代方案，请查看 [pywis-pubsub 项目](https://github.com/World-Meteorological-Organization/pywis-pubsub)。

## 准备工作和要求

!!! note "如果在受限网络中"

    以下步骤仅需在下载器运行于不同网络且所需端口无法访问时应用。在任何配置中，以下端口是使用 WIS2 Downloader 堆栈全部功能所需的唯一端口。

在开始之前，请登录到您的学生虚拟机，并通过 SSH 隧道以下端口：

- `5002 (API)`
- `8080 (UI)`
- `3000 (Grafana)`

您可以通过修改 Putty 的连接设置，将这三个端口映射到您自己的电脑（localhost）：

![在 Putty 中添加隧道](../assets/img/putty-add-tunnel.png)

!!! note "在 Linux 和 macOS 上设置隧道"

    在 Linux 和 macOS 上，您可以直接从终端使用 SSH 命令的 `-L` 标志设置隧道：

    ```bash
    ssh -L 5002:localhost:5002 -L 8080:localhost:8080 -L 3000:localhost:3000 <username>@<WIS2DOWNLOADER_BASE_URL>
    ```

    将 `<username>` 和 `<WIS2DOWNLOADER_BASE_URL>` 替换为您的学生虚拟机凭据。

## WIS2 Downloader 安装

从 GitHub 下载最新的发布压缩包并在您的学生虚拟机上解压：

```bash
wget https://github.com/World-Meteorological-Organization/wis2downloader/archive/refs/tags/v1.0.0b1+rc4.tar.gz
tar -xzf v1.0.0b1+rc4.tar.gz
cd wis2downloader-*
```

运行安装脚本以生成配置文件：

```bash
bash setup.sh
```

使用以下下载路径 `/home/<username>/wis2-downloads`，将 `<username>` 替换为您的用户名。接下来，按 Enter 使用用户和组的默认值。

!!! note "管理用户权限"
    您可以通过修改 `.env` 文件中的 `WIS2DWONLOADER_UID` 和 `WIS2DWONLOADER_GID` 来使用不同的用户和组值。
    记得在更改这些值后重新构建镜像以应用更改。

这会根据默认值创建 `.env` 文件，并为 `FLASK_SECRET_KEY` 和 `REDIS_PASSWORD` 生成随机值。您可以使用 `cat .env` 查看文件内容——默认值适用于单机部署。

启动完整的服务堆栈：

```bash
docker compose up -d
```

!!! note "检查运行中的容器"
    您可以使用以下命令验证所有容器是否成功启动：
    ```bash
    docker compose ps
    ```
    您应该会看到订阅管理器、MQTT 订阅者、UI、Celery 工作器、Redis、Prometheus、Grafana 和 Loki 的服务。

## 访问 WIS2 Downloader UI

打开浏览器，导航到您的 WIS2 Downloader 实例的 UI，地址为 `http://<WIS2DOWNLOADER_BASE_URL>:8080`。

您将进入默认设置为 `Dashboard` 视图的登录页面，显示 Grafana 仪表板。

![WIS2 Downloader 登录页面](../assets/img/wis2-downloader-landing-page.png)

在左侧侧边栏菜单中，您可以浏览 UI 的所有不同部分。

主要可用部分包括：

- **Dashboard** — 默认登录页面，嵌入的 Grafana 仪表板显示下载活动、队列状态和运行服务的指标。也可通过 `http://<WIS2DOWNLOADER_BASE_URL>:3000` 访问。
- **Catalogue View** — 通过搜索或过滤全局目录浏览可用的 WIS2 数据集。选择一个主题和保存目录，然后点击 *Subscribe* 开始下载。
- **Tree View** — 以可折叠树的形式浏览 WIS2 主题层次结构。适用于在订阅之前探索可用主题。
- **Manual Subscribe** — 直接输入主题详细信息创建订阅，而无需依赖全局发现目录。适用于更自由地使用通配符订阅主题，并允许访问未在 GDC 中找到的主题，例如 GTS 网关和在非默认配置中发布于私有代理的主题。
- **Manage Subscriptions** — 查看和管理所有活动订阅。从这里可以看到正在监控的主题，并删除不再需要的订阅。
- **Settings** — 当前允许从全局发现目录重新加载数据集目录。未来版本将扩展此部分以涵盖 WIS2 Downloader 的一般配置和管理。
- **Documentation** — 显示 WIS2 Downloader 的内置文档。

## 在 UI 中管理订阅

如上例所示，您可以通过访问 `http://<WIS2DOWNLOADER_BASE_URL>:8080` 来访问运行实例的 UI。

设置订阅有三种方式：

- 在 **Catalogue View** 中，通过类似 GDC 门户的方式浏览可用主题。
- 在 **Tree View** 中，通过探索主题以类似 MQTT Explorer 的方式从 GDC 目录中选择主题。
- 在 **Manual Subscribe** 中，您可以输入自己想要的主题、过滤器和其他参数。

在以下练习中，我们将订阅来自所有 WIS2 节点的所有 synop 通知：

- 首先，进入 **Manual Subscribe**。
- 输入主题为 `cache/a/wis2/+/data/core/weather/surface-based-observations/synop`
- 设置目标文件夹为 `synop-data`

最终结果应类似于：
![WIS2 Downloader 手动订阅](../assets/img/wis2-downloader-manual-subscribe.png)

现在点击 **Subscribe** 按钮并确认您的订阅。

随后，通过以下命令检查学生虚拟机中的下载文件夹：

```bash
ls -R ~/wis2-downloads
```

现在您应该会看到由您的实例下载的一系列文件。

最后一步，我们可以通过进入 **Manage Subscriptions** 视图并点击 **Unsubscribe** 按钮来删除订阅。

![WIS2 Downloader 删除订阅](../assets/img/wis2-downloader-delete-subscription.png)

!!! note "删除下载的文件"

    建议在完成练习后清理下载文件夹，以释放学生虚拟机上的空间。因此，请运行以下命令删除之前练习的文件：

    ```bash
    rm -fr ~/wis2-downloads/synop-data
    ```

## 查看 WIS2 Downloader 配置

WIS2 Downloader 实例通过 `.env` 文件中定义的环境变量进行配置。

您可以在 [WIS2 Downloader 管理指南第 2.1 节](https://world-meteorological-organization.github.io/wis2downloader/en/admin-guide.html) 中查看环境变量的详细说明。

要查看当前的 WIS2 Downloader 配置，可以使用以下命令：

```bash
cat .env
```

!!! question "查看 WIS2 Downloader 的配置"

    下载数据的默认保留期是多少？

    订阅管理器 API 使用哪个端口？

??? success "点击查看答案"

    下载数据的默认保留期为 `30` 天，由 `DOWNLOAD_RETENTION_PERIOD` 设置。

    订阅管理器 API 使用端口 `5002`，由 `WIS2DOWNLOADER_SUBSCRIPTION_MANAGER_URL` 定义。

!!! note "更新 WIS2 Downloader 的配置"

    要更新配置，请编辑 `.env` 文件并重新启动堆栈以应用更改：

    ```bash
    docker compose up -d
    ```

您可以为接下来的练习保留默认配置。

## WIS2 Downloader API

WIS2 Downloader 在 `<WIS2DOWNLOADER_BASE_URL>:5002` 提供 REST API。确认服务已准备好：

```bash
curl localhost:5002/health
```

您应该会看到：

```json
{"status": "healthy"}
```

要创建订阅，请发送带有 MQTT `topic` 和可选 `target` 子目录的 `POST` 请求，文件将保存到该子目录：

```bash
curl -s -X POST localhost:5002/subscriptions \
  -H "Content-Type: application/json" \
  -d '{"topic": "cache/a/wis2/+/data/core/weather/surface-based-observations/#", "target": "surface-obs"}'
```

与之前一样，可以通过检查下载目录中的 `surface-obs` 文件夹查看下载的文件：

```bash
ls -R ~/wis2-downloads/surface-obs
```

响应中包含分配给新订阅的 UUID。当不再需要订阅时，可以使用它删除订阅：

```bash
curl -X DELETE localhost:5002/subscriptions/{id}
```

!!! note "删除下载的文件"

    建议在完成练习后清理下载文件夹，以释放学生虚拟机上的空间。因此，请运行以下命令删除之前练习的文件：

    ```bash
    rm -fr ~/wis2-downloads/surface-obs
    ```

有关可用端点的完整列表（列出、获取、更新订阅等），请参考位于 `localhost:5002/swagger` 的交互式 Swagger 文档。

## 总结

!!! success "恭喜！"

    在本次实践课程中，您学习了如何：

    - 在本地系统上安装 WIS2 Downloader 并更改默认配置
    - 使用 UI 创建和删除订阅
    - 使用 API 管理订阅
    - 在本地系统上查看下载的数据
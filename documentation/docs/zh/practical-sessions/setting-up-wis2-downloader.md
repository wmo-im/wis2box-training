---
title: 在学生虚拟机上设置 WIS2 Downloader
---

# 在学生虚拟机上设置 WIS2 Downloader

!!! abstract "学习目标！"

    完成本次实践课程后，您将能够：

    - 设置自己的 "WIS2 Downloader" 实例并管理所需的特定配置
    - 浏览实例并利用其不同功能

## 简介

在本次课程中，您将学习如何在提供的学生虚拟机上设置 WIS2 Downloader 实例，以及如何浏览其不同服务。

!!! note "关于 WIS2 Downloader"
     
     WIS2 Downloader 可作为独立的 Docker Compose 项目使用，建议在与 wis2box 不同的服务器上运行，以避免下载过程干扰消息发布。

     如果您希望开发自己的服务来订阅 WIS2 通知并下载数据，可以参考 [WIS2 Downloader 源代码](https://github.com/World-Meteorological-Organization/wis2downloader)。

## 准备和要求

!!! note "如果不是在培训期间"

    以下步骤仅在服务器默认未开放所需端口时适用。在任何配置中，以下端口是使用 WIS2 Downloader 堆栈全部功能所需的唯一端口。

在开始之前，请登录到您的学生虚拟机，并通过 SSH 隧道以下端口：

- `5002 (API)`
- `8080 (UI)`
- `3000 (Grafana)`

您可以在 Putty 中更改连接设置来完成此操作：

![访问 Putty 隧道设置](../assets/img/putty-tunnel-settings.png)

然后将这三个端口映射到您自己的电脑（localhost）上的端口：

![在 Putty 中添加隧道](../assets/img/putty-add-tunnel.png)

## WIS2 Downloader 安装

从 GitHub 下载最新发布的 tarball 并在您的学生虚拟机上解压：

```bash
wget https://github.com/World-Meteorological-Organization/wis2downloader/releases/latest/download/wis2downloader-latest.tar.gz
tar -xzf wis2downloader-latest.tar.gz
cd wis2downloader-*
```

运行设置脚本以生成配置文件：

```bash
bash setup.sh
```

此操作会根据默认值创建一个 `.env` 文件，并为 `FLASK_SECRET_KEY` 和 `REDIS_PASSWORD` 生成随机值。您可以使用 `cat .env` 查看文件内容——默认值适用于单机部署。

安装用于日志传输的 Loki Docker 插件：

```bash
ARCH=$(uname -m | sed 's/x86_64/amd64/;s/aarch64/arm64/')
docker plugin install grafana/loki-docker-driver:3.6.7-${ARCH} --alias loki --grant-all-permissions
```

验证插件是否已启用：

```bash
docker plugin ls
```

您应该看到 `loki:latest` 列出，并且 `ENABLED` 设置为 `true`。

创建一个专用的 `wis2` 组，将您的用户添加到该组，并相应地配置 `.env` 文件和下载目录：

```bash
sudo groupadd wis2
sudo usermod -aG wis2 $USER
sed -i "s/^UID=.*/UID=$(id -u)/" .env
sed -i "s/^GID=.*/GID=$(getent group wis2 | cut -d: -f3)/" .env
mkdir -p downloads
sudo chown $(id -un):wis2 downloads
chmod 775 downloads
```

!!! note "需要重新登录"
    用户组变更仅在您注销并重新登录 SSH 会话后生效。

启动完整的服务堆栈：

```bash
docker compose up -d
```

等待约 30 秒以通过健康检查，然后确认订阅管理器已准备好：

```bash
curl http://<WIS2DOWNLOADER_BASE_URL>:5002/health
```

!!! note "检查运行中的容器"
    您可以通过以下命令验证所有容器是否成功启动：
    ```bash
    docker compose ps
    ```
    您应该看到订阅管理器、MQTT 订阅者、UI、Celery 工作器、Redis、Prometheus、Grafana 和 Loki 的服务。

### 访问 WIS2 Downloader UI

打开浏览器并导航到您的 WIS2 Downloader 实例的 UI，地址为 `http://<WIS2DOWNLOADER_BASE_URL>:8080`。

您将进入默认设置为 `Help` 部分的登录页面，该页面显示文档内容。

![WIS2 Downloader 登录页面](../assets/img/wis2-downloader-landing-page.png)

在左侧的侧边栏菜单中，您可以浏览 UI 的所有不同部分。

主要可用部分包括：

- **Dashboard** — 一个嵌入的 Grafana 仪表板，显示下载活动、队列状态以及运行服务的指标。也可通过 `http://<WIS2DOWNLOADER_BASE_URL>:3000` 访问。
- **Catalogue View** — 通过搜索或过滤全局目录浏览可用的 WIS2 数据集。选择一个主题和保存目录，然后点击 *Subscribe* 开始下载。
- **Tree View** — 以可折叠树的形式浏览 WIS2 主题层次结构。用于在订阅之前探索可用主题。
- **Manual Subscribe** — 直接输入主题和代理详细信息创建订阅，而无需依赖 Global Discovery Catalogues。适用于订阅特定 WIS2 节点或私有代理的主题。
- **Manage Subscriptions** — 查看和管理所有活动订阅。从这里可以查看正在监控的主题并删除不再需要的订阅。
- **Settings** — 当前允许从 Global Discovery Catalogues 重新加载数据集目录。此部分将在未来版本中扩展，以涵盖 WIS2 Downloader 的一般配置和管理。
- **Help** — 默认登录页面，显示 WIS2 Downloader 的内置文档。

### 在 UI 中管理订阅

如上例所示，您可以通过访问运行实例的 UI，地址为 `http://<WIS2DOWNLOADER_BASE_URL>:8080`。

从那里可以通过以下三种方式设置订阅：

- 在 **Catalogue View** 中，通过类似 GDC 门户的方式浏览可用主题。
- 在 **Tree View** 中，通过探索主题（类似于 MQTT Explorer）从 GDC 目录中选择主题。
- 在 **Manual Subscribe** 中，输入您自己的主题、过滤器和其他参数。

在接下来的练习中，我们将订阅来自 DWD 管理的 GTS 到 WIS2 Gateway 的通知：

- 首先，进入 **Manual Subscribe**。
- 输入主题为 `cache/a/wis2/de-dwd-gts-to-wis2/data/core/#`
- 设置目标文件夹为 `gts-data`

最终结果应类似于：
![WIS2 Downloader 手动订阅](../assets/img/wis2-downloader-manual-subscribe.png)

接下来，通过以下命令进入学生虚拟机中的下载文件夹：

```bash
ls -R wisdownloader/downloads
```

现在您应该看到由您的实例下载的一系列文件。

最后一步，我们可以通过进入 **Manage Subscriptions** 视图并点击 **Unsubscribe** 按钮删除订阅。

![WIS2 Downloader 删除订阅](../assets/img/wis2-downloader-delete-subscription.png)

!!! note "删除下载的文件"

    建议在完成练习后清理下载文件夹，以释放学生虚拟机上的空间。因此，请运行以下命令删除之前练习的文件。

    ```bash
    rm -fr wisdownloader/downloads
    ```

### 查看 WIS2 Downloader 配置

WIS2 Downloader 实例可以通过 `.env` 文件中定义的环境变量进行配置。

您可以在 [WIS2 Downloader 管理指南第 2.1 节](https://world-meteorological-organization.github.io/wis2downloader/en/admin-guide.html) 中查看环境变量的详细说明。

要查看当前的 WIS2 Downloader 配置，可以使用以下命令：

```bash
cat .env
```

!!! question "查看 WIS2 Downloader 的配置"

    下载数据的默认保留期限是多少？

    订阅管理器 API 监听的端口是什么？

??? success "点击查看答案"

    下载数据的默认保留期限为 `30` 天，由 `DOWNLOAD_RETENTION_PERIOD` 设置。

    订阅管理器 API 监听的端口为 `5002`，由 `WIS2DOWNLOADER_SUBSCRIPTION_MANAGER_URL` 定义。

!!! note "更新 WIS2 Downloader 的配置"

    要更新配置，请编辑 `.env` 文件并重新启动堆栈以应用更改：

    ```bash
    docker compose up -d
    ```

您可以保留默认配置以进行后续练习。

### WIS2 Downloader API

WIS2 Downloader 在 `<WIS2DOWNLOADER_BASE_URL>:5002/api` 公开了一个 REST API。确认服务已准备好：

```bash
curl <WIS2DOWNLOADER_BASE_URL>:5002/api/health
```

您应该看到：

```json
{"status": "healthy"}
```

要创建订阅，请发送一个包含 MQTT `topic` 和可选 `target` 子目录的 `POST` 请求，文件将保存到该子目录：

```bash
curl -s -X POST <WIS2DOWNLOADER_BASE_URL>:5002/api/subscriptions \
  -H "Content-Type: application/json" \
  -d '{"topic": "cache/a/wis2/+/data/core/weather/surface-based-observations/#", "target": "surface-obs"}'
```

响应中包含分配给新订阅的 UUID。当不再需要时，可以使用它删除订阅：

```bash
curl -X DELETE <WIS2DOWNLOADER_BASE_URL>:5002/api/subscriptions/{id}
```

有关可用端点的完整列表（列出、获取、更新订阅等），请参考 `<WIS2DOWNLOADER_BASE_URL>:5002/api/openapi` 提供的交互式 Swagger 文档。

## 结论

!!! success "恭喜！"

    在本次实践课程中，您学习了：

    - 在本地系统上安装 WIS2 Downloader 并更改默认配置
    - 使用 UI 创建和删除订阅
    - 使用 API 管理订阅
    - 在本地系统上查看下载的数据
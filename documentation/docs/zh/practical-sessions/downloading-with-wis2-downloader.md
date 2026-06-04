---
title: 使用 WIS2 Downloader 下载数据
---

# 使用 WIS2 Downloader 下载数据

!!! abstract "学习目标！"

    在本次实践课程结束时，您将能够：

    - 探索并查找 WIS2 Downloader 中的数据集
    - 使用过滤功能控制下载的文件
    - 使用身份验证下载受访问控制的数据集
    - 修改 WIS2 Downloader 的默认设置以适应更高级的使用场景

## 介绍

在 WIS2 中，所有数据集都有一个元数据文件，可以在 **Global Discovery Catalogues** 中找到。因此，用户应始终通过这些服务查找在 WIS2 上共享的数据。

WIS2 Downloader 基于这一原则，通过查找这些 GDC 中的所有记录并在内部组合它们，使用户能够浏览 WIS2 上可用的数据。由于记录数量庞大，必须提供一种方式让用户筛选记录并找到正确的记录。即使找到并订阅了正确的记录，有些数据集的文件数量可能超出用户当前的需求。因此，需要第二级过滤——在决定是否下载文件时进行操作的过滤。

## 在目录视图中使用

**目录视图**是 WIS2 Downloader 中查找和订阅数据集的两种方式之一。它汇总来自 Global Discovery Catalogues 的记录，并以可搜索、可过滤的界面呈现——类似于直接浏览 GDC 门户。

在左侧边栏中导航到 **目录视图**。

![WIS2 Downloader 目录视图](../assets/img/wis2-downloader-catalogue-view.png)

页面顶部有一个搜索栏和一组过滤器。您可以使用这些工具通过关键字、Centre ID 或数据策略（核心与推荐）缩小可用记录的列表。

您还可以通过定义一个 **边界框** 来进行空间过滤，使用四个坐标输入——**北、东、南、西**——以十进制纬度和经度值表示。当设置边界框时，您可以选择两种匹配模式：

- **交叉**——返回空间范围与边界框有任何重叠的记录。
- **内部**——仅返回空间范围完全位于边界框内的记录。

!!! note "重新加载目录"

    目录在 WIS2 Downloader 启动时从 GDC 加载。如果您认为列表已过时，可以在左侧边栏的 **设置** 部分强制重新加载。

### 练习：查找并订阅数据集

!!! question "查找地面观测数据集"

    使用目录视图中的过滤器查找与温度和降水相关的 **核心** 地面观测数据集。

    1. 在搜索栏中输入 `surface`，观察记录列表如何被过滤。
    2. 将数据策略过滤器设置为 **核心**。
    3. 将关键字设置为包含 `temperature, precipitation`，观察结果如何变化。
    4. 从结果中选择一个记录以展开其详细信息。
    5. 查看显示的元数据——注意主题、来源中心和数据策略。
    6. 将目标文件夹设置为 `surface-obs`。
    7. 点击 **订阅** 创建订阅。

    订阅后，导航到 **管理订阅** 确认新订阅是否出现在列表中。

??? success "点击查看答案"

    任何主题包含 `surface-based-observations` 且数据策略为 `core` 的记录都是有效选择。应用关键字过滤器 `temperature, precipitation` 将进一步缩小结果范围到与这些变量相关的数据集。

    一旦订阅，**管理订阅** 视图将显示活动订阅及其主题和目标文件夹。文件将在代理上收到新通知后开始下载。

!!! note "取消订阅并删除已下载文件"
    
    转到 **管理订阅** 视图并从上一个练习中选择的主题中 `取消订阅`。

    然后清理下载文件夹：

    ```bash
    rm -fr /home/{USER}/wis2-downloads/surface-obs
    ```

## 在树视图中使用

**树视图** 以可折叠树的形式呈现 WIS2 主题层次结构，允许您逐级浏览可用主题——类似于在 MQTT Explorer 中导航主题。它设计用于更高层次的、自上而下的探索 WIS2 上可用的数据，从层次结构的根开始逐步深入。这与目录视图形成对比，后者直接将您带到单个数据集记录，更适合当您已经知道自己在寻找什么时使用。

在左侧边栏中导航到 **树视图**。

![WIS2 Downloader 树视图](../assets/img/wis2-downloader-tree-view.png)

树结构按照 WIS2 主题层次组织。点击节点展开每一层以显示其子节点。在任何层级，您都可以通过选择一个节点并点击 **订阅** 来订阅——使用通配符 (`#`) 捕获该节点下的所有主题。

!!! note "在不同层级订阅"

    在树结构较高层级订阅（例如在 Centre ID 层级）将捕获该中心发布的所有数据集。在较低层级订阅可以提供更细粒度的控制。使用 WIS2 Downloader 在树视图中订阅时自动附加的通配符 `#` 后缀。

### 练习：使用树视图查找并订阅数据集

!!! question "通过树视图订阅数据集"

    使用树视图查找并订阅来自特定中心的地面观测数据。

    1. 从 `cache` 节点开始展开树，然后依次导航 `a` → `wis2`。
    2. 选择您选择的 Centre ID 并继续展开，直到到达与 `surface-based-observations` 相关的主题。
    3. 查看显示的完整主题路径——确认它与您想要的数据集相符。
    4. 将目标文件夹设置为 `surface-obs-tree`。
    5. 点击 **订阅** 创建订阅。

    导航到 **管理订阅** 确认订阅是否激活。

??? success "点击查看答案"

    任何遵循模式 `cache/a/wis2/<centre-id>/data/core/weather/surface-based-observations/#` 的主题路径都是有效选择。Centre ID 部分将根据您在树中选择的中心而有所不同。

    **管理订阅** 视图将显示新订阅以及之前创建的任何订阅。

!!! note "取消订阅并删除已下载文件"
    
    转到 **管理订阅** 视图并从上一个练习中选择的主题中 **取消订阅**，然后清理下载文件夹：

    ```bash
    rm -fr /home/{USER}/wis2-downloads/surface-obs-tree
    ```

## 在手动订阅视图中使用

**手动订阅** 视图允许您直接输入主题创建订阅，而无需依赖 Global Discovery Catalogues。与目录视图和树视图——两者都从 GDC 中获取主题——不同，手动订阅在您已经知道确切的主题并希望在不浏览目录的情况下设置时非常有用，同时可以更自由地选择 WTH。

在左侧边栏中导航到 **手动订阅**。

![WIS2 Downloader 手动订阅](../assets/img/wis2-downloader-manual-subscribe.png)

表单允许您指定：

- **主题**——完整的 MQTT 订阅主题，包括任何通配符（例如 `#` 和 `+`）。
- **目标文件夹**——下载文件将保存的本地子目录。
- **过滤器**——控制下载哪些通知的可选过滤对象，以文本形式输入。
- **优先队列**——控制从该订阅接收的通知的下载优先级。
- **身份验证**——访问受控数据集所需的凭据。

!!! note "何时使用手动订阅"

    当您已经知道确切的主题并希望快速设置时使用手动订阅；当主题未包含在目录中，或需要为受访问控制的数据集提供凭据时使用。

## 从受访问控制的数据集中下载

WIS2 上的一些数据集是受访问控制的，这意味着在下载文件之前需要有效的凭据。WIS2 Downloader 在手动订阅视图中支持两种身份验证方法：

- **基本 HTTP 身份验证**——提供与您的访问凭据相关的用户名和密码。
- **Bearer token**——提供由数据发布者颁发的令牌代替用户名和密码。

这些凭据按订阅存储，并在下载该主题的文件时自动应用。

### 练习：订阅您 wis2box 上的受访问控制数据集

在本练习中，您将设置一个受访问控制的数据集，配置 WIS2 Downloader 订阅其代理，并验证在提供 Bearer token 时文件是否正确下载。

!!! question "设置并订阅受访问控制的数据集"

    **步骤 1 — 在 wis2box 上创建受访问控制的数据集**

    在您的 wis2box 实例上创建一个启用访问控制的数据集，并记录生成的主题和 Bearer token。如果尚未完成，请参考 [Datasets with access control](../datasets-with-access-control) 实践课程以完成完整设置步骤。

    **步骤 2 — 配置 WIS2 Downloader 监听 wis2box 代理**

    默认情况下，WIS2 Downloader 监听 Global Broker。要直接从您的 wis2box 实例接收通知，您需要在 WIS2 Downloader 的 compose 文件中添加一个指向 wis2box 内部 MQTT 代理的订阅者。

    打开 WIS2 Downloader 目录中的 `docker-compose.yml` 文件，并添加以下订阅者配置：

    ```yaml
      subscriber-test:
    container_name: subscriber-test
    restart: always
    build:
      context: .
      dockerfile: ./containers/subscriber/Dockerfile
      args:
        WIS2DOWNLOADER_UID: ${WIS2DOWNLOADER_UID:-10001}
        WIS2DOWNLOADER_GID: ${WIS2DOWNLOADER_GID:-988}
    env_file: *default-env
    environment:
      GLOBAL_BROKER_HOST: WIS2BOX_URL
      GLOBAL_BROKER_PORT: 443
      GLOBAL_BROKER_USERNAME: everyone
      GLOBAL_BROKER_PASSWORD: everyone
      MQTT_PROTOCOL: websockets
    depends_on:
      - redis
    networks:
      - redis-net
    logging: *loki-logging
    healthcheck:
      test: ["CMD", "pgrep", "-f", "subscriber_start"]
      interval: 30s
      timeout: 5s
      retries: 3
    ```

    重启堆栈以应用更改：

    ```bash
    docker compose down
    docker compose up -d
    ```

    **步骤 3 — 在 WIS2 Downloader 中订阅数据集**

    1. 在 WIS2 Downloader UI 中导航到 **手动订阅**。
    2. 将主题设置为您在 wis2box 上为受访问控制的数据集配置的主题。
    3. 将目标文件夹设置为 `restricted-data`。
    4. 在 **身份验证** 字段中输入步骤 1 中生成的 Bearer token。
    5. 点击 **订阅** 创建订阅。

    **步骤 4 — 将数据推送到 wis2box 上的数据集**

    在您的 wis2box 实例上，将文件发布到受访问控制的数据集。请参考 [Ingesting data for publication](../ingesting-data-for-publication) 实践课程以了解发布数据的步骤。

    **步骤 5 — 验证下载**

    检查文件是否已被 WIS2 Downloader 下载：

    ```bash
    ls /home/{USER}/wis2-downloads/restricted-data
    ```

??? success "点击查看答案"

    使用有效的 Bearer token 时，WIS2 Downloader 将在下载受限制主题的文件时进行身份验证。步骤 4 中发布的文件应在被 wis2box 接收后不久出现在 `restricted-data` 文件夹中。

    如果身份验证失败，即使订阅在 **管理订阅** 视图中显示为活动状态，文件也不会被下载。请仔细检查 Bearer token 是否与 wis2box 数据集上配置的匹配。

!!! note "取消订阅并删除已下载文件"

    转到 **管理订阅** 视图并 **取消订阅** 主题，然后清理下载文件夹：

    ```bash
    rm -fr /home/{USER}/wis2-downloads/restricted-data
    ```
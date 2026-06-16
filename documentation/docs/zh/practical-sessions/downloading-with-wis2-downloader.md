---
title: 使用 WIS2 Downloader 下载数据
---

# 使用 WIS2 Downloader 下载数据

!!! abstract "学习目标！"

    在本次实践课程结束时，您将能够：

    - 查找并订阅数据集
    - 使用过滤功能控制下载的文件
    - 使用身份验证下载受访问权限控制的数据集
    - 更改 WIS2 Downloader 的默认设置以适应更高级的使用场景

## 简介

在 WIS2 中，所有数据集都有一个元数据文件，可以在 **Global Discovery Catalogues** 中找到。因此，建议用户始终通过这些服务查找在 WIS2 上共享的数据。

WIS2 Downloader 使用这一原则，通过查找这些 GDC 中的所有记录并在内部组合它们，使用户能够浏览 WIS2 上可用的数据。由于记录数量庞大，必须提供一种方法让用户筛选这些记录并找到正确的记录。即使找到并订阅了正确的记录，某些数据集的文件数量可能仍然超过用户当前的需求。因此，需要第二级过滤——在决定是否下载文件时进行操作。

## 在目录视图中使用

**目录视图**是 WIS2 Downloader 中查找和订阅数据集的两种方式之一。它从 Global Discovery Catalogues 中聚合记录，并以可搜索、可过滤的界面呈现——类似于直接浏览 GDC 门户。

在左侧边栏导航到 **目录视图**。

![WIS2 Downloader Catalogue View](../assets/img/wis2-downloader-catalogue-view.png)

在页面顶部，您会看到一个搜索栏和一组过滤器。您可以使用这些工具通过关键字、Centre ID 或数据策略（核心与推荐）缩小可用记录的列表。

您还可以通过定义一个 **边界框** 来进行空间过滤，使用四个坐标输入——**北**、**西**、**南**和**东**——以十进制纬度和经度值表示。当设置边界框时，您可以选择两种匹配模式：

- **交叉**——返回空间范围与边界框有任何重叠的记录。
- **内部**——仅返回空间范围完全落在边界框内的记录。

!!! note "重新加载目录"

    目录在 WIS2 Downloader 启动时从 GDC 加载。如果您认为列表已过时，可以从左侧边栏的 **设置** 部分强制重新加载。

### 练习：查找并订阅数据集

!!! question "查找地面观测数据集"

    使用目录视图中的过滤器查找与温度和降水相关的 **核心** 地面观测数据集。

    1. 在搜索栏中输入 `surface`，观察记录列表如何被过滤。
    2. 将数据策略过滤器设置为 **核心**。
    3. 将关键字设置为包括 `temperature, precipitation`，观察结果如何变化。
    4. 从结果中选择一个记录以展开其详细信息。
    5. 查看显示的元数据——注意主题、来源中心和数据策略。
    6. 将目标文件夹设置为 `surface-obs`。
    7. 点击 **订阅** 创建订阅。

    订阅后，导航到 **管理订阅** 确认新订阅是否出现在列表中。

??? success "点击查看答案"

    任何主题包含 `surface-based-observations` 且数据策略为 `core` 的记录都是有效选择。应用关键字过滤器 `temperature, precipitation` 将进一步缩小结果范围至与这些变量相关的数据集。

    订阅后，**管理订阅** 视图将显示活动订阅及其主题和目标文件夹。文件将在代理接收到新通知时开始下载。

!!! note "取消订阅并删除下载的文件"
    
    转到 **管理订阅** 视图并从之前练习中选择的主题 `取消订阅`。

    然后清理下载文件夹：

    ```bash
    rm -fr /home/<username>/wis2-downloads/surface-obs
    ```

## 在树视图中使用

**树视图** 以可折叠树的形式呈现 WIS2 主题层次结构，允许您逐级浏览可用主题——类似于在 MQTT Explorer 中导航主题。它旨在从高层次、从上到下探索 WIS2 上可用的数据，从层次结构的根开始逐步深入。这与目录视图形成对比，后者直接将您带到单个数据集记录，更适合当您已经知道自己在寻找什么时使用。

在左侧边栏导航到 **树视图**。

![WIS2 Downloader Tree View](../assets/img/wis2-downloader-tree-view.png)

树结构按照 WIS2 主题层次组织。通过点击节点展开每一级以显示其子节点。在任何级别，您都可以通过选择一个节点并点击 **订阅** 来订阅——使用通配符 (`#`) 捕获该节点下的所有主题。

!!! note "在不同级别订阅"

    在树中较高的级别订阅（例如在 Centre ID 级别）将捕获该中心发布的所有数据集。在较低级别订阅可以提供更细粒度的控制。使用 WIS2 Downloader 在树视图中订阅时自动附加的通配符 `#` 后缀。

### 练习：使用树视图查找并订阅

!!! question "通过树视图订阅数据集"

    使用树视图查找并订阅来自特定中心的地面观测数据。

    1. 从 `cache` 节点开始展开树，然后导航到 `a` → `wis2`。
    2. 选择您选择的 Centre ID 并继续展开，直到找到与 `surface-based-observations` 相关的主题。
    3. 查看显示的完整主题路径——确认它与您想要的数据集相符。
    4. 将目标文件夹设置为 `surface-obs-tree`。
    5. 点击 **订阅** 创建订阅。

    导航到 **管理订阅** 确认订阅是否处于活动状态。

??? success "点击查看答案"

    任何遵循模式 `cache/a/wis2/<centre-id>/data/core/weather/surface-based-observations/#` 的主题路径都是有效选择。Centre ID 段将根据您在树中选择的中心而有所不同。

    **管理订阅** 视图将显示新订阅以及之前创建的订阅。

!!! note "取消订阅并删除下载的文件"
    
    转到 **管理订阅** 视图并从之前练习中选择的主题 `取消订阅`。

    然后清理下载文件夹：

    ```bash
    rm -fr /home/<username>/wis2-downloads/surface-obs-tree
    ```

## 使用手动订阅视图

**手动订阅** 视图允许您直接输入主题创建订阅，而无需依赖 Global Discovery Catalogues。与目录视图和树视图不同——它们都从 GDC 中获取主题——手动订阅在您已经知道确切的主题并希望设置订阅时非常有用，无需浏览目录，并且可以更自由地选择 WTH。

在左侧边栏导航到 **手动订阅**。

![WIS2 Downloader Manual Subscribe](../assets/img/wis2-downloader-manual-subscribe.png)

表单允许您指定：

- **主题**——完整的 MQTT 订阅主题，包括任何通配符（例如 `#` 和 `+`）。
- **目标文件夹**——下载的文件将保存到的本地子目录。
- **过滤器**——控制下载哪些通知的可选过滤对象，以文本形式输入。
- **优先队列**——控制从该订阅接收的通知的下载优先级。
- **身份验证**——访问受控数据集所需的凭据。

!!! note "何时使用手动订阅"

    当您已经知道确切的主题并希望快速设置订阅时使用手动订阅；当主题未包含在目录中时，或当您需要为受访问权限控制的数据集提供凭据时使用。

## 从受访问权限控制的数据集中下载

WIS2 上的某些数据集是受访问权限控制的，这意味着在下载文件之前需要有效的凭据。WIS2 Downloader 在手动订阅视图中支持两种身份验证方法：

- **基本 HTTP 身份验证**——提供与您的访问凭据相关的用户名和密码。
- **Bearer token**——提供由数据发布者签发的令牌代替用户名和密码。

这些凭据按订阅存储，并在为该主题下载文件时自动应用。

### 练习：订阅您 wis2box 上的受访问权限控制的数据集

在本练习中，您将设置一个受访问权限控制的数据集在您的 wis2box 实例上，配置 WIS2 Downloader 订阅其代理，并验证在提供 Bearer token 时文件是否正确下载。

!!! question "设置并订阅受访问权限控制的数据集"

    **步骤 1 — 在 wis2box 上创建一个受访问权限控制的数据集**

    在您的 wis2box 实例上创建一个启用访问控制的数据集，并记录其主题和为其生成的 Bearer token。如果尚未完成，请参考 [Datasets with access control](datasets-with-access-control.md) 实践课程以获取完整的设置步骤。

**步骤 2 — 配置 WIS2 Downloader 监听 wis2box broker**

默认情况下，WIS2 Downloader 监听 Global Broker。为了直接接收来自您的 wis2box 实例的通知，您需要在 WIS2 Downloader 的 compose 文件中添加一个订阅者，该订阅者指向 wis2box 内部的 MQTT broker。

打开 WIS2 Downloader 目录中的 `docker-compose.yml` 文件，并添加以下订阅者配置，将 `WIS2BOX_URL` 替换为您的 wis2box 实例的 URL：

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

重启服务以应用更改：

```bash
docker compose down
docker compose up -d
```

**步骤 3 — 在 WIS2 Downloader 中订阅数据集**

1. 在 WIS2 Downloader UI 中导航到 **Manual Subscribe**。
2. 将主题设置为您在 wis2box 上为访问控制数据集配置的主题。
3. 将目标文件夹设置为 `restricted-data`。
4. 在 **Authentication** 字段中输入步骤 1 中生成的 bearer token。
5. 点击 **Subscribe** 创建订阅。

**步骤 4 — 将数据推送到 wis2box 上的数据集**

在您的 wis2box 实例上，将文件发布到访问控制的数据集。有关数据发布的步骤，请参考 [Ingesting data for publication](ingesting-data-for-publication.md) 实践课程。

**步骤 5 — 验证下载**

检查文件是否已被 WIS2 Downloader 下载：

```bash
ls /home/<username>/wis2-downloads/restricted-data
```

??? success "点击查看答案"

使用有效的 bearer token 时，WIS2 Downloader 在下载访问控制主题的文件时会进行身份验证。步骤 4 中发布的文件应在被 wis2box 接收后不久出现在 `restricted-data` 文件夹中。

如果身份验证失败，即使订阅在 **Manage Subscriptions** 视图中显示为活动状态，文件也不会被下载。请仔细检查 bearer token 是否与 wis2box 数据集上配置的 token 匹配。

!!! note "取消订阅并删除已下载文件"

进入 **Manage Subscriptions** 视图，点击 **Unsubscribe** 取消订阅主题，然后清理下载文件夹：

```bash
rm -fr /home/<username>/wis2-downloads/restricted-data
```

## 下载过滤

过滤器允许您在通知级别控制从订阅中下载哪些文件——这是介绍中提到的第二级过滤。您可以定义过滤器，使只有符合特定条件的通知触发下载，而不是下载主题上发布的所有文件。

在 **Catalogue View** 或 **Tree View** 中选择数据集后，右侧屏幕会出现一个过滤器面板。在订阅之前，您可以在此填写要应用的过滤器值。WIS2 Downloader 会根据您的输入自动生成过滤器对象。

在 **Manual Subscribe** 视图中，您需要手动填写过滤器对象，通过表单中的 `Filter (JSON)` 输入字段完成。

!!! note "可用过滤器输入"

- **媒体类型** — 限制下载特定内容类型（例如 `application/bufr`）。
- **数据集** — 根据元数据标识符限制下载特定数据集。
- **边界框** — 限制下载通知，其数据位于由 `north`、`south`、`east` 和 `west` 值定义的空间区域内。
- **日期和时间范围** — 限制下载通知，其发布时间在特定时间范围内。
- **自定义过滤器** — 根据元数据记录中定义的任何其他通知属性进行过滤，通过指定属性值（例如通过 `wigos_station_identifier` 过滤，仅下载来自特定站点的数据）。

以下是根据这些输入生成的过滤器对象示例：

```json
{
  "rules": [
    {
      "id": "accept",
      "order": 1,
      "match": {
        "all": [
          {
            "any": [
              { "media_type": { "exists": false } },
              { "media_type": { "in": ["application/bufr", "application/x-bufr"] } }
            ]
          },
          { "metadata_id": { "in": ["urn:wmo:md:ir-irimo:core.surface-based-observations.temp"] } },
          { "bbox": { "north": 23.0, "south": 27.0, "east": 25.0, "west": 28.0 } },
          {
            "property": "pubtime",
            "type": "datetime",
            "between": ["2026-06-08T20:00:00+00:00", "2026-06-09T05:00:59+00:00"]
          },
          {
            "property": "wigos_station_identifier",
            "type": "string",
            "in": ["0-20000-0-78338"]
          }
        ]
      },
      "action": "accept"
    },
    {
      "id": "default",
      "order": 999,
      "match": { "always": true },
      "action": "reject",
      "reason": "No filter criteria matched"
    }
  ]
}
```

### 练习：使用过滤器订阅

使用 Catalogue View 找到一个地面观测数据集，并在订阅前应用空间过滤器。

1. 导航到 **Catalogue View**，搜索您选择的地面观测数据集。
2. 选择数据集以在右侧面板中展开其详细信息。
3. 在过滤器输入中，为您选择的区域设置 **边界框**。
4. 可选：设置 **媒体类型** 过滤器以限制下载 BUFR 文件。
5. 将目标文件夹设置为 `filtered-obs`。
6. 点击 **Subscribe** 创建订阅。

等待文件到达并验证只有符合过滤器条件的文件被下载。

??? success "点击查看答案"

只有符合您定义的所有条件的通知才会被接受并下载。其他通知将被默认的兜底规则拒绝。

!!! note "取消订阅并删除已下载文件"

进入 **Manage Subscriptions** 视图，点击 **Unsubscribe** 取消订阅主题，然后清理下载文件夹：

```bash
rm -fr /home/<username>/wis2-downloads/filtered-obs
```

## 结论

!!! success "恭喜！"

在本次实践课程中，您学习了：

- 如何使用 Catalogue View 和 Tree View 查找并订阅数据集
- 如何直接使用 Manual Subscribe 视图订阅主题
- 如何应用过滤器控制从订阅中下载哪些文件
- 如何使用身份验证从访问控制的数据集中下载文件
---
title: 使用 MQTT 连接到 WIS2
---

# 使用 MQTT 连接到 WIS2

!!! abstract "学习目标"

    在本次实践课程结束时，您将能够：

    - 使用 MQTT Explorer 连接到 WIS2 Global Broker
    - 查看 WIS2 的主题结构
    - 查看 WIS2 通知消息结构

## 简介

WIS2 使用 MQTT 协议来宣传天气/气候/水文数据的可用性。WIS2 Global Broker 订阅网络中所有 WIS2 Node，并重新发布它接收到的消息。Global Cache 订阅 Global Broker，下载消息中的数据，然后在 `cache` 主题上重新发布消息，并附上新的 URL。Global Discovery Catalogue 从 Broker 发布发现元数据，并提供搜索 API。

以下是一个 WIS2 通知消息结构的示例，该消息接收自主题 `origin/a/wis2/br-inmet/data/core/weather/surface-based-observations/synop`：

```json
{
   "id":"3c14d7bf-e6b9-4f59-b4ea-f2fc52a33cd3",
   "type":"Feature",
   "conformsTo":[
      "http://wis.wmo.int/spec/wnm/1/conf/core"
   ],
   "geometry":{
      "coordinates":[
         -99.1964,
         19.404,
         2314
      ],
      "type":"Point"
   },
   "properties":{
      "data_id":"br-inmet:data:core:weather:surface-based-observations:synop/WIGOS_0-20000-0-76679_20250206T231600",
      "datetime":"2025-02-06T23:16:00Z",
      "pubtime":"2026-01-20T13:14:52Z",
      "integrity":{
         "method":"sha512",
         "value":"qtlI3Noay2I4zcdA1XCpn8vzVLIt0RKrR398VGFgTttc1XRUVb4dHWNCDKPXUo4mNkiFKx5TTHBvrxlzqWmMnQ=="
      },
      "metadata_id":"urn:wmo:md:br-inmet:data:core:weather:surface-based-observations:synop",
      "wigos_station_identifier":"0-20000-0-76679"
   },
   "links":[
      {
         "rel":"canonical",
         "type":"application/bufr",
         "href":"http://localhost/data/2025-02-06/wis/urn:wmo:md:br-inmet:data:core:weather:surface-based-observations:synop/WIGOS_0-20000-0-76679_20250206T231600.bufr4",
         "length":125117
      },
      {
         "rel":"via",
         "type":"text/html",
         "href":"https://oscar.wmo.int/surface/#/search/station/stationReportDetails/0-20000-0-76679"
      }
   ],
   "generated_by":"wis2box 1.2.0"
}
```

在本次实践课程中，您将学习如何使用 MQTT Explorer 工具设置 MQTT 客户端连接到 WIS2 Global Broker，并能够显示 WIS2 通知消息。

MQTT Explorer 是一个浏览和查看特定 MQTT Broker 主题结构的有用工具，用于查看正在发布的数据。

!!! note "关于 MQTT"
    MQTT Explorer 提供了一个用户友好的界面，用于连接到 MQTT Broker 并探索 WIS2 使用的主题和消息结构。
    
    实际上，MQTT 旨在用于机器对机器的通信，其中应用程序或服务订阅主题并以编程方式实时处理消息。
    
    如果需要以编程方式使用 MQTT（例如在 Python 中），您可以使用 MQTT 客户端库，例如 [paho-mqtt](https://pypi.org/project/paho-mqtt)，连接到 MQTT Broker 并处理传入的消息。根据您的需求和技术环境，有许多 MQTT 客户端和服务器软件可供选择。

## 使用 MQTT Explorer 连接到 Global Broker

要查看 WIS2 Global Broker 发布的消息，您可以使用 "MQTT Explorer"，可以从 [MQTT Explorer 网站](https://mqtt-explorer.com) 下载。

打开 MQTT Explorer，并使用以下详细信息添加一个新的连接到由 MeteoFrance 托管的 Global Broker：

- host: globalbroker.meteo.fr
- port: 8883
- username: everyone
- password: everyone

<img alt="mqtt-explorer-global-broker-connection" src="/../assets/img/mqtt-explorer-global-broker-connection.png" width="800">

点击 'ADVANCED' 按钮，移除预配置的主题，并添加以下订阅主题：

- `origin/a/wis2/#`

<img alt="mqtt-explorer-global-broker-advanced" src="/../assets/img/mqtt-explorer-global-broker-sub-origin.png" width="800">

!!! note
    设置 MQTT 订阅时，您可以使用以下通配符：

    - **单层通配符 (+)**：单层通配符替代一个主题层级
    - **多层通配符 (#)**：多层通配符替代多个主题层级

    在此情况下，`origin/a/wis2/#` 将订阅 `origin/a/wis2` 主题下的所有主题。

点击 'BACK'，然后点击 'SAVE' 保存您的连接和订阅详细信息。接着点击 'CONNECT'：

消息应开始出现在您的 MQTT Explorer 会话中，如下所示：

<img alt="mqtt-explorer-global-broker-topics" src="/../assets/img/mqtt-explorer-global-broker-msg-origin.png" width="800">

现在，您已准备好开始探索 WIS2 的主题和消息结构。

## 练习 1：查看 WIS2 主题结构

使用 MQTT 浏览 `origin` 主题下的主题结构。

!!! question
    
    我们如何区分发布数据的 WIS 中心？

??? success "点击查看答案"

    您可以点击 MQTT Explorer 左侧窗口，展开主题结构。
    
    我们可以通过查看主题结构的第四层来区分发布数据的 WIS 中心。例如，以下主题：

    `origin/a/wis2/br-inmet/data/core/weather/surface-based-observations/synop`

    告诉我们数据是由 WIS 中心 `br-inmet` 发布的，这是巴西 Instituto Nacional de Meteorologia - INMET 的中心 ID。

!!! question

    我们如何区分由托管 GTS-to-WIS2 网关的 WIS 中心发布的消息和由托管 WIS2 Node 的 WIS 中心发布的消息？

??? success "点击查看答案"

    我们可以通过查看主题结构中的中心 ID 来区分来自 GTS-to-WIS2 网关的消息。例如，以下主题：

    `origin/a/wis2/de-dwd-gts-to-wis2/data/core/I/S/A/I/01/sbbr`

    告诉我们数据是由德国 Deutscher Wetterdienst (DWD) 托管的 GTS-to-WIS2 网关发布的。GTS-to-WIS2 网关是一种特殊类型的数据发布者，它将来自全球电信系统 (GTS) 的数据发布到 WIS2。主题结构由 GTS 消息的 TTAAii CCCC 头组成。

## 练习 2：查看 WIS2 消息结构

断开 MQTT Explorer 的连接，并更新 'Advanced' 部分，将订阅更改为以下内容：

* `origin/a/wis2/+/data/core/weather/surface-based-observations/synop`
* `cache/a/wis2/+/data/core/weather/surface-based-observations/synop`

<img alt="mqtt-explorer-global-broker-topics-exercise2" src="/../assets/img/mqtt-explorer-global-broker-sub-origin-cache-synop.png" width="800">

!!! note
    `+` 通配符用于订阅所有 WIS 中心。

重新连接到 Global Broker 并等待消息出现。

您可以在右侧的 "Value" 部分查看 WIS2 消息的内容。尝试展开主题结构，查看消息的不同层级，直到到达最后一层，并查看其中一条消息的内容。

!!! question

    我们如何识别数据发布的时间戳？我们如何识别数据收集的时间戳？

??? success "点击查看答案"

    数据发布的时间戳包含在消息的 `properties` 部分，键为 `pubtime`。

    数据收集的时间戳包含在消息的 `properties` 部分，键为 `datetime`。

    <img alt="mqtt-explorer-global-broker-msg-properties" src="/../assets/img/mqtt-explorer-global-broker-msg-properties.png" width="800">

!!! question

    我们如何从消息中提供的 URL 下载数据？

??? success "点击查看答案"

    URL 包含在 `links` 部分，`rel="canonical"`，由 `href` 键定义。

    您可以复制该 URL 并将其粘贴到浏览器中下载数据。

## 练习 3：查看 'origin' 和 'cache' 主题的区别

确保您仍然使用 `origin/a/wis2/+/data/core/weather/surface-based-observations/synop` 和 `cache/a/wis2/+/data/core/weather/surface-based-observations/synop` 主题订阅连接到 Global Broker，如练习 2 中所述。

尝试识别在 `origin` 和 `cache` 主题上由相同中心 ID 发布的消息。

!!! question

    发布在 `origin` 和 `cache` 主题上的消息有什么区别？

??? success "点击查看答案"

    发布在 `origin` 主题上的消息是 Global Broker 从网络中的 WIS2 Node 重新发布的原始消息。

    发布在 `cache` 主题上的消息是 Global Cache 下载数据后重新发布的消息。如果您检查以 `cache` 开头的主题中的消息内容，您会发现 'canonical' 链接已更新为一个新的 URL。
    
    WIS2 网络中有多个 Global Cache，因此您将收到每个下载该消息的 Global Cache 发布的一条消息。

    Global Cache 仅下载并重新发布发布在 `../data/core/...` 主题层级上的消息。

## 结论

!!! success "恭喜！"
    在本次实践课程中，您学习了：

    - 如何使用 MQTT Explorer 订阅 WIS2 Global Broker 服务
    - WIS2 的主题结构
    - WIS2 的通知消息结构
    - 核心数据和推荐数据的区别
    - GTS-to-WIS2 网关使用的主题结构
    - 发布在 `origin` 和 `cache` 主题上的 Global Broker 消息的区别
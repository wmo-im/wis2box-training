---
title: 通过 MQTT 连接到 WIS2
---

# 通过 MQTT 连接到 WIS2

!!! abstract "学习目标"

    在本次实践课程结束时，您将能够：

    - 使用 MQTT Explorer 连接到 WIS2 Global Broker
    - 查看 WIS2 的主题结构
    - 查看 WIS2 通知消息结构

## 简介

WIS2 使用 MQTT 协议来宣传天气/气候/水文数据的可用性。WIS2 Global Broker 订阅网络中所有 WIS2 Nodes，并重新发布其接收到的消息。Global Cache 订阅 Global Broker，下载消息中的数据，然后在 `cache` 主题上以新的 URL 重新发布消息。Global Discovery Catalogue 从 Broker 发布发现元数据，并提供搜索 API。

以下是一个 WIS2 通知消息结构的示例，该消息接收到的主题为 `origin/a/wis2/br-inmet/data/core/weather/surface-based-observations/synop`：

```json
{
   "id":"7a34051b-aa92-40f3-bbab-439143657c8c",
   "type":"Feature",
   "conformsTo":[
      "http://wis.wmo.int/spec/wnm/1/conf/core"
   ],
   "geometry":{
      "type":"Polygon",
      "coordinates":[
         [
            [
               -73.98723548042966,
               5.244486395687602
            ],
            [
               -34.729993455533034,
               5.244486395687602
            ],
            [
               -34.729993455533034,
               -33.768377780900764
            ],
            [
               -73.98723548042966,
               -33.768377780900764
            ],
            [
               -73.98723548042966,
               5.244486395687602
            ]
         ]
      ]
   },
   "properties":{
      "data_id":"br-inmet/metadata/urn:wmo:md:br-inmet:rr1ieq",
      "datetime":"2026-01-20T08:30:21Z",
      "pubtime":"2026-01-20T08:30:22Z",
      "integrity":{
         "method":"sha512",
         "value":"RN+GzqgONURtkzOCo5vQJ5t7SzlAvaGONywEnTXHrHew9RQmUhrHbASvmDlCeRTb8vhE+1/h/7/20f2XJFHCcA=="
      },
      "content":{
         "encoding":"base64",
         "value":"eyJpZCI6ICJ1cm46d21vOm1kOmJyLWlubWV0OnJyMWllcSIsICJjb25mb3Jtc1RvIjogWyJodHRwOi8vd2lzLndtby5pbnQvc3BlYy93Y21wLzIvY29uZi9jb3JlIl0sICJ0eXBlIjogIkZlYXR1cmUiLCAidGltZSI6IHsiaW50ZXJ2YWwiOiBbIjIwMjYtMDEtMjAiLCAiLi4iXSwgInJlc29sdXRpb24iOiAiUFQxSCJ9LCAiZ2VvbWV0cnkiOiB7InR5cGUiOiAiUG9seWdvbiIsICJjb29yZGluYXRlcyI6IFtbWy03My45ODcyMzU0ODA0Mjk2NiwgNS4yNDQ0ODYzOTU2ODc2MDJdLCBbLTM0LjcyOTk5MzQ1NTUzMzAzNCwgNS4yNDQ0ODYzOTU2ODc2MDJdLCBbLTM0LjcyOTk5MzQ1NTUzMzAzNCwgLTMzLjc2ODM3Nzc4MDkwMDc2NF0sIFstNzMuOTg3MjM1NDgwNDI5NjYsIC0zMy43NjgzNzc3ODA5MDA3NjRdLCBbLTczLjk4NzIzNTQ4MDQyOTY2LCA1LjI0NDQ4NjM5NTY4NzYwMl1dXX0sICJwcm9wZXJ0aWVzIjogeyJ0eXBlIjogImRhdGFzZXQiLCAiaWRlbnRpZmllciI6ICJ1cm46d21vOm1kOmJyLWlubWV0OnJyMWllcSIsICJ0aXRsZSI6ICJIb3VybHkgc3lub3B0aWMgb2JzZXJ2YXRpb25zIGZyb20gZml4ZWQtbGFuZCBzdGF0aW9ucyAoU1lOT1ApIChici1pbm1ldCkiLCAiZGVzY3JpcHRpb24iOiAidGVzdCIsICJrZXl3b3JkcyI6IFsib2JzZXJ2YXRpb25zIiwgInRlbXBlcmF0dXJlIiwgInZpc2liaWxpdHkiLCAicHJlY2lwaXRhdGlvbiIsICJwcmVzc3VyZSIsICJjbG91ZHMiLCAic25vdyBkZXB0aCIsICJldmFwb3JhdGlvbiIsICJyYWRpYXRpb24iLCAid2luZCIsICJ0b3RhbCBzdW5zaGluZSIsICJodW1pZGl0eSJdLCAidGhlbWVzIjogW3siY29uY2VwdHMiOiBbeyJpZCI6ICJ3ZWF0aGVyIiwgInRpdGxlIjogIldlYXRoZXIifV0sICJzY2hlbWUiOiAiaHR0cDovL2NvZGVzLndtby5pbnQvd2lzL3RvcGljLWhpZXJhcmNoeS9lYXJ0aC1zeXN0ZW0tZGlzY2lwbGluZSJ9XSwgImNvbnRhY3RzIjogW3sib3JnYW5pemF0aW9uIjogIndtbyIsICJlbWFpbHMiOiBbeyJ2YWx1ZSI6ICJ0ZXN0QGNuLmNvbSJ9XSwgImFkZHJlc3NlcyI6IFt7ImNvdW50cnkiOiAiQlJBIn1dLCAibGlua3MiOiBbeyJyZWwiOiAiYWJvdXQiLCAiaHJlZiI6ICJodHRwOi8vdGVzdC5jb20iLCAidHlwZSI6ICJ0ZXh0L2h0bWwifV0sICJyb2xlcyI6IFsiaG9zdCJdfV0sICJjcmVhdGVkIjogIjIwMjYtMDEtMjBUMDg6MzA6MjFaIiwgInVwZGF0ZWQiOiAiMjAyNi0wMS0yMFQwODozMDoyMVoiLCAid21vOmRhdGFQb2xpY3kiOiAiY29yZSIsICJpZCI6ICJ1cm46d21vOm1kOmJyLWlubWV0OnJyMWllcSJ9LCAibGlua3MiOiBbeyJocmVmIjogIm1xdHQ6Ly9ldmVyeW9uZTpldmVyeW9uZUBsb2NhbGhvc3Q6MTg4MyIsICJ0eXBlIjogImFwcGxpY2F0aW9uL2pzb24iLCAibmFtZSI6ICJvcmlnaW4vYS93aXMyL2JyLWlubWV0L2RhdGEvY29yZS93ZWF0aGVyL3N1cmZhY2UtYmFzZWQtb2JzZXJ2YXRpb25zL3N5bm9wIiwgInJlbCI6ICJpdGVtcyIsICJjaGFubmVsIjogIm9yaWdpbi9hL3dpczIvYnItaW5tZXQvZGF0YS9jb3JlL3dlYXRoZXIvc3VyZmFjZS1iYXNlZC1vYnNlcnZhdGlvbnMvc3lub3AiLCAiZmlsdGVycyI6IHsid2lnb3Nfc3RhdGlvbl9pZGVudGlmaWVyIjogeyJ0eXBlIjogInN0cmluZyIsICJ0aXRsZSI6ICJXSUdPUyBTdGF0aW9uIElkZW50aWZpZXIiLCAiZGVzY3JpcHRpb24iOiAiRmlsdGVyIGJ5IFdJR09TIFN0YXRpb24gSWRlbnRpZmllciJ9fSwgInRpdGxlIjogIk5vdGlmaWNhdGlvbnMifSwgeyJocmVmIjogImh0dHA6Ly9sb2NhbGhvc3QvbWV0YWRhdGEvZGF0YS91cm46d21vOm1kOmJyLWlubWV0OnJyMWllcS5qc29uIiwgInR5cGUiOiAiYXBwbGljYXRpb24vZ2VvK2pzb24iLCAibmFtZSI6ICJ1cm46d21vOm1kOmJyLWlubWV0OnJyMWllcSIsICJyZWwiOiAiY2Fub25pY2FsIiwgInRpdGxlIjogInVybjp3bW86bWQ6YnItaW5tZXQ6cnIxaWVxIn1dfQ==",
         "size":1957
      }
   },
   "links":[
      {
         "rel":"canonical",
         "type":"application/geo+json",
         "href":"http://localhost/data/metadata/urn:wmo:md:br-inmet:rr1ieq.json",
         "length":1957
      }
   ],
   "generated_by":"wis2box 1.2.0"
}
```

在本次实践课程中，您将学习如何使用 MQTT Explorer 工具设置一个 MQTT 客户端连接到 WIS2 Global Broker，并能够显示 WIS2 通知消息。

MQTT Explorer 是一个有用的工具，可以浏览和查看指定 MQTT broker 的主题结构，以审查正在发布的数据。

!!! note "关于 MQTT"
    MQTT Explorer 提供了一个用户友好的界面，用于连接到 MQTT broker 并探索 WIS2 使用的主题和消息结构。
    
    实际上，MQTT 旨在用于机器与机器之间的通信，其中一个应用程序或服务订阅主题并以编程方式实时处理消息。
    
    要以编程方式使用 MQTT（例如，在 Python 中），您可以使用 MQTT 客户端库，例如 [paho-mqtt](https://pypi.org/project/paho-mqtt)，连接到 MQTT broker 并处理传入的消息。根据您的需求和技术环境，还存在许多 MQTT 客户端和服务器软件。

## 使用 MQTT Explorer 连接到 Global Broker

要查看 WIS2 Global Broker 发布的消息，可以使用 "MQTT Explorer"，可从 [MQTT Explorer 网站](https://mqtt-explorer.com) 下载。

打开 MQTT Explorer，并添加一个新的连接到由 MeteoFrance 托管的 Global Broker，使用以下详细信息：

- host: globalbroker.meteo.fr
- port: 8883
- username: everyone
- password: everyone

<img alt="mqtt-explorer-global-broker-connection" src="/../assets/img/mqtt-explorer-global-broker-connection.png" width="800">

点击 'ADVANCED' 按钮，移除预配置的主题，并添加以下主题以订阅：

- `origin/a/wis2/#`

<img alt="mqtt-explorer-global-broker-advanced" src="/../assets/img/mqtt-explorer-global-broker-sub-origin.png" width="800">

!!! note
    设置 MQTT 订阅时，您可以使用以下通配符：

    - **单层通配符 (+)**：单层通配符替代一个主题层级
    - **多层通配符 (#)**：多层通配符替代多个主题层级

    在此情况下，`origin/a/wis2/#` 将订阅 `origin/a/wis2` 主题下的所有主题。

点击 'BACK'，然后点击 'SAVE' 保存您的连接和订阅详细信息。然后点击 'CONNECT'：

消息应开始出现在您的 MQTT Explorer 会话中，如下所示：

<img alt="mqtt-explorer-global-broker-topics" src="/../assets/img/mqtt-explorer-global-broker-msg-origin.png" width="800">

现在，您可以开始探索 WIS2 的主题和消息结构。

## 练习 1：查看 WIS2 的主题结构

使用 MQTT 浏览 `origin` 主题下的主题结构。

!!! question
    
    我们如何区分发布数据的 WIS 中心？

??? success "点击查看答案"

    您可以点击 MQTT Explorer 左侧窗口，展开主题结构。
    
    我们可以通过查看主题结构的第四层来区分发布数据的 WIS 中心。例如，以下主题：

    `origin/a/wis2/br-inmet/data/core/weather/surface-based-observations/synop`

    告诉我们数据是由中心 ID 为 `br-inmet` 的 WIS 中心发布的，这是巴西 Instituto Nacional de Meteorologia - INMET 的中心 ID。

!!! question

    我们如何区分由托管 GTS-to-WIS2 网关的 WIS 中心发布的消息和由托管 WIS2 节点的 WIS 中心发布的消息？

??? success "点击查看答案"

    我们可以通过查看主题结构中的中心 ID 来区分来自 GTS-to-WIS2 网关的消息。例如，以下主题：

    `origin/a/wis2/de-dwd-gts-to-wis2/data/core/I/S/A/I/01/sbbr`

    告诉我们数据是由德国 Deutscher Wetterdienst (DWD) 托管的 GTS-to-WIS2 网关发布的。GTS-to-WIS2 网关是一种特殊类型的数据发布者，它将来自全球电信系统 (GTS) 的数据发布到 WIS2。主题结构由 GTS 消息的 TTAAii CCCC 标头组成。

## 练习 2：查看 WIS2 的消息结构

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

    数据发布的时间戳包含在消息的 `properties` 部分，其键为 `pubtime`。

    数据收集的时间戳包含在消息的 `properties` 部分，其键为 `datetime`。

    <img alt="mqtt-explorer-global-broker-msg-properties" src="/../assets/img/mqtt-explorer-global-broker-msg-properties.png" width="800">

!!! question

    我们如何从消息中提供的 URL 下载数据？

??? success "点击查看答案"

    URL 包含在 `links` 部分，其 `rel="canonical"` 并由 `href` 键定义。

    您可以复制该 URL 并将其粘贴到网络浏览器中以下载数据。

## 练习 3：查看 'origin' 和 'cache' 主题之间的区别

确保您仍然使用练习 2 中描述的主题订阅 `origin/a/wis2/+/data/core/weather/surface-based-observations/synop` 和 `cache/a/wis2/+/data/core/weather/surface-based-observations/synop` 连接到 Global Broker。

尝试识别由相同中心 ID 发布的消息，这些消息分别出现在 `origin` 和 `cache` 主题中。

!!! question

    发布在 `origin` 和 `cache` 主题上的消息有什么区别？

??? success "点击查看答案"

    发布在 `origin` 主题上的消息是 Global Broker 从网络中的 WIS2 节点重新发布的原始消息。

    发布在 `cache` 主题上的消息是 Global Cache 下载的数据的消息。如果您检查从以 `cache` 开头的主题发布的消息内容，您会发现 'canonical' 链接已更新为一个新的 URL。
    
    在 WIS2 网络中有多个 Global Cache，因此您将从每个下载了消息的 Global Cache 收到一条消息。

    Global Cache 仅下载并重新发布发布在 `../data/core/...` 主题层级上的消息。

## 总结

!!! success "恭喜！"
    在本次实践课程中，您学习了：

    - 如何使用 MQTT Explorer 订阅 WIS2 Global Broker 服务
    - WIS2 的主题结构
    - WIS2 的通知消息结构
    - 核心数据和推荐数据之间的区别
    - GTS-to-WIS2 网关使用的主题结构
    - 发布在 `origin` 和 `cache` 主题上的 Global Broker 消息之间的区别
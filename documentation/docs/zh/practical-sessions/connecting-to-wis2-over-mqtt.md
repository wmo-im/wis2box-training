---
title: 通过 MQTT 连接到 WIS2
---

# 通过 MQTT 连接到 WIS2

!!! abstract "学习成果"

    通过本实践课程，您将能够：

    - 使用 MQTT Explorer 连接到 WIS2 全球代理
    - 查看 WIS2 主题结构
    - 查看 WIS2 通知消息结构

## 引言

WIS2 使用 MQTT 协议来宣传天气/气候/水数据的可用性。WIS2 全球代理订阅网络中所有 WIS2 节点的消息，并重新发布它接收到的消息。全球缓存订阅全球代理，下载消息中的数据，然后在 `cache` 主题上用新的 URL 重新发布消息。全球发现目录从代理发布发现元数据并提供搜索 API。

这是一个在主题 `origin/a/wis2/br-inmet/data/core/weather/surface-based-observations/synop` 上接收到的 WIS2 通知消息结构的示例：

```json
{
  "id": "59f9b013-c4b3-410a-a52d-fff18f3f1b47",
  "type": "Feature",
  "version": "v04",
  "geometry": {
    "coordinates": [
      -38.69389,
      -17.96472,
      60
    ],
    "type": "Point"
  },
  "properties": {
    "data_id": "br-inmet/data/core/weather/surface-based-observations/synop/WIGOS_0-76-2-2900801000W83499_20240815T060000",
    "datetime": "2024-08-15T06:00:00Z",
    "pubtime": "2024-08-15T09:52:02Z",
    "integrity": {
      "method": "sha512",
      "value": "TBuWycx/G0lIiTo47eFPBViGutxcIyk7eikppAKPc4aHgOmTIS5Wb9+0v3awMOyCgwpFhTruRRCVReMQMp5kYw=="
    },
    "content": {
      "encoding": "base64",
      "value": "QlVGUgAA+gQAABYAACsAAAAAAAIAHAAH6AgPBgAAAAALAAABgMGWx1AAAM0ABOIAAAODM0OTkAAAAAAAAAAAAAAKb5oKEpJ6YkJ6mAAAAAAAAAAAAAAAAv0QeYA29WQa87ZhH4CQP//z+P//BD////+ASznXuUb///8MgAS3/////8X///e+AP////AB/+R/yf////////////////////6/1/79H/3///gEt////////4BLP6QAf/+/pAB//4H0YJ/YeAh/f2///7TH/////9+j//f///////////////////v0f//////////////////////wNzc3Nw==",
      "size": 250
    },
    "wigos_station_identifier": "0-76-2-2900801000W83499"
  },
  "links": [
    {
      "rel": "canonical",
      "type": "application/bufr",
      "href": "http://wis2bra.inmet.gov.br/data/2024-08-15/wis/br-inmet/data/core/weather/surface-based-observations/synop/WIGOS_0-76-2-2900801000W83499_20240815T060000.bufr4",
      "length": 250
    }
  ]
}
``` 

在本实践课程中，您将学习如何使用 MQTT Explorer 工具设置 MQTT 客户端连接到 WIS2 全球代理，并能够显示 WIS2 通知消息。

MQTT Explorer 是一个有用的工具，用于浏览和查看给定 MQTT 代理的主题结构以及正在发布的数据。

请注意，MQTT 主要用于“机器对机器”的通信；这意味着通常会有一个客户端自动解析接收到的消息。要以编程方式使用 MQTT（例如，在 Python 中），您可以使用 MQTT 客户端库，如 [paho-mqtt](https://pypi.org/project/paho-mqtt)，连接到 MQTT 代理并处理传入消息。根据您的需求和技术环境，存在许多 MQTT 客户端和服务器软件。

## 使用 MQTT Explorer 连接到全球代理

要查看由 WIS2 全球代理发布的消息，您可以使用“MQTT Explorer”，该工具可以从 [MQTT Explorer 网站](https://mqtt-explorer.com)下载。

打开 MQTT Explorer 并使用以下详细信息添加新连接到由 MeteoFrance 托管的全球代理：

- 主机：globalbroker.meteo.fr
- 端口：8883
- 用户名：everyone
- 密码：everyone

<img alt="mqtt-explorer-global-broker-connection" src="/../assets/img/mqtt-explorer-global-broker-connection.png" width="800">

点击 'ADVANCED' 按钮，删除预配置的主题并添加以下主题进行订阅：

- `origin/a/wis2/#`

<img alt="mqtt-explorer-global-broker-advanced" src="/../assets/img/mqtt-explorer-global-broker-sub-origin.png" width="800">

!!! note
    设置 MQTT 订阅时，您可以使用以下通配符：

    - **单级 (+)**：单级通配符替换一个主题级别
    - **多级 (#)**：多级通配符替换多个主题级别

    在这种情况下，`origin/a/wis2/#` 将订阅 `origin/a/wis2` 主题下的所有主题。

点击 'BACK'，然后 'SAVE' 保存您的连接和订阅详情。然后点击 'CONNECT'：

消息应该开始在您的 MQTT Explorer 会话中出现，如下所示：

<img alt="mqtt-explorer-global-broker-topics" src="/../assets/img/mqtt-explorer-global-broker-msg-origin.png" width="800">

现在您已经准备好开始探索 WIS2 的主题和消息结构。

## 练习 1：查看 WIS2 主题结构

使用 MQTT 浏览 `origin` 主题下的主题结构。

!!! question
    
    我们如何区分发布数据的 WIS 中心？

??? success "点击以显示答案"

    您可以点击 MQTT Explorer 中左侧窗口以展开主题结构。
    
    我们可以通过查看主题结构的第四级来区分发布数据的 WIS 中心。例如，以下主题：

    `origin/a/wis2/br-inmet/data/core/weather/surface-based-observations/synop`

    告诉我们数据是由巴西国家气象学院 - INMET 发布的，中心 ID 为 `br-inmet`。

!!! question

    我们如何区分由托管 GTS 到 WIS2 网关的 WIS 中心发布的消息和由托管 WIS2 节点的 WIS 中心发布的消息？

??? success "点击以显示答案"

    我们可以通过查看主题结构中的中心 ID 来区分来自 GTS 到 WIS2 网关的消息。例如，以下主题：

    `origin/a/wis2/de-dwd-gts-to-wis2/data/core/I/S/A/I/01/sbbr`

    告诉我们数据是由德国气象局 (DWD) 托管的 GTS 到 WIS2 网关发布的。GTS 到 WIS2 网关是一种特殊类型的数据发布者，它将全球电信系统 (GTS) 的数据发布到 WIS2。主题结构由 GTS 消息的 TTAAii CCCC 头组成。

## 练习 2：查看 WIS2 消息结构

从 MQTT Explorer 断开连接并更新 'Advanced' 部分以更改订阅为以下内容：

* `origin/a/wis2/+/data/core/weather/surface-based-observations/synop`
* `cache/a/wis2/+/data/core/weather/surface-based-observations/synop`

<img alt="mqtt-explorer-global-broker-topics-exercise2" src="/../assets/img/mqtt-explorer-global-broker-sub-origin-cache-synop.png" width="800">

!!! note
    `+` 通配符用于订阅所有 WIS 中心。

重新连接到全球代理并等待消息出现。

您可以在右侧的“Value”部分查看 WIS2 消息的内容。尝试展开主题结构以查看消息的不同级别，直到您到达最后一级并查看其中一条消息的消息内容。

!!! question

    我们如何识别数据发布的时间戳？我们又如何识别数据收集的时间戳？

??? success "点击以显示答案"

    数据发布的时间戳包含在消息的 `properties` 部分，键为 `pubtime`。

    数据收集的时间戳包含在消息的 `properties` 部分，键为 `datetime`。

    <img alt="mqtt-explorer-global-broker-msg-properties" src="/../assets/img/mqtt-explorer-global-broker-msg-properties.png" width="800">

!!! question

    我们如何从消息中提供的 URL 下载数据？

??? success "点击以显示答案"

    URL 包含在 `links` 部分，`rel="canonical"` 并由 `href` 键定义。

    您可以复制 URL 并将其粘贴到网络浏览器中以下载数据。

## 练习 3：查看 'origin' 和 'cache' 主题之间的区别

确保您仍然使用在练习 2 中描述的主题订阅 `origin/a/wis2/+/data/core/weather/surface-based-observations/synop` 和 `cache/a/wis2/+/data/core/weather/surface-based-observations/synop` 连接到全球代理。

尝试识别在 `origin` 和 `cache` 主题上发布的同一中心 ID 的消息。

!!! question

    发布在 `origin` 和 `cache` 主题上的消息有什么区别？

??? success "点击以显示答案"

    发布在 `origin` 主题上的消息是全球代理从 WIS2 节点网络中重新发布的原始消息。

    发布在 `cache` 主题上的消息是全球缓存下载的数据的消息。如果您检查以 `cache` 开头的主题的消息内容，您会看到 'canonical' 链接已更新为新的 URL。
    
    WIS2 网络中有多个全球缓存，因此您将收到每个下载了该消息的全球缓存的一条消息。

    全球缓存只会下载并重新发布在 `../data/core/...` 主题层次结构上发布的消息。

## 结论

!!! success "恭喜！"
    在这个实践课程中，您学到了：

    - 如何使用 MQTT Explorer 订阅 WIS2 全球代理服务
    - WIS2 主题结构
    - WIS2 通知消息结构
    - 核心数据和推荐数据的区别
    - GTS 到 WIS2 网关使用的主题结构
    - 全球代理在 `origin` 和 `cache` 主题上发布的消息的区别
---
title: 使用wis2box API查询数据
---

# 使用wis2box API查询数据

!!! abstract "学习目标"
    完成本实践课程后，您将能够：

    - 使用wis2box API查询和过滤站点信息
    - 使用wis2box API查询和过滤数据

## 简介

wis2box API以机器可读的方式提供对已导入wis2box的数据的发现和查询访问。该API基于OGC API - Features标准，并使用[pygeoapi](https://pygeoapi.io)实现。

wis2box API提供对以下集合的访问：

- 站点
- 发现元数据
- 数据通知
- 每个配置的数据集都有一个集合，用于存储bufr2geojson的输出（需要在数据映射配置中启用`bufr2geojson`插件才能填充数据集集合中的项目）。

在本实践课程中，您将学习如何使用数据API浏览和查询已导入wis2box的数据。

## 准备工作

!!! note
    在网络浏览器中导航到wis2box API登录页面：

    `http://YOUR-HOST/oapi`

<img alt="wis2box-api-landing-page" src="/../assets/img/wis2box-api-landing-page.png" width="600">

## 检查集合

从登录页面，点击"Collections"链接。

!!! question
    在结果页面中看到多少个数据集集合？您认为每个集合代表什么？

??? success "点击查看答案"
    应该显示4个集合，包括"Stations"、"Discovery metadata"和"Data notifications"

## 检查站点

从登录页面，点击"Collections"链接，然后点击"Stations"链接。

<img alt="wis2box-api-collections-stations" src="/../assets/img/wis2box-api-collections-stations.png" width="600">

点击"Browse"链接，然后点击"json"链接。

!!! question
    返回了多少个站点？将这个数字与`http://YOUR-HOST/wis2box-webapp/station`中的站点列表进行比较

??? success "点击查看答案"
    API返回的站点数量应该等于您在wis2box webapp中看到的站点数量。

!!! question
    我们如何查询单个站点（例如`Balaka`）？

??? success "点击查看答案"
    使用`http://YOUR-HOST/oapi/collections/stations/items?q=Balaka`查询API。

!!! note
    上述示例基于马拉维测试数据。请尝试针对您在之前练习中导入的站点进行测试。

## 检查观测数据

!!! note
    上述示例基于马拉维测试数据。请尝试针对您在练习中导入的观测数据进行测试。

从登录页面，点击"Collections"链接，然后点击"Surface weather observations from Malawi"链接。

<img alt="wis2box-api-collections-malawi-obs" src="/../assets/img/wis2box-api-collections-malawi-obs.png" width="600">

点击"Queryables"链接。

<img alt="wis2box-api-collections-malawi-obs-queryables" src="/../assets/img/wis2box-api-collections-malawi-obs-queryables.png" width="600">

!!! question
    使用哪个查询参数可以按站点标识符进行过滤？

??? success "点击查看答案"
    `wigos_station_identifer`是正确的查询参数。

返回上一页（即`http://YOUR-HOST/oapi/collections/urn:wmo:md:mwi:mwi_met_centre:surface-weather-observations`）

点击"Browse"链接。

!!! question
    我们如何可视化JSON响应？

??? success "点击查看答案"
    通过点击页面右上角的"JSON"链接，或在网络浏览器的API请求中添加`f=json`。

检查观测数据的JSON响应。

!!! question
    返回了多少条记录？

!!! question
    我们如何将响应限制为3条观测记录？

??? success "点击查看答案"
    在API请求中添加`limit=3`。

!!! question
    我们如何按最新观测数据对响应进行排序？

??? success "点击查看答案"
    在API请求中添加`sortby=-resultTime`（注意`-`符号表示降序排序）。要按最早的观测数据排序，请在请求中包含`sortby=resultTime`。

!!! question
    我们如何按单个站点过滤观测数据？

??? success "点击查看答案"
    在API请求中添加`wigos_station_identifier=<WSI>`。

!!! question
    我们如何以CSV格式接收观测数据？

??? success "点击查看答案"
    在API请求中添加`f=csv`。

!!! question
    我们如何显示单个观测记录（id）？

??? success "点击查看答案"
    使用观测数据API请求中的要素标识符，查询API`http://YOUR-HOST/oapi/collections/{collectionId}/items/{featureId}`，其中`{collectionId}`是您的观测数据集合的名称，`{itemId}`是感兴趣的单个观测记录的标识符。

## 总结

!!! success "恭喜！"
    在本实践课程中，您学会了如何：

    - 使用wis2box API查询和过滤站点信息
    - 使用wis2box API查询和过滤数据
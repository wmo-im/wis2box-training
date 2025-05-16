---
title: 配置站点元数据
---

# 配置站点元数据

!!! abstract "学习目标"

    完成本实践课程后，您将能够：

    - 为 `collections/stations` 端点创建授权令牌
    - 向 wis2box 添加站点元数据 
    - 使用 **wis2box-webapp** 更新/删除站点元数据

## 简介

为了在 WMO 成员之间进行国际数据共享，对产生数据的站点有共同的理解非常重要。WMO 综合全球观测系统(WIGOS)为观测系统和数据管理系统的整合提供了框架。**WIGOS 站点标识符(WSI)** 用作产生特定观测数据的站点的唯一参考。

wis2box 包含一个站点元数据集合,用于描述产生观测数据的站点,这些元数据应从 **OSCAR/Surface** 中获取。wis2box 中的站点元数据被 BUFR 转换工具用来检查输入数据是否包含有效的 WIGOS 站点标识符(WSI),并提供 WSI 与站点元数据之间的映射。

## 为 collections/stations 创建授权令牌

要通过 **wis2box-webapp** 编辑站点,您首先需要创建一个授权令牌。

登录到您的学生虚拟机并确保您在 `wis2box` 目录中:

```bash
cd ~/wis2box
```

然后使用以下命令登录到 **wis2box-management** 容器:

```bash
python3 wis2box-ctl.py login
```

在 **wis2box-management** 容器中,您可以使用命令为特定端点创建授权令牌: `wis2box auth add-token --path <my-endpoint>`。

例如,要为 `collections/stations` 端点使用随机生成的令牌:

```{.copy}
wis2box auth add-token --path collections/stations
```

输出将如下所示:

```{.copy}
Continue with token: 7ca20386a131f0de384e6ffa288eb1ae385364b3694e47e3b451598c82e899d1 [y/N]? y
Token successfully created
```

或者,如果您想为 `collections/stations` 端点定义自己的令牌,可以使用以下示例:

```{.copy}
wis2box auth add-token --path collections/stations DataIsMagic
```

输出:
    
```{.copy}
Continue with token: DataIsMagic [y/N]? y
Token successfully created
```

请按照上述说明为 `collections/stations` 端点创建授权令牌。

## 使用 **wis2box-webapp** 添加站点元数据

**wis2box-webapp** 提供了一个图形用户界面来编辑站点元数据。

在浏览器中打开 **wis2box-webapp**,导航到 `http://YOUR-HOST/wis2box-webapp`,并选择站点:

<img alt="wis2box-webapp-select-stations" src="/../assets/img/wis2box-webapp-select-stations.png" width="250">

当您点击"添加新站点"时,系统会要求您提供要添加的站点的 WIGOS 站点标识符:

<img alt="wis2box-webapp-import-station-from-oscar" src="/../assets/img/wis2box-webapp-import-station-from-oscar.png" width="800">

!!! note "添加 3 个或更多站点的元数据"
    请为您的 wis2box 的站点元数据集合添加三个或更多站点。
      
    如果可能,请使用您所在国家的站点,特别是如果您带来了自己的数据。
      
    如果您的国家在 OSCAR/Surface 中没有任何站点,您可以使用以下站点进行练习:

      - 0-20000-0-91334
      - 0-20000-0-96323 (注意 OSCAR 中缺少站点海拔)
      - 0-20000-0-96749 (注意 OSCAR 中缺少站点海拔)

当您点击搜索时,系统会从 OSCAR/Surface 检索站点数据,请注意这可能需要几秒钟。

检查 OSCAR/Surface 返回的数据,并在需要时添加缺失的数据。为站点选择一个主题,提供您的 `collections/stations` 端点的授权令牌,然后点击"保存":

<img alt="wis2box-webapp-create-station-save" src="/../assets/img/wis2box-webapp-create-station-save.png" width="800">

<img alt="wis2box-webapp-create-station-success" src="/../assets/img/wis2box-webapp-create-station-success.png" width="500">

返回站点列表,您将看到您添加的站点:

<img alt="wis2box-webapp-stations-with-one-station" src="/../assets/img/wis2box-webapp-stations-with-one-station.png" width="800">

重复此过程,直到您配置了至少 3 个站点。

!!! tip "获取缺失的海拔信息"

    如果您的站点海拔缺失,可以使用在线服务通过开放海拔数据查找海拔。一个这样的例子是 [Open Topo Data API](https://www.opentopodata.org)。

    例如,要获取纬度 -6.15558 和经度 106.84204 的海拔,您可以在新的浏览器标签中复制粘贴以下 URL:

    ```{.copy}
    https://api.opentopodata.org/v1/aster30m?locations=-6.15558,106.84204
    ```

    输出:

    ```{.copy}
    {
      "results": [
        {
          "dataset": "aster30m", 
          "elevation": 7.0, 
          "location": {
            "lat": -6.15558, 
            "lng": 106.84204
          }
        }
      ], 
      "status": "OK"
    }
    ```

## 检查您的站点元数据

站点元数据存储在 wis2box 的后端,并通过 **wis2box-api** 提供访问。

如果您打开浏览器并导航到 `http://YOUR-HOST/oapi/collections/stations/items`,您将看到您添加的站点元数据:

<img alt="wis2box-api-stations" src="/../assets/img/wis2box-api-stations.png" width="800">

!!! note "检查您的站点元数据"

    通过在浏览器中访问 `http://YOUR-HOST/oapi/collections/stations/items` 验证您添加的站点是否与您的数据集关联。

您还可以在 **wis2box-webapp** 中查看/更新/删除站点。请注意,要更新/删除站点,您需要提供 `collections/stations` 端点的授权令牌。

!!! note "更新/删除站点元数据"

    尝试使用 **wis2box-webapp** 更新/删除您添加的其中一个站点的元数据。

## 批量站点元数据上传

请注意,wis2box 还可以使用 **wis2box-management** 容器中的命令行从 CSV 文件执行站点元数据的"批量"加载。

```bash
python3 wis2box-ctl.py login
wis2box metadata station publish-collection -p /data/wis2box/metadata/station/station_list.csv -th origin/a/wis2/centre-id/weather/surface-based-observations/synop
```

这允许您一次上传大量站点并将它们与特定主题关联。

您可以使用 Excel 或文本编辑器创建 CSV 文件,然后将其上传到 wis2box-host-datadir,使其在 `/data/wis2box/` 目录中对 **wis2box-management** 容器可用。

批量上传站点后,建议在 **wis2box-webapp** 中检查站点,以确保数据上传正确。

有关如何使用此功能的更多信息,请参阅官方 [wis2box 文档](https://docs.wis2box.wis.wmo.int)。

## 结论

!!! success "恭喜!"
    在本实践课程中,您学会了如何:

    - 为 `collections/stations` 端点创建授权令牌以用于 **wis2box-webapp**
    - 使用 **wis2box-webapp** 向 wis2box 添加站点元数据
    - 使用 **wis2box-webapp** 查看/更新/删除站点元数据
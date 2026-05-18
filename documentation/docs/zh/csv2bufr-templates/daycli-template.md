---
title: DAYCLI 模板
---

# 用于每日气候数据的 csv2bufr 模板 (DAYCLI)

**DAYCLI** 模板提供了一种标准化的 CSV 格式，用于将每日气候数据转换为 BUFR 序列 307075。

该格式旨在与气候数据管理系统一起使用，以支持 WIS2 上的数据发布，满足每日气候观测的报告要求。

此模板映射了以下每日观测数据：

- 24 小时内的最低、最高和平均温度
- 24 小时内的累计降水量
- 观测时的总积雪深度
- 24 小时内的新积雪深度

与简化的 AWS 模板相比，此模板需要额外的元数据：平均温度的计算方法；传感器和站点的高度；暴露条件和测量质量分类。

!!! 注意 "关于 DAYCLI 模板"
    请注意，DAYCLI BUFR 序列将在 2026 年更新，以包含更多信息和修订的质量控制标志。包含在 wis2box 中的 DAYCLI 模板将会更新以反映这些变化。WMO 将在 wis2box 软件更新以包含新的 DAYCLI 模板时进行通知，以便用户相应地更新其系统。

## CSV 列及描述

{{ read_csv("docs/assets/tables/daycli-table.csv") }}

## 平均计算方法

{{ read_csv("docs/assets/tables/averaging-method-table.csv") }}

## 质量标志

{{ read_csv("docs/assets/tables/quality_flag.csv") }}

## 站点分类参考

[温度站点分类参考](https://library.wmo.int/idviewer/35625/839)。

[降水站点分类参考](https://library.wmo.int/idviewer/35625/840)。

## 示例

符合 DAYCLI 模板的示例 CSV 文件：[daycli-example.csv](../../sample-data/daycli-example.csv)。
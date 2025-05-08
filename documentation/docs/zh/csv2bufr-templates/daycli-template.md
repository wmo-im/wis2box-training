---
title: DAYCLI 模板
---

# 日常气候数据的 csv2bufr 模板（DAYCLI）

**DAYCLI** 模板提供了一个标准化的 CSV 格式，用于将日常气候数据转换为 BUFR 序列 307075。

该格式旨在与气候数据管理系统一起使用，以支持在 WIS2 上发布数据，以满足日常气候观测的报告要求。

此模板映射了每日观测数据：

 - 24小时内的最低、最高和平均温度
 - 24小时内的总降水量
 - 观测时的总积雪深度
 - 24小时内的新雪深度

此模板需要额外的元数据，相对于简化的 AWS-模板：计算平均温度的方法；传感器和站点高度；暴露和测量质量分类。

!!! 注意 "关于 DAYCLI 模板"
    请注意，DAYCLI BUFR 序列将在 2025 年更新，以包括额外信息和修订的质量控制标志。包含在 wis2box 中的 DAYCLI 模板将更新以反映这些变化。WMO 将通知何时更新 wis2box-软件以包含新的 DAYCLI 模板，以便用户相应更新其系统。

## CSV 列和描述

{{ read_csv("docs/assets/tables/daycli-table.csv") }}

## 平均方法

{{ read_csv("docs/assets/tables/averaging-method-table.csv") }}

## 质量标志

{{ read_csv("docs/assets/tables/quality_flag.csv") }}

## 定位分类参考

[“温度定位分类”参考资料](https://library.wmo.int/idviewer/35625/839)。

[“降水定位分类”参考资料](https://library.wmo.int/idviewer/35625/840)。

## 示例

符合 DAYCLI 模板的示例 CSV 文件：[daycli-example.csv](./../../sample-data/daycli-example.csv)。
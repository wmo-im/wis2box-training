---
title: CLIMAT 模板
---

# 用于每日气候数据（CLIMAT）的 csv2bufr 模板

**CLIMAT** 报文报告由天气和气候观测站每日观测数据汇总的月度气候摘要，用于支持气候监测、研究和存档。

CLIMAT 模板提供了一种标准化的 CSV 格式，用于生成符合 BUFR 格式的 CLIMAT 报文，适用于序列 301150,307073。

## CSV 列及描述

{{ read_csv("docs/assets/tables/climat-table.csv") }}

## 示例

符合 CLIMAT 模板的示例 CSV 文件：[climat-example.csv](../../sample-data/climat-example.csv)。
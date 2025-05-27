---
title: AWS 模板
---

# 用于报告每小时 GBON 数据的自动气象站的 csv2bufr 模板

**AWS 模板**使用标准化的 CSV 格式来接收自动气象站的数据，以支持 GBON 报告要求。此映射模板将 CSV 数据转换为 BUFR 序列 301150、307096。

该格式旨在用于自动气象站，每小时报告最少数量的参数，包括气压、气温和湿度、风速和风向以及降水量。

## CSV 列及说明

{{ read_csv("docs/assets/tables/aws-minimal.csv") }}

## 示例

符合 AWS 模板的示例 CSV 文件：[aws-example.csv](../sample-data/aws-example.csv)。
---
title: WIS2 in a box 速查表
---

# WIS2 in a box 速查表

## 概述

wis2box 作为一组 Docker Compose 命令运行。``wis2box-ctl.py`` 是一个实用工具（用 Python 编写），可以方便地运行 Docker Compose 命令。

## wis2box 命令要点

### 启动和停止

* 启动 wis2box：

```bash
python3 wis2box-ctl.py start
```

* 停止 wis2box：

```bash
python3 wis2box-ctl.py stop
```

* 验证所有 wis2box 容器是否正在运行：

```bash
python3 wis2box-ctl.py status
```

* 登录到一个 wis2box 容器（默认是 *wis2box-management*）：

```bash
python3 wis2box-ctl.py login
```

* 登录到一个特定的 wis2box 容器：

```bash
python3 wis2box-ctl.py login wis2box-api
```
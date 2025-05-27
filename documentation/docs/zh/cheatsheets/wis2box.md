---
title: WIS2 盒装版速查表
---

# WIS2 盒装版速查表

## 概览

wis2box 通过一系列 Docker Compose 命令运行。``wis2box-ctl.py`` 命令是一个工具
（用 Python 编写），用于轻松运行 Docker Compose 命令。

## wis2box 命令要点

### 启动与停止

* 启动 wis2box：

```bash
python3 wis2box-ctl.py start
```

* 停止 wis2box：

```bash
python3 wis2box-ctl.py stop
```

* 验证所有 wis2box 容器是否在运行：

```bash
python3 wis2box-ctl.py status
```

* 登录到一个 wis2box 容器（默认为 *wis2box-management*）：

```bash
python3 wis2box-ctl.py login
```

* 登录到特定的 wis2box 容器：

```bash
python3 wis2box-ctl.py login wis2box-api
```
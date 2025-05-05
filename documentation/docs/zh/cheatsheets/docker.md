---
title: Docker 速查表
---

# Docker 速查表

## 概述

Docker 允许以隔离的方式创建虚拟环境，支持计算资源的虚拟化。Docker 背后的基本概念是容器化，
其中软件可以作为服务运行，例如与其他软件容器互动。

典型的 Docker 工作流程包括创建和构建**镜像**，然后将其作为活动的**容器**运行。

Docker 用于使用预构建的镜像运行组成 wis2box 的服务套件。

### 镜像管理

* 列出可用的镜像

```bash
docker image ls
```

* 更新镜像：

```bash
docker pull my-image:latest
```

* 删除镜像：

```bash
docker rmi my-image:local
```

### 卷管理

* 列出所有创建的卷：

```bash
docker volume ls
```

* 显示卷的详细信息：

```bash
docker volume inspect my-volume
```

* 删除卷：

```bash
docker volume rm my-volume
```

* 删除所有未使用的卷：

```bash
docker volume prune
```

### 容器管理

* 显示当前运行的容器列表：

```bash
docker ps
```

* 列出所有容器：

```bash
docker ps -a
```

* 进入运行中容器的交互式终端：


!!! 提示

    使用 `docker ps` 在下面的命令中使用容器 id

```bash
docker exec -it my-container /bin/bash
```

* 删除容器

```bash
docker rm my-container
```

* 删除正在运行的容器：

```bash
docker rm -f my-container
```

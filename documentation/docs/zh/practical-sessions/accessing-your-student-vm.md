---
title: 访问你的学生虚拟机
---

# 访问你的学生虚拟机

!!! abstract "学习目标"

    在本次实践课程结束时，你将能够：

    - 通过 SSH 和 WinSCP 访问你的学生虚拟机
    - 验证实践所需的软件是否已安装
    - 验证你是否可以在本地学生虚拟机上访问本次培训的练习材料

## 简介

作为本地运行的 WIS2 培训工作坊的一部分，你可以通过名为 "WIS2-training" 的本地培训网络访问你的个人学生虚拟机。

你的学生虚拟机已预安装以下软件：

- Ubuntu 22.04 LTS [ubuntu-22.04.5-live-server-amd64.iso](https://releases.ubuntu.com/jammy/ubuntu-22.04.5-live-server-amd64.iso)
- Python 3.10.12
- Docker 24.0.6
- Docker Compose 2.21.0
- 文本编辑器：vim、nano

!!! note

    如果你希望在本地培训课程之外运行本次培训，可以使用任何云服务提供商提供的实例，例如：

    - GCP (Google Cloud Platform) VM 实例 `e2-medium`
    - AWS (Amazon Web Services) ec2 实例 `t3a.medium`
    - Azure (Microsoft) Azure 虚拟机 `standard_b2s`

    选择 Ubuntu Server 22.0.4 LTS 作为操作系统。
    
    创建虚拟机后，请确保已安装 python、docker 和 docker compose，如 [wis2box-software-dependencies](https://docs.wis2box.wis.wmo.int/en/latest/user/getting-started.html#software-dependencies) 中所述。
    
    本次培训使用的 wis2box 发行版可以通过以下方式下载：

    ```bash
    wget https://github.com/World-Meteorological-Organization/wis2box-release/releases/download/1.2.0/wis2box-setup-1.2.0.zip
    unzip wis2box-setup-1.2.0.zip
    ```
    
    你可以随时在 [https://github.com/World-Meteorological-Organization/wis2box/releases](https://github.com/World-Meteorological-Organization/wis2box-release/releases) 找到最新的 'wis2box-setup' 归档文件。

    本次培训使用的练习材料可以通过以下方式下载：

    ```bash
    wget https://training.wis2box.wis.wmo.int/exercise-materials.zip
    unzip exercise-materials.zip
    ```

    运行练习材料需要安装以下额外的 Python 包：

    ```bash
    pip3 install minio
    pip3 install pywiscat==0.4.0
    ```

    如果你使用的是本地 WIS2 培训课程中提供的学生虚拟机，所需的软件已经预先安装。

## 在本地培训网络上连接到你的学生虚拟机

根据培训师提供的说明，将你的电脑连接到培训期间房间内广播的本地 Wi-Fi。

使用 SSH 客户端连接到你的学生虚拟机，连接信息如下：

- **主机名：（由现场培训提供）**
- **端口：22**
- **用户名：（由现场培训提供）**
- **密码：（由现场培训提供）**

!!! tip
    如果你不确定主机名或用户名，或者连接有问题，请联系培训师。

连接后，请更改密码以确保其他人无法访问你的虚拟机：

```bash
limper@student-vm:~$ passwd
Changing password for testuser.
Current password:
New password:
Retype new password:
passwd: password updated successfully
```

## 验证软件版本

为了运行 wis2box，学生虚拟机应预安装 Python、Docker 和 Docker Compose。

检查 Python 版本：
```bash
python3 --version
```
返回：
```console
Python 3.10.12
```

检查 Docker 版本：
```bash
docker --version
```
返回：
```console
Docker version 24.0.6, build ed223bc
```

检查 Docker Compose 版本：
```bash
docker compose version
```
返回：
```console
Docker Compose version v2.21.0
```

为了确保你的用户可以运行 Docker 命令，用户已被添加到 `docker` 组。

测试用户是否可以运行 Docker hello-world，执行以下命令：
```bash
docker run hello-world
```

此命令会拉取 hello-world 镜像并运行一个容器，打印一条消息。

检查输出中是否包含以下内容：

```console
...
Hello from Docker!
This message shows that your installation appears to be working correctly.
...
```

## 检查练习材料

检查你的主目录内容；这些是培训和实践课程中使用的材料。

```bash
ls ~/
```
返回：
```console
exercise-materials  wis2box
```

如果你的本地电脑安装了 WinSCP，可以使用它连接到学生虚拟机，检查主目录内容，并在虚拟机和本地电脑之间上传或下载文件。

虽然 WinSCP 不是培训的必需工具，但如果你希望使用本地电脑上的文本编辑器编辑虚拟机上的文件，它会非常有用。

以下是如何使用 WinSCP 连接到学生虚拟机：

打开 WinSCP 并点击 "New Site"。你可以创建一个新的 SCP 连接，设置如下：

<img alt="winscp-student-vm-scp.png" src="/../assets/img/winscp-student-vm-scp.png" width="400">

点击 'Save' 然后点击 'Login' 连接到你的虚拟机。

现在你应该可以看到学生虚拟机主目录的内容，并访问你的文件。

## 总结

!!! success "恭喜！"
    在本次实践课程中，你学会了：

    - 通过 SSH 和 WinSCP 访问你的学生虚拟机
    - 验证实践所需的软件是否已安装
    - 验证你是否可以在本地学生虚拟机上访问本次培训的练习材料
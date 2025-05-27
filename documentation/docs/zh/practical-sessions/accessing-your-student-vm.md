---
title: 访问您的学生虚拟机
---

# 访问您的学生虚拟机

!!! abstract "学习目标"

    完成本实践课程后，您将能够：

    - 通过 SSH 和 WinSCP 访问您的学生虚拟机
    - 验证实践练习所需的软件是否已安装
    - 验证您是否可以在本地学生虚拟机上访问此培训的练习材料

## 简介

作为本地运行的 wis2box 培训课程的一部分，您可以在名为"WIS2-training"的本地培训网络上访问您的个人学生虚拟机。

您的学生虚拟机预装了以下软件：

- Ubuntu 22.0.4.3 LTS [ubuntu-22.04.3-live-server-amd64.iso](https://releases.ubuntu.com/jammy/ubuntu-22.04.3-live-server-amd64.iso)
- Python 3.10.12
- Docker 24.0.6
- Docker Compose 2.21.0
- 文本编辑器：vim, nano

!!! note

    如果您想在本地培训课程之外进行此培训，您可以使用任何云服务提供商提供自己的实例，例如：

    - GCP (Google Cloud Platform) 虚拟机实例 `e2-medium`
    - AWS (Amazon Web Services) ec2实例 `t3a.medium`
    - Azure (Microsoft) Azure虚拟机 `standard_b2s`

    选择 Ubuntu Server 22.0.4 LTS 作为操作系统。
    
    创建虚拟机后，请确保已按照[wis2box-software-dependencies](https://docs.wis2box.wis.wmo.int/en/latest/user/getting-started.html#software-dependencies)中的说明安装了python、docker和docker compose。
    
    本培训中使用的 wis2box 发布包可以通过以下方式下载：

    ```bash
    wget https://github.com/World-Meteorological-Organization/wis2box-release/releases/download/1.0.0/wis2box-setup.zip
    unzip wis2box-setup.zip
    ```
    
    您可以在[https://github.com/World-Meteorological-Organization/wis2box/releases](https://github.com/World-Meteorological-Organization/wis2box-release/releases)找到最新的'wis2box-setup'压缩包。

    本培训使用的练习材料可以通过以下方式下载：

    ```bash
    wget https://training.wis2box.wis.wmo.int/exercise-materials.zip
    unzip exercise-materials.zip
    ```

    运行练习材料需要以下额外的Python包：

    ```bash
    pip3 install minio
    pip3 install pywiscat==0.2.2
    ```

    如果您使用的是本地WIS2培训课程期间提供的学生虚拟机，所需的软件将已经安装。

## 连接到本地培训网络上的学生虚拟机

按照培训讲师提供的说明，将您的PC连接到培训室内广播的本地Wi-Fi。

使用SSH客户端连接到您的学生虚拟机，使用以下信息：

- **主机：（在现场培训期间提供）**
- **端口：22**
- **用户名：（在现场培训期间提供）**
- **密码：（在现场培训期间提供）**

!!! tip
    如果您不确定主机名/用户名或连接有问题，请联系培训讲师。

连接后，请更改密码以确保其他人无法访问您的虚拟机：

```bash
limper@student-vm:~$ passwd
Changing password for testuser.
Current password:
New password:
Retype new password:
passwd: password updated successfully
```

## 验证软件版本

为了能够运行wis2box，学生虚拟机应该预装Python、Docker和Docker Compose。

检查Python版本：
```bash
python3 --version
```
返回：
```console
Python 3.10.12
```

检查docker版本：
```bash
docker --version
```
返回：
```console
Docker version 24.0.6, build ed223bc
```

检查Docker Compose版本：
```bash
docker compose version
```
返回：
```console
Docker Compose version v2.21.0
```

为确保您的用户可以运行Docker命令，您的用户已被添加到`docker`组。

要测试您的用户是否可以运行docker hello-world，请运行以下命令：
```bash
docker run hello-world
```

这应该会拉取hello-world镜像并运行一个打印消息的容器。

检查输出中是否包含以下内容：

```console
...
Hello from Docker!
This message shows that your installation appears to be working correctly.
...
```

## 检查练习材料

检查您的主目录内容；这些是培训和实践课程中使用的材料。

```bash
ls ~/
```
返回：
```console
exercise-materials  wis2box
```

如果您的本地PC上安装了WinSCP，您可以使用它连接到您的学生虚拟机并检查主目录的内容，以及在虚拟机和本地PC之间下载或上传文件。

WinSCP不是培训所必需的，但如果您想使用本地PC上的文本编辑器编辑虚拟机上的文件，它会很有用。

以下是如何使用WinSCP连接到您的学生虚拟机：

打开WinSCP并点击"New Site"。您可以按如下方式创建到虚拟机的新SCP连接：

<img alt="winscp-student-vm-scp.png" src="/../assets/img/winscp-student-vm-scp.png" width="400">

点击'Save'然后点击'Login'以连接到您的虚拟机。

您应该能够看到以下内容：

<img alt="winscp-student-vm-exercise-materials.png" src="/../assets/img/winscp-student-vm-exercise-materials.png" width="600">

## 结论

!!! success "恭喜！"
    在本实践课程中，您学会了如何：

    - 通过SSH和WinSCP访问您的学生虚拟机
    - 验证实践练习所需的软件是否已安装
    - 验证您是否可以在本地学生虚拟机上访问此培训的练习材料
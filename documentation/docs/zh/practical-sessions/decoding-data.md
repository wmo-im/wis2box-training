---
title: 从WMO二进制格式解码数据
---

# 从WMO二进制格式解码数据

!!! abstract "学习目标！"

    在本次实践课程结束时，您将能够：

    - 运行 "demo-decode-eccodes-jupyter" 镜像的 Docker 容器
    - 运行示例 Jupyter notebooks 来解码 GRIB2、NetCDF 和 BUFR 格式的数据
    - 了解其他用于解码和可视化 WMO 二进制格式的工具

## 介绍

WMO 二进制格式（如 BUFR 和 GRIB）广泛应用于气象领域，用于观测数据和模式数据的交换。这些格式需要专门的工具来解码和可视化数据。

从 WIS2 下载数据后，您通常需要解码这些数据以便使用。

目前有多种代码库可用于编写脚本或程序来解码 WMO 二进制格式。此外，还有一些工具提供了用户界面，无需编写代码即可解码和可视化数据。

在本次实践课程中，我们将通过 Jupyter notebook 演示如何解码三种不同类型的数据：

- GRIB2：包含 CMA 全球区域同化预报系统（GRAPES）生成的全球集合预报数据
- BUFR：包含 ECMWF 集合预报系统生成的热带气旋路径数据
- NetCDF：包含月度温度异常数据

## 在 Jupyter notebook 中解码下载的数据

为了演示如何解码下载的数据，我们将使用 'decode-bufr-jupyter' 镜像启动一个新容器。

该容器将在您的实例上启动一个 Jupyter notebook 服务器，其中包含用于解码 BUFR 数据的 "ecCodes" 库。

我们将使用 `~/exercise-materials/notebook-examples` 中的示例 notebooks 来解码热带气旋路径的下载数据。

启动容器的命令如下：

```bash
docker run -d --name demo-decode-eccodes-jupyter \
    -v ~/wis2box-data/downloads:/root/downloads \
    -p 8888:8888 \
    -e JUPYTER_TOKEN=dataismagic! \
    ghcr.io/wmo-im/wmo-im/demo-decode-eccodes-jupyter:latest
```

以下是该命令的功能说明：

- `docker run -d --name demo-decode-eccodes-jupyter`：以分离模式（`-d`）启动一个新容器，并将其命名为 `demo-decode-eccodes-jupyter`。
- `-v ~/wis2box-data/downloads:/root/downloads`：将虚拟机上的 `~/wis2box-data/downloads` 目录挂载到容器中的 `/root/downloads` 目录。这是存储从 WIS2 下载数据的位置。
- `-p 8888:8888`：将虚拟机上的 8888 端口映射到容器中的 8888 端口。这使得 Jupyter notebook 服务器可以通过浏览器访问，地址为 `http://YOUR-HOST:8888`。
- `-e JUPYTER_TOKEN=dataismagic!`：设置访问 Jupyter notebook 服务器所需的令牌。您需要在浏览器中访问服务器时提供此令牌。
- `ghrc.io/wmo-im/demo-decode-eccodes-jupyter:latest`：指定容器使用的镜像，该镜像预先包含了下一步练习中使用的示例 Jupyter notebooks。

!!! note "关于 demo-decode-eccodes-jupyter 镜像"

    `demo-decode-eccodes-jupyter` 是为本次培训开发的镜像，基于包含 ecCodes 库的基础镜像，添加了 Jupyter notebook 服务器以及用于数据分析和可视化的一组 Python 库。

    您可以在 [wmo-im/demo-decode-eccodes-jupyter](https://github.com/wmo-im/demo-decode-eccodes-jupyter) 找到该镜像的源代码，包括示例 notebooks。
    
容器启动后，您可以通过浏览器访问 `http://YOUR-HOST:8888` 来访问 Jupyter notebook 服务器。

您会看到一个页面，要求输入 "Password or token"。

输入令牌 `dataismagic!` 登录 Jupyter notebook 服务器（除非您在上述命令中使用了不同的令牌）。

登录后，您应该会看到以下页面，列出了容器中的目录：

![Jupyter notebook home](../assets/img/jupyter-files-screen1.png)

双击 `example-notebooks` 目录以打开它。

您应该会看到以下页面，列出了示例 notebooks：

![Jupyter notebook example notebooks](../assets/img/jupyter-files-screen2.png)

现在，您可以打开示例 notebooks 来解码下载的数据。

### GRIB2 解码示例：CMA GRAPES 的 GEPS 数据

打开 `example-notebooks` 目录中的文件 `GRIB2_CMA_global_ensemble_prediction.ipynb`：

![Jupyter notebook GRIB2 global ensemble prediction](../assets/img/jupyter-grib2-global-ensemble-prediction.png)

阅读 notebook 中的说明并运行单元格以解码全球集合预报的下载数据。通过点击单元格并点击工具栏中的运行按钮，或者按下 `Shift+Enter` 来运行每个单元格。

最后，您应该会看到一张显示海平面气压（MSL）的地图：

![Global ensemble prediction temperature](../assets/img/grib2-global-ensemble-prediction-map.png)

!!! question 

    结果显示了距地面 2 米的温度。您将如何更新 notebook 以显示距地面 10 米的风速？

??? success "点击查看答案"

    要更新 notebook，请执行以下操作。

### BUFR 解码示例：热带气旋路径

打开 `example-notebooks` 目录中的文件 `BUFR_tropical_cyclone_track.ipynb`：

![Jupyter notebook tropical cyclone track](../assets/img/jupyter-tropical-cyclone-track.png)

阅读 notebook 中的说明并运行单元格以解码热带气旋路径的下载数据。通过点击单元格并点击工具栏中的运行按钮，或者按下 `Shift+Enter` 来运行每个单元格。

最后，您应该会看到一张显示热带气旋路径的置信概率的图表：

![Tropical cyclone tracks](../assets/img/tropical-cyclone-track-map.png)

!!! question 

    结果显示了热带风暴路径在 200 公里范围内的预测概率。您将如何更新 notebook 以显示热带风暴路径在 300 公里范围内的预测概率？

??? success "点击查看答案"

    要更新 notebook 以显示热带风暴路径在不同距离范围内的预测概率，您可以更新计算置信概率的代码块中的 `distance_threshold` 变量。

    要显示热带风暴路径在 300 公里范围内的预测概率：

    ```python
    # 设置距离阈值（米）
    distance_threshold = 300000  # 300 公里（以米为单位）
    ```

    然后重新运行 notebook 中的单元格以查看更新后的图表。

!!! note "解码 BUFR 数据"

    您刚刚完成的练习提供了一个使用 ecCodes 库解码 BUFR 数据的具体示例。不同的数据类型可能需要不同的解码步骤，您可能需要参考您正在处理的数据类型的文档。
    
    更多信息请参考 [ecCodes 文档](https://confluence.ecmwf.int/display/ECC)。

### NetCDF 解码示例：月度温度异常

打开 `example-notebooks` 目录中的文件 `NetCDF4_monthly_temperature_anomaly.ipynb`：

![Jupyter notebook monthly temperature anomalies](../assets/img/jupyter-netcdf4-monthly-temperature-anomalies.png)

阅读 notebook 中的说明并运行单元格以解码月度温度异常的下载数据。通过点击单元格并点击工具栏中的运行按钮，或者按下 `Shift+Enter` 来运行每个单元格。

最后，您应该会看到一张显示温度异常的地图：

![Monthly temperature anomalies](../assets/img/netcdf4-monthly-temperature-anomalies-map.png)

!!! note "解码 NetCDF 数据"

    NetCDF 是一种灵活的格式，在本示例中，报告了变量 'anomaly' 的值，并沿 'lat' 和 'lon' 维度进行报告。不同的 NetCDF 数据集可能使用不同的变量名和维度。

## 使用其他工具查看和解码 WMO 二进制格式

示例 notebooks 演示了如何使用 Python 代码解码常用的 WMO 二进制格式。

您还可以使用其他工具解码和可视化 WMO 二进制格式，而无需编写代码，例如：

- [Panoply](https://www.giss.nasa.gov/tools/panoply/) - 一个跨平台应用程序，可绘制来自 NetCDF、HDF、GRIB 和其他数据集的地理参考数组和其他数组。
- [ECMWF Metview](https://confluence.ecmwf.int/display/METV/Metview) - 一个用于数据分析和可视化的气象应用程序，支持 GRIB 和 BUFR 格式。
- [Integrated Data Viewer (IDV)](https://www.unidata.ucar.edu/software/idv/) - 一个免费的基于 Java 的软件框架，用于分析和可视化地球科学数据，包括支持 GRIB 和 NetCDF 格式。

## 结论

!!! success "恭喜！"

    在本次实践课程中，您学习了如何：

    - 运行 "demo-decode-eccodes-jupyter" 镜像的 Docker 容器
    - 运行示例 Jupyter notebooks 来解码 GRIB2、NetCDF 和 BUFR 格式的数据
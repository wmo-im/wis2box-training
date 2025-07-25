---
title: Linux 速查表
---

# Linux 速查表

## 概览

在 Linux 操作系统中工作的基本概念是**文件**和**目录**（文件夹），它们在一个**环境**中以树状结构组织。

一旦你登录到 Linux 系统，你就在一个**shell**中工作，在这里你可以通过执行系统上安装的命令来操作文件和目录。Bash shell 是一个常见且流行的 shell，通常可以在 Linux 系统上找到。

## Bash

### 目录导航

* 进入一个绝对目录：

```bash
cd /dir1/dir2
```

* 进入一个相对目录：

```bash
cd ./somedir
```

* 上移一级目录：

```bash
cd ..
```

* 上移两级目录：

```bash
cd ../..
```

* 移动到你的“主”目录：

```bash
cd -
```

### 文件管理

* 列出当前目录中的文件：

```bash
ls
```

* 详细列出当前目录中的文件：

```bash
ls -l
```

* 列出文件系统的根目录：

```bash
ls -l /
```

* 创建一个空文件：

```bash
touch foo.txt
```

* 使用 `echo` 命令创建一个文件：

```bash
echo "hi there" > test-file.txt
```

* 查看文件内容：

```bash
cat test-file.txt
```

* 复制文件：

```bash
cp file1 file2
```

* 通配符：操作文件模式：

```bash
ls -l fil*  # 匹配 file1 和 file2
```

* 将两个文件合并为一个新文件 `newfile`：

```bash
cat file1 file2 > newfile
```

* 将另一个文件追加到 `newfile` 中

```bash
cat file3 >> newfile
```

* 删除文件：

```bash
rm newfile
```

* 删除所有具有相同文件扩展名的文件：

```bash
rm *.dat
```

* 创建一个目录

```bash
mkdir dir1
```

### 用管道连接命令

管道允许用户使用管道 `|` 符号将一个命令的输出发送到另一个命令：

```bash
echo "hi" | sed 's/hi/bye/'
```

* 使用 grep 过滤命令输出：

```bash
echo "id,title" > test-file.txt
echo "1,birds" >> test-file.txt
echo "2,fish" >> test-file.txt
echo "3,cats" >> test-file.txt

cat test-file.txt | grep fish
```

* 忽略大小写：

```bash
grep -i FISH test-file.txt
```

* 计数匹配行：

```bash
grep -c fish test-file.txt
```

* 返回不包含关键词的输出：

```bash
grep -v birds test-file.txt
```

* 计算 `test-file.txt` 中的行数：

```bash
wc -l test-file.txt
```

* 逐屏显示输出：

```bash
more test-file.txt
```

...带有控制：

- 逐行向下滚动：*enter*
- 跳到下一页：*space bar*
- 回到上一页：*b*

* 显示文件的前3行：

```bash
head -3 test-file.txt
```

* 显示文件的最后2行：

```bash
tail -2 test-file.txt
```

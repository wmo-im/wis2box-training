---
title: Docker cheatsheet
---

# Docker cheatsheet

## نظرة عامة

يتيح Docker إنشاء بيئات افتراضية بطريقة معزولة دعمًا لتقنيات الحوسبة الافتراضية. المفهوم الأساسي وراء Docker هو الحاويات، حيث يمكن تشغيل البرمجيات كخدمات، تتفاعل مع حاويات برمجية أخرى، على سبيل المثال.

يتضمن سير العمل النموذجي لـ Docker إنشاء وبناء **الصور**، والتي يتم تشغيلها بعد ذلك كـ **حاويات** حية.

يُستخدم Docker لتشغيل مجموعة الخدمات التي تشكل wis2box باستخدام صور مُعدة مسبقًا.

### إدارة الصور

* عرض الصور المتاحة

```bash
docker image ls
```

* تحديث صورة:

```bash
docker pull my-image:latest
```

* إزالة صورة:

```bash
docker rmi my-image:local
```

### إدارة الأحجام

* عرض جميع الأحجام المُنشأة:

```bash
docker volume ls
```

* عرض معلومات تفصيلية عن حجم:

```bash
docker volume inspect my-volume
```

* إزالة حجم:

```bash
docker volume rm my-volume
```

* إزالة جميع الأحجام غير المستخدمة:

```bash
docker volume prune
```

### إدارة الحاويات

* عرض قائمة بالحاويات الجاري تشغيلها:

```bash
docker ps
```

* قائمة بجميع الحاويات:

```bash
docker ps -a
```

* الدخول إلى الطرفية التفاعلية لحاوية جاري تشغيلها:


!!! tip

    استخدم `docker ps` لاستخدام معرف الحاوية في الأمر أدناه

```bash
docker exec -it my-container /bin/bash
```

* إزالة حاوية

```bash
docker rm my-container
```

* إزالة حاوية جاري تشغيلها:

```bash
docker rm -f my-container
```
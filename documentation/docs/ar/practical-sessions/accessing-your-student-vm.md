---
title: الوصول إلى جهاز الطالب الافتراضي (VM)
---

# الوصول إلى جهاز الطالب الافتراضي (VM)

!!! abstract "نتائج التعلم"

    بنهاية هذه الجلسة العملية، ستكون قادرًا على:

    - الوصول إلى جهاز الطالب الافتراضي الخاص بك عبر SSH وWinSCP
    - التحقق من تثبيت البرامج المطلوبة للتمارين العملية
    - التحقق من أنك تمتلك مواد التمارين لهذا التدريب على جهاز الطالب الافتراضي المحلي الخاص بك

## المقدمة

كجزء من ورش العمل التدريبية المحلية لـWIS2، يمكنك الوصول إلى جهاز الطالب الافتراضي الشخصي الخاص بك على الشبكة التدريبية المحلية المسماة "WIS2-training".

يحتوي جهاز الطالب الافتراضي الخاص بك على البرامج التالية المثبتة مسبقًا:

- Ubuntu 22.04 LTS [ubuntu-22.04.5-live-server-amd64.iso](https://releases.ubuntu.com/jammy/ubuntu-22.04.5-live-server-amd64.iso)
- Python 3.10.12
- Docker 24.0.6
- Docker Compose 2.21.0
- محررات نصوص: vim، nano

!!! note

    إذا كنت ترغب في إجراء هذا التدريب خارج جلسة تدريب محلية، يمكنك توفير جهاز افتراضي خاص بك باستخدام أي مزود خدمة سحابية، على سبيل المثال:

    - GCP (Google Cloud Platform) VM instance `e2-medium`
    - AWS (Amazon Web Services) ec2-instance `t3a.medium`
    - Azure (Microsoft) Azure Virtual Machine `standard_b2s`

    اختر Ubuntu Server 22.0.4 LTS كنظام تشغيل.

    بعد إنشاء الجهاز الافتراضي، تأكد من تثبيت Python وDocker وDocker Compose، كما هو موضح في [wis2box-software-dependencies](https://docs.wis2box.wis.wmo.int/en/latest/user/getting-started.html#software-dependencies).

    يمكن تنزيل أرشيف الإصدار الخاص بـwis2box المستخدم في هذا التدريب كما يلي:

    ```bash
    wget https://github.com/World-Meteorological-Organization/wis2box-release/releases/download/1.0.0/wis2box-setup.zip
    unzip wis2box-setup.zip
    ```

    يمكنك دائمًا العثور على أحدث أرشيف 'wis2box-setup' على [https://github.com/World-Meteorological-Organization/wis2box/releases](https://github.com/World-Meteorological-Organization/wis2box-release/releases).

    يمكن تنزيل مواد التمارين المستخدمة في هذا التدريب كما يلي:

    ```bash
    wget https://training.wis2box.wis.wmo.int/exercise-materials.zip
    unzip exercise-materials.zip
    ```

    الحزم الإضافية التالية من Python مطلوبة لتشغيل مواد التمارين:

    ```bash
    pip3 install minio
    pip3 install pywiscat==0.2.2
    ```

    إذا كنت تستخدم جهاز الطالب الافتراضي المقدم خلال جلسات التدريب المحلية لـWIS2، فسيتم تثبيت البرامج المطلوبة مسبقًا.

## الاتصال بجهاز الطالب الافتراضي على الشبكة التدريبية المحلية

قم بتوصيل جهاز الكمبيوتر الخاص بك بشبكة Wi-Fi المحلية التي يتم بثها في الغرفة أثناء تدريب WIS2 وفقًا للتعليمات المقدمة من المدرب.

استخدم عميل SSH للاتصال بجهاز الطالب الافتراضي الخاص بك باستخدام المعلومات التالية:

- **المضيف: (يتم توفيره أثناء التدريب الشخصي)**
- **المنفذ: 22**
- **اسم المستخدم: (يتم توفيره أثناء التدريب الشخصي)**
- **كلمة المرور: (يتم توفيرها أثناء التدريب الشخصي)**

!!! tip
    تواصل مع المدرب إذا كنت غير متأكد من اسم المضيف/اسم المستخدم أو إذا واجهت مشاكل في الاتصال.

بمجرد الاتصال، يرجى تغيير كلمة المرور الخاصة بك لضمان عدم تمكن الآخرين من الوصول إلى جهازك الافتراضي:

```bash
limper@student-vm:~$ passwd
Changing password for testuser.
Current password:
New password:
Retype new password:
passwd: password updated successfully
```

## التحقق من إصدارات البرامج

لكي تتمكن من تشغيل wis2box، يجب أن يحتوي جهاز الطالب الافتراضي على Python وDocker وDocker Compose مثبتة مسبقًا.

تحقق من إصدار Python:
```bash
python3 --version
```
النتيجة:
```console
Python 3.10.12
```

تحقق من إصدار Docker:
```bash
docker --version
```
النتيجة:
```console
Docker version 24.0.6, build ed223bc
```

تحقق من إصدار Docker Compose:
```bash
docker compose version
```
النتيجة:
```console
Docker Compose version v2.21.0
```

لضمان أن المستخدم الخاص بك يمكنه تشغيل أوامر Docker، تم إضافة المستخدم الخاص بك إلى مجموعة `docker`.

لاختبار أن المستخدم الخاص بك يمكنه تشغيل docker hello-world، قم بتشغيل الأمر التالي:
```bash
docker run hello-world
```

يجب أن يقوم هذا بتنزيل صورة hello-world وتشغيل حاوية تطبع رسالة.

تحقق من أنك ترى ما يلي في الإخراج:

```console
...
Hello from Docker!
This message shows that your installation appears to be working correctly.
...
```

## فحص مواد التمارين

افحص محتويات دليل المنزل الخاص بك؛ هذه هي المواد المستخدمة كجزء من التدريب والجلسات العملية.

```bash
ls ~/
```
النتيجة:
```console
exercise-materials  wis2box
```

إذا كان لديك WinSCP مثبتًا على جهاز الكمبيوتر المحلي الخاص بك، يمكنك استخدامه للاتصال بجهاز الطالب الافتراضي الخاص بك وفحص محتويات دليل المنزل الخاص بك وتنزيل أو تحميل الملفات بين جهازك الافتراضي وجهاز الكمبيوتر المحلي الخاص بك.

WinSCP ليس مطلوبًا للتدريب، ولكنه يمكن أن يكون مفيدًا إذا كنت ترغب في تحرير الملفات على جهازك الافتراضي باستخدام محرر نصوص على جهاز الكمبيوتر المحلي الخاص بك.

إليك كيفية الاتصال بجهاز الطالب الافتراضي الخاص بك باستخدام WinSCP:

افتح WinSCP وانقر على "New Site". يمكنك إنشاء اتصال SCP جديد بجهازك الافتراضي كما يلي:

<img alt="winscp-student-vm-scp.png" src="/../assets/img/winscp-student-vm-scp.png" width="400">

انقر على 'Save' ثم 'Login' للاتصال بجهازك الافتراضي.

ويجب أن تكون قادرًا على رؤية المحتوى التالي:

<img alt="winscp-student-vm-exercise-materials.png" src="/../assets/img/winscp-student-vm-exercise-materials.png" width="600">

## الخاتمة

!!! success "تهانينا!"
    في هذه الجلسة العملية، تعلمت كيفية:

    - الوصول إلى جهاز الطالب الافتراضي الخاص بك عبر SSH وWinSCP
    - التحقق من تثبيت البرامج المطلوبة للتمارين العملية
    - التحقق من أنك تمتلك مواد التمارين لهذا التدريب على جهاز الطالب الافتراضي المحلي الخاص بك
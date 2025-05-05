---
title: الوصول إلى الجهاز الافتراضي الخاص بالطالب
---

# الوصول إلى الجهاز الافتراضي الخاص بالطالب

!!! abstract "مخرجات التعلم"

    بنهاية هذه الجلسة العملية، ستكون قادراً على:

    - الوصول إلى جهازك الافتراضي عبر SSH و WinSCP
    - التحقق من تثبيت البرامج المطلوبة للتمارين العملية
    - التحقق من وصولك إلى مواد التمارين لهذا التدريب على جهازك الافتراضي المحلي

## مقدمة

كجزء من جلسات تدريب wis2box المحلية، يمكنك الوصول إلى جهازك الافتراضي الشخصي على شبكة التدريب المحلية المسماة "WIS2-training".

جهازك الافتراضي مثبت عليه البرامج التالية مسبقاً:

- Ubuntu 22.0.4.3 LTS [ubuntu-22.04.3-live-server-amd64.iso](https://releases.ubuntu.com/jammy/ubuntu-22.04.3-live-server-amd64.iso)
- Python 3.10.12
- Docker 24.0.6
- Docker Compose 2.21.0
- محررات النصوص: vim, nano

!!! note

    إذا كنت ترغب في تشغيل هذا التدريب خارج جلسة تدريب محلية، يمكنك توفير نسختك الخاصة باستخدام أي مزود سحابي، على سبيل المثال:

    - GCP (Google Cloud Platform) VM instance `e2-medium`
    - AWS (Amazon Web Services) ec2-instance `t3a.medium`
    - Azure (Microsoft) Azure Virtual Machine `standard_b2s`

    اختر Ubuntu Server 22.0.4 LTS كنظام تشغيل.

    بعد إنشاء جهازك الافتراضي، تأكد من تثبيت python و docker و docker compose، كما هو موضح في [wis2box-software-dependencies](https://docs.wis2box.wis.wmo.int/en/latest/user/getting-started.html#software-dependencies).

    يمكن تحميل أرشيف الإصدار لـ wis2box المستخدم في هذا التدريب كما يلي:

    ```bash
    wget https://github.com/World-Meteorological-Organization/wis2box-release/releases/download/1.0.0/wis2box-setup.zip
    unzip wis2box-setup.zip
    ```

    يمكنك دائماً العثور على أحدث أرشيف 'wis2box-setup' في [https://github.com/World-Meteorological-Organization/wis2box/releases](https://github.com/World-Meteorological-Organization/wis2box-release/releases).

    يمكن تحميل مواد التمارين المستخدمة في هذا التدريب كما يلي:

    ```bash
    wget https://training.wis2box.wis.wmo.int/exercise-materials.zip
    unzip exercise-materials.zip
    ```

    حزم Python الإضافية التالية مطلوبة لتشغيل مواد التمارين:

    ```bash
    pip3 install minio
    pip3 install pywiscat==0.2.2
    ```

    إذا كنت تستخدم الجهاز الافتراضي للطالب المقدم خلال جلسات تدريب WIS2 المحلية، فسيتم تثبيت البرامج المطلوبة مسبقاً.

## الاتصال بجهازك الافتراضي على شبكة التدريب المحلية

قم بتوصيل جهاز الكمبيوتر الخاص بك بشبكة Wi-Fi المحلية المبثوثة في الغرفة خلال تدريب WIS2 وفقاً للتعليمات المقدمة من المدرب.

استخدم عميل SSH للاتصال بجهازك الافتراضي باستخدام ما يلي:

- **المضيف: (يتم توفيره خلال التدريب الشخصي)**
- **المنفذ: 22**
- **اسم المستخدم: (يتم توفيره خلال التدريب الشخصي)**
- **كلمة المرور: (يتم توفيرها خلال التدريب الشخصي)**

!!! tip
    اتصل بالمدرب إذا كنت غير متأكد من اسم المضيف/اسم المستخدم أو واجهت مشاكل في الاتصال.

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

لتتمكن من تشغيل wis2box، يجب أن يكون لدى الجهاز الافتراضي للطالب Python و Docker و Docker Compose مثبتة مسبقاً.

تحقق من إصدار Python:
```bash
python3 --version
```
يعيد:
```console
Python 3.10.12
```

تحقق من إصدار docker:
```bash
docker --version
```
يعيد:
```console
Docker version 24.0.6, build ed223bc
```

تحقق من إصدار Docker Compose:
```bash
docker compose version
```
يعيد:
```console
Docker Compose version v2.21.0
```

للتأكد من أن مستخدمك يمكنه تشغيل أوامر Docker، تمت إضافة مستخدمك إلى مجموعة `docker`.

لاختبار أن مستخدمك يمكنه تشغيل docker hello-world، قم بتشغيل الأمر التالي:
```bash
docker run hello-world
```

يجب أن يقوم هذا بسحب صورة hello-world وتشغيل حاوية تطبع رسالة.

تحقق من أنك ترى ما يلي في المخرجات:

```console
...
Hello from Docker!
This message shows that your installation appears to be working correctly.
...
```

## فحص مواد التمارين

افحص محتويات الدليل الرئيسي الخاص بك؛ هذه هي المواد المستخدمة كجزء من التدريب والجلسات العملية.

```bash
ls ~/
```
يعيد:
```console
exercise-materials  wis2box
```

إذا كان لديك WinSCP مثبت على جهاز الكمبيوتر المحلي الخاص بك، يمكنك استخدامه للاتصال بجهازك الافتراضي وفحص محتويات الدليل الرئيسي الخاص بك وتنزيل أو تحميل الملفات بين جهازك الافتراضي وجهاز الكمبيوتر المحلي الخاص بك.

WinSCP ليس مطلوباً للتدريب، ولكنه قد يكون مفيداً إذا كنت تريد تحرير الملفات على جهازك الافتراضي باستخدام محرر نصوص على جهاز الكمبيوتر المحلي الخاص بك.

إليك كيفية الاتصال بجهازك الافتراضي باستخدام WinSCP:

افتح WinSCP وانقر على "New Site". يمكنك إنشاء اتصال SCP جديد بجهازك الافتراضي كما يلي:

<img alt="winscp-student-vm-scp.png" src="../../assets/img/winscp-student-vm-scp.png" width="400">

انقر على 'Save' ثم 'Login' للاتصال بجهازك الافتراضي.

ويجب أن تكون قادراً على رؤية المحتوى التالي:

<img alt="winscp-student-vm-exercise-materials.png" src="../../assets/img/winscp-student-vm-exercise-materials.png" width="600">

## الخاتمة

!!! success "تهانينا!"
    في هذه الجلسة العملية، تعلمت كيفية:

    - الوصول إلى جهازك الافتراضي عبر SSH و WinSCP
    - التحقق من تثبيت البرامج المطلوبة للتمارين العملية
    - التحقق من وصولك إلى مواد التمارين لهذا التدريب على جهازك الافتراضي المحلي
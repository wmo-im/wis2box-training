---
title: الوصول إلى جهاز الطالب الافتراضي الخاص بك
---

# الوصول إلى جهاز الطالب الافتراضي الخاص بك

!!! abstract "نتائج التعلم"

    بنهاية هذه الجلسة العملية، ستكون قادرًا على:

    - الوصول إلى جهاز الطالب الافتراضي الخاص بك عبر SSH و WinSCP
    - التحقق من تثبيت البرامج المطلوبة للتمارين العملية
    - التحقق من وجود مواد التمرين لهذا التدريب على جهاز الطالب الافتراضي المحلي الخاص بك

## مقدمة

كجزء من جلسات تدريب wis2box المحلية، يمكنك الوصول إلى جهاز الطالب الافتراضي الشخصي الخاص بك على شبكة التدريب المحلية التي تُسمى "WIS2-training".

يحتوي جهاز الطالب الافتراضي الخاص بك على البرامج التالية المثبتة مسبقًا:

- Ubuntu 22.0.4.3 LTS [ubuntu-22.04.3-live-server-amd64.iso](https://releases.ubuntu.com/jammy/ubuntu-22.04.3-live-server-amd64.iso)
- Python 3.10.12
- Docker 24.0.6
- Docker Compose 2.21.0
- محررات النصوص: vim، nano

!!! note

    إذا كنت ترغب في تشغيل هذا التدريب خارج جلسة تدريب محلية، يمكنك توفير نسختك الخاصة باستخدام أي مزود سحابي، على سبيل المثال:

    - نسخة VM من GCP (Google Cloud Platform) `e2-medium`
    - نسخة ec2 من AWS (Amazon Web Services) `t3a.medium`
    - نسخة Azure Virtual Machine من Azure (Microsoft) `standard_b2s`

    اختر Ubuntu Server 22.0.4 LTS كنظام تشغيل.
    
    بعد إنشاء جهاز الطالب الافتراضي الخاص بك، تأكد من تثبيت python، docker و docker compose، كما هو موضح في [wis2box-software-dependencies](https://docs.wis2box.wis.wmo.int/en/latest/user/getting-started.html#software-dependencies).
    
    يمكن تنزيل أرشيف الإصدار الخاص بـ wis2box المستخدم في هذا التدريب كما يلي:

    ```bash
    wget https://github.com/World-Meteorological-Organization/wis2box-release/releases/download/1.0.0/wis2box-setup.zip
    unzip wis2box-setup.zip
    ```
    
    يمكنك دائمًا العثور على أحدث أرشيف 'wis2box-setup' في [https://github.com/World-Meteorological-Organization/wis2box/releases](https://github.com/World-Meteorological-Organization/wis2box-release/releases).

    يمكن تنزيل مواد التمرين المستخدمة في هذا التدريب كما يلي:

    ```bash
    wget https://training.wis2box.wis.wmo.int/exercise-materials.zip
    unzip exercise-materials.zip
    ```

    تتطلب الحزم الإضافية لـ Python التالية لتشغيل مواد التمرين:

    ```bash
    pip3 install minio
    pip3 install pywiscat==0.2.2
    ```

    إذا كنت تستخدم جهاز الطالب الافتراضي المقدم خلال جلسات تدريب WIS2 المحلية، فسيكون البرنامج المطلوب مثبتًا بالفعل.

## الاتصال بجهاز الطالب الافتراضي الخاص بك على شبكة التدريب المحلية

قم بتوصيل جهاز الكمبيوتر الخاص بك بشبكة Wi-Fi المحلية التي يتم بثها في الغرفة خلال تدريب WIS2 وفقًا للتعليمات التي يقدمها المدرب.

استخدم عميل SSH للاتصال بجهاز الطالب الافتراضي الخاص بك باستخدام التالي:

- **المضيف: (مقدم خلال التدريب الشخصي)**
- **المنفذ: 22**
- **اسم المستخدم: (مقدم خلال التدريب الشخصي)**
- **كلمة المرور: (مقدمة خلال التدريب الشخصي)**

!!! tip
    اتصل بالمدرب إذا كنت غير متأكد من اسم المضيف/اسم المستخدم أو إذا واجهت مشكلات في الاتصال.

بمجرد الاتصال، يرجى تغيير كلمة المرور الخاصة بك لضمان عدم قدرة الآخرين على الوصول إلى جهاز الطالب الافتراضي الخاص بك:

```bash
limper@student-vm:~$ passwd
Changing password for testuser.
Current password:
New password:
Retype new password:
passwd: password updated successfully
```

## التحقق من إصدارات البرامج

لتتمكن من تشغيل wis2box، يجب أن يكون لدى جهاز الطالب الافتراضي الخاص بك Python، Docker و Docker Compose مثبتين مسبقًا.

تحقق من إصدار Python:
```bash
python3 --version
```
يعود:
```console
Python 3.10.12
```

تحقق من إصدار docker:
```bash
docker --version
```
يعود:
```console
Docker version 24.0.6, build ed223bc
```

تحقق من إصدار Docker Compose:
```bash
docker compose version
```
يعود:
```console
Docker Compose version v2.21.0
```

لضمان قدرة المستخدم على تشغيل أوامر Docker، تمت إضافة المستخدم إلى مجموعة `docker`.

لتجربة قدرة المستخدم على تشغيل docker hello-world، قم بتشغيل الأمر التالي:
```bash
docker run hello-world
```

يجب أن يقوم هذا بسحب صورة hello-world وتشغيل حاوية تطبع رسالة.

تحقق من رؤية التالي في الإخراج:

```console
...
Hello from Docker!
This message shows that your installation appears to be working correctly.
...
```

## فحص مواد التمرين

افحص محتويات دليل البيت الخاص بك؛ هذه هي المواد المستخدمة كجزء من التدريب والجلسات العملية.

```bash
ls ~/
```
يعود:
```console
exercise-materials  wis2box
```

إذا كان لديك WinSCP مثبتًا على جهاز الكمبيوتر المحلي الخاص بك، يمكنك استخدامه للاتصال بجهاز الطالب الافتراضي الخاص بك وفحص محتويات دليل البيت الخاص بك وتنزيل أو تحميل الملفات بين جهاز الطالب الافتراضي الخاص بك وجهاز الكمبيوتر المحلي الخاص بك.

ليس من الضروري استخدام WinSCP للتدريب، ولكنه قد يكون مفيدًا إذا كنت ترغب في تحرير الملفات على جهاز الطالب الافتراضي الخاص بك باستخدام محرر نصوص على جهاز الكمبيوتر المحلي الخاص بك.

إليك كيفية الاتصال بجهاز الطالب الافتراضي الخاص بك باستخدام WinSCP:

افتح WinSCP وانقر على "موقع جديد". يمكنك إنشاء اتصال SCP جديد بجهاز الطالب الافتراضي الخاص بك كما يلي:

<img alt="winscp-student-vm-scp.png" src="/../assets/img/winscp-student-vm-scp.png" width="400">

انقر على 'حفظ' ثم 'تسجيل الدخول' للاتصال بجهاز الطالب الافتراضي الخاص بك.

ويجب أن تتمكن من رؤية المحتوى التالي:

<img alt="winscp-student-vm-exercise-materials.png" src="/../assets/img/winscp-student-vm-exercise-materials.png" width="600">

## الخاتمة

!!! success "تهانينا!"
    في هذه الجلسة العملية، تعلمت كيفية:

    - الوصول إلى جهاز الطالب الافتراضي الخاص بك عبر SSH و WinSCP
    - التحقق من تثبيت البرامج المطلوبة للتمارين العملية
    - التحقق من وجود مواد التمرين لهذا التدريب على جهاز الطالب الافتراضي المحلي الخاص بك
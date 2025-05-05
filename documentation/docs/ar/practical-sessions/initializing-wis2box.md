---
title: تهيئة wis2box
---

# تهيئة wis2box

!!! abstract "مخرجات التعلم"

    بنهاية هذه الجلسة العملية، ستكون قادراً على:

    - تشغيل برنامج `wis2box-create-config.py` لإنشاء التكوين الأولي
    - بدء تشغيل wis2box والتحقق من حالة مكوناته
    - عرض محتويات **wis2box-api**
    - الوصول إلى **wis2box-webapp**
    - الاتصال بـ **wis2box-broker** المحلي باستخدام MQTT Explorer

!!! note

    تستند المواد التدريبية الحالية على wis2box-release 1.0.0.
    
    راجع [accessing-your-student-vm](accessing-your-student-vm.md) للحصول على تعليمات حول كيفية تنزيل وتثبيت حزمة برامج wis2box إذا كنت تقوم بهذا التدريب خارج جلسة تدريب محلية.

## التحضير

قم بتسجيل الدخول إلى الجهاز الافتراضي المخصص لك باستخدام اسم المستخدم وكلمة المرور وتأكد من أنك في مجلد `wis2box`:

```bash
cd ~/wis2box
```

## إنشاء التكوين الأولي

يتطلب التكوين الأولي لـ wis2box:

- ملف بيئة `wis2box.env` يحتوي على معلمات التكوين
- مجلد على الجهاز المضيف للمشاركة بين الجهاز المضيف وحاويات wis2box محدد بواسطة متغير البيئة `WIS2BOX_HOST_DATADIR`

يمكن استخدام برنامج `wis2box-create-config.py` لإنشاء التكوين الأولي لـ wis2box الخاص بك.

سيطرح عليك مجموعة من الأسئلة للمساعدة في إعداد التكوين الخاص بك.

ستتمكن من مراجعة وتحديث ملفات التكوين بعد اكتمال البرنامج.

قم بتشغيل البرنامج كما يلي:

```bash
python3 wis2box-create-config.py
```

### مجلد wis2box-host-data

سيطلب منك البرنامج إدخال المجلد المراد استخدامه لمتغير البيئة `WIS2BOX_HOST_DATADIR`.

لاحظ أنك تحتاج إلى تحديد المسار الكامل لهذا المجلد.

على سبيل المثال، إذا كان اسم المستخدم الخاص بك هو `username`، فإن المسار الكامل للمجلد هو `/home/username/wis2box-data`:

```{.copy}
username@student-vm-username:~/wis2box$ python3 wis2box-create-config.py
Please enter the directory to be used for WIS2BOX_HOST_DATADIR:
/home/username/wis2box-data
The directory to be used for WIS2BOX_HOST_DATADIR will be set to:
    /home/username/wis2box-data
Is this correct? (y/n/exit)
y
The directory /home/username/wis2box-data has been created.
```

### عنوان URL لـ wis2box

بعد ذلك، سيُطلب منك إدخال عنوان URL لـ wis2box الخاص بك. هذا هو عنوان URL الذي سيتم استخدامه للوصول إلى تطبيق wis2box وواجهة برمجة التطبيقات وواجهة المستخدم.

الرجاء استخدام `http://<your-hostname-or-ip>` كعنوان URL.

```{.copy}
Please enter the URL of the wis2box:
 For local testing the URL is http://localhost
 To enable remote access, the URL should point to the public IP address or domain name of the server hosting the wis2box.
http://username.wis2.training
The URL of the wis2box will be set to:
  http://username.wis2.training
Is this correct? (y/n/exit)
```

### كلمات مرور WEBAPP و STORAGE و BROKER

يمكنك استخدام خيار توليد كلمة مرور عشوائية عند المطالبة بـ `WIS2BOX_WEBAPP_PASSWORD` و `WIS2BOX_STORAGE_PASSWORD` و `WIS2BOX_BROKER_PASSWORD` وتحديد كلمات المرور الخاصة بك.

لا تقلق بشأن تذكر كلمات المرور هذه، سيتم تخزينها في ملف `wis2box.env` في مجلد wis2box الخاص بك.

### مراجعة `wis2box.env`

بمجرد اكتمال البرنامج، تحقق من محتويات ملف `wis2box.env` في المجلد الحالي:

```bash
cat ~/wis2box/wis2box.env
```

أو تحقق من محتوى الملف عبر WinSCP.

!!! question

    ما هي قيمة WISBOX_BASEMAP_URL في ملف wis2box.env؟

??? success "انقر لكشف الإجابة"

    القيمة الافتراضية لـ WIS2BOX_BASEMAP_URL هي `https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png`.

    يشير عنوان URL هذا إلى خادم بلاط OpenStreetMap. إذا كنت تريد استخدام مزود خرائط مختلف، يمكنك تغيير عنوان URL هذا ليشير إلى خادم بلاط مختلف.

!!! question 

    ما هي قيمة متغير البيئة WIS2BOX_STORAGE_DATA_RETENTION_DAYS في ملف wis2box.env؟

??? success "انقر لكشف الإجابة"

    القيمة الافتراضية لـ WIS2BOX_STORAGE_DATA_RETENTION_DAYS هي 30 يوماً. يمكنك تغيير هذه القيمة إلى عدد مختلف من الأيام إذا رغبت في ذلك.
    
    تقوم حاوية wis2box-management بتشغيل مهمة cron يومياً لإزالة البيانات الأقدم من عدد الأيام المحدد بواسطة WIS2BOX_STORAGE_DATA_RETENTION_DAYS من دلو `wis2box-public` وواجهة برمجة التطبيقات الخلفية:
    
    ```{.copy}
    0 0 * * * su wis2box -c "wis2box data clean --days=$WIS2BOX_STORAGE_DATA_RETENTION_DAYS"
    ```

[يتبع الترجمة للجزء المتبقي...]
---
title: تهيئة wis2box
---

# تهيئة wis2box

!!! abstract "نتائج التعلم"

    بنهاية هذه الجلسة العملية، ستكون قادرًا على:

    - تشغيل السكربت `wis2box-create-config.py` لإنشاء التكوين الأولي
    - بدء تشغيل wis2box والتحقق من حالة مكوناته
    - عرض محتويات **wis2box-api**
    - الوصول إلى **wis2box-webapp**
    - الاتصال بـ **wis2box-broker** المحلي باستخدام MQTT Explorer

!!! note

    المواد التدريبية الحالية مبنية على إصدار wis2box-release 1.0.0.
    
    انظر [accessing-your-student-vm](./accessing-your-student-vm.md) للحصول على تعليمات حول كيفية تنزيل وتثبيت حزمة برامج wis2box إذا كنت تقوم بتشغيل هذا التدريب خارج جلسة تدريب محلية.

## التحضير

قم بتسجيل الدخول إلى الجهاز الافتراضي المخصص لك باستخدام اسم المستخدم وكلمة المرور الخاصة بك وتأكد من أنك في دليل `wis2box`:

```bash
cd ~/wis2box
```

## إنشاء التكوين الأولي

التكوين الأولي لـ wis2box يتطلب:

- ملف بيئة `wis2box.env` يحتوي على معلمات التكوين
- دليل على جهاز المضيف للمشاركة بين جهاز المضيف وحاويات wis2box المحددة بواسطة متغير البيئة `WIS2BOX_HOST_DATADIR`

يمكن استخدام السكربت `wis2box-create-config.py` لإنشاء التكوين الأولي لـ wis2box.

سيطرح عليك مجموعة من الأسئلة لمساعدتك في إعداد التكوين الخاص بك.

سيكون بإمكانك مراجعة وتحديث ملفات التكوين بعد اكتمال السكربت.

قم بتشغيل السكربت على النحو التالي:

```bash
python3 wis2box-create-config.py
```

### دليل بيانات wis2box-host

سيطلب منك السكربت إدخال الدليل الذي سيتم استخدامه لمتغير البيئة `WIS2BOX_HOST_DATADIR`.

لاحظ أنه يجب تحديد المسار الكامل لهذا الدليل.

على سبيل المثال، إذا كان اسم المستخدم الخاص بك هو `username`، فإن المسار الكامل للدليل هو `/home/username/wis2box-data`:

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

بعد ذلك، سيُطلب منك إدخال عنوان URL لـ wis2box. هذا هو العنوان URL الذي سيتم استخدامه للوصول إلى تطبيق الويب wis2box وواجهة برمجة التطبيقات وواجهة المستخدم.

يرجى استخدام `http://<your-hostname-or-ip>` كعنوان URL.

```{.copy}
Please enter the URL of the wis2box:
 For local testing the URL is http://localhost
 To enable remote access, the URL should point to the public IP address or domain name of the server hosting the wis2box.
http://username.wis2.training
The URL of the wis2box will be set to:
  http://username.wis2.training
Is this correct? (y/n/exit)
```

### كلمات مرور WEBAPP، STORAGE و BROKER

يمكنك استخدام خيار إنشاء كلمة مرور عشوائية عندما يُطلب منك `WIS2BOX_WEBAPP_PASSWORD`، `WIS2BOX_STORAGE_PASSWORD`، `WIS2BOX_BROKER_PASSWORD` وتحديد كلمة المرور الخاصة بك.

لا داعي للقلق بشأن تذكر هذه الكلمات، سيتم تخزينها في ملف `wis2box.env` في دليل wis2box الخاص بك.

### مراجعة `wis2box.env`

بمجرد اكتمال السكربتات، تحقق من محتويات ملف `wis2box.env` في دليلك الحالي:

```bash
cat ~/wis2box/wis2box.env
```

أو تحقق من محتوى الملف عبر WinSCP.

!!! question

    ما هي قيمة WISBOX_BASEMAP_URL في ملف wis2box.env؟

??? success "انقر لكشف الإجابة"

    القيمة الافتراضية لـ WIS2BOX_BASEMAP_URL هي `https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png`.

    يشير هذا العنوان إلى خادم البلاط OpenStreetMap. إذا كنت ترغب في استخدام مزود خرائط مختلف، يمكنك تغيير هذا العنوان ليشير إلى خادم بلاط مختلف.

!!! question 

    ما هي قيمة متغير البيئة WIS2BOX_STORAGE_DATA_RETENTION_DAYS في ملف wis2box.env؟

??? success "انقر لكشف الإجابة"

    القيمة الافتراضية لـ WIS2BOX_STORAGE_DATA_RETENTION_DAYS هي 30 يومًا. يمكنك تغيير هذه القيمة إلى عدد مختلف من الأيام إذا كنت ترغب في ذلك.
    
    تقوم حاوية wis2box-management بتشغيل وظيفة cron يوميًا لإزالة البيانات الأقدم من عدد الأيام المحدد بواسطة WIS2BOX_STORAGE_DATA_RETENTION_DAYS من دلو `wis2box-public` وواجهة برمجة التطبيقات الخلفية:
    
    ```{.copy}
    0 0 * * * su wis2box -c "wis2box data clean --days=$WIS2BOX_STORAGE_DATA_RETENTION_DAYS"
    ```

!!! note

    يحتوي ملف `wis2box.env` على متغيرات البيئة التي تحدد تكوين wis2box الخاص بك. لمزيد من المعلومات، راجع [wis2box-documentation](https://docs.wis2box.wis.wmo.int/en/latest/reference/configuration.html).

    لا تقم بتعديل ملف `wis2box.env` إلا إذا كنت متأكدًا من التغييرات التي تقوم بها. قد تؤدي التغييرات غير الصحيحة إلى توقف wis2box عن العمل.

    لا تشارك محتويات ملف `wis2box.env` الخاص بك مع أي شخص، حيث يحتوي على معلومات حساسة مثل كلمات المرور.

## بدء تشغيل wis2box

تأكد من أنك في الدليل الذي يحتوي على ملفات تعريف حزمة برامج wis2box:

```{.copy}
cd ~/wis2box
```

ابدأ تشغيل wis2box بالأمر التالي:

```{.copy}
python3 wis2box-ctl.py start
```

عند تشغيل هذا الأمر لأول مرة، سترى الإخراج التالي:

```
No docker-compose.images-*.yml files found, creating one
Current version=Undefined, latest version=1.0.0
Would you like to update ? (y/n/exit)
```

اختر ``y`` وسيقوم السكربت بإنشاء الملف ``docker-compose.images-1.0.0.yml``، وتنزيل الصور Docker المطلوبة وبدء الخدمات.

قد يستغرق تنزيل الصور بعض الوقت اعتمادًا على سرعة اتصالك بالإنترنت. هذه الخطوة مطلوبة فقط في المرة الأولى التي تبدأ فيها wis2box.

تفقد الحالة بالأمر التالي:

```{.copy}
python3 wis2box-ctl.py status
```

كرر هذا الأمر حتى تكون جميع الخدمات قيد التشغيل والعمل.

!!! note "wis2box و Docker"
    يعمل wis2box كمجموعة من حاويات Docker التي يديرها docker-compose.
    
    تُعرف الخدمات في ملفات `docker-compose*.yml` المختلفة التي يمكن العثور عليها في دليل `~/wis2box/`.
    
    يُستخدم السكربت البرمجي `wis2box-ctl.py` لتشغيل أوامر Docker Compose الأساسية التي تتحكم في خدمات wis2box.

    لا تحتاج إلى معرفة تفاصيل حاويات Docker لتشغيل حزمة برامج wis2box، ولكن يمكنك فحص ملفات `docker-compose*.yml` لرؤية كيفية تعريف الخدمات. إذا كنت مهتمًا بمعرفة المزيد عن Docker، يمكنك العثور على مزيد من المعلومات في [Docker documentation](https://docs.docker.com/).

لتسجيل الدخول إلى حاوية wis2box-management، استخدم الأمر التالي:

```{.copy}
python3 wis2box-ctl.py login
```

داخل حاوية wis2box-management، يمكنك تشغيل أوامر مختلفة لإدارة wis2box الخاص بك، مثل:

- `wis2box auth add-token --path processes/wis2box` : لإنشاء رمز تفويض لنقطة النهاية `processes/wis2box`
- `wis2box data clean --days=<number-of-days>` : لتنظيف البيانات الأقدم من عدد معين من الأيام من دلو `wis2box-public`

للخروج من الحاوية والعودة إلى جهاز المضيف، استخدم الأمر التالي:

```{.copy}
exit
```

قم بتشغيل الأمر التالي لرؤية حاويات docker التي تعمل على جهاز المضيف الخاص بك:

```{.copy}
docker ps
```

يجب أن ترى الحاويات التالية قيد التشغيل:

- wis2box-management
- wis2box-api
- wis2box-minio
- wis2box-webapp
- wis2box-auth
- wis2box-ui
- wis2downloader
- elasticsearch
- elasticsearch-exporter
- nginx
- mosquitto
- prometheus
- grafana
- loki

هذه الحاويات جزء من حزمة برامج wis2box وتوفر الخدمات المختلفة المطلوبة لتشغيل wis2box.

قم بتشغيل الأمر التالي لرؤية أحجام docker التي تعمل على جهاز المضيف الخاص بك:

```{.copy}
docker volume ls
```

يجب أن ترى الأحجام التالية:

- wis2box_project_auth-data
- wis2box_project_es-data
- wis2box_project_htpasswd
- wis2box_project_minio-data
- wis2box_project_prometheus-data
- wis2box_project_loki-data
- wis2box_project_mosquitto-config

بالإضافة إلى بعض الأحجام المجهولة التي تستخدمها الحاويات المختلفة.

تُستخدم الأحجام التي تبدأ بـ `wis2box_project_` لتخزين البيانات المستمرة للخدمات المختلفة في حزمة برامج wis2box.

## واجهة برمجة تطبيقات wis2box

تحتوي wis2box على واجهة برمجة تطبيقات (API) توفر الوصول إلى البيانات والعمليات للتصور التفاعلي وتحويل البيانات والنشر.

افتح علامة تبويب جديدة وانتقل إلى الصفحة `http://YOUR-HOST/oapi`.

<img alt="wis2box-api.png" src="/../assets/img/wis2box-api.png" width="800">

هذه هي صفحة البداية لواجهة برمجة تطبيقات wis2box (تعمل عبر حاوية **wis2box-api**).

!!! question
     
     ما هي المجموعات المتاحة حاليًا؟

??? success "انقر لكشف الإجابة"
    
    لعرض المجموعات المتاحة حاليًا من خلال الواجهة، انقر على `View the collections in this service`:

    <img alt="wis2box-api-collections.png" src="/../assets/img/wis2box-api-collections.png" width="600">

    المجموعات المتاحة حاليًا هي:

    - المحطات
    - إشعارات البيانات
    - بيانات الاكتشاف


!!! question

    كم عدد إشعارات البيانات التي تم نشرها؟

??? success "انقر لكشف الإجابة"

بمجرد أن تكون متصلاً، تحقق من أن إحصائيات mosquitto الداخلية يتم نشرها بواسطة الوسيط الخاص بك تحت موضوع `$SYS`:

<img alt="mqtt-explorer-sys-topic.png" src="/../assets/img/mqtt-explorer-sys-topic.png" width="400">

احتفظ بـ MQTT Explorer مفتوحًا، حيث سنستخدمه لمراقبة الرسائل المنشورة على الوسيط.

## الخلاصة

!!! success "تهانينا!"
    في هذه الجلسة العملية، تعلمت كيفية:

    - تشغيل السكربت `wis2box-create-config.py` لإنشاء التكوين الأولي
    - بدء تشغيل wis2box والتحقق من حالة مكوناته
    - الوصول إلى wis2box-webapp و wis2box-API في المتصفح
    - الاتصال بوسيط MQTT على VM الطالب الخاص بك باستخدام MQTT Explorer
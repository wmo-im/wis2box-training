---
title: تهيئة wis2box
---

# تهيئة wis2box

!!! abstract "نتائج التعلم"

    بنهاية هذه الجلسة العملية، ستكون قادرًا على:

    - تشغيل سكربت `wis2box-create-config.py` لإنشاء الإعدادات الأولية
    - بدء تشغيل wis2box والتحقق من حالة مكوناته
    - عرض محتويات **wis2box-api**
    - الوصول إلى **wis2box-webapp**
    - الاتصال بـ **wis2box-broker** المحلي باستخدام MQTT Explorer

!!! note

    تعتمد المواد التدريبية الحالية على الإصدار wis2box-release 1.3.0.

    راجع [accessing-your-student-vm](./accessing-your-student-vm.md) للحصول على تعليمات حول كيفية تنزيل وتثبيت حزمة برامج wis2box إذا كنت تقوم بإجراء هذا التدريب خارج جلسة تدريب محلية.

## التحضير

قم بتسجيل الدخول إلى الجهاز الافتراضي المخصص لك باستخدام اسم المستخدم وكلمة المرور الخاصة بك، وتأكد من أنك في دليل `wis2box`:

```bash
cd ~/wis2box
```

## إنشاء الإعدادات الأولية

تتطلب الإعدادات الأولية لـ wis2box ما يلي:

- ملف بيئة `wis2box.env` يحتوي على معلمات التكوين
- دليل على الجهاز المضيف لمشاركته بين الجهاز المضيف وحاويات wis2box، يتم تعريفه بواسطة متغير البيئة `WIS2BOX_HOST_DATADIR`

يمكن استخدام سكربت `wis2box-create-config.py` لإنشاء الإعدادات الأولية لـ wis2box.

سيطلب منك مجموعة من الأسئلة للمساعدة في إعداد التكوين.

ستتمكن من مراجعة وتحديث ملفات التكوين بعد انتهاء السكربت.

قم بتشغيل السكربت كما يلي:

```bash
python3 wis2box-create-config.py
```

### دليل wis2box-host-data

سيطلب منك السكربت إدخال الدليل الذي سيتم استخدامه لمتغير البيئة `WIS2BOX_HOST_DATADIR`.

لاحظ أنه يجب عليك تحديد المسار الكامل لهذا الدليل.

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

### عنوان URL الخاص بـ wis2box

بعد ذلك، سيُطلب منك إدخال عنوان URL الخاص بـ wis2box. هذا هو عنوان URL الذي سيتم استخدامه للوصول إلى تطبيق الويب، وواجهة API، وواجهة المستخدم الخاصة بـ wis2box.

يرجى استخدام `http://<your-hostname-or-ip>` كعنوان URL.

```{.copy}
Please enter the URL of the wis2box:
 For local testing the URL is http://localhost
 To enable remote access, the URL should point to the public IP address or domain name of the server hosting the wis2box.
http://username.training.wis2dev.io
The URL of the wis2box will be set to:
  http://username.training.wis2dev.io
Is this correct? (y/n/exit)
```

### كلمات المرور لـ WEBAPP، STORAGE و BROKER

يمكنك استخدام خيار إنشاء كلمات مرور عشوائية عند المطالبة بـ `WIS2BOX_WEBAPP_PASSWORD`، `WIS2BOX_STORAGE_PASSWORD`، و `WIS2BOX_BROKER_PASSWORD` أو تحديد كلمات المرور الخاصة بك.

لا تقلق بشأن تذكر هذه الكلمات، حيث سيتم تخزينها في ملف `wis2box.env` داخل دليل wis2box الخاص بك.

### مراجعة ملف `wis2box.env`

بمجرد اكتمال السكربت، تحقق من محتويات ملف `wis2box.env` في الدليل الحالي:

```bash
cat ~/wis2box/wis2box.env
```

أو تحقق من محتويات الملف عبر WinSCP.

!!! question

    ما هي قيمة WISBOX_BASEMAP_URL في ملف wis2box.env؟

??? success "اضغط للكشف عن الإجابة"

    القيمة الافتراضية لـ WIS2BOX_BASEMAP_URL هي `https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png`.

    يشير هذا العنوان إلى خادم OpenStreetMap. إذا كنت ترغب في استخدام مزود خرائط مختلف، يمكنك تغيير هذا العنوان للإشارة إلى خادم خرائط آخر.

!!! question 

    ما هي قيمة متغير البيئة WIS2BOX_STORAGE_DATA_RETENTION_DAYS في ملف wis2box.env؟

??? success "اضغط للكشف عن الإجابة"

    القيمة الافتراضية لـ WIS2BOX_STORAGE_DATA_RETENTION_DAYS هي 30 يومًا. يمكنك تغيير هذه القيمة إلى عدد مختلف من الأيام إذا أردت.

    يقوم حاوية wis2box-management بتشغيل مهمة مجدولة يوميًا لإزالة البيانات الأقدم من عدد الأيام المحدد بواسطة WIS2BOX_STORAGE_DATA_RETENTION_DAYS من حاوية `wis2box-public` والواجهة الخلفية لـ API:

    ```{.copy}
    0 0 * * * su wis2box -c "wis2box data clean --days=$WIS2BOX_STORAGE_DATA_RETENTION_DAYS"
    ```

!!! note

    يحتوي ملف `wis2box.env` على متغيرات البيئة التي تحدد إعدادات wis2box. لمزيد من المعلومات، راجع [wis2box-documentation](https://docs.wis2box.wis.wmo.int/en/latest/reference/configuration.html).

    لا تقم بتحرير ملف `wis2box.env` إلا إذا كنت متأكدًا من التغييرات التي تقوم بها. قد تؤدي التغييرات غير الصحيحة إلى توقف wis2box عن العمل.

    لا تشارك محتويات ملف `wis2box.env` مع أي شخص، حيث يحتوي على معلومات حساسة مثل كلمات المرور.

## بدء تشغيل wis2box

تأكد من أنك في الدليل الذي يحتوي على ملفات تعريف حزمة برامج wis2box:

```{.copy}
cd ~/wis2box
```

ابدأ تشغيل wis2box باستخدام الأمر التالي:

```{.copy}
python3 wis2box-ctl.py start
```

عند تشغيل هذا الأمر لأول مرة، سترى الإخراج التالي:

```
No docker-compose.images-*.yml files found, creating one
Current version=Undefined, latest version=1.3.0
Would you like to update ? (y/n/exit)
```

اختر ``y`` وسيقوم السكربت بإنشاء الملف ``docker-compose.images-1.3.0.yml``، وتنزيل صور Docker المطلوبة وبدء الخدمات.

قد يستغرق تنزيل الصور بعض الوقت حسب سرعة اتصالك بالإنترنت. هذه الخطوة مطلوبة فقط في المرة الأولى التي تبدأ فيها تشغيل wis2box.

تحقق من الحالة باستخدام الأمر التالي:

```{.copy}
python3 wis2box-ctl.py status
```

كرر هذا الأمر حتى تكون جميع الخدمات قيد التشغيل.

!!! note "wis2box و Docker"
    يعمل wis2box كمجموعة من حاويات Docker التي تتم إدارتها بواسطة docker-compose.

    يتم تعريف الخدمات في ملفات `docker-compose*.yml` المختلفة الموجودة في دليل `~/wis2box/`.

    يتم استخدام سكربت Python `wis2box-ctl.py` لتشغيل أوامر Docker Compose الأساسية التي تتحكم في خدمات wis2box.

    لا تحتاج إلى معرفة تفاصيل حاويات Docker لتشغيل حزمة برامج wis2box، ولكن يمكنك فحص ملفات `docker-compose*.yml` لمعرفة كيفية تعريف الخدمات. إذا كنت مهتمًا بمعرفة المزيد عن Docker، يمكنك العثور على مزيد من المعلومات في [وثائق Docker](https://docs.docker.com/).

لتسجيل الدخول إلى حاوية wis2box-management، استخدم الأمر التالي:

```{.copy}
python3 wis2box-ctl.py login
```

لاحظ أنه بعد تسجيل الدخول، سيتغير الموجه الخاص بك، مما يشير إلى أنك الآن داخل حاوية wis2box-management:

```{bash}
root@025381da3c40:/home/wis2box#
```

داخل حاوية wis2box-management، يمكنك تشغيل أوامر مختلفة لإدارة wis2box الخاص بك، مثل:

- `wis2box auth add-token --path processes/wis2box` : لإنشاء رمز تفويض لنقطة النهاية *processes/wis2box*
- `wis2box data clean --days=<number-of-days>` : لتنظيف البيانات الأقدم من عدد معين من الأيام من حاوية *wis2box-public*

للخروج من الحاوية والعودة إلى جهازك المضيف، استخدم الأمر التالي:

```{.copy}
exit
```

قم بتشغيل الأمر التالي لرؤية حاويات Docker التي تعمل على جهازك المضيف:

```{.copy}
docker ps --format "table {{.Names}} \t{{.Status}} \t{{.Image}}"
```

يجب أن ترى الحاويات التالية قيد التشغيل:

```{bash}
NAMES                     STATUS                         IMAGE
nginx                     Up 56 seconds                  nginx:1.30.1-alpine
mqtt_metrics_collector    Up 58 seconds                  ghcr.io/world-meteorological-organization/wis2box-mqtt-metrics-collector:1.3.0
wis2box-auth              Up 59 seconds                  ghcr.io/world-meteorological-organization/wis2box-auth:1.3.0
wis2box-ui                Up About a minute              ghcr.io/world-meteorological-organization/wis2box-ui:1.3.0
wis2box-management        Up About a minute              ghcr.io/world-meteorological-organization/wis2box-management:1.3.0
wis2box-minio             Up 2 minutes (healthy)         ghcr.io/world-meteorological-organization/wis2box-minio:latest
wis2box-api               Up About a minute (healthy)    ghcr.io/world-meteorological-organization/wis2box-api:1.3.0
elasticsearch             Up 2 minutes (healthy)         docker.elastic.co/elasticsearch/elasticsearch:8.6.2
grafana                   Up 2 minutes                   grafana/grafana-oss:12.4.2
loki                      Up 2 minutes                   grafana/loki:2.4.1
elasticsearch-exporter    Up 2 minutes                   quay.io/prometheuscommunity/elasticsearch-exporter:latest
prometheus                Up 2 minutes                   prom/prometheus:v2.37.0
mosquitto                 Up 2 minutes                   ghcr.io/world-meteorological-organization/wis2box-broker:1.3.0
wis2box-webapp            Up 2 minutes (healthy)         ghcr.io/world-meteorological-organization/wis2box-webapp:1.3.0
```

تُعد هذه الحاويات جزءًا من مجموعة برامج `wis2box` وتوفر الخدمات المختلفة المطلوبة لتشغيل `wis2box`.

قم بتشغيل الأمر التالي لعرض وحدات التخزين الخاصة بـ Docker التي تعمل على جهازك:

```{.copy}
docker volume ls
```

يجب أن ترى وحدات التخزين التالية:

- wis2box_project_auth-data
- wis2box_project_es-data
- wis2box_project_minio-data
- wis2box_project_prometheus-data
- wis2box_project_loki-data
- wis2box_project_mosquitto-config

بالإضافة إلى بعض وحدات التخزين المجهولة التي تُستخدم بواسطة الحاويات المختلفة.

تُستخدم وحدات التخزين التي تبدأ بـ `wis2box_project_` لتخزين البيانات الدائمة للخدمات المختلفة في مجموعة برامج `wis2box`.

## واجهة برمجة التطبيقات (API) الخاصة بـ wis2box

تحتوي `wis2box` على واجهة برمجة تطبيقات (API) توفر الوصول إلى البيانات والعمليات للتصور التفاعلي وتحويل البيانات والنشر.

افتح علامة تبويب جديدة وانتقل إلى الصفحة `http://YOUR-HOST/oapi`.

<img alt="wis2box-api.png" src="/../assets/img/wis2box-api.png" width="800">

هذه هي الصفحة الرئيسية لواجهة برمجة التطبيقات الخاصة بـ `wis2box` (تعمل عبر الحاوية **wis2box-api**).

!!! question
     
     ما هي المجموعات المتوفرة حاليًا؟

??? success "اضغط لعرض الإجابة"
    
    لعرض المجموعات المتوفرة حاليًا عبر واجهة برمجة التطبيقات، اضغط على `View the collections in this service`:

    <img alt="wis2box-api-collections.png" src="/../assets/img/wis2box-api-collections.png" width="600">

    المجموعات التالية متوفرة حاليًا:

    - المحطات
    - إشعارات البيانات
    - بيانات الاكتشاف الوصفية


!!! question

    كم عدد إشعارات البيانات التي تم نشرها؟

??? success "اضغط لعرض الإجابة"

    اضغط على "إشعارات البيانات"، ثم اضغط على `Browse through the items of "Data Notifications"`. 
    
    ستلاحظ أن الصفحة تقول "No items" حيث لم يتم نشر أي إشعارات بيانات بعد.

## تطبيق الويب الخاص بـ wis2box

افتح متصفح الويب وانتقل إلى الصفحة `http://YOUR-HOST/wis2box-webapp`.

ستظهر نافذة منبثقة تطلب اسم المستخدم وكلمة المرور الخاصة بك. استخدم اسم المستخدم الافتراضي `wis2box-user` وكلمة المرور `WIS2BOX_WEBAPP_PASSWORD` المحددة في ملف `wis2box.env` واضغط على "Sign in":

!!! note 

    تحقق من ملف `wis2box.env` للحصول على قيمة `WIS2BOX_WEBAPP_PASSWORD`. يمكنك استخدام الأمر التالي للتحقق من قيمة هذا المتغير البيئي:

    ```{.copy}
    cat ~/wis2box/wis2box.env | grep WIS2BOX_WEBAPP_PASSWORD
    ```

بمجرد تسجيل الدخول، حرك مؤشر الماوس إلى القائمة الموجودة على اليسار لرؤية الخيارات المتاحة في تطبيق الويب الخاص بـ `wis2box`:

<img alt="wis2box-webapp-menu.png" src="/../assets/img/wis2box-webapp-menu.png" width="400">

هذا هو تطبيق الويب الخاص بـ `wis2box` الذي يتيح لك التفاعل مع `wis2box` الخاص بك:

- إنشاء وإدارة مجموعات البيانات
- تحديث/مراجعة بيانات المحطات الوصفية
- تحميل الملاحظات اليدوية باستخدام نموذج FM-12 synop
- مراقبة الإشعارات المنشورة على `wis2box-broker`

سنستخدم هذا التطبيق في جلسة لاحقة.

## الوسيط الخاص بـ wis2box

افتح تطبيق `MQTT Explorer` على جهاز الكمبيوتر الخاص بك وقم بإعداد اتصال جديد للاتصال بالوسيط الخاص بك (يعمل عبر الحاوية **wis2box-broker**).

اضغط على `+` لإضافة اتصال جديد:

<img alt="mqtt-explorer-new-connection.png" src="/../assets/img/mqtt-explorer-new-connection.png" width="300">

يمكنك الضغط على زر 'ADVANCED' والتحقق من أنك مشترك في المواضيع التالية:

- `#`
- `$SYS/#`

<img alt="mqtt-explorer-topics.png" src="/../assets/img/mqtt-explorer-topics.png" width="550">

!!! note

    الموضوع `#` هو اشتراك عام يشترك في جميع المواضيع المنشورة على الوسيط.

    الرسائل المنشورة تحت الموضوع `$SYS` هي رسائل نظام يتم نشرها بواسطة خدمة mosquitto نفسها.

استخدم تفاصيل الاتصال التالية، مع التأكد من استبدال قيمة `<your-host>` باسم المضيف الخاص بك وقيمة `<WIS2BOX_BROKER_PASSWORD>` بالقيمة الموجودة في ملف `wis2box.env` الخاص بك:

- **Protocol: mqtt://**
- **Host: `<your-host>`**
- **Port: 1883**
- **Username: wis2box**
- **Password: `<WIS2BOX_BROKER_PASSWORD>`**

!!! note 

    يمكنك التحقق من ملف `wis2box.env` للحصول على قيمة `WIS2BOX_BROKER_PASSWORD`. يمكنك استخدام الأمر التالي للتحقق من قيمة هذا المتغير البيئي:

    ```{.copy}
    cat ~/wis2box/wis2box.env | grep WIS2BOX_BROKER_PASSWORD
    ```

    لاحظ أن هذه هي كلمة المرور **الداخلية** الخاصة بالوسيط، وسيستخدم الوسيط العالمي بيانات اعتماد مختلفة (للقراءة فقط) للاشتراك في الوسيط الخاص بك. لا تشارك هذه الكلمة مع أي شخص.

تأكد من الضغط على "SAVE" لحفظ تفاصيل الاتصال الخاصة بك.

ثم اضغط على "CONNECT" للاتصال بـ **wis2box-broker**.

<img alt="mqtt-explorer-wis2box-broker-port1883.png" src="/../assets/img/mqtt-explorer-wis2box-broker-port1883.png" width="700">

بمجرد الاتصال، ستشاهد إحصائيات mosquitto الداخلية التي يتم نشرها بواسطة الوسيط الخاص بك تحت الموضوع `$SYS`:

<img alt="mqtt-explorer-sys-topic.png" src="/../assets/img/mqtt-explorer-sys-topic.png" width="400">

يمكن تحقيق نفس الاتصال باستخدام MQTT عبر WebSockets على المنفذ 80، باستخدام تفاصيل الاتصال التالية:

<img alt="mqtt-explorer-wis2box-broker-websockets.png" src="/../assets/img/mqtt-explorer-wis2box-broker-websockets.png" width="700">

## الخاتمة

!!! success "تهانينا!"
    في هذه الجلسة العملية، تعلمت كيفية:

    - تشغيل سكربت `wis2box-create-config.py` لإنشاء الإعداد الأولي
    - تشغيل `wis2box` والتحقق من حالة مكوناته
    - الوصول إلى `wis2box-webapp` و `wis2box-API` عبر المتصفح
    - الاتصال بوسيط MQTT على جهاز الطالب الخاص بك باستخدام `MQTT Explorer`
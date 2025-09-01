---
title: تنزيل البيانات من WIS2 باستخدام wis2downloader
---

# تنزيل البيانات من WIS2 باستخدام wis2downloader

!!! abstract "نتائج التعلم!"

    بنهاية هذه الجلسة العملية، ستكون قادرًا على:

    - استخدام "wis2downloader" للاشتراك في إشعارات بيانات WIS2 وتنزيل البيانات إلى نظامك المحلي
    - عرض حالة التنزيلات في لوحة معلومات Grafana
    - تعلم كيفية تكوين wis2downloader للاشتراك في وسيط غير افتراضي

## المقدمة

في هذه الجلسة، ستتعلم كيفية إعداد اشتراك في WIS2 Broker وتنزيل البيانات تلقائيًا إلى نظامك المحلي باستخدام خدمة "wis2downloader" المضمنة في wis2box.

!!! note "حول wis2downloader"
     
     يتوفر wis2downloader أيضًا كخدمة مستقلة يمكن تشغيلها على نظام مختلف عن النظام الذي ينشر إشعارات WIS2. راجع [wis2downloader](https://pypi.org/project/wis2downloader/) لمزيد من المعلومات حول استخدام wis2downloader كخدمة مستقلة.

     إذا كنت ترغب في تطوير خدمتك الخاصة للاشتراك في إشعارات WIS2 وتنزيل البيانات، يمكنك استخدام [كود المصدر الخاص بـ wis2downloader](https://github.com/World-Meteorological-Organization/wis2downloader) كمرجع.

## التحضير

قبل البدء، يرجى تسجيل الدخول إلى جهاز الطالب الافتراضي الخاص بك والتأكد من أن مثيل wis2box الخاص بك يعمل.

## أساسيات wis2downloader

يتم تضمين wis2downloader كحاوية منفصلة في wis2box كما هو محدد في ملفات Docker Compose. يتم تكوين حاوية Prometheus في wis2box لجمع المقاييس من حاوية wis2downloader، ويمكن عرض هذه المقاييس من خلال لوحة معلومات في Grafana.

### عرض لوحة معلومات wis2downloader في Grafana

افتح متصفح الويب وانتقل إلى لوحة معلومات Grafana لمثيل wis2box الخاص بك عن طريق الذهاب إلى `http://YOUR-HOST:3000`.

انقر على لوحات المعلومات في القائمة الجانبية، ثم اختر **لوحة معلومات wis2downloader**.

يجب أن ترى لوحة المعلومات التالية:

![wis2downloader dashboard](../assets/img/wis2downloader-dashboard.png)

تعتمد هذه اللوحة على المقاييس التي تنشرها خدمة wis2downloader وستعرض لك حالة التنزيلات الجارية حاليًا.

في الزاوية العلوية اليسرى، يمكنك رؤية الاشتراكات النشطة حاليًا.

احتفظ بهذه اللوحة مفتوحة حيث ستستخدمها لمراقبة تقدم التنزيل في التمرين التالي.

### مراجعة تكوين wis2downloader

يمكن تكوين خدمة wis2downloader في wis2box باستخدام المتغيرات البيئية المعرفة في ملف `wis2box.env` الخاص بك.

المتغيرات البيئية التالية تُستخدم بواسطة wis2downloader:

    - DOWNLOAD_BROKER_HOST: اسم المضيف الخاص بـ MQTT broker للاتصال به. الافتراضي هو globalbroker.meteo.fr
    - DOWNLOAD_BROKER_PORT: منفذ MQTT broker للاتصال به. الافتراضي هو 443 (HTTPS للويب سوكيت)
    - DOWNLOAD_BROKER_USERNAME: اسم المستخدم للاتصال بـ MQTT broker. الافتراضي هو everyone
    - DOWNLOAD_BROKER_PASSWORD: كلمة المرور للاتصال بـ MQTT broker. الافتراضي هو everyone
    - DOWNLOAD_BROKER_TRANSPORT: websockets أو tcp، آلية النقل للاتصال بـ MQTT broker. الافتراضي هو websockets
    - DOWNLOAD_RETENTION_PERIOD_HOURS: فترة الاحتفاظ بالبيانات التي تم تنزيلها بالساعات. الافتراضي هو 24
    - DOWNLOAD_WORKERS: عدد عمال التنزيل المستخدمين. الافتراضي هو 8. يحدد عدد التنزيلات المتوازية.
    - DOWNLOAD_MIN_FREE_SPACE_GB: الحد الأدنى للمساحة الحرة بالجيجابايت للحفاظ عليها على وحدة التخزين التي تستضيف التنزيلات. الافتراضي هو 1.

لمراجعة التكوين الحالي لـ wis2downloader، يمكنك استخدام الأمر التالي:

```bash
cat ~/wis2box/wis2box.env | grep DOWNLOAD
```

!!! question "مراجعة تكوين wis2downloader"
    
    ما هو MQTT broker الافتراضي الذي يتصل به wis2downloader؟

    ما هي فترة الاحتفاظ الافتراضية للبيانات التي تم تنزيلها؟

??? success "اضغط لعرض الإجابة"

    MQTT broker الافتراضي الذي يتصل به wis2downloader هو `globalbroker.meteo.fr`.

    فترة الاحتفاظ الافتراضية للبيانات التي تم تنزيلها هي 24 ساعة.

!!! note "تحديث تكوين wis2downloader"

    لتحديث تكوين wis2downloader، يمكنك تحرير ملف wis2box.env. لتطبيق التغييرات، يمكنك إعادة تشغيل أمر بدء تشغيل wis2box-stack:

    ```bash
    python3 wis2box-ctl.py start
    ```

    وسترى خدمة wis2downloader تعيد التشغيل بالتكوين الجديد.

يمكنك الاحتفاظ بالتكوين الافتراضي للتمرين التالي.

### واجهة سطر الأوامر لـ wis2downloader

للوصول إلى واجهة سطر الأوامر الخاصة بـ wis2downloader داخل wis2box، يمكنك تسجيل الدخول إلى حاوية **wis2downloader** باستخدام الأمر التالي:

```bash
python3 wis2box-ctl.py login wis2downloader
```

استخدم الأمر التالي لعرض الاشتراكات النشطة حاليًا:

```bash
wis2downloader list-subscriptions
```

سيعيد هذا الأمر قائمة فارغة، حيث لم يتم إعداد أي اشتراكات بعد.

## تنزيل بيانات GTS باستخدام WIS2 Global Broker

إذا احتفظت بالتكوين الافتراضي لـ wis2downloader، فهو متصل حاليًا بـ WIS2 Global Broker المستضاف بواسطة Météo-France.

### إعداد الاشتراك

استخدم الأمر التالي `cache/a/wis2/de-dwd-gts-to-wis2/#` للاشتراك في البيانات التي ينشرها GTS-to-WIS2 gateway المستضاف بواسطة DWD، والمتاحة من خلال Global Caches:

```bash
wis2downloader add-subscription --topic cache/a/wis2/de-dwd-gts-to-wis2/#
```

ثم اخرج من حاوية **wis2downloader** بكتابة `exit`:

```bash
exit
```

### التحقق من البيانات التي تم تنزيلها

تحقق من لوحة معلومات wis2downloader في Grafana لرؤية الاشتراك الجديد المضاف. انتظر بضع دقائق ويجب أن ترى التنزيلات الأولى تبدأ. انتقل إلى التمرين التالي بمجرد تأكيد بدء التنزيلات.

تقوم خدمة wis2downloader في wis2box بتنزيل البيانات في دليل 'downloads' في الدليل الذي حددته كـ `WIS2BOX_HOST_DATADIR` في ملف `wis2box.env` الخاص بك. لعرض محتويات دليل التنزيلات، استخدم الأمر التالي:

```bash
ls -R ~/wis2box-data/downloads
```

لاحظ أن البيانات التي تم تنزيلها يتم تخزينها في أدلة مسماة بناءً على الموضوع الذي تم نشر إشعار WIS2 عليه.

!!! question "عرض البيانات التي تم تنزيلها"

    ما هي الأدلة التي تراها في دليل التنزيلات؟

    هل يمكنك رؤية أي ملفات تم تنزيلها في هذه الأدلة؟

??? success "اضغط لعرض الإجابة"
    يجب أن ترى بنية دليل تبدأ بـ `cache/a/wis2/de-dwd-gts-to-wis2/` تحتها ستجد المزيد من الأدلة المسماة بناءً على رؤوس نشرات GTS للبيانات التي تم تنزيلها.

    بناءً على وقت بدء الاشتراك، قد ترى أو لا ترى أي ملفات تم تنزيلها في هذا الدليل بعد. إذا لم ترَ أي ملفات بعد، انتظر بضع دقائق أخرى وتحقق مرة أخرى.

دعونا ننظف الاشتراك والبيانات التي تم تنزيلها قبل الانتقال إلى التمرين التالي.

سجل الدخول مرة أخرى إلى حاوية wis2downloader:

```bash
python3 wis2box-ctl.py login wis2downloader
```

وأزل الاشتراك الذي قمت به من wis2downloader باستخدام الأمر التالي:

```bash
wis2downloader remove-subscription --topic cache/a/wis2/de-dwd-gts-to-wis2/#
```

قم بإزالة البيانات التي تم تنزيلها باستخدام الأمر التالي:

```bash
rm -rf /wis2box-data/downloads/cache/*
```

واخرج من حاوية wis2downloader بكتابة `exit`:
    
```bash
exit
```

تحقق من لوحة معلومات wis2downloader في Grafana لرؤية الاشتراك الذي تمت إزالته. يجب أن ترى التنزيلات تتوقف.

!!! note "حول بوابات GTS-to-WIS2"
    هناك حاليًا بوابتان GTS-to-WIS2 تنشران البيانات من خلال WIS2 Global Broker وGlobal Caches:

    - DWD (ألمانيا): centre-id=*de-dwd-gts-to-wis2*
    - JMA (اليابان): centre-id=*jp-jma-gts-to-wis2*
    
    إذا استبدلت في التمرين السابق `de-dwd-gts-to-wis2` بـ `jp-jma-gts-to-wis2`، ستتلقى الإشعارات والبيانات التي تنشرها بوابة JMA GTS-to-WIS2.

!!! note "مواضيع الأصل مقابل مواضيع التخزين المؤقت"

    عند الاشتراك في موضوع يبدأ بـ `origin/`، ستتلقى إشعارات تحتوي على عنوان URL قانوني يشير إلى خادم بيانات يوفره مركز WIS الذي ينشر البيانات.

    عند الاشتراك في موضوع يبدأ بـ `cache/`، ستتلقى إشعارات متعددة لنفس البيانات، واحدة لكل Global Cache. ستحتوي كل إشعار على عنوان URL قانوني يشير إلى خادم البيانات الخاص بـ Global Cache المعني. سيقوم wis2downloader بتنزيل البيانات من أول عنوان URL قانوني يمكن الوصول إليه.

## تنزيل بيانات تجريبية من WIS2 Training Broker

في هذا التمرين، ستشترك في WIS2 Training Broker الذي ينشر بيانات تجريبية لأغراض التدريب.

### تغيير تكوين wis2downloader

هذا يوضح كيفية الاشتراك في وسيط ليس الوسيط الافتراضي، مما يتيح لك تنزيل بعض البيانات المنشورة من WIS2 Training Broker.

قم بتحرير ملف `wis2box.env` وقم بتغيير `DOWNLOAD_BROKER_HOST` إلى `wis2training-broker.wis2dev.io`، و`DOWNLOAD_BROKER_PORT` إلى `1883`، و`DOWNLOAD_BROKER_TRANSPORT` إلى `tcp`:

```copy
# إعدادات التنزيل
DOWNLOAD_BROKER_HOST=wis2training-broker.wis2dev.io
DOWNLOAD_BROKER_PORT=1883
DOWNLOAD_BROKER_USERNAME=everyone
DOWNLOAD_BROKER_PASSWORD=everyone
# آلية نقل التنزيل (tcp أو websockets)
DOWNLOAD_BROKER_TRANSPORT=tcp
```

ثم قم بتشغيل الأمر 'start' مرة أخرى لتطبيق التغييرات:

```bash
python3 wis2box-ctl.py start
```

تحقق من سجلات wis2downloader لمعرفة ما إذا تم الاتصال بالوسيط الجديد بنجاح:

```bash
docker logs wis2downloader
```

يجب أن ترى رسالة السجل التالية:

```copy
...
INFO - Connecting...
INFO - Host: wis2training-broker.wis2dev.io, port: 1883
INFO - Connected successfully
```

### إعداد اشتراكات جديدة

الآن سنقوم بإعداد اشتراك جديد للموضوع لتنزيل بيانات مسار الأعاصير من WIS2 Training Broker.

قم بتسجيل الدخول إلى حاوية **wis2downloader**:

```bash
python3 wis2box-ctl.py login wis2downloader
```

وقم بتنفيذ الأمر التالي (انسخه والصقه لتجنب الأخطاء الإملائية):

```bash
wis2downloader add-subscription --topic origin/a/wis2/int-wis2-training/data/core/weather/prediction/forecast/medium-range/probabilistic/trajectory
```

اخرج من حاوية **wis2downloader** بكتابة `exit`.

### التحقق من البيانات التي تم تنزيلها

انتظر حتى ترى بدء التنزيلات في لوحة معلومات wis2downloader في Grafana.

تحقق من تنزيل البيانات عن طريق التحقق من سجلات wis2downloader مرة أخرى باستخدام:

```bash
docker logs wis2downloader
```

يجب أن ترى رسالة سجل مشابهة لما يلي:

```copy
[...] INFO - Message received under topic origin/a/wis2/int-wis2-training/data/core/weather/prediction/forecast/medium-range/probabilistic/trajectory
[...] INFO - Downloaded A_JSXX05ECEP020000_C_ECMP_...
```

تحقق من محتويات دليل التنزيلات مرة أخرى:

```bash
ls -R ~/wis2box-data/downloads
```

يجب أن ترى دليلًا جديدًا باسم `origin/a/wis2/int-wis2-training/data/core/weather/prediction/forecast/medium-range/probabilistic/trajectory` يحتوي على البيانات التي تم تنزيلها.

!!! question "مراجعة البيانات التي تم تنزيلها"
    
    ما هو تنسيق الملفات للبيانات التي تم تنزيلها؟

??? success "اضغط للكشف عن الإجابة"

    البيانات التي تم تنزيلها بتنسيق BUFR كما هو موضح بامتداد الملف `.bufr`.

بعد ذلك، حاول إضافة اشتراكين آخرين لتنزيل بيانات شذوذ درجة حرارة السطح الشهرية وبيانات التنبؤ العالمي من الموضوعات التالية:

- `origin/a/wis2/int-wis2-training/data/core/weather/prediction/forecast/medium-range/probabilistic/global`
- `origin/a/wis2/int-wis2-training/data/core/climate/experimental/anomalies/monthly/surface-temperature`

انتظر حتى ترى بدء التنزيلات في لوحة معلومات wis2downloader في Grafana.

تحقق من محتويات دليل التنزيلات مرة أخرى:

```bash
ls -R ~/wis2box-data/downloads
```

يجب أن ترى دليلين جديدين بأسماء `origin/a/wis2/int-wis2-training/data/core/weather/prediction/forecast/medium-range/probabilistic/global` و`origin/a/wis2/int-wis2-training/data/core/climate/experimental/anomalies/monthly/surface-temperature` يحتويان على البيانات التي تم تنزيلها.

!!! question "مراجعة البيانات التي تم تنزيلها للموضوعين الجديدين"
    
    ما هو تنسيق الملفات للبيانات التي تم تنزيلها للموضوع `../prediction/forecast/medium-range/probabilistic/global`؟

    ما هو تنسيق الملفات للبيانات التي تم تنزيلها للموضوع `../climate/experimental/anomalies/monthly/surface-temperature`؟

??? success "اضغط للكشف عن الإجابة"

    البيانات التي تم تنزيلها للموضوع `../prediction/forecast/medium-range/probabilistic/global` بتنسيق GRIB2 كما هو موضح بامتداد الملف `.grib2`.

    البيانات التي تم تنزيلها للموضوع `../climate/experimental/anomalies/monthly/surface-temperature` بتنسيق NetCDF كما هو موضح بامتداد الملف `.nc`.

## الخاتمة

!!! success "تهانينا!"

    في هذه الجلسة العملية، تعلمت كيفية:

    - استخدام 'wis2downloader' للاشتراك في WIS2 Broker وتنزيل البيانات إلى نظامك المحلي
    - عرض حالة التنزيلات في لوحة معلومات Grafana
    - كيفية تغيير الإعداد الافتراضي لـ wis2downloader للاشتراك في وسيط مختلف
    - كيفية عرض البيانات التي تم تنزيلها على نظامك المحلي
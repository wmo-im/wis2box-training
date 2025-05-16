---
title: تكوين بيانات المحطة الوصفية
---

# تكوين بيانات المحطة الوصفية

!!! abstract "نتائج التعلم"

    بنهاية هذه الجلسة العملية، ستكون قادرًا على:

    - إنشاء رمز تفويض لنقطة النهاية `collections/stations`
    - إضافة بيانات وصفية للمحطة إلى wis2box
    - تحديث/حذف بيانات المحطة الوصفية باستخدام **wis2box-webapp**

## مقدمة

لمشاركة البيانات دوليًا بين أعضاء المنظمة العالمية للأرصاد الجوية، من المهم أن يكون هناك فهم مشترك للمحطات التي تنتج البيانات. يوفر نظام المراقبة العالمي المتكامل (WIGOS) إطارًا لتكامل أنظمة المراقبة وأنظمة إدارة البيانات. يُستخدم **معرف محطة WIGOS (WSI)** كمرجع فريد للمحطة التي أنتجت مجموعة محددة من بيانات المراقبة.

يحتوي wis2box على مجموعة من بيانات المحطة الوصفية التي تُستخدم لوصف المحطات التي تنتج بيانات المراقبة ويجب استرجاعها من **OSCAR/Surface**. تُستخدم بيانات المحطة الوصفية في wis2box بواسطة أدوات تحويل BUFR للتحقق من أن البيانات المدخلة تحتوي على معرف محطة WIGOS (WSI) صالح ولتوفير تعيين بين WSI وبيانات المحطة الوصفية.

## إنشاء رمز تفويض لـ collections/stations

لتحرير المحطات عبر **wis2box-webapp** ستحتاج أولاً إلى إنشاء رمز تفويض.

قم بتسجيل الدخول إلى جهاز الطالب الافتراضي الخاص بك وتأكد من أنك في دليل `wis2box`:

```bash
cd ~/wis2box
```

ثم قم بتسجيل الدخول إلى حاوية **wis2box-management** باستخدام الأمر التالي:

```bash
python3 wis2box-ctl.py login
```

داخل حاوية **wis2box-management** يمكنك إنشاء رمز تفويض لنقطة نهاية محددة باستخدام الأمر: `wis2box auth add-token --path <my-endpoint>`.

على سبيل المثال، لاستخدام رمز تلقائي عشوائي مُنشأ لنقطة النهاية `collections/stations`:

```{.copy}
wis2box auth add-token --path collections/stations
```	

سيظهر الإخراج كما يلي:

```{.copy}
Continue with token: 7ca20386a131f0de384e6ffa288eb1ae385364b3694e47e3b451598c82e899d1 [y/N]? y
Token successfully created
```

أو، إذا كنت ترغب في تحديد رمزك الخاص لنقطة النهاية `collections/stations`، يمكنك استخدام المثال التالي:

```{.copy}
wis2box auth add-token --path collections/stations DataIsMagic
```

الإخراج:
    
```{.copy}
Continue with token: DataIsMagic [y/N]? y
Token successfully created
```

يرجى إنشاء رمز تفويض لنقطة النهاية `collections/stations` باستخدام التعليمات المذكورة أعلاه.

## إضافة بيانات المحطة الوصفية باستخدام **wis2box-webapp**

يوفر **wis2box-webapp** واجهة مستخدم رسومية لتحرير بيانات المحطة الوصفية.

افتح **wis2box-webapp** في متصفحك بالانتقال إلى `http://YOUR-HOST/wis2box-webapp`، واختر المحطات:

<img alt="wis2box-webapp-select-stations" src="/../assets/img/wis2box-webapp-select-stations.png" width="250">

عند النقر على 'إضافة محطة جديدة'، سيُطلب منك توفير معرف محطة WIGOS للمحطة التي تريد إضافتها:

<img alt="wis2box-webapp-import-station-from-oscar" src="/../assets/img/wis2box-webapp-import-station-from-oscar.png" width="800">

!!! note "إضافة بيانات وصفية للمحطة لثلاث محطات أو أكثر"
    يرجى إضافة ثلاث محطات أو أكثر إلى مجموعة بيانات المحطة الوصفية wis2box الخاصة بك.
      
    يرجى استخدام المحطات من بلدك إذا أمكن، خاصة إذا كنت قد جلبت بياناتك الخاصة.
      
    إذا لم يكن لدى بلدك أي محطات في OSCAR/Surface، يمكنك استخدام المحطات التالية لغرض هذا التمرين:

      - 0-20000-0-91334
      - 0-20000-0-96323 (لاحظ عدم وجود ارتفاع المحطة في OSCAR)
      - 0-20000-0-96749 (لاحظ عدم وجود ارتفاع المحطة في OSCAR)

عند النقر على البحث، يتم استرجاع بيانات المحطة من OSCAR/Surface، يرجى ملاحظة أن هذا قد يستغرق بضع ثوان.

راجع البيانات التي تم إرجاعها من OSCAR/Surface وأضف البيانات المفقودة حسب الحاجة. اختر موضوعًا للمحطة وقدم رمز التفويض الخاص بك لنقطة النهاية `collections/stations` وانقر على 'حفظ':

<img alt="wis2box-webapp-create-station-save" src="/../assets/img/wis2box-webapp-create-station-save.png" width="800">

<img alt="wis2box-webapp-create-station-success" src="/../assets/img/wis2box-webapp-create-station-success.png" width="500">

عد إلى قائمة المحطات وسترى المحطة التي أضفتها:

<img alt="wis2box-webapp-stations-with-one-station" src="/../assets/img/wis2box-webapp-stations-with-one-station.png" width="800">

كرر هذه العملية حتى يكون لديك ثلاث محطات على الأقل مكونة.

!!! tip "استخراج معلومات الارتفاع المفقودة"

    إذا كان ارتفاع محطتك مفقودًا، هناك خدمات عبر الإنترنت للمساعدة في البحث عن الارتفاع باستخدام بيانات الارتفاع المفتوحة. أحد هذه الأمثلة هو [واجهة برمجة تطبيقات Open Topo Data](https://www.opentopodata.org).

    على سبيل المثال، للحصول على الارتفاع عند خط العرض -6.15558 وخط الطول 106.84204، يمكنك نسخ ولصق الرابط التالي في علامة تبويب متصفح جديدة:

    ```{.copy}
    https://api.opentopodata.org/v1/aster30m?locations=-6.15558,106.84204
    ```

    الإخراج:

    ```{.copy}
    {
      "results": [
        {
          "dataset": "aster30m", 
          "elevation": 7.0, 
          "location": {
            "lat": -6.15558, 
            "lng": 106.84204
          }
        }
      ], 
      "status": "OK"
    }
    ```

## مراجعة بيانات المحطة الوصفية الخاصة بك

تُخزن بيانات المحطة الوصفية في الخلفية لـ wis2box وتتاح عبر **wis2box-api**.

إذا فتحت متصفحًا وانتقلت إلى `http://YOUR-HOST/oapi/collections/stations/items` سترى بيانات المحطة الوصفية التي أضفتها:

<img alt="wis2box-api-stations" src="/../assets/img/wis2box-api-stations.png" width="800">

!!! note "مراجعة بيانات المحطة الوصفية الخاصة بك"

    تحقق من أن المحطات التي أضفتها مرتبطة بمجموعة البيانات الخاصة بك بزيارة `http://YOUR-HOST/oapi/collections/stations/items` في متصفحك.

لديك أيضًا خيار عرض/تحديث/حذف المحطة في **wis2box-webapp**. لاحظ أنه يتعين عليك تقديم رمز التفويض الخاص بك لنقطة النهاية `collections/stations` لتحديث/حذف المحطة.

!!! note "تحديث/حذف بيانات المحطة الوصفية"

    حاول وانظر إذا كان بإمكانك تحديث/حذف بيانات المحطة الوصفية لإحدى المحطات التي أضفتها باستخدام **wis2box-webapp**.

## تحميل بيانات المحطة الوصفية بالجملة

لاحظ أن لدى wis2box أيضًا القدرة على تحميل بيانات المحطة الوصفية "بالجملة" من ملف CSV باستخدام سطر الأوامر في حاوية **wis2box-management**.

```bash
python3 wis2box-ctl.py login
wis2box metadata station publish-collection -p /data/wis2box/metadata/station/station_list.csv -th origin/a/wis2/centre-id/weather/surface-based-observations/synop
```

هذا يتيح لك تحميل عدد كبير من المحطات دفعة واحدة وربطها بموضوع محدد.

يمكنك إنشاء ملف CSV باستخدام Excel أو محرر نصوص ثم تحميله إلى wis2box-host-datadir لجعله متاحًا لحاوية **wis2box-management** في دليل `/data/wis2box/`.

بعد إجراء تحميل بيانات المحطة بالجملة، يُوصى بمراجعة المحطات في **wis2box-webapp** للتأكد من تحميل البيانات بشكل صحيح.

راجع الوثائق الرسمية لـ [wis2box](https://docs.wis2box.wis.wmo.int) لمزيد من المعلومات حول كيفية استخدام هذه الميزة.

## خاتمة

!!! success "تهانينا!"
    في هذه الجلسة العملية، تعلمت كيفية:

    - إنشاء رمز تفويض لنقطة النهاية `collections/stations` لاستخدامه مع **wis2box-webapp**
    - إضافة بيانات المحطة الوصفية إلى wis2box باستخدام **wis2box-webapp**
    - عرض/تحديث/حذف بيанات المحطة الوصفية باستخدام **wis2box-webapp**
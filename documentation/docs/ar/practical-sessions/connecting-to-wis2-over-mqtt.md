---
title: الاتصال بـ WIS2 عبر MQTT
---

# الاتصال بـ WIS2 عبر MQTT

!!! abstract "نتائج التعلم"

    بنهاية هذه الجلسة العملية، ستكون قادرًا على:

    - الاتصال بـ WIS2 Global Broker باستخدام MQTT Explorer
    - مراجعة هيكل الموضوعات في WIS2
    - مراجعة هيكل رسائل الإشعارات في WIS2

## المقدمة

يستخدم WIS2 بروتوكول MQTT للإعلان عن توفر بيانات الطقس/المناخ/المياه. يقوم WIS2 Global Broker بالاشتراك في جميع WIS2 Nodes في الشبكة ويعيد نشر الرسائل التي يتلقاها. يقوم Global Cache بالاشتراك في Global Broker، وتنزيل البيانات الموجودة في الرسالة، ثم يعيد نشر الرسالة على موضوع `cache` مع عنوان URL جديد. ينشر Global Discovery Catalogue بيانات الاكتشاف الوصفية من Broker ويوفر واجهة برمجة تطبيقات للبحث.

هذا مثال على هيكل رسالة إشعار WIS2 لرسالة تم استلامها على الموضوع `origin/a/wis2/br-inmet/data/core/weather/surface-based-observations/synop`:

```json
{
   "id":"3c14d7bf-e6b9-4f59-b4ea-f2fc52a33cd3",
   "type":"Feature",
   "conformsTo":[
      "http://wis.wmo.int/spec/wnm/1/conf/core"
   ],
   "geometry":{
      "coordinates":[
         -99.1964,
         19.404,
         2314
      ],
      "type":"Point"
   },
   "properties":{
      "data_id":"br-inmet:data:core:weather:surface-based-observations:synop/WIGOS_0-20000-0-76679_20250206T231600",
      "datetime":"2025-02-06T23:16:00Z",
      "pubtime":"2026-01-20T13:14:52Z",
      "integrity":{
         "method":"sha512",
         "value":"qtlI3Noay2I4zcdA1XCpn8vzVLIt0RKrR398VGFgTttc1XRUVb4dHWNCDKPXUo4mNkiFKx5TTHBvrxlzqWmMnQ=="
      },
      "metadata_id":"urn:wmo:md:br-inmet:data:core:weather:surface-based-observations:synop",
      "wigos_station_identifier":"0-20000-0-76679"
   },
   "links":[
      {
         "rel":"canonical",
         "type":"application/bufr",
         "href":"http://localhost/data/2025-02-06/wis/urn:wmo:md:br-inmet:data:core:weather:surface-based-observations:synop/WIGOS_0-20000-0-76679_20250206T231600.bufr4",
         "length":125117
      },
      {
         "rel":"via",
         "type":"text/html",
         "href":"https://oscar.wmo.int/surface/#/search/station/stationReportDetails/0-20000-0-76679"
      }
   ],
   "generated_by":"wis2box 1.2.0"
}
```

في هذه الجلسة العملية، ستتعلم كيفية استخدام أداة MQTT Explorer لإعداد اتصال عميل MQTT بـ WIS2 Global Broker وعرض رسائل إشعارات WIS2.

يعد MQTT Explorer أداة مفيدة لتصفح ومراجعة هيكل الموضوعات لأي MQTT broker لمراجعة البيانات التي يتم نشرها.

!!! note "حول MQTT"
    يوفر MQTT Explorer واجهة سهلة الاستخدام للاتصال بـ MQTT broker واستكشاف الموضوعات وهيكل الرسائل المستخدمة في WIS2.
    
    في الممارسة العملية، يتم استخدام MQTT للتواصل بين الآلات، حيث يشترك تطبيق أو خدمة في الموضوعات ويعالج الرسائل برمجيًا في الوقت الفعلي.
    
    للعمل مع MQTT برمجيًا (على سبيل المثال، باستخدام Python)، يمكنك استخدام مكتبات عملاء MQTT مثل [paho-mqtt](https://pypi.org/project/paho-mqtt) للاتصال بـ MQTT broker ومعالجة الرسائل الواردة. هناك العديد من برامج العملاء والخوادم لـ MQTT، بناءً على متطلباتك وبيئتك التقنية.

## استخدام MQTT Explorer للاتصال بـ Global Broker

لعرض الرسائل التي ينشرها WIS2 Global Broker، يمكنك استخدام "MQTT Explorer" الذي يمكن تنزيله من [موقع MQTT Explorer](https://mqtt-explorer.com).

افتح MQTT Explorer وأضف اتصالًا جديدًا بـ Global Broker المستضاف بواسطة MeteoFrance باستخدام التفاصيل التالية:

- host: globalbroker.meteo.fr
- port: 8883
- username: everyone
- password: everyone

<img alt="mqtt-explorer-global-broker-connection" src="/../assets/img/mqtt-explorer-global-broker-connection.png" width="800">

انقر على زر 'ADVANCED'، وقم بإزالة الموضوعات المُعدة مسبقًا وأضف الموضوعات التالية للاشتراك فيها:

- `origin/a/wis2/#`

<img alt="mqtt-explorer-global-broker-advanced" src="/../assets/img/mqtt-explorer-global-broker-sub-origin.png" width="800">

!!! note
    عند إعداد اشتراكات MQTT، يمكنك استخدام الرموز العامة التالية:

    - **مستوى واحد (+)**: الرمز العام لمستوى واحد يستبدل مستوى واحد من الموضوع
    - **متعدد المستويات (#)**: الرمز العام متعدد المستويات يستبدل مستويات متعددة من الموضوع

    في هذه الحالة، `origin/a/wis2/#` سيشترك في جميع الموضوعات تحت الموضوع `origin/a/wis2`.

انقر على 'BACK'، ثم 'SAVE' لحفظ تفاصيل الاتصال والاشتراك. ثم انقر على 'CONNECT':

يجب أن تبدأ الرسائل في الظهور في جلسة MQTT Explorer كما يلي:

<img alt="mqtt-explorer-global-broker-topics" src="/../assets/img/mqtt-explorer-global-broker-msg-origin.png" width="800">

أنت الآن جاهز لبدء استكشاف موضوعات WIS2 وهيكل الرسائل.

## التمرين 1: مراجعة هيكل الموضوعات في WIS2

استخدم MQTT لتصفح هيكل الموضوعات تحت موضوعات `origin`.

!!! question
    
    كيف يمكننا التمييز بين مركز WIS الذي نشر البيانات؟

??? success "انقر للكشف عن الإجابة"

    يمكنك النقر على نافذة الجانب الأيسر في MQTT Explorer لتوسيع هيكل الموضوعات.
    
    يمكننا التمييز بين مركز WIS الذي نشر البيانات من خلال النظر إلى المستوى الرابع من هيكل الموضوعات. على سبيل المثال، الموضوع التالي:

    `origin/a/wis2/br-inmet/data/core/weather/surface-based-observations/synop`

    يخبرنا أن البيانات تم نشرها من مركز WIS مع المعرف `br-inmet`، وهو المعرف الخاص بـ Instituto Nacional de Meteorologia - INMET، البرازيل.

!!! question

    كيف يمكننا التمييز بين الرسائل المنشورة من مراكز WIS التي تستضيف بوابة GTS-to-WIS2 والرسائل المنشورة من مراكز WIS التي تستضيف WIS2 Node؟

??? success "انقر للكشف عن الإجابة"

    يمكننا التمييز بين الرسائل القادمة من بوابة GTS-to-WIS2 من خلال النظر إلى معرف المركز في هيكل الموضوعات. على سبيل المثال، الموضوع التالي:

    `origin/a/wis2/de-dwd-gts-to-wis2/data/core/I/S/A/I/01/sbbr`

    يخبرنا أن البيانات تم نشرها من بوابة GTS-to-WIS2 المستضافة بواسطة Deutscher Wetterdienst (DWD)، ألمانيا. بوابة GTS-to-WIS2 هي نوع خاص من ناشري البيانات الذين ينشرون البيانات من نظام الاتصالات العالمي (GTS) إلى WIS2. يتكون هيكل الموضوعات من رؤوس TTAAii CCCC لرسائل GTS.

## التمرين 2: مراجعة هيكل رسائل WIS2

افصل الاتصال بـ MQTT Explorer وقم بتحديث قسم 'Advanced' لتغيير الاشتراك إلى ما يلي:

* `origin/a/wis2/+/data/core/weather/surface-based-observations/synop`
* `cache/a/wis2/+/data/core/weather/surface-based-observations/synop`

<img alt="mqtt-explorer-global-broker-topics-exercise2" src="/../assets/img/mqtt-explorer-global-broker-sub-origin-cache-synop.png" width="800">

!!! note
    يتم استخدام الرمز العام `+` للاشتراك في جميع مراكز WIS.

أعد الاتصال بـ Global Broker وانتظر ظهور الرسائل.

يمكنك عرض محتوى رسالة WIS2 في قسم "Value" على الجانب الأيمن. حاول توسيع هيكل الموضوعات لرؤية المستويات المختلفة للرسالة حتى تصل إلى المستوى الأخير ومراجعة محتوى إحدى الرسائل.

!!! question

    كيف يمكننا تحديد الطابع الزمني الذي تم فيه نشر البيانات؟ وكيف يمكننا تحديد الطابع الزمني الذي تم فيه جمع البيانات؟

??? success "انقر للكشف عن الإجابة"

    الطابع الزمني الذي تم فيه نشر البيانات موجود في قسم `properties` من الرسالة مع المفتاح `pubtime`.

    الطابع الزمني الذي تم فيه جمع البيانات موجود في قسم `properties` من الرسالة مع المفتاح `datetime`.

    <img alt="mqtt-explorer-global-broker-msg-properties" src="/../assets/img/mqtt-explorer-global-broker-msg-properties.png" width="800">

!!! question

    كيف يمكننا تنزيل البيانات من عنوان URL المقدم في الرسالة؟

??? success "انقر للكشف عن الإجابة"

    عنوان URL موجود في قسم `links` مع `rel="canonical"` ويتم تعريفه بواسطة المفتاح `href`.

    يمكنك نسخ عنوان URL ولصقه في متصفح ويب لتنزيل البيانات.

## التمرين 3: مراجعة الفرق بين موضوعات 'origin' و 'cache'

تأكد من أنك لا تزال متصلًا بـ Global Broker باستخدام اشتراكات الموضوعات `origin/a/wis2/+/data/core/weather/surface-based-observations/synop` و `cache/a/wis2/+/data/core/weather/surface-based-observations/synop` كما هو موضح في التمرين 2.

حاول تحديد رسالة لنفس معرف المركز المنشورة على كل من موضوعات `origin` و `cache`.

!!! question

    ما الفرق بين الرسائل المنشورة على موضوعات `origin` و `cache`؟

??? success "انقر للكشف عن الإجابة"

    الرسائل المنشورة على موضوعات `origin` هي الرسائل الأصلية التي يعيد Global Broker نشرها من WIS2 Nodes في الشبكة.

    الرسائل المنشورة على موضوعات `cache` هي الرسائل التي تم تنزيل البيانات الخاصة بها بواسطة Global Cache. إذا قمت بفحص محتوى الرسالة من الموضوع الذي يبدأ بـ `cache`، ستلاحظ أن الرابط 'canonical' قد تم تحديثه إلى عنوان URL جديد.
    
    هناك العديد من Global Caches في شبكة WIS2، لذلك ستتلقى رسالة واحدة من كل Global Cache قامت بتنزيل الرسالة.

    يقوم Global Cache فقط بتنزيل وإعادة نشر الرسائل التي تم نشرها على التسلسل الهرمي للموضوعات `../data/core/...`.

## الخاتمة

!!! success "تهانينا!"
    في هذه الجلسة العملية، تعلمت:

    - كيفية الاشتراك في خدمات WIS2 Global Broker باستخدام MQTT Explorer
    - هيكل الموضوعات في WIS2
    - هيكل رسائل الإشعارات في WIS2
    - الفرق بين البيانات الأساسية والموصى بها
    - هيكل الموضوعات المستخدم بواسطة بوابة GTS-to-WIS2
    - الفرق بين رسائل Global Broker المنشورة على موضوعات `origin` و `cache`
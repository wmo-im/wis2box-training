---
title: الاتصال بـ WIS2 عبر MQTT
---

# الاتصال بـ WIS2 عبر MQTT

!!! abstract "نتائج التعلم"

    بنهاية هذه الجلسة العملية، ستكون قادرًا على:

    - الاتصال بـ Global Broker الخاص بـ WIS2 باستخدام MQTT Explorer
    - مراجعة هيكل موضوع WIS2
    - مراجعة هيكل رسالة الإشعارات في WIS2

## مقدمة

يستخدم WIS2 بروتوكول MQTT للإعلان عن توفر بيانات الطقس/المناخ/المياه. يشترك Global Broker الخاص بـ WIS2 في جميع WIS2 Nodes في الشبكة ويعيد نشر الرسائل التي يتلقاها. يشترك Global Cache في Global Broker، يقوم بتنزيل البيانات في الرسالة ثم يعيد نشر الرسالة على موضوع `cache` برابط URL جديد. ينشر Global Discovery Catalogue بيانات الاكتشاف من الوسيط ويوفر واجهة برمجة تطبيقات للبحث.

هذا مثال على هيكل رسالة الإشعارات في WIS2 لرسالة تم استلامها على الموضوع `origin/a/wis2/br-inmet/data/core/weather/surface-based-observations/synop`:	

```json
{
  "id": "59f9b013-c4b3-410a-a52d-fff18f3f1b47",
  "type": "Feature",
  "version": "v04",
  "geometry": {
    "coordinates": [
      -38.69389,
      -17.96472,
      60
    ],
    "type": "Point"
  },
  "properties": {
    "data_id": "br-inmet/data/core/weather/surface-based-observations/synop/WIGOS_0-76-2-2900801000W83499_20240815T060000",
    "datetime": "2024-08-15T06:00:00Z",
    "pubtime": "2024-08-15T09:52:02Z",
    "integrity": {
      "method": "sha512",
      "value": "TBuWycx/G0lIiTo47eFPBViGutxcIyk7eikppAKPc4aHgOmTIS5Wb9+0v3awMOyCgwpFhTruRRCVReMQMp5kYw=="
    },
    "content": {
      "encoding": "base64",
      "value": "QlVGUgAA+gQAABYAACsAAAAAAAIAHAAH6AgPBgAAAAALAAABgMGWx1AAAM0ABOIAAAODM0OTkAAAAAAAAAAAAAAKb5oKEpJ6YkJ6mAAAAAAAAAAAAAAAAv0QeYA29WQa87ZhH4CQP//z+P//BD////+ASznXuUb///8MgAS3/////8X///e+AP////AB/+R/yf////////////////////6/1/79H/3///gEt////////4BLP6QAf/+/pAB//4H0YJ/YeAh/f2///7TH/////9+j//f///////////////////v0f//////////////////////wNzc3Nw==",
      "size": 250
    },
    "wigos_station_identifier": "0-76-2-2900801000W83499"
  },
  "links": [
    {
      "rel": "canonical",
      "type": "application/bufr",
      "href": "http://wis2bra.inmet.gov.br/data/2024-08-15/wis/br-inmet/data/core/weather/surface-based-observations/synop/WIGOS_0-76-2-2900801000W83499_20240815T060000.bufr4",
      "length": 250
    }
  ]
}
``` 

في هذه الجلسة العملية ستتعلم كيفية استخدام أداة MQTT Explorer لإعداد اتصال عميل MQTT بـ Global Broker الخاص بـ WIS2 وستكون قادرًا على عرض رسائل الإشعارات في WIS2.

MQTT Explorer هي أداة مفيدة لتصفح ومراجعة هيكل الموضوع لوسيط MQTT معين لمراجعة البيانات التي يتم نشرها.

لاحظ أن MQTT يستخدم بشكل أساسي للتواصل "من آلة إلى آلة"؛ مما يعني أنه عادةً ما يكون هناك عميل يقوم بتحليل الرسائل تلقائيًا عند استلامها. للعمل مع MQTT برمجيًا (على سبيل المثال، في Python)، يمكنك استخدام مكتبات عميل MQTT مثل [paho-mqtt](https://pypi.org/project/paho-mqtt) للاتصال بوسيط MQTT ومعالجة الرسائل الواردة. توجد العديد من برامج عميل وخادم MQTT، اعتمادًا على متطلباتك وبيئتك التقنية.

## استخدام MQTT Explorer للاتصال بـ Global Broker

لعرض الرسائل التي ينشرها Global Broker الخاص بـ WIS2، يمكنك استخدام "MQTT Explorer" الذي يمكن تنزيله من [موقع MQTT Explorer](https://mqtt-explorer.com).

افتح MQTT Explorer وأضف اتصالًا جديدًا بـ Global Broker المستضاف من قبل MeteoFrance باستخدام التفاصيل التالية:

- host: globalbroker.meteo.fr
- port: 8883
- username: everyone
- password: everyone

<img alt="mqtt-explorer-global-broker-connection" src="/../assets/img/mqtt-explorer-global-broker-connection.png" width="800">

انقر على زر 'ADVANCED'، أزل المواضيع المُعدة مسبقًا وأضف المواضيع التالية للاشتراك فيها:

- `origin/a/wis2/#`

<img alt="mqtt-explorer-global-broker-advanced" src="/../assets/img/mqtt-explorer-global-broker-sub-origin.png" width="800">

!!! note
    عند إعداد اشتراكات MQTT، يمكنك استخدام العلامات البديلة التالية:

    - **علامة بديلة لمستوى واحد (+)**: تحل العلامة البديلة لمستوى واحد محل مستوى موضوع واحد
    - **علامة بديلة متعددة المستويات (#)**: تحل العلامة البديلة متعددة المستويات محل مستويات موضوع متعددة

    في هذه الحالة، سيشترك `origin/a/wis2/#` في جميع المواضيع تحت موضوع `origin/a/wis2`.

انقر على 'BACK'، ثم 'SAVE' لحفظ تفاصيل الاتصال والاشتراك. ثم انقر على 'CONNECT':

يجب أن تبدأ الرسائل في الظهور في جلسة MQTT Explorer الخاصة بك على النحو التالي:

<img alt="mqtt-explorer-global-broker-topics" src="/../assets/img/mqtt-explorer-global-broker-msg-origin.png" width="800">

أنت الآن جاهز لبدء استكشاف مواضيع وهيكل الرسائل في WIS2.

## التمرين 1: مراجعة هيكل موضوع WIS2

استخدم MQTT لتصفح هيكل الموضوع تحت مواضيع `origin`.

!!! question
    
    كيف يمكننا التمييز بين مركز WIS الذي نشر البيانات؟

??? success "انقر للكشف عن الإجابة"

    يمكنك النقر على نافذة الجانب الأيسر في MQTT Explorer لتوسيع هيكل الموضوع.
    
    يمكننا التمييز بين مركز WIS الذي نشر البيانات من خلال النظر إلى المستوى الرابع من هيكل الموضوع. على سبيل المثال، يخبرنا الموضوع التالي:

    `origin/a/wis2/br-inmet/data/core/weather/surface-based-observations/synop`

    أن البيانات تم نشرها بواسطة مركز WIS مع معرف المركز `br-inmet`، وهو معرف المركز لـ Instituto Nacional de Meteorologia - INMET، البرازيل.

!!! question

    كيف يمكننا التمييز بين الرسائل التي نشرها مراكز WIS التي تستضيف بوابة GTS-to-WIS2 والرسائل التي نشرها مراكز WIS التي تستضيف عقدة WIS2؟

??? success "انقر للكشف عن الإجابة"

    يمكننا التمييز بين الرسائل القادمة من بوابة GTS-to-WIS2 من خلال النظر إلى معرف المركز في هيكل الموضوع. على سبيل المثال، يخبرنا الموضوع التالي:

    `origin/a/wis2/de-dwd-gts-to-wis2/data/core/I/S/A/I/01/sbbr`

    أن البيانات تم نشرها بواسطة بوابة GTS-to-WIS2 المستضافة من قبل Deutscher Wetterdienst (DWD)، ألمانيا. بوابة GTS-to-WIS2 هي نوع خاص من الناشرين للبيانات ينشر البيانات من نظام الاتصالات العالمي (GTS) إلى WIS2. يتكون هيكل الموضوع من رؤوس TTAAii CCCC لرسائل GTS.

## التمرين 2: مراجعة هيكل رسالة WIS2

قم بقطع الاتصال من MQTT Explorer وقم بتحديث الأقسام 'Advanced' لتغيير الاشتراك إلى التالي:

* `origin/a/wis2/+/data/core/weather/surface-based-observations/synop`
* `cache/a/wis2/+/data/core/weather/surface-based-observations/synop`

<img alt="mqtt-explorer-global-broker-topics-exercise2" src="/../assets/img/mqtt-explorer-global-broker-sub-origin-cache-synop.png" width="800">

!!! note
    يتم استخدام العلامة البديلة `+` للاشتراك في جميع مراكز WIS.

أعد الاتصال بـ Global Broker وانتظر حتى تظهر الرسائل.

يمكنك عرض محتوى رسالة WIS2 في قسم "Value" على الجانب الأيمن. حاول توسيع هيكل الموضوع لرؤية المستويات المختلفة للرسالة حتى تصل إلى المستوى الأخير ومراجعة محتوى الرسالة لإحدى الرسائل.

!!! question

    كيف يمكننا تحديد الطابع الزمني الذي تم فيه نشر البيانات؟ وكيف يمكننا تحديد الطابع الزمني الذي تم فيه جمع البيانات؟

??? success "انقر للكشف عن الإجابة"

    الطابع الزمني الذي تم فيه نشر البيانات موجود في قسم `properties` من الرسالة بمفتاح `pubtime`.

    الطابع الزمني الذي تم فيه جمع البيانات موجود في قسم `properties` من الرسالة بمفتاح `datetime`.

    <img alt="mqtt-explorer-global-broker-msg-properties" src="/../assets/img/mqtt-explorer-global-broker-msg-properties.png" width="800">

!!! question

    كيف يمكننا تنزيل البيانات من الرابط URL الموجود في الرسالة؟

??? success "انقر للكشف عن الإجابة"

    الرابط URL موجود في قسم `links` بـ `rel="canonical"` ومحدد بمفتاح `href`.

    يمكنك نسخ الرابط URL ولصقه في متصفح ويب لتنزيل البيانات.

## التمرين 3: مراجعة الفرق بين مواضيع 'origin' و 'cache'

تأكد من أنك لا تزال متصلاً بـ Global Broker باستخدام اشتراكات الموضوع `origin/a/wis2/+/data/core/weather/surface-based-observations/synop` و `cache/a/wis2/+/data/core/weather/surface-based-observations/synop` كما هو موضح في التمرين 2.

حاول تحديد رسالة لنفس معرف المركز المنشورة على كلا الموضوعين `origin` و `cache`.


!!! question

    ما الفرق بين الرسائل المنشورة على مواضيع `origin` و `cache`؟

??? success "انقر للكشف عن الإجابة"

    الرسائل المنشورة على مواضيع `origin` هي الرسائل الأصلية التي يعيد Global Broker نشرها من WIS2 Nodes في الشبكة. 

    الرسائل المنشورة على مواضيع `cache` هي الرسائل التي تم تنزيل البيانات فيها بواسطة Global Cache. إذا قمت بفحص محتوى الرسالة من الموضوع الذي يبدأ بـ `cache`، سترى أن الرابط 'canonical' قد تم تحديثه إلى رابط URL جديد.
    
    هناك العديد من Global Caches في شبكة WIS2، لذا ستتلقى رسالة واحدة من كل Global Cache قام بتنزيل الرسالة.
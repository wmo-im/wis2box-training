---
title: الاتصال بـ WIS2 عبر MQTT
---

# الاتصال بـ WIS2 عبر MQTT

!!! abstract "نتائج التعلم"

    بنهاية هذه الجلسة العملية، ستكون قادرًا على:

    - الاتصال بـ WIS2 Global Broker باستخدام MQTT Explorer
    - مراجعة بنية المواضيع في WIS2
    - مراجعة بنية رسائل الإشعارات في WIS2

## المقدمة

يستخدم WIS2 بروتوكول MQTT للإعلان عن توفر بيانات الطقس/المناخ/المياه. يقوم WIS2 Global Broker بالاشتراك في جميع WIS2 Nodes في الشبكة ويعيد نشر الرسائل التي يتلقاها. يقوم Global Cache بالاشتراك في Global Broker، بتحميل البيانات الموجودة في الرسالة، ثم يعيد نشر الرسالة على موضوع `cache` مع رابط URL جديد. ينشر Global Discovery Catalogue بيانات التعريف الاكتشافية من Broker ويوفر واجهة برمجة تطبيقات للبحث.

هذا مثال على بنية رسالة إشعار WIS2 لرسالة تم تلقيها على الموضوع `origin/a/wis2/br-inmet/data/core/weather/surface-based-observations/synop`:

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

في هذه الجلسة العملية، ستتعلم كيفية استخدام أداة MQTT Explorer لإعداد اتصال عميل MQTT بـ WIS2 Global Broker وعرض رسائل إشعارات WIS2.

يعد MQTT Explorer أداة مفيدة لتصفح ومراجعة بنية المواضيع لأي MQTT broker لمراجعة البيانات المنشورة.

!!! note "حول MQTT"
    يوفر MQTT Explorer واجهة سهلة الاستخدام للاتصال بـ MQTT broker واستكشاف المواضيع وبنية الرسائل المستخدمة في WIS2.
    
    عمليًا، يُستخدم MQTT للتواصل بين الآلات، حيث يشترك تطبيق أو خدمة في المواضيع ويعالج الرسائل برمجيًا في الوقت الفعلي.
    
    للعمل مع MQTT برمجيًا (على سبيل المثال، باستخدام Python)، يمكنك استخدام مكتبات عملاء MQTT مثل [paho-mqtt](https://pypi.org/project/paho-mqtt) للاتصال بـ MQTT broker ومعالجة الرسائل الواردة. هناك العديد من برامج العملاء والخوادم لـ MQTT، حسب متطلباتك والبيئة التقنية.

## استخدام MQTT Explorer للاتصال بـ Global Broker

لعرض الرسائل المنشورة بواسطة WIS2 Global Broker، يمكنك استخدام "MQTT Explorer" الذي يمكن تنزيله من [موقع MQTT Explorer](https://mqtt-explorer.com).

افتح MQTT Explorer وأضف اتصالًا جديدًا بـ Global Broker المستضاف بواسطة MeteoFrance باستخدام التفاصيل التالية:

- host: globalbroker.meteo.fr
- port: 8883
- username: everyone
- password: everyone

<img alt="mqtt-explorer-global-broker-connection" src="/../assets/img/mqtt-explorer-global-broker-connection.png" width="800">

انقر على زر 'ADVANCED'، وقم بإزالة المواضيع المُعدة مسبقًا وأضف المواضيع التالية للاشتراك فيها:

- `origin/a/wis2/#`

<img alt="mqtt-explorer-global-broker-advanced" src="/../assets/img/mqtt-explorer-global-broker-sub-origin.png" width="800">

!!! note
    عند إعداد اشتراكات MQTT، يمكنك استخدام البدل التالي:

    - **مستوى واحد (+)**: يستبدل البدل ذو المستوى الواحد مستوى واحدًا من المواضيع.
    - **مستويات متعددة (#)**: يستبدل البدل ذو المستويات المتعددة مستويات متعددة من المواضيع.

    في هذه الحالة، `origin/a/wis2/#` ستشترك في جميع المواضيع تحت موضوع `origin/a/wis2`.

انقر على 'BACK'، ثم 'SAVE' لحفظ تفاصيل الاتصال والاشتراك. ثم انقر على 'CONNECT':

يجب أن تبدأ الرسائل في الظهور في جلسة MQTT Explorer كما يلي:

<img alt="mqtt-explorer-global-broker-topics" src="/../assets/img/mqtt-explorer-global-broker-msg-origin.png" width="800">

أنت الآن جاهز لبدء استكشاف مواضيع WIS2 وبنية الرسائل.

## التمرين 1: مراجعة بنية المواضيع في WIS2

استخدم MQTT لتصفح بنية المواضيع تحت مواضيع `origin`.

!!! question
    
    كيف يمكننا التمييز بين مركز WIS الذي نشر البيانات؟

??? success "انقر للكشف عن الإجابة"

    يمكنك النقر على نافذة الجانب الأيسر في MQTT Explorer لتوسيع بنية المواضيع.
    
    يمكننا التمييز بين مركز WIS الذي نشر البيانات من خلال النظر إلى المستوى الرابع من بنية المواضيع. على سبيل المثال، الموضوع التالي:

    `origin/a/wis2/br-inmet/data/core/weather/surface-based-observations/synop`

    يخبرنا أن البيانات نُشرت من مركز WIS بمُعرّف المركز `br-inmet`، وهو مُعرّف المركز الخاص بـ Instituto Nacional de Meteorologia - INMET، البرازيل.

!!! question

    كيف يمكننا التمييز بين الرسائل المنشورة من مراكز WIS التي تستضيف بوابة GTS-to-WIS2 والرسائل المنشورة من مراكز WIS التي تستضيف WIS2 Node؟

??? success "انقر للكشف عن الإجابة"

    يمكننا التمييز بين الرسائل القادمة من بوابة GTS-to-WIS2 من خلال النظر إلى مُعرّف المركز في بنية المواضيع. على سبيل المثال، الموضوع التالي:

    `origin/a/wis2/de-dwd-gts-to-wis2/data/core/I/S/A/I/01/sbbr`

    يخبرنا أن البيانات نُشرت من بوابة GTS-to-WIS2 المستضافة بواسطة Deutscher Wetterdienst (DWD)، ألمانيا. بوابة GTS-to-WIS2 هي نوع خاص من ناشري البيانات الذين ينشرون البيانات من نظام الاتصالات العالمي (GTS) إلى WIS2. تتكون بنية المواضيع من رؤوس TTAAii CCCC لرسائل GTS.

## التمرين 2: مراجعة بنية الرسائل في WIS2

افصل الاتصال بـ MQTT Explorer وقم بتحديث قسم 'Advanced' لتغيير الاشتراك إلى ما يلي:

* `origin/a/wis2/+/data/core/weather/surface-based-observations/synop`
* `cache/a/wis2/+/data/core/weather/surface-based-observations/synop`

<img alt="mqtt-explorer-global-broker-topics-exercise2" src="/../assets/img/mqtt-explorer-global-broker-sub-origin-cache-synop.png" width="800">

!!! note
    يتم استخدام البدل `+` للاشتراك في جميع مراكز WIS.

أعد الاتصال بـ Global Broker وانتظر ظهور الرسائل.

يمكنك عرض محتوى رسالة WIS2 في قسم "Value" على الجانب الأيمن. حاول توسيع بنية المواضيع لرؤية المستويات المختلفة للرسالة حتى تصل إلى المستوى الأخير ومراجعة محتوى إحدى الرسائل.

!!! question

    كيف يمكننا تحديد الطابع الزمني الذي نُشرت فيه البيانات؟ وكيف يمكننا تحديد الطابع الزمني الذي جُمعت فيه البيانات؟

??? success "انقر للكشف عن الإجابة"

    الطابع الزمني الذي نُشرت فيه البيانات موجود في قسم `properties` من الرسالة مع المفتاح `pubtime`.

    الطابع الزمني الذي جُمعت فيه البيانات موجود في قسم `properties` من الرسالة مع المفتاح `datetime`.

    <img alt="mqtt-explorer-global-broker-msg-properties" src="/../assets/img/mqtt-explorer-global-broker-msg-properties.png" width="800">

!!! question

    كيف يمكننا تنزيل البيانات من الرابط الموجود في الرسالة؟

??? success "انقر للكشف عن الإجابة"

    الرابط موجود في قسم `links` مع `rel="canonical"` ومُعرّف بواسطة المفتاح `href`.

    يمكنك نسخ الرابط ولصقه في متصفح ويب لتنزيل البيانات.

## التمرين 3: مراجعة الفرق بين مواضيع 'origin' و 'cache'

تأكد من أنك لا تزال متصلًا بـ Global Broker باستخدام اشتراكات المواضيع `origin/a/wis2/+/data/core/weather/surface-based-observations/synop` و `cache/a/wis2/+/data/core/weather/surface-based-observations/synop` كما هو موضح في التمرين 2.

حاول تحديد رسالة لنفس مُعرّف المركز نُشرت على كل من مواضيع `origin` و `cache`.

!!! question

    ما الفرق بين الرسائل المنشورة على مواضيع `origin` و `cache`؟

??? success "انقر للكشف عن الإجابة"

    الرسائل المنشورة على مواضيع `origin` هي الرسائل الأصلية التي يعيد Global Broker نشرها من WIS2 Nodes في الشبكة.

    الرسائل المنشورة على مواضيع `cache` هي الرسائل التي تم تنزيل البيانات الخاصة بها بواسطة Global Cache. إذا قمت بمراجعة محتوى الرسالة من الموضوع الذي يبدأ بـ `cache`، ستلاحظ أن الرابط 'canonical' قد تم تحديثه إلى رابط URL جديد.
    
    هناك العديد من Global Caches في شبكة WIS2، لذا ستتلقى رسالة واحدة من كل Global Cache قامت بتنزيل الرسالة.

    يقوم Global Cache فقط بتنزيل وإعادة نشر الرسائل التي نُشرت على التسلسل الهرمي للمواضيع `../data/core/...`.

## الخاتمة

!!! success "تهانينا!"
    في هذه الجلسة العملية، تعلمت:

    - كيفية الاشتراك في خدمات WIS2 Global Broker باستخدام MQTT Explorer
    - بنية المواضيع في WIS2
    - بنية رسائل الإشعارات في WIS2
    - الفرق بين البيانات الأساسية والموصى بها
    - بنية المواضيع المستخدمة بواسطة بوابة GTS-to-WIS2
    - الفرق بين رسائل Global Broker المنشورة على مواضيع `origin` و `cache`
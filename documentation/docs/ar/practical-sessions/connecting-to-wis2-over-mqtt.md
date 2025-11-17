---
title: الاتصال بـ WIS2 عبر MQTT
---

# الاتصال بـ WIS2 عبر MQTT

!!! abstract "نتائج التعلم"

    بنهاية هذه الجلسة العملية، ستكون قادرًا على:

    - الاتصال بـ WIS2 Global Broker باستخدام MQTT Explorer
    - مراجعة هيكل المواضيع في WIS2
    - مراجعة هيكل رسائل الإشعارات في WIS2

## المقدمة

يستخدم WIS2 بروتوكول MQTT للإعلان عن توفر بيانات الطقس/المناخ/المياه. يقوم WIS2 Global Broker بالاشتراك في جميع WIS2 Nodes في الشبكة ويعيد نشر الرسائل التي يتلقاها. يقوم Global Cache بالاشتراك في Global Broker، وتنزيل البيانات الموجودة في الرسالة، ثم يعيد نشر الرسالة على موضوع `cache` مع عنوان URL جديد. ينشر Global Discovery Catalogue بيانات الاكتشاف الوصفية من Broker ويوفر واجهة برمجة تطبيقات للبحث.

هذا مثال على هيكل رسالة الإشعار في WIS2 لرسالة تم استلامها على الموضوع `origin/a/wis2/br-inmet/data/core/weather/surface-based-observations/synop`:

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
    "data_id": "br-inmet:synop-obs/WIGOS_0-20000-0-82022_20251114T180000",
    "datetime": "2025-11-14T18:00:00Z",
    "pubtime": "2025-11-14T20:49:31Z",
    "metadata_id": "urn:wmo:md:br-inmet:synop-obs",
    "integrity": {
      "method": "sha512",
      "value": "TBuWycx/G0lIiTo47eFPBViGutxcIyk7eikppAKPc4aHgOmTIS5Wb9+0v3awMOyCgwpFhTruRRCVReMQMp5kYw=="
    },
    "content": {
      "encoding": "base64",
      "value": "QlVGUgAA+gQAABYAACsAAAAAAAIAHAAH6AgPBgAAAAALAAABgMGWx1AAAM0ABOIAAAODM0OTkAAAAAAAAAAAAAAKb5oKEpJ6YkJ6mAAAAAAAAAAAAAAAAv0QeYA29WQa87ZhH4CQP//z+P//BD////+ASznXuUb///8MgAS3/////8X///e+AP////AB/+R/yf////////////////////6/1/79H/3///gEt////////4BLP6QAf/+/pAB//4H0YJ/YeAh/f2///7TH/////9+j//f///////////////////v0f//////////////////////wNzc3Nw==",
      "size": 250
    },
    "wigos_station_identifier": "0-20000-0-82022"
  },
  "links": [
    {
      "rel": "canonical",
      "type": "application/bufr",
      "href": "http://wis2bra.inmet.gov.br/data/2025-11-14/wis/urn:wmo:md:br-inmet:synop-man/WIGOS_0-20000-0-82022_20251114T180000.bufr4"",
      "length": 250
    }
  ]
}
```

في هذه الجلسة العملية، ستتعلم كيفية استخدام أداة MQTT Explorer لإعداد اتصال عميل MQTT بـ WIS2 Global Broker وعرض رسائل الإشعارات في WIS2.

يُعد MQTT Explorer أداة مفيدة لتصفح ومراجعة هيكل المواضيع لأي MQTT broker لمراجعة البيانات التي يتم نشرها.

!!! note "حول MQTT"
    يوفر MQTT Explorer واجهة سهلة الاستخدام للاتصال بـ MQTT broker واستكشاف المواضيع وهيكل الرسائل المستخدمة في WIS2.
    
    في الواقع، يُقصد باستخدام MQTT للتواصل بين الآلات، حيث يشترك تطبيق أو خدمة في المواضيع ويعالج الرسائل برمجيًا في الوقت الفعلي.
    
    للعمل مع MQTT برمجيًا (على سبيل المثال، باستخدام Python)، يمكنك استخدام مكتبات عملاء MQTT مثل [paho-mqtt](https://pypi.org/project/paho-mqtt) للاتصال بـ MQTT broker ومعالجة الرسائل الواردة. هناك العديد من برامج عملاء وخوادم MQTT، حسب احتياجاتك وبيئتك التقنية.

## استخدام MQTT Explorer للاتصال بـ Global Broker

لعرض الرسائل التي ينشرها WIS2 Global Broker، يمكنك استخدام "MQTT Explorer" الذي يمكن تنزيله من [موقع MQTT Explorer](https://mqtt-explorer.com).

افتح MQTT Explorer وأضف اتصالًا جديدًا بـ Global Broker المستضاف من قبل MeteoFrance باستخدام التفاصيل التالية:

- المضيف: globalbroker.meteo.fr
- المنفذ: 8883
- اسم المستخدم: everyone
- كلمة المرور: everyone

<img alt="mqtt-explorer-global-broker-connection" src="/../assets/img/mqtt-explorer-global-broker-connection.png" width="800">

انقر على زر 'ADVANCED'، وقم بإزالة المواضيع المُعدة مسبقًا وأضف المواضيع التالية للاشتراك فيها:

- `origin/a/wis2/#`

<img alt="mqtt-explorer-global-broker-advanced" src="/../assets/img/mqtt-explorer-global-broker-sub-origin.png" width="800">

!!! note
    عند إعداد اشتراكات MQTT، يمكنك استخدام الرموز التالية:

    - **مستوى واحد (+)**: رمز استبدال لمستوى واحد من المواضيع
    - **متعدد المستويات (#)**: رمز استبدال لمستويات متعددة من المواضيع

    في هذه الحالة، سيشترك `origin/a/wis2/#` في جميع المواضيع تحت موضوع `origin/a/wis2`.

انقر على 'BACK'، ثم 'SAVE' لحفظ تفاصيل الاتصال والاشتراك. ثم انقر على 'CONNECT':

يجب أن تبدأ الرسائل بالظهور في جلسة MQTT Explorer كما يلي:

<img alt="mqtt-explorer-global-broker-topics" src="/../assets/img/mqtt-explorer-global-broker-msg-origin.png" width="800">

أنت الآن جاهز لبدء استكشاف مواضيع WIS2 وهيكل الرسائل.

## التمرين 1: مراجعة هيكل المواضيع في WIS2

استخدم MQTT لتصفح هيكل المواضيع تحت مواضيع `origin`.

!!! question
    
    كيف يمكننا التمييز بين مركز WIS الذي نشر البيانات؟

??? success "انقر للكشف عن الإجابة"

    يمكنك النقر على نافذة الجانب الأيسر في MQTT Explorer لتوسيع هيكل المواضيع.
    
    يمكننا التمييز بين مركز WIS الذي نشر البيانات من خلال النظر إلى المستوى الرابع من هيكل المواضيع. على سبيل المثال، الموضوع التالي:

    `origin/a/wis2/br-inmet/data/core/weather/surface-based-observations/synop`

    يخبرنا أن البيانات نُشرت من مركز WIS بمُعرف المركز `br-inmet`، وهو مُعرف المركز الخاص بـ Instituto Nacional de Meteorologia - INMET، البرازيل.

!!! question

    كيف يمكننا التمييز بين الرسائل المنشورة من مراكز WIS التي تستضيف بوابة GTS-to-WIS2 والرسائل المنشورة من مراكز WIS التي تستضيف WIS2 Node؟

??? success "انقر للكشف عن الإجابة"

    يمكننا التمييز بين الرسائل القادمة من بوابة GTS-to-WIS2 من خلال النظر إلى مُعرف المركز في هيكل المواضيع. على سبيل المثال، الموضوع التالي:

    `origin/a/wis2/de-dwd-gts-to-wis2/data/core/I/S/A/I/01/sbbr`

    يخبرنا أن البيانات نُشرت من بوابة GTS-to-WIS2 المستضافة من قبل Deutscher Wetterdienst (DWD)، ألمانيا. بوابة GTS-to-WIS2 هي نوع خاص من ناشري البيانات الذين ينشرون البيانات من نظام الاتصالات العالمي (GTS) إلى WIS2. يتكون هيكل المواضيع من رؤوس TTAAii CCCC لرسائل GTS.

## التمرين 2: مراجعة هيكل الرسائل في WIS2

افصل الاتصال بـ MQTT Explorer وقم بتحديث قسم 'Advanced' لتغيير الاشتراك إلى التالي:

* `origin/a/wis2/+/data/core/weather/surface-based-observations/synop`
* `cache/a/wis2/+/data/core/weather/surface-based-observations/synop`

<img alt="mqtt-explorer-global-broker-topics-exercise2" src="/../assets/img/mqtt-explorer-global-broker-sub-origin-cache-synop.png" width="800">

!!! note
    يتم استخدام الرمز `+` للاشتراك في جميع مراكز WIS.

أعد الاتصال بـ Global Broker وانتظر حتى تظهر الرسائل.

يمكنك عرض محتوى رسالة WIS2 في قسم "Value" على الجانب الأيمن. حاول توسيع هيكل المواضيع لرؤية المستويات المختلفة للرسالة حتى تصل إلى المستوى الأخير ومراجعة محتوى إحدى الرسائل.

!!! question

    كيف يمكننا تحديد الطابع الزمني الذي تم فيه نشر البيانات؟ وكيف يمكننا تحديد الطابع الزمني الذي تم فيه جمع البيانات؟

??? success "انقر للكشف عن الإجابة"

    الطابع الزمني الذي تم فيه نشر البيانات موجود في قسم `properties` من الرسالة مع المفتاح `pubtime`.

    الطابع الزمني الذي تم فيه جمع البيانات موجود في قسم `properties` من الرسالة مع المفتاح `datetime`.

    <img alt="mqtt-explorer-global-broker-msg-properties" src="/../assets/img/mqtt-explorer-global-broker-msg-properties.png" width="800">

!!! question

    كيف يمكننا تنزيل البيانات من عنوان URL الموجود في الرسالة؟

??? success "انقر للكشف عن الإجابة"

    عنوان URL موجود في قسم `links` مع `rel="canonical"` ومُعرّف بواسطة المفتاح `href`.

    يمكنك نسخ عنوان URL ولصقه في متصفح ويب لتنزيل البيانات.

## التمرين 3: مراجعة الفرق بين مواضيع 'origin' و 'cache'

تأكد من أنك لا تزال متصلًا بـ Global Broker باستخدام اشتراكات المواضيع `origin/a/wis2/+/data/core/weather/surface-based-observations/synop` و `cache/a/wis2/+/data/core/weather/surface-based-observations/synop` كما هو موضح في التمرين 2.

حاول تحديد رسالة لنفس مُعرف المركز المنشورة على كل من مواضيع `origin` و `cache`.

!!! question

    ما الفرق بين الرسائل المنشورة على مواضيع `origin` و `cache`؟

??? success "انقر للكشف عن الإجابة"

    الرسائل المنشورة على مواضيع `origin` هي الرسائل الأصلية التي يعيد Global Broker نشرها من WIS2 Nodes في الشبكة.

    الرسائل المنشورة على مواضيع `cache` هي الرسائل التي تم تنزيل البيانات الخاصة بها بواسطة Global Cache. إذا قمت بفحص محتوى الرسالة من الموضوع الذي يبدأ بـ `cache`، ستلاحظ أن الرابط 'canonical' تم تحديثه إلى عنوان URL جديد.
    
    هناك العديد من Global Caches في شبكة WIS2، لذلك ستتلقى رسالة واحدة من كل Global Cache قامت بتنزيل الرسالة.

    يقوم Global Cache فقط بتنزيل وإعادة نشر الرسائل التي تم نشرها على التسلسل الهرمي للمواضيع `../data/core/...`.

## الخاتمة

!!! success "تهانينا!"
    في هذه الجلسة العملية، تعلمت:

    - كيفية الاشتراك في خدمات WIS2 Global Broker باستخدام MQTT Explorer
    - هيكل المواضيع في WIS2
    - هيكل رسائل الإشعارات في WIS2
    - الفرق بين البيانات الأساسية والموصى بها
    - هيكل المواضيع المستخدم بواسطة بوابة GTS-to-WIS2
    - الفرق بين رسائل Global Broker المنشورة على مواضيع `origin` و `cache`
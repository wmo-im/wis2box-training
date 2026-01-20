---
title: الاتصال بـ WIS2 عبر MQTT
---

# الاتصال بـ WIS2 عبر MQTT

!!! abstract "نتائج التعلم"

    بنهاية هذه الجلسة العملية، ستكون قادرًا على:

    - الاتصال بـ WIS2 Global Broker باستخدام MQTT Explorer
    - مراجعة هيكل موضوع WIS2
    - مراجعة هيكل رسالة الإشعار الخاصة بـ WIS2

## المقدمة

يستخدم WIS2 بروتوكول MQTT للإعلان عن توفر بيانات الطقس/المناخ/المياه. يقوم WIS2 Global Broker بالاشتراك في جميع WIS2 Nodes في الشبكة ويعيد نشر الرسائل التي يتلقاها. يشترك Global Cache في Global Broker، يقوم بتنزيل البيانات الموجودة في الرسالة ثم يعيد نشر الرسالة على موضوع `cache` مع عنوان URL جديد. ينشر Global Discovery Catalogue بيانات الاكتشاف الوصفية من Broker ويوفر واجهة برمجة تطبيقات للبحث.

هذا مثال على هيكل رسالة الإشعار الخاصة بـ WIS2 لرسالة تم استلامها على الموضوع `origin/a/wis2/br-inmet/data/core/weather/surface-based-observations/synop`:

```json
{
   "id":"7a34051b-aa92-40f3-bbab-439143657c8c",
   "type":"Feature",
   "conformsTo":[
      "http://wis.wmo.int/spec/wnm/1/conf/core"
   ],
   "geometry":{
      "type":"Polygon",
      "coordinates":[
         [
            [
               -73.98723548042966,
               5.244486395687602
            ],
            [
               -34.729993455533034,
               5.244486395687602
            ],
            [
               -34.729993455533034,
               -33.768377780900764
            ],
            [
               -73.98723548042966,
               -33.768377780900764
            ],
            [
               -73.98723548042966,
               5.244486395687602
            ]
         ]
      ]
   },
   "properties":{
      "data_id":"br-inmet/metadata/urn:wmo:md:br-inmet:rr1ieq",
      "datetime":"2026-01-20T08:30:21Z",
      "pubtime":"2026-01-20T08:30:22Z",
      "integrity":{
         "method":"sha512",
         "value":"RN+GzqgONURtkzOCo5vQJ5t7SzlAvaGONywEnTXHrHew9RQmUhrHbASvmDlCeRTb8vhE+1/h/7/20f2XJFHCcA=="
      },
      "content":{
         "encoding":"base64",
         "value":"eyJpZCI6ICJ1cm46d21vOm1kOmJyLWlubWV0OnJyMWllcSIsICJjb25mb3Jtc1RvIjogWyJodHRwOi8vd2lzLndtby5pbnQvc3BlYy93Y21wLzIvY29uZi9jb3JlIl0sICJ0eXBlIjogIkZlYXR1cmUiLCAidGltZSI6IHsiaW50ZXJ2YWwiOiBbIjIwMjYtMDEtMjAiLCAiLi4iXSwgInJlc29sdXRpb24iOiAiUFQxSCJ9LCAiZ2VvbWV0cnkiOiB7InR5cGUiOiAiUG9seWdvbiIsICJjb29yZGluYXRlcyI6IFtbWy03My45ODcyMzU0ODA0Mjk2NiwgNS4yNDQ0ODYzOTU2ODc2MDJdLCBbLTM0LjcyOTk5MzQ1NTUzMzAzNCwgNS4yNDQ0ODYzOTU2ODc2MDJdLCBbLTM0LjcyOTk5MzQ1NTUzMzAzNCwgLTMzLjc2ODM3Nzc4MDkwMDc2NF0sIFstNzMuOTg3MjM1NDgwNDI5NjYsIC0zMy43NjgzNzc3ODA5MDA3NjRdLCBbLTczLjk4NzIzNTQ4MDQyOTY2LCA1LjI0NDQ4NjM5NTY4NzYwMl1dXX0sICJwcm9wZXJ0aWVzIjogeyJ0eXBlIjogImRhdGFzZXQiLCAiaWRlbnRpZmllciI6ICJ1cm46d21vOm1kOmJyLWlubWV0OnJyMWllcSIsICJ0aXRsZSI6ICJIb3VybHkgc3lub3B0aWMgb2JzZXJ2YXRpb25zIGZyb20gZml4ZWQtbGFuZCBzdGF0aW9ucyAoU1lOT1ApIChici1pbm1ldCkiLCAiZGVzY3JpcHRpb24iOiAidGVzdCIsICJrZXl3b3JkcyI6IFsib2JzZXJ2YXRpb25zIiwgInRlbXBlcmF0dXJlIiwgInZpc2liaWxpdHkiLCAicHJlY2lwaXRhdGlvbiIsICJwcmVzc3VyZSIsICJjbG91ZHMiLCAic25vdyBkZXB0aCIsICJldmFwb3JhdGlvbiIsICJyYWRpYXRpb24iLCAid2luZCIsICJ0b3RhbCBzdW5zaGluZSIsICJodW1pZGl0eSJdLCAidGhlbWVzIjogW3siY29uY2VwdHMiOiBbeyJpZCI6ICJ3ZWF0aGVyIiwgInRpdGxlIjogIldlYXRoZXIifV0sICJzY2hlbWUiOiAiaHR0cDovL2NvZGVzLndtby5pbnQvd2lzL3RvcGljLWhpZXJhcmNoeS9lYXJ0aC1zeXN0ZW0tZGlzY2lwbGluZSJ9XSwgImNvbnRhY3RzIjogW3sib3JnYW5pemF0aW9uIjogIndtbyIsICJlbWFpbHMiOiBbeyJ2YWx1ZSI6ICJ0ZXN0QGNuLmNvbSJ9XSwgImFkZHJlc3NlcyI6IFt7ImNvdW50cnkiOiAiQlJBIn1dLCAibGlua3MiOiBbeyJyZWwiOiAiYWJvdXQiLCAiaHJlZiI6ICJodHRwOi8vdGVzdC5jb20iLCAidHlwZSI6ICJ0ZXh0L2h0bWwifV0sICJyb2xlcyI6IFsiaG9zdCJdfV0sICJjcmVhdGVkIjogIjIwMjYtMDEtMjBUMDg6MzA6MjFaIiwgInVwZGF0ZWQiOiAiMjAyNi0wMS0yMFQwODozMDoyMVoiLCAid21vOmRhdGFQb2xpY3kiOiAiY29yZSIsICJpZCI6ICJ1cm46d21vOm1kOmJyLWlubWV0OnJyMWllcSJ9LCAibGlua3MiOiBbeyJocmVmIjogIm1xdHQ6Ly9ldmVyeW9uZTpldmVyeW9uZUBsb2NhbGhvc3Q6MTg4MyIsICJ0eXBlIjogImFwcGxpY2F0aW9uL2pzb24iLCAibmFtZSI6ICJvcmlnaW4vYS93aXMyL2JyLWlubWV0L2RhdGEvY29yZS93ZWF0aGVyL3N1cmZhY2UtYmFzZWQtb2JzZXJ2YXRpb25zL3N5bm9wIiwgInJlbCI6ICJpdGVtcyIsICJjaGFubmVsIjogIm9yaWdpbi9hL3dpczIvYnItaW5tZXQvZGF0YS9jb3JlL3dlYXRoZXIvc3VyZmFjZS1iYXNlZC1vYnNlcnZhdGlvbnMvc3lub3AiLCAiZmlsdGVycyI6IHsid2lnb3Nfc3RhdGlvbl9pZGVudGlmaWVyIjogeyJ0eXBlIjogInN0cmluZyIsICJ0aXRsZSI6ICJXSUdPUyBTdGF0aW9uIElkZW50aWZpZXIiLCAiZGVzY3JpcHRpb24iOiAiRmlsdGVyIGJ5IFdJR09TIFN0YXRpb24gSWRlbnRpZmllciJ9fSwgInRpdGxlIjogIk5vdGlmaWNhdGlvbnMifSwgeyJocmVmIjogImh0dHA6Ly9sb2NhbGhvc3QvbWV0YWRhdGEvZGF0YS91cm46d21vOm1kOmJyLWlubWV0OnJyMWllcS5qc29uIiwgInR5cGUiOiAiYXBwbGljYXRpb24vZ2VvK2pzb24iLCAibmFtZSI6ICJ1cm46d21vOm1kOmJyLWlubWV0OnJyMWllcSIsICJyZWwiOiAiY2Fub25pY2FsIiwgInRpdGxlIjogInVybjp3bW86bWQ6YnItaW5tZXQ6cnIxaWVxIn1dfQ==",
         "size":1957
      }
   },
   "links":[
      {
         "rel":"canonical",
         "type":"application/geo+json",
         "href":"http://localhost/data/metadata/urn:wmo:md:br-inmet:rr1ieq.json",
         "length":1957
      }
   ],
   "generated_by":"wis2box 1.2.0"
}
```

في هذه الجلسة العملية، ستتعلم كيفية استخدام أداة MQTT Explorer لإعداد اتصال عميل MQTT مع WIS2 Global Broker وعرض رسائل الإشعارات الخاصة بـ WIS2.

MQTT Explorer هي أداة مفيدة لاستعراض ومراجعة بنية المواضيع الخاصة بأي MQTT broker لمراجعة البيانات المنشورة.

!!! note "حول MQTT"
    يوفر MQTT Explorer واجهة سهلة الاستخدام للاتصال بـ MQTT broker واستكشاف المواضيع وبنية الرسائل المستخدمة بواسطة WIS2.
    
    عمليًا، يتم استخدام MQTT للتواصل بين الآلات، حيث تشترك التطبيقات أو الخدمات في المواضيع وتعالج الرسائل برمجيًا في الوقت الفعلي.
    
    للعمل مع MQTT برمجيًا (على سبيل المثال، باستخدام Python)، يمكنك استخدام مكتبات عملاء MQTT مثل [paho-mqtt](https://pypi.org/project/paho-mqtt) للاتصال بـ MQTT broker ومعالجة الرسائل الواردة. هناك العديد من برامج عملاء وخوادم MQTT، حسب احتياجاتك وبيئتك التقنية.

## استخدام MQTT Explorer للاتصال بـ Global Broker

لعرض الرسائل المنشورة بواسطة WIS2 Global Broker، يمكنك استخدام "MQTT Explorer" الذي يمكن تنزيله من [موقع MQTT Explorer](https://mqtt-explorer.com).

افتح MQTT Explorer وأضف اتصالًا جديدًا مع Global Broker المستضاف بواسطة MeteoFrance باستخدام التفاصيل التالية:

- host: globalbroker.meteo.fr
- port: 8883
- username: everyone
- password: everyone

<img alt="mqtt-explorer-global-broker-connection" src="/../assets/img/mqtt-explorer-global-broker-connection.png" width="800">

انقر على زر 'ADVANCED'، وقم بإزالة المواضيع المُعدة مسبقًا وأضف المواضيع التالية للاشتراك فيها:

- `origin/a/wis2/#`

<img alt="mqtt-explorer-global-broker-advanced" src="/../assets/img/mqtt-explorer-global-broker-sub-origin.png" width="800">

!!! note
    عند إعداد اشتراكات MQTT، يمكنك استخدام الرموز التالية:

    - **مستوى واحد (+)**: الرمز العام لمستوى واحد يستبدل مستوى واحدًا من الموضوع.
    - **مستويات متعددة (#)**: الرمز العام لمستويات متعددة يستبدل مستويات متعددة من الموضوع.

    في هذه الحالة، `origin/a/wis2/#` سيشترك في جميع المواضيع تحت الموضوع `origin/a/wis2`.

انقر على 'BACK'، ثم 'SAVE' لحفظ تفاصيل الاتصال والاشتراك. ثم انقر على 'CONNECT':

يجب أن تبدأ الرسائل في الظهور في جلسة MQTT Explorer كما يلي:

<img alt="mqtt-explorer-global-broker-topics" src="/../assets/img/mqtt-explorer-global-broker-msg-origin.png" width="800">

أنت الآن جاهز لبدء استكشاف مواضيع WIS2 وبنية الرسائل.

## التمرين 1: مراجعة بنية مواضيع WIS2

استخدم MQTT لاستعراض بنية المواضيع تحت المواضيع `origin`.

!!! question
    
    كيف يمكننا التمييز بين مركز WIS الذي نشر البيانات؟

??? success "انقر لعرض الإجابة"

    يمكنك النقر على نافذة الجانب الأيسر في MQTT Explorer لتوسيع بنية المواضيع.
    
    يمكننا التمييز بين مركز WIS الذي نشر البيانات من خلال النظر إلى المستوى الرابع من بنية المواضيع. على سبيل المثال، الموضوع التالي:

    `origin/a/wis2/br-inmet/data/core/weather/surface-based-observations/synop`

    يخبرنا أن البيانات تم نشرها من مركز WIS بمُعرّف المركز `br-inmet`، وهو مُعرّف المركز الخاص بـ Instituto Nacional de Meteorologia - INMET، البرازيل.

!!! question

    كيف يمكننا التمييز بين الرسائل المنشورة من مراكز WIS التي تستضيف بوابة GTS-to-WIS2 والرسائل المنشورة من مراكز WIS التي تستضيف WIS2 Node؟

??? success "انقر لعرض الإجابة"

    يمكننا التمييز بين الرسائل القادمة من بوابة GTS-to-WIS2 من خلال النظر إلى مُعرّف المركز في بنية المواضيع. على سبيل المثال، الموضوع التالي:

    `origin/a/wis2/de-dwd-gts-to-wis2/data/core/I/S/A/I/01/sbbr`

    يخبرنا أن البيانات تم نشرها بواسطة بوابة GTS-to-WIS2 المستضافة بواسطة Deutscher Wetterdienst (DWD)، ألمانيا. بوابة GTS-to-WIS2 هي نوع خاص من ناشري البيانات الذين ينشرون البيانات من نظام الاتصالات العالمي (GTS) إلى WIS2. تتكون بنية المواضيع من رؤوس TTAAii CCCC لرسائل GTS.

## التمرين 2: مراجعة بنية رسائل WIS2

افصل الاتصال بـ MQTT Explorer وقم بتحديث قسم 'Advanced' لتغيير الاشتراك إلى ما يلي:

* `origin/a/wis2/+/data/core/weather/surface-based-observations/synop`
* `cache/a/wis2/+/data/core/weather/surface-based-observations/synop`

<img alt="mqtt-explorer-global-broker-topics-exercise2" src="/../assets/img/mqtt-explorer-global-broker-sub-origin-cache-synop.png" width="800">

!!! note
    يتم استخدام الرمز العام `+` للاشتراك في جميع مراكز WIS.

أعد الاتصال بـ Global Broker وانتظر حتى تظهر الرسائل.

يمكنك عرض محتوى رسالة WIS2 في قسم "Value" على الجانب الأيمن. حاول توسيع بنية المواضيع لرؤية المستويات المختلفة للرسالة حتى تصل إلى المستوى الأخير وراجع محتوى إحدى الرسائل.

!!! question

    كيف يمكننا تحديد الطابع الزمني الذي تم نشر البيانات فيه؟ وكيف يمكننا تحديد الطابع الزمني الذي تم جمع البيانات فيه؟

??? success "انقر لعرض الإجابة"

    الطابع الزمني الذي تم نشر البيانات فيه موجود في قسم `properties` من الرسالة مع مفتاح `pubtime`.

    الطابع الزمني الذي تم جمع البيانات فيه موجود في قسم `properties` من الرسالة مع مفتاح `datetime`.

    <img alt="mqtt-explorer-global-broker-msg-properties" src="/../assets/img/mqtt-explorer-global-broker-msg-properties.png" width="800">

!!! question

    كيف يمكننا تنزيل البيانات من الرابط المقدم في الرسالة؟

??? success "انقر لعرض الإجابة"

    الرابط موجود في قسم `links` مع `rel="canonical"` ويتم تعريفه بواسطة المفتاح `href`.

    يمكنك نسخ الرابط ولصقه في متصفح ويب لتنزيل البيانات.

## التمرين 3: مراجعة الفرق بين مواضيع 'origin' و 'cache'

تأكد من أنك لا تزال متصلًا بـ Global Broker باستخدام اشتراكات المواضيع `origin/a/wis2/+/data/core/weather/surface-based-observations/synop` و `cache/a/wis2/+/data/core/weather/surface-based-observations/synop` كما هو موضح في التمرين 2.

حاول تحديد رسالة لنفس مُعرّف المركز المنشورة على كل من مواضيع `origin` و `cache`.

!!! question

    ما الفرق بين الرسائل المنشورة على مواضيع `origin` و `cache`؟

??? success "انقر لعرض الإجابة"

    الرسائل المنشورة على مواضيع `origin` هي الرسائل الأصلية التي يعيد Global Broker نشرها من WIS2 Nodes في الشبكة.

    الرسائل المنشورة على مواضيع `cache` هي الرسائل التي تم تنزيل البيانات الخاصة بها بواسطة Global Cache. إذا قمت بفحص محتوى الرسالة من الموضوع الذي يبدأ بـ `cache`، ستلاحظ أن الرابط 'canonical' قد تم تحديثه إلى رابط جديد.
    
    هناك العديد من Global Caches في شبكة WIS2، لذلك ستتلقى رسالة واحدة من كل Global Cache قامت بتنزيل الرسالة.

    سيقوم Global Cache فقط بتنزيل وإعادة نشر الرسائل التي تم نشرها على التسلسل الهرمي للموضوع `../data/core/...`.

## الخاتمة

!!! success "تهانينا!"
    في هذه الجلسة العملية، تعلمت:

    - كيفية الاشتراك في خدمات WIS2 Global Broker باستخدام MQTT Explorer
    - بنية مواضيع WIS2
    - بنية رسائل الإشعارات الخاصة بـ WIS2
    - الفرق بين البيانات الأساسية والموصى بها
    - بنية المواضيع المستخدمة بواسطة بوابة GTS-to-WIS2
    - الفرق بين الرسائل المنشورة على مواضيع `origin` و `cache` في Global Broker
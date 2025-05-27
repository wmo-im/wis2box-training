---
title: قوالب تحويل CSV إلى BUFR
---

# قوالب تحويل CSV إلى BUFR

!!! abstract "نتائج التعلم"
    بنهاية هذه الجلسة العملية، ستكون قادرًا على:

    - إنشاء قالب تحويل BUFR جديد لبيانات CSV الخاصة بك
    - تعديل وتصحيح قالب تحويل BUFR الخاص بك من خلال سطر الأوامر
    - تكوين إضافة تحويل البيانات من CSV إلى BUFR لاستخدام قالب تحويل BUFR مخصص
    - استخدام قوالب AWS و DAYCLI المدمجة لتحويل بيانات CSV إلى BUFR

## مقدمة

تُستخدم ملفات بيانات القيم المفصولة بفواصل (CSV) غالبًا لتسجيل البيانات المراقبة وغيرها في تنسيق جدولي.
معظم أجهزة تسجيل البيانات المستخدمة لتسجيل مخرجات الحساسات قادرة على تصدير الملاحظات في ملفات محددة، بما في ذلك بتنسيق CSV.
بالمثل، عندما يتم استيعاب البيانات في قاعدة بيانات، من السهل تصدير البيانات المطلوبة في ملفات مُنسقة بتنسيق CSV.

يوفر وحدة wis2box csv2bufr أداة سطر أوامر لتحويل بيانات CSV إلى تنسيق BUFR. عند استخدام csv2bufr، تحتاج إلى توفير قالب تحويل BUFR يُعين أعمدة CSV إلى عناصر BUFR المقابلة. إذا كنت لا ترغب في إنشاء قالب تحويل خاص بك، يمكنك استخدام قوالب AWS و DAYCLI المدمجة لتحويل بيانات CSV إلى BUFR، ولكن ستحتاج إلى التأكد من أن بيانات CSV التي تستخدمها بالتنسيق الصحيح لهذه القوالب. إذا كنت ترغب في فك تشفير المعلمات التي لا تتضمنها قوالب AWS و DAYCLI، ستحتاج إلى إنشاء قالب تحويل خاص بك.

في هذه الجلسة ستتعلم كيفية إنشاء قالب تحويل خاص بك لتحويل بيانات CSV إلى BUFR. ستتعلم أيضًا كيفية استخدام قوالب AWS و DAYCLI المدمجة لتحويل بيانات CSV إلى BUFR.

## التحضير

تأكد من أنه تم بدء تشغيل wis2box-stack باستخدام `python3 wis2box.py start`

تأكد من أن لديك متصفح ويب مفتوح مع واجهة MinIO لنسختك بالانتقال إلى `http://YOUR-HOST:9000`
إذا لم تتذكر بيانات اعتماد MinIO الخاصة بك، يمكنك العثور عليها في ملف `wis2box.env` في دليل `wis2box` على VM الطالب الخاص بك.

تأكد من أن لديك MQTT Explorer مفتوحًا ومتصلًا بوسيطك باستخدام بيانات الاعتماد `everyone/everyone`.

## إنشاء قالب تحويل

تأتي وحدة csv2bufr مع أداة سطر أوامر لإنشاء قالب تحويل خاص بك باستخدام مجموعة من تسلسلات BUFR و/أو عنصر BUFR كمدخلات.

للعثور على تسلسلات BUFR وعناصر محددة، يمكنك الرجوع إلى جداول BUFR على [https://confluence.ecmwf.int/display/ECC/BUFR+tables](https://confluence.ecmwf.int/display/ECC/BUFR+tables).

### أداة سطر أوامر تعيينات csv2bufr

للوصول إلى أداة سطر أوامر csv2bufr، تحتاج إلى تسجيل الدخول إلى حاوية wis2box-api:

```bash
cd ~/wis2box
python3 wis2box-ctl.py login wis2box-api
```

لطباعة صفحة المساعدة للأمر `csv2bufr mapping`:

```bash
csv2bufr mappings --help
```

تعرض صفحة المساعدة أمرين فرعيين:

- `csv2bufr mappings create` : إنشاء قالب تحويل جديد
- `csv2bufr mappings list` : سرد قوالب التحويل المتاحة في النظام

!!! Note "قائمة تعيينات csv2bufr"

    سيعرض لك الأمر `csv2bufr mapping list` قوالب التحويل المتاحة في النظام.
    تُخزن القوالب الافتراضية في الدليل `/opt/wis2box/csv2bufr/templates` في الحاوية.

    لمشاركة قوالب التحويل المخصصة مع النظام، يمكنك تخزينها في الدليل المحدد بواسطة `$CSV2BUFR_TEMPLATES`، والذي يُضبط افتراضيًا على `/data/wis2box/mappings` في الحاوية. نظرًا لأن الدليل `/data/wis2box/mappings` في الحاوية مُثبت على الدليل `$WIS2BOX_HOST_DATADIR/mappings` على المضيف، ستجد قوالب التحويل المخصصة الخاصة بك في الدليل `$WIS2BOX_HOST_DATADIR/mappings` على المضيف.

لنحاول إنشاء قالب تحويل مخصص جديد باستخدام الأمر `csv2bufr mapping create` باستخدام تسلسل BUFR 301150 بالإضافة إلى عنصر BUFR 012101.

```bash
csv2bufr mappings create 301150 012101 --output /data/wis2box/mappings/my_custom_template.json
```

يمكنك التحقق من محتوى قالب التحويل الذي أنشأته للتو باستخدام الأمر `cat`:

```bash
cat /data/wis2box/mappings/my_custom_template.json
```

!!! question "فحص قالب التحويل"

    كم عدد أعمدة CSV التي يتم تعيينها إلى عناصر BUFR؟ ما هو رأس CSV لكل عنصر BUFR يتم تعيينه؟

??? success "انقر لكشف الإجابة"
    
    يعين قالب التحويل الذي أنشأته **5** أعمدة CSV إلى عناصر BUFR، وهي العناصر الأربعة في تسلسل 301150 بالإضافة إلى عنصر BUFR 012101.

    تُعين الأعمدة CSV التالية إلى عناصر BUFR:

    - **wigosIdentifierSeries** يُعين إلى `"eccodes_key": "#1#wigosIdentifierSeries"` (عنصر BUFR 001125)
    - **wigosIssuerOfIdentifier** يُعين إلى `"eccodes_key": "#1#wigosIssuerOfIdentifier` (عنصر BUFR 001126)
    - **wigosIssueNumber** يُعين إلى `"eccodes_key": "#1#wigosIssueNumber"` (عنصر BUFR 001127)
    - **wigosLocalIdentifierCharacter** يُعين إلى `"eccodes_key": "#1#wigosLocalIdentifierCharacter"` (عنصر BUFR 001128)
    - **airTemperature** يُعين إلى `"eccodes_key": "#1#airTemperature"` (عنصر BUFR 012101)

يفتقد قالب التحويل الذي أنشأته معلومات metadata المهمة حول الملاحظة التي تمت، تاريخ ووقت الملاحظة، وخطوط العرض والطول للمحطة.

الخطوة التالية سنقوم بتحديث قالب التحويل وإضافة التسلسلات التالية:
    
- **301011** للتاريخ (السنة، الشهر، اليوم)
- **301012** للوقت (الساعة، الدقيقة)
- **301023** للموقع (خطوط العرض/الطول (دقة خشنة))

والعناصر التالية:

- **010004** للضغط
- **007031** لارتفاع البارومتر فوق مستوى سطح البحر

نفذ الأمر التالي لتحديث قالب التحويل:

```bash
csv2bufr mappings create 301150 301011 301012 301023 007031 012101 010004  --output /data/wis2box/mappings/my_custom_template.json
```

وافحص محتوى قالب التحويل مرة أخرى:

```bash
cat /data/wis2box/mappings/my_custom_template.json
```

!!! question "فحص قالب التحويل المحدث"

    كم عدد أعمدة CSV التي يتم تعيينها الآن إلى عناصر BUFR؟ ما هو رأس CSV لكل عنصر BUFR يتم تعيينه؟

??? success "انقر لكشف الإجابة"
    
    يعين قالب التحويل الذي أنشأته الآن **18** عمود CSV إلى عناصر BUFR:
    - 4 عناصر BUFR من تسلسل BUFR 301150
    - 3 عناصر BUFR من تسلسل BUFR 301011
    - 2 عناصر BUFR من تسلسل BUFR 301012
    - 2 عناصر BUFR من تسلسل BUFR 301023
    - عنصر BUFR 007031
    - عنصر BUFR 012101

    تُعين الأعمدة CSV التالية إلى عناصر BUFR:

    - **wigosIdentifierSeries** يُعين إلى `"eccodes_key": "#1#wigosIdentifierSeries"` (عنصر BUFR 001125)
    - **wigosIssuerOfIdentifier** يُعين إلى `"eccodes_key": "#1#wigosIssuerOfIdentifier` (عنصر BUFR 001126)
    - **wigosIssueNumber** يُعين إلى `"eccodes_key": "#1#wigosIssueNumber"` (عنصر BUFR 001127)
    - **wigosLocalIdentifierCharacter** يُعين إلى `"eccodes_key": "#1#wigosLocalIdentifierCharacter"` (عنصر BUFR 001128)
    - **year** يُعين إلى `"eccodes_key": "#1#year"` (عنصر BUFR 004001)
    - **month** يُعين إلى `"eccodes_key": "#1#month"` (عنصر BUFR 004002)
    - **day** يُعين إلى `"eccodes_key": "#1#day"` (عنصر BUFR 004003)
    - **hour** يُعين إلى `"eccodes_key": "#1#hour"` (عنصر BUFR 004004)
    - **minute** يُعين إلى `"eccodes_key": "#1#minute"` (عنصر BUFR 004005)
    - **latitude** يُعين إلى `"eccodes_key": "#1#latitude"` (عنصر BUFR 005002)
    - **longitude** يُعين إلى `"eccodes_key": "#1#longitude"` (عنصر BUFR 006002)
    - **heightOfBarometerAboveMeanSeaLevel"** يُعين إلى `"eccodes_key": "#1#heightOfBarometerAboveMeanSeaLevel"` (عنصر BUFR 007031)
    - **airTemperature** يُعين إلى `"eccodes_key": "#1#airTemperature"` (عنصر BUFR 012101)
    - **nonCoordinatePressure** يُعين إلى `"eccodes_key": "#1#nonCoordinatePressure"` (عنصر BUFR 010004)

تحقق من محتوى الملف `custom_template_data.csv` في الدليل `/root/data-conversion-exercises`:

```bash
cat /root/data-conversion-exercises/custom_template_data.csv
```

لاحظ أن رؤوس هذا الملف CSV هي نفس رؤوس CSV في قالب التحويل الذي أنشأته.

لتجربة تحويل البيانات، يمكننا استخدام أداة السطر الأمر `csv2bufr` لتحويل ملف CSV إلى BUFR باستخدام قالب التعيين الذي أنشأناه:

```bash
csv2bufr data transform --bufr-template my_custom_template /root/data-conversion-exercises/custom_template_data.csv
```

يجب أن ترى الناتج التالي:

```bash
CLI:    ... Transforming /root/data-conversion-exercises/custom_template_data.csv to BUFR ...
CLI:    ... Processing subsets:
CLI:    ..... 94 bytes written to ./WIGOS_0-20000-0-15015_20250412T210000.bufr4
CLI:    End of processing, exiting.
```

!!! question "تحقق من محتوى ملف BUFR"
    
    كيف يمكنك التحقق من محتوى ملف BUFR الذي أنشأته للتأكد من أنه قد تم ترميز البيانات بشكل صحيح؟

??? success "انقر للكشف عن الإجابة"

    يمكنك استخدام الأمر `bufr_dump -p` للتحقق من محتوى ملف BUFR الذي أنشأته.
    سيعرض الأمر محتوى ملف BUFR بتنسيق يمكن قراءته بواسطة الإنسان.

    ```bash
    bufr_dump -p ./WIGOS_0-20000-0-15015_20250412T210000.bufr4
    ```

    في الناتج سترى قيم لعناصر BUFR التي قمت بتعيينها في القالب، على سبيل المثال سيظهر "airTemperature":
    
    ```bash
    airTemperature=298.15
    ```

يمكنك الآن الخروج من الحاوية:

```bash
exit
```

### استخدام قالب التعيين في wis2box

للتأكد من أن القالب الجديد للتعيين يتم التعرف عليه بواسطة حاوية wis2box-api، تحتاج إلى إعادة تشغيل الحاوية:

```bash
docker restart wis2box-api
```

يمكنك الآن تكوين مجموعة البيانات الخاصة بك في wis2box-webapp لاستخدام قالب التعيين المخصص لمكون إضافي لتحويل CSV إلى BUFR.

سيكتشف wis2box-webapp تلقائيًا قالب التعيين الذي أنشأته ويجعله متاحًا في قائمة القوالب لمكون إضافي لتحويل CSV إلى BUFR.

انقر على مجموعة البيانات التي أنشأتها في الجلسة العملية السابقة وانقر على "تحديث" بجانب المكون الإضافي باسم "تحويل بيانات CSV إلى BUFR":

<img alt="Image showing the dataset editor in the wis2box-webapp" src="/../assets/img/wis2box-webapp-data-mapping-update-csv2bufr.png"/>

يجب أن ترى القالب الجديد الذي أنشأته في قائمة القوالب المتاحة:

<img alt="Image showing the csv2bufr-templates in the wis2box-webapp" src="/../assets/img/wis2box-webapp-csv2bufr-templates.png"/>

!!! hint

    لاحظ أنه إذا لم ترى القالب الجديد الذي أنشأته، حاول تحديث الصفحة أو فتحها في نافذة متخفية جديدة.

للحفاظ على اختيار القالب الافتراضي لـ AWS (انقر في الزاوية العلوية اليمنى لإغلاق تكوين المكون الإضافي).

## استخدام قالب 'AWS'

يوفر قالب 'AWS' قالب تعيين لتحويل بيانات CSV إلى تسلسل BUFR 301150، 307096، دعمًا لمتطلبات GBON الدنيا.

يمكن العثور على وصف قالب AWS هنا [aws-template](./../csv2bufr-templates/aws-template.md).

### مراجعة بيانات الإدخال aws-example

قم بتنزيل المثال لهذا التمرين من الرابط أدناه:

[aws-example.csv](./../../sample-data/aws-example.csv)

افتح الملف الذي قمت بتنزيله في محرر وتفقد المحتوى:

!!! question
    عند فحص حقول التاريخ والوقت والتعريف (معرفات WIGOS والتقليدية) ما الذي تلاحظه؟ كيف سيتم تمثيل تاريخ اليوم؟

??? success "انقر للكشف عن الإجابة"
    كل عمود يحتوي على قطعة معلومات واحدة. على سبيل المثال، يتم تقسيم التاريخ إلى سنة وشهر ويوم، مما يعكس كيفية تخزين البيانات في BUFR. سيتم تقسيم تاريخ اليوم عبر الأعمدة "السنة" و"الشهر" و"اليوم". بالمثل، يحتاج الوقت إلى التقسيم إلى "الساعة" و"الدقيقة" ويجب تقسيم معرف محطة WIGOS إلى مكوناته المعنية.

!!! question
    عند النظر إلى ملف البيانات كيف يتم ترميز البيانات المفقودة؟

??? success "انقر للكشف عن الإجابة"
    البيانات المفقودة داخل الملف ممثلة بخلايا فارغة. في ملف CSV، سيتم ترميز ذلك بـ ``,,``. لاحظ أن هذه خلية فارغة وليست مشفرة كسلسلة ذات طول صفر، مثل ``,"",``.

!!! hint "البيانات المفقودة"
    من المعترف به أن البيانات قد تكون مفقودة لأسباب متنوعة، سواء بسبب فشل الجهاز الاستشعاري أو عدم ملاحظة العامل. في هذه الحالات، يمكن ترميز البيانات المفقودة وفقًا للإجابة أعلاه، تظل البيانات الأخرى في التقرير صالحة.

### تحديث ملف المثال

قم بتحديث ملف المثال الذي قمت بتنزيله لاستخدام تاريخ ووقت اليوم وغير معرفات محطة WIGOS لاستخدام المحطات التي قمت بتسجيلها في wis2box-webapp.

### تحميل البيانات إلى MinIO والتحقق من النتيجة

انتقل إلى واجهة مستخدم MinIO وقم بتسجيل الدخول باستخدام بيانات الاعتماد من ملف `wis2box.env`.

انتقل إلى **wis2box-incoming** وانقر على الزر "إنشاء مسار جديد":

<img alt="Image showing MinIO UI with the create folder button highlighted" src="/../assets/img/minio-create-new-path.png"/>

أنشئ مجلدًا جديدًا في دلو MinIO يطابق معرف مجموعة البيانات للمجموعة التي أنشأتها بالقالب='weather/surface-weather-observations/synop':

<img alt="Image showing MinIO UI with the create folder button highlighted" src="/../assets/img/minio-create-new-path-metadata_id.png"/>

قم بتحميل ملف المثال الذي قمت بتنزيله إلى المجلد الذي أنشأته في دلو MinIO:

<img alt="Image showing MinIO UI with aws-example uploaded" src="/../assets/img/minio-upload-aws-example.png"/></center>

تحقق من لوحة تحكم Grafana على `http://YOUR-HOST:3000` لمعرفة ما إذا كانت هناك أي تحذيرات أو أخطاء. إذا رأيت أيًا منها، حاول إصلاحها وكرر التمرين.

تحقق من MQTT Explorer لمعرفة ما إذا كنت تتلقى إشعارات بيانات WIS2.

إذا نجحت في إدخال البيانات، يجب أن ترى 3 إشعارات في MQTT explorer على الموضوع `origin/a/wis2/<centre-id>/data/weather/surface-weather-observations/synop` للمحطات الثلاث التي أبلغت عن البيانات لها:

<img width="450" alt="Image showing MQTT explorer after uploading AWS" src="/../assets/img/mqtt-explorer-aws-upload.png"/>

## استخدام قالب 'DayCLI'

يوفر قالب **DayCLI** قالب تعيين لتحويل بيانات CSV اليومية للمناخ إلى تسلسل BUFR 307075، دعمًا للإبلاغ عن بيانات المناخ اليومية.

يمكن العثور على وصف قالب DAYCLI هنا [daycli-template](./../csv2bufr-templates/daycli-template.md).

لمشاركة هذه البيانات على WIS2، ستحتاج إلى إنشاء مجموعة بيانات جديدة في wis2box-webapp تحتوي على التسلسل الهرمي لموضوع WIS2 الصحيح والذي يستخدم قالب DAYCLI لتحويل بيانات CSV إلى BUFR.

### إنشاء مجموعة بيانات wis2box لنشر رسائل DAYCLI

انتقل إلى محرر المجموعات في wis2box-webapp وأنشئ مجموعة بيانات جديدة. استخدم نفس معرف المركز كما في الجلسات العملية السابقة وحدد **نوع البيانات='climate/surface-based-observations/daily'**:

<img alt="Create a new dataset in the wis2box-webapp for DAYCLI" src="/../assets/img/wis2box-webapp-create-dataset-daycli.png"/>

انقر على "الاستمرار إلى النموذج" وأضف وصفًا لمجموعة البيانات الخاصة بك، وحدد المربع المحيط وقدم معلومات الاتصال لمجموعة البيانات. بمجرد الانتهاء من ملء جميع الأقسام، انقر على 'تحقق من النموذج' وتحقق من النموذج.

راجع مكونات البيانات الإضافية للمجموعات. انقر على "تحديث" بجانب المكون الإضافي باسم "تحويل بيانات CSV إلى BUFR" وسترى أن القالب مضبوط على **DayCLI**:

<img alt="Update the data plugin for the dataset to use the DAYCLI template" src="/../assets/img/wis2box-webapp-update-data-plugin-daycli.png"/>

أغلق تكوين المكون الإضافي وأرسل النموذج باستخدام الرمز المميز للمصادقة الذي أنشأته في الجلسة العملية السابقة.

يجب أن يكون لديك الآن مجموعة بيانات ثانية في wis2box-webapp مكونة لاستخدام قالب DAYCLI لتحويل بيانات CSV إلى BUFR.

### مراجعة بيانات الإدخال daycli-example

قم بتنزيل المثال لهذا التمرين من الرابط أدناه:

[daycli-example.csv](./../../sample-data/daycli-example.csv)

افتح الملف الذي قمت بتنزيله في محرر وتفقد المحتوى:

!!! question
    ما هي المتغيرات الإضافية المدرجة في قالب daycli؟

??? success "انقر للكشف عن الإجابة"
    يتضمن قالب daycli بيانات تعريفية مهمة حول موقع الأداة وتصنيفات جودة القياس لدرجة الحرارة والرطوبة، علامات التحكم بالجودة ومعلومات حول كيفية حساب متوسط درجة الحرارة اليومية.

### تحديث ملف المثال

يحتوي ملف المثال على صف بيانات لكل يوم في شهر، ويقدم بيانات لمحطة واحدة. قم بتحديث ملف المثال الذي قمت بتنزيله لاستخدام تاريخ ووقت اليوم وغير معرفات محطة WIGOS لاستخدام محطة قمت بتسجيلها في `wis2box-webapp`.

### رفع البيانات إلى MinIO وفحص النتيجة

كما في السابق، ستحتاج إلى رفع البيانات إلى دلو `wis2box-incoming` في MinIO ليتم معالجتها بواسطة محول csv2bufr. هذه المرة ستحتاج إلى إنشاء مجلد جديد في دلو MinIO يطابق dataset-id للمجموعة التي أنشأتها بالقالب='climate/surface-based-observations/daily' والذي سيكون مختلفًا عن dataset-id الذي استخدمته في التمرين السابق:

<img alt="صورة تُظهر واجهة MinIO مع تحميل DAYCLI-example" src="/../assets/img/minio-upload-daycli-example.png"/></center>

بعد رفع البيانات تحقق من عدم وجود تحذيرات أو أخطاء في لوحة Grafana وتحقق من MQTT Explorer لمعرفة ما إذا كنت تتلقى إشعارات بيانات WIS2.

إذا نجحت في إدخال البيانات يجب أن ترى 30 إشعارًا في MQTT Explorer على الموضوع `origin/a/wis2/<centre-id>/data/climate/surface-based-observations/daily` للـ 30 يومًا التي أبلغت عن بيانات لها:

<img width="450" alt="صورة تُظهر MQTT Explorer بعد رفع DAYCLI" src="/../assets/img/mqtt-daycli-template-success.png"/>

## الخاتمة

!!! success "تهانينا"
    في هذه الجلسة العملية تعلمت:

    - كيفية إنشاء قالب تعيين مخصص لتحويل بيانات CSV إلى BUFR
    - كيفية استخدام قوالب AWS و DAYCLI المدمجة لتحويل بيانات CSV إلى BUFR
---
title: قوالب تحويل CSV إلى BUFR
---

# قوالب تحويل CSV إلى BUFR

!!! abstract "نتائج التعلم"
    بنهاية هذه الجلسة العملية، ستكون قادرًا على:

    - إنشاء قالب جديد لتحويل BUFR لبيانات CSV الخاصة بك
    - تعديل وتصحيح قالب تحويل BUFR المخصص الخاص بك من خلال سطر الأوامر
    - تكوين الإضافة الخاصة بتحويل CSV إلى BUFR لاستخدام قالب تحويل BUFR مخصص
    - استخدام القوالب المدمجة AWS وDAYCLI لتحويل بيانات CSV إلى BUFR

## المقدمة

تُستخدم ملفات البيانات ذات القيم المفصولة بفواصل (CSV) غالبًا لتسجيل البيانات الرصدية وغيرها في شكل جدولي. 
تستطيع معظم أجهزة تسجيل البيانات المستخدمة لتسجيل مخرجات المستشعرات تصدير الملاحظات في ملفات مفصولة، بما في ذلك CSV.
وبالمثل، عند إدخال البيانات إلى قاعدة بيانات، يكون من السهل تصدير البيانات المطلوبة في ملفات بتنسيق CSV.

يوفر وحدة `wis2box csv2bufr` أداة سطر أوامر لتحويل بيانات CSV إلى تنسيق BUFR. عند استخدام `csv2bufr`، تحتاج إلى توفير قالب تحويل BUFR يربط أعمدة CSV بالعناصر المقابلة في BUFR. إذا لم ترغب في إنشاء قالب تحويل خاص بك، يمكنك استخدام القوالب المدمجة AWS وDAYCLI لتحويل بيانات CSV إلى BUFR، ولكن ستحتاج إلى التأكد من أن بيانات CSV التي تستخدمها في التنسيق الصحيح لهذه القوالب. إذا كنت ترغب في فك تشفير المعلمات غير المدرجة في القوالب AWS وDAYCLI، فستحتاج إلى إنشاء قالب تحويل خاص بك.

في هذه الجلسة، ستتعلم كيفية إنشاء قالب تحويل خاص بك لتحويل بيانات CSV إلى BUFR. ستتعلم أيضًا كيفية استخدام القوالب المدمجة AWS وDAYCLI لتحويل بيانات CSV إلى BUFR.

## التحضير

تأكد من تشغيل `wis2box-stack` باستخدام الأمر التالي:  
`python3 wis2box.py start`

تأكد من فتح متصفح ويب مع واجهة MinIO لبيئتك من خلال الانتقال إلى:  
`http://YOUR-HOST:9000`  
إذا لم تتذكر بيانات اعتماد MinIO الخاصة بك، يمكنك العثور عليها في ملف `wis2box.env` الموجود في دليل `wis2box` على جهاز الطالب الافتراضي الخاص بك.

تأكد من فتح MQTT Explorer والاتصال بالوسيط الخاص بك باستخدام بيانات الاعتماد:  
`everyone/everyone`.

## إنشاء قالب تحويل

تأتي وحدة `csv2bufr` مع أداة سطر أوامر لإنشاء قالب تحويل خاص بك باستخدام مجموعة من تسلسلات BUFR و/أو عناصر BUFR كمدخلات.

للعثور على تسلسلات وعناصر BUFR محددة، يمكنك الرجوع إلى جداول BUFR على الرابط التالي:  
[https://confluence.ecmwf.int/display/ECC/BUFR+tables](https://confluence.ecmwf.int/display/ECC/BUFR+tables).

### أداة سطر الأوامر لإنشاء قوالب csv2bufr

للوصول إلى أداة سطر الأوامر `csv2bufr`، تحتاج إلى تسجيل الدخول إلى حاوية `wis2box-api`:

```bash
cd ~/wis2box
python3 wis2box-ctl.py login wis2box-api
```

لطباعة صفحة المساعدة للأمر `csv2bufr mapping`:

```bash
csv2bufr mappings --help
```

تعرض صفحة المساعدة أمرين فرعيين:

- `csv2bufr mappings create` : لإنشاء قالب تحويل جديد
- `csv2bufr mappings list` : لعرض قوالب التحويل المتوفرة في النظام

!!! Note "csv2bufr mapping list"

    يعرض الأمر `csv2bufr mapping list` قوالب التحويل المتوفرة في النظام. 
    يتم تخزين القوالب الافتراضية في الدليل `/opt/wis2box/csv2bufr/templates` داخل الحاوية.

    لمشاركة قوالب التحويل المخصصة مع النظام، يمكنك تخزينها في الدليل المحدد بواسطة `$CSV2BUFR_TEMPLATES`، والذي يتم تعيينه افتراضيًا إلى `/data/wis2box/mappings` داخل الحاوية. نظرًا لأن الدليل `/data/wis2box/mappings` داخل الحاوية يتم تركيبه مع الدليل `$WIS2BOX_HOST_DATADIR/mappings` على المضيف، ستجد قوالب التحويل المخصصة الخاصة بك في الدليل `$WIS2BOX_HOST_DATADIR/mappings` على المضيف.

لنحاول إنشاء قالب تحويل مخصص جديد باستخدام الأمر `csv2bufr mapping create` مع تسلسل BUFR 301150 بالإضافة إلى عنصر BUFR 012101 كمدخل:

```bash
csv2bufr mappings create 301150 012101 --output /data/wis2box/mappings/my_custom_template.json
```

يمكنك التحقق من محتوى قالب التحويل الذي أنشأته للتو باستخدام الأمر `cat`:

```bash
cat /data/wis2box/mappings/my_custom_template.json
```

!!! question "فحص قالب التحويل"

    كم عدد أعمدة CSV التي يتم ربطها بعناصر BUFR؟ وما هو عنوان CSV لكل عنصر BUFR يتم ربطه؟

??? success "اضغط للكشف عن الإجابة"
    
    يقوم قالب التحويل الذي أنشأته بربط **5** أعمدة CSV بعناصر BUFR، وهي العناصر الأربعة في تسلسل 301150 بالإضافة إلى عنصر BUFR 012101.

    يتم ربط أعمدة CSV التالية بعناصر BUFR:

    - **wigosIdentifierSeries** يرتبط بـ `"eccodes_key": "#1#wigosIdentifierSeries"` (عنصر BUFR 001125)
    - **wigosIssuerOfIdentifier** يرتبط بـ `"eccodes_key": "#1#wigosIssuerOfIdentifier"` (عنصر BUFR 001126)
    - **wigosIssueNumber** يرتبط بـ `"eccodes_key": "#1#wigosIssueNumber"` (عنصر BUFR 001127)
    - **wigosLocalIdentifierCharacter** يرتبط بـ `"eccodes_key": "#1#wigosLocalIdentifierCharacter"` (عنصر BUFR 001128)
    - **airTemperature** يرتبط بـ `"eccodes_key": "#1#airTemperature"` (عنصر BUFR 012101)

يفتقد قالب التحويل الذي أنشأته إلى بيانات وصفية مهمة حول الملاحظة التي تم إجراؤها، مثل تاريخ ووقت الملاحظة وخط العرض وخط الطول للمحطة.

بعد ذلك، سنقوم بتحديث قالب التحويل وإضافة التسلسلات التالية:

- **301011** للتاريخ (السنة، الشهر، اليوم)
- **301012** للوقت (الساعة، الدقيقة)
- **301023** للموقع (خط العرض/خط الطول بدقة منخفضة)

والعناصر التالية:

- **010004** للضغط
- **007031** لارتفاع البارومتر فوق مستوى سطح البحر

نفذ الأمر التالي لتحديث قالب التحويل:

```bash
csv2bufr mappings create 301150 301011 301012 301023 007031 012101 010004  --output /data/wis2box/mappings/my_custom_template.json
```

وتحقق من محتوى قالب التحويل مرة أخرى:

```bash
cat /data/wis2box/mappings/my_custom_template.json
```

!!! question "فحص قالب التحويل المحدث"

    كم عدد أعمدة CSV التي يتم ربطها الآن بعناصر BUFR؟ وما هو عنوان CSV لكل عنصر BUFR يتم ربطه؟

??? success "اضغط للكشف عن الإجابة"
    
    يقوم قالب التحويل الذي أنشأته الآن بربط **18** عمودًا من CSV بعناصر BUFR:
    - 4 عناصر BUFR من تسلسل BUFR 301150
    - 3 عناصر BUFR من تسلسل BUFR 301011
    - 2 عنصر BUFR من تسلسل BUFR 301012
    - 2 عنصر BUFR من تسلسل BUFR 301023
    - عنصر BUFR 007031
    - عنصر BUFR 012101

    يتم ربط أعمدة CSV التالية بعناصر BUFR:

    - **wigosIdentifierSeries** يرتبط بـ `"eccodes_key": "#1#wigosIdentifierSeries"` (عنصر BUFR 001125)
    - **wigosIssuerOfIdentifier** يرتبط بـ `"eccodes_key": "#1#wigosIssuerOfIdentifier"` (عنصر BUFR 001126)
    - **wigosIssueNumber** يرتبط بـ `"eccodes_key": "#1#wigosIssueNumber"` (عنصر BUFR 001127)
    - **wigosLocalIdentifierCharacter** يرتبط بـ `"eccodes_key": "#1#wigosLocalIdentifierCharacter"` (عنصر BUFR 001128)
    - **year** يرتبط بـ `"eccodes_key": "#1#year"` (عنصر BUFR 004001)
    - **month** يرتبط بـ `"eccodes_key": "#1#month"` (عنصر BUFR 004002)
    - **day** يرتبط بـ `"eccodes_key": "#1#day"` (عنصر BUFR 004003)
    - **hour** يرتبط بـ `"eccodes_key": "#1#hour"` (عنصر BUFR 004004)
    - **minute** يرتبط بـ `"eccodes_key": "#1#minute"` (عنصر BUFR 004005)
    - **latitude** يرتبط بـ `"eccodes_key": "#1#latitude"` (عنصر BUFR 005002)
    - **longitude** يرتبط بـ `"eccodes_key": "#1#longitude"` (عنصر BUFR 006002)
    - **heightOfBarometerAboveMeanSeaLevel** يرتبط بـ `"eccodes_key": "#1#heightOfBarometerAboveMeanSeaLevel"` (عنصر BUFR 007031)
    - **airTemperature** يرتبط بـ `"eccodes_key": "#1#airTemperature"` (عنصر BUFR 012101)
    - **nonCoordinatePressure** يرتبط بـ `"eccodes_key": "#1#nonCoordinatePressure"` (عنصر BUFR 010004)

تحقق من محتوى الملف `custom_template_data.csv` في الدليل `/tmp/data-conversion-exercises`:

```bash
cat /tmp/data-conversion-exercises/custom_template_data.csv
```

لاحظ أن رؤوس هذا الملف بصيغة CSV هي نفسها رؤوس CSV في قالب التعيين الذي قمت بإنشائه.

لاختبار تحويل البيانات، يمكننا استخدام أداة سطر الأوامر `csv2bufr` لتحويل ملف CSV إلى BUFR باستخدام قالب التعيين الذي قمنا بإنشائه:

```bash
csv2bufr data transform --bufr-template my_custom_template /tmp/data-conversion-exercises/custom_template_data.csv
```

يجب أن ترى المخرجات التالية:

```bash
CLI:    ... Transforming /tmp/data-conversion-exercises/custom_template_data.csv to BUFR ...
CLI:    ... Processing subsets:
CLI:    ..... 94 bytes written to ./WIGOS_0-20000-0-15015_20250412T210000.bufr4
CLI:    End of processing, exiting.
```

!!! question "تحقق من محتوى ملف BUFR"
    
    كيف يمكنك التحقق من محتوى ملف BUFR الذي قمت بإنشائه للتو والتأكد من أنه قام بترميز البيانات بشكل صحيح؟

??? success "انقر لعرض الإجابة"

    يمكنك استخدام الأمر `bufr_dump -p` للتحقق من محتوى ملف BUFR الذي قمت بإنشائه. 
    سيعرض الأمر محتوى ملف BUFR بصيغة قابلة للقراءة البشرية.

    ```bash
    bufr_dump -p ./WIGOS_0-20000-0-15015_20250412T210000.bufr4
    ```

    في المخرجات، سترى القيم للعناصر الموجودة في BUFR التي قمت بتعيينها في القالب، على سبيل المثال "airTemperature" ستظهر كما يلي:
    
    ```bash
    airTemperature=298.15
    ```

يمكنك الآن الخروج من الحاوية:

```bash
exit
```

### استخدام قالب التعيين في wis2box

لضمان التعرف على قالب التعيين الجديد من قبل حاوية wis2box-api، تحتاج إلى إعادة تشغيل الحاوية:

```bash
docker restart wis2box-api
```

يمكنك الآن تكوين مجموعة البيانات الخاصة بك في wis2box-webapp لاستخدام قالب التعيين المخصص لمكون تحويل CSV إلى BUFR.

سيقوم wis2box-webapp بالكشف تلقائيًا عن قالب التعيين الذي قمت بإنشائه وجعله متاحًا في قائمة القوالب لمكون تحويل CSV إلى BUFR.

انقر على مجموعة البيانات التي أنشأتها في الجلسة العملية السابقة وانقر على "UPDATE" بجانب المكون المسمى "CSV data converted to BUFR":

<img alt="صورة تعرض محرر مجموعة البيانات في wis2box-webapp" src="/../assets/img/wis2box-webapp-data-mapping-update-csv2bufr.png"/>

يجب أن ترى القالب الجديد الذي قمت بإنشائه في قائمة القوالب المتاحة:

<img alt="صورة تعرض قوالب csv2bufr في wis2box-webapp" src="/../assets/img/wis2box-webapp-csv2bufr-templates.png"/>

!!! hint

    لاحظ أنه إذا لم ترَ القالب الجديد الذي قمت بإنشائه، حاول تحديث الصفحة أو فتحها في نافذة تصفح خاصة.

في الوقت الحالي، احتفظ بالاختيار الافتراضي لقالب AWS (انقر في الزاوية العلوية اليمنى لإغلاق إعدادات المكون).

## استخدام قالب 'AWS'

يوفر قالب 'AWS' قالب تعيين لتحويل بيانات CSV إلى تسلسل BUFR 301150، 307096، لدعم متطلبات GBON الدنيا.

يمكن العثور على وصف قالب AWS هنا [aws-template](./../csv2bufr-templates/aws-template.md).

### مراجعة بيانات الإدخال aws-example

قم بتنزيل المثال لهذا التمرين من الرابط أدناه:

[aws-example.csv](./../sample-data/aws-example.csv)

افتح الملف الذي قمت بتنزيله في محرر وتفحص المحتوى:

!!! question
    عند فحص الحقول الخاصة بالتاريخ، الوقت، والمعرفات (WIGOS والمعرفات التقليدية)، ماذا تلاحظ؟ كيف سيتم تمثيل تاريخ اليوم؟

??? success "انقر لعرض الإجابة"
    يحتوي كل عمود على قطعة واحدة من المعلومات. على سبيل المثال، يتم تقسيم التاريخ إلى السنة، الشهر، واليوم، مما يعكس كيفية تخزين البيانات في BUFR. سيتم تقسيم تاريخ اليوم عبر الأعمدة "year"، "month"، و"day". وبالمثل، يجب تقسيم الوقت إلى "hour" و"minute"، كما يجب تقسيم معرف محطة WIGOS إلى مكوناته الخاصة.

!!! question
    عند النظر إلى ملف البيانات، كيف يتم ترميز البيانات المفقودة؟
    
??? success "انقر لعرض الإجابة"
    يتم تمثيل البيانات المفقودة داخل الملف بخلايا فارغة. في ملف CSV، يتم ترميز ذلك بـ ``,,``. لاحظ أن هذه خلية فارغة وليست سلسلة نصية بطول صفر، مثل ``,"",``.

!!! hint "البيانات المفقودة"
    من المعروف أن البيانات قد تكون مفقودة لأسباب متنوعة، سواء بسبب عطل في المستشعر أو لأن المعلمة لم يتم ملاحظتها. في هذه الحالات، يمكن ترميز البيانات المفقودة كما هو موضح أعلاه، بينما تظل البيانات الأخرى في التقرير صالحة.

### تحديث ملف المثال

قم بتحديث ملف المثال الذي قمت بتنزيله لاستخدام تاريخ ووقت اليوم وقم بتغيير معرفات محطة WIGOS لاستخدام المحطات التي قمت بتسجيلها في wis2box-webapp.

### تحميل البيانات إلى MinIO والتحقق من النتيجة

انتقل إلى واجهة MinIO وقم بتسجيل الدخول باستخدام بيانات الاعتماد من ملف `wis2box.env`.

انتقل إلى **wis2box-incoming** وانقر على الزر "Create new path":

<img alt="صورة تعرض واجهة MinIO مع تمييز زر إنشاء مجلد جديد" src="/../assets/img/minio-create-new-path.png"/>

قم بإنشاء مجلد جديد في حاوية MinIO يطابق معرف مجموعة البيانات التي قمت بإنشائها مع القالب='weather/surface-weather-observations/synop':

<img alt="صورة تعرض واجهة MinIO مع تمييز زر إنشاء مجلد جديد" src="/../assets/img/minio-create-new-path-metadata_id.png"/>

قم بتحميل ملف المثال الذي قمت بتنزيله إلى المجلد الذي أنشأته في حاوية MinIO:

<img alt="صورة تعرض واجهة MinIO مع تحميل aws-example" src="/../assets/img/minio-upload-aws-example.png"/></center>

تحقق من لوحة معلومات Grafana على `http://YOUR-HOST:3000` لمعرفة ما إذا كانت هناك أي تحذيرات أو أخطاء. إذا رأيت أيًا منها، حاول إصلاحها وكرر التمرين.

تحقق من MQTT Explorer لمعرفة ما إذا كنت تتلقى إشعارات بيانات WIS2.

إذا قمت بإدخال البيانات بنجاح، يجب أن ترى 3 إشعارات في MQTT Explorer على الموضوع `origin/a/wis2/<centre-id>/data/weather/surface-weather-observations/synop` للمحطات الثلاث التي أبلغت عنها:

<img width="450" alt="صورة تعرض MQTT Explorer بعد تحميل AWS" src="/../assets/img/mqtt-explorer-aws-upload.png"/>

## استخدام قالب 'DayCLI'

يوفر قالب **DayCLI** قالب تعيين لتحويل بيانات المناخ اليومية بصيغة CSV إلى تسلسل BUFR 307075، لدعم الإبلاغ عن بيانات المناخ اليومية.

يمكن العثور على وصف قالب DAYCLI هنا [daycli-template](./../csv2bufr-templates/daycli-template.md).

لمشاركة هذه البيانات على WIS2، ستحتاج إلى إنشاء مجموعة بيانات جديدة في wis2box-webapp تحتوي على التسلسل الهرمي الصحيح لموضوع WIS2 وتستخدم قالب DAYCLI لتحويل بيانات CSV إلى BUFR.

### إنشاء مجموعة بيانات wis2box لنشر رسائل DAYCLI

انتقل إلى محرر مجموعة البيانات في wis2box-webapp وقم بإنشاء مجموعة بيانات جديدة. استخدم نفس معرف المركز كما في الجلسات العملية السابقة واختر **Data Type='climate/surface-based-observations/daily'**:

<img alt="إنشاء مجموعة بيانات جديدة في wis2box-webapp لـ DAYCLI" src="/../assets/img/wis2box-webapp-create-dataset-daycli.png"/>

انقر على "CONTINUE TO FORM" وأضف وصفًا لمجموعة البيانات الخاصة بك، حدد المربع المحيط وقدم معلومات الاتصال لمجموعة البيانات. بمجرد الانتهاء من ملء جميع الأقسام، انقر على 'VALIDATE FORM' وتحقق من النموذج.

راجع مكونات البيانات لمجموعة البيانات. انقر على "UPDATE" بجانب المكون المسمى "CSV data converted to BUFR" وسترى أن القالب مضبوط على **DayCLI**:

<img alt="تحديث مكون البيانات لمجموعة البيانات لاستخدام قالب DAYCLI" src="/../assets/img/wis2box-webapp-update-data-plugin-daycli.png"/>

أغلق إعدادات المكون وقم بإرسال النموذج باستخدام رمز المصادقة الذي قمت بإنشائه في الجلسة العملية السابقة.

يجب أن يكون لديك الآن مجموعة بيانات ثانية في wis2box-webapp تم تكوينها لاستخدام قالب DAYCLI لتحويل بيانات CSV إلى BUFR.

### مراجعة بيانات الإدخال daycli-example

قم بتنزيل المثال لهذا التمرين من الرابط أدناه:

[daycli-example.csv](./../sample-data/daycli-example.csv)

افتح الملف الذي قمت بتنزيله في محرر وتفحص المحتوى:

!!! question
    ما هي المتغيرات الإضافية التي تم تضمينها في قالب daycli؟

??? success "انقر لعرض الإجابة"
    يتضمن قالب daycli بيانات وصفية مهمة حول موقع الأدوات وتصنيفات جودة القياس لدرجة الحرارة والرطوبة، أعلام مراقبة الجودة، ومعلومات حول كيفية حساب متوسط درجة الحرارة اليومية.

### تحديث ملف المثال

يحتوي ملف المثال على صف واحد من البيانات لكل يوم في الشهر، ويبلغ عن البيانات لمحطة واحدة. قم بتحديث ملف المثال الذي قمت بتنزيله لاستخدام تاريخ ووقت اليوم وقم بتغيير معرفات محطة WIGOS لاستخدام محطة قمت بتسجيلها في wis2box-webapp.

### تحميل البيانات إلى MinIO والتحقق من النتيجة

كما في السابق، ستحتاج إلى تحميل البيانات إلى الحاوية 'wis2box-incoming' في MinIO ليتم معالجتها بواسطة محول csv2bufr. هذه المرة ستحتاج إلى إنشاء مجلد جديد في حاوية MinIO يتطابق مع معرف مجموعة البيانات (dataset-id) الخاصة بمجموعة البيانات التي أنشأتها باستخدام القالب template='climate/surface-based-observations/daily'، والذي سيكون مختلفًا عن معرف مجموعة البيانات الذي استخدمته في التمرين السابق:

<img alt="Image showing MinIO UI with DAYCLI-example uploaded" src="/../assets/img/minio-upload-daycli-example.png"/></center>

بعد تحميل البيانات، تحقق من عدم وجود تحذيرات (WARNINGS) أو أخطاء (ERRORS) في لوحة تحكم Grafana، وتحقق من MQTT Explorer لمعرفة ما إذا كنت تتلقى إشعارات بيانات WIS2.

إذا قمت بإدخال البيانات بنجاح، يجب أن ترى 30 إشعارًا في MQTT Explorer على الموضوع `origin/a/wis2/<centre-id>/data/climate/surface-based-observations/daily` للأيام الثلاثين في الشهر الذي أبلغت فيه عن البيانات:

<img width="450" alt="Image showing MQTT explorer after uploading DAYCLI" src="/../assets/img/mqtt-daycli-template-success.png"/>

## الخاتمة

!!! success "تهانينا"
    في هذه الجلسة العملية، تعلمت:

    - كيفية إنشاء قالب تخصيص لتحويل بيانات CSV إلى BUFR
    - كيفية استخدام القوالب المدمجة لـ AWS وDAYCLI لتحويل بيانات CSV إلى BUFR
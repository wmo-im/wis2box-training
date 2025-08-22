---
title: أدوات تحويل البيانات
---

# أدوات تحويل البيانات

!!! abstract "نتائج التعلم"
    بنهاية هذه الجلسة العملية، ستكون قادرًا على:

    - الوصول إلى أدوات ecCodes عبر سطر الأوامر داخل حاوية `wis2box-api`
    - استخدام أداة `synop2bufr` لتحويل تقارير FM-12 SYNOP إلى BUFR من خلال سطر الأوامر
    - تشغيل تحويل `synop2bufr` عبر تطبيق `wis2box-webapp`
    - استخدام أداة `csv2bufr` لتحويل بيانات CSV إلى BUFR من خلال سطر الأوامر

## المقدمة

يجب أن تلتزم البيانات المنشورة على WIS2 بالمتطلبات والمعايير التي تحددها مجتمعات الخبراء في مجالات نظم الأرض المختلفة. لتسهيل عملية نشر البيانات للملاحظات السطحية الأرضية، يوفر `wis2box` أدوات لتحويل البيانات إلى تنسيق BUFR. هذه الأدوات متاحة عبر حاوية `wis2box-api` ويمكن استخدامها من خلال سطر الأوامر لاختبار عملية تحويل البيانات.

التحويلات الرئيسية التي يدعمها `wis2box` حاليًا هي تحويل تقارير FM-12 SYNOP إلى BUFR وتحويل بيانات CSV إلى BUFR. يتم دعم بيانات FM-12 لأنها لا تزال تُستخدم على نطاق واسع ويتم تبادلها في مجتمع WMO، بينما يتم دعم بيانات CSV للسماح بتعيين البيانات التي تنتجها محطات الطقس الآلية إلى تنسيق BUFR.

### حول FM-12 SYNOP

تم تاريخيًا الإبلاغ عن تقارير الطقس السطحي من المحطات الأرضية كل ساعة أو في الساعات الرئيسية (00، 06، 12، و18 بالتوقيت العالمي) والساعات الوسيطة (03، 09، 15، 21 بالتوقيت العالمي). قبل الانتقال إلى BUFR، كانت هذه التقارير تُشفر في شكل نصي عادي باستخدام كود FM-12 SYNOP. على الرغم من أن الانتقال إلى BUFR كان من المقرر أن يكتمل بحلول عام 2012، إلا أن عددًا كبيرًا من التقارير لا يزال يتم تبادلها بتنسيق FM-12 SYNOP القديم. يمكن العثور على مزيد من المعلومات حول تنسيق FM-12 SYNOP في دليل WMO حول الأكواد، المجلد I.1 (WMO-No. 306, Volume I.1).

### حول ecCodes

مكتبة ecCodes هي مجموعة من المكتبات البرمجية والأدوات المصممة لفك تشفير وترميز البيانات الأرصادية بتنسيقات GRIB وBUFR. يتم تطويرها من قبل المركز الأوروبي للتنبؤات الجوية متوسطة المدى (ECMWF). راجع [وثائق ecCodes](https://confluence.ecmwf.int/display/ECC/ecCodes+documentation) لمزيد من المعلومات.

يتضمن برنامج `wis2box` مكتبة ecCodes في الصورة الأساسية لحاوية `wis2box-api`. يتيح ذلك للمستخدمين الوصول إلى أدوات سطر الأوامر والمكتبات من داخل الحاوية. تُستخدم مكتبة ecCodes داخل حزمة `wis2box-stack` لفك تشفير وترميز رسائل BUFR.

### حول csv2bufr وsynop2bufr

بالإضافة إلى ecCodes، يستخدم `wis2box` الوحدات البرمجية التالية المكتوبة بلغة Python والتي تعمل مع ecCodes لتحويل البيانات إلى تنسيق BUFR:

- **synop2bufr**: لدعم تنسيق FM-12 SYNOP القديم الذي كان يُستخدم تقليديًا من قبل المراقبين اليدويين. تعتمد وحدة synop2bufr على بيانات وصفية إضافية للمحطات لترميز معلمات إضافية في ملف BUFR. راجع [مستودع synop2bufr على GitHub](https://github.com/World-Meteorological-Organization/synop2bufr)
- **csv2bufr**: لتمكين تحويل بيانات CSV التي تنتجها محطات الطقس الآلية إلى تنسيق BUFR. تُستخدم وحدة csv2bufr لتحويل بيانات CSV إلى تنسيق BUFR باستخدام قالب تعيين يحدد كيفية تعيين بيانات CSV إلى تنسيق BUFR. راجع [مستودع csv2bufr على GitHub](https://github.com/World-Meteorological-Organization/csv2bufr)

يمكن استخدام هذه الوحدات بشكل مستقل أو كجزء من حزمة `wis2box`.

## التحضير

!!! warning "المتطلبات المسبقة"

    - تأكد من أن `wis2box` الخاص بك قد تم تكوينه وتشغيله
    - تأكد من أنك قد قمت بإعداد مجموعة بيانات وقمت بتكوين محطة واحدة على الأقل في `wis2box`
    - قم بالاتصال بـ MQTT broker الخاص بمثيل `wis2box` الخاص بك باستخدام MQTT Explorer
    - افتح تطبيق `wis2box` على الويب (`http://YOUR-HOST/wis2box-webapp`) وتأكد من تسجيل الدخول
    - افتح لوحة التحكم Grafana لمثيلك عن طريق الذهاب إلى `http://YOUR-HOST:3000`

لاستخدام أدوات BUFR عبر سطر الأوامر، ستحتاج إلى تسجيل الدخول إلى حاوية `wis2box-api`. ما لم يُذكر خلاف ذلك، يجب تشغيل جميع الأوامر على هذه الحاوية. ستحتاج أيضًا إلى فتح MQTT Explorer والاتصال بـ broker الخاص بك.

أولاً، قم بالاتصال بجهاز الطالب الافتراضي الخاص بك عبر عميل SSH الخاص بك وانسخ مواد التمرين إلى حاوية `wis2box-api`:

```bash
docker cp ~/exercise-materials/data-conversion-exercises wis2box-api:/root
```

ثم قم بتسجيل الدخول إلى حاوية `wis2box-api` وانتقل إلى الدليل حيث توجد مواد التمرين:

```bash
cd ~/wis2box
python3 wis2box-ctl.py login wis2box-api
cd /root/data-conversion-exercises
```

تأكد من أن الأدوات متوفرة، بدءًا من ecCodes:

```bash
bufr_dump -V
```

يجب أن تحصل على الاستجابة التالية:

```
ecCodes Version 2.36.0
```

بعد ذلك، تحقق من إصدار synop2bufr:

```bash
synop2bufr --version
```

يجب أن تحصل على الاستجابة التالية:

```
synop2bufr, version 0.7.0
```

بعد ذلك، تحقق من csv2bufr:

```bash
csv2bufr --version
```

يجب أن تحصل على الاستجابة التالية:

```
csv2bufr, version 0.8.6
```

## أدوات ecCodes عبر سطر الأوامر

تتضمن مكتبة ecCodes الموجودة في حاوية `wis2box-api` عددًا من أدوات سطر الأوامر للعمل مع ملفات BUFR. 
توضح التمارين التالية كيفية استخدام `bufr_ls` و`bufr_dump` لفحص محتوى ملف BUFR.

### bufr_ls

في هذا التمرين الأول، ستستخدم أمر `bufr_ls` لفحص رؤوس ملف BUFR وتحديد نوع محتويات الملف.

استخدم الأمر التالي لتشغيل `bufr_ls` على الملف `bufr-cli-ex1.bufr4`:

```bash
bufr_ls bufr-cli-ex1.bufr4
```

يجب أن ترى الإخراج التالي:

```bash
bufr-cli-ex1.bufr4
centre                     masterTablesVersionNumber  localTablesVersionNumber   typicalDate                typicalTime                numberOfSubsets
cnmc                       29                         0                          20231002                   000000                     1
1 of 1 messages in bufr-cli-ex1.bufr4

1 of 1 total messages in 1 file
```

يمكن تمرير خيارات مختلفة إلى `bufr_ls` لتغيير كل من التنسيق وحقول الرؤوس المطبوعة.

!!! question
     
    ما هو الأمر الذي يمكن استخدامه لعرض الإخراج السابق بتنسيق JSON؟

    يمكنك تشغيل الأمر `bufr_ls` مع العلمة `-h` لرؤية الخيارات المتاحة.

??? success "اضغط للكشف عن الإجابة"
    يمكنك تغيير تنسيق الإخراج إلى JSON باستخدام العلمة `-j`، أي:
    ```bash
    bufr_ls -j bufr-cli-ex1.bufr4
    ```

    عند التشغيل، يجب أن تحصل على الإخراج التالي:
    ```
    { "messages" : [
      {
        "centre": "cnmc",
        "masterTablesVersionNumber": 29,
        "localTablesVersionNumber": 0,
        "typicalDate": 20231002,
        "typicalTime": "000000",
        "numberOfSubsets": 1
      }
    ]}
    ```

الإخراج المطبوع يمثل قيم بعض مفاتيح الرؤوس في ملف BUFR.

بمفرده، لا يكون هذا الإخراج مفيدًا جدًا، حيث يوفر معلومات محدودة فقط عن محتويات الملف.

عند فحص ملف BUFR، نرغب غالبًا في تحديد نوع البيانات الموجودة في الملف والتاريخ/الوقت النموذجي للبيانات في الملف. يمكن سرد هذه المعلومات باستخدام العلمة `-p` لتحديد الرؤوس التي سيتم طباعتها. يمكن تضمين رؤوس متعددة باستخدام قائمة مفصولة بفواصل.

يمكنك استخدام الأمر التالي لسرد فئة البيانات، الفئة الفرعية، التاريخ النموذجي، والوقت:

```bash
bufr_ls -p dataCategory,internationalDataSubCategory,typicalDate,typicalTime -j bufr-cli-ex1.bufr4
```

!!! question

    قم بتنفيذ الأمر السابق وقم بتفسير الإخراج باستخدام [جدول الأكواد المشترك C-13](https://github.com/wmo-im/CCT/blob/master/C13.csv) لتحديد فئة البيانات والفئة الفرعية.

    ما هو نوع البيانات (فئة البيانات والفئة الفرعية) الموجودة في الملف؟ ما هو التاريخ والوقت النموذجي للبيانات؟

??? success "اضغط للكشف عن الإجابة"
    
    ```
    { "messages" : [
      {
        "dataCategory": 2,
        "internationalDataSubCategory": 4,
        "typicalDate": 20231002,
        "typicalTime": "000000"
      }
    ]}
    ```

    من هذا، نرى أن:

- فئة البيانات هي 2، مما يشير إلى بيانات **"الرصدات الرأسية (غير الساتلية)"**.
- الفئة الفرعية الدولية هي 4، مما يشير إلى بيانات **"تقارير درجة الحرارة/الرطوبة/الرياح على المستويات العليا من محطات أرضية ثابتة (TEMP)"**.
- التاريخ والوقت النموذجيان هما 2023-10-02 و00:00:00z على التوالي.

### bufr_dump

يمكن استخدام الأمر `bufr_dump` لعرض وفحص محتويات ملف BUFR، بما في ذلك البيانات نفسها.

حاول تشغيل الأمر `bufr_dump` على ملف المثال الثاني `bufr-cli-ex2.bufr4`:

```{.copy}
bufr_dump bufr-cli-ex2.bufr4
```

ينتج عن ذلك JSON قد يكون من الصعب تحليله. حاول استخدام الخيار `-p` لإخراج البيانات بتنسيق نص عادي (key=value):

```{.copy}
bufr_dump -p bufr-cli-ex2.bufr4
```

سترى عددًا كبيرًا من المفاتيح كإخراج، العديد منها مفقود. هذا أمر شائع مع البيانات الواقعية حيث لا يتم تعبئة جميع مفاتيح eccodes بالبيانات المبلغ عنها.

يمكنك استخدام الأمر `grep` لتصفية الإخراج وعرض المفاتيح غير المفقودة فقط. على سبيل المثال، لعرض جميع المفاتيح غير المفقودة، يمكنك استخدام الأمر التالي:

```{.copy}
bufr_dump -p bufr-cli-ex2.bufr4 | grep -v MISSING
```

!!! question

    ما هو الضغط المعدل إلى مستوى سطح البحر المبلغ عنه في ملف BUFR `bufr-cli-ex2.bufr4`؟

??? success "اضغط للكشف عن الإجابة"

    باستخدام الأمر التالي:

    ```bash
    bufr_dump -p bufr-cli-ex2.bufr4 | grep -i 'pressureReducedToMeanSeaLevel'
    ```

    سترى الإخراج التالي:

    ```
    pressureReducedToMeanSeaLevel=105590
    ```
    يشير هذا إلى أن الضغط المعدل إلى مستوى سطح البحر هو 105590 باسكال (1055.90 هكتوباسكال).

!!! question

    ما هو معرف محطة WIGOS للمحطة التي أبلغت عن البيانات في ملف BUFR `bufr-cli-ex2.bufr4`؟

??? success "اضغط للكشف عن الإجابة"

    باستخدام الأمر التالي:

    ```bash
    bufr_dump -p bufr-cli-ex2.bufr4 | grep -i 'wigos'
    ```

    سترى الإخراج التالي:

    ```
    wigosIdentifierSeries=0
    wigosIssuerOfIdentifier=20000
    wigosIssueNumber=0
    wigosLocalIdentifierCharacter="99100"
    ```

    يشير هذا إلى أن معرف محطة WIGOS هو `0-20000-0-99100`.

## تحويل synop2bufr

بعد ذلك، دعونا نلقي نظرة على كيفية تحويل بيانات FM-12 SYNOP إلى تنسيق BUFR باستخدام وحدة `synop2bufr`. تُستخدم وحدة `synop2bufr` لتحويل بيانات FM-12 SYNOP إلى تنسيق BUFR. يتم تثبيت الوحدة في حاوية wis2box-api ويمكن استخدامها من سطر الأوامر كما يلي:

```{.copy}
synop2bufr data transform \
    --metadata <station-metadata.csv> \
    --output-dir <output-directory-path> \
    --year <year-of-observation> \
    --month <month-of-observation> \
    <input-fm12.txt>
```

يُستخدم الوسيط `--metadata` لتحديد ملف بيانات المحطة الوصفية، الذي يوفر معلومات إضافية ليتم ترميزها في ملف BUFR.
يُستخدم الوسيط `--output-dir` لتحديد الدليل الذي سيتم كتابة ملفات BUFR المحولة فيه. تُستخدم الوسيطتان `--year` و`--month` لتحديد سنة وشهر الملاحظة.

تُستخدم وحدة `synop2bufr` أيضًا في wis2box-webapp لتحويل بيانات FM-12 SYNOP إلى تنسيق BUFR باستخدام نموذج إدخال مستند إلى الويب.

ستوضح التمارين التالية كيفية عمل وحدة `synop2bufr` وكيفية استخدامها لتحويل بيانات FM-12 SYNOP إلى تنسيق BUFR.

### مراجعة رسالة SYNOP كمثال

افحص ملف رسالة SYNOP كمثال لهذا التمرين `synop_message.txt`:

```bash
cd /root/data-conversion-exercises
more synop_message.txt
```

!!! question

    كم عدد تقارير SYNOP الموجودة في هذا الملف؟

??? success "اضغط للكشف عن الإجابة"
    
    يُظهر الإخراج ما يلي:

    ```{.copy}
    AAXX 21121
    15015 02999 02501 10103 21090 39765 42952 57020 60001=
    15020 02997 23104 10130 21075 30177 40377 58020 60001 81041=
    15090 02997 53102 10139 21075 30271 40364 58031 60001 82046=
    ```

    هناك 3 تقارير SYNOP في الملف، تتوافق مع 3 محطات مختلفة (تم تحديدها بواسطة معرفات المحطات التقليدية المكونة من 5 أرقام: 15015، 15020، و15090).
    لاحظ أن نهاية كل تقرير يتم تمييزها بالحرف `=`.

### مراجعة قائمة المحطات

يتطلب الوسيط `--metadata` ملف CSV باستخدام تنسيق محدد مسبقًا. يتم توفير مثال عملي في الملف `station_list.csv`:

استخدم الأمر التالي لفحص محتويات ملف `station_list.csv`:

```bash
more station_list.csv
```

!!! question

    كم عدد المحطات المدرجة في قائمة المحطات؟ ما هي معرفات محطات WIGOS لهذه المحطات؟

??? success "اضغط للكشف عن الإجابة"

    يُظهر الإخراج ما يلي:

    ```{.copy}
    station_name,wigos_station_identifier,traditional_station_identifier,facility_type,latitude,longitude,elevation,barometer_height,territory_name,wmo_region
    OCNA SUGATAG,0-20000-0-15015,15015,landFixed,47.7770616258,23.9404602638,503.0,504.0,ROU,europe
    BOTOSANI,0-20000-0-15020,15020,landFixed,47.7356532437,26.6455501701,161.0,162.1,ROU,europe
    ```

    يتوافق هذا مع بيانات المحطة الوصفية لمحطتين: معرفات محطات WIGOS هي `0-20000-0-15015` و`0-20000-0-15020`.

### تحويل SYNOP إلى BUFR

بعد ذلك، استخدم الأمر التالي لتحويل رسالة FM-12 SYNOP إلى تنسيق BUFR:

```bash
synop2bufr data transform --metadata station_list.csv --output-dir ./ --year 2024 --month 09 synop_message.txt
```

!!! question
    كم عدد ملفات BUFR التي تم إنشاؤها؟ ماذا تعني رسالة التحذير في الإخراج؟

??? success "اضغط للكشف عن الإجابة"
    يُظهر الإخراج ما يلي:

    ```{.copy}
    [WARNING] Station 15090 not found in station file
    ```

    إذا قمت بفحص محتوى الدليل الخاص بك باستخدام الأمر `ls -lh`، يجب أن ترى أنه تم إنشاء ملفي BUFR جديدين: `WIGOS_0-20000-0-15015_20240921T120000.bufr4` و`WIGOS_0-20000-0-15020_20240921T120000.bufr4`.

    تشير رسالة التحذير إلى أن المحطة ذات المعرف التقليدي `15090` لم يتم العثور عليها في ملف قائمة المحطات `station_list.csv`. وهذا يعني أن تقرير SYNOP لهذه المحطة لم يتم تحويله إلى تنسيق BUFR.

!!! question
    تحقق من محتوى ملف BUFR `WIGOS_0-20000-0-15015_20240921T120000.bufr4` باستخدام الأمر `bufr_dump`.

    هل يمكنك التحقق من أن المعلومات المقدمة في ملف `station_list.csv` موجودة في ملف BUFR؟

??? success "اضغط للكشف عن الإجابة"
    يمكنك استخدام الأمر التالي للتحقق من محتوى ملف BUFR:

    ```bash
    bufr_dump -p WIGOS_0-20000-0-15015_20240921T120000.bufr4 | grep -v MISSING
    ```

    ستلاحظ الإخراج التالي:

    ```{.copy}
    wigosIdentifierSeries=0
    wigosIssuerOfIdentifier=20000
    wigosIssueNumber=0
    wigosLocalIdentifierCharacter="15015"
    blockNumber=15
    stationNumber=15
    stationOrSiteName="OCNA SUGATAG"
    stationType=1
    year=2024
    month=9
    day=21
    hour=12
    minute=0
    latitude=47.7771
    longitude=23.9405
    heightOfStationGroundAboveMeanSeaLevel=503
    heightOfBarometerAboveMeanSeaLevel=504
    ```

    لاحظ أن هذا يتضمن البيانات المقدمة في ملف `station_list.csv`.

### نموذج SYNOP في wis2box-webapp

يُستخدم أيضًا الوحدة `synop2bufr` في تطبيق `wis2box-webapp` لتحويل بيانات FM-12 SYNOP إلى صيغة BUFR باستخدام نموذج إدخال عبر الويب.  
لاختبار ذلك، انتقل إلى `http://YOUR-HOST/wis2box-webapp` وقم بتسجيل الدخول.

اختر `SYNOP Form` من القائمة على اليسار وقم بنسخ ولصق محتويات ملف `synop_message.txt`:

```{.copy}
AAXX 21121
15015 02999 02501 10103 21090 39765 42952 57020 60001=
15020 02997 23104 10130 21075 30177 40377 58020 60001 81041=
15090 02997 53102 10139 21075 30271 40364 58031 60001 82046=
```

في منطقة النص `SYNOP message`:

<img alt="synop-form" src="/../assets/img/wis2box-webapp-synop-form.png" width="800">

!!! question
    هل يمكنك إرسال النموذج؟ ما هي النتيجة؟

??? success "انقر للكشف عن الإجابة"

    تحتاج إلى اختيار مجموعة بيانات وتوفير الرمز المميز لـ "processes/wis2box" الذي قمت بإنشائه في التمرين السابق لإرسال النموذج.

    إذا قمت بتوفير رمز مميز غير صالح، ستظهر الرسالة التالية:
    
    - النتيجة: غير مصرح بها، يرجى توفير رمز مميز صالح لـ 'processes/wis2box'

    إذا قمت بتوفير رمز مميز صالح، ستظهر الرسالة "WARNINGS: 3". انقر على "WARNINGS" لفتح القائمة المنسدلة التي ستعرض:

    - المحطة 15015 غير موجودة في ملف المحطات
    - المحطة 15020 غير موجودة في ملف المحطات
    - المحطة 15090 غير موجودة في ملف المحطات

    لتحويل هذه البيانات إلى صيغة BUFR، ستحتاج إلى تكوين المحطات المقابلة في `wis2box` والتأكد من أن المحطات مرتبطة بالموضوع الخاص بمجموعة البيانات الخاصة بك.

!!! note

    في التمرين الخاص بـ [ingesting-data-for-publication](./ingesting-data-for-publication.md)، قمت بإدخال الملف "synop_202412030900.txt" وتم تحويله إلى صيغة BUFR بواسطة الوحدة `synop2bufr`.

    في سير العمل الآلي في `wis2box`، يتم استخراج السنة والشهر تلقائيًا من اسم الملف واستخدامهما لملء الوسيطتين `--year` و`--month` المطلوبتين بواسطة `synop2bufr`، بينما يتم استخراج بيانات المحطة تلقائيًا من تكوين المحطة في `wis2box`.

## تحويل csv2bufr

!!! note
    تأكد من أنك لا تزال مسجل الدخول في حاوية `wis2box-api` وفي الدليل `/root/data-conversion-exercises`. إذا خرجت من الحاوية في التمرين السابق، يمكنك تسجيل الدخول مرة أخرى كما يلي:

    ```bash
    cd ~/wis2box
    python3 wis2box-ctl.py login wis2box-api
    cd /root/data-conversion-exercises
    ```

الآن دعنا نلقي نظرة على كيفية تحويل بيانات CSV إلى صيغة BUFR باستخدام الوحدة `csv2bufr`. الوحدة مثبتة في حاوية `wis2box-api` ويمكن استخدامها من سطر الأوامر كما يلي:

```{.copy}
csv2bufr data transform \
    --bufr-template <bufr-mapping-template> \
    <input-csv-file>
```

يُستخدم الوسيط `--bufr-template` لتحديد ملف قالب تعيين BUFR، الذي يوفر التعيين بين بيانات CSV المدخلة وبيانات BUFR الناتجة، ويتم تحديده في ملف JSON. يتم تثبيت قوالب التعيين الافتراضية في الدليل `/opt/csv2bufr/templates` في حاوية `wis2box-api`.

### مراجعة ملف CSV المثال

راجع محتوى ملف CSV المثال `aws-example.csv`:

```bash
more aws-example.csv
```

!!! question
    كم عدد صفوف البيانات الموجودة في ملف CSV؟ ما هو معرف محطة WIGOS للمحطات التي تقدم تقارير في ملف CSV؟

??? question "انقر للكشف عن الإجابة"

    يُظهر الإخراج ما يلي:

    ```{.copy}
    wsi_series,wsi_issuer,wsi_issue_number,wsi_local,wmo_block_number,wmo_station_number,station_type,year,month,day,hour,minute,latitude,longitude,station_height_above_msl,barometer_height_above_msl,station_pressure,msl_pressure,geopotential_height,thermometer_height,air_temperature,dewpoint_temperature,relative_humidity,method_of_ground_state_measurement,ground_state,method_of_snow_depth_measurement,snow_depth,precipitation_intensity,anemometer_height,time_period_of_wind,wind_direction,wind_speed,maximum_wind_gust_direction_10_minutes,maximum_wind_gust_speed_10_minutes,maximum_wind_gust_direction_1_hour,maximum_wind_gust_speed_1_hour,maximum_wind_gust_direction_3_hours,maximum_wind_gust_speed_3_hours,rain_sensor_height,total_precipitation_1_hour,total_precipitation_3_hours,total_precipitation_6_hours,total_precipitation_12_hours,total_precipitation_24_hours
    0,20000,0,60355,60,355,1,2024,3,31,1,0,47.77706163,23.94046026,503,504.43,100940,101040,1448,5,298.15,294.55,80,3,1,1,0,0.004,10,-10,30,3,30,5,40,9,20,11,2,4.7,5.3,7.9,9.5,11.4
    0,20000,0,60355,60,355,1,2024,3,31,2,0,47.77706163,23.94046026,503,504.43,100940,101040,1448,5,25.,294.55,80,3,1,1,0,0.004,10,-10,30,3,30,5,40,9,20,11,2,4.7,5.3,7.9,9.5,11.4
    0,20000,0,60355,60,355,1,2024,3,31,3,0,47.77706163,23.94046026,503,504.43,100940,101040,1448,5,298.15,294.55,80,3,1,1,0,0.004,10,-10,30,3,30,5,40,9,20,11,2,4.7,5.3,7.9,9.5,11.4
    ```

    يحتوي الصف الأول من ملف CSV على رؤوس الأعمدة، التي تُستخدم لتحديد البيانات في كل عمود.

    بعد صف الرؤوس، هناك 3 صفوف من البيانات، تمثل 3 ملاحظات جوية من نفس المحطة بمعرف محطة WIGOS `0-20000-0-60355` في ثلاث طوابع زمنية مختلفة: `2024-03-31 01:00:00`، `2024-03-31 02:00:00`، و`2024-03-31 03:00:00`.

### مراجعة aws-template

يتضمن `wis2box-api` مجموعة من قوالب تعيين BUFR المعرفة مسبقًا والتي يتم تثبيتها في الدليل `/opt/csv2bufr/templates`.

تحقق من محتوى الدليل `/opt/csv2bufr/templates`:

```bash
ls /opt/csv2bufr/templates
```

يجب أن ترى الإخراج التالي:

```{.copy}
CampbellAfrica-v1-template.json  aws-template.json  daycli-template.json
```

دعنا نتحقق من محتوى ملف `aws-template.json`:

```bash
cat /opt/csv2bufr/templates/aws-template.json
```

يعيد هذا ملف JSON كبيرًا، يوفر التعيين لـ 43 عمودًا في CSV.

!!! question
    ما هو عمود CSV الذي يتم تعيينه إلى المفتاح `airTemperature` في eccodes؟ ما هي القيم الدنيا والقصوى الصالحة لهذا المفتاح؟

??? success "انقر للكشف عن الإجابة"

    باستخدام الأمر التالي لتصفية الإخراج:

    ```bash
    cat /opt/csv2bufr/templates/aws-template.json | grep -i airTemperature
    ```
    يجب أن ترى الإخراج التالي:

    ```{.copy}
    {"eccodes_key": "#1#airTemperature", "value": "data:air_temperature", "valid_min": "const:193.15", "valid_max": "const:333.15"},
    ```

    القيمة التي سيتم ترميزها للمفتاح `airTemperature` في eccodes سيتم أخذها من البيانات في عمود CSV: **air_temperature**.

    القيم الدنيا والقصوى لهذا المفتاح هي `193.15` و`333.15` على التوالي.

!!! question

    ما هو عمود CSV الذي يتم تعيينه إلى المفتاح `internationalDataSubCategory` في eccodes؟ ما هي قيمة هذا المفتاح؟

??? success "انقر للكشف عن الإجابة"
    باستخدام الأمر التالي لتصفية الإخراج:

    ```bash
    cat /opt/csv2bufr/templates/aws-template.json | grep -i internationalDataSubCategory
    ```
    يجب أن ترى الإخراج التالي:

    ```{.copy}
    {"eccodes_key": "internationalDataSubCategory", "value": "const:2"},
    ```

**لا يوجد عمود CSV مرتبط بالمفتاح `internationalDataSubCategory` في eccodes**، وبدلاً من ذلك يتم استخدام القيمة الثابتة 2 والتي سيتم ترميزها في جميع ملفات BUFR التي يتم إنتاجها باستخدام قالب التعيين هذا.

### تحويل CSV إلى BUFR

لنحاول تحويل الملف إلى تنسيق BUFR باستخدام الأمر `csv2bufr`:

```{.copy}
csv2bufr data transform --bufr-template aws-template ./aws-example.csv
```

!!! question
    كم عدد ملفات BUFR التي تم إنشاؤها؟

??? success "اضغط للكشف عن الإجابة"

    تُظهر النتيجة ما يلي:

    ```{.copy}
    CLI:    ... Transforming ./aws-example.csv to BUFR ...
    CLI:    ... Processing subsets:
    CLI:    ..... 384 bytes written to ./WIGOS_0-20000-0-60355_20240331T010000.bufr4
    #1#airTemperature: Value (25.0) out of valid range (193.15 - 333.15).; Element set to missing
    CLI:    ..... 384 bytes written to ./WIGOS_0-20000-0-60355_20240331T020000.bufr4
    CLI:    ..... 384 bytes written to ./WIGOS_0-20000-0-60355_20240331T030000.bufr4
    CLI:    End of processing, exiting.
    ```

    تشير النتيجة إلى أنه تم إنشاء 3 ملفات BUFR: `WIGOS_0-20000-0-60355_20240331T010000.bufr4`، `WIGOS_0-20000-0-60355_20240331T020000.bufr4`، و`WIGOS_0-20000-0-60355_20240331T030000.bufr4`.

للتحقق من محتوى ملفات BUFR مع تجاهل القيم المفقودة، يمكنك استخدام الأمر التالي:

```bash
bufr_dump -p WIGOS_0-20000-0-60355_20240331T010000.bufr4 | grep -v MISSING
```

!!! question
    ما هي قيمة المفتاح `airTemperature` في ملف BUFR `WIGOS_0-20000-0-60355_20240331T010000.bufr4`؟ وماذا عن ملف BUFR `WIGOS_0-20000-0-60355_20240331T020000.bufr4`؟

??? success "اضغط للكشف عن الإجابة"
    لتصفية النتيجة، يمكنك استخدام الأمر التالي:

    ```bash
    bufr_dump -p WIGOS_0-20000-0-60355_20240331T010000.bufr4 | grep -v MISSING | grep airTemperature
    ```
    يجب أن ترى النتيجة التالية:

    ```{.copy}
    #1#airTemperature=298.15
    ```

    بينما بالنسبة للملف الثاني:

    ```bash
    bufr_dump -p WIGOS_0-20000-0-60355_20240331T020000.bufr4 | grep -v MISSING | grep airTemperature
    ```

    لن تحصل على أي نتيجة، مما يشير إلى أن القيمة للمفتاح `airTemperature` مفقودة في ملف BUFR `WIGOS_0-20000-0-60355_20240331T020000.bufr4`. رفض `csv2bufr` ترميز القيمة `25.0` من بيانات CSV لأنها تقع خارج النطاق المسموح به `193.15` و`333.15` كما هو محدد في قالب التعيين.

لاحظ أن تحويل CSV إلى BUFR باستخدام أحد قوالب تعيين BUFR المحددة مسبقًا له قيود:

- يجب أن يكون ملف CSV بالتنسيق المحدد في قالب التعيين، أي يجب أن تتطابق أسماء أعمدة CSV مع الأسماء المحددة في قالب التعيين.
- يمكنك فقط ترميز المفاتيح المحددة في قالب التعيين.
- عمليات التحقق من الجودة محدودة بالتحقق المحدد في قالب التعيين.

للحصول على معلومات حول كيفية إنشاء واستخدام قوالب تعيين BUFR مخصصة، راجع التمرين العملي التالي [csv2bufr-templates](./csv2bufr-templates.md).

## الخلاصة

!!! success "تهانينا!"
    في هذه الجلسة العملية، تعلمت:

    - كيفية الوصول إلى أدوات سطر الأوامر ecCodes داخل حاوية wis2box-api
    - كيفية استخدام `synop2bufr` لتحويل تقارير FM-12 SYNOP إلى BUFR من سطر الأوامر
    - كيفية استخدام نموذج SYNOP في wis2box-webapp لتحويل تقارير FM-12 SYNOP إلى BUFR
    - كيفية استخدام `csv2bufr` لتحويل بيانات CSV إلى BUFR من سطر الأوامر
---
title: العمل مع بيانات BUFR
---

# العمل مع بيانات BUFR

!!! abstract "نتائج التعلم"
    في هذه الجلسة العملية، سيتم تعريفك على بعض أدوات BUFR المتضمنة في حاوية **wis2box-api** والتي تُستخدم لتحويل البيانات إلى تنسيق BUFR وقراءة المحتوى المُشفر في BUFR.
    
    ستتعلم:

    - كيفية فحص الرؤوس في ملف BUFR باستخدام الأمر `bufr_ls`
    - كيفية استخراج وفحص البيانات داخل ملف bufr باستخدام `bufr_dump`
    - الهيكل الأساسي لقوالب bufr المستخدمة في csv2bufr وكيفية استخدام أداة سطر الأوامر
    - وكيفية إجراء تغييرات أساسية على قوالب bufr وكيفية تحديث wis2box لاستخدام النسخة المعدلة

## مقدمة

الإضافات التي تنتج إشعارات ببيانات BUFR تستخدم عمليات في wis2box-api للعمل مع بيانات BUFR، على سبيل المثال لتحويل البيانات من CSV إلى BUFR أو من BUFR إلى geojson.

تشتمل حاوية wis2box-api على عدد من الأدوات للعمل مع بيانات BUFR.

تشمل هذه الأدوات المطورة من قبل ECMWF والمتضمنة في برنامج ecCodes، يمكن العثور على مزيد من المعلومات حول هذه على [موقع ecCodes](https://confluence.ecmwf.int/display/ECC/BUFR+tools).

في هذه الجلسة، سيتم تعريفك على الأوامر `bufr_ls` و `bufr_dump` من حزمة برامج ecCodes وتكوين متقدم لأداة csv2bufr.

## التحضير

لكي تستخدم أدوات سطر الأوامر BUFR، ستحتاج إلى تسجيل الدخول إلى حاوية wis2box-api
وما لم يُذكر خلاف ذلك، يجب تشغيل جميع الأوامر على هذه الحاوية. ستحتاج أيضًا إلى فتح MQTT Explorer والاتصال بوسيطك.

أولاً، قم بالاتصال بجهاز الطالب الافتراضي الخاص بك عبر عميل ssh الخاص بك ثم سجل الدخول إلى حاوية wis2box-api:

```{.copy}
cd ~/wis2box-1.0.0rc1
python3 wis2box-ctl.py login wis2box-api
```

تأكد من توفر الأدوات، بدءًا من ecCodes:

``` {.copy}
bufr_dump -V
```
يجب أن تحصل على الاستجابة التالية:

```
ecCodes Version 2.28.0
```

ثم تحقق من csv2bufr:

```{.copy}
csv2bufr --version
```

يجب أن تحصل على الاستجابة التالية:

```
csv2bufr, version 0.7.4
```

أخيرًا، قم بإنشاء دليل عمل للعمل فيه:

```{.copy}
cd /data/wis2box
mkdir -p working/bufr-cli
cd working/bufr-cli
```

أنت الآن جاهز لبدء استخدام أدوات BUFR.

## استخدام أدوات سطر الأوامر BUFR

### التمرين 1 - bufr_ls
في هذا التمرين الأول، ستستخدم الأمر `bufr_ls` لفحص رؤوس ملف BUFR وتحديد محتويات الملف. تتضمن الرؤوس التالية في ملف BUFR:

| الرأس                            | مفتاح ecCodes                  | الوصف                                                                                                                                           |
|-----------------------------------|------------------------------|-------------------------------------------------------------------------------------------------------------------------------------------------------|
| المركز الأصلي/المولد     | centre                       | المركز الأصلي / المولد للبيانات                                                                                                      |
| المركز الفرعي الأصلي/المولد | bufrHeaderSubCentre          | المركز الفرعي الأصلي / المولد للبيانات                                                                                                  | 
| رقم تسلسل التحديث            | updateSequenceNumber         | هل هذه هي النسخة الأولى من البيانات (0) أو تحديث (>0)                                                                                   |               
| فئة البيانات                     | dataCategory                 | نوع البيانات الموجودة في رسالة BUFR، على سبيل المثال، بيانات السطح. انظر [جدول BUFR A](https://github.com/wmo-im/BUFR4/blob/master/BUFR_TableA_en.csv)  |
| الفئة الفرعية الدولية للبيانات   | internationalDataSubCategory | النوع الفرعي للبيانات الموجودة في رسالة BUFR، على سبيل المثال، بيانات السطح. انظر [جدول الرموز المشترك C-13](https://github.com/wmo-im/CCT/blob/master/C13.csv) |
| السنة                              | typicalYear (typicalDate)    | الوقت الأكثر نموذجية لمحتويات رسالة BUFR                                                                                                       |
| الشهر                             | typicalMonth (typicalDate)   | الوقت الأكثر نموذجية لمحتويات رسالة BUFR                                                                                                       |
| اليوم                               | typicalDay (typicalDate)     | الوقت الأكثر نموذجية لمحتويات رسالة BUFR                                                                                                       |
| الساعة                              | typicalHour (typicalTime)    | الوقت الأكثر نموذجية لمحتويات رسالة BUFR                                                                                                       |
| الدقيقة                            | typicalMinute (typicalTime)  | الوقت الأكثر نموذجية لمحتويات رسالة BUFR                                                                                                       |
| وصفات BUFR                  | unexpandedDescriptors        | قائمة بواحد أو أكثر من وصفات BUFR التي تحدد البيانات الموجودة في الملف                                                                        |

قم بتنزيل الملف المثالي مباشرة إلى حاوية إدارة wis2box باستخدام الأمر التالي:

``` {.copy}
curl https://training.wis2box.wis.wmo.int/sample-data/bufr-cli-ex1.bufr4 --output bufr-cli-ex1.bufr4
```

الآن استخدم الأمر التالي لتشغيل `bufr_ls` على هذا الملف:

```bash
bufr_ls bufr-cli-ex1.bufr4
```

يجب أن ترى الإخراج التالي:

```bash
bufr-cli-ex1.bufr4
centre                     masterTablesVersionNumber  localTablesVersionNumber   typicalDate                typicalTime                numberOfSubsets
cnmc                       29                         0                          20231002                   000000                     1
1 of 1 messages in bufr-cli-ex1.bufr4

1 of 1 total messages in 1 files
```

بمفردها، هذه المعلومات ليست مفيدة جدًا، حيث تقدم معلومات محدودة فقط عن محتويات الملف.

الإخراج الافتراضي لا يقدم معلومات حول نوع الرصد أو البيانات، وهو بتنسيق ليس سهل القراءة. ومع ذلك، يمكن تمرير خيارات مختلفة إلى `bufr_ls` لتغيير كل من التنسيق وحقول الرأس المطبوعة.

استخدم `bufr_ls` بدون أي حجج لعرض الخيارات:

```{.copy}
bufr_ls
```

يجب أن ترى الإخراج التالي:

```
NAME    bufr_ls

DESCRIPTION
        List content of BUFR files printing values of some header keys.
        Only scalar keys can be printed.
        It does not fail when a key is not found.

USAGE
        bufr_ls [options] bufr_file bufr_file ...

OPTIONS
        -p key[:{s|d|i}],key[:{s|d|i}],...
                Declaration of keys to print.
                For each key a string (key:s), a double (key:d) or an integer (key:i)
                type can be requested. Default type is string.
        -F format
                C style format for floating-point values.
        -P key[:{s|d|i}],key[:{s|d|i}],...
                As -p adding the declared keys to the default list.
        -w key[:{s|d|i}]{=|!=}value,key[:{s|d|i}]{=|!=}value,...
                Where clause.
                Messages are processed only if they match all the key/value constraints.
                A valid constraint is of type key=value or key!=value.
                For each key a string (key:s), a double (key:d) or an integer (key:i)
                type can be specified. Default type is string.
                In the value you can also use the forward-slash character '/' to specify an OR condition (i.e. a logical disjunction)
                Note: only one -w clause is allowed.
        -j      JSON output
        -s key[:{s|d|i}]=value,key[:{s|d|i}]=value,...
                Key/values to set.
                For each key a string (key:s), a double (key:d) or an integer (key:i)
                type can be defined. By default the native type is set.
        -n namespace
                All the keys belonging to the given namespace are printed.
        -m      Mars keys are printed.
        -V      Version.
        -W width
                Minimum width of each column in output. Default is 10.
        -g      Copy GTS header.
        -7      Does not fail when the message has wrong length

SEE ALSO
        Full documentation and examples at:
        <https://confluence.ecmwf.int/display/ECC/bufr_ls>
```

الآن قم بتشغيل نفس الأمر على الملف المثالي ولكن قم بإخراج المعلومات بتنسيق JSON.

!!! question
    أي علم تمرره إلى الأمر `bufr_ls` لعرض الإخراج بتنسيق JSON؟

??? success "انقر لكشف الإجابة"
    يمكنك تغيير تنسيق الإخراج إلى json باستخدام العلم `-j`، أي
    `bufr_ls -j <input-file>`. قد يكون هذا أكثر قابلية للقراءة من تنسيق الإخراج الافتراضي. انظر الإخراج المثالي أدناه:

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

عند فحص ملف BUFR، غالبًا ما نرغب في تحديد نوع البيانات الموجودة في الملف والتاريخ / الوقت النموذجي
للبيانات في الملف. يمكن سرد هذه المعلومات باستخدام العلم `-p` لتحديد الرؤوس للإخراج. يمكن تضمين رؤوس متعددة باستخدام قائمة مفصولة بفواصل.

باستخدام الأمر `bufr_ls`، فحص ملف الاختبار وتحديد نوع البيانات الموجودة في الملف والتاريخ والوقت النموذجي لتلك البيانات.

??? hint
    تُعطى مفاتيح ecCodes في الجدول أعلاه. يمكننا استخدام ما يلي لسرد فئة البيانات و
    الفئة الفرعية الدولية لبيانات BUFR:

    ```
    bufr_ls -p dataCategory,internationalDataSubCategory bufr-cli-ex1.bufr4
    ```

    يمكن إضافة مفاتيح إضافية حسب الحاجة.

!!! question
    ما نوع البيانات (فئة البيانات والفئة الفرعية) الموجودة في الملف؟ ما هو التاريخ والوقت النموذجي
    للبيانات؟

??? success "انقر لكشف الإجابة"
    يجب أن يكون الأمر الذي تحتاج إلى تشغيله مشابهًا لما يلي:
    
    ```
    bufr_ls -p dataCategory,internationalDataSubCategory,typicalDate,typicalTime -j bufr-cli-ex1.bufr4
    ```

    قد تكون لديك مفاتيح إضافية، أو قمت بسرد السنة والشهر واليوم وما إلى ذلك بشكل فردي. يجب أن يكون الإخراج مشابهًا لما يلي، اعتمادًا على ما إذا كنت قد اخترت تنسيق JSON أو الإخراج الافتراضي.

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

    من هذا نرى أن:

    - فئة البيانات هي 2، من [جدول BUFR A](https://github.com/wmo-im/BUFR4/blob/master/BUFR_TableA_en.csv)
      يمكننا أن نرى أن هذا الملف يحتوي على بيانات "الرصد العمودي (بخلاف الأقمار الصناعية)".
    - الفئة الفرعية الدولية هي 4، مما يشير
      إلى "تقارير درجة الحرارة/الرطوبة/الرياح على مستوى ع
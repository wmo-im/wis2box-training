---
title: اكتشاف مجموعات البيانات من WIS2 Global Discovery Catalogue
---

# اكتشاف مجموعات البيانات من WIS2 Global Discovery Catalogue

!!! abstract "نتائج التعلم!"

    بنهاية هذه الجلسة العملية، ستكون قادرًا على:

    - استخدام pywiscat لاكتشاف مجموعات البيانات من Global Discovery Catalogue (GDC)

## المقدمة

في هذه الجلسة، ستتعلم كيفية اكتشاف البيانات من WIS2 Global Discovery Catalogue (GDC) باستخدام [pywiscat](https://github.com/wmo-im/pywiscat)، وهو أداة سطر أوامر للبحث واسترجاع البيانات الوصفية من WIS2 GDC.

حاليًا، تتوفر GDCs التالية:

- هيئة البيئة وتغير المناخ الكندية، خدمة الأرصاد الجوية الكندية: <https://wis2-gdc.weather.gc.ca>
- إدارة الأرصاد الجوية الصينية: <https://gdc.wis.cma.cn>
- خدمة الأرصاد الجوية الألمانية: <https://wis2.dwd.de/gdc>

خلال جلسات التدريب المحلية، يتم إعداد GDC محلي للسماح للمشاركين بالاستعلام عن GDC للحصول على البيانات الوصفية التي قاموا بنشرها من مثيلات wis2box الخاصة بهم. في هذه الحالة، سيقدم المدربون عنوان URL الخاص بـ GDC المحلي.

## التحضير

!!! note
    قبل البدء، يرجى تسجيل الدخول إلى جهاز الطالب الافتراضي الخاص بك.

## تثبيت pywiscat

استخدم أداة تثبيت حزم Python `pip3` لتثبيت pywiscat على جهازك الافتراضي:
```bash
pip3 install pywiscat
```

!!! note

    إذا واجهت الخطأ التالي:

    ```
    WARNING: The script pywiscat is installed in '/home/username/.local/bin' which is not on PATH.
    Consider adding this directory to PATH or, if you prefer to suppress this warning, use --no-warn-script-location.
    ```

    قم بتشغيل الأمر التالي:

    ```bash
    export PATH=$PATH:/home/$USER/.local/bin
    ```

    ...حيث `$USER` هو اسم المستخدم الخاص بك على جهازك الافتراضي.

تحقق من نجاح التثبيت:

```bash
pywiscat --version
```

## العثور على البيانات باستخدام pywiscat

بشكل افتراضي، يتصل pywiscat بـ Global Discovery Catalogue (GDC) المستضاف من قبل Environment and Climate Change Canada (ECCC).

!!! note "تغيير عنوان URL الخاص بـ GDC"
    إذا كنت تقوم بهذا التمرين خلال جلسة تدريب محلية، يمكنك تكوين pywiscat للاستعلام عن GDC المحلي عن طريق تعيين متغير البيئة `PYWISCAT_GDC_URL`:

    ```bash
    export PYWISCAT_GDC_URL=http://gdc.wis2.training:5002
    ```

لرؤية الخيارات المتاحة، قم بتشغيل:

```bash
pywiscat search --help
```

يمكنك البحث في GDC عن جميع السجلات:

```bash
pywiscat search
```

!!! question

    كم عدد السجلات التي تم إرجاعها من البحث؟

??? success "اضغط للكشف عن الإجابة"
    يعتمد عدد السجلات على GDC الذي تقوم بالاستعلام منه. عند استخدام GDC التدريب المحلي، يجب أن ترى أن عدد السجلات يساوي عدد مجموعات البيانات التي تم إدخالها في GDC خلال الجلسات العملية الأخرى.

لنجرّب استعلام GDC باستخدام كلمة مفتاحية:

```bash
pywiscat search -q observations
```

!!! question

    ما هي سياسة البيانات للنتائج؟

??? success "اضغط للكشف عن الإجابة"
    يجب أن تحدد جميع البيانات التي تم إرجاعها أنها بيانات "core".

جرّب استعلامات إضافية باستخدام `-q`

!!! tip

    يتيح لك العلم `-q` استخدام الصيغ التالية:

    - `-q synop`: العثور على جميع السجلات التي تحتوي على الكلمة "synop"
    - `-q temp`: العثور على جميع السجلات التي تحتوي على الكلمة "temp"
    - `-q "observations AND oman"`: العثور على جميع السجلات التي تحتوي على الكلمات "observations" و"oman"
    - `-q "observations NOT oman"`: العثور على جميع السجلات التي تحتوي على الكلمة "observations" ولكن ليس الكلمة "oman"
    - `-q "synop OR temp"`: العثور على جميع السجلات التي تحتوي على "synop" أو "temp"
    - `-q "obs*"`: البحث باستخدام النمط

    عند البحث عن مصطلحات تحتوي على مسافات، قم بوضعها بين علامات اقتباس مزدوجة.

للحصول على مزيد من التفاصيل حول نتيجة بحث محددة تهمك:

```bash
pywiscat get <id>
```

!!! tip

    استخدم قيمة `id` من البحث السابق.

## الخاتمة

!!! success "تهانينا!"

    في هذه الجلسة العملية، تعلمت كيفية:

    - استخدام pywiscat لاكتشاف مجموعات البيانات من WIS2 Global Discovery Catalogue
---
title: اكتشاف مجموعات البيانات من كتالوج الاكتشاف العالمي WIS2
---

# اكتشاف مجموعات البيانات من كتالوج الاكتشاف العالمي WIS2

!!! abstract "نتائج التعلم!"

    بنهاية هذه الجلسة العملية، ستكون قادراً على:

    - استخدام pywiscat لاكتشاف مجموعات البيانات من Global Discovery Catalogue (GDC)

## مقدمة

في هذه الجلسة ستتعلم كيفية اكتشاف البيانات من WIS2 Global Discovery Catalogue (GDC).

حالياً، تتوفر كتالوجات GDC التالية:

- Environment and Climate Change Canada, Meteorological Service of Canada: <https://wis2-gdc.weather.gc.ca>
- China Meteorological Administration: <https://gdc.wis.cma.cn>
- Deutscher Wetterdienst: <https://wis2.dwd.de/gdc>

خلال جلسات التدريب المحلية، يتم إعداد GDC محلي للسماح للمشاركين بالاستعلام عن البيانات الوصفية التي نشروها من أجهزة wis2box الخاصة بهم. في هذه الحالة سيقدم المدربون رابط GDC المحلي.

## التحضير

!!! note
    قبل البدء، يرجى تسجيل الدخول إلى الجهاز الافتراضي الخاص بك.

## تثبيت pywiscat

استخدم مثبت حزم Python `pip3` لتثبيت pywiscat على جهازك الافتراضي:
```bash
pip3 install pywiscat
```

!!! note

    إذا واجهت الخطأ التالي:

    ```
    WARNING: The script pywiscat is installed in '/home/username/.local/bin' which is not on PATH.
    Consider adding this directory to PATH or, if you prefer to suppress this warning, use --no-warn-script-location.
    ```

    قم بتنفيذ الأمر التالي:

    ```bash
    export PATH=$PATH:/home/$USER/.local/bin
    ```

    حيث `$USER` هو اسم المستخدم الخاص بك على جهازك الافتراضي.

تحقق من نجاح التثبيت:

```bash
pywiscat --version
```

## البحث عن البيانات باستخدام pywiscat

افتراضياً، يتصل pywiscat بكتالوج الاكتشاف العالمي الكندي. دعنا نقوم بتكوين pywiscat للاستعلام عن GDC التدريبي عن طريق تعيين متغير البيئة `PYWISCAT_GDC_URL`:

```bash
export PYWISCAT_GDC_URL=http://gdc.wis2.training:5002
```

لنستخدم [pywiscat](https://github.com/wmo-im/pywiscat) للاستعلام عن GDC المعد كجزء من التدريب.

```bash
pywiscat search --help
```

الآن ابحث في GDC عن جميع السجلات:

```bash
pywiscat search
```

!!! question

    كم عدد السجلات التي تم إرجاعها من البحث؟

??? success "انقر لكشف الإجابة"
    يعتمد عدد السجلات على GDC الذي تستعلم عنه. عند استخدام GDC التدريبي المحلي، يجب أن ترى أن عدد السجلات يساوي عدد مجموعات البيانات التي تم إدخالها في GDC خلال الجلسات العملية الأخرى.

دعنا نجرب الاستعلام عن GDC باستخدام كلمة مفتاحية:

```bash
pywiscat search -q observations
```

!!! question

    ما هي سياسة البيانات للنتائج؟

??? success "انقر لكشف الإجابة"
    جميع البيانات المرجعة يجب أن تحدد بيانات "core"

جرب استعلامات إضافية باستخدام `-q`

!!! tip

    يسمح خيار `-q` بالصيغ التالية:

    - `-q synop`: البحث عن جميع السجلات التي تحتوي على كلمة "synop"
    - `-q temp`: البحث عن جميع السجلات التي تحتوي على كلمة "temp"
    - `-q "observations AND oman"`: البحث عن جميع السجلات التي تحتوي على كلمتي "observations" و "oman"
    - `-q "observations NOT oman"`: البحث عن جميع السجلات التي تحتوي على كلمة "observations" ولكن لا تحتوي على كلمة "oman"
    - `-q "synop OR temp"`: البحث عن جميع السجلات التي تحتوي على "synop" أو "temp"
    - `-q "obs*"`: البحث الضبابي

    عند البحث عن مصطلحات تحتوي على مسافات، ضعها بين علامتي اقتباس مزدوجة.

دعنا نحصل على مزيد من التفاصيل حول نتيجة بحث محددة نهتم بها:

```bash
pywiscat get <id>
```

!!! tip

    استخدم قيمة `id` من البحث السابق.

## الخاتمة

!!! success "تهانينا!"

    في هذه الجلسة العملية، تعلمت كيفية:

    - استخدام pywiscat لاكتشاف مجموعات البيانات من WIS2 Global Discovery Catalogue
---
title: فك تشفير البيانات من التنسيقات الثنائية لـ WMO
---

# فك تشفير البيانات من التنسيقات الثنائية لـ WMO

!!! abstract "نتائج التعلم!"

    بنهاية هذه الجلسة العملية، ستكون قادرًا على:

    - تشغيل حاوية Docker باستخدام صورة "demo-decode-eccodes-jupyter"
    - تشغيل دفاتر Jupyter التوضيحية لفك تشفير البيانات بتنسيقات GRIB2 وNetCDF وBUFR
    - التعرف على أدوات أخرى لفك تشفير وعرض تنسيقات WMO table driven code form (TDCF)

## المقدمة

تُستخدم التنسيقات الثنائية لـ WMO مثل BUFR وGRIB على نطاق واسع في مجتمع الأرصاد الجوية لتبادل بيانات الرصد والنماذج، وعادةً ما تتطلب أدوات متخصصة لفك تشفير البيانات وعرضها.

بعد تنزيل البيانات من WIS2، ستحتاج غالبًا إلى فك تشفير البيانات للاستفادة منها بشكل أكبر.

تتوفر مكتبات برمجية متنوعة لكتابة نصوص أو برامج لفك تشفير التنسيقات الثنائية لـ WMO. كما توجد أدوات توفر واجهة مستخدم لفك تشفير البيانات وعرضها دون الحاجة إلى كتابة برامج.

في هذه الجلسة العملية، سنوضح كيفية فك تشفير ثلاثة أنواع مختلفة من البيانات باستخدام دفتر Jupyter:

- GRIB2 يحتوي على بيانات لتوقعات عالمية مجمعة كما تم إنتاجها بواسطة نظام CMA Global Regional Assimilation PrEdiction System (GRAPES)
- BUFR يحتوي على بيانات مسارات الأعاصير المدارية من نظام التنبؤات المجمعة لـ ECMWF
- NetCDF يحتوي على بيانات شذوذ درجات الحرارة الشهرية

## فك تشفير البيانات التي تم تنزيلها في دفتر Jupyter

لفك تشفير البيانات التي تم تنزيلها، سنبدأ حاوية جديدة باستخدام صورة 'decode-bufr-jupyter'.

ستقوم هذه الحاوية بتشغيل خادم دفتر Jupyter على مثيلك، والذي يتضمن مكتبة [ecCodes](https://sites.ecmwf.int/docs/eccodes) التي يمكنك استخدامها لفك تشفير بيانات BUFR.

سنستخدم دفاتر الملاحظات التوضيحية الموجودة في `~/exercise-materials/notebook-examples` لفك تشفير البيانات التي تم تنزيلها لمسارات الأعاصير.

لتشغيل الحاوية، استخدم الأمر التالي:

```bash
docker run -d --name demo-decode-eccodes-jupyter \
    -v ~/wis2box-data/downloads:/root/downloads \
    -p 8888:8888 \
    -e JUPYTER_TOKEN=dataismagic! \
    ghcr.io/wmo-im/wmo-im/demo-decode-eccodes-jupyter:latest
```

تفصيل الأمر أعلاه:

- `docker run -d --name demo-decode-eccodes-jupyter` يقوم بتشغيل حاوية جديدة في وضع الخلفية (`-d`) ويسميها `demo-decode-eccodes-jupyter`
- `-v ~/wis2box-data/downloads:/root/downloads` يربط دليل `~/wis2box-data/downloads` على جهازك الظاهري بـ `/root/downloads` داخل الحاوية. هذا هو المكان الذي يتم فيه تخزين البيانات التي تم تنزيلها من WIS2
- `-p 8888:8888` يربط المنفذ 8888 على جهازك الظاهري بالمنفذ 8888 داخل الحاوية. هذا يجعل خادم دفتر Jupyter متاحًا من متصفح الويب الخاص بك على `http://YOUR-HOST:8888`
- `-e JUPYTER_TOKEN=dataismagic!` يحدد الرمز المطلوب للوصول إلى خادم دفتر Jupyter. ستحتاج إلى تقديم هذا الرمز عند الوصول إلى الخادم من متصفح الويب الخاص بك
- `ghrc.io/wmo-im/demo-decode-eccodes-jupyter:latest` يحدد الصورة المستخدمة بواسطة الحاوية والتي تتضمن دفاتر الملاحظات التوضيحية المستخدمة في التمارين التالية

!!! note "حول صورة demo-decode-eccodes-jupyter"

    تم تطوير صورة `demo-decode-eccodes-jupyter` لهذه الدورة التدريبية، وهي تستخدم صورة أساسية تتضمن مكتبة ecCodes وتضيف خادم دفتر Jupyter بالإضافة إلى حزم Python لتحليل البيانات وعرضها.

    يمكن العثور على الشيفرة المصدرية لهذه الصورة، بما في ذلك دفاتر الملاحظات التوضيحية، في [wmo-im/demo-decode-eccodes-jupyter](https://github.com/wmo-im/demo-decode-eccodes-jupyter).
    
بمجرد بدء تشغيل الحاوية، يمكنك الوصول إلى خادم دفتر Jupyter على الجهاز الظاهري الخاص بك عن طريق الانتقال إلى `http://YOUR-HOST:8888` في متصفح الويب الخاص بك.

سترى شاشة تطلب منك إدخال "كلمة مرور أو رمز".

قم بإدخال الرمز `dataismagic!` لتسجيل الدخول إلى خادم دفتر Jupyter (ما لم تكن قد استخدمت رمزًا مختلفًا في الأمر أعلاه).

بعد تسجيل الدخول، يجب أن ترى الشاشة التالية التي تعرض الدلائل في الحاوية:

![Jupyter notebook home](../assets/img/jupyter-files-screen1.png)

انقر نقرًا مزدوجًا على دليل `example-notebooks` لفتحه. يجب أن ترى الشاشة التالية التي تعرض دفاتر الملاحظات التوضيحية:

![Jupyter notebook example notebooks](../assets/img/jupyter-files-screen2.png)

يمكنك الآن فتح دفاتر الملاحظات التوضيحية لفك تشفير البيانات التي تم تنزيلها.

### مثال فك تشفير GRIB2: بيانات GEPS من CMA GRAPES

افتح الملف `GRIB2_CMA_global_ensemble_prediction.ipynb` في دليل `example-notebooks`:

![Jupyter notebook GRIB2 global ensemble prediction](../assets/img/jupyter-grib2-global-ensemble-prediction.png)

اقرأ التعليمات في دفتر الملاحظات وقم بتشغيل الخلايا لفك تشفير البيانات التي تم تنزيلها لتوقع التجميع العالمي. قم بتشغيل كل خلية بالنقر عليها ثم النقر على زر التشغيل في شريط الأدوات أو بالضغط على `Shift+Enter`.

بعد تنفيذ جميع الخلايا، يجب أن ترى تصورًا لإحدى التوقعات الاحتمالية لشذوذ درجة الحرارة الموجود في بيانات GRIB2:

![Global ensemble prediction temperature anomaly](../assets/img/grib2-global-ensemble-prediction-map.png)

!!! question 

    كيف يمكنك تحديث التصور في هذا الدفتر لعرض توقع لـ "سرعة الرياح (الهبات)"؟

??? success "انقر للكشف عن الإجابة"

    لتحديث الدفتر، ابحث عن هذا السطر:

    ```python
    my_parameter_name = "Temperature anomaly"
    ```

    وقم بتغييره إلى:

    ```python
    my_parameter_name = "Wind speed (gust)"
    ```

    ثم أعد تشغيل الخلايا في الدفتر لرؤية الرسم المحدث.

### مثال فك تشفير BUFR: مسارات الأعاصير المدارية

افتح الملف `BUFR_tropical_cyclone_track.ipynb` في دليل `example-notebooks`:

![Jupyter notebook tropical cyclone track](../assets/img/jupyter-tropical-cyclone-track.png)

اقرأ التعليمات في دفتر الملاحظات وقم بتشغيل الخلايا لفك تشفير البيانات التي تم تنزيلها لمسارات الأعاصير المدارية. قم بتشغيل كل خلية بالنقر عليها ثم النقر على زر التشغيل في شريط الأدوات أو بالضغط على `Shift+Enter`.

في النهاية، يجب أن ترى رسمًا يوضح احتمالية الضرب لمسارات الأعاصير المدارية:

![Tropical cyclone tracks](../assets/img/tropical-cyclone-track-map.png)

!!! question 

    تعرض النتيجة الاحتمالية المتوقعة لمسار العاصفة المدارية ضمن 200 كم. كيف يمكنك تحديث الدفتر لعرض الاحتمالية المتوقعة لمسار العاصفة المدارية ضمن 300 كم؟

??? success "انقر للكشف عن الإجابة"

    لتحديث الدفتر لعرض الاحتمالية المتوقعة لمسار العاصفة المدارية ضمن مسافة مختلفة، يمكنك تحديث المتغير `distance_threshold` في الكتلة البرمجية التي تحسب احتمالية الضرب.

    لعرض الاحتمالية المتوقعة لمسار العاصفة المدارية ضمن 300 كم:

    ```python
    # set distance threshold (meters)
    distance_threshold = 300000  # 300 km in meters
    ```

    ثم أعد تشغيل الخلايا في الدفتر لرؤية الرسم المحدث.

!!! note "فك تشفير بيانات BUFR"

    التمرين الذي قمت به للتو قدم مثالًا محددًا لكيفية فك تشفير بيانات BUFR باستخدام مكتبة ecCodes. قد تتطلب أنواع البيانات المختلفة خطوات فك تشفير مختلفة، وقد تحتاج إلى الرجوع إلى الوثائق الخاصة بنوع البيانات الذي تعمل عليه.
    
    لمزيد من المعلومات، يرجى الاطلاع على [وثائق ecCodes](https://confluence.ecmwf.int/display/ECC).

### مثال فك تشفير NetCDF: شذوذ درجات الحرارة الشهرية

افتح الملف `NetCDF4_monthly_temperature_anomaly.ipynb` في دليل `example-notebooks`:

![Jupyter notebook monthly temperature anomalies](../assets/img/jupyter-netcdf4-monthly-temperature-anomalies.png)

اقرأ التعليمات في دفتر الملاحظات وقم بتشغيل الخلايا لفك تشفير البيانات التي تم تنزيلها لشذوذ درجات الحرارة الشهرية. قم بتشغيل كل خلية بالنقر عليها ثم النقر على زر التشغيل في شريط الأدوات أو بالضغط على `Shift+Enter`.

في النهاية، يجب أن ترى خريطة لشذوذ درجات الحرارة:

![Monthly temperature anomalies](../assets/img/netcdf4-monthly-temperature-anomalies-map.png)

!!! note "فك تشفير بيانات NetCDF"

    NetCDF هو تنسيق مرن، وفي هذا المثال تم الإبلاغ عن القيم للمتغير 'anomaly' على طول الأبعاد 'lat' و'lon'. يمكن أن تستخدم مجموعات بيانات NetCDF المختلفة أسماء متغيرات وأبعاد مختلفة.

## استخدام أدوات أخرى لعرض وفك تشفير التنسيقات الثنائية لـ WMO

أوضحت دفاتر الملاحظات التوضيحية كيفية فك تشفير التنسيقات الثنائية الشائعة لـ WMO باستخدام Python.

يمكنك أيضًا استخدام أدوات أخرى لفك تشفير وعرض تنسيقات WMO table driven code form دون الحاجة إلى كتابة برامج، مثل:

- [Panoply](https://www.giss.nasa.gov/tools/panoply/) - تطبيق متعدد المنصات يعرض المصفوفات الجغرافية وغيرها من NetCDF وHDF وGRIB ومجموعات بيانات أخرى
- [ECMWF Metview](https://confluence.ecmwf.int/display/METV/Metview) - تطبيق أرصاد جوية لتحليل البيانات وعرضها، يدعم تنسيقات GRIB وBUFR
- [Integrated Data Viewer (IDV)](https://www.unidata.ucar.edu/software/idv/) - إطار عمل مجاني قائم على Java لتحليل وعرض بيانات علوم الأرض، بما في ذلك دعم تنسيقات GRIB وNetCDF

## الخاتمة

!!! success "تهانينا!"

    في هذه الجلسة العملية، تعلمت كيفية:

    - تشغيل حاوية Docker باستخدام صورة "demo-decode-eccodes-jupyter"
    - تشغيل دفاتر Jupyter التوضيحية لفك تشفير البيانات بتنسيقات GRIB2 وNetCDF وBUFR
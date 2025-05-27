---
title: إضافة رؤوس GTS إلى إشعارات WIS2
---

# إضافة رؤوس GTS إلى إشعارات WIS2

!!! abstract "نتائج التعلم"

    بنهاية هذه الجلسة العملية، ستكون قادرًا على:
    
    - تكوين تعيين بين اسم الملف ورؤوس GTS
    - إدخال البيانات بأسماء ملفات تتطابق مع رؤوس GTS
    - عرض رؤوس GTS في إشعارات WIS2

## مقدمة

الأعضاء في المنظمة العالمية للأرصاد الجوية الراغبين في إيقاف نقل بياناتهم على GTS خلال مرحلة الانتقال إلى WIS2 سيحتاجون إلى إضافة رؤوس GTS إلى إشعاراتهم WIS2. تمكن هذه الرؤوس بوابة WIS2 إلى GTS من توجيه البيانات إلى شبكة GTS.

هذا يسمح للأعضاء الذين انتقلوا إلى استخدام عقدة WIS2 لنشر البيانات بتعطيل نظام MSS الخاص بهم وضمان توفر بياناتهم للأعضاء الذين لم ينتقلوا بعد إلى WIS2.

يجب إضافة خاصية GTS في رسالة إشعار WIS2 كخاصية إضافية إلى رسالة إشعار WIS2. خاصية GTS هي كائن JSON يحتوي على رؤوس GTS المطلوبة لتوجيه البيانات إلى شبكة GTS.

```json
{
  "gts": {
    "ttaaii": "FTAE31",
    "cccc": "VTBB"
  }
}
```

ضمن wis2box يمكنك إضافة هذا إلى إشعارات WIS2 تلقائيًا عن طريق توفير ملف إضافي يسمى `gts_headers_mapping.csv` يحتوي على المعلومات المطلوبة لتعيين رؤوس GTS إلى أسماء الملفات الواردة.

يجب وضع هذا الملف في الدليل المحدد بواسطة `WIS2BOX_HOST_DATADIR` في ملف `wis2box.env` الخاص بك ويجب أن يحتوي على الأعمدة التالية:

- `string_in_filepath`: سلسلة تكون جزءًا من اسم الملف الذي سيتم استخدامه لمطابقة رؤوس GTS
- `TTAAii`: رأس TTAAii الذي سيتم إضافته إلى إشعار WIS2
- `CCCC`: رأس CCCC الذي سيتم إضافته إلى إشعار WIS2

## التحضير

تأكد من أن لديك وصول SSH إلى VM الطالب الخاص بك وأن نسخة wis2box الخاصة بك قيد التشغيل.

تأكد من أنك متصل بوسيط MQTT الخاص بنسخة wis2box باستخدام MQTT Explorer. يمكنك استخدام بيانات الاعتماد العامة `everyone/everyone` للاتصال بالوسيط.

تأكد من أن لديك متصفح ويب مفتوحًا مع لوحة تحكم Grafana لنسختك بالانتقال إلى `http://YOUR-HOST:3000`

## إنشاء `gts_headers_mapping.csv`

لإضافة رؤوس GTS إلى إشعارات WIS2 الخاصة بك، مطلوب ملف CSV يعين رؤوس GTS إلى أسماء الملفات الواردة.

يجب تسمية الملف (بالضبط) `gts_headers_mapping.csv` ويجب وضعه في الدليل المحدد بواسطة `WIS2BOX_HOST_DATADIR` في ملف `wis2box.env` الخاص بك.

## توفير ملف `gts_headers_mapping.csv`

انسخ الملف `exercise-materials/gts-headers-exercises/gts_headers_mapping.csv` إلى نسخة wis2box الخاصة بك وضعه في الدليل المحدد بواسطة `WIS2BOX_HOST_DATADIR` في ملف `wis2box.env` الخاص بك.

```bash
cp ~/exercise-materials/gts-headers-exercises/gts_headers_mapping.csv ~/wis2box-data
```

ثم أعد تشغيل حاوية wis2box-management لتطبيق التغييرات:

```bash
docker restart wis2box-management
```

## إدخال البيانات مع رؤوس GTS

انسخ الملف `exercise-materials/gts-headers-exercises/A_SMRO01YRBK171200_C_EDZW_20240717120502.txt` إلى الدليل المحدد بواسطة `WIS2BOX_HOST_DATADIR` في ملف `wis2box.env` الخاص بك:

```bash
cp ~/exercise-materials/gts-headers-exercises/A_SMRO01YRBK171200_C_EDZW_20240717120502.txt ~/wis2box-data
```

ثم قم بتسجيل الدخول إلى حاوية **wis2box-management**:

```bash
cd ~/wis2box
python3 wis2box-ctl.py login
```

من سطر أوامر wis2box يمكننا إدخال ملف البيانات النموذجي `A_SMRO01YRBK171200_C_EDZW_20240717120502.txt` في مجموعة بيانات محددة كما يلي:

```bash
wis2box data ingest -p /data/wis2box/A_SMRO01YRBK171200_C_EDZW_20240717120502.txt --metadata-id urn:wmo:md:not-my-centre:core.surface-based-observations.synop
```

تأكد من استبدال خيار `metadata-id` بالمعرف الصحيح لمجموعة البيانات الخاصة بك.

تحقق من لوحة تحكم Grafana لمعرفة ما إذا تم إدخال البيانات بشكل صحيح. إذا رأيت أي تحذيرات أو أخطاء، حاول إصلاحها وكرر تمرين الأمر `wis2box data ingest`.

## عرض رؤوس GTS في إشعار WIS2

انتقل إلى MQTT Explorer وتحقق من رسالة إشعار WIS2 للبيانات التي أدخلتها للتو.

يجب أن تحتوي رسالة إشعار WIS2 على رؤوس GTS التي قدمتها في ملف `gts_headers_mapping.csv`.

## خاتمة

!!! success "تهانينا!"
    في هذه الجلسة العملية، تعلمت كيفية:
      - إضافة رؤوس GTS إلى إشعارات WIS2 الخاصة بك
      - التحقق من توفر رؤوس GTS عبر تثبيت wis2box الخاص بك
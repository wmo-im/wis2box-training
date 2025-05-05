---
title: إضافة ترويسات GTS إلى إشعارات WIS2
---

# إضافة ترويسات GTS إلى إشعارات WIS2

!!! abstract "نتائج التعلم"

    بنهاية هذه الجلسة العملية، ستكون قادراً على:
    
    - تكوين تخطيط بين اسم الملف وترويسات GTS
    - إدخال البيانات باسم ملف يتطابق مع ترويسات GTS
    - عرض ترويسات GTS في إشعارات WIS2

## مقدمة

سيحتاج أعضاء المنظمة العالمية للأرصاد الجوية الراغبين في إيقاف نقل بياناتهم على GTS خلال مرحلة الانتقال إلى WIS2 إلى إضافة ترويسات GTS إلى إشعارات WIS2 الخاصة بهم. تمكن هذه الترويسات بوابة WIS2 إلى GTS من إعادة توجيه البيانات إلى شبكة GTS.

هذا يسمح للأعضاء الذين انتقلوا إلى استخدام عقدة WIS2 لنشر البيانات بتعطيل نظام MSS الخاص بهم وضمان أن بياناتهم لا تزال متاحة للأعضاء الذين لم ينتقلوا بعد إلى WIS2.

يجب إضافة خاصية GTS في رسالة إشعار WIS2 كخاصية إضافية لرسالة إشعار WIS2. خاصية GTS هي كائن JSON يحتوي على ترويسات GTS المطلوبة لإعادة توجيه البيانات إلى شبكة GTS.

```json
{
  "gts": {
    "ttaaii": "FTAE31",
    "cccc": "VTBB"
  }
}
```

داخل wis2box يمكنك إضافة هذا إلى إشعارات WIS2 تلقائياً عن طريق توفير ملف إضافي يسمى `gts_headers_mapping.csv` يحتوي على المعلومات المطلوبة لتخطيط ترويسات GTS إلى أسماء الملفات الواردة.

يجب وضع هذا الملف في الدليل المحدد بواسطة `WIS2BOX_HOST_DATADIR` في ملف `wis2box.env` الخاص بك ويجب أن يحتوي على الأعمدة التالية:

- `string_in_filepath`: سلسلة تشكل جزءاً من اسم الملف سيتم استخدامها لمطابقة ترويسات GTS
- `TTAAii`: ترويسة TTAAii التي سيتم إضافتها إلى إشعار WIS2
- `CCCC`: ترويسة CCCC التي سيتم إضافتها إلى إشعار WIS2

## التحضير

تأكد من أن لديك وصول SSH إلى VM الخاص بك وأن نسخة wis2box الخاصة بك تعمل.

تأكد من أنك متصل بوسيط MQTT الخاص بنسخة wis2box باستخدام MQTT Explorer. يمكنك استخدام بيانات الاعتماد العامة `everyone/everyone` للاتصال بالوسيط.

تأكد من أن لديك متصفح ويب مفتوح مع لوحة معلومات Grafana لنسختك عن طريق الذهاب إلى `http://YOUR-HOST:3000`

## إنشاء `gts_headers_mapping.csv`

لإضافة ترويسات GTS إلى إشعارات WIS2 الخاصة بك، مطلوب ملف CSV يخطط ترويسات GTS إلى أسماء الملفات الواردة.

يجب تسمية ملف CSV (بالضبط) `gts_headers_mapping.csv` ويجب وضعه في الدليل المحدد بواسطة `WIS2BOX_HOST_DATADIR` في ملف `wis2box.env` الخاص بك.

## توفير ملف `gts_headers_mapping.csv`
    
انسخ الملف `exercise-materials/gts-headers-exercises/gts_headers_mapping.csv` إلى نسخة wis2box الخاصة بك وضعه في الدليل المحدد بواسطة `WIS2BOX_HOST_DATADIR` في ملف `wis2box.env` الخاص بك.

```bash
cp ~/exercise-materials/gts-headers-exercises/gts_headers_mapping.csv ~/wis2box-data
```

ثم أعد تشغيل حاوية wis2box-management لتطبيق التغييرات:

```bash
docker restart wis2box-management
```

## إدخال البيانات مع ترويسات GTS

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

تحقق من لوحة معلومات Grafana لمعرفة ما إذا تم إدخال البيانات بشكل صحيح. إذا رأيت أي تحذيرات أو أخطاء، حاول إصلاحها وكرر التمرين باستخدام أمر `wis2box data ingest`.

## عرض ترويسات GTS في إشعار WIS2

انتقل إلى MQTT Explorer وتحقق من رسالة إشعار WIS2 للبيانات التي قمت بإدخالها للتو.

يجب أن تحتوي رسالة إشعار WIS2 على ترويسات GTS التي قدمتها في ملف `gts_headers_mapping.csv`.

## الخاتمة

!!! success "تهانينا!"
    في هذه الجلسة العملية، تعلمت كيفية:
      - إضافة ترويسات GTS إلى إشعارات WIS2 الخاصة بك
      - التحقق من أن ترويسات GTS متاحة عبر تثبيت wis2box الخاص بك
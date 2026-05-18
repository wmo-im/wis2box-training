---
title: قالب CLIMAT
---

# قالب csv2bufr لبيانات المناخ اليومية (CLIMAT)

تُبلغ رسائل **CLIMAT** عن ملخصات المناخ الشهرية التي يتم تجميعها من الملاحظات اليومية في المحطات السطحية والمناخية، لدعم مراقبة المناخ، البحث، والأرشفة.

يوفر قالب CLIMAT تنسيق CSV موحد لإنتاج رسائل CLIMAT مشفرة بصيغة BUFR للتسلسل 301150,307073.

## أعمدة CSV والوصف

{{ read_csv("docs/assets/tables/climat-table.csv") }}

## مثال

ملف CSV مثال يتوافق مع قالب CLIMAT: [climat-example.csv](../../sample-data/climat-example.csv).
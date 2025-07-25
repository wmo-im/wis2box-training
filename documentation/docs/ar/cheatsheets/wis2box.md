---
title: دليل مختصر لـ WIS2 in a box
---

# دليل مختصر لـ WIS2 in a box

## نظرة عامة

يعمل `wis2box` كمجموعة من أوامر Docker Compose. يُعتبر الأمر ``wis2box-ctl.py`` أداة 
(مكتوبة بلغة Python) لتسهيل تشغيل أوامر Docker Compose.

## الأساسيات لأوامر wis2box

### بدء التشغيل والإيقاف

* بدء تشغيل wis2box:

```bash
python3 wis2box-ctl.py start
```

* إيقاف wis2box:

```bash
python3 wis2box-ctl.py stop
```

* التحقق من أن جميع حاويات wis2box تعمل:

```bash
python3 wis2box-ctl.py status
```

* تسجيل الدخول إلى حاوية wis2box (*wis2box-management* بشكل افتراضي):

```bash
python3 wis2box-ctl.py login
```

* تسجيل الدخول إلى حاوية wis2box محددة:

```bash
python3 wis2box-ctl.py login wis2box-api
```
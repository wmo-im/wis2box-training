---
title: ورقة الغش لـ WIS2 في صندوق
---

# ورقة الغش لـ WIS2 في صندوق

## نظرة عامة

يعمل wis2box كمجموعة من أوامر Docker Compose. أمر ``wis2box-ctl.py`` هو أداة
(مكتوبة بلغة Python) لتشغيل أوامر Docker Compose بسهولة.

## أساسيات أوامر wis2box

### بدء وإيقاف

* بدء تشغيل wis2box:

```bash
python3 wis2box-ctl.py start
```

* إيقاف تشغيل wis2box:

```bash
python3 wis2box-ctl.py stop
```

* التحقق من تشغيل جميع حاويات wis2box:

```bash
python3 wis2box-ctl.py status
```

* تسجيل الدخول إلى حاوية wis2box (الافتراضية هي *wis2box-management*):

```bash
python3 wis2box-ctl.py login
```

* تسجيل الدخول إلى حاوية wis2box محددة:

```bash
python3 wis2box-ctl.py login wis2box-api
```
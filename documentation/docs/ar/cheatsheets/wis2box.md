---
title: ورقة غش WIS2 في صندوق
---

# ورقة غش WIS2 في صندوق

## نظرة عامة

يعمل wis2box كمجموعة من أوامر Docker Compose. الأمر ``wis2box-ctl.py`` هو أداة
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

* تسجيل الدخول إلى حاوية wis2box (الافتراضي هو *wis2box-management*):

```bash
python3 wis2box-ctl.py login
```

* تسجيل الدخول إلى حاوية wis2box محددة:

```bash
python3 wis2box-ctl.py login wis2box-api
```
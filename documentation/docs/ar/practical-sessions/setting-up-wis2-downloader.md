---
title: إعداد WIS2 Downloader على جهاز الطالب الافتراضي
---

# إعداد WIS2 Downloader على جهاز الطالب الافتراضي

!!! abstract "نتائج التعلم!"

    بنهاية هذه الجلسة العملية، ستكون قادرًا على:

    - إعداد نسخة خاصة بك من "WIS2 Downloader" وإدارة التكوينات المطلوبة
    - التنقل عبر النسخة وإعداد الاشتراكات

## المقدمة

في هذه الجلسة، ستتعلم كيفية إعداد نسخة من WIS2 Downloader على جهاز الطالب الافتراضي المقدم وكيفية التنقل عبر خدماته المختلفة.

!!! note "حول WIS2 Downloader"
     
     يتوفر WIS2 Downloader كمشروع مستقل باستخدام Docker Compose، ويوصى بتشغيله على خادم منفصل عن wis2box لتجنب تداخل التنزيلات مع نشر الرسائل.

     إذا كنت ترغب في تطوير خدمة خاصة بك للاشتراك في إشعارات WIS2 وتنزيل البيانات، يمكنك استخدام [كود المصدر لـ WIS2 Downloader](https://github.com/World-Meteorological-Organization/wis2downloader) كمرجع.

## التحضير والمتطلبات

!!! note "إذا لم يكن أثناء التدريب"

    الخطوات التالية تُطبق فقط إذا كانت المنافذ المذكورة غير متاحة افتراضيًا على الخادم. في أي تكوين، هذه هي المنافذ الوحيدة التي تحتاج إلى الوصول إليها لاستخدام إمكانيات WIS2 Downloader الكاملة.

قبل البدء، يرجى تسجيل الدخول إلى جهاز الطالب الافتراضي الخاص بك مع التأكد من إنشاء نفق عبر SSH للمنافذ التالية:

- `5002 (API)`
- `8080 (UI)`
- `3000 (Grafana)`

للقيام بذلك، يمكنك تغيير إعدادات الاتصال في برنامج Putty:

![إعدادات نفق Putty](../assets/img/putty-tunnel-settings.png)

ثم إضافة تعيين المنافذ الثلاثة إلى المنافذ على جهاز الكمبيوتر الخاص بك (localhost):

![إضافة أنفاق في Putty](../assets/img/putty-add-tunnel.png)

## تثبيت WIS2 Downloader

قم بتنزيل أحدث إصدار من GitHub واستخراجه على جهاز الطالب الافتراضي الخاص بك:

```bash
wget https://github.com/World-Meteorological-Organization/wis2downloader/releases/latest/download/wis2downloader-latest.tar.gz
tar -xzf wis2downloader-latest.tar.gz
cd wis2downloader-*
```

قم بتشغيل سكربت الإعداد لإنشاء ملف التكوين الخاص بك:

```bash
bash setup.sh
```

يتم إنشاء ملف `.env` من الإعدادات الافتراضية وتوليد قيم عشوائية لـ `FLASK_SECRET_KEY` و `REDIS_PASSWORD`. يمكنك مراجعة الملف باستخدام `cat .env` — الإعدادات الافتراضية مناسبة لنشر على جهاز واحد.

قم بتثبيت إضافة Docker الخاصة بـ Loki المستخدمة لنقل السجلات:

```bash
ARCH=$(uname -m | sed 's/x86_64/amd64/;s/aarch64/arm64/')
docker plugin install grafana/loki-docker-driver:3.6.7-${ARCH} --alias loki --grant-all-permissions
```

تحقق من تمكين الإضافة:

```bash
docker plugin ls
```

يجب أن ترى `loki:latest` مدرجًا مع `ENABLED` مضبوطًا على `true`.

قم بإنشاء مجموعة مخصصة باسم `wis2`، وأضف المستخدم الخاص بك إليها، وقم بتكوين ملف `.env` ودليل التنزيلات وفقًا لذلك:

```bash
sudo groupadd wis2
sudo usermod -aG wis2 $USER
sed -i "s/^UID=.*/UID=$(id -u)/" .env
sed -i "s/^GID=.*/GID=$(getent group wis2 | cut -d: -f3)/" .env
mkdir -p downloads
sudo chown $(id -un):wis2 downloads
chmod 775 downloads
```

!!! note "إعادة تسجيل الدخول مطلوبة"
    تغيير عضوية المجموعة لا يأخذ تأثيرًا إلا بعد تسجيل الخروج وإعادة تسجيل الدخول إلى جلسة SSH الخاصة بك.

ابدأ تشغيل مجموعة الخدمات الكاملة:

```bash
docker compose up -d
```

انتظر حوالي 30 ثانية حتى يتم اجتياز فحوصات الصحة، ثم تأكد من أن مدير الاشتراكات جاهز:

```bash
curl http://<WIS2DOWNLOADER_BASE_URL>:5002/health
```

!!! note "التحقق من الحاويات قيد التشغيل"
    يمكنك التحقق من بدء تشغيل جميع الحاويات بنجاح باستخدام:
    ```bash
    docker compose ps
    ```
    يجب أن ترى خدمات لمدير الاشتراكات، مشتركي MQTT، واجهة المستخدم، عمال Celery، Redis، Prometheus، Grafana، و Loki.

## الوصول إلى واجهة المستخدم لـ WIS2 Downloader

افتح متصفح ويب وانتقل إلى واجهة المستخدم الخاصة بنسخة WIS2 Downloader الخاصة بك عن طريق الذهاب إلى `http://<WIS2DOWNLOADER_BASE_URL>:8080`.

ستجد نفسك في صفحة الهبوط التي تم تعيينها إلى قسم `Help` افتراضيًا، حيث تعرض الوثائق.

![صفحة الهبوط لـ WIS2 Downloader](../assets/img/wis2-downloader-landing-page.png)

في قائمة الشريط الجانبي الأيسر، ستتمكن من التنقل عبر جميع الأقسام المختلفة لواجهة المستخدم.

الأقسام الرئيسية المتاحة هي:

- **Dashboard** — لوحة معلومات Grafana مضمنة تعرض نشاط التنزيل، حالة الطابور، ومقاييس الخدمة قيد التشغيل. متاحة أيضًا على `http://<WIS2DOWNLOADER_BASE_URL>:3000`.
- **Catalogue View** — تصفح مجموعات بيانات WIS2 المتاحة عن طريق البحث أو التصفية في الكتالوج العالمي. اختر موضوعًا ودليل حفظ، ثم انقر على *Subscribe* لبدء التنزيل.
- **Tree View** — التنقل في تسلسل مواضيع WIS2 كهيكل شجري قابل للطي. مفيد لاستكشاف المواضيع المتاحة قبل الاشتراك.
- **Manual Subscribe** — إنشاء اشتراك عن طريق إدخال موضوع وتفاصيل الوسيط مباشرة، دون الاعتماد على الكتالوجات العالمية. مفيد للاشتراك في مواضيع من WIS2 Nodes محددة أو وسطاء خاصين.
- **Manage Subscriptions** — عرض وإدارة جميع الاشتراكات النشطة. من هنا يمكنك رؤية المواضيع التي يتم مراقبتها وإزالة أي منها لم تعد بحاجة إليها.
- **Settings** — يسمح حاليًا بإعادة تحميل كتالوج مجموعة البيانات من الكتالوجات العالمية. سيتم توسيع هذا القسم في الإصدارات المستقبلية ليشمل التكوين والإدارة العامة لـ WIS2 Downloader.
- **Help** — صفحة الهبوط الافتراضية، تعرض الوثائق المدمجة لـ WIS2 Downloader.

## إدارة الاشتراكات في واجهة المستخدم

كما في المثال الأخير، ستصل إلى واجهة المستخدم للنسخة قيد التشغيل عن طريق الذهاب إلى `http://<WIS2DOWNLOADER_BASE_URL>:8080`.

من هناك، هناك 3 طرق لإعداد اشتراك:

- في **Catalogue View** عن طريق تصفح المواضيع المتاحة بطريقة مشابهة لبوابات GDC.
- في **Tree View** عن طريق اختيار موضوع من كتالوج GDC من خلال استكشاف المواضيع كما في MQTT Explorer.
- في **Manual Subscribe** حيث يمكنك كتابة المواضيع المطلوبة، الفلاتر، والمعلمات الأخرى.

للتمرين التالي، سنشترك في الإشعارات القادمة من GTS إلى بوابة WIS2 التي تديرها DWD:

- أولاً، انتقل إلى **Manual Subscribe**.
- اكتب المواضيع كـ `cache/a/wis2/de-dwd-gts-to-wis2/data/core/#`
- قم بتعيين مجلد الوجهة كـ `gts-data`

النتيجة النهائية يجب أن تكون مشابهة لـ:
![WIS2 Downloader Manual Subscribe](../assets/img/wis2-downloader-manual-subscribe.png)

بعد ذلك، انتقل إلى مجلد التنزيل على جهاز الطالب الافتراضي الخاص بك باستخدام الأوامر:

```bash
ls -R wisdownloader/downloads
```

والآن يجب أن ترى سلسلة من الملفات التي تم تنزيلها بواسطة النسخة الخاصة بك.

كخطوة نهائية، يمكننا حذف الاشتراك عن طريق الذهاب إلى عرض **Manage Subscriptions** والضغط على زر **Unsubscribe**.

![WIS2 Downloader Delete Subscription](../assets/img/wis2-downloader-delete-subscription.png)

!!! note "حذف الملفات التي تم تنزيلها"

    يُوصى بتنظيف مجلد التنزيلات بعد إكمال التمرين لتحرير مساحة على جهاز الطالب الافتراضي. لذلك قم بتشغيل الأمر التالي لحذف ملفات التمارين السابقة.

    ```bash
    rm -fr wisdownloader/downloads/gts-data
    ```

## مراجعة تكوين WIS2 Downloader

يمكن تكوين نسخة WIS2 Downloader باستخدام متغيرات البيئة المحددة في ملف `.env`.

يمكنك الاطلاع على تفصيل لمتغيرات البيئة في [دليل إدارة WIS2 Downloader القسم 2.1](https://world-meteorological-organization.github.io/wis2downloader/en/admin-guide.html)

لمراجعة التكوين الحالي لـ WIS2 Downloader، يمكنك استخدام الأمر التالي:

```bash
cat .env
```

!!! question "مراجعة تكوين WIS2 Downloader"

    ما هي فترة الاحتفاظ الافتراضية للبيانات التي تم تنزيلها؟

    أي منفذ يستمع إليه API مدير الاشتراكات؟

??? success "انقر للكشف عن الإجابة"

    فترة الاحتفاظ الافتراضية للبيانات التي تم تنزيلها هي `30` يومًا، كما هو محدد بواسطة `DOWNLOAD_RETENTION_PERIOD`.

    يستمع API مدير الاشتراكات على المنفذ `5002`، كما هو محدد في `WIS2DOWNLOADER_SUBSCRIPTION_MANAGER_URL`.

!!! note "تحديث تكوين WIS2 Downloader"

    لتحديث التكوين، قم بتحرير ملف `.env` وأعد تشغيل المجموعة لتطبيق التغييرات:

    ```bash
    docker compose up -d
    ```

يمكنك الاحتفاظ بالتكوين الافتراضي للتمارين القادمة.

## واجهة برمجة التطبيقات لـ WIS2 Downloader

يتيح WIS2 Downloader واجهة REST API على `<WIS2DOWNLOADER_BASE_URL>:5002/api`. تأكد من أن الخدمة جاهزة:

```bash
curl <WIS2DOWNLOADER_BASE_URL>:5002/api/health
```

يجب أن ترى:

```json
{"status": "healthy"}
```

لإنشاء اشتراك، أرسل طلب `POST` مع موضوع MQTT وخيار `target` الفرعي حيث سيتم حفظ الملفات:

```bash
curl -s -X POST <WIS2DOWNLOADER_BASE_URL>:5002/api/subscriptions \
  -H "Content-Type: application/json" \
  -d '{"topic": "cache/a/wis2/+/data/core/weather/surface-based-observations/#", "target": "surface-obs"}'
```

يتضمن الرد UUID المخصص للاشتراك الجديد. استخدمه لحذف الاشتراك عند عدم الحاجة إليه:

```bash
curl -X DELETE <WIS2DOWNLOADER_BASE_URL>:5002/api/subscriptions/{id}
```

للحصول على القائمة الكاملة لنقاط النهاية المتاحة (القائمة، الحصول، تحديث الاشتراكات والمزيد)، راجع الوثائق التفاعلية لـ Swagger المتاحة على `<WIS2DOWNLOADER_BASE_URL>:5002/api/openapi`.

## الخاتمة

!!! success "تهانينا!"

    في هذه الجلسة العملية، تعلمت كيفية:

    - تثبيت WIS2 Downloader على نظامك المحلي وتغيير التكوينات الافتراضية
    - التفاعل مع واجهة المستخدم لإنشاء وإزالة الاشتراكات
    - إدارة الاشتراكات باستخدام واجهة برمجة التطبيقات
    - عرض البيانات التي تم تنزيلها على نظامك المحلي
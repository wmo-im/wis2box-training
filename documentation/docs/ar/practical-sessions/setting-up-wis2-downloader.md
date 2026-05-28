---
title: إعداد WIS2 Downloader على جهاز الطالب الافتراضي الخاص بك
---

# إعداد WIS2 Downloader على جهاز الطالب الافتراضي الخاص بك

!!! abstract "نتائج التعلم!"

    بنهاية هذه الجلسة العملية، ستكون قادرًا على:

    - إعداد نسخة خاصة بك من "WIS2 Downloader" وإدارة التكوينات المطلوبة
    - التنقل عبر النسخة للاستفادة من قدراتها المختلفة

## المقدمة

في هذه الجلسة، ستتعلم كيفية إعداد نسخة من WIS2 Downloader على جهاز الطالب الافتراضي المقدم وكيفية التنقل عبر خدماته المختلفة.

!!! note "حول WIS2 Downloader"
     
     يتوفر WIS2 Downloader كمشروع مستقل باستخدام Docker Compose، ويوصى بتشغيله على خادم منفصل عن wis2box لتجنب تداخل التنزيلات مع نشر الرسائل.

     إذا كنت ترغب في تطوير خدمتك الخاصة للاشتراك في إشعارات WIS2 وتنزيل البيانات، يمكنك استخدام [الشفرة المصدرية لـ WIS2 Downloader](https://github.com/World-Meteorological-Organization/wis2downloader) كمرجع.

## التحضير والمتطلبات

!!! note "إذا لم يكن أثناء التدريب"

    الخطوات التالية يتم تطبيقها فقط إذا كانت المنافذ المذكورة غير متوفرة افتراضيًا على الخادم. في أي تكوين، هذه هي المنافذ الوحيدة التي يجب الوصول إليها لاستخدام القدرات الكاملة لمجموعة WIS2 Downloader.

قبل البدء، يرجى تسجيل الدخول إلى جهاز الطالب الافتراضي الخاص بك مع التأكد من إنشاء نفق عبر SSH للمنافذ التالية:

- `5002 (API)`
- `8080 (UI)`
- `3000 (Grafana)`

للقيام بذلك، يمكنك تغيير إعدادات الاتصال في Putty:

![access putty tunnel settings](../assets/img/putty-tunnel-settings.png)

ثم أضف تعيين المنافذ الثلاثة إلى المنافذ على جهاز الكمبيوتر الخاص بك (localhost):

![adding tunnels in putty](../assets/img/putty-add-tunnel.png)

## تثبيت WIS2 Downloader

قم بتنزيل أحدث إصدار من GitHub واستخرجه على جهاز الطالب الافتراضي الخاص بك:

```bash
wget https://github.com/World-Meteorological-Organization/wis2downloader/releases/latest/download/wis2downloader-latest.tar.gz
tar -xzf wis2downloader-latest.tar.gz
cd wis2downloader-*
```

قم بتشغيل سكربت الإعداد لإنشاء ملف التكوين الخاص بك:

```bash
bash setup.sh
```

سيتم إنشاء ملف `.env` باستخدام القيم الافتراضية وتوليد قيم عشوائية لـ `FLASK_SECRET_KEY` و `REDIS_PASSWORD`. يمكنك مراجعة الملف باستخدام `cat .env` — القيم الافتراضية مناسبة للنشر على جهاز واحد.

قم بتثبيت إضافة Docker الخاصة بـ Loki المستخدمة لنقل السجلات:

```bash
ARCH=$(uname -m | sed 's/x86_64/amd64/;s/aarch64/arm64/')
docker plugin install grafana/loki-docker-driver:3.6.7-${ARCH} --alias loki --grant-all-permissions
```

تحقق من تمكين الإضافة:

```bash
docker plugin ls
```

يجب أن ترى `loki:latest` مدرجًا مع تعيين `ENABLED` إلى `true`.

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
    لن يتم تطبيق تغيير عضوية المجموعة إلا بعد تسجيل الخروج وإعادة تسجيل الدخول إلى جلسة SSH.

ابدأ تشغيل مجموعة الخدمات الكاملة:

```bash
docker compose up -d
```

انتظر حوالي 30 ثانية حتى تمر فحوصات الصحة، ثم تأكد من أن مدير الاشتراكات جاهز:

```bash
curl http://localhost:5002/health
```

!!! note "التحقق من الحاويات قيد التشغيل"
    يمكنك التحقق من أن جميع الحاويات بدأت بنجاح باستخدام:
    ```bash
    docker compose ps
    ```
    يجب أن ترى خدمات لمدير الاشتراكات، مشتركي MQTT، واجهة المستخدم، عمال Celery، Redis، Prometheus، Grafana، وLoki.

### الوصول إلى واجهة WIS2 Downloader

افتح متصفح ويب وانتقل إلى واجهة المستخدم الخاصة بنسخة WIS2 Downloader الخاصة بك عن طريق الذهاب إلى `http://localhost:8080`.

ستجد نفسك في صفحة البداية التي يتم تعيينها افتراضيًا إلى قسم `Help` الذي يعرض الوثائق.

![WIS2 Downloader Landing Page](../assets/img/wis2-downloader-landing-page.png)

في قائمة الشريط الجانبي الأيسر، ستتمكن من التنقل عبر جميع الأقسام المختلفة لواجهة المستخدم.

الأقسام الرئيسية المتاحة هي:

- **Dashboard** — لوحة معلومات Grafana مدمجة تعرض نشاط التنزيل، حالة الطابور، ومقاييس الخدمة قيد التشغيل. متوفرة أيضًا على `http://localhost:3000`.
- **Catalogue View** — تصفح مجموعات بيانات WIS2 المتاحة عن طريق البحث أو التصفية في الكتالوج العالمي. اختر موضوعًا ودليل حفظ، ثم انقر على *Subscribe* لبدء التنزيل.
- **Tree View** — التنقل في تسلسل مواضيع WIS2 كهيكل شجري قابل للطي. مفيد لاستكشاف المواضيع المتاحة قبل الاشتراك.
- **Manual Subscription** — إنشاء اشتراك عن طريق إدخال موضوع وتفاصيل الوسيط مباشرة، دون الاعتماد على الكتالوجات العالمية. مفيد للاشتراك في مواضيع من WIS2 Nodes محددة أو وسطاء خاصين.
- **Subscriptions** — عرض وإدارة جميع الاشتراكات النشطة. من هنا يمكنك رؤية المواضيع التي يتم مراقبتها وإزالة أي منها لم تعد بحاجة إليها.
- **Settings** — يسمح حاليًا بإعادة تحميل كتالوج البيانات من الكتالوجات العالمية. سيتم توسيع هذا القسم في الإصدارات المستقبلية لتغطية التكوين والإدارة العامة لـ WIS2 Downloader.
- **Help** — صفحة البداية الافتراضية، تعرض الوثائق المدمجة لـ WIS2 Downloader.

### مراجعة تكوين WIS2 Downloader

يمكن تكوين نسخة WIS2 Downloader باستخدام متغيرات البيئة المحددة في ملف `.env`.

يمكنك مراجعة تحليل متغيرات البيئة في [دليل إدارة WIS2 Downloader القسم 2.1](https://world-meteorological-organization.github.io/wis2downloader/en/admin-guide.html)

لمراجعة التكوين الحالي لـ WIS2 Downloader، يمكنك استخدام الأمر التالي:

```bash
cat .env
```

!!! question "مراجعة تكوين WIS2 Downloader"

    ما هي فترة الاحتفاظ الافتراضية للبيانات التي تم تنزيلها؟

    ما هو المنفذ الذي يستمع إليه API الخاص بمدير الاشتراكات؟

??? success "انقر للكشف عن الإجابة"

    فترة الاحتفاظ الافتراضية للبيانات التي تم تنزيلها هي `30` يومًا، كما هو محدد بواسطة `DOWNLOAD_RETENTION_PERIOD`.

    يستمع API الخاص بمدير الاشتراكات على المنفذ `5002`، كما هو محدد في `WIS2DOWNLOADER_SUBSCRIPTION_MANAGER_URL`.

!!! note "تحديث تكوين WIS2 Downloader"

    لتحديث التكوين، قم بتحرير ملف `.env` وأعد تشغيل المجموعة لتطبيق التغييرات:

    ```bash
    docker compose up -d
    ```

يمكنك الاحتفاظ بالتكوين الافتراضي للتمارين التالية.

### واجهة برمجة التطبيقات (API) لـ WIS2 Downloader

يقدم WIS2 Downloader واجهة REST API عند `<WIS2DOWNLOADER_BASE_URL>:5002/api`. تأكد من أن الخدمة جاهزة:

```bash
curl <WIS2DOWNLOADER_BASE_URL>:5002/api/health
```

يجب أن ترى:

```json
{"status": "healthy"}
```

لإنشاء اشتراك، أرسل طلب `POST` مع `topic` الخاص بـ MQTT ودليل فرعي اختياري `target` حيث سيتم حفظ الملفات:

```bash
curl -s -X POST <WIS2DOWNLOADER_BASE_URL>:5002/api/subscriptions \
  -H "Content-Type: application/json" \
  -d '{"topic": "cache/a/wis2/+/data/core/weather/surface-based-observations/#", "target": "surface-obs"}'
```

يتضمن الرد UUID المخصص للاشتراك الجديد. استخدمه لحذف الاشتراك عند عدم الحاجة إليه:

```bash
curl -X DELETE <WIS2DOWNLOADER_BASE_URL>:5002/api/subscriptions/{id}
```

للحصول على القائمة الكاملة لنقاط النهاية المتاحة (قائمة، الحصول على، تحديث الاشتراكات والمزيد)، راجع وثائق Swagger التفاعلية المتوفرة عند `<WIS2DOWNLOADER_BASE_URL>:5002/api/openapi`.

## الخاتمة

!!! success "تهانينا!"

    في هذه الجلسة العملية، تعلمت كيفية:

    - تثبيت WIS2 Downloader على نظامك المحلي وتغيير التكوينات الافتراضية
    - التفاعل مع واجهة المستخدم لإنشاء وإزالة الاشتراكات
    - إدارة الاشتراكات باستخدام API
    - عرض البيانات التي تم تنزيلها على نظامك المحلي
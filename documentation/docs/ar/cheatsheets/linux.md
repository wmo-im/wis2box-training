---
title: دليل Linux المختصر
---

# دليل Linux المختصر

## نظرة عامة

المفاهيم الأساسية للعمل في نظام التشغيل Linux هي **الملفات** و**المجلدات** المنظمة في
هيكل شجري داخل **البيئة**.

بمجرد تسجيل الدخول إلى نظام Linux، تعمل داخل **الواجهة البرمجية** حيث يمكنك التعامل مع الملفات والمجلدات،
من خلال تنفيذ الأوامر المثبتة على النظام. واجهة Bash هي واجهة شائعة ومنتشرة عادةً في أنظمة Linux.

## Bash

### التنقل بين المجلدات

* الدخول إلى مجلد مطلق:

```bash
cd /dir1/dir2
```

* الدخول إلى مجلد نسبي:

```bash
cd ./somedir
```

* الانتقال للمجلد الأعلى:

```bash
cd ..
```

* الانتقال لمجلدين للأعلى:

```bash
cd ../..
```

* الانتقال إلى مجلد "المنزل" الخاص بك:

```bash
cd -
```

### إدارة الملفات

* عرض الملفات في المجلد الحالي:

```bash
ls
```

* عرض الملفات في المجلد الحالي بمزيد من التفاصيل:

```bash
ls -l
```

* عرض جذر نظام الملفات:

```bash
ls -l /
```

* إنشاء ملف فارغ:

```bash
touch foo.txt
```

* إنشاء ملف من أمر `echo`:

```bash
echo "hi there" > test-file.txt
```

* عرض محتويات ملف:

```bash
cat test-file.txt
```

* نسخ ملف:

```bash
cp file1 file2
```

* البدائل: التعامل مع أنماط الملفات:

```bash
ls -l fil*  # يطابق file1 و file2
```

* دمج ملفين في ملف جديد يسمى `newfile`:

```bash
cat file1 file2 > newfile
```

* إضافة ملف آخر إلى `newfile`

```bash
cat file3 >> newfile
```

* حذف ملف:

```bash
rm newfile
```

* حذف جميع الملفات بنفس امتداد الملف:

```bash
rm *.dat
```

* إنشاء مجلد

```bash
mkdir dir1
```

### ربط الأوامر معاً باستخدام الأنابيب

تسمح الأنابيب للمستخدم بإرسال ناتج أمر إلى آخر باستخدام رمز الأنبوب `|`:

```bash
echo "hi" | sed 's/hi/bye/'
```

* تصفية نواتج الأوامر باستخدام grep:

```bash
echo "id,title" > test-file.txt
echo "1,birds" >> test-file.txt
echo "2,fish" >> test-file.txt
echo "3,cats" >> test-file.txt

cat test-file.txt | grep fish
```

* تجاهل حالة الأحرف:

```bash
grep -i FISH test-file.txt
```

* عد الأسطر المطابقة:

```bash
grep -c fish test-file.txt
```

* إرجاع النواتج التي لا تحتوي على الكلمة المفتاحية:

```bash
grep -v birds test-file.txt
```

* عد عدد الأسطر في `test-file.txt`:

```bash
wc -l test-file.txt
```

* عرض الناتج شاشة تلو الأخرى:

```bash
more test-file.txt
```

...مع التحكمات:

- التمرير لأسفل سطراً بسطر: *enter*
- الانتقال إلى الصفحة التالية: *space bar*
- العودة لصفحة واحدة للخلف: *b*

* عرض أول 3 أسطر من الملف:

```bash
head -3 test-file.txt
```

* عرض آخر سطرين من الملف:

```bash
tail -2 test-file.txt
```
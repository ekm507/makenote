[English](./README.md)

# ابزار خط فرمان makenote

یک ابزار خط فرمان برای نوشتن یادداشت‌ها، نوشته‌های روزمره، گزارش‌کار و غیره.

## نصب

### پیش از نصب

پیش از نصب مطمئن باشید نیازمندی‌های برنامه نصب شده‌است.  
این برنامه از sqlite3 استقاده می‌کند. برای نصب آن در سیستم‌های دبیانی از این دستور استفاده کنید:



```bash
apt install sqlite3
```

### نصب

ابتدا این مخزن را کلون کنید:


```bash
git clone 'https://github.com/ekm507/makenote.git'
```

سپس فایل `install.sh` را با دسترسی روت اجرا کنید:

```bash
./install.sh
```

## استفاده

### ایجاد جدول

این ابزار نوشته‌ها را در جدول‌های مختلف نگه‌داری می‌کند. شما می‌توانید نوشته‌های خود را در دسته‌بندی‌هایی مثل journals, tasks, work و غیره نگه‌داری کنید..

برای ایجاد یک جدول دستور خط فرمان زیر را اجرا کنید:



```bash
makenote -create <table_name>
```

### افزودن یک یادداشت

برای اضافه کردن یک یادداشت به یکی از جدول‌ها، دستور زیر را اجرا کنید:

اگر اسم جدول مشخص نشود، جدول پیشفرض با اسم journals استفاده خواهدشد.


```bash
makenote +<table_name> <note_text>
```

هم‌چنین این ابزار می‌تواند فرودی را به جای خط فرمان، از ورودی stdin دریافت کند. برای مثال می‌توانید از این ابزار به این شکل استفاده کنید:


```bash
echo "من این ابزار را نصب کردم" | makenote +journals
```


### دیدن لیست جدول‌ها

برای دیدن یک لیست از اسم جدول‌های ایجادشده، از این دستور استفاده کنید:


```bash
makenote -list
```

### مشاهده یک جدول

برای دیدن یادداشت‌های داخل یکی از جدول‌ها، از این دستور استفاده کنید:


```bash
makenote -show <table_name>
```

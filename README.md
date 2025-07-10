# Django Shop - Celery Worker Supervisor Configuration

رای اجرای خودکار `Celery` در پروژه ‍`Django` بدون نیاز به اجرای دستی در ترمینال

## توضیحات فایل کانفیگ

- `user=elicipher`  
  اجرای سرویس با دسترسی کاربر `elicipher` برای رعایت مجوزها.

- `directory=/home/elicipher/Templates/my_project/Online-shop/`  
  مسیر ریشه پروژه Django که Celery در آن اجرا می‌شود.

- `command=/home/elicipher/Templates/my_project/Online-shop/env/bin/celery -A shop worker -l INFO`  
  دستور اجرای Celery worker برای اپلیکیشن `shop` با سطح گزارش‌گیری INFO.

- `numprocs=1`  
  تنها یک پردازش worker اجرا می‌شود.

- `autostart=true`  
  اجرای خودکار سرویس پس از شروع Supervisor.

- `autorestart=true`  
  راه‌اندازی مجدد خودکار سرویس در صورت توقف یا کرش.

- `stdout_logfile=/var/log/django_shop/celery_out.log`  
  مسیر فایل لاگ خروجی معمول.

- `stderr_logfile=/var/log/djago_shop/celery_err.log`  
  مسیر فایل لاگ خطاها.

این تنظیمات باعث می‌شود Celery worker همیشه فعال بماند و در صورت بروز مشکل به صورت خودکار راه‌اندازی شود.

---

## منابع و تشکر

این تنظیمات ترکیبی از مستندات رسمی Supervisor و راهنمای مدرس محترم است که می‌توانید آن را در لینک زیر مشاهده کنید:  
[supervisor_commands.txt - amirbigg](https://github.com/amirbigg/oneFile-codes/blob/36c3d691cbc08839a4d5eca9ac4abb7471e796f2/supervisor_commands.txt)

---

## نحوه استفاده

1. فایل کانفیگ را در مسیر `/etc/supervisor.d/` قرار دهید.(پسوند فایل کانفیگ باید ini باشد)
2. با استفاده از دستورهای زیر Supervisor را مجدداً بارگذاری و سرویس را استارت کنید:

```bash
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl start django_shop

```

برای مشاهده وضعیت از دستور :

‍‍```bash
sudo supervisorctl status django_shop
```
در صورت عدم پیدا نکردن کانفیگ و برخورد با ارور دستور زیر رو بزنید 

‍‍```bash
sudo supervisorctl -c /etc/supervisord.conf status django_shop
```



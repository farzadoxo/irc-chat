
<h1>چت آی آر سی (FA) <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/f/fd/State_flag_of_Iran_%281964%E2%80%931980%29.svg/330px-State_flag_of_Iran_%281964%E2%80%931980%29.svg.png" width="70px" height="70px"></h1>
یه سیستم ساده چت متنی که کمک میکنه در شرایط عدم دسترسی به پیامرسان های بین المللی ارتباط حفظ بشه.
*این پروژه صرفا یک **irc chat** نیست و فقط نامش از اون الهام گرفته شده.*

## قابلیت ها:
- کاملا رایگان
- ناشناس بودن کاربران
- بدون نیاز به احراز هویت
- حذف پیام ها به صورت خودکا و مدت دار


# نحوه راه اندازی
1. ابتدا پروژه رو با گیت Clone و یا فایل پروژه رو به صورت مسیتقیم دانلود کنید.
2. [داکر](https://www.docker.com/) و [داکر کامپوز](https://docs.docker.com/compose/) رو نصب کنید.
3. به محل فایل های پروژه برید و دستور زیر رو اجرا کنید:
```bash
$ sudo docker compose up
```
4. منتظر بمونید تا ایمیج های داکر و پکیج های پایتونی دانلود بشن 
5. در صورت اجرای موفقیت آمیز با متن زیر مواجه میشید:
```bash
api-1 | INFO:  Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)
```


 # IRC Chat (EN) 🇺🇸
A simple system for chatting and exchanging text messages like the old IRC. This system helps you to easily set up and use it on a server in special situations such as internet outages or when you feel the need for a messaging system under your supervision.
- Completely free
- Easy to set up (Docker)
- Under your supervision
- No interception or permanent storage of information
- Room creating

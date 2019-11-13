## How to use
### 1. Configure environment
``virtualenv -p python3 env
source env/bin/acivate
pip install -r requirements.txt``
### 2. Configure database
just run:
``python models.py``
### 3. Token
add your token in [token variable](https://github.com/alistvt/friendship-quiz-bot/blob/master/consts/token.py)
### 4. Star this repo
## Support
For more support you can contact with [me](t.me/alistvt). It would be a pleasure to help.

## راهنمای کاربران ایرانی
[گروه کاربران ایرانی کتابخانه پایتون-تلگرام-بات](t.me/ptbir)

ساختن لینک | لیست برترین دوستان
لینک من | راهنما

اون اولش ساختن لینک دکمش فعاله . بعد اگه وسط ساختن لینک انصرافو بزنه همه سوالایی که جواب داده پاک میشه.
اگه بیستا سوالشو جواب داد که میره و دیگه آخرش لینکو بهش نشون میده.

بعد دیگه ازین بعد نباید بتونه ساختن لینکو ببینه تو منوی اصلی.

دیگه حالا اگه کسی با لینک یه نفر وارد شد باید همه منوها براش پاک بشه و شروع کنه به جواب دادن بیستا سوالش.
بعد اون اول میاد لیست کسایی که قبلا جواب دادنو میاره حدود 20 نفر. و زیرش یه دکمه شروع میذاره.
اگه وسطش کارشو قطع کرد یا استارت زد دوباره تا همونجا که بوده امتیاز باید براش ثبت بشه
احتمالا از یه دیتابیس منی تو منی باید استفاده بشه.

# اینلاین کیبورها
قسمت تستها کالبکش میشه اون آیدی دیتابیس تست و بعد شماره سوال و سپس شماره گزینه.

بعد هر یه سوالو که جواب میده خود به خود میره بعدی.

# answer <answerskeeper_id> <question_number> <option>
  answerer answers like this

# start <answererkeeper_id>
  sends the first question of questioner

# set <question_number> <main_question_number> <answer>
  sets the answers of the questioner

# skip <question_number> <main_question_number>
  skip question

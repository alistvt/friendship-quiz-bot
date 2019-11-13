## A. How to use
### 1. Configure environment
```
virtualenv -p python3 env
source env/bin/acivate
pip install -r requirements.txt
```
### 2. Configure database
just run:
```
python models.py
```
### 3. Token
add your token in [token variable](https://github.com/alistvt/friendship-quiz-bot/blob/master/consts/token.py)
### 4. Star this repo

## B. Inline Keyboard Grammer
### answer <answerskeeper_id> <question_number> <option>
  answerer answers like this

### start <answererkeeper_id>
  sends the first question of questioner

### set <question_number> <main_question_number> <answer>
  sets the answers of the questioner

### skip <question_number> <main_question_number>
  skip question
  
## C. Support
For more support you can contact with [me](t.me/alistvt). It would be a pleasure to help.
## D. Coding Style
Coding conventions and direcotries and the whole system is tried to be something like django and I have tried to simulate that model here. 
As you can see I have 
`models` file which handles my db parts,
`templates` directory is for the constant parts of the bot, like keyboards and buttons (like django templates dir),
`handlers` directory is the alternative for views in django,
`consts` directory is like settings module in django,
and I have also an `admin.py` file to add features for the admins!
## E. راهنمای کاربران ایرانی
[گروه کاربران ایرانی کتابخانه پایتون-تلگرام-بات](t.me/ptbir)


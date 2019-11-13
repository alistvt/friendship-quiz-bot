# Define your buttons here each as a string variable
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove

start = '/start'
answer_self_questions = '➕ ایجاد کوییز خودم'
sure_to_restart = '💯 بله مطمئنم'
not_sure_to_restart = '❌ نه منصرف شدم'
view_scoreboard = '👁 مشاهده نتایج'
share = '🔗 لینک کوییز من'
support = '📨 پشتیبانی'
about = 'ℹ️ درباره'
help = 'ℹ️ راهنما'
cancel = '✖️ انصراف'
start_test_cmd = 'start'
start_test = 'start {}'
show_question_cmd = 'show'
show_question = 'show {}'
answer_question_cmd = 'answer'
answer_question = 'answer {} {} {}'
set_answer_cmd = 'set'
set_answer = 'set {} {} {}'
skip_question_cmd = 'skip'
skip_question = 'skip {} {}'
end_test_cmd = 'end'
select_question_cmd = 'select'
goto_question_cmd = select_question_cmd

all = [start, answer_self_questions, view_scoreboard, sure_to_restart, not_sure_to_restart, share, about, help,
        show_question_cmd, show_question, answer_question_cmd, answer_question, end_test_cmd,
        select_question_cmd, goto_question_cmd]

admin_num = 'Number'
admin_cancel = '/cancel'
admin_forward_to_all = 'Bulk Forward'
admin_send_to_all = 'Bulk Send'

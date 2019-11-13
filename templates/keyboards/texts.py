# ReplyKeyboardMarkup(cv.RK_MAIN_MENU, resize_keyboard = True)
# ReplyKeyboardRemove
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove
from templates import textbuttons as tb

main_menu = ReplyKeyboardMarkup([[tb.answer_self_questions, tb.view_scoreboard], [tb.share, tb.help]], resize_keyboard=True)
restart_test = ReplyKeyboardMarkup([[tb.sure_to_restart, tb.not_sure_to_restart]], resize_keyboard=True)
support = ReplyKeyboardMarkup([[tb.cancel]])
admin_main = ReplyKeyboardMarkup([[tb.admin_num], [tb.admin_cancel, tb.admin_forward_to_all], [tb.admin_send_to_all]], resize_keyboard=True)

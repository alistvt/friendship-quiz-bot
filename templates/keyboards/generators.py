# this module is for dynamic keyboards which take some args and
# create a keyboard.
from telegram import ReplyKeyboardMarkup, ReplyKeyboardRemove, InlineKeyboardMarkup
from templates import inlinebuttons as ib
from consts import questions


def question_options_questioner(question_number, main_question_number, options):
    footer = [[ib.skip(question_number, main_question_number)]]
    header = [reversed([ib.option_questioner(question_number, main_question_number, i) for i in range(1, options+1)])]
    keyboard = header + footer
    return InlineKeyboardMarkup(keyboard)

def question_options_anwerer(answerskeeper_id, question_number, options):
    keyboard = [reversed([ib.option_answerer(answerskeeper_id, question_number, i) for i in range(1, options+1)])]
    return InlineKeyboardMarkup(keyboard)

def select_question(number_of_questions=questions.num, columns=5):
    keyboard = []
    buttons = [ib.select(i) for i in range(1, number_of_questions+1)]
    keyboard = [buttons[i:i + columns] for i in range(0, len(buttons), columns)]
    keyboard += [[ib.end_test]]
    return InlineKeyboardMarkup(keyboard)

remove_text_keyboard = ReplyKeyboardRemove()

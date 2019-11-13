# Define your constant 'callback_data's here,
# callback_data's text and templates are here but
# their constant parts should be in textbuttons
#
# Examples:
# InlineKeyboardButton('text', callback_data='')
# InlineKeyboardButton('text', url='')

from telegram import InlineKeyboardButton
from . import textbuttons as tb

# current means current question
def skip(question_number, main_question_number):
	return InlineKeyboardButton('رد کردن ◄', callback_data=tb.skip_question.format(question_number, main_question_number))

def show_prev(current):
	return InlineKeyboardButton('«', callback_data=tb.show_question.format(current-1))

def select(current):
	return InlineKeyboardButton('{}'.format(current), callback_data=tb.show_question.format(current))

def option_questioner(question_number, main_question_number, answer):
	# answer is the option number
	return InlineKeyboardButton('◂ {} ▸'.format(answer), callback_data=tb.set_answer.format(question_number, main_question_number, answer))

def option_answerer(answerskeeper_id, question_number, option):
	# answer is the option number
	return InlineKeyboardButton('◂ {} ▸'.format(option), callback_data=tb.answer_question.format(answerskeeper_id, question_number, option))

select_question = InlineKeyboardButton('🔍 Go to Question', callback_data=tb.select_question_cmd)

def start_test(answerskeeper_id):
	return InlineKeyboardButton('☑️ شروع کوییز', callback_data=tb.start_test.format(answerskeeper_id))

end_test = InlineKeyboardButton('📍 End Test 📍', callback_data=tb.end_test_cmd)

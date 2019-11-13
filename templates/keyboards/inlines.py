# keyboard = InlineKeyboardMarkup([[IB, IB],[IB]])

from telegram import InlineKeyboardMarkup
from templates import inlinebuttons as ib
from . import generators as kg

def test_preview(answerskeeper_id):
    return InlineKeyboardMarkup([[ib.start_test(answerskeeper_id)]])

questions = kg.select_question()

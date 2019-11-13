# Define your kwargs here, a kwarg is something constant
# that is used to be passed to the bot's send method.
# Example:
#    welcome = {'text':Q.welcome, 'reply_markup':RM.main}
import telegram

from . import quotes as q
from . import types as t
from consts import numbers as cn
from consts import ids as ci
from consts import fileids as cfi
from consts import questions as cqs
from consts.questions import all as cq
from .keyboards import texts as kt
from .keyboards import inlines as ki
from .keyboards import generators as kg


markdown = telegram.ParseMode.MARKDOWN

def invitation_banner(chat_id):
    return {
        'type': t.send_message,
        # 'photo': cfi.share_photo,
        'text': q.invitation_caption.format(chat_id),
        'parse_mode': markdown,
    }

def should_invite(inviteds, limit):
    return {
        'type': t.send_message,
        'text': q.should_invite.format(inviteds=inviteds, should_invite=limit-inviteds, limit=limit),
        'parse_mode': markdown,
    }

def parent_invited_before_activated(inviteds, limit):
    return {
        'type': t.send_message,
        'text': q.parent_invited_after_activation.format(inviteds=inviteds, should_invite=limit-inviteds, limit=limit),
        'parse_mode': markdown,
    }

def question(question_number, message_id=None):
    """Sends and handles edit of a message(showing the first question)
    """
    question = cq[question_number]
    return {
        'type': t.edit_message_text,
        'text': question['text'],
        'message_id': message_id,
        'reply_markup': kg.question_options(question_number),
        'parse_mode': markdown,
    }

def show_link(chat_id):
    return {
        'type': t.send_message,
        'text': q.show_link.format(chat_id),
        'parse_mode': markdown,
    }

def show_question_to_answerer(answerskeeper_id, question_number, questioner_name, main_question_number, message_id):
    """Sends and handles edit of a message
    """
    # TODO:
    question = cq[main_question_number]
    name = questioner_name
    name = name.replace('_', '')
    name = name.replace('`', '')
    name = name.replace('*', '')
    name = name.replace('[', '')
    name = name.replace(']', '')
    name = name.replace('(', '')
    name = name.replace(')', '')
    question_text = q.question_template.format(question_number=question_number, text=question['text-answerer'].replace('name', name))
    options = len(question['options'])
    return {
        'type': t.edit_message_media,
        'caption': question_text,
        'photo': question['photo'],
        'message_id': message_id,
        'reply_markup': kg.question_options_anwerer(answerskeeper_id, question_number, options),
        'parse_mode': markdown,
    }

def show_question_to_questioner(question_number, main_question_number, message_id=None):
    """Sends and handles edit of a message
    """
    # TODO:
    question = cq[main_question_number]
    question_text = q.question_template.format(question_number=question_number, text=question['text'])
    options = len(question['options'])
    if not message_id:
        return {
            # 'type': t.send_message,
            'type': t.send_photo,
            # 'text': question_text,
            'caption': question_text,
            'photo': question['photo'],
            'reply_markup': kg.question_options_questioner(question_number, main_question_number, options),
            'parse_mode': markdown,
        }
    else:
        return {
            # 'type': t.edit_message_text,
            'type': t.edit_message_media,
            'caption': question_text,
            'photo': question['photo'],
            'message_id': message_id,
            'reply_markup': kg.question_options_questioner(question_number, main_question_number, options),
            'parse_mode': markdown,
        }

def edit_answered(question_number, answer, message_id):
    """Should edit the answer and add an answered option
    """
    question = cq[question_number]
    return {
        'type': t.edit_message_reply_markup,
        'message_id': message_id,
        'reply_markup': kg.question_options(question_number, answer),
        'parse_mode': markdown,
    }

def show_question_numbers(message_id):
    return {
        'type': t.edit_message_reply_markup,
        'message_id': message_id,
        'reply_markup': ki.questions,
        'parse_mode': markdown,
    }

def edit_to_end(message_id):
    """Should edit the message and show ending and remove the keyboards.
    """
    question = cq[question_number]
    return {
        'type': t.edit_message_text,
        'text': q.end_of_test,
        'message_id': message_id,
        'reply_markup': None,
        'parse_mode': markdown,
    }

def scoreboard(text):
    return {
        'type': t.send_photo,
        'photo': cfi.scoreboard_photo,
        'caption': text,
        'parse_mode': markdown,
    }

def show_grade(answerskeeper, scoreboard):
    return {
        # 'type': t.edit_message_text,
        'type': t.edit_message_media,
        'caption': scoreboard,
        'photo': cfi.scoreboard_photo_updated,
        'message_id':answerskeeper.message_id,
        'parse_mode': markdown,
        'reply_markup': None,
    }

def show_start_preview(scoreboard, answerskeeper_id):
    text = q.show_start_preview.format(scoreboard)
    return {
        # 'type': t.send_message,
        'type': t.send_photo,
        'caption': text,
        'photo': cfi.scoreboard_photo,
        'reply_markup': ki.test_preview(answerskeeper_id),
        'parse_mode': markdown,
    }

someone_done = {
    'type': t.send_message,
    'text': q.someone_done,
}

has_done_once = {
    'type': t.send_message,
    'text': q.has_done_once,
}

new_user_join = {
    'type': t.send_message,
    'text': q.welcome,
    'reply_markup': kt.main_menu,
    'parse_mode': markdown,
}

parent_invited_after_activation = {
    'type': t.send_message,
    'text': q.parent_invited_after_activation,
    'parse_mode': markdown,
}

parent_invited_just_activated = {
    'type': t.send_message,
    'text': q.parent_invited_just_activated,
    'parse_mode': markdown,
}

main_menu_choose = {
    'type': t.send_message,
    'text': q.choose_option,
    'reply_markup': kt.main_menu,
}

answer_questions = {
    'type': t.send_message,
    'text': q.answer_questions,
}

invalid_join_link = {
    'type': t.send_message,
    'text': q.invalid_join_link,
    'reply_markup': kt.main_menu,
}

def link_created(message_id):
    return {
    'type': t.send_message,
    'text': q.link_created,
    'reply_to_message_id': message_id,
    'reply_markup': kt.main_menu,
}

help = {
    'type': t.send_message,
    'text': q.help,
    'parse_mode': markdown,
}

about = {
    'type': t.send_message,
    'text': q.about,
    'parse_mode': markdown,
}

ask_for_restart_answers = {
    'type': t.send_message,
    'text': q.restart_test_ask,
    'reply_markup': kt.restart_test,
}

# something that shows test information with a button: start, callback_data = start
test_preview = {
    'type': t.send_message,
    'text': q.test_info,
    'reply_markup': ki.test_preview,
    'parse_mode': markdown,
}

loading_test = {
    'type': t.send_message,
    'text': q.loading_test,
    'reply_markup': kg.remove_text_keyboard,
}

user_should_join_channel = {
    'type': t.send_message,
    'text': q.user_should_join_channel,
}

after_end = {
    'type': t.send_message,
    'text': q.choose_option_after_test,
    'reply_markup': kt.main_menu,
    'parse_mode': markdown,
}

havent_done_test = {
    'type': t.send_message,
    'text': q.havent_done_test,
}

enter_name = {
    'type': t.send_message,
    'text': q.enter_name,
    'reply_markup': kg.remove_text_keyboard,
    'parse_mode': markdown,
}

just_english = {
    'type': t.send_message,
    'text': q.just_english,
    'parse_mode': markdown,
}

long_name = {
    'type': t.send_message,
    'text': q.long_name,
    'parse_mode': markdown,
}

get_suppport = {
    'type': t.send_message,
    'text': q.get_suppport,
    'reply_markup': kt.support,
}

support_sent = {
    'type': t.send_message,
    'text': q.support_sent,
    'reply_markup': kt.main_menu,
}

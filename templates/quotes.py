# -*- coding: utf-8 -*-
# Write your constant texts here, like:
#   welcome = 'welcome to our bot.'
from consts import questions as qs
import telegram


right_answer = "✅"
wrong_answer = "❌"
please_try_again = '🔂 Please try again!'
exprired_test = '🚫 Test is expired! Please start another test.'
choose_option = '— لطفا یک گزینه رو انتخاب کنید'
choose_option_after_test = 'منوی اصلی.\nلطفا یک گزینه رو انتخاب کنید.'
restart_test_ask = '⁉️ شما قبلا کوییز خودتون رو آماده کردید. اگه این کارو انجام بدید کوییز قبلی پاک میشه. برا ادامه مطمئنید؟'
test_info = '🔖 Test title: `Cambridge General English Placement Test`\n\n📌 Number of questions: `%d`\n\n🎈 _Good Luck_'%qs.num # better to read from a questions file
end_of_test = '📍 Test is ended now. You can get your grade from main menu.'
parent_invited_before_activation = '💥 Someone just joined via your link.\n\n📊 You\'ve invited {inviteds}. \n👮🏽‍♂️ You should invite {should_invite} to reach {limit}'
parent_invited_after_activation = 'tnx. some on joined.'
parent_invited_just_activated = '✅ Congradulations! Someone just joined via your link and your account activated.'
answer_questions = "☘️ شما هنوز به سوالات خودتون پاسخ ندادید و کوییزتون رو درست نکردید❕ لطفا از گزینه  'ایجاد کوییز خودم' برای ساختن کوییزتون اقدام کنید."
loading_test = '⏳ در حال بارگذاری ...'
havent_done_test = 'You haven\'t completed any tests yet‼️'
has_done_once = '😊 شما این کوییزو یه بار انجام دادی! دوستای خوب تقلب نمیکنن 😐'
enter_name = '🔖 Please enter your first name and last name in English: \n  (e.g _John Smith_)'
just_english = '⌨️ Please change your keyboard to English.'
long_name = 'What a long name ❗️ I haven\'t such a memory to remember it❗️'
user_should_join_channel = '👮🏻‍♂️ لطفا توی کانال اسپانسر ما عضو بشید و بعدش ادامه بدید 🙏\n\n@linkdoonist  @linkdoonist\n@linkdoonist  @linkdoonist'
get_suppport = '📄 Any problems? Please write for us:'
invalid_join_link = "لینک ورودی معتبر نیست❗️"
support_sent = '📨 Message sent to us, we try to respond soon.'
link_created = '✅ لینک کوییز شما با موفقیت ساخته شد.\nلینک بالا 👆🏻 را بین دوستان خود در تلگرام و اینستاگرام به اشتراک بگذارید تا در کوییز شما شرکت کنند.'
welcome = "🌹 اوه! به ربات کوییز دوستی خوش اومدید. از منوی اصلی کوییز خودتونو بسازید و بین دوستاتون به اشتراک بذارید تا دوستای واقعیتون مشخص بشن ☺️"
someone_done = "🔖 یه نفر کوییز شما رو به اتمام رسوند. برای مشاهده نتایج از منوی اصلی اقدام کنید."
show_start_preview = "{}\n\n☘️ برای هر سوال حدس بزنید که دوست شما چه پاسخی داده. شروع کنیم؟؟"
score_record_for_questioner = "*{rank}.* [{name}](tg://user?id={chat_id}) با {points} امتیاز"
score_record_for_answerer = "*{rank}.* {name} با {points} امتیاز"
score_record_for_answerer_selected = "\n► *{rank}.* {name} با {points} امتیاز\n"
# score_record_for_answerer_selected = "*{rank}.* [{name}](tg://user?id={chat_id}) با {points} امتیاز"
nobody_has_done_yet_questioner = "🤷‍♂️ هنوز کسی کوییز شمارو انجام نداده. لینکتون رو از منوی اصلی برای دوستاتون به اشتراک بگذارید."
nobody_has_done_yet_answerer = "☺️ شما اولین نفری هستید که کوییز دوستتونو انجام میدید! احتمال زیادی میدم که از دوستای نزدیکش باشید. برای شروع آماده اید؟"
should_invite = '🔒 Sorry! This part is locked! Please invite `{limit}` persons to the bot via your Share link and then try again.\n\n 📊 You\'ve invited `{inviteds}` \n➕ You should invite `{should_invite}`'
show_link = "t.me/dQuizBot?start={}"
question_template = """
*{question_number}-* {text}
"""
help = """📘 راهنمای ربات

— برای ساختن کوییز خودتون از منوی اصلی گزینه ایجاد کوییز خودم رو انتخاب کنید.
— سوالاتیکه به شما مربوط نیستند رو رد کنید.
— بعد از اتمام تست ربات به شما یک لینک میده.
— اون لینک رو به دوستاتون بدید و بگید بیان به کوییز شما جواب بدن.
— لیست کسایی که به کوییز شما جواب دادن از منوی اصلی قابل مشاهدس.
— مشکلی بود با @engoyi در میون بذارید.

🌹 با آرزوی موفقیت"""
invitation_caption = """🎟 t.me/dQuizBot?start={}"""
about = """ℹ️ This placement test is provided to determine English levels of our users so we can plan more precise and more wised for them and also they can know which levels of us is appropriate for them.

⚜️ Sponsered by channel [🍊engoy](http://t.me/engoy), the channel which helps people [enjoy](http://t.me/engoy) learning English.


©️_2019_ [dbots™️](t.me/dbots) _all rights reserved_"""

admin_message = """📮 *Message from admin:*

{message}
"""

def create_score_board_text(answerers, questioner=True, answerer_id=None, name=''):
	if questioner:
		scoreboard = ""
	else:
		scoreboard = "🌟 لیست دوستان برتر دوست شما {}:\n\n".format(name,)

	separator = '\n'

	if len(answerers):
		for i, answerer in enumerate(answerers):
			name, chat_id, points = answerer
			if questioner:
				scoreboard += score_record_for_questioner.format(rank=i+1, name=name, chat_id=chat_id, points=points)
			else:
				if answerer_id == answerer[1]:
					scoreboard += score_record_for_answerer_selected.format(rank=i+1, name=name, points=points)
					# scoreboard += score_record_for_answerer_selected.format(rank=i+1, name=name, points=points)
				else:
					scoreboard += score_record_for_answerer.format(rank=i+1, name=name, points=points)

			scoreboard += separator
		return scoreboard
	else:
		if questioner:
			return nobody_has_done_yet_questioner
		else:
			return nobody_has_done_yet_answerer

# ADMIN

admin_sent = 'Message sent to the user successfully'
admin_choose = 'Please choose:'
send_to_all_stats = 'Takes `{mins}` mins to send your message to `{users}` users. send /cancel to stop.'
admin_sent_messages = 'Your message has been sent to `{users}`'
num_of_users = '{num} users.'
link_to_user = '[{chat_id}](tg://user?id={chat_id})\n'
stats = """
All = {}

direct = {}
invite = {}
"""

import json
import logging
from ast import literal_eval

import telegram

from models import User, AnswersKeeper
from .base import MyBaseHandler
from templates import kwargs, textbuttons, inlinebuttons, quotes
from consts import questions

logger = logging.getLogger(__name__)


class MyCallbackQueryHandler:
	def __init__(self, bot, update):
		self.bot = bot
		self.update = update
		self.data = update.callback_query.data
		self.cmd = self.data
		self.chat_id=update.callback_query.message.chat_id
		self.callback_query = update.callback_query
		self.user = User.get(chat_id=update.callback_query.message.chat_id)
		self.message = update.callback_query.message
		self.run()

	def run(self):
		# logger.info(f"data : {self.cmd}")
		if textbuttons.start_test_cmd in self.cmd:
			logger.info("request to start test")
			self.start_command()
			self.answer_callback_query()

		elif textbuttons.set_answer_cmd in self.cmd:
			cmd = self.cmd.split()
			question_number = int(cmd[1])
			main_question_number = int(cmd[2])
			answer = int(cmd[3])

			# logger.info(f"user answers: {self.user.answers}")

			self.user.set_answer(question_number, main_question_number, answer)

			# logger.info(f"user answers: {self.user.answers}")

			if question_number < questions.max_question_num:
				self.show_question_to_questioner(question_number+1, (main_question_number+1)%questions.num)
			else:
				self.show_link()
			self.answer_callback_query()

		elif textbuttons.skip_question_cmd in self.cmd:
			cmd = self.cmd.split()
			question_number = int(cmd[1])
			main_question_number = int(cmd[2])
			self.show_question_to_questioner(question_number, (main_question_number+1)%questions.num)
			self.answer_callback_query()

		elif textbuttons.answer_question_cmd in self.cmd:
			cmd = self.cmd.split()
			answerskeeper_id = int(cmd[1])
			question_number = int(cmd[2])
			answer = int(cmd[3])
			answerskeeper = AnswersKeeper.get(AnswersKeeper.id==answerskeeper_id)

			self.answer_question_command(answerskeeper, question_number, answer)

			if question_number < questions.max_question_num:
				self.show_question_to_answerer(question_number + 1, answerskeeper)
			else:
				self.show_end(answerskeeper)

	def show_link(self):
		"""edits current questions and shows the invite link
		and a link to select forward chat
		"""
		self.bot.delete_message(self.user.chat_id, message_id=self.message.message_id)
		message = self.bot.send(self.chat_id, kwargs.show_link(self.chat_id))
		self.bot.send(self.chat_id, kwargs.link_created(message.message_id))

	def answer_question_command(self, answerskeeper: AnswersKeeper, question_number: int, answer: int):
		"""answer <answers_id> <question_number> <option>
		"""
		# logger.info(f"answers: {answerskeeper.answers}")
		answerskeeper.set_answer(question_number, answer)
		# logger.info(f"answers: {answerskeeper.answers}")

		# self.user.answer_question(question_number, answer)

		check = answerskeeper.questioner.check_answer(question_number, answer)
		right_answer = answerskeeper.questioner.get_answer(question_number)

		if not check:
			self.answer_callback_query(quotes.wrong_answer.format(right_answer))
		else:
			self.answer_callback_query(quotes.right_answer)
		# self.bot.send(self.user.chat_id, kwargs.edit_answered(question_number, answer, self.user.test_message_id))

	def answer_callback_query(self, text=None):
		try:
			self.bot.answer_callback_query(self.update.callback_query.id, text)
		except Exception as e:
			pass

	def show_question_to_answerer(self, question_number: int, answerskeeper: AnswersKeeper):
		# logger.info(f"{question_number}: {answerskeeper}")
		# TODO: check for last message id
		main_question_number = answerskeeper.questioner.get_question(question_number)
		# question = questions.all[main_question_number]
		self.bot.send(
			self.chat_id,
			kwargs.show_question_to_answerer(answerskeeper.id, question_number, answerskeeper.questioner.name, main_question_number, self.message.message_id)
		)

	def show_question_to_questioner(self, question_number: int, main_question_number: int):
		# main_question_number = answerskeeper.questioner.get_question(question_number)
		# question = questions.all[main_question_number]
		self.bot.send(
			self.user.chat_id,
			kwargs.show_question_to_questioner(
				question_number,
				main_question_number,
				self.message.message_id
			)
		)

	def show_end(self, answerskeeper: AnswersKeeper):
		grade = answerskeeper.calculate_grade()
		answerskeeper.set_grade(grade)
		answerskeeper.set_ended()

		answerers = answerskeeper.questioner.get_answerers()

		# logger.info(f"answerers: {answerers}")

		scoreboard = quotes.create_score_board_text(answerers, questioner=False, answerer_id=self.chat_id, name=answerskeeper.questioner.name)

		self.bot.send(answerskeeper.questioner.chat_id, kwargs.someone_done)
		self.bot.send(self.chat_id, kwargs.show_grade(answerskeeper, scoreboard))
		self.bot.send(self.chat_id, kwargs.main_menu_choose)

	def check_expiration(method):
		"""Decorator for checking if the test is expired
		"""
		def decorator(self):
			if self.user.test_message_id != self.message.message_id:
				self.bot.answer_callback_query(self.callback_query.id, quotes.exprired_test)
				return
			return method(self)
		return decorator

	# @check_expiration
	def start_command(self):
		cmd = self.cmd.split()
		answerskeeper_id = int(cmd[1])
		answerskeeper = AnswersKeeper.get(AnswersKeeper.id==answerskeeper_id)
		# logger.info(f"answers keeper found: {answerskeeper}")
		self.show_question_to_answerer(1, answerskeeper)

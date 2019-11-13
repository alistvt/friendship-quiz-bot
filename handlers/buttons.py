import os
import logging
from time import sleep

import telegram

from templates import kwargs, textbuttons, quotes
from models import User
import consts
from consts import states, numbers, questions
from certificate.funcs import create_certificate
from .base import MyBaseHandler

logger = logging.getLogger(__name__)


class MyButtonHandler:
	def __init__(self, bot, update):
		self.bot = bot
		self.update = update
		self.chat_id = update.message.chat_id
		self.cmd = self.update.message.text
		# NOTE: check here for exception
		self.user = User.get(User.chat_id==self.chat_id)

		logger.info("user: {}".format(self.user))

		self.run()

	def member_required(method):
		"""Decorator for forcing user to join to channel
		"""
		def decorator(self):
			# TODO
			if self.bot.get_chat_member(chat_id=consts.ids.channel, user_id=self.chat_id).status[0] in ['m', 'a', 'c']:
				pass
			else:
				self.bot.send(self.chat_id, kwargs.user_should_join_channel)
				return
			return method(self)
		return decorator

	@member_required
	def run(self):
		states_ = {
			states.joining: self.joining_state,
			states.main: self.main_state,
			states.get_name: self.get_name,
			states.get_support: self.get_support_message_state,
		}
		states_[self.user.state]()

	def get_support_message_state(self):
		if self.cmd in textbuttons.all:
			return
		elif self.cmd == textbuttons.cancel:
			self.bot.send(self.chat_id, kwargs.main_menu_choose)
			self.user.set_state(states.main_menu)
		else:
			self.bot.send(self.chat_id, kwargs.support_sent)
			self.user.set_state(states.main_menu)
			self.update.message.forward(consts.ids.support_admin)

	def joining_state(self):
		self.user.set_state(states.main)
		self.user.add_to_parent(self.bot)
		self.main_state()

	def main_state(self):
		if self.cmd == textbuttons.answer_self_questions:
			self.answer_self_questions_button()
		elif self.cmd == textbuttons.sure_to_restart:
			self.sure_to_restart_button()
		elif self.cmd == textbuttons.not_sure_to_restart:
			self.bot.send(self.chat_id, kwargs.main_menu_choose)
		elif self.cmd == textbuttons.view_scoreboard:
			self.view_scoreboard_button()
		elif self.cmd == textbuttons.help:
			self.bot.send(self.chat_id, kwargs.help)
		elif self.cmd == textbuttons.share:
			if self.user.has_set_answers():
				message = self.bot.send(self.chat_id, kwargs.invitation_banner(self.chat_id))
				self.bot.send(self.chat_id, kwargs.link_created(message.message_id))
			else:
				self.bot.send(self.chat_id, kwargs.answer_questions)
		elif self.cmd == textbuttons.about:
			self.bot.send(self.chat_id, kwargs.about)
		elif self.cmd == textbuttons.support:
			self.support_button()

	def support_button(self):
		self.bot.send(self.chat_id, kwargs.get_suppport)
		self.user.set_state(states.get_suppport)

	def answer_self_questions_button(self):
		if not self.user.is_answers_empty():
			# means user has an active test yet.
			logger.info("hasent set answers yet.")
			self.bot.send(self.chat_id, kwargs.ask_for_restart_answers)
		else:
			self.delete_last_answers_message_and_remove_keyboard()
			# message = self.bot.send(self.chat_id, kwargs.test_preview)
			logger.info("hasent set answers yet.")
			message = self.bot.send(self.chat_id, kwargs.show_question_to_questioner(1, 0))
			self.user.set_answers_message_id(message.message_id)

			# logger.info(f"user set message_id: {self.user}")

	def sure_to_restart_button(self):
		self.delete_last_answers_message_and_remove_keyboard()
		# message = self.bot.send(self.chat_id, kwargs.test_preview)
		message = self.bot.send(self.chat_id, kwargs.show_question_to_questioner(1, 0))
		self.user.set_answers_message_id(message.message_id)

	def delete_last_test(self):
		try:
			self.bot.delete_message(self.user.chat_id, message_id=self.user.answers_message_id)
			self.user.delete_last_answers()
		except Exception as e:
			# whould be raised if message is for a long time ago
			pass

	def remove_keyboard():
		try:
			message = self.bot.send(self.chat_id, kwargs.loading_test)
			# sleep(1)
			self.bot.delete_message(self.user.chat_id, message_id=message.message_id)
		except Exception as e:
			pass

	def delete_last_answers_message_and_remove_keyboard(self):
		"""Deletes the last message and sets the last message of user to null
		And then Here we send a message without buttons and then delete it
		Send and say we are removing last message... and initing new test.
		"""
		try:
			message = self.bot.send(self.chat_id, kwargs.loading_test)
			try:
				self.bot.delete_message(self.user.chat_id, message_id=self.user.test_message_id)
			except Exception as e:
				# whould be raised if message is for a long time ago
				# logger.exception(e)
				pass
			self.user.delete_last_answers()
			self.bot.delete_message(self.user.chat_id, message_id=message.message_id)
		except Exception as e:
			pass

	def view_scoreboard_button(self):
		answerers = self.user.get_answerers()
		scoreboard = quotes.create_score_board_text(answerers, questioner=True)

		return self.bot.send(self.chat_id, kwargs.scoreboard(scoreboard))


	def prepare_get_name(self):
		self.bot.send(self.chat_id, kwargs.enter_name)
		self.user.set_state(states.get_name)


	def get_name(self):
		# HACK: : hacker???
		if self.cmd in textbuttons.all:
			pass
		if len(self.cmd) > 60:
			return self.bot.send(self.chat_id, kwargs.long_name)

		self.user.set_name(self.cmd)
		self.user.set_state(states.main)
		self.view_grade_button()

import logging

import telegram
from peewee import DoesNotExist

from models import User, AnswersKeeper
from templates import kwargs, quotes
from consts import states, numbers
from .base import MyBaseHandler

logger = logging.getLogger(__name__)


class MyStartHandler:
	def __init__(self, bot, update):
		self.bot = bot
		self.update = update
		self.chat_id = update.message.chat_id
		self.cmd = update.message.text
		self.run()

	def run(self):
		questioner_id = int(self.cmd.split()[-1]) if len(self.cmd.split())==2 else None
		if User.select().where(User.chat_id==self.chat_id).exists():
			self.user = User.get(User.chat_id==self.chat_id)
			if questioner_id:
				# with invite link
				if questioner_id != self.chat_id:
					self.start_test(questioner_id)
				else:
					self.bot.send(self.chat_id, kwargs.main_menu_choose)
			else:
				# without invite link
				self.user.set_state(states.main)
				self.bot.send(self.chat_id, kwargs.main_menu_choose)
		else:
			join_link = self.cmd.split()[-1] if len(self.cmd.split())==2 else ''
			first_name = self.update.message.chat.first_name or ''
			last_name = self.update.message.chat.last_name or ''
			name = first_name + ' ' + last_name
			self.user = User.create(name=name, join_link=self.cmd, chat_id=self.chat_id)

			logger.info("user created: {}".format(self.user))

			# self.bot.send(self.chat_id, kwargs.new_user_join)

			logger.info("joined link: {}".format(join_link))

			if join_link and questioner_id != self.chat_id:
				questioner_id = int(join_link)
				self.start_test(questioner_id)
			else:
				self.bot.send(self.chat_id, kwargs.main_menu_choose)

	def start_test(self, questioner_id):
		try:
			questioner = User.get(User.chat_id==questioner_id)
		except DoesNotExist:
			return self.bot.send(self.chat_id, kwargs.invalid_join_link)

		logger.info("questioner: {}".format(questioner))

		answerer = self.user

		logger.info("answerer: {}".format(answerer))

		if not questioner.has_set_answers():
			return self.bot.send(self.chat_id, kwargs.invalid_join_link)

		if AnswersKeeper.select().where((AnswersKeeper.questioner==questioner)&(AnswersKeeper.answerer==answerer)).exists():
			answerskeeper = AnswersKeeper.get((AnswersKeeper.questioner==questioner)&(AnswersKeeper.answerer==answerer))
			# logger.info(f"answerskeeper found : {answerskeeper}")
			if answerskeeper.ended:
				# logger.info(f"answerskeeper is ended")
				return self.bot.send(self.chat_id, kwargs.has_done_once)
			# logger.info(f"answerskeeper is not ended")
		else:
			answerskeeper = AnswersKeeper.create(questioner= questioner, answerer=answerer)
			# logger.info(f"answerskeeper created : {answerskeeper}")

		answerers = questioner.get_answerers()
		scoreboard = quotes.create_score_board_text(answerers, questioner=False)

		message = self.bot.send(self.chat_id, kwargs.show_start_preview(scoreboard, answerskeeper.id))

		answerskeeper.message_id = message.message_id
		answerskeeper.save()

	def delete_last_test(self):
		try:
			self.bot.delete_message(self.user.chat_id, message_id=self.user.test_message_id)
			self.user.delete_last_test()
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

	def delete_last_test_and_remove_keyboard(self):
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
			self.user.delete_last_test()
			self.bot.delete_message(self.user.chat_id, message_id=message.message_id)
		except Exception as e:
			pass

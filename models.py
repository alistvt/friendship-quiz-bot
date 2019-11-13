import json
import sys
from enum import Enum
from datetime import datetime, timedelta
from peewee import *

import logging
from telegram import (InlineKeyboardButton, InlineKeyboardMarkup)

import consts
from consts import states
from templates import quotes

logger = logging.getLogger(__name__)
db = SqliteDatabase('db.sqlite3', check_same_thread=False)


class BaseModel(Model):
	class Meta:
		database = db


class User(BaseModel):
	chat_id = IntegerField(unique=True)
	name = CharField()
	state = SmallIntegerField(default=states.main)
	inviteds = IntegerField(default=0)
	joined_date = DateTimeField(default=datetime.now)
	last_seen_date = DateTimeField(default=datetime.now)
	join_link = CharField(max_length=256, default='')
	# a dictionary containing user questions and answers: {i: (q, ans)}
	answers = CharField(max_length=256, default='{}')
	answers_message_id = BigIntegerField(null=True)

	def save(self, *args, **kwargs):
		self.last_seen_date = datetime.now()
		super(User, self).save(*args, **kwargs)

	def __str__(self):
		return 'User(id={id}, name={name}, chat_id={chat_id}, state={state}, answers_message_id={answers_message_id}, answers={answers})'.format(
				id=self.id, chat_id=self.chat_id, state=self.state, name=self.name, answers_message_id=self.answers_message_id, answers=self.answers
		)

	def set_state(self, state):
		self.state = state
		self.save()

	def set_answer(self, question_number: int, main_question_number: int, answer: int):
		answers = eval(self.answers)
		answers[question_number] = (main_question_number, answer)
		self.answers = str(answers)
		self.save()

	def check_answer(self, question_number: int, answer: int) -> bool:
		answers = eval(self.answers)
		if answers[question_number][1] == answer:
			return True
		return False

	def get_answer(self, question_number: int) -> int:
		answers = eval(self.answers)
		return answers[question_number][1]

	def get_question(self, question_number: int) -> int:
		answers = eval(self.answers)
		return answers[question_number][0]

	def has_set_answers(self) -> bool:
		answers = eval(self.answers)
		return len(answers) == consts.questions.max_question_num

	def is_answers_empty(self) -> bool:
		answers = eval(self.answers)
		return len(answers) == 0

	def set_answers_message_id(self, message_id):
		self.answers_message_id = message_id
		self.save()

	def delete_last_answers(self):
		try:
			self.answers_message_id = None
			self.answers = '{}'
			self.save()
		except Exception as e:
			logger.exception(e)

	def get_answerers(self):
		answereds = self.answereds.select().where(AnswersKeeper.ended==True).order_by(AnswersKeeper.grade.desc())
		answerers = []
		for answered in answereds:
			answerers.append((answered.answerer.name, answered.answerer.chat_id, answered.grade))
		return answerers

	@staticmethod
	def CountAll():
		"""return count all users cursor
		"""
		return User.select().count()

	@staticmethod
	def CountMoreThanWeek():
		now = datetime.now()
		weekago = datetime.now() - timedelta(days=7)
		return User.select().where(~(User.last_seen_date.between(weekago, now))).count()

	@staticmethod
	def CountLastWeekJoined():
		now = datetime.now()
		weekago = datetime.now() - timedelta(days=7)
		return User.select().where(User.joined_date.between(weekago, now)).count()

	@staticmethod
	def CountInvitedUsers():
		return User.select().where(User.join_link!='').count()

	def CountDirectUsers():
		return User.select().where(User.join_link=='').count()

	@staticmethod
	def Stats():
		# TODO
		pass
		return quotes.stats.format(User.CountAll(),
									# User.CountNotActivated(),
									# User.CountMoreThanWeek(),
									# User.CountLastWeekJoined(),
									User.CountDirectUsers(),
									User.CountInvitedUsers())

	@staticmethod
	def Cursor():
		"return all users cursor"
		count = User.CountAll()
		q = User.select()
		cursor = db.execute(q)
		return cursor, count

	@staticmethod
	def CursorMoreThanWeek():
		now = datetime.now()
		weekago = datetime.now() - timedelta(days=7)
		count = User.CountMoreThanWeek()
		q = User.select().where(~(User.last_seen_date.between(weekago, now)))
		cursor = db.execute(q)
		return cursor, count


class AnswersKeeper(BaseModel):
	answerer = ForeignKeyField(User)
	questioner = ForeignKeyField(User, backref='answereds')
	answers = CharField(max_length=256, default='{}')
	ended = BooleanField(default=False)
	grade = SmallIntegerField(null=True)
	message_id = BigIntegerField(null=True)
	creation_date = DateTimeField(default=datetime.now)

	def __str__(self):
		return "AnswersKeeper(id={id}, answerer={answerer}, questioner={questioner}, ended={ended}, grade={grade}, answers={answers})".format(
				id=self.id, answerer=self.answerer, questioner=self.questioner, ended=self.ended, grade=self.grade, answers=self.answers
		)

	def set_answer(self, question_number: int, answer: int):
		"""sets the answer
		"""
		answers = eval(self.answers)
		answers[question_number] = answer
		self.answers = str(answers)
		self.save()

	def set_ended(self):
		self.ended = True
		self.save()

	def set_grade(self, grade):
		self.grade = grade
		self.save()

	def calculate_grade(self):
		self_answers = eval(self.answers)
		answers = eval(self.questioner.answers)
		grade = 0
		for question in self_answers:
			if answers[question][1]==self_answers[question]:
				grade += 1
		return grade


def delete_all():
	connect()
	users = User.select()
	count = users.count()
	answer=input('Are you sure to delete %d users?(Y/n) '%count)
	if answer=='Y':
		try:
			count = User.delete().where(True).execute()
		except Exception as e:
			raise e
		print('   %d users deleted.'%count)

	answerskeepers = AnswersKeeper.select()
	count = answerskeepers.count()
	answer=input('Are you sure to delete %d answerskeepers?(Y/n) '%count)
	if answer=='Y':
		try:
			count = AnswersKeeper.delete().where(True).execute()
		except Exception as e:
			raise e
		print('   %d answerskeepers deleted.'%count)
	else:
		return


def create():
	db.connect()
	db.create_tables([User, AnswersKeeper])


def connect():
	db.connect()


if __name__ == '__main__':
	if len(sys.argv)==1:
		create()
	else:
		if sys.argv[1]=='delete':
			delete_all()
		else:
			print('- command not found.')
else:
	connect()

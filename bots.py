import logging

import telegram
from telegram import InputMediaPhoto
from telegram.utils.request import Request
from telegram.ext.messagequeue import MessageQueue, queuedmessage

from consts import token
from templates import types
logger = logging.getLogger(__name__)


class MyBot(telegram.bot.Bot):
	"""A subclass of Bot which delegates send method handling to MQ
	"""
	def __init__(self, *args, **kwargs):
		mqueue = MessageQueue(all_burst_limit=29, all_time_limit_ms=1024)
		request = Request(con_pool_size=8)
		is_queued_def=True
		super(MyBot, self).__init__(token = token.token, *args, request=request, **kwargs)
		# below 2 attributes should be provided for decorator usage
		self._is_messages_queued_default = is_queued_def
		self._msg_queue = mqueue or mq.MessageQueue()

	def __del__(self):
		try:
			self._msg_queue.stop()
		except:
			pass
		super(MyBot, self).__del__()

	# @queuedmessage
	def send_message(self, *args, **kwargs):
		"""Wrapped method would accept new `queued` and `isgroup`
		OPTIONAL arguments
		"""
		return super(MyBot, self).send_message(*args, **kwargs)

	# @queuedmessage
	def edit_message_text(self, *args, **kwargs):
		"""Wrapped method would accept new `queued` and `isgroup`
		OPTIONAL arguments
		"""
		return super(MyBot, self).edit_message_text(*args, **kwargs)

	def send(self, chat_id, kwargs):
		"""Should return a message instance
		"""
		kwargs = dict(kwargs)
		t = kwargs['type']
		if t == types.send_message:
			return self.send_message(chat_id, **kwargs)
		elif t == types.edit_message_text:
			text = kwargs.pop('text')
			return self.edit_message_text(text=text, chat_id=chat_id, **kwargs)
		elif t == types.edit_message_media:
			media = InputMediaPhoto(media=kwargs.pop('photo'), caption=kwargs.pop('caption'), parse_mode=kwargs.pop('parse_mode', None))
			return self.edit_message_media(chat_id=chat_id, media=media, **kwargs)
		elif t == types.edit_message_reply_markup:
			return self.edit_message_reply_markup(chat_id, **kwargs)
		elif t == types.send_photo:
			photo = kwargs.pop('photo')
			return self.send_photo(chat_id=chat_id, photo=photo, **kwargs)

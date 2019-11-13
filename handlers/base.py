from models import User


class MyBaseHandler:
	def __init__(self, bot, update):
		self.bot = bot
		self.update = update
		self.callback_query = update.callback_query
		# self.data = update.callback_query.data
		# self.user = User.get(chat_id=update.callback_query.message.chat_id)
		# self.cmd = self.data
		# self.message = update.callback_query.message
		self.run()

	def run(self):
		raise NotImplemented("run method not implemented.")

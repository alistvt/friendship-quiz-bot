import logging
import telegram
import copy
import consts.ids as cid
import consts.states as states
import templates.textbuttons as tb
import templates.quotes as cq
import templates.keyboards.texts as kt
from models import User

logger = logging.getLogger(__name__)


class MyAdminHandler:
	def __init__(self, bot, update, job_queue=None, chat_data=None):
		self.bot = bot
		self.update = update
		self.job_queue = job_queue
		self.chat_data = chat_data
		self.chat_id = update.message.chat_id
		self.user = User.get(chat_id=self.chat_id)
		try:
			self.run()
		except Exception as e:
			logger.exception(e)
			self.bot.send_message(cid.debug_admin, text=repr(e))

	def run(self):
		if self.user.state == states.admin_forward_to_all:
			try:
				self.sendBulkMessages()
			except Exception as e:
				logger.exception('xxxxx')
				self.bot.send_message(self.chat_id, text='Error')
			finally:
				self.user.set_state(states.admin_main)
		elif self.user.state == states.admin_send_to_all:
			try:
				self.sendBulkMessages(forward=False)
			except Exception as e:
				logger.exception('xxx')
				self.bot.send_message(self.chat_id, text='Error')
			finally:
				self.user.set_state(states.admin_main)
		elif self.update.message.reply_to_message:
			self.bot.send_message(self.update.message.reply_to_message.forward_from.id,
				text=cq.admin_message.format(message=self.update.message.text),
				parse_mode=telegram.ParseMode.MARKDOWN)
			self.bot.send_message(self.chat_id, text=cq.admin_sent)
		elif self.update.message.text == tb.start:
			self.bot.send_message(self.chat_id, text=cq.admin_choose, reply_markup=kt.admin_main)
			self.user.set_state(states.admin_main)
		elif self.update.message.text == tb.admin_num:
			num = User.select().count()
			self.bot.send_message(self.update.message.chat_id,
								  text=User.Stats())
		elif self.update.message.text == tb.admin_cancel:
			self.cancel()
		elif self.update.message.text == tb.admin_send_to_all:
			self.bot.send_message(self.update.message.chat_id, text='send me to send it')
			self.user.set_state(states.admin_send_to_all)
		elif self.update.message.text == tb.admin_forward_to_all:
			self.bot.send_message(self.update.message.chat_id, text='send me to forward it')
			self.user.set_state(states.admin_forward_to_all)

	def cancel(self):
		if 'job' not in self.chat_data:
			self.update.message.reply_text('You have no active send')
			return
		job = self.chat_data['job']
		job.schedule_removal()
		del self.chat_data['job']
		self.update.message.reply_text('Sending successfully cancelled! sent to: %d'%(job.context['sent']))
		job.context=''

	def sendBulkMessages(self, forward=True):
		try:
			del self.chat_data['job']
		except KeyError as e:
			pass

		context = dict()
		context['cursor'] = User.Cursor()
		context['chat_id'] = self.chat_id
		context['message'] = copy.deepcopy(self.update.message)
		context['sent'] = 0
		context['fw'] = forward
		try:
			due = 1
			# Add job to queue
			job = self.job_queue.run_repeating(AdminHandler.send20, due, first=0, context=context, name='send to all')
			self.chat_data['job'] = job
			self.update.message.reply_text(cq.send_to_all_stats.format(mins=int(User.select().count()/(1200)), users=User.select().count()), parse_mode=telegram.ParseMode.MARKDOWN)

		except Exception:
			logger.exception('here111')
			self.update.message.reply_text('Error ?')

	@staticmethod
	def send20(bot, job):
		blockeds = []
		for x in range(0,20):
			try:
				chat_id = next(job.context['cursor'])[1]
				if job.context['fw']:
					job.context['message'].forward(chat_id)
				else:
					bot.send_message(chat_id, text=job.context['message'].text)
				job.context['sent'] += 1
			except telegram.error.Unauthorized:
				blockeds.append(cq.link_to_user.format(chat_id=user.chat_id))
			except telegram.error.BadRequest:
				pass
			except StopIteration:
				job.schedule_removal()
				bot.send_message(job.context['chat_id'], cq.admin_sent_messages.format(users=job.context['sent']), parse_mode=telegram.ParseMode.MARKDOWN)
				return
			except Exception as e:
				logger.exception(e)

		blockeds = 'blocked by:\n\n' + ''.join(blockeds)
		bot.send_message(job.context['chat_id'], text=blockeds, parse_mode=telegram.ParseMode.MARKDOWN)

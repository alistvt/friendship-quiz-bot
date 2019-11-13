import logging
import telegram
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, Job, JobQueue, CallbackQueryHandler
import consts
from bots import MyBot
from handlers import (MyStartHandler, MyButtonHandler, MyErrorHandler,
					  MyIDGetterHandler, MyCallbackQueryHandler, MyAdminHandler)

logging.basicConfig(filename='bot.log', format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.WARNING)
logger = logging.getLogger(__name__)


def main():
	logger.info('Loading handlers for telegram bot')

	bot = MyBot()

	updater = telegram.ext.updater.Updater(bot=bot)
	dp = updater.dispatcher

	dp.add_handler(MessageHandler(Filters.chat(consts.ids.admins), MyAdminHandler, pass_job_queue=True, pass_chat_data=True))
	dp.add_handler(CommandHandler('start', MyStartHandler))
	dp.add_handler(MessageHandler(Filters.text, MyButtonHandler))
	dp.add_handler(CallbackQueryHandler(MyCallbackQueryHandler))
	dp.add_error_handler(MyErrorHandler)

	logger.info('Bot Started')
	dp.bot.send_message(consts.ids.main_admin, '/start me!')

	updater.start_polling()
	updater.idle()


if __name__ == '__main__':
	main()

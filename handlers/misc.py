
def MyIDGetterHandler(bot, update):
	print(update.message)
	bot.send_message(74174159, text=update.message.photo[-1].file_id)

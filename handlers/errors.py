import logging

logger = logging.getLogger(__name__)


def MyErrorHandler(bot, update, error):
    logger.exception(error)
    logger.warn('Update "%s" caused error "%s"' % (update, error))

import logging


from telegram.ext import Updater

from rosalind.bot import RosalindBot
logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)


def start():
    """
    Instantiates a Telegram updater to collect and manage events.

    :return:
    """
    bot = RosalindBot()

    updater = Updater(bot=bot)
    bot._add_handlers(updater)
    updater.start_polling()
    updater.idle()



if __name__ == '__main__':
   start()
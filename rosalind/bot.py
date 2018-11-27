import os
import logging

from telegram.bot import Bot
from telegram.ext import CommandHandler, CallbackQueryHandler

from rosalind.db.connection import RosalindDatabase
import rosalind.handlers as handlers

logger = logging.getLogger(__name__)

class RosalindBot(Bot):

    def __init__(self, token:str=""):
        if not token:
            self.__token = os.environ.get("TELEGRAM_TOKEN")
        else:
            self.__token = token

        super().__init__(self.__token)


        self.db = RosalindDatabase()
        self.inline_query_data = {}

    @staticmethod
    def _add_handlers(updater):
        """
        Adds all the handlers to the telegram updater object.
        """
        # basic commands
        updater.dispatcher.add_handler(CommandHandler('start', handlers.start))
        updater.dispatcher.add_handler(CommandHandler('help', handlers.start))

        # Hyper parameter search functionality.
        updater.dispatcher.add_handler(CommandHandler('runhypersearch', handlers.run_experiment_group))
        updater.dispatcher.add_handler(CallbackQueryHandler(handlers.button))
        updater.dispatcher.add_handler(CommandHandler('continuegroup', handlers.restart_experiment_group))

        # experiment montioring
        updater.dispatcher.add_handler(CommandHandler('running', handlers.running_experiments))
        updater.dispatcher.add_handler(CommandHandler('completed', handlers.completed_experiments))
        updater.dispatcher.add_handler(CommandHandler('pending', handlers.pending_experiments))
import os
import logging

from telegram.bot import Bot
from telegram.ext import CommandHandler

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

    @staticmethod
    def _add_handlers(updater):
        """
        Adds all the handlers to the telegram updater object.
        """
        updater.dispatcher.add_handler(CommandHandler('start', handlers.start))
        updater.dispatcher.add_handler(CommandHandler('runa2c', handlers.run_a2c_experiment))
        updater.dispatcher.add_handler(CommandHandler('runranda2c', handlers.run_experiment_group))
        updater.dispatcher.add_handler(CommandHandler('running', handlers.running_experiments))
        updater.dispatcher.add_handler(CommandHandler('completed', handlers.completed_experiments))
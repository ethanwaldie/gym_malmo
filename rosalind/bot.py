import os
import logging

from telegram.bot import Bot
from telegram.ext import CommandHandler

from rosalind.db.connection import ExperimentResultsDatabase
import rosalind.handlers as handlers

logger = logging.getLogger(__name__)

class RosalindBot(Bot):

    def __init__(self, token:str=""):
        if not token:
            self.__token = os.environ.get("TELEGRAM_TOKEN")
        else:
            self.__token = token

        super().__init__(self.__token)

        self.db = ExperimentResultsDatabase()

    @staticmethod
    def _add_handlers(updater):
        """
        Adds all the handlers to the telegram updater object.
        """
        updater.dispatcher.add_handler(CommandHandler('start', handlers.start))

def start(bot, update):
    """
    This is the initial setup of the bot.

    :param updater:
    :return:
    """

    update.message.reply_text(
        'Hello {} Looks like we are ready to go'.format(update.message.from_user.first_name))
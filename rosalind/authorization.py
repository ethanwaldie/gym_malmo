from enum import Enum

from rosalind.db.queries import get_user

class UserRoles(Enum):
    ADMIN = 1
    VIEWER = 2


def authorized_user(role=None):
    def authorized_user_wrapper(func):
        def wrapper(bot, update):
            try:
                user = get_user(bot.db, update.effective_user.id)
                if user and UserRoles[user.role].value <= role.value:
                    func(bot, update)
                else:
                    update.message.reply_text(
                        'Hello {} you do not have permission to use that method. \n'
                        'Please contact my administrator.'.format(update.message.from_user.first_name))
            except KeyError:
                update.message.reply_text(
                    'Hello {} something went wrong, and you could not be authorized. \n'
                    'Please contact my administrator.'.format(update.message.from_user.first_name))
        return wrapper
    return authorized_user_wrapper
import logging

from telegram.update import Update

from rosalind.authorization import authorized_user, UserRoles
from rosalind.db.queries import get_experiments_by_status_df
from rosalind.db.types import ExperimentStatus

from rosalind.experiment_runners.user_flow_handlers import run_experiment_group_button_handler, generate_keyboard_markup_for_options

logger = logging.getLogger(__name__)

@authorized_user(role=UserRoles.VIEWER)
def start(bot, update:Update):
    """
    This handler returns the instructions and available methods for the bot.

    :param updater:
    :return:
    """

    update.message.reply_text(
        'Hello {} Looks like we are ready to go! \n'
        'Avaliable methods are: \n'
        '/start - Returns the list of commands.\n'
        '/running - get the running experiments and their progress\n'
        '/completed - gets the completed experiments\n'
        '/pending - get the currently pending experiments\n'
        ''.format(update.message.from_user.first_name))


@authorized_user(role=UserRoles.VIEWER)
def running_experiments(bot, update:Update):
    """
    This handler displays the currently running experiments.

    :param bot:
    :param update:
    :return:
    """
    experiments_df = get_experiments_by_status_df(rosalind_connection=bot.db,
                                                  status=ExperimentStatus.RUNNING.name)

    cols = ['model', 'status', 'current_timestep', 'total_timesteps', 'updated_date']

    update.message.reply_html('<code>' + experiments_df.to_string(columns=cols) +  '</code>')


@authorized_user(role=UserRoles.VIEWER)
def completed_experiments(bot, update:Update):
    """
    This handler displays the completed experiments.

    :param bot:
    :param update:
    :return:
    """
    experiments_df = get_experiments_by_status_df(rosalind_connection=bot.db,
                                                  status=ExperimentStatus.COMPLETED.name,
                                                  limit=5)

    cols = ['model', 'status', 'current_timestep', 'total_timesteps', 'updated_date']

    update.message.reply_html('<code>' + experiments_df.to_string(columns=cols) + '</code>')


@authorized_user(role=UserRoles.VIEWER)
def pending_experiments(bot, update:Update):
    """
    This handler displays the completed experiments.

    :param bot:
    :param update:
    :return:
    """
    experiments_df = get_experiments_by_status_df(rosalind_connection=bot.db,
                                                  status=ExperimentStatus.PENDING.name)

    cols = ['model', 'status', 'current_timestep', 'total_timesteps', 'updated_date']

    update.message.reply_html('<code>' + experiments_df.to_string(columns=cols) + '</code>')


@authorized_user(role=UserRoles.VIEWER)
def plot_experiment(bot, update:Update):
    pass

@authorized_user(role=UserRoles.VIEWER)
def button(bot, update:Update):
    query = update.callback_query

    data = query.data

    run_experiment_group_button_handler(bot, update, query, data)

@authorized_user(role=UserRoles.ADMIN)
def run_experiment_group(bot, update:Update):

    options = ["a2c", "deepq"]

    reply_markup = generate_keyboard_markup_for_options(options=options)

    update.message.reply_text('Select a model to run:', reply_markup=reply_markup)

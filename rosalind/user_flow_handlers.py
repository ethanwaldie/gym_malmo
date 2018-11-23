import logging
import traceback
import json
import uuid

from telegram.update import Update
from telegram.callbackquery import CallbackQuery
from telegram import InlineKeyboardButton, InlineKeyboardMarkup


from experiments.a2c.hyper_parameter_search import generate_a2c_hyper_param_set
from experiments.deep_dqn.hyper_parameter_search import generate_dqn_hyper_param_set

from rosalind.experiment_utils import run_new_single_experiment_with_monitoring

from rosalind.db.queries import get_user

logger = logging.getLogger(__name__)

def generate_keyboard_markup_for_options(options, labels=None):
    """
    This function generates a keyboard markup where one field in the callback data is changed.

    :param options:
    :param data_key:
    :param data:
    :return:
    """
    keyboard = []
    for i, option in enumerate(options):
        if labels:
            key = InlineKeyboardButton(labels[i], callback_data=option)
        else:
            key = InlineKeyboardButton(option, callback_data=option)

        keyboard.append([key])

    return InlineKeyboardMarkup(keyboard)
def run_experiment_group_button_handler(bot, update:Update, query:CallbackQuery, data):
    """
    This handler manages incoming requests to run certain experiment groups.




    :param bot:
    :param update:
    :param query:
    :return:
    """

    keyboard = None

    # if "model" in data:
    #     if data["model"] == "deepq" and "network" not in data:
    #
    #         options = ["mlp", "cnn", "cnn_small"]
    #
    #         reply_markup = generate_keyboard_markup_for_options(options=options,
    #                                                         data_key="network",
    #                                                         data=data)
    #
    #         query.message.reply_text('Select a Network for the Policy', reply_markup=reply_markup)
    #
    #         return
    #
    #     options = ["MalmoDiscreteSimpleHallways-v0",
    #                "MalmoDiscreteSimpleHallwaysVisual-v0"]
    #
    #     reply_markup = generate_keyboard_markup_for_options(options=options,
    #                                                     data_key="env_id",
    #                                                     data=data)
    #
    #     query.message.reply_text('Select an Environment', reply_markup=reply_markup)
    #
    #     return


    model = data.split("|")[-1]

    try:
        if model == "a2c":
            params = generate_a2c_hyper_param_set(number=20,
                                                  total_timesteps=1000000)

        elif model == "deepq":
            params = generate_dqn_hyper_param_set(number=20,
                                                  network="mlp",
                                                  total_timesteps=1000000)
        else:
            params = []

        group_id = uuid.uuid4()

        user = get_user(bot.db, update.effective_user.id)

        for i in range(len(params)):
            run_new_single_experiment_with_monitoring(bot=bot,
                                                      user=user,
                                                      model=model,
                                                      env_id="MalmoDiscreteSimpleHallways-v0",
                                                      group_id=group_id,
                                                      model_params=params[i])
    except Exception as e:
        tb = traceback.format_exc()
        logger.exception("Unable to start Experiment. ")
        query.message.reply_text(
            'Unable to Start Experiment Failed with ```{}```'.format(tb))
    else:
        query.message.reply_text(
            'Started Experiment Group {}'.format(group_id))
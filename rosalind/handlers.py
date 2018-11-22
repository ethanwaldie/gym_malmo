import logging
import traceback
import json
import pandas
import random
import uuid

from rosalind.authorization import authorized_user, UserRoles
from rosalind.experiment_utils import run_new_single_experiment_with_monitoring
from rosalind.db.queries import get_user, get_recent_completed_experiments_df, get_running_experiments_df


logger = logging.getLogger(__name__)

@authorized_user(role=UserRoles.VIEWER)
def start(bot, update):
    """
    This handler returns the instructions and available methods for the bot.

    :param updater:
    :return:
    """

    update.message.reply_text(
        'Hello {} Looks like we are ready to go! \n'
        'Avaliable methods are: \n'
        '/start - Returns the list of commands.\n'
        '/runa2c - runs the A2C model with specified params\n'
        '        - env_ids are:\n'
        '                      MalmoDiscreteSimpleHallways-v0\n'
        '                      MalmoDiscreteSimpleHallwaysVisual-v0\n'
        '/running - get the running experiments and their progress\n'
        '/completed - gets the completed experiments\n'
        '/plot - gets the training reward plots for an experiment. \n'
        ''.format(update.message.from_user.first_name))


@authorized_user(role=UserRoles.VIEWER)
def running_experiments(bot, update):
    """
    This handler displays the currently running experiments.

    :param bot:
    :param update:
    :return:
    """
    experiments_df = get_running_experiments_df(rosalind_connection=bot.db)

    cols = ['model', 'status', 'current_timestep', 'total_timesteps', 'updated_date']

    update.message.reply_html('<code>' + experiments_df.to_string(columns=cols) +  '</code>')


@authorized_user(role=UserRoles.VIEWER)
def completed_experiments(bot, update):
    """
    This handler displays the completed experiments.

    :param bot:
    :param update:
    :return:
    """
    experiments_df = get_recent_completed_experiments_df(rosalind_connection=bot.db)

    cols = ['model', 'status', 'current_timestep', 'total_timesteps', 'updated_date']

    update.message.reply_html('<code>' + experiments_df.to_string(columns=cols) + '</code>')


@authorized_user(role=UserRoles.VIEWER)
def plot_experiment(bot, update):
    pass

@authorized_user(role=UserRoles.ADMIN)
def run_a2c_experiment(bot, update):
    """
    This handler runs an experiment, with specified hyper parameters.

    :param bot:
    :param update:
    :return:
    """
    user = get_user(bot.db, update.effective_user.id)

    base_params = {
        "env_id": "MalmoDiscreteSimpleHallwaysVisual-v0",
        "model_params": {
            "network": "cnn",
            "total_timesteps": 400000,
            "checkpoint_freq": 1000,
            "print_freq":10
            }
        }
    try:

        experiment = run_new_single_experiment_with_monitoring(bot=bot,
                                              user=user,
                                              model='deepq',
                                              env_id=base_params['env_id'],
                                              model_params=base_params['model_params'])
    except Exception as e:
        tb = traceback.format_exc()
        logger.exception("Unable to start Experiment. ")
        update.message.reply_text(
            'Unable to Start Experiment Failed with ```{}```'.format(tb))
    else:
        update.message.reply_text(
            'Started Experiment {}'.format(experiment.id))


@authorized_user(role=UserRoles.ADMIN)
def run_experiment_group(bot, update):
    base_params = {
            "env_id": "MalmoDiscreteSimpleHallways-v0",
            "model_params": {
                "network": "lstm",
                "seed": None,
                "nsteps": 5,
                "total_timesteps": 1000000,
                "vf_coef": 0.5,
                "ent_coef": 0.01,
                "max_grad_norm": 0.5,
                "lr": 7e-4,
                "lrschedule": "linear",
                "epsilon": 1e-5,
                "alpha": 0.99,
                "gamma": 0.99,
                "log_interval": 1000,
            }
        }

    hyper_param_ranges = {
        "vf_coef" : (0, 1),
        "ent_coef": (0.001, 0.1),
        "max_grad_norm": (0, 1),
        "lr": (7e-3, 7e-5),
        "epsilon": (1e-4, 1e-6),
        "alpha": (0.7, 0.99),
        "gamma": (0.7, 0.99)
    }


    user = get_user(bot.db, update.effective_user.id)
    group_id = uuid.uuid4()

    try:
        for i in range(10):
            data = base_params
            for k,v in hyper_param_ranges.items():
                data['model_params'][k] = random.uniform(*v)

            logger.info(data)

            experiment = run_new_single_experiment_with_monitoring(bot=bot,
                                                  user=user,
                                                  model='a2c',
                                                  env_id=data['env_id'],
                                                  group_id=group_id,
                                                  model_params=data['model_params'])
    except Exception as e:
        tb = traceback.format_exc()
        logger.exception("Unable to start Experiment. ")
        update.message.reply_text(
            'Unable to Start Experiment Failed with ```{}```'.format(tb))
    else:
        update.message.reply_text(
            'Started Experiment Group {}'.format(group_id))







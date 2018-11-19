import logging
import uuid
import os
import time
import traceback
import datetime

from multiprocessing import Process
from experiments.a2c.train import train_a2c

from rosalind.experiment_monitor import ExperimentMonitor
from rosalind.db.schema import Experiments, ClientPool
from rosalind.db.queries import create_experiment, update_experiment, \
    find_available_client, update_client, get_user, get_experiment
from rosalind.db.types import ClientStatus, ExperimentStatus

_MODELS = {
    'a2c': train_a2c
}

def build_log_dir(experiment_id):
    base_log_dir = os.path.join(os.path.dirname(__file__), "logs")

    if not os.path.isdir(base_log_dir):
        os.mkdir(base_log_dir)

    log_dir = os.path.join(base_log_dir, str(experiment_id))

    if not os.path.isdir(log_dir):
        os.mkdir(log_dir)

    return log_dir

def send_message_to_owner(bot, experiment, message):
    """
    This function sends a telegram message to the experiment owner.

    :param experiment:
    :param message:
    :return:
    """

    user = get_user(experiments_connection=bot.db, user_id=experiment.owner)

    bot.send_message(chat_id=user.chat_id,
                     text=message)

def train_model(
              bot,
              experiment,
              log_dir: str,
              model_runner,
              env_id:str,
              model_params):

    logger = logging.getLogger("experiment-{}".format(experiment.id))
    fh = logging.FileHandler(os.path.join(log_dir,'train.log'))
    fh.setLevel(logging.INFO)
    logger.addHandler(fh)

    experiment_monitor = ExperimentMonitor(log_dir=log_dir,
                                           name="ExperimentMonitor-{}".format(experiment.id),
                                           experiment_id=experiment.id,
                                           bot=bot, logger=logger)

    client = find_available_client(experiments_connection=bot.db)

    while not client:
        logger.info("No clients available, waiting for available clients...")
        time.sleep(10)
        client = find_available_client(experiments_connection=bot.db)

    logger.debug("Reserving Client {}".format(client.address))

    update_client(experiments_connection=bot.db,
                  client_address=client.address,
                  fields={ClientPool.status: ClientStatus.OCCUPIED.name,
                          ClientPool.current_experiment: experiment.id})

    client_pool = client.address.split(":")
    client_pool = [(client_pool[0], int(client_pool[1]))]

    try:

        update_experiment(experiments_connection=bot.db,
                          experiment_id=experiment.id,
                          fields={Experiments.status: ExperimentStatus.RUNNING.name})

        experiment_monitor.start()

        model_runner(log_dir,
                     env_id,
                     client_pool,
                     10,
                     logger,
                     **model_params)

    except Exception as e:

        experiment_monitor.stop()
        experiment_monitor.join(timeout=2)

        update_experiment(experiments_connection=bot.db,
                          experiment_id=experiment.id,
                          fields={Experiments.status: ExperimentStatus.FAILED.name,
                                  Experiments. end_date: datetime.datetime.utcnow()})

        logger.exception("Experiment {} Failed!".format(experiment.id))
        tb = traceback.format_exc()
        send_message_to_owner(bot=bot,
                              experiment=experiment,
                              message='The experiment with id {} failed!'
                                      'Traceback: \n '
                                      '{}'.format(experiment.id, tb))
        raise e
    else:

        update_experiment(experiments_connection=bot.db,
                          experiment_id=experiment.id,
                          fields={Experiments.status: ExperimentStatus.COMPLETED.name,
                                  Experiments. end_date: datetime.datetime.utcnow()})
        send_message_to_owner(bot=bot,
                              experiment=experiment,
                              message='The experiment with id {} completed!'.format(experiment.id))
    finally:
        experiment_monitor.stop()
        experiment_monitor.join(timeout=2)
        client.status = ClientStatus.AVALIABLE.name
        update_client(experiments_connection=bot.db, client=client)

def run_new_single_experiment_with_monitoring(bot,
                                       user,
                                       model:str,
                                       env_id: str,
                                       model_params):

    model_runner = _MODELS.get(model)

    if not model_runner:
        raise KeyError("The model {} has not been implemented.".format(model))

    experiment_id = uuid.uuid4()
    group_id = uuid.uuid4()
    log_dir = build_log_dir(experiment_id)

    create_experiment(experiments_connection=bot.db,
                                   experiment_id=experiment_id,
                                   group_id=group_id,
                                   model=model,
                                   env_id=env_id,
                                   owner=user,
                                   total_timesteps=model_params['total_timesteps'],
                                   log_dir=log_dir,
                                   model_params=model_params)
    experiment = get_experiment(experiments_connection=bot.db, experiment_id=experiment_id)

    try:
        training_process = Process(target=train_model, args=(bot,
                                              experiment,
                                              log_dir,
                                              model_runner,
                                              env_id,
                                              model_params))
        training_process.start()
    except Exception as e:
        tb = traceback.format_exc()
        send_message_to_owner(bot=bot,
                              experiment=experiment,
                              message='The experiment with id {} failed!'
                                      'Traceback: \n '
                                      '{}'.format(experiment.id, tb))
        raise e


    update_experiment(experiments_connection=bot.db,
                      experiment_id=experiment.id,
                      fields={Experiments.pid: training_process.pid})

    return experiment
















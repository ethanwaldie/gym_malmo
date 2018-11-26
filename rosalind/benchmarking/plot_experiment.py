import os
import logging
import datetime
import pprint
import matplotlib.pyplot as plt




from rosalind.db.schema import Experiments
from rosalind.experiment_runners.experiment_utils import build_log_dir
from rosalind.db.queries import get_experiments_group_id

from rosalind.benchmarking.utils import build_results_dir
from rosalind.benchmarking.plot_utils import plot_results

def get_experiments_results_plot(bot,
                                experiment:Experiments,
                                ylims=(-300000, 5000)):
    """
    This function plots the learning curve for a specified experiment.

    :param bot:
    :param experiment_id:
    :return:
    """


    log_dir = build_log_dir(experiment_id=experiment.id)

    results_dir = build_results_dir()

    plot_results([log_dir],
                 num_timesteps=experiment.total_timesteps,
                 task_name="Episode Rewards for Model {} and Experiment {}".format(experiment.model, experiment.id),
                 xaxis="timesteps",
                 yaxis="reward")

    plot_path = os.path.join(results_dir, "{}-episodes.png".format(experiment.id))

    plt.ylim(*ylims)
    plt.savefig(plot_path)

    return plot_path



def get_experiment_group_results_plot(bot,
                                 group_id:str,
                                 ylims=(-300000, 5000)):
    log_dirs = []

    results_dir = build_results_dir()

    experiments = get_experiments_group_id(rosalind_connection=bot.db,
                                           group_id=group_id)

    for experiment in experiments:
        if experiment.status in [ExperimentStatus.RUNNING.name, ExperimentStatus.COMPLETED.name]:
            log_dir = build_log_dir(experiment_id=experiment.id)
            log_dirs.append(log_dir)

    timesteps = min([e.total_timesteps for e in experiments])

    plot_results(log_dirs,
                 num_timesteps=timesteps,
                 task_name="Episode Rewards for Model {} and Group {}".format(experiments[0].model, group_id),
                 xaxis="timesteps",
                 yaxis="reward")

    plot_path = os.path.join(results_dir, "{}-episodes.png".format(group_id))

    plt.ylim(*ylims)
    plt.savefig(plot_path)

    return plot_path


if __name__ == '__main__':
    X_TIMESTEPS = 'timesteps'
    X_EPISODES = 'episodes'
    X_WALLTIME = 'walltime_hrs'
    Y_REWARD = 'reward'
    Y_TIMESTEPS = 'timesteps'

    from rosalind.bot import RosalindBot
    from rosalind.db.queries import get_experiments_by_status
    from rosalind.db.types import ExperimentStatus

    bot = RosalindBot()

    experiments = get_experiments_by_status(bot.db, ExperimentStatus.COMPLETED.name)

    for experiment in experiments:
        get_experiments_results_plot(bot, experiment)

    get_experiment_group_results_plot(bot, experiments[0].group_id)


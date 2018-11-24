import logging
import matplotlib

from baselines.results_plotter import plot_results

from rosalind.db.schema import Experiments
from rosalind.experiment_runners.experiment_utils import build_log_dir


def get_experiment_result_plot(bot, experiment:Experiments):
    """
    This function plots the learning curve for a specified experiment.
    It returns the png file of the plot that can be sent via telegram.


    :param bot:
    :param experiment_id:
    :return:
    """


    log_dir = build_log_dir(experiment_id=experiment.id)

    plot_results([log_dir],
                 num_timesteps=experiment.total_timesteps,
                 task_name=" Model {} Experiment ID {}".format(experiment.model, experiment.id),
                 xaxis="timesteps",
                 yaxis="rewards")


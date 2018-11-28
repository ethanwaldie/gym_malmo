import os
import time
import mmap
import subprocess
import select
import threading
import json

from rosalind.db.schema import Experiments
from rosalind.db.queries import get_experiment, increment_experiment_timesteps


class ExperimentMonitor(threading.Thread):
    """
    This class generates a thread that can be used to montior the status of a long running
    experiment and save it status to a database. This database is queried by rosalind to provide up
    to date statistics on what experiments are running at a given time.

    """

    def __init__(self,
                 log_dir: str,
                 name: str,
                 bot,
                 experiment_id,
                 logger):
        """

        :param log_dir:
        :param name:
        :param bot:
        """
        super().__init__(name=name)
        self.logger = logger
        self.log_dir = log_dir
        self.bot = bot
        self.experiment_id = experiment_id
        self.progress_file = os.path.join(log_dir, 'progress.json')
        self._stop_event = threading.Event()

    def stop(self):
        self._stop_event.set()

    def stopped(self):
        return self._stop_event.is_set()

    def run(self):
        """
        The thread polls the experiments log files, and saves results.

        :return:
        """
        while not self.stopped():
            if os.path.isfile(self.progress_file):
                f = subprocess.Popen(['tail', '-f', self.progress_file],
                                     stdout=subprocess.PIPE, stderr=subprocess.PIPE)
                p = select.poll()
                p.register(f.stdout)

                while not self.stopped():
                    data = json.loads(f.stdout.readline())

                    total_timesteps = data.get('total_timesteps')

                    # dqn logs differently.
                    if not total_timesteps:
                        total_timesteps = data.get("steps")

                    if total_timesteps:
                        increment_experiment_timesteps(rosalind_connection=self.bot.db,
                                                       experiment_id=self.experiment_id,
                                                       timesteps=total_timesteps)
                    time.sleep(1)
            time.sleep(1)


if __name__ == '__main__':
    import logging

    logger = logging.getLogger(__name__)
    log_dir = '/Users/ethanwaldie/thesis/gym_malmo/rosalind/logs/0bf349cc-0e80-4fc0-abd8-58667b14bed3'
    experiment_monitor = ExperimentMonitor(log_dir=log_dir,
                                           name="ExperimentMonitor-{}".format(1),
                                           bot=None, logger=logger)

    experiment_monitor.start()
    experiment_monitor.join()

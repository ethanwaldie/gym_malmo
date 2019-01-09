import time
import logging
import argparse
import uuid
import traceback
from rosalind.bot import RosalindBot

from experiments.a2c.hyper_parameter_search import generate_a2c_hyper_param_set
from experiments.deep_dqn.hyper_parameter_search import generate_dqn_hyper_param_set

from rosalind.experiment_runners.experiment_utils import run_new_single_experiment_with_monitoring,send_message_to_owner

from rosalind.db.queries import get_user, get_experiments_by_group_id

logger = logging.getLogger(__name__)

USER = 287235005

if __name__ == '__main__':

    parser = argparse.ArgumentParser(description='Runs A Hyper Parameter search ')


    parser.add_argument('--number', type=int,
                        default=2,
                        help='The number hyper_parameter_variations')
    parser.add_argument('--env_id', type=str,
                        default='MalmoDiscreteSimpleHallways-v0',
                        help='The hostname to stamp in the experiments database.')
    parser.add_argument('--model', type=str,
                        default='a2c',
                        help='The starting port, client ports will increment from here.')

    args = parser.parse_args()

    bot = RosalindBot()

    user = get_user(bot.db, USER)

    try:
        if args.model == "a2c":
            params = generate_a2c_hyper_param_set(number=args.number,
                                                  total_timesteps=500000)

        elif args.model == "deepq":
            params = generate_dqn_hyper_param_set(number=args.number,
                                                  network="cnn_small",
                                                  total_timesteps=500000)
        else:
            params = []

        group_id = uuid.uuid4()

        for i in range(len(params)):
            run_new_single_experiment_with_monitoring(bot=bot,
                                                      user=user,
                                                      model=args.model,
                                                      env_id=args.env_id,
                                                      group_id=group_id,
                                                      model_params=params[i])
    except Exception as e:
        tb = traceback.format_exc()
        bot.send_message(text='Unable to Start Experiment Failed with ```{}```'.format(tb),
                         chat_id=user.chat_id)
    else:
        bot.send_message(
            text='Started Experiment Group {}'.format(group_id),
        chat_id=user.chat_id)

        while True:
            logger.info("Experiments Running...")
            time.sleep(100)




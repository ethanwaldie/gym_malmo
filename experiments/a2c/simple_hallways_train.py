import gym
import logging
import traceback
import argparse

# ------- PARSE ARGUMENTS --------

from experiments.env_args import add_standard_env_args
from experiments.a2c.a2c_args import add_a2c_args

parser = argparse.ArgumentParser(description='Trains the A2C model on the SimpleHallwaysEnv')

parser = add_standard_env_args(parser)
parser = add_a2c_args(parser)
args = parser.parse_args()

# ---------------------------

from common.notifier.telegram_notifier import send_message
from baselines.a2c import a2c
from baselines.common.vec_env.dummy_vec_env import DummyVecEnv
from envs.discrete.simple_hallways import SimpleHallwaysEnv

from baselines.bench.monitor import Monitor



logging.basicConfig(level=args.log_level)
logger = logging.getLogger(__name__)

env = SimpleHallwaysEnv(tick_speed=args.tick_speed)


if args.record:
    env.init(start_minecraft=False ,recordDestination='recording.tgz',
             recordMP4=(10, 400000))
else:
    env.init(start_minecraft=False )

env_fn = lambda: env

vec_env = Monitor(DummyVecEnv([env_fn]), "train_a2c.log")

send_message("A2C Experiment Started")

try:
    act = a2c.learn(
        network=args.network,
        env=vec_env,
        seed=args.seed,
        nsteps=args.nsteps,
        total_timesteps=args.total_timesteps,
        vf_coef=args.vf_coef,
        ent_coef=args.ent_coef,
        max_grad_norm=args.max_grad_norm,
        lr=args.lr,
        lrschedule=args.lrschedule,
        epsilon=args.epsilon,
        alpha=args.alpha,
        gamma=args.gamma,
        log_interval=args.log_interval,
        load_path='simple_hallways_a2c_model.pkl'
    )

    send_message("Saving model to trained .pkl")
    act.save("simple_hallways_a2c_model.pkl")
except:
    send_message("A2C Experiment Failing ```{}```".format(traceback.format_exc()))
    env.close()
    logger.exception("Failed in Training A2C")
import gym
import logging
import traceback

from common.notifier.telegram_notifier import send_message
from baselines.a2c import a2c
from baselines.common.vec_env.dummy_vec_env import DummyVecEnv

from envs.discrete.simple_hallways import SimpleHallwaysEnv

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

env = SimpleHallwaysEnv()

env.init(start_minecraft=False,recordDestination='recording.tgz',
         recordMP4=(10, 400000))

env_fn = lambda: env

vec_env = DummyVecEnv([env_fn])

send_message("A2C Experiment Started")

try:
    act = a2c.learn(
        network='lstm',
        env=vec_env,
        seed=None,
        nsteps=5,
        total_timesteps=100000,
        vf_coef=0.5,
        ent_coef=0.01,
        max_grad_norm=0.5,
        lr=7e-4,
        lrschedule='linear',
        epsilon=1e-5,
        alpha=0.99,
        gamma=0.99,
        log_interval=100,
        load_path=None
    )

    send_message("Saving model to trained .pkl")
    act.save("simple_hallways_a2c_model.pkl")
except:
    send_message("A2C Experiment Failing ```{}```".format(traceback.format_exc()))
    logger.exception("Failed in Training A2C")
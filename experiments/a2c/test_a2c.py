import gym
import logging
import traceback


from common.notifier.telegram_notifier import send_message
from baselines.a2c import a2c
from baselines.common.vec_env.dummy_vec_env import DummyVecEnv

from envs.discrete.simple_hallways import SimpleHallwaysEnv


logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

env = SimpleHallwaysEnv(tick_speed=20)

env.init(start_minecraft=False)

env_fn = lambda: env

vec_env = DummyVecEnv([env_fn])

act = a2c.learn(network='lstm',env=vec_env, total_timesteps=0, load_path="simple_hallways_a2c_model.pkl")

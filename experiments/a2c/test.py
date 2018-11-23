import time
import logging

from envs.discrete.simple_hallways import SimpleHallwaysEnv

from baselines.a2c import a2c
from baselines.a2c.runner import Runner
from baselines.common.vec_env.dummy_vec_env import DummyVecEnv

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

env = SimpleHallwaysEnv()

env.init(start_minecraft=False, logger=logger)

env_fn = lambda: env
vec_env = DummyVecEnv([env_fn])

params = {"network": "lstm", "seed": None, "nsteps": 5, "vf_coef": 0.7296517437546484, "ent_coef": 0.08170105386305099, "max_grad_norm": 0.28316872667632487, "lr": 0.004572103455541685, "lrschedule": "linear", "epsilon": 7.350402288162664e-06, "alpha": 0.7974457456640998, "gamma": 0.7621534677537529, "log_interval": 1000}

model = a2c.learn(
    env=vec_env,
    total_timesteps=0,
    load_path='../../rosalind/logs/758dfa59-8e79-4f01-b5bd-91475b28a85e/model.pkl',
    **params)

runner = Runner(vec_env, model, nsteps=params['nsteps'], gamma=params['gamma'])

while True:
    obs, states, rewards, masks, actions, values = runner.run()
    print("Episode reward", rewards)


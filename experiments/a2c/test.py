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

params = {
  "lr": 0.0398918521489106,
  "seed": None,
  "alpha": 0.99,
  "gamma": 0.99,
  "nsteps": 5,
  "epsilon": 0.00001,
  "network": "lstm",
  "vf_coef": 0.515792291405908,
  "ent_coef": 0.07217431211508817,
  "lrschedule": "linear",
  "log_interval": 1000,
  "max_grad_norm": 0.4278537190622296,
}

model = a2c.learn(
    env=vec_env,
    total_timesteps=0,
    load_path='../../rosalind/experiment_runners/logs/faaf742d-beac-4645-89ba-f4136afd446f/model.pkl',
    **params)

runner = Runner(vec_env, model, nsteps=params['nsteps'], gamma=params['gamma'])

while True:
    obs, states, rewards, masks, actions, values = runner.run()
    print("Episode reward", rewards)


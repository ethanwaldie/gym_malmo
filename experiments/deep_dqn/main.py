import time
import logging

from envs.discrete.simple_hallways import SimpleHallwaysEnv

from baselines.deepq import deepq

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

env = SimpleHallwaysEnv()

env.init(start_minecraft=False)


act = deepq.learn(env, network='mlp', total_timesteps=0, load_path="simple_hallways_dqn_model.pkl")

while True:
    obs, done = env.reset(), False
    episode_rew = 0
    while not done:
        env.render()
        obs, rew, done, _ = env.step(act(obs[None])[0])
        episode_rew += rew
    print("Episode reward", episode_rew)



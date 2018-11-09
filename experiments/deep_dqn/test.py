import gym
import logging

from baselines import deepq



from envs.discrete.simple_hallways_visual import SimpleHallwaysVisualEnv

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

env = SimpleHallwaysVisualEnv()

env.init(start_minecraft=False)


act = deepq.learn(env, network='cnn_small', total_timesteps=0, load_path="experiment.pkl")

while True:
    episode_rew = 0
    obs, done = env.reset(), False
    while not done:
        env.render()
        obs, rew, done, _ = env.step(act(obs[None])[0])
        episode_rew += rew
    print("Episode reward", episode_rew)


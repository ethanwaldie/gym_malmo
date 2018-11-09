import gym
import logging
import matplotlib.pyplot as plt
from matplotlib import style

style.use('fivethirtyeight')

plt.axis([0, 10000, 0, 600])

from baselines import deepq, a2c

from envs.discrete.simple_hallways_visual import SimpleHallwaysVisualEnv

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

env = SimpleHallwaysVisualEnv()

env.init(start_minecraft=False)

def callback(lcl, _glb):
    # stop training if reward exceeds 199
    is_solved = lcl['t'] > 100 and len(lcl['episode_rewards']) >= 500
    return is_solved

act = deepq.learn(
    env,
    network='cnn',
    lr=1e-3,
    total_timesteps=20000,
    buffer_size=10000,
    exploration_fraction=0.1,
    exploration_final_eps=0.02,
    checkpoint_freq=50,
    checkpoint_path='simple_hallways_dqn_checkpoint',
    print_freq=10,
    callback=callback
)
print("Saving model to trained .pkl")
act.save("simple_hallways_dqn_model.pkl")
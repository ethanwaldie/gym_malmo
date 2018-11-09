import gym
import logging
from baselines import deepq, a2c

from envs.discrete.simple_hallways_visual import SimpleHallwaysVisualEnv

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

env = SimpleHallwaysVisualEnv()

env.init(start_minecraft=False,
         recordDestination='recording.tgz',
         recordMP4=(10, 400000))

def callback(lcl, _glb):
    # stop training if reward exceeds 199
    is_solved = sum(lcl['episode_rewards'][-101:-1]) / 100 >= 100
    return is_solved

act = deepq.learn(
    env,
    network='cnn_small',
    lr=1e-3,
    total_timesteps=20000,
    buffer_size=10000,
    exploration_fraction=0.1,
    exploration_final_eps=0.05,
    checkpoint_freq=50,
    checkpoint_path='simple_hallways_dqn_checkpoint',
    print_freq=10,
    callback=callback
)
print("Saving model to trained .pkl")
act.save("simple_hallways_dqn_model.pkl")
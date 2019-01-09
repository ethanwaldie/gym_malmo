import gym
import logging

from baselines import deepq



from envs.discrete.simple_hallways import SimpleHallwaysEnv

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

env = SimpleHallwaysEnv()

env.init(start_minecraft=False)

params = {
  "lr": 0.002743864619682306,
  "seed": None,
  "gamma": 1,
  "network": "mlp",
  "callback": None,
  "batch_size": 32,
  "print_freq": 10,
  "train_freq": 1,
  "buffer_size": 1000,
  "param_noise": False,
  "checkpoint_freq": 50,
  "checkpoint_path": None,
  "learning_starts": 500,
  "prioritized_replay": False,
  "exploration_fraction": 0.1,
  "exploration_final_eps": 0.02,
  "prioritized_replay_eps": 0.000001,
  "prioritized_replay_alpha": 0.6,
  "prioritized_replay_beta0": 0.4,
  "target_network_update_freq": 100,
  "prioritized_replay_beta_iters": None
}

act = deepq.learn(env,
                  total_timesteps=0,
                  load_path="../../rosalind/experiment_runners/logs/c0ac9c12-a4aa-4174-8782-398c7a70dff8/model.pkl",
                  **params)

while True:
    episode_rew = 0
    obs, done = env.reset(), False
    while not done:
        env.render()
        obs, rew, done, _ = env.step(act(obs[None])[0])
        episode_rew += rew
    print("Episode reward", episode_rew)


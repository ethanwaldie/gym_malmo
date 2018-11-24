import random


def generate_dqn_hyper_param_set(number: int,
                                 network: str="mlp",
                                 total_timesteps=1000000):
    base_params = {
                   "network": network,
                   "seed": None,
                   "lr": 5e-4,
                   "total_timesteps": total_timesteps,
                   "buffer_size": 5000,
                   "exploration_fraction": 0.1,
                   "exploration_final_eps": 0.02,
                   "train_freq": 1,
                   "batch_size": 32,
                   "print_freq": 10,
                   "checkpoint_freq": 50,
                   "checkpoint_path": None,
                   "learning_starts": 1000,
                   "gamma": 1.0,
                   "target_network_update_freq": 500,
                   "prioritized_replay": False,
                   "prioritized_replay_alpha": 0.6,
                   "prioritized_replay_beta0": 0.4,
                   "prioritized_replay_beta_iters": None,
                   "prioritized_replay_eps": 1e-6,
                   "param_noise": False,
                   "callback": None,
                   "load_path": None}

    hyper_param_ranges = {
        "lr": (7e-3, 7e-5),
        "batch_size": list(range(20, 50)),
        "exploration_fraction": (0.05, 0.2),
        "exploration_final_eps":(0.01, 0.1),
        "gamma": (0.7, 0.99),
        "prioritized_replay_alpha": (0.5, 1),
        "prioritized_replay_beta0": (0.3, 0.6),
        "prioritized_replay_eps": (1e-5, 1e-7),
    }

    params = []

    for i in range(number):
        model_params = base_params.copy()
        for hyper_param, param_range in hyper_param_ranges.items():
            if isinstance(param_range, list):
                model_params[hyper_param] = random.choice(param_range)
            else:
                model_params[hyper_param] = random.uniform(*param_range)
        params.append(model_params)
    return params

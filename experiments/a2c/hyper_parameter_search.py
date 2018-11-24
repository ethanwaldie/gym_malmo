import random


def generate_a2c_hyper_param_set(number: int,
                                 total_timesteps=1000000):
    """
    This functions generates model hyper parameter sets which can be used when preforming a hyper parameter search.


    :param number:
    :param grid:
    :return:
    """

    base_params = {
        "network": "lstm",
        "seed": None,
        "nsteps": 5,
        "total_timesteps": total_timesteps,
        "vf_coef": 0.5,
        "ent_coef": 0.01,
        "max_grad_norm": 0.5,
        "lr": 7e-4,
        "lrschedule": "linear",
        "epsilon": 1e-5,
        "alpha": 0.99,
        "gamma": 0.99,
        "log_interval": 1000,
    }

    hyper_param_ranges = {
        "lr": (7e-2, 7e-5),
        "vf_coef": (0, 1),
        "ent_coef": (0.001, 0.1),
        "max_grad_norm": (0, 1),
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
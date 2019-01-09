import os
import gym
import envs
import logging


def train_dqn(log_dir: str,
              env_id:str,
              client_pool: [(str, str)],
              tick_speed=10,
              logger=None,
              record=False,
              network='mlp',
              seed=None,
              lr=5e-4,
              total_timesteps=100000,
              buffer_size=50000,
              exploration_fraction=0.1,
              exploration_final_eps=0.02,
              train_freq=1,
              batch_size=32,
              print_freq=100,
              checkpoint_freq=10000,
              checkpoint_path=None,
              learning_starts=1000,
              gamma=1.0,
              target_network_update_freq=500,
              prioritized_replay=False,
              prioritized_replay_alpha=0.6,
              prioritized_replay_beta0=0.4,
              prioritized_replay_beta_iters=None,
              prioritized_replay_eps=1e-6,
              param_noise=False,
              callback=None,
              load_path=None,
              **network_kwargs):
    """
    This function trains and runs the A2C model. It accepts a list of hyper parameters.

    :param log_dir:
    :param experiment_id:
    :param env_id:
    :param network:
    :param seed:
    :param nsteps:
    :param total_timesteps:
    :param vf_coef:
    :param ent_coef:
    :param max_grad_norm:
    :param lr:
    :param lrschedule:
    :param epsilon:
    :param alpha:
    :param gamma:
    :param log_interval:
    :param load_path:
    :param network_kwargs:
    :return:
    """

    # set the logging env_vars
    os.environ['OPENAI_LOG_FORMAT'] = 'json'
    os.environ['OPENAI_LOGDIR'] = log_dir

    # import inside the function to make sure all logging is configured correctly.
    from baselines import deepq
    from baselines.common.vec_env.dummy_vec_env import DummyVecEnv
    from baselines.bench.monitor import Monitor

    if len(client_pool) > 1:
        logging.warning("Too many clients specified for this model. Only 1 will be used!")

    client_address = client_pool[0]

    env = gym.make(env_id)

    if record:
        env.init(start_minecraft=False ,recordDestination=os.path.join(os.environ['OPENAI_LOGDIR'],'recording.tgz'),
                 recordMP4=(10, 400000), client_pool=client_pool, recordRewards=True,
                 recordCommands=True, tick_speed=tick_speed, logger=logger)
    else:
        env.init(start_minecraft=False, client_pool=client_pool, tick_speed=tick_speed, logger=logger)

    menv = Monitor(env, os.path.join(os.environ['OPENAI_LOGDIR'],'monitor.csv'))


    act = deepq.learn(
        env=menv,
        network= network,
        seed = seed,
        lr = lr,
        total_timesteps = total_timesteps,
        buffer_size = buffer_size,
        exploration_fraction = exploration_fraction,
        exploration_final_eps = exploration_final_eps,
        train_freq = train_freq,
        batch_size = batch_size,
        print_freq = print_freq,
        checkpoint_freq = checkpoint_freq,
        checkpoint_path = os.path.join(os.environ['OPENAI_LOGDIR'],'checkpoint.pkl'),
        learning_starts = learning_starts,
        gamma = gamma,
        target_network_update_freq = target_network_update_freq,
        prioritized_replay = prioritized_replay,
        prioritized_replay_alpha = prioritized_replay_alpha,
        prioritized_replay_beta0 = prioritized_replay_beta0,
        prioritized_replay_beta_iters = prioritized_replay_beta_iters,
        prioritized_replay_eps = prioritized_replay_eps,
        param_noise = param_noise,
        callback = callback,
        load_path = load_path,
        ** network_kwargs
        )

    act.save(os.path.join(os.environ['OPENAI_LOGDIR'],'model.pkl'))















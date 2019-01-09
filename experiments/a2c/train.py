import os
import gym
import envs
import logging


def train_a2c(log_dir: str,
              env_id:str,
              client_pool: [(str, str)],
              tick_speed=10,
              logger=None,
              record=False,
              network='lstm',
              seed=None,
              nsteps=5,
              total_timesteps=1000,
              vf_coef=0.5,
              ent_coef=0.01,
              max_grad_norm=0.5,
              lr=7e-4,
              lrschedule='linear',
              epsilon=1e-5,
              alpha=0.99,
              gamma=0.99,
              log_interval=100,
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
    from baselines.a2c import a2c
    from baselines.common.vec_env.shmem_vec_env import ShmemVecEnv
    from baselines.bench.monitor import Monitor

    env_fns = []

    spaces = None

    for client in client_pool:
        env = gym.make(env_id)

        if record:
            env.init(start_minecraft=False ,recordDestination=os.path.join(os.environ['OPENAI_LOGDIR'],'recording.tgz'),
                     recordMP4=(10, 400000), client_pool=client_pool, recordRewards=True,
                     recordCommands=True, tick_speed=tick_speed, logger=logger)
        else:
            env.init(start_minecraft=False, client_pool=client_pool, tick_speed=tick_speed, logger=logger)

        menv = Monitor(env, os.path.join(os.environ['OPENAI_LOGDIR'],'monitor.csv'))
        env_fn = lambda: menv
        env_fns.append(env_fn)

        spaces = (env.observation_space, env.action_space)

    vec_env = ShmemVecEnv(env_fns, spaces=spaces)

    act = a2c.learn(
        network=network,
        env=vec_env,
        seed=seed,
        nsteps=nsteps,
        total_timesteps=total_timesteps,
        vf_coef=vf_coef,
        ent_coef=ent_coef,
        max_grad_norm=max_grad_norm,
        lr=lr,
        lrschedule=lrschedule,
        epsilon=epsilon,
        alpha=alpha,
        gamma=gamma,
        log_interval=log_interval,
        load_path=load_path,
        **network_kwargs
    )

    act.save(os.path.join(os.environ['OPENAI_LOGDIR'],'model.pkl'))















from gym.envs.registration import register

register(
    id='MalmoDiscreteSimpleHallways-v0',
    entry_point='gym_malmo.envs.discrete.simple_hallways:SimpleHallwaysEnv',
)

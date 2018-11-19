from gym.envs.registration import register

register(
    id='MalmoDiscreteSimpleHallways-v0',
    entry_point='envs.discrete.simple_hallways:SimpleHallwaysEnv',
)

register(
    id='MalmoKeysAndDoors-v0',
    entry_point='envs.discrete.keys_and_doors:KeysAndDoorsEnv',
)

register(
    id='MalmoDiscreteSimpleHallwaysVisual-v0',
    entry_point='envs.discrete.simple_hallways_visual:SimpleHallwaysVisualEnv',
)
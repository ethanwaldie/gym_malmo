import MalmoPython
import os
import logging
import random
import json
import numpy as np
from gym import spaces

from common.malmo.malmo_env import MalmoEnvironment




class SimpleHallwaysEnv(MalmoEnvironment):
    """
    This environment represents the simplest of partially observable environments, an I
    shaped set of hallways consisting of a south_hallway, a north_hallway and a connecting
    hallway.

    Based on: http://proceedings.mlr.press/v48/oh16.pdf
    """

    metadata = {'render.modes': []}

    def __init__(self):
        self._spec_path = os.path.join(os.path.dirname(__file__), "schemas/simple_hallways_mission.xml")
        self.observation_space = spaces.Box(low=0, high=1, shape=(18, 5), dtype=np.int32)

        self.__observe_grid = "floor4x4"

        self.___obs_map = {
            "stone": [1, 0, 0, 0, 0, 0],
            "dirt": [0, 1, 0, 0, 0, 0],
            "air": [0, 0, 1, 0, 0, 0],
            "redstone_block": [0, 0, 0, 1, 0, 0],
            "gold_block": [0, 0, 0, 0, 1, 0],
            "diamond_block": [0, 0, 0, 0, 0, 1]
        }

        super().__init__(parse_world_state=True)


    def __draw_hallways(self):

        # south hallway
        self.mission_spec.drawCuboid(5, 2, 0, 0, 3, 0, 'air')
        self.mission_spec.drawCuboid(5, 2, 0, 5, 3, 10, 'air')
        self.mission_spec.drawCuboid(10, 2, 10, 0, 3, 10, 'air')


    def __draw_goals(self):

        # clear old goals
        self.mission_spec.drawBlock(10, 1, 10, 'stone')
        self.mission_spec.drawBlock(10, 1, 0, 'stone')
        self.mission_spec.drawBlock(0, 1, 10, 'stone')


        goal_position = random.choice(['left', 'right'])

        self.logger.info("Goal is on the {}".format(goal_position))


        if goal_position == 'left':
            self.mission_spec.drawBlock(10, 1, 10, 'diamond_block')
            self.mission_spec.drawBlock(2, 1, 0, 'gold_block')
        elif goal_position == 'right':
            self.mission_spec.drawBlock(0, 1, 10, 'diamond_block')
            self.mission_spec.drawBlock(2, 1, 0, 'redstone_block')

    def _build_observation_space(self):
        """
        Builds the observation space, based on the size of the grid and the replay_buffer.

        :return:
        """
        num_block_types = len(list(self.___obs_map.values())[0])

        if self.__observe_grid == "floor4x4":
            num_blocks_observed = 50
        elif self.__observe_grid == "floor3x3":
            num_blocks_observed = 18
        else:
            raise KeyError("Unable to determine grid size {}".format(self.__observe_grid))

        num_blocks_observed = num_blocks_observed*self.replay_buffer_size

        self.observation_space = spaces.Box(low=0, high=1, shape=(num_blocks_observed, num_block_types), dtype=np.int32)

    def _load_mission(self, **kwargs):
        """
        Mutates and returns the mission spec.

        :param kwargs:
        :return:
        """

        with open(self._spec_path, 'r') as f:
            mission_spec = f.read()

        mission_spec.replace("<MsPerTick>5</MsPerTick>", "<MsPerTick>{}</MsPerTick>".format(self.tick_speed))

        self.mission_spec = MalmoPython.MissionSpec(mission_spec, True)

        self.__draw_hallways()
        self.__draw_goals()

        return self.mission_spec


    def _world_state_parser(self, world_state):

        observations = self._get_observation(world_state)

        surrounds = observations[self.__observe_grid]

        obs = []

        for block in surrounds:
            obs.append(self.___obs_map[block])

        observation = self._update_replay_buffer_and_get_observation(np.array(obs, dtype=np.int32))

        return observation, sum([r.getValue() for r in world_state.rewards])

if __name__ == '__main__':
    import gym

    env = SimpleHallwaysEnv()
    env.init(start_minecraft=False)
    env.reset(force_reset=True)
    done = False

    while not done:
        action = env.action_space.sample()
        obs, reward, done, info = env.step(action)

    env.close()

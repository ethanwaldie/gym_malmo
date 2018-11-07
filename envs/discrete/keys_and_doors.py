import MalmoPython
import os
import logging
import random
import json
import numpy as np
from gym import spaces

from common.malmo.malmo_env import MalmoEnvironment

logger = logging.getLogger(__name__)


class KeysAndDoorsEnv(MalmoEnvironment):
    """
    This environment focuses on an agents ability to remember and make connections between tasks in an environment.

    There are two levers that each operate two doors. The agent needs to
    """

    metadata = {'render.modes': []}

    def __init__(self):
        self._spec_path = os.path.join(os.path.dirname(__file__), "schemas/keys_and_doors_mission.xml")

        self.observation_space = spaces.Box(low=0, high=1, shape=(5,18),dtype=np.int32)
        super().__init__(parse_world_state=True)



    def __draw_hallways(self):

        # connecting +
        self.mission_spec.drawCuboid(5, 2, 0, 0, 3, 0, 'air')
        self.mission_spec.drawCuboid(-5, 2, 0, 0, 3, 0, 'air')
        self.mission_spec.drawCuboid(0, 2, 5, 0, 3, 0, 'air')
        self.mission_spec.drawCuboid(0, 2, -5, 0, 3, 0, 'air')

        # Goal Hallway
        self.mission_spec.drawCuboid(5, 2, 4, 5, 3, 0, 'air')

    def __draw_rooms(self):

        # Three rooms
        self.mission_spec.drawCuboid(-5, 2, -1, -7, 3, 1, 'air')
        self.mission_spec.drawCuboid(-1, 2, 5, 1, 3, 7, 'air')
        self.mission_spec.drawCuboid(-1, 2, -5, 1, 3, -7, 'air')

    def __draw_levers_and_doors(self):
        #self.mission_spec.drawBlock(5, 2, 1, 'wooden_door')
        pass


    def _load_mission(self, **kwargs):
        """
        Mutates and returns the mission spec.

        :param kwargs:
        :return:
        """

        with open(self._spec_path, 'r') as f:
            mission_spec = f.read()

        self.mission_spec = MalmoPython.MissionSpec(mission_spec, True)

        #self.__draw_hallways()
        #self.__draw_rooms()
        #self.__draw_levers_and_doors()

        return self.mission_spec

    def _world_state_parser(self, world_state):

        obs_map = {
            "stone": [1, 0, 0, 0, 0],
            "dirt": [1, 0, 0, 0, 0],
            "air": [0, 1, 0, 0, 0],
            "redstone_block": [0, 0, 1, 0, 0],
            "gold_block": [0, 0, 0, 1, 0],
            "diamond_block": [0, 0, 0, 0, 1]
        }


        observations = self._get_observation(world_state)

        floor = observations["floor3x3"]

        obs = []

        for block in floor:
            obs.append(obs_map[block])

        return np.array(obs, dtype=np.int32), sum([r.getValue() for r in world_state.rewards])

    def seed(self, seed=None):
        pass


if __name__ == '__main__':
    import gym
    env = KeysAndDoorsEnv()
    env.init(start_minecraft=False)
    env.reset(force_reset=True)
    done = False

    env.render(mode="human")
    action = env.action_space.sample()
    obs, reward, done, info = env.step(action)

    env.close()
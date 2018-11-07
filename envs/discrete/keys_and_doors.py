import MalmoPython
import os
import logging
import random
import json
import numpy as np
from gym import spaces

from common.malmo.malmo_env import MalmoEnvironment
from common.malmo.mission_xml import MissionSpec
from common.malmo.drawing_utils import *

logger = logging.getLogger(__name__)


class KeysAndDoorsEnv(MalmoEnvironment):
    """
    This environment focuses on an agents ability to remember and make connections between tasks in an environment.

    There are two levers that each operate two doors. The agent needs to
    """

    metadata = {'render.modes': []}

    def __init__(self):
        self._spec_path = os.path.join(os.path.dirname(__file__), "schemas/keys_and_doors_mission.xml")

        self.observation_space = spaces.Box(low=0, high=1, shape=(5, 18), dtype=np.int32)
        super().__init__(parse_world_state=True)

    def __draw_hallways(self):
        hallways = []

        hallways.append(
            build_element(malmo_types.DrawCuboid, x1=5, y1=2, z1=0, x2=0, y2=3, z2=0,type=malmo_types.BlockType.air))
        hallways.append(
            build_element(malmo_types.DrawCuboid, x1=-5, y1=2, z1=0, x2=0, y2=3, z2=0, type=malmo_types.BlockType.air))
        hallways.append(
            build_element(malmo_types.DrawCuboid, x1=0, y1=2, z1=5, x2=0, y2=3, z2=0, type=malmo_types.BlockType.air))
        hallways.append(
            build_element(malmo_types.DrawCuboid, x1=0, y1=2, z1=-5, x2=0, y2=3, z2=0, type=malmo_types.BlockType.air))

        # Goal Hallway
        hallways.append(
            build_element(malmo_types.DrawCuboid, x1=5, y1=2, z1=-4, x2=5, y2=3, z2=0, type=malmo_types.BlockType.air))

        self.mission_spec.append_objects_to_drawing_decorator(hallways)

    def __draw_rooms(self):

        rooms = []

        rooms.append(
            build_element(malmo_types.DrawCuboid, x1=-5, y1=2, z1=-1, x2=-7, y2=3, z2=1, type=malmo_types.BlockType.air)
        )
        rooms.append(
            build_element(malmo_types.DrawCuboid, x1=-1, y1=2, z1=5, x2=1, y2=3, z2=7, type=malmo_types.BlockType.air)
        )
        rooms.append(
            build_element(malmo_types.DrawCuboid, x1=-1, y1=2, z1=-5, x2=1, y2=3, z2=-7, type=malmo_types.BlockType.air)
        )

        self.mission_spec.append_objects_to_drawing_decorator(rooms)

    def __draw_levers_and_doors(self):

        doors_and_levers = []

        doors_and_levers += DrawDoor(x=5, y=2, z=-2)

        self.mission_spec.append_objects_to_drawing_decorator(doors_and_levers)

    def _load_mission(self, **kwargs):
        """
        Mutates and returns the mission spec.

        :param kwargs:
        :return:
        """

        self.mission_spec = MissionSpec(self._spec_path)

        self.__draw_hallways()
        self.__draw_rooms()
        self.__draw_levers_and_doors()


        return MalmoPython.MissionSpec(str(self.mission_spec), True)

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

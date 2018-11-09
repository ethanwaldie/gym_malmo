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
            build_element(malmo_types.DrawCuboid, x1=5, y1=2, z1=0, x2=0, y2=3, z2=0, type=malmo_types.BlockType.air))
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

        doors_and_levers += draw_door(x=5, y=2, z=-2, type=malmo_types.BlockType.iron_door)

        lever_positions = [{'x': -6, 'y': 3, 'z': -1, 'face': malmo_types.Facing.SOUTH},
                           {'x': 1, 'y': 3, 'z': -6, 'face': malmo_types.Facing.WEST},
                           {'x': -1, 'y': 3, 'z': 6, 'face': malmo_types.Facing.EAST}]

        # first we clear the old lever positions
        doors_and_levers += [build_element(malmo_types.DrawBlock, type=malmo_types.BlockType.air, **pos)
                             for pos in lever_positions]

        # select a new lever position
        current_lever_position = random.choice(lever_positions)
        doors_and_levers.append(
            build_element(malmo_types.DrawBlock, type=malmo_types.BlockType.lever, **current_lever_position))

        self.mission_spec.append_objects_to_drawing_decorator(doors_and_levers)

    def __draw_wires(self):
        corners = [{'x': -8, 'y': 4, 'z': -8},
                   {'x': -8, 'y': 4, 'z': 8},
                   {'x': 6, 'y': 4, 'z': 8},
                   {'x': 6, 'y': 4, 'z': -8},
                   {'x': -8, 'y': 4, 'z': -8}]

        connections = [[
                            {'x': -2, 'y': 4, 'z': 8},
                            {'x': -2, 'y': 4, 'z': 6}
                        ],
                        [
                            {'x': 2, 'y': 4, 'z': -8},
                            {'x': 2, 'y': 4, 'z': -6}
                        ],
                        [
                            {'x': -8, 'y': 4, 'z': -2},
                            {'x': -6, 'y': 4, 'z': -2}
                        ],
                    ]

        wires = draw_connected_points(vertices=corners, type=malmo_types.BlockType.redstone_wire)
        for connection in connections:
            wires += draw_connected_points(vertices=connection, type=malmo_types.BlockType.redstone_wire)


        repeater_positions = [{'x': -7, 'y': 4, 'z': 8, 'face': malmo_types.Facing.WEST},
                              {'x': 6, 'y': 4, 'z': 7, 'face': malmo_types.Facing.SOUTH},
                              {'x': -7, 'y': 4, 'z': -8, 'face': malmo_types.Facing.WEST},
                              {'x': 6, 'y': 4, 'z': -7, 'face': malmo_types.Facing.NORTH}]

        repeaters = [build_element(malmo_types.DrawBlock, type=malmo_types.BlockType.unpowered_repeater, **pos)
                     for pos in repeater_positions]

        self.mission_spec.append_objects_to_drawing_decorator(wires + repeaters)


    def __draw_goal(self):
        goal = build_element(malmo_types.DrawBlock, x=5, y=1, z=-4,
                             type=malmo_types.BlockType.diamond_block)

        self.mission_spec.append_objects_to_drawing_decorator([goal])

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
        self.__draw_wires()
        self.__draw_goal()

        return MalmoPython.MissionSpec(str(self.mission_spec), True)

    def _world_state_parser(self, world_state):
        obs_map = {
            "stone": [1, 0, 0, 0, 0],
            "dirt": [1, 0, 0, 0, 0],
            "air": [0, 1, 0, 0, 0],
            "iron_door": [0, 0, 1, 0, 0],
            "lever": [0, 0, 0, 1, 0],
            "diamond_block": [0, 0, 0, 0, 1],
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

    while not done:
        action = env.action_space.sample()
        obs, reward, done, info = env.step(action)

    env.close()

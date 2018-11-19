import MalmoPython
import os
import logging
import random
import json
import numpy as np
from gym import spaces

from common.malmo.malmo_env import MalmoEnvironment


class SimpleHallwaysVisualEnv(MalmoEnvironment):
    """
    This environment represents the simplest of partially observable environments, an I
    shaped set of hallways consisting of a south_hallway, a north_hallway and a connecting
    hallway.

    Based on: http://proceedings.mlr.press/v48/oh16.pdf
    """

    metadata = {'render.modes': []}

    def __init__(self, hall_params:dict = None):
        self._spec_path = os.path.join(os.path.dirname(__file__), "schemas/simple_hallways_visual_mission.xml")

        super().__init__(parse_world_state=False)



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

    def _load_mission(self, **kwargs):
        """
        Mutates and returns the mission spec.

        :param kwargs:
        :return:
        """

        with open(self._spec_path, 'r') as f:
            mission_spec = f.read()

        self.mission_spec = MalmoPython.MissionSpec(mission_spec, True)

        self.__draw_hallways()
        self.__draw_goals()

        return self.mission_spec

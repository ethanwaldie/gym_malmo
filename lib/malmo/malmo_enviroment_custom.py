import MalmoPython
import os
import sys
import time
import logging
import json


import gym
from gym import spaces
from gym.utils import seeding
import numpy as np



logger = logging.getLogger(__name__)


class MalmoEnvironment(gym.Env):
    """
    This is a simple object for generating and destroying malmo environments.

    This environment subclasses the openAI gym. This is used so that the environment can
    be interfaced with the openAI baselines.

    """
    def __init__(self):
        super().__init__()
        self._agent_host = MalmoPython.AgentHost()
        self.mission_spec = None
        self._mission_record_spec = None


    def _load_mission(self, **kwargs) -> str:
        """
        Override this function to generate a mission spec. The return should be
        a string containing the XML for this mission.

        :return:
        """
        raise NotImplementedError("You must Implement a Mission Spec in order to start a mission!")


    def _generate_mission_record_spec(self, **kwargs) -> str:
        """
        Defines what components of the mission should be recorded.
        The default is to record nothing.

        To update what should be recorded from this mission override this function and use the spec:
        https://microsoft.github.io/malmo/0.21.0/Documentation/structmalmo_1_1_mission_record_spec.html

        :param kwargs:
        :return:
        """

        return MalmoPython.MissionRecordSpec()

    @staticmethod
    def parse_observations(world_state):
        return json.loads(world_state.observations[-1].text)

    def wait_for_valid_observations(self):
        """
        This function polls continuously for a valid world state from the malmo environment. Once it has a valid state
        observation it waits for a connection with video frames.
        :return:
        """
        world_state = self._agent_host.peekWorldState()
        while world_state.is_mission_running and all(e.text == '{}' for e in world_state.observations):
            world_state = self._agent_host.peekWorldState()

        # wait for a frame to arrive after that
        num_frames_seen = world_state.number_of_video_frames_since_last_state

        while world_state.is_mission_running and world_state.number_of_video_frames_since_last_state == num_frames_seen:
            world_state = self._agent_host.peekWorldState()

        for err in world_state.errors:
            logger.error("Errors in World States", err.text)

        assert len(world_state.video_frames) > 0, 'No video frames!?'

        return world_state, not world_state.is_mission_running


    def _wait_for_mission_start(self):
        # Loop until mission starts:
        logger.info("Waiting for the mission to start...")
        world_state = self._agent_host.getWorldState()

        while not world_state.has_mission_begun:
            time.sleep(0.1)

            world_state = self._agent_host.getWorldState()
            for error in world_state.errors:
                logger.error("Unable to fetch initial world state:", error.text)

            logger.info("Mission running ")

    def _start(self, max_retries:int=3):
        """
        This function actually starts the malmo mission.

        :param num_retires:
        :return:
        """

        # if no mission spec is passed we try to load the misson spec
        # with defualt parameters.



        self.mission_spec = self._load_mission()

        if not self._mission_record_spec:
            self._mission_record_spec = self._generate_mission_record_spec()

        logger.debug("Loaded Mission Spec... Starting Mission")

        # Attempt to start a mission:
        for retry in range(max_retries):
            try:
                self._agent_host.startMission(self.mission_spec, self._mission_record_spec)
                break
            except RuntimeError as e:
                if retry == max_retries - 1:
                    logger.exception("Error starting mission number of retries {}:".format(retry), e)
                    exit(1)
                else:
                    time.sleep(2)

        self._wait_for_mission_start()








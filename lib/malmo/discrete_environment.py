import random
import json
import logging
import time

from gym import spaces

from lib.malmo.malmo_enviroment_custom import MalmoEnvironment
from lib.malmo.position import AgentPositionOrientation

logger = logging.getLogger(__name__)

class DiscreteMalmoEnvironment(MalmoEnvironment):
    """
    This defines a discrete motion MalmoEnvironment.
    """
    _action_map = {
        0: "movenorth 1",
        1: "movesouth 1",
        2: "movewest 1",
        3: "moveeast 1"
    }

    def __init__(self):
        super().__init__()
        self.action_space = spaces.Discrete(4)
        self.state = None
        self.num_actions = 0
        self.agent_position = None
        self._start()

    def _world_state_parser(self, world_state):
        """
        This function pre-processes the world state from malmo into the observation space. This may be custom
        depending on the environments, blocks used encoding etc so this method should always be overwritten.

        :param world_state: World State Returned from Malmo
        :return:
        """
        raise NotImplementedError("A parser for the world state has not been implemented!")



    def _take_motion_action_and_wait_for_result(self, action_command: str, world_state):
        """
        This function attempts to take an action in the client and verify that this action has
        resulted in a change in the agents position. It will wait for up to 50ms for the action to take
        an effect on the space. If the action has not had any effect within those 50ms it will assume that the
        action could not effect the agents position and return the current state.

        TODO Update this to check for valid actions based on the agents surroundings to save the 50ms delay.


        :param action_command: command string.
        :param world_state:  initial world state
        :return: world_state, done where the observations are assumed to be complete.
        """
        if not self.agent_position:
            self.agent_position = AgentPositionOrientation.from_observation(self.parse_observations(world_state))

        # Send the Command to move to the agent host.
        self._agent_host.sendCommand(action_command)

        new_world_state = self._agent_host.peekWorldState()
        new_agent_position = AgentPositionOrientation.from_observation(self.parse_observations(new_world_state))

        # wait until the action takes effect
        for i in range(50):
            if self.agent_position == new_agent_position and new_world_state.is_mission_running:
                new_world_state = self._agent_host.peekWorldState()
                new_agent_position = AgentPositionOrientation.from_observation(self.parse_observations(new_world_state))
            else:
                logger.debug("Action did not change position returning original state.")
                break
            time.sleep(0.001)

        self.agent_position = new_agent_position

        return self.wait_for_valid_observations()


    def step(self, action):
        """
        Main environment action function. Used by the openAI scripts to interact with the environment

        :param action:
        :return:
        """

        assert self.action_space.contains(action), "%r (%s) invalid" % (action, type(action))

        world_state, done = self.wait_for_valid_observations()

        if not done:
            self.state, done = self._take_motion_action_and_wait_for_result(self._action_map[action],
                world_state)

        obs, reward = self._world_state_parser(self.state)

        return obs, reward, done, self.parse_observations(self.state)

    def reset(self):
        self._start()

    def render(self, mode='human'):
        pass


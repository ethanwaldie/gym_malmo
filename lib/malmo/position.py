import logging

logger = logging.getLogger(__name__)

class AgentPositionOrientation:
    def __init__(self, x:float=0, y:float=0, z:float=0, yaw:float=0, pitch:float=0):
        self._x = x
        self._y = y
        self._z = z
        self._yaw = yaw
        self._pitch = pitch

    @property
    def x(self):
        return self._x

    @property
    def y(self):
        return self._y

    @property
    def z(self):
        return self._z

    @property
    def yaw(self):
        return self._yaw

    @property
    def pitch(self):
        return self._pitch

    @property
    def pos(self):
        return (self._x, self._y, self._z)

    def __eq__(self, other):
        return self._x == other._x and \
               self._y == other._y and \
               self._z == other._z and \
               self._yaw == other._yaw and \
               self._pitch == other._pitch


    @classmethod
    def from_observation(cls, observation:dict):
        """
        Takes observations

        :param observation:
        :return:
        """
        if not u'XPos' in observation or \
                not u'YPos' in observation or \
                not u'ZPos' in observation or \
                not u'Pitch' in observation or \
                not u'Yaw' in observation:
            logger.error("Incomplete observation received: %s")
            return  cls(None, None, None, None, None)

        return cls(
            x=observation[u'XPos'],
            y=observation[u'YPos'],
            z=observation[u'ZPos'],
            yaw=observation[u'Yaw'],
            pitch=observation[u'Pitch'],
        )

    def update(self, observation:dict):
        """
        Updates the position information

        :param observation:
        :return:
        """
        if not observation:
            return self

        if not u'XPos' in observation or \
                not u'YPos' in observation or \
                not u'ZPos' in observation or \
                not u'Pitch' in observation or \
                not u'Yaw' in observation:
            logger.error("Incomplete observation received: %s")


        self._x=observation[u'XPos']
        self._y=observation[u'YPos']
        self._z=observation[u'ZPos']
        self._yaw=observation[u'Yaw']
        self._pitch=observation[u'Pitch']

        return self




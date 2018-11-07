import common.malmo.binding as malmo_types


def build_element(element, **kwargs):
    """
    This is a wrapper to allow kwarg assignment of XML elements.

    :param element:
    :param kwargs:
    :return:
    """
    obj = element()
    for key, value in kwargs.items():
        obj.__setattr__(key, value)
    return obj


def DrawDoor(x: int, y: int, z: int, type: malmo_types.BlockType = malmo_types.BlockType.wooden_door):
    """
    Draws a Door, where x,y,z specifies the bottom of the door.

    :param x:
    :param y:
    :param z:
    :param type:
    :return:
    """

    bottom = build_element(malmo_types.DrawBlock,
                           type=type,
                           variant=malmo_types.HalfTypes.lower,
                           x=x,
                           y=y,
                           z=z)

    top = build_element(malmo_types.DrawBlock,
                        type=type,
                        variant=malmo_types.HalfTypes.upper,
                        x=x,
                        y=y + 1,
                        z=z)

    return [bottom, top]

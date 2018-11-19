from enum import Enum


class ExperimentStatus(Enum):
    PENDING = 1
    RUNNING = 2
    COMPLETED = 3
    FAILED = 4

class ClientStatus(Enum):
    AVALIABLE = 1
    FAILED = 2
    OCCUPIED = 3

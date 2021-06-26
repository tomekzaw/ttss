from enum import Enum


class Status(Enum):
    PREDICTED = 'PREDICTED'
    PLANNED = 'PLANNED'
    STOPPING = 'STOPPING'
    DEPARTED = 'DEPARTED'

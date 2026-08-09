from .state import State
from enum import Enum, auto


class Direction(Enum):
    NORDEN = auto()
    WESTEN = auto()
    OSTEN = auto()
    SUEDEN = auto()

    def __str__(self):
        return self.name.title()


class Agent:

    def __init__(
        self, x: float, y: float, direction: Direction, speed: float, state: State
    ) -> None:
        self.x = x
        self.y = y
        self.direction = direction
        self.speed = speed
        self.state = state

from enum import Enum, auto


class State(Enum):
    GESUND = auto()
    KRANK = auto()
    IMMUN = auto()

    def __str__(self):
        return self.name.title()

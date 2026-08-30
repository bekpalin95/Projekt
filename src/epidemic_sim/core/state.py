from enum import Enum, auto


class State(Enum):
    GESUND = auto()
    KRANK = auto()
    GENESEN = auto()

    def __str__(self) -> str:
        return self.name.title()

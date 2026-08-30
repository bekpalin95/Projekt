"""
Dieses Modul enthält die Kernlogik der Epidemie-Simulation.
"""

from enum import Enum, auto


class State(Enum):
    """Gesundheitsstatus der Agenten"""

    GESUND = auto()
    KRANK = auto()
    GENESEN = auto()

    def __str__(self) -> str:
        """str representation"""
        return self.name.title()

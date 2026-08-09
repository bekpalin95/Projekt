# from ..viz.renderer import game_loop
from .agent import Agent
from ..config import SimulationConfig
from .state import State

import numpy


class Simulation:
    def __init__(self, config: SimulationConfig) -> None:
        self.config = config
        self.rng = numpy.random.default_rng(config.seed)
        self._agents = self._create_agents()

    def _create_agents(self) -> list[Agent]:
        agents = []
        for _ in range(self.config.n_agents):
            x_pos = self.rng.uniform(0, self.config.field_width)
            y_pos = self.rng.uniform(0, self.config.field_height)

            direction = self.rng.uniform(0, 360)

            agents.append(
                Agent(x_pos, y_pos, direction, self.config.agent_speed, State.GESUND)
            )

        for i in range(self.config.n_infizierte):
            agents[i].state = State.KRANK

        return agents

    # ein Tick
    def step(self) -> None:
        for agent in self._agents:
            agent.move(self.config.field_width, self.config.field_height)

    @property
    def agents(self) -> list[Agent]:
        return self._agents

    def counts(self) -> tuple[int, int, int]:  # (S, I, R) für den Invarianten-Test
        pass

    @property
    def get_field_width(self) -> float:
        return self.config.field_width

    @property
    def get_field_height(self) -> float:
        return self.config.field_height


if __name__ == "__main__":
    pass

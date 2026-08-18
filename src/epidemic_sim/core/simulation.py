# from ..viz.renderer import game_loop
from .agent import Agent
from ..config import SimulationConfig
from .state import State
import math

import numpy


class Simulation:
    def __init__(self, config: SimulationConfig) -> None:
        self.config = config
        self.rng = numpy.random.default_rng(config.seed)
        self._agents = self._create_agents()

        self.n_gesund = config.n_agents - config.n_infizierte
        self.n_krank = config.n_infizierte
        self.n_genesen = 0

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
        grid_size = 5
        grid = self._build_grid(size=grid_size)

        # Gesunde vermeiden Infizierte
        for agent in self._agents:
            if agent.state != State.GESUND:
                continue

            nachbarn = self._get_nachbarn(
                grid, agent.x // grid_size, agent.y // grid_size
            )
            infiizierte_nachbarn = [
                nachbar for nachbar in nachbarn if nachbar.state == State.KRANK
            ]

            if infiizierte_nachbarn:
                agent.calculate_escape_direction(infiizierte_nachbarn)

        # Infektion
        for infizierter in self._agents:
            if infizierter.state != State.KRANK:
                continue

            block_x, block_y = infizierter.x // grid_size, infizierter.y // grid_size

            nachbarn = self._get_nachbarn(grid, block_x, block_y)

            for nachbar in nachbarn:
                if nachbar.state != State.GESUND:
                    continue

                distanz = math.dist(
                    [nachbar.x, nachbar.y], [infizierter.x, infizierter.y]
                )

                if (
                    distanz <= self.config.infection_radius
                    and numpy.random.random() <= self.config.infection_chance
                ):
                    nachbar.change_state(State.KRANK)
                    self.n_gesund -= 1
                    self.n_krank += 1

        # Bewegung
        for agent in self._agents:
            agent.move(self.config.field_width, self.config.field_height)

    @property
    def agents(self) -> list[Agent]:
        return self._agents

    def _build_grid(self, size: int = 5) -> dict[tuple[int, int], list[Agent]]:
        grid = {}
        for x in range(self.config.field_width // size):
            for y in range(self.config.field_height // size):
                grid[(x, y)] = []

        for agent in self.agents:
            grid[(agent.x // size, agent.y // size)].append(agent)

        return grid

    def _get_nachbarn(self, grid: dict, block_x: int, block_y: int) -> list[Agent]:
        nachbarn = []
        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                zelle_key = (block_x + dx, block_y + dy)
                nachbarn.extend(grid.get(zelle_key, []))

        return nachbarn

    def counts(
        self,
    ) -> tuple[int, int, int]:  # (Gesund, Krank, Genesen) für den Invarianten-Test
        return self.n_gesund, self.n_krank, self.n_genesen

    @property
    def get_field_width(self) -> float:
        return self.config.field_width

    @property
    def get_field_height(self) -> float:
        return self.config.field_height


if __name__ == "__main__":
    pass

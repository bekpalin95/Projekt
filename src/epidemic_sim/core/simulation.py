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

        self._n_gesund = config.n_agents - config.n_infizierte
        self._n_krank = config.n_infizierte
        self._n_genesen = 0
        self.history = []

    def _create_agents(self) -> list[Agent]:
        agents = []
        for _ in range(self.config.n_agents):
            x_pos = self.rng.uniform(0, self.config.field_width)
            y_pos = self.rng.uniform(0, self.config.field_height)

            direction = self.rng.uniform(0, 360)

            agents.append(
                Agent(
                    x_pos,
                    y_pos,
                    direction,
                    self.config.gesunder_agent_speed,
                    State.GESUND,
                    self.config.recovery_duration,
                )
            )

        for i in range(self.config.n_infizierte):
            agents[i].change_state(State.KRANK, self.config)

        return agents

    # ein Tick
    def step(self) -> None:
        grid_size = 5
        grid = self._build_grid(size=grid_size)

        # Gesunde vermeiden Infizierte
        for agent in self._agents:
            if agent.state != State.GESUND:
                continue

            nachbarn = agent.get_nachbarn(grid, grid_size)

            infiizierte_nachbarn = [
                nachbar for nachbar in nachbarn if nachbar.state == State.KRANK
            ]

            agent.calculate_escape_direction(infiizierte_nachbarn)

        # Infektion und Genesung
        for infizierter in self._agents:
            if infizierter.state != State.KRANK:
                continue

            if infizierter.is_genesen():
                infizierter.change_state(State.GENESEN, self.config)
                self._n_genesen += 1
                self._n_krank -= 1
                continue

            nachbarn = infizierter.get_nachbarn(grid, grid_size)

            for nachbar in nachbarn:
                if nachbar.state != State.GESUND:
                    continue

                distanz = math.dist(
                    [nachbar.x, nachbar.y], [infizierter.x, infizierter.y]
                )

                if (
                    distanz <= self.config.infection_radius
                    and self.rng.random() <= self.config.infection_chance
                ):
                    nachbar.change_state(State.KRANK, self.config)
                    self._n_gesund -= 1
                    self._n_krank += 1

        # Bewegung
        for agent in self._agents:
            agent.move(self.config.field_width, self.config.field_height)

        # History für den Plot am Ende
        self.history.append(self.counts())

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

    def counts(
        self,
    ) -> tuple[int, int, int]:  # (Gesund, Krank, Genesen) für den Invarianten-Test
        return self._n_gesund, self._n_krank, self._n_genesen

    def inf_follow_mouse(self, mouse_x: float, mouse_y: float) -> None:
        for agent in self.agents:
            if agent.state == State.KRANK:
                agent.move_to_cords(mouse_x, mouse_y)

    @property
    def get_field_width(self) -> float:
        return self.config.field_width

    @property
    def get_field_height(self) -> float:
        return self.config.field_height


if __name__ == "__main__":
    pass

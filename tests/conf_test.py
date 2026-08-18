from epidemic_sim.core import Agent, Simulation, State
from epidemic_sim import SimulationConfig
import pytest


def test_grid_building():
    conf = SimulationConfig(field_width=200, field_height=200)
    sim = Simulation(conf)

    sim._agents = [
        Agent(0, 0, 260, 1, None),
        Agent(50, 199.9, 260, 1, None),
        Agent(9, 9, 260, 1, None),
        Agent(55, 199.9, 260, 1, None),
        Agent(40, 40, 260, 1, None),
    ]

    grid = sim._build_grid(size=10)

    assert len(grid[(0, 0)]) == 2
    assert len(grid[(5, 19)]) == 2
    assert len(grid[(4, 4)]) == 1
    assert len(grid[(1, 1)]) == 0

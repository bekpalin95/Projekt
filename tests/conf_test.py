from epidemic_sim.core import Agent, Simulation, State
from epidemic_sim import SimulationConfig
from .config_builder import make_config
import pytest


def test_grid_building():
    config = make_config(field_width=200, field_height=200)
    sim = Simulation(config)

    sim._agents = [
        Agent(0, 0, 260, 1, None, 1),
        Agent(50, 199.9, 260, 1, None, 1),
        Agent(9, 9, 260, 1, None, 1),
        Agent(55, 199.9, 260, 1, None, 1),
        Agent(40, 40, 260, 1, None, 1),
    ]

    grid = sim._build_grid(size=10)

    assert len(grid[(0, 0)]) == 2
    assert len(grid[(5, 19)]) == 2
    assert len(grid[(4, 4)]) == 1
    assert len(grid[(1, 1)]) == 0

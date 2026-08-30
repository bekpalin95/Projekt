from epidemic_sim.core import Agent, Simulation
from argparse import Namespace
from .config_builder import make_config
import pytest
from epidemic_sim.config import SimulationConfig


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


def test_n_infizierte_groesser_als_n_agents_wirft_error():
    args = Namespace(
        n_agents=10,
        n_infizierte=50,
        infection_chance=None,
        infection_radius=None,
        recovery_duration=None,
        agent_speed=None,
        field_width=None,
        field_height=None,
        seed=None,
        lockdown_threshold=None,
        lockdown_infection_radius=None,
    )
    with pytest.raises(ValueError):
        SimulationConfig(args)

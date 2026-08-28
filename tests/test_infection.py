import pytest

from epidemic_sim.core import Agent, Simulation, State
from .config_builder import make_config


def test_infection_happens_when_close_and_certain():
    """Bei Chance=1.0 und Distanz innerhalb r muss die Infektion garantiert passieren."""
    config = make_config(
        field_width=200, field_height=200, infection_radius=5, infection_chance=1.0
    )
    sim = Simulation(config)

    krank = Agent(x=0, y=0, direction=0, speed=0, state=State.KRANK, recovery_time=1000)
    gesund = Agent(
        x=1, y=0, direction=0, speed=0, state=State.GESUND, recovery_time=1000
    )
    sim._agents = [krank, gesund]
    sim._n_gesund, sim._n_krank, sim._n_genesen = 1, 1, 0

    sim.step()

    assert gesund.state == State.KRANK


def test_no_infection_when_out_of_radius():
    """Weit entfernte Agenten (auch in anderen Grid-Zellen) dürfen nicht infizieren."""
    config = make_config(
        field_width=200, field_height=200, infection_radius=1, infection_chance=1.0
    )
    sim = Simulation(config)

    krank = Agent(x=0, y=0, direction=0, speed=0, state=State.KRANK, recovery_time=1000)
    gesund = Agent(
        x=100, y=100, direction=0, speed=0, state=State.GESUND, recovery_time=1000
    )
    sim._agents = [krank, gesund]
    sim._n_gesund, sim._n_krank, sim._n_genesen = 1, 1, 0

    sim.step()

    assert gesund.state == State.GESUND


def test_no_infection_when_chance_zero():
    """Selbst in unmittelbarer Nähe darf bei Chance=0.0 keine Infektion passieren."""
    config = make_config(
        field_width=200,
        field_height=200,
        infection_radius=5,
        infection_chance=0.0,
        seed=42,
    )
    sim = Simulation(config)

    krank = Agent(x=0, y=0, direction=0, speed=0, state=State.KRANK, recovery_time=1000)
    gesund = Agent(
        x=1, y=0, direction=0, speed=0, state=State.GESUND, recovery_time=1000
    )
    sim._agents = [krank, gesund]
    sim._n_gesund, sim._n_krank, sim._n_genesen = 1, 1, 0

    sim.step()

    assert gesund.state == State.GESUND


def test_same_seed_gives_identical_history():
    """gleicher Seed -> identischer Verlauf"""
    config_a = make_config(n_agents=30, n_infizierte=5, seed=7)
    config_b = make_config(n_agents=30, n_infizierte=5, seed=7)
    sim_a = Simulation(config_a)
    sim_b = Simulation(config_b)

    for _ in range(1000):
        sim_a.step()
        sim_b.step()

    assert sim_a.history == sim_b.history

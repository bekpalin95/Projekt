from epidemic_sim.core import Agent, Simulation, State

from .config_builder import make_config


def test_lockdown_inactive_below_threshold():
    config = make_config(lockdown_threshold=10)
    sim = Simulation(config)
    sim._n_krank = 9

    assert sim.lockdown_aktiv is False


def test_lockdown_active_at_threshold():
    config = make_config(lockdown_threshold=10)
    sim = Simulation(config)
    sim._n_krank = 10

    assert sim.lockdown_aktiv is True


def test_lockdown_active_above_threshold():
    config = make_config(lockdown_threshold=10)
    sim = Simulation(config)
    sim._n_krank = 15

    assert sim.lockdown_aktiv is True


def test_infection_radius_reduced_during_lockdown():
    """Außerhalb des reduzierten, aber innerhalb des normalen Radius:
    Infektion darf im Lockdown NICHT passieren, ohne Lockdown SCHON."""
    config = make_config(
        field_width=200,
        field_height=200,
        infection_radius=5,
        lockdown_infection_radius=0.5,
        infection_chance=1.0,
        lockdown_threshold=1,
    )
    sim = Simulation(config)

    krank = Agent(x=0, y=0, direction=0, speed=0, state=State.KRANK, recovery_time=1000)
    gesund = Agent(
        x=2, y=0, direction=0, speed=0, state=State.GESUND, recovery_time=1000
    )
    sim._agents = [krank, gesund]
    sim._n_gesund, sim._n_krank, sim._n_genesen = 1, 1, 0

    # lockdown_threshold=1, n_krank=1 -> Lockdown ist aktiv
    assert sim.lockdown_aktiv is True

    sim.step()

    # Distanz 2 liegt zwischen lockdown_radius (0.5) und normalem radius (5)
    assert gesund.state == State.GESUND


def test_escape_behavior_only_during_lockdown():
    """Ausweichverhalten darf nur greifen, wenn Lockdown aktiv ist."""
    config = make_config(
        field_width=200,
        field_height=200,
        lockdown_threshold=100,
        infection_chance=0.0,
    )
    sim = Simulation(config)

    gesund = Agent(x=5, y=5, direction=0, speed=1, state=State.GESUND, recovery_time=1)
    krank = Agent(x=6, y=5, direction=0, speed=0, state=State.KRANK, recovery_time=1000)
    sim._agents = [gesund, krank]
    sim._n_gesund, sim._n_krank, sim._n_genesen = 1, 1, 0

    original_direction = gesund.direction
    sim.step()

    # Lockdown NICHT aktiv (n_krank=1 < threshold=100) -> Richtung bleibt unverändert
    assert gesund.direction == original_direction

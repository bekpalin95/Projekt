import pytest

from epidemic_sim.core import Agent, State
from .config_builder import make_config


def test_agent_recovers_after_recovery_duration():
    """is_genesen() muss erst nach genau recovery_time Aufrufen True liefern."""
    agent = Agent(x=0, y=0, direction=0, speed=0, state=State.KRANK, recovery_time=3)

    for _ in range(3):
        assert agent.is_genesen() is False

    assert agent.is_genesen() is True


def test_change_state_updates_speed():
    config = make_config()
    agent = Agent(
        x=0,
        y=0,
        direction=0,
        speed=config.gesunder_agent_speed,
        state=State.GESUND,
        recovery_time=1,
    )

    agent.change_state(State.KRANK, config)
    assert agent.state == State.KRANK
    assert agent.speed == config.kranker_agent_speed

    agent.change_state(State.GENESEN, config)
    assert agent.state == State.GENESEN
    assert agent.speed == config.gesunder_agent_speed


def test_calculate_escape_direction_points_away_from_infected():
    gesund = Agent(x=5, y=5, direction=0, speed=1, state=State.GESUND, recovery_time=1)
    krank = Agent(x=10, y=5, direction=0, speed=0, state=State.KRANK, recovery_time=1)

    gesund.calculate_escape_direction([krank])

    # Infizierter liegt rechts von Gesundem -> Flucht nach links (180 Grad)
    assert gesund.direction == pytest.approx(180.0)


def test_move_to_cords_points_towards_target():
    agent = Agent(x=0, y=0, direction=0, speed=1, state=State.GESUND, recovery_time=1)

    agent.move_to_cords(10, 0)
    assert agent.direction == pytest.approx(0.0)

    agent.move_to_cords(0, 10)
    assert agent.direction == pytest.approx(90.0)

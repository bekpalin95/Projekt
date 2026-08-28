from epidemic_sim.core import Agent, Simulation, State
from epidemic_sim import SimulationConfig
import pytest


def test_move_ohne_wandberuehrung():
    agent = Agent(x=0, y=0, direction=0, speed=1, state=State.GESUND, recovery_time=1)

    agent.move(100.0, 100.0)

    assert agent.x == pytest.approx(1.0)
    assert agent.y == pytest.approx(0.0)


def test_move_ohne_wandberuehrung_2():
    agent = Agent(x=0, y=0, direction=90, speed=1, state=State.GESUND, recovery_time=1)

    agent.move(100.0, 100.0)

    assert agent.x == pytest.approx(0.0)
    assert agent.y == pytest.approx(1.0)


def test_move_wandberuehrung():
    agent = Agent(x=1, y=0, direction=0, speed=1, state=State.GESUND, recovery_time=1)

    assert agent.x == pytest.approx(1.0)

    agent.move(1.0, 100.0)

    assert agent.x == pytest.approx(0.0) and agent.y == pytest.approx(0.0)
    assert agent.direction == pytest.approx(180)


def test_move_in_die_ecke():
    agent = Agent(
        x=100, y=100, direction=45, speed=1, state=State.GESUND, recovery_time=1
    )

    agent.move(100, 100)

    assert agent.x < 100 and agent.y < 100
    assert agent.direction == pytest.approx(225)


def test_agent_bleibt_im_feld():
    agent = Agent(x=0, y=0, direction=67, speed=13, state=State.GESUND, recovery_time=1)

    for _ in range(1000):
        agent.move(30, 30)
        assert agent.x >= 0 and agent.x <= 30
        assert agent.y >= 0 and agent.y <= 30

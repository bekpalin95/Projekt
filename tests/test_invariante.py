from epidemic_sim.core import Agent, Simulation, State
from epidemic_sim import SimulationConfig
from .config_builder import make_config


def test_population_invariant_holds_over_time():
    config = make_config(n_agents=50, n_infizierte=5, seed=1)
    simulation = Simulation(config)

    for _ in range(10000):
        simulation.step()
        gesund, krank, genesen = simulation.counts()
        assert gesund + krank + genesen == config.n_agents

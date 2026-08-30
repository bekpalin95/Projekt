from epidemic_sim.core import Simulation, State

from .config_builder import make_config


def test_population_invariant_holds_over_time():
    config = make_config(n_agents=50, n_infizierte=5, seed=1)
    simulation = Simulation(config)

    for _ in range(10000):
        simulation.step()
        gesund, krank, genesen = simulation.counts()
        assert gesund + krank + genesen == config.n_agents


def test_counts_matches_actual_agent_states():
    config = make_config(n_agents=40, n_infizierte=8, seed=3)
    sim = Simulation(config)

    for _ in range(300):
        sim.step()
        gesund, krank, genesen = sim.counts()
        tatsaechlich_gesund = sum(1 for a in sim.agents if a.state == State.GESUND)
        tatsaechlich_krank = sum(1 for a in sim.agents if a.state == State.KRANK)
        tatsaechlich_genesen = sum(1 for a in sim.agents if a.state == State.GENESEN)

        assert gesund == tatsaechlich_gesund
        assert krank == tatsaechlich_krank
        assert genesen == tatsaechlich_genesen

from epidemic_sim.core import Simulation

from .config_builder import make_config


def test_kurvenverlauf_ist_plausibel():
    """S monoton fallend, R monoton steigend, I steigt und faellt zurueck auf 0."""
    config = make_config(n_agents=100, n_infizierte=5, seed=1)
    sim = Simulation(config)

    max_ticks = 20000
    ticks = 0
    while sim.counts()[1] > 0 and ticks < max_ticks:
        sim.step()
        ticks += 1

    assert ticks < max_ticks, "Simulation hat n_krank=0 nicht erreicht"

    gesund_verlauf = [eintrag[0] for eintrag in sim.history]
    krank_verlauf = [eintrag[1] for eintrag in sim.history]
    genesen_verlauf = [eintrag[2] for eintrag in sim.history]

    # S monoton fallend: darf nie ansteigen
    assert all(
        gesund_verlauf[i] >= gesund_verlauf[i + 1]
        for i in range(len(gesund_verlauf) - 1)
    )

    # R monoton steigend: darf nie sinken
    assert all(
        genesen_verlauf[i] <= genesen_verlauf[i + 1]
        for i in range(len(genesen_verlauf) - 1)
    )

    # I endet bei 0
    assert krank_verlauf[-1] == 0

    # I steigt zuerst an (Peak > Startwert), bevor es zurückgeht
    assert max(krank_verlauf) > krank_verlauf[0]

"""Batch-Modus: Parameter-Sweep, mehrere Szenarien ohne Visualisierung"""

import argparse
from argparse import Namespace

import matplotlib.pyplot as plt

from .config import SimulationConfig
from .core import Simulation


def args_parser() -> argparse.Namespace:
    """parses args"""
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--infection_chance_values",
        type=float,
        nargs="+",
        required=True,
        help="Liste von infection_chance-Werten, z.B. 0.05 0.1 0.2 0.3",
    )
    parser.add_argument(
        "--n_agents", type=int, required=False, help="Gesamtanzahl Agenten"
    )
    parser.add_argument(
        "--n_infizierte", type=int, required=False, help="Anzahl Infizierter"
    )
    parser.add_argument(
        "--infection_radius", type=float, required=False, help="Radius der Infektion"
    )
    parser.add_argument(
        "--recovery_duration", type=int, required=False, help="Recovery Duration"
    )
    parser.add_argument(
        "--agent_speed", type=float, required=False, help="Bewegungsgeschwindigkeit"
    )
    parser.add_argument(
        "--field_width", type=int, required=False, help="Breite des Feldes"
    )
    parser.add_argument(
        "--field_height", type=int, required=False, help="Höhe des Feldes"
    )
    parser.add_argument(
        "--seed", type=int, required=False, help="Seed des Zufallsgenerators"
    )
    parser.add_argument(
        "--lockdown_threshold",
        type=int,
        required=False,
        help="Schwellwert für Lockdown",
    )
    parser.add_argument(
        "--lockdown_infection_radius",
        type=float,
        required=False,
        help="Reduzierter Radius im Lockdown",
    )
    parser.add_argument(
        "--max_ticks",
        type=int,
        required=False,
        default=50000,
        help="Sicherheitslimit an Ticks pro Szenario",
    )
    return parser.parse_args()


def run_scenario(
    base_args: Namespace, infection_chance: float, max_ticks: int
) -> list[tuple[int, int, int]]:
    """Führt ein einzelnes Szenario bis n_krank == 0 (oder max_ticks) aus."""
    args_dict = vars(base_args).copy()
    args_dict["infection_chance"] = infection_chance
    args_dict.pop("infection_chance_values", None)
    args_dict.pop("max_ticks", None)

    try:
        config = SimulationConfig(Namespace(**args_dict))
    except ValueError as e:
        print(f"Ungültige Eingabe: {e}")
        raise SystemExit(1)

    simulation = Simulation(config)

    ticks = 0
    while simulation.counts()[1] > 0 and ticks < max_ticks:
        simulation.step()
        ticks += 1

    if ticks >= max_ticks:
        print(
            f"Warnung: infection_chance={infection_chance} hat max_ticks erreicht, ohne n_krank=0 zu erreichen."
        )

    return simulation.history


def plot_sweep(results: dict[float, list[tuple[int, int, int]]]) -> None:
    """Zeigt die I-Kurve (Infizierte über Zeit) für jedes Szenario in einem Plot."""
    _, ax = plt.subplots(figsize=(10, 6))

    for infection_chance, history in results.items():
        krank_verlauf = [eintrag[1] for eintrag in history]
        ax.plot(range(len(history)), krank_verlauf, label=f"chance={infection_chance}")

    ax.set_xlabel("Zeitschritt")
    ax.set_ylabel("Anzahl Infizierter")
    ax.set_title("Parameter-Sweep: infection_chance")
    ax.legend()
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.show()


if __name__ == "__main__":
    args = args_parser()

    results = {}
    for chance in args.infection_chance_values:
        print(f"Simuliere infection_chance={chance} ...")
        results[chance] = run_scenario(args, chance, args.max_ticks)

    plot_sweep(results)

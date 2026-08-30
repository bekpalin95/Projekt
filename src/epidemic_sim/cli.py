"""cli für die Simulation"""

import argparse

from .config import SimulationConfig
from .core import Simulation, export_history_csv
from .viz import game_loop, plot_history


def args_parser() -> argparse.Namespace:
    """parses args"""
    parser = argparse.ArgumentParser()

    parser.add_argument(
        "--n_agents", type=int, required=False, help="Gesamtanzahl Agenten"
    )
    parser.add_argument(
        "--n_infizierte", type=int, required=False, help="Anzahl Infizierter"
    )
    parser.add_argument(
        "--infection_chance", type=float, required=False, help="Chance der Infektion"
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
        "--lockdown_threshold", type=int, required=False, help="lockdown threshold"
    )
    parser.add_argument(
        "--lockdown_infection_radius", type=int, required=False, help=""
    )

    parser.add_argument(
        "--export_csv",
        type=str,
        required=False,
        help="Pfad, unter dem die S/I/R-Zeitreihe als CSV gespeichert wird",
    )

    return parser.parse_args()


if __name__ == "__main__":
    args = args_parser()

    config = SimulationConfig(args)

    simulation = Simulation(config)

    game_loop(simulation)

    plot_history(simulation.history)

    if (
        args.export_csv
    ):  # Beispielaufruf: uv run python -m epidemic_sim.cli --export_csv ergebnis.csv
        export_history_csv(simulation.history, args.export_csv)
        print(f"Zeitreihe gespeichert unter: {args.export_csv}")

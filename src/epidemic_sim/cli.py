from .core import Simulation
from .config import SimulationConfig
from .viz import game_loop, plot_history
import argparse


def args_parser() -> argparse.Namespace:
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

    return parser.parse_args()


if __name__ == "__main__":
    args = args_parser()

    config = SimulationConfig(args)

    simulation = Simulation(config)

    game_loop(simulation)

    plot_history(simulation.history)

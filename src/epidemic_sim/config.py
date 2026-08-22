from dataclasses import dataclass
from argparse import Namespace


@dataclass
class SimulationConfig:

    # Populationsgröße
    n_agents: int = 1000
    n_infizierte: int = 10

    assert n_infizierte <= n_agents

    # Infektionseigenschaften
    infection_chance: float = 0.05
    infection_radius: float = 2.0  # Meter
    recovery_duration: int = 100

    # Bewegung
    agent_speed: float = 0.2

    # Raum
    field_width: int = 200
    field_height: int = 200

    # Reproduzierbarkeit
    seed: int = 42

    def __init__(self, args: Namespace):
        if args.n_agents:
            self.n_agents = args.n_agents

        if args.n_infizierte:
            assert args.n_infizierte <= self.n_agents
            self.n_infizierte = args.n_infizierte

        if args.infection_chance:
            self.infection_chance = args.infection_chance

        if args.infection_radius:
            self.infection_radius = args.infection_radius

        if args.recovery_duration:
            self.recovery_duration = args.recovery_duration

        if args.agent_speed:
            self.agent_speed = args.agent_speed

        if args.field_width:
            self.field_width = args.field_width

        if args.field_height:
            self.field_height = args.field_height

        if args.seed:
            self.seed = args.seed

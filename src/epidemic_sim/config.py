"""Config"""

from argparse import Namespace
from dataclasses import dataclass


@dataclass
class SimulationConfig:
    """Config für die Simulation"""

    # Populationsgröße
    n_agents: int = 1000
    n_infizierte: int = 10

    assert n_infizierte <= n_agents

    # Infektionseigenschaften
    infection_chance: float = 0.05
    infection_radius: float = 1.5  # Meter
    recovery_duration: int = 3000

    # Bewegung
    krank_boost = 0.04
    gesunder_agent_speed: float = 0.2
    kranker_agent_speed: float = gesunder_agent_speed + krank_boost

    # Raum
    field_width: int = 200
    field_height: int = 200

    # Reproduzierbarkeit
    seed: int = 42

    # Lockdown
    lockdown_threshold: float = n_agents * 0.2  # 20% der Agenten
    lockdown_infection_radius: float = infection_radius - 0.5

    def __init__(self, args: Namespace):
        """Initialisierung mit Usereingaben"""
        if args.n_agents:
            self.n_agents = args.n_agents

        if args.n_infizierte:
            if args.n_infizierte > self.n_agents:
                raise ValueError(
                    f"n_infizierte ({args.n_infizierte}) darf nicht größer als "
                    f"n_agents ({self.n_agents}) sein."
                )
            self.n_infizierte = args.n_infizierte

        if args.infection_chance:
            self.infection_chance = args.infection_chance

        if args.infection_radius:
            self.infection_radius = args.infection_radius

        if args.recovery_duration:
            self.recovery_duration = args.recovery_duration

        if args.agent_speed:
            self.gesunder_agent_speed = args.agent_speed
            self.kranker_agent_speed = self.gesunder_agent_speed + self.krank_boost

        if args.field_width:
            self.field_width = args.field_width

        if args.field_height:
            self.field_height = args.field_height

        if args.seed:
            self.seed = args.seed

        self.lockdown_threshold = self.n_agents * 0.2
        self.lockdown_infection_radius = self.infection_radius - 0.5

        if args.lockdown_threshold:
            self.lockdown_threshold = args.lockdown_threshold

        if args.lockdown_infection_radius:
            self.lockdown_infection_radius = args.lockdown_infection_radius

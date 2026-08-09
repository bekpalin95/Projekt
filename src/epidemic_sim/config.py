from dataclasses import dataclass


@dataclass
class SimulationConfig:

    # Populationsgröße
    n_agents: int = 120
    n_infizierte: int = 10

    assert n_infizierte <= n_agents

    # Infektionseigenschaften
    infection_chance: float = 0.05
    infection_radius: float = 2.0  # Meter
    recovery_duration: int = 100

    # Bewegung
    agent_speed: float = 1.0

    # Raum
    field_width: int = 200
    field_height: int = 200

    # Reproduzierbarkeit
    seed: int = 42

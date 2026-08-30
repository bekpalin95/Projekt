from argparse import Namespace

from epidemic_sim import SimulationConfig


def make_config(**overrides) -> SimulationConfig:
    """Baut eine SimulationConfig mit Test-Defaults, überschreibbar per Keyword."""
    defaults = {
        "n_agents": None,
        "n_infizierte": None,
        "infection_chance": None,
        "infection_radius": None,
        "recovery_duration": None,
        "agent_speed": None,
        "field_width": None,
        "field_height": None,
        "seed": None,
        "lockdown_threshold": None,
        "lockdown_infection_radius": None,
    }
    defaults.update(overrides)
    return SimulationConfig(Namespace(**defaults))

from .core import Simulation
from .config import SimulationConfig
from .viz import game_loop

if __name__ == "__main__":
    config = SimulationConfig()

    simulation = Simulation(config)

    game_loop(simulation)

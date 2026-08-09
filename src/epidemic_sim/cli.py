from .core.simulation import Simulation
from .config import SimulationConfig
from .viz.renderer import game_loop

if __name__ == "__main__":
    config = SimulationConfig()

    simulation = Simulation(config)

    game_loop(simulation)

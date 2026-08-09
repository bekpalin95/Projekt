import pygame
from ..core import Simulation, State

_RGB_MAPPER = {
    State.GESUND: (255, 255, 255),
    State.KRANK: (255, 0, 0),
    State.IMMUN: (60, 226, 0),
}

WIDTH = 800
HEIGHT = 600


def _size_skaliert(field_width: float, field_height: float) -> tuple[float, float]:
    return WIDTH / field_width, HEIGHT / field_height


def game_loop(simulation: Simulation) -> None:
    pygame.init()

    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    clock = pygame.time.Clock()

    running = True

    while running:
        # 1. INPUT EVENT PROCESSING
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        screen.fill((30, 30, 30))

        agents = simulation.agents

        width_skal, height_skal = _size_skaliert(
            simulation.get_field_width, simulation.get_field_height
        )

        for agent in agents:
            pygame.draw.circle(
                screen,
                _RGB_MAPPER[agent.state],
                (width_skal * agent.x, height_skal * agent.y),
                2,
            )

        pygame.display.flip()

        simulation.step()

    pygame.quit()

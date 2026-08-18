import pygame
from ..core import Simulation, State
import os
from pathlib import Path

path = Path(__file__).parent


_RGB_MAPPER = {
    State.GESUND: (255, 255, 255),
    State.KRANK: (255, 0, 0),
    State.IMMUN: (60, 226, 0),
}

clock = pygame.time.Clock()

WIDTH = 800
HEIGHT = 600


def _size_skaliert(field_width: float, field_height: float) -> tuple[float, float]:
    return WIDTH / field_width, HEIGHT / field_height


def show_text(screen, font, text, center_x, y):
    surface = font.render(text, True, (182, 143, 64))
    rect = surface.get_rect()

    rect.centerx = center_x
    rect.y = y

    screen.blit(surface, rect)


def game_loop(simulation: Simulation) -> None:
    pygame.init()

    screen = pygame.display.set_mode((WIDTH, HEIGHT))

    clock = pygame.time.Clock()

    running = True

    font = pygame.font.Font(path / "ressources" / "font.ttf", 12)

    while running:
        clock.tick(60)
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

        show_text(
            screen,
            font,
            f"Gesund: {simulation.n_gesund}, Krank: {simulation.n_krank}, Genesen: {simulation.n_genesen}",
            WIDTH // 2,
            20,
        )

        pygame.display.flip()

        simulation.step()

    pygame.quit()

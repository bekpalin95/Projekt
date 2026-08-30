import pygame
from ..core import Simulation, State
import os
from pathlib import Path

path = Path(__file__).parent


_RGB_MAPPER = {
    State.GESUND: (255, 255, 255),
    State.KRANK: (255, 0, 0),
    State.GENESEN: (60, 226, 0),
}

clock = pygame.time.Clock()

WIDTH = 800
HEIGHT = 600


def _size_skaliert(field_width: float, field_height: float) -> tuple[float, float]:
    return WIDTH / field_width, HEIGHT / field_height


def show_text(
    screen: pygame.Surface, font: pygame.font.Font, text: str, center_x: int, y: int
) -> None:
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

    width_skal, height_skal = _size_skaliert(
        simulation.get_field_width, simulation.get_field_height
    )

    FOLLOW_MODE = False

    TICK_RATES = [60, 120, 240, 480]
    current_tick_rate = 0

    while running:
        clock.tick(TICK_RATES[current_tick_rate])
        # 1. INPUT EVENT PROCESSING
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_f:
                    FOLLOW_MODE = not FOLLOW_MODE
                elif event.key == pygame.K_SPACE:
                    current_tick_rate = (current_tick_rate + 1) % len(TICK_RATES)

        screen.fill((30, 30, 30))

        agents = simulation.agents

        for agent in agents:
            pygame.draw.circle(
                screen,
                _RGB_MAPPER[agent.state],
                (width_skal * agent.x, height_skal * agent.y),
                2,
            )

        count = simulation.counts()  # gesund, krank, genesen

        # ----TEXT ANZEIGEN----
        show_text(screen, font, f"{current_tick_rate+1}x", WIDTH - 30, 20)

        show_text(
            screen,
            font,
            f"Gesund: {count[0]}, Krank: {count[1]}, Genesen: {count[2]}",
            WIDTH // 2,
            20,
        )

        show_text(
            screen,
            font,
            f"Follow Mode: {"ON" if FOLLOW_MODE else "OFF"}",
            WIDTH - 100,
            HEIGHT - 20,
        )

        show_text(
            screen,
            font,
            f"Lockdown: {'ON' if simulation.lockdown_aktiv else 'OFF'}",
            100,
            HEIGHT - 20,
        )

        pygame.display.flip()

        if FOLLOW_MODE:
            mouse_x, mouse_y = (
                pygame.mouse.get_pos()[0] / width_skal,
                pygame.mouse.get_pos()[1] / height_skal,
            )
            simulation.inf_follow_mouse(mouse_x, mouse_y)

        simulation.step()

    pygame.quit()

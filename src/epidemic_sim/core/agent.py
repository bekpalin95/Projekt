from .state import State
from ..config import SimulationConfig
import math


class Agent:
    # Direction als Winkel(0-360)
    def __init__(
        self,
        x: float,
        y: float,
        direction: float,
        speed: float,
        state: State,
        recovery_time: int,
    ) -> None:
        self.x = x
        self.y = y
        self.direction = direction
        self.speed = speed
        self.state = state
        self.recovery_time = recovery_time

        if not (0 <= self.direction <= 360):
            raise ValueError("Direction must be between 0 and 360")

    def move(self, field_width: float, field_height: float) -> None:
        # Winkel von Grad in Bogenmaß (Radians) umwandeln
        winkel_rad = math.radians(self.direction)

        # Neue Koordinaten berechnen
        x_neu = self.x + self.speed * math.cos(winkel_rad)
        y_neu = self.y + self.speed * math.sin(winkel_rad)

        x_neu, y_neu, new_direction = self._check_walls(
            x_neu, y_neu, self.direction, field_width, field_height
        )

        self.x = x_neu
        self.y = y_neu
        self.direction = new_direction

    def calculate_escape_direction(self, infizierte: list["Agent"]) -> None:
        """
        Fluchtvektor berechnen:
        für jeden infizierten Nachbarn einen Vektor berechnen, der von ihm weg zum Gesunden zeigt
        diese Vektoren summieren und die Nähe beachten => Fluchtvektor
        """
        if not infizierte:
            return

        summe_dx = sum(
            (self.x - inf.x) / math.dist([self.x, self.y], [inf.x, inf.y]) ** 2
            for inf in infizierte
        )
        summe_dy = sum(
            (self.y - inf.y) / math.dist([self.x, self.y], [inf.x, inf.y]) ** 2
            for inf in infizierte
        )

        radiant = math.atan2(summe_dy, summe_dx)  # aus dem Vektor den passenden Winkel

        self.direction = math.degrees(radiant)  # aus den Winkel => Grad

    def move_to_cords(self, x: float, y: float) -> None:
        vec_x, vec_y = x - self.x, y - self.y

        radiant = math.atan2(vec_y, vec_x)

        self.direction = math.degrees(radiant)

    def get_nachbarn(
        self, grid: dict[tuple[float, float], list["Agent"]], grid_size: int
    ) -> list["Agent"]:
        nachbarn = []
        block_x, block_y = self.x // grid_size, self.y // grid_size

        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                zelle_key = (block_x + dx, block_y + dy)
                nachbarn.extend(grid.get(zelle_key, []))

        return nachbarn

    def is_genesen(self) -> bool:
        if self.state == State.KRANK and self.recovery_time <= 0:
            return True

        self.recovery_time -= 1
        return False

    def change_state(self, state: State, config: SimulationConfig) -> None:
        if state == State.KRANK:
            self.state = state
            self.speed = config.kranker_agent_speed

        if state == State.GENESEN:
            self.state = state
            self.speed = config.gesunder_agent_speed

    def _check_walls(
        self,
        x: float,
        y: float,
        direction: float,
        field_width: float,
        field_height: float,
    ) -> tuple[float, float, float]:
        new_x = x
        new_y = y
        new_dir = direction

        if x < 0 or x > field_width:
            new_dir = (180 - new_dir) % 360
            new_x = self.x + self.speed * math.cos(math.radians(new_dir))

        if y < 0 or y > field_height:
            new_dir = (360 - new_dir) % 360
            new_y = self.y + self.speed * math.sin(math.radians(new_dir))

        return new_x, new_y, new_dir

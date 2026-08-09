from .state import State
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
    ) -> None:
        self.x = x
        self.y = y
        self.direction = direction
        self.speed = speed
        self.state = state

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

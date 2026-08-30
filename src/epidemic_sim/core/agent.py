"""
Dieses Modul enthält die Kernlogik der Epidemie-Simulation.
"""

import math

from ..config import SimulationConfig
from .state import State


class Agent:
    """Repräsentiert einen einzelnen Akteur in der Simulation.

    Verwaltet die Position, Bewegung, den Gesundheitszustand und die
    Kollisionslogik eines Agenten auf dem Simulationsfeld.
    """

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
        """Initialisiert einen neuen Agenten.

        Args:
            x (float): Die Startposition auf der X-Achse.
            y (float): Die Startposition auf der Y-Achse.
            direction (float): Die Bewegungsrichtung als Winkel in Grad (0 bis 360).
            speed (float): Die Bewegungsgeschwindigkeit pro Schritt.
            state (State): Der anfängliche Gesundheitszustand des Agenten.
            recovery_time (int): Die Anzahl der Simulationsschritte bis zur Genesung.

        Raises:
            ValueError: Wenn die angegebene Richtung nicht zwischen 0 und 360 liegt.
        """
        self.x = x
        self.y = y
        self.direction = direction
        self.speed = speed
        self.state = state
        self.recovery_time = recovery_time

        if not (0 <= self.direction <= 360):
            raise ValueError("Direction must be between 0 and 360")

    def move(self, field_width: float, field_height: float) -> None:
        """Bewegt den Agenten basierend auf seiner Geschwindigkeit und Richtung.

        Berechnet die neue Position mittels trigonometrischer Funktionen und
        korrigiert diese automatisch, falls der Agent den Rand des Spielfelds
        erreicht (Wandkollision).

        Args:
            field_width (float): Die maximale Breite des Simulationsfeldes.
            field_height (float): Die maximale Höhe des Simulationsfeldes.
        """
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
        """Richtet den Agenten auf eine spezifische Zielkoordinate aus.

        Args:
            x (float): Die X-Koordinate des Ziels.
            y (float): Die Y-Koordinate des Ziels.
        """
        vec_x, vec_y = x - self.x, y - self.y

        radiant = math.atan2(vec_y, vec_x)

        self.direction = math.degrees(radiant)

    def get_nachbarn(
        self, grid: dict[tuple[float, float], list["Agent"]], grid_size: int
    ) -> list["Agent"]:
        """Sammelt alle Agenten in den angrenzenden Rasterzellen (Grid).

        Args:
            grid (dict[tuple[float, float], list["Agent"]]): Das räumliche Verzeichnis
                aller Agenten, unterteilt in Rasterzellen.
            grid_size (int): Die Seitenlänge einer einzelnen Rasterzelle.

        Returns:
            list["Agent"]: Eine Liste aller Agenten in der eigenen und den
            acht angrenzenden Zellen.
        """
        nachbarn = []
        block_x, block_y = self.x // grid_size, self.y // grid_size

        for dx in (-1, 0, 1):
            for dy in (-1, 0, 1):
                zelle_key = (block_x + dx, block_y + dy)
                nachbarn.extend(grid.get(zelle_key, []))

        return nachbarn

    def is_genesen(self) -> bool:
        """Prüft, ob der Agent von einer Infektion genesen ist"""
        if self.state == State.KRANK and self.recovery_time <= 0:
            return True

        self.recovery_time -= 1
        return False

    def change_state(self, state: State, config: SimulationConfig) -> None:
        """Ändert den Gesundheitszustand und aktualisiert die Parameter des Agenten.

        Abhängig vom neuen Zustand wird auch die Bewegungsgeschwindigkeit
        anhand der zentralen Konfiguration angepasst.
        """
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
        """Prüft auf Kollisionen mit den Spielfeldrändern und berechnet den Abprall.

        Diese interne Funktion wird während der Bewegung aufgerufen, um zu
        verhindern, dass Agenten das Spielfeld verlassen
        """

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

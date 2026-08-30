"""
Dieses Modul enthält die Kernlogik der Epidemie-Simulation.
"""

import math

import numpy

from ..config import SimulationConfig
from .agent import Agent
from .state import State


class Simulation:
    """Verwaltet den Hauptablauf und Zustand der Epidemie-Simulation.

    Diese Klasse ist das Herzstück des Programms. Sie instanziiert die Agenten,
    steuert die tick-basierte Logik (Bewegung, Infektion, Genesung) und
    zeichnet den Verlauf der Pandemie auf.
    """

    def __init__(self, config: SimulationConfig) -> None:
        """Initialisiert die Simulation basierend auf der Konfiguration.

        Richtet den Zufallsgenerator (RNG) mit einem Seed ein, erstellt die
        Agenten und bereitet die History-Aufzeichnung vor.

        Args:
            config (SimulationConfig): Die zentrale Konfiguration mit allen
                Simulationsparametern (Feldgröße, Radien, Chancen, etc.).
        """

        self.config = config
        self.rng = numpy.random.default_rng(config.seed)
        self._agents = self._create_agents()

        self._n_gesund = config.n_agents - config.n_infizierte
        self._n_krank = config.n_infizierte
        self._n_genesen = 0
        self.history: list[tuple[int, int, int]] = []
        self.is_lockdown = False

    def _create_agents(self) -> list[Agent]:
        """Erzeugt und platziert die initiale Population von Agenten.

        Verteilt die Agenten zufällig auf dem Spielfeld und infiziert die
        in der Konfiguration festgelegte Anzahl von Start-Agenten.
        """

        agents = []
        for _ in range(self.config.n_agents):
            x_pos = self.rng.uniform(0, self.config.field_width)
            y_pos = self.rng.uniform(0, self.config.field_height)

            direction = self.rng.uniform(0, 360)

            agents.append(
                Agent(
                    x_pos,
                    y_pos,
                    direction,
                    self.config.gesunder_agent_speed,
                    State.GESUND,
                    self.config.recovery_duration,
                )
            )

        for i in range(self.config.n_infizierte):
            agents[i].change_state(State.KRANK, self.config)

        return agents

    # ein Tick
    def step(self) -> None:
        """Führt einen einzelnen Simulationsschritt (Tick) aus.

        Baut das räumliche Suchraster auf, wendet Lockdown-Verhaltensweisen an
        (falls aktiv), verarbeitet Infektionen und Genesungen, bewegt alle
        Agenten und speichert den aktuellen Zustand in der History.
        """

        grid_size = 5
        grid = self._build_grid(size=grid_size)

        # Gesunde vermeiden Infizierte beim Lockdown
        if self.lockdown_aktiv:
            self._gesunde_weichen_kranken_aus(grid, grid_size)

        # Infektion und Genesung
        self._infektion_und_genesung(grid, grid_size)

        # Bewegung
        for agent in self._agents:
            agent.move(self.config.field_width, self.config.field_height)

        # History für den Plot am Ende
        self.history.append(self.counts())

    @property
    def agents(self) -> list[Agent]:
        """Gibt die Liste aller Agenten in der Simulation zurück"""
        return self._agents

    @property
    def lockdown_aktiv(self) -> bool:
        """Prüft und aktualisiert den Lockdown-Status.

        Einmal aktiviert (wenn die Schwelle überschritten wird), bleibt
        der Lockdown für den Rest der Simulation bestehen.
        """

        if self._n_krank >= self.config.lockdown_threshold or self.is_lockdown:
            self.is_lockdown = True
            return True

        return False

    def _infektion_und_genesung(
        self, grid: dict[tuple[float, float], list[Agent]], grid_size: int
    ) -> None:
        """Verarbeitet die Ansteckungslogik und den Genesungsprozess.

        Prüft für jeden infizierten Agenten, ob er genesen ist. Wenn nicht,
        werden benachbarte gesunde Agenten gesucht und basierend auf
        Distanz und Infektionswahrscheinlichkeit angesteckt.
        """

        for infizierter in self._agents:
            if infizierter.state != State.KRANK:
                continue

            if infizierter.is_genesen():
                infizierter.change_state(State.GENESEN, self.config)
                self._n_genesen += 1
                self._n_krank -= 1
                continue

            nachbarn = infizierter.get_nachbarn(grid, grid_size)

            for nachbar in nachbarn:
                if nachbar.state != State.GESUND:
                    continue

                distanz = math.dist(
                    [nachbar.x, nachbar.y], [infizierter.x, infizierter.y]
                )

                aktueller_radius = (
                    self.config.lockdown_infection_radius
                    if self.lockdown_aktiv
                    else self.config.infection_radius
                )

                if (
                    distanz <= aktueller_radius
                    and self.rng.random() <= self.config.infection_chance
                ):
                    nachbar.change_state(State.KRANK, self.config)
                    self._n_gesund -= 1
                    self._n_krank += 1

    def _gesunde_weichen_kranken_aus(
        self, grid: dict[tuple[float, float], list[Agent]], grid_size: int
    ) -> None:
        """Lässt gesunde Agenten vor kranken Agenten fliehen.

        Wird während eines aktiven Lockdowns aufgerufen. Jeder gesunde
        Agent berechnet einen Fluchtvektor basierend auf den umliegenden
        infizierten Agenten.
        """
        for agent in self._agents:
            if agent.state != State.GESUND:
                continue

            nachbarn = agent.get_nachbarn(grid, grid_size)

            infiizierte_nachbarn = [
                nachbar for nachbar in nachbarn if nachbar.state == State.KRANK
            ]

            agent.calculate_escape_direction(infiizierte_nachbarn)

    def _build_grid(self, size: int = 5) -> dict[tuple[float, float], list[Agent]]:
        """Erstellt ein räumliches Raster (Grid) zur Nachbarschaftssuche.

        Teilt das Spielfeld in quadratische Zellen der Länge `size` auf
        und ordnet jeden Agenten der passenden Zelle zu.
        """

        grid: dict[tuple[float, float], list[Agent]] = {}
        for x in range(self.config.field_width // size):
            for y in range(self.config.field_height // size):
                grid[(x, y)] = []

        for agent in self.agents:
            grid[(agent.x // size, agent.y // size)].append(agent)

        return grid

    def counts(
        self,
    ) -> tuple[int, int, int]:  # (Gesund, Krank, Genesen) für den Invarianten-Test
        """Ermittelt die aktuelle Verteilung der Gesundheitszustände"""
        return self._n_gesund, self._n_krank, self._n_genesen

    def inf_follow_mouse(self, mouse_x: float, mouse_y: float) -> None:
        """Richtet alle infizierten Agenten auf die Mauskoordinaten aus"""
        for agent in self.agents:
            if agent.state == State.KRANK:
                agent.move_to_cords(mouse_x, mouse_y)

    @property
    def get_field_width(self) -> float:
        """Gibt die logische Breite des Simulationsfeldes zurück"""
        return self.config.field_width

    @property
    def get_field_height(self) -> float:
        """Gibt die logische Höhe des Simulationsfeldes zurück"""
        return self.config.field_height

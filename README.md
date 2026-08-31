# Agentenbasierte Epidemie-Simulation

Eine 2D-Simulation der Ausbreitung einer Infektionskrankheit durch bewegliche Agenten (Random Walk), mit Live-Visualisierung in pygame und Auswertung der Fallzahlen über Zeit als matplotlib-Plot.

## Features

- Zustandsmodell **S**usceptible → **I**nfected → **R**ecovered pro Agent
- Zufallsbewegung mit Randreflektion innerhalb eines begrenzten Feldes
- Infektion basierend auf Distanz (Radius) und Wahrscheinlichkeit pro Zeitschritt
- Genesung nach fester Dauer
- Grid-basierte Nachbarschaftssuche (statt naivem O(n²)-Vergleich) für bessere Performance bei vielen Agenten
- **Lockdown-Mechanismus**: Ab einer konfigurierbaren Anzahl Infizierter wird automatisch ein reduzierter Infektionsradius ("Masken") aktiv, und gesunde Agenten weichen infizierten Agenten aus
- Live-Anzeige der aktuellen Fallzahlen und des Lockdown-Status im Simulationsfenster
- CSV-Export der Zeitreihe (Gesund/Krank/Genesen pro Tick)
- Batch-Modus für Parameter-Sweeps (z. B. Vergleich mehrerer `infection_chance`-Werte) ohne Visualisierung

## Installation

Voraussetzung: [uv](https://docs.astral.sh/uv/) und Python ≥ 3.12.

```bash
git clone <repo-url>
cd epidemic_sim
uv sync
```

`uv sync` installiert alle Abhängigkeiten (numpy, pygame, matplotlib) sowie die Dev-Werkzeuge (pytest, mypy, ruff, interrogate) in eine virtuelle Umgebung.

## Nutzung

### Simulation mit Live-Visualisierung starten

```bash
uv run python -m epidemic_sim.cli
```

Alle Parameter sind optional und haben sinnvolle Defaults. Beispiel mit angepassten Werten:

```bash
uv run python -m epidemic_sim.cli --n_agents 300 --n_infizierte 10 --infection_chance 0.1 --seed 7
```

Nach Schließen des Fensters wird automatisch der S/I/R-Verlauf als Plot angezeigt.

#### Verfügbare CLI-Parameter

| Parameter | Beschreibung |
|---|---|
| `--n_agents` | Gesamtanzahl Agenten |
| `--n_infizierte` | Anzahl initial Infizierter |
| `--infection_chance` | Infektionswahrscheinlichkeit pro Zeitschritt |
| `--infection_radius` | Infektionsradius |
| `--recovery_duration` | Dauer bis zur Genesung (in Ticks) |
| `--agent_speed` | Bewegungsgeschwindigkeit gesunder Agenten |
| `--field_width` / `--field_height` | Größe des Simulationsfeldes |
| `--seed` | Seed des Zufallsgenerators (für reproduzierbare Läufe) |
| `--lockdown_threshold` | Anzahl Infizierter, ab der Maßnahmen aktiv werden |
| `--lockdown_infection_radius` | Reduzierter Infektionsradius während des Lockdowns |
| `--export_csv <pfad>` | Speichert die Zeitreihe zusätzlich als CSV-Datei |

### Tastenkürzel im Simulationsfenster

| Taste | Wirkung |
|---|---|
| `F` | Follow-Modus an/aus – infizierte Agenten bewegen sich in Richtung der Maus |
| `Leertaste` | Tick-Rate umschalten (60 / 120 / 240 / 480, zyklisch) |
| Fenster schließen | Beendet die Simulation und öffnet den Abschluss-Plot |

Im Fenster werden zusätzlich laufend angezeigt: aktuelle Anzahl Gesund/Krank/Genesen, aktuelle Tick-Rate, Follow-Modus-Status und Lockdown-Status.

### Parameter-Sweep ohne Visualisierung (Batch-Modus)

```bash
uv run python -m epidemic_sim.batch --infection_chance_values 0.05 0.1 0.2 0.3 0.5
```

Führt für jeden angegebenen `infection_chance`-Wert eine vollständige Simulation aus (bis `Krank == 0`, mit `--max_ticks` als Sicherheitslimit, Default 50000) und zeigt am Ende einen Vergleichsplot der Infiziertenzahl über die Zeit. Alle übrigen Parameter aus der obigen Tabelle (außer `--infection_chance` selbst) können ebenfalls übergeben werden.

## Tests

```bash
uv run pytest
```

Deckt u. a. Bewegung/Randreflektion, Infektions- und Genesungslogik, die Populations-Invariante (Gesund + Krank + Genesen = N), den Lockdown-Mechanismus und die Reproduzierbarkeit bei festem Seed ab.

## Weitere Werkzeuge

```bash
uv run mypy src/          # Typprüfung
uv run ruff check .       # Linting
uv run ruff format .      # Formatierung
uv run interrogate src/   # Docstring-Abdeckung
```

## Projektstruktur

```
src/epidemic_sim/
├── core/           # Simulationslogik (unabhängig von pygame)
│   ├── agent.py
│   ├── simulation.py
│   ├── state.py
│   └── export.py
├── viz/            # Darstellung
│   ├── renderer.py
│   └── plot.py
├── config.py       # Zentrale Simulationskonfiguration
├── cli.py          # Einstiegspunkt: Simulation + Live-Visualisierung
└── batch.py        # Einstiegspunkt: Parameter-Sweep ohne Visualisierung
tests/
```
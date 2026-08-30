"""
Dieses Modul enthält die Kernlogik der Epidemie-Simulation.
"""

import csv
from pathlib import Path


def export_history_csv(history: list[tuple[int, int, int]], path: str | Path) -> None:
    """Schreibt die S/I/R-Zeitreihe als CSV-Datei.

    Args:
        history: Liste von Tupeln (anzahl_gesund, anzahl_krank, anzahl_genesen),
                 ein Eintrag pro Zeitschritt.
        path: Zieldatei, z.B. "ergebnis.csv".
    """
    with open(path, "w", newline="", encoding="utf-8") as f:
        writer = csv.writer(f)
        writer.writerow(["tick", "gesund", "krank", "genesen"])

        for tick, (gesund, krank, genesen) in enumerate(history):
            writer.writerow([tick, gesund, krank, genesen])

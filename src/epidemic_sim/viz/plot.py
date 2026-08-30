"""
Zeigt einen Plot von S/I/R-Verlauf über die Zeit
"""

import matplotlib.pyplot as plt


def plot_history(history: list[tuple[int, int, int]]) -> None:
    """Zeigt einen Plot von S/I/R-Verlauf über die Zeit.

    Args:
        history: Liste von Tupeln (anzahl_gesund, anzahl_krank, anzahl_genesen),
                 ein Eintrag pro Zeitschritt.
    """
    if not history:
        print("Keine Daten zum Plotten vorhanden.")
        return

    # Tupel-Liste in drei getrennte Listen entpacken
    gesund_verlauf = [eintrag[0] for eintrag in history]
    krank_verlauf = [eintrag[1] for eintrag in history]
    genesen_verlauf = [eintrag[2] for eintrag in history]

    zeitschritte = range(len(history))

    _, ax = plt.subplots(figsize=(10, 6))

    ax.plot(zeitschritte, gesund_verlauf, label="Gesund (S)", color="blue")
    ax.plot(zeitschritte, krank_verlauf, label="Krank (I)", color="red")
    ax.plot(zeitschritte, genesen_verlauf, label="Genesen (R)", color="green")

    ax.set_xlabel("Zeitschritt")
    ax.set_ylabel("Anzahl Agenten")
    ax.set_title("Verlauf der Epidemie-Simulation")
    ax.legend()
    ax.grid(True, alpha=0.3)

    plt.tight_layout()
    plt.show()

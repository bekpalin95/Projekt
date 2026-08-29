import csv

from epidemic_sim.core import export_history_csv


def test_export_creates_correct_csv(tmp_path):
    history = [(95, 5, 0), (93, 6, 1), (90, 7, 3)]
    output_file = tmp_path / "test_output.csv"

    export_history_csv(history, output_file)

    assert output_file.exists()

    with open(output_file, newline="") as f:
        rows = list(csv.reader(f))

    assert rows[0] == ["tick", "gesund", "krank", "genesen"]
    assert rows[1] == ["0", "95", "5", "0"]
    assert rows[2] == ["1", "93", "6", "1"]
    assert rows[3] == ["2", "90", "7", "3"]


import csv

from src.data_logger import save_rail_test_result


def test_save_rail_test_result_creates_csv(tmp_path, monkeypatch):
    import src.data_logger as data_logger

    monkeypatch.setattr(
        data_logger.Path,
        "resolve",
        lambda self: tmp_path / "src" / "data_logger.py",
    )

    test_result = {
        "measurements": {
            "rail_5v": 5.0,
            "rail_3v3": 3.3,
        },
        "results": {
            "rail_5v": "PASS",
            "rail_3v3": "PASS",
        },
        "overall": "PASS",
    }

    save_rail_test_result(test_result)

    csv_file = tmp_path / "data" / "rail_test_results.csv"

    assert csv_file.exists()

    with csv_file.open(
        "r", newline="", encoding="utf-8"
    ) as file:
        rows = list(csv.DictReader(file))

    assert len(rows) == 1
    assert rows[0]["rail_5v_voltage"] == "5.0"
    assert rows[0]["rail_3v3_voltage"] == "3.3"
    assert rows[0]["rail_5v_result"] == "PASS"
    assert rows[0]["rail_3v3_result"] == "PASS"
    assert rows[0]["overall_result"] == "PASS"
    assert rows[0]["timestamp"]


def test_save_rail_test_result_records_failure(tmp_path, monkeypatch):
    import src.data_logger as data_logger

    monkeypatch.setattr(
        data_logger.Path,
        "resolve",
        lambda self: tmp_path / "src" / "data_logger.py",
    )

    test_result = {
        "measurements": {
            "rail_5v": 5.0,
            "rail_3v3": 2.5,
        },
        "results": {
            "rail_5v": "PASS",
            "rail_3v3": "FAIL",
        },
        "overall": "FAIL",
    }

    save_rail_test_result(test_result)

    csv_file = tmp_path / "data" / "rail_test_results.csv"

    with csv_file.open(
        "r", newline="", encoding="utf-8"
    ) as file:
        rows = list(csv.DictReader(file))

    assert len(rows) == 1
    assert rows[0]["rail_3v3_result"] == "FAIL"
    assert rows[0]["overall_result"] == "FAIL"

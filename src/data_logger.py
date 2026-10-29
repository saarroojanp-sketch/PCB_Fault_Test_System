
import csv
from pathlib import Path
from datetime import datetime


def save_test_result(measurements, results, diagnosis):
    data_folder = Path(__file__).resolve().parent.parent / "data"
    data_folder.mkdir(exist_ok=True)

    csv_file = data_folder / "test_results.csv"

    file_exists = csv_file.exists()

    overall = (
        "PASS"
        if all(result == "PASS" for result in results.values())
        else "FAIL"
    )

    row = {
        "timestamp": datetime.now().isoformat(
            timespec="seconds"
        ),
        **measurements,
        "overall_result": overall,
        "diagnosis": diagnosis,
    }

    with csv_file.open(
        "a", newline="", encoding="utf-8"
    ) as file:
        writer = csv.DictWriter(
            file, fieldnames=row.keys()
        )

        if not file_exists:
            writer.writeheader()

        writer.writerow(row)

    print(f"\nTest result saved to: {csv_file}")


def save_rail_test_result(test_result):
    """
    Save simulated PCB rail measurements and PASS/FAIL results to CSV.
    """
    data_folder = Path(__file__).resolve().parent.parent / "data"
    data_folder.mkdir(exist_ok=True)

    csv_file = data_folder / "rail_test_results.csv"
    file_exists = csv_file.exists()

    measurements = test_result["measurements"]
    results = test_result["results"]

    row = {
        "timestamp": datetime.now().isoformat(timespec="seconds"),
        "rail_5v_voltage": measurements["rail_5v"],
        "rail_5v_result": results["rail_5v"],
        "rail_3v3_voltage": measurements["rail_3v3"],
        "rail_3v3_result": results["rail_3v3"],
        "overall_result": test_result["overall"],
    }

    with csv_file.open("a", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=row.keys())

        if not file_exists:
            writer.writeheader()

        writer.writerow(row)

    print(f"\nRail test result saved to: {csv_file}")


def save_test_summary(test_summaries):
    """
    Save a summary of all simulated PCB fault tests to CSV.
    """
    data_folder = Path(__file__).resolve().parent.parent / "data"
    data_folder.mkdir(exist_ok=True)

    csv_file = data_folder / "test_summary.csv"

    fieldnames = [
        "timestamp",
        "fault_mode",
        "overall_result",
        "rail_5v_result",
        "rail_3v3_result",
        "diagnosis",
    ]

    with csv_file.open(
        "w", newline="", encoding="utf-8"
    ) as file:
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()

        for summary in test_summaries:
            writer.writerow({
                "timestamp": datetime.now().isoformat(
                    timespec="seconds"
                ),
                **summary,
            })

    passed = sum(
        item["overall_result"] == "PASS"
        for item in test_summaries
    )
    failed = sum(
        item["overall_result"] == "FAIL"
        for item in test_summaries
    )

    print("\nAUTOMATED TEST SUMMARY")
    print("=" * 45)
    print(f"Total tests : {len(test_summaries)}")
    print(f"PASS        : {passed}")
    print(f"FAIL        : {failed}")
    print(f"Summary CSV : {csv_file}")

    return {
        "total": len(test_summaries),
        "passed": passed,
        "failed": failed,
        "file": csv_file,
    }


import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path


def plot_test_results():
    project_root = Path(__file__).resolve().parent.parent
    csv_file = project_root / "data" / "test_results.csv"
    reports_folder = project_root / "reports"

    reports_folder.mkdir(exist_ok=True)

    if not csv_file.exists():
        print("No CSV test data found. Run main.py first.")
        return

    df = pd.read_csv(csv_file)

    if df.empty:
        print("CSV file contains no test records.")
        return

    required_columns = [
        "rail_5v",
        "rail_3v3",
        "current",
        "overall_result",
    ]

    missing = [
        column for column in required_columns
        if column not in df.columns
    ]

    if missing:
        print(f"Missing CSV columns: {missing}")
        return

    df["test_number"] = range(1, len(df) + 1)

    # Count PASS and FAIL results
    result_counts = (
        df["overall_result"]
        .astype(str)
        .str.upper()
        .value_counts()
        .reindex(["PASS", "FAIL"], fill_value=0)
    )

    fig, axes = plt.subplots(3, 1, figsize=(10, 12))

    # 1. Voltage results
    axes[0].plot(
        df["test_number"],
        df["rail_5v"],
        marker="o",
        label="5V rail",
    )
    axes[0].plot(
        df["test_number"],
        df["rail_3v3"],
        marker="s",
        label="3.3V rail",
    )
    axes[0].axhline(5.0, linestyle="--", label="5V nominal")
    axes[0].axhline(3.3, linestyle=":", label="3.3V nominal")
    axes[0].set_title("PCB Voltage Test Results")
    axes[0].set_xlabel("Test Number")
    axes[0].set_ylabel("Voltage (V)")
    axes[0].legend()
    axes[0].grid(True)

    # 2. Current results
    axes[1].plot(
        df["test_number"],
        df["current"],
        marker="o",
        label="Measured current",
    )
    axes[1].axhline(
        1.5,
        linestyle="--",
        label="Configured current limit",
    )
    axes[1].set_title("PCB Current Test Results")
    axes[1].set_xlabel("Test Number")
    axes[1].set_ylabel("Current (A)")
    axes[1].legend()
    axes[1].grid(True)

    # 3. PASS / FAIL summary
    bars = axes[2].bar(
        result_counts.index,
        result_counts.values,
    )
    axes[2].set_title("PCB Test PASS / FAIL Summary")
    axes[2].set_xlabel("Test Result")
    axes[2].set_ylabel("Number of Tests")
    axes[2].grid(axis="y", linestyle="--", alpha=0.5)

    axes[2].bar_label(bars, padding=3)
    axes[2].set_ylim(
        0,
        max(1, int(result_counts.max()) + 1),
    )

    fig.tight_layout()

    output_file = reports_folder / "pcb_test_results.png"
    fig.savefig(output_file, dpi=150)
    plt.show()
    plt.close(fig)

    print(f"Graph saved to: {output_file}")
    print(f"Total test records: {len(df)}")
    print(result_counts)


if __name__ == "__main__":
    plot_test_results()

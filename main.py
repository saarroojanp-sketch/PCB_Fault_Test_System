
from src.pcb_model import VirtualPCB
from src.measurements import check_measurements, evaluate_pcb_rails
from src.fault_analysis import diagnose_fault
from src.data_logger import (
    save_test_result,
    save_rail_test_result,
    save_test_summary,
)
from src.config_loader import load_limits
from src.instrument_sim import VirtualMultimeter


def main():
    limits = load_limits()
    dmm = VirtualMultimeter()

    fault_modes = [
        "NORMAL",
        "5V_LOW",
        "3V3_LOW",
        "SHORT_CIRCUIT",
        "OVERLOAD",
    ]

    test_summaries = []

    for fault in fault_modes:
        pcb = VirtualPCB(fault=fault)
        measurements = pcb.measure()

        results = check_measurements(measurements, limits)

        overall = (
            "PASS"
            if all(result == "PASS" for result in results.values())
            else "FAIL"
        )

        diagnosis = diagnose_fault(measurements)

        print(f"\nPCB AUTOMATED TEST REPORT: {fault}")
        print("=" * 45)

        for parameter, value in measurements.items():
            print(
                f"{parameter:20} "
                f"{value:6.2f}  "
                f"{results[parameter]}"
            )

        print("=" * 45)
        print(f"OVERALL RESULT: {overall}")
        print("\nFAULT ANALYSIS")
        print("-" * 45)
        print(diagnosis)

        save_test_result(measurements, results, diagnosis)

        print("\nPCB POWER RAIL VALIDATION")
        print("-" * 45)

        rail_result = evaluate_pcb_rails(pcb, dmm, limits)

        for rail, voltage in rail_result["measurements"].items():
            status = rail_result["results"][rail]
            print(f"{rail:20} {voltage:6.2f} V  {status}")

        print(f"RAIL TEST RESULT: {rail_result['overall']}")

        save_rail_test_result(rail_result)

        test_summaries.append({
            "fault_mode": fault,
            "overall_result": overall,
            "rail_5v_result": rail_result["results"]["rail_5v"],
            "rail_3v3_result": rail_result["results"]["rail_3v3"],
            "diagnosis": diagnosis,
        })

    save_test_summary(test_summaries)


if __name__ == "__main__":
    main()


import pytest

from src.pcb_model import VirtualPCB
from src.measurements import check_measurements
from src.fault_analysis import diagnose_fault


LIMITS = {
    "input_voltage": {"min": 11.5, "max": 12.5},
    "current": {"min": 0.0, "max": 1.5},
    "rail_5v": {"min": 4.75, "max": 5.25},
    "rail_3v3": {"min": 3.135, "max": 3.465},
}


@pytest.mark.parametrize(
    "fault, expected_result",
    [
        ("NORMAL", "PASS"),
        ("5V_LOW", "FAIL"),
        ("3V3_LOW", "FAIL"),
        ("SHORT_CIRCUIT", "FAIL"),
        ("OVERLOAD", "FAIL"),
    ],
)
def test_pcb_fault_detection(fault, expected_result):
    pcb = VirtualPCB(fault)
    measurements = pcb.measure()

    results = check_measurements(measurements, LIMITS)

    overall = (
        "PASS"
        if all(value == "PASS" for value in results.values())
        else "FAIL"
    )

    assert overall == expected_result

    diagnosis = diagnose_fault(measurements)
    assert isinstance(diagnosis, str)
    assert len(diagnosis) > 0

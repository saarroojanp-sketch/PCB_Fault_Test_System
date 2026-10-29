
from src.pcb_model import VirtualPCB
from src.measurements import check_measurements


LIMITS = {
    "input_voltage": {"min": 11.5, "max": 12.5},
    "current": {"min": 0.0, "max": 1.5},
    "rail_5v": {"min": 4.75, "max": 5.25},
    "rail_3v3": {"min": 3.135, "max": 3.465},
}


def test_normal_current():
    pcb = VirtualPCB("NORMAL")
    results = check_measurements(pcb.measure(), LIMITS)

    assert results["current"] == "PASS"


def test_short_circuit_high_current():
    pcb = VirtualPCB("SHORT_CIRCUIT")
    results = check_measurements(pcb.measure(), LIMITS)

    assert results["current"] == "FAIL"


def test_overload_high_current():
    pcb = VirtualPCB("OVERLOAD")
    results = check_measurements(pcb.measure(), LIMITS)

    assert results["current"] == "FAIL"

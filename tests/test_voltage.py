
from src.pcb_model import VirtualPCB
from src.measurements import check_measurements


LIMITS = {
    "input_voltage": {"min": 11.5, "max": 12.5},
    "current": {"min": 0.0, "max": 1.5},
    "rail_5v": {"min": 4.75, "max": 5.25},
    "rail_3v3": {"min": 3.135, "max": 3.465},
}


def test_normal_pcb_voltage():
    pcb = VirtualPCB("NORMAL")
    measurements = pcb.measure()

    results = check_measurements(measurements, LIMITS)

    assert results["rail_5v"] == "PASS"
    assert results["rail_3v3"] == "PASS"


def test_5v_low_is_detected():
    pcb = VirtualPCB("5V_LOW")
    measurements = pcb.measure()

    results = check_measurements(measurements, LIMITS)

    assert results["rail_5v"] == "FAIL"


def test_3v3_low_is_detected():
    pcb = VirtualPCB("3V3_LOW")
    measurements = pcb.measure()

    results = check_measurements(measurements, LIMITS)

    assert results["rail_3v3"] == "FAIL"

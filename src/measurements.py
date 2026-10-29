
def check_measurements(measurements, limits):
    results = {}

    for parameter, value in measurements.items():
        if parameter not in limits:
            results[parameter] = "NOT TESTED"
            continue

        minimum = limits[parameter]["min"]
        maximum = limits[parameter]["max"]

        if minimum <= value <= maximum:
            results[parameter] = "PASS"
        else:
            results[parameter] = "FAIL"

    return results

def measure_input_voltage(power_supply, multimeter):
    """
    Measure the simulated power-supply output using a simulated DMM.
    """
    voltage = power_supply.read_voltage()
    measured_voltage = multimeter.measure_voltage(voltage)

    return measured_voltage


def measure_pcb_rails(pcb, multimeter):
    """
    Measure simulated 5V and 3.3V PCB rails using a virtual DMM.
    """
    measurements = pcb.measure()

    return {
        "rail_5v": multimeter.measure_voltage(
            measurements["rail_5v"]
        ),
        "rail_3v3": multimeter.measure_voltage(
            measurements["rail_3v3"]
        ),
    }


def evaluate_pcb_rails(pcb, multimeter, limits):
    """
    Measure PCB rails and evaluate them against configured limits.
    """
    measurements = measure_pcb_rails(pcb, multimeter)
    results = check_measurements(measurements, limits)

    return {
        "measurements": measurements,
        "results": results,
        "overall": (
            "PASS"
            if all(result == "PASS" for result in results.values())
            else "FAIL"
        ),
    }

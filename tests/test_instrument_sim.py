
import pytest

from src.instrument_sim import VirtualPowerSupply, VirtualMultimeter
from src.measurements import measure_input_voltage, measure_pcb_rails
from src.pcb_model import VirtualPCB
from src.measurements import (
    measure_input_voltage,
    measure_pcb_rails,
    evaluate_pcb_rails
)
def test_power_supply_output_is_off_initially():
    psu = VirtualPowerSupply()

    assert psu.output_enabled is False
    assert psu.read_voltage() == 0.0


def test_power_supply_outputs_12v_when_enabled():
    psu = VirtualPowerSupply(voltage=12.0)
    psu.output_on()

    assert psu.read_voltage() == 12.0


def test_power_supply_output_can_be_disabled():
    psu = VirtualPowerSupply()
    psu.output_on()
    psu.output_off()

    assert psu.read_voltage() == 0.0


def test_power_supply_voltage_can_be_changed():
    psu = VirtualPowerSupply()
    psu.set_voltage(5.0)
    psu.output_on()

    assert psu.read_voltage() == 5.0


def test_negative_power_supply_voltage_is_rejected():
    psu = VirtualPowerSupply()

    with pytest.raises(ValueError):
        psu.set_voltage(-1.0)


def test_multimeter_reads_voltage_to_three_decimal_places():
    dmm = VirtualMultimeter()

    assert dmm.measure_voltage(5.12345) == 5.123


def test_multimeter_rejects_negative_voltage():
    dmm = VirtualMultimeter()

    with pytest.raises(ValueError):
        dmm.measure_voltage(-1.0)

        
def test_measure_input_voltage_using_virtual_instruments():
    psu = VirtualPowerSupply(voltage=12.0)
    dmm = VirtualMultimeter()

    psu.output_on()
    measured_voltage = measure_input_voltage(psu, dmm)

    assert measured_voltage == 12.0


def test_measure_input_voltage_when_supply_is_off():
    psu = VirtualPowerSupply(voltage=12.0)
    dmm = VirtualMultimeter()

    measured_voltage = measure_input_voltage(psu, dmm)

    assert measured_voltage == 0.0

 
def test_measure_normal_pcb_rails():
    pcb = VirtualPCB(fault="NORMAL")
    dmm = VirtualMultimeter()

    measurements = measure_pcb_rails(pcb, dmm)

    assert measurements["rail_5v"] == 5.0
    assert measurements["rail_3v3"] == 3.3


def test_measure_faulty_pcb_rails():
    pcb = VirtualPCB(fault="3V3_LOW")
    dmm = VirtualMultimeter()

    measurements = measure_pcb_rails(pcb, dmm)

    assert measurements["rail_5v"] == 5.0
    assert measurements["rail_3v3"] == 2.5

    
from src.config_loader import load_limits


def test_normal_pcb_rails_overall_pass():
    pcb = VirtualPCB(fault="NORMAL")
    dmm = VirtualMultimeter()
    limits = load_limits()

    result = evaluate_pcb_rails(pcb, dmm, limits)

    assert result["results"]["rail_5v"] == "PASS"
    assert result["results"]["rail_3v3"] == "PASS"
    assert result["overall"] == "PASS"


def test_faulty_pcb_rails_overall_fail():
    pcb = VirtualPCB(fault="3V3_LOW")
    dmm = VirtualMultimeter()
    limits = load_limits()

    result = evaluate_pcb_rails(pcb, dmm, limits)

    assert result["results"]["rail_5v"] == "PASS"
    assert result["results"]["rail_3v3"] == "FAIL"
    assert result["overall"] == "FAIL"


def test_low_5v_rail_causes_overall_fail():
    pcb = VirtualPCB(fault="5V_LOW")
    dmm = VirtualMultimeter()
    limits = load_limits()

    result = evaluate_pcb_rails(pcb, dmm, limits)

    assert result["results"]["rail_5v"] == "FAIL"
    assert result["overall"] == "FAIL"


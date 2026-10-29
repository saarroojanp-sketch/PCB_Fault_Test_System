
class VirtualPowerSupply:
    """Simulated programmable DC power supply."""

    def __init__(self, voltage=12.0):
        self.voltage = voltage
        self.output_enabled = False

    def set_voltage(self, voltage):
        if voltage < 0:
            raise ValueError("Voltage cannot be negative")
        self.voltage = voltage

    def output_on(self):
        self.output_enabled = True

    def output_off(self):
        self.output_enabled = False

    def read_voltage(self):
        if not self.output_enabled:
            return 0.0
        return self.voltage


class VirtualMultimeter:
    """Simulated digital multimeter for voltage measurements."""

    def measure_voltage(self, voltage):
        if voltage < 0:
            raise ValueError("Voltage cannot be negative")
        return round(voltage, 3)

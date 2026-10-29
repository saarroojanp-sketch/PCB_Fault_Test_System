class VirtualPCB:
    """
    Simulated PCB used as a Device Under Test (DUT).
    """

    def __init__(self, fault="NORMAL"):
        self.fault = fault

    def measure(self):
        """
        Simulate PCB electrical measurements.
        """

        if self.fault == "NORMAL":
            return {
                "input_voltage": 12.0,
                "current": 0.80,
                "rail_5v": 5.00,
                "rail_3v3": 3.30
            }

        elif self.fault == "5V_LOW":
            return {
                "input_voltage": 12.0,
                "current": 1.10,
                "rail_5v": 3.80,
                "rail_3v3": 2.90
            }

        elif self.fault == "3V3_LOW":
            return {
                "input_voltage": 12.0,
                "current": 0.90,
                "rail_5v": 5.00,
                "rail_3v3": 2.50
            }

        elif self.fault == "SHORT_CIRCUIT":
            return {
                "input_voltage": 12.0,
                "current": 2.80,
                "rail_5v": 3.20,
                "rail_3v3": 1.20
            }

        elif self.fault == "OVERLOAD":
            return {
                "input_voltage": 12.0,
                "current": 1.90,
                "rail_5v": 4.20,
                "rail_3v3": 3.00
            }

        else:
            raise ValueError(f"Unknown fault: {self.fault}")
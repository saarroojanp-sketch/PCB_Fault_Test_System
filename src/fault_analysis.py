
def diagnose_fault(measurements):
    vin = measurements["input_voltage"]
    current = measurements["current"]
    rail_5v = measurements["rail_5v"]
    rail_3v3 = measurements["rail_3v3"]

    if vin < 11.5 or vin > 12.5:
        return "Input voltage abnormal: check power source"

    if current > 1.5 and rail_5v < 4.75:
        return "Possible 5V rail short circuit or overload"

    if rail_5v < 4.75 and rail_3v3 < 3.135:
        return "Possible 5V regulator fault or upstream problem"

    if rail_5v >= 4.75 and rail_3v3 < 3.135:
        return "Possible 3.3V regulator or rail fault"

    if current > 1.5:
        return "Excessive current: check for short or overload"

    return "No fault detected by current diagnostic rules"

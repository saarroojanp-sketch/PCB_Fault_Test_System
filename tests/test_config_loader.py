
import pytest

from src.config_loader import load_limits


def test_load_limits_returns_required_parameters():
    limits = load_limits()

    assert "input_voltage" in limits
    assert "current" in limits
    assert "rail_5v" in limits
    assert "rail_3v3" in limits


def test_load_limits_has_min_and_max():
    limits = load_limits()

    for parameter, values in limits.items():
        assert "min" in values, f"{parameter} missing min"
        assert "max" in values, f"{parameter} missing max"
        assert values["min"] <= values["max"], (
            f"{parameter}: min exceeds max"
        )


def test_load_limits_expected_values():
    limits = load_limits()

    assert limits["input_voltage"]["min"] == 11.5
    assert limits["input_voltage"]["max"] == 12.5

    assert limits["current"]["max"] == 1.5

    assert limits["rail_5v"]["min"] == 4.75
    assert limits["rail_3v3"]["min"] == 3.135

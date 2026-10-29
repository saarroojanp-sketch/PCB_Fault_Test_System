
from pathlib import Path
import yaml


def load_limits():
    project_root = Path(__file__).resolve().parent.parent
    config_file = project_root / "config" / "limits.yaml"

    if not config_file.exists():
        raise FileNotFoundError(
            f"Test limits file not found: {config_file}"
        )

    with config_file.open("r", encoding="utf-8") as file:
        config = yaml.safe_load(file)

    if not isinstance(config, dict) or "limits" not in config:
        raise ValueError(
            "Configuration must contain a 'limits' section"
        )

    limits = config["limits"]

    required = [
        "input_voltage",
        "current",
        "rail_5v",
        "rail_3v3",
    ]

    for parameter in required:
        if parameter not in limits:
            raise ValueError(
                f"Missing test limit: {parameter}"
            )

        item = limits[parameter]

        if not isinstance(item, dict):
            raise ValueError(
                f"Invalid configuration for {parameter}"
            )

        if "min" not in item or "max" not in item:
            raise ValueError(
                f"{parameter} requires min and max"
            )

        if item["min"] > item["max"]:
            raise ValueError(
                f"Minimum exceeds maximum for {parameter}"
            )

    return limits

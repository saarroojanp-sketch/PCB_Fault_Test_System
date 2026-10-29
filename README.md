# Automated PCB Fault Diagnosis and Test System

## Project Overview

A Python-based simulated PCB testing system designed to evaluate voltage rails and current measurements, identify potential fault conditions, log test results, and generate test-result visualizations.

**Project status:** Software simulation and automated test workflow.

## Key Features

- Simulated PCB device under test (DUT)
- Configurable electrical limits using YAML
- Voltage and current limit checking
- Fault diagnosis for simulated PCB conditions
- CSV-based test result logging
- Automated 5V and 3.3V power-rail validation
- PASS/FAIL summary generation
- Voltage, current, and test-summary graphs
- Automated regression tests using pytest

## Simulated Fault Conditions

- NORMAL
- 5V_LOW
- 3V3_LOW
- SHORT_CIRCUIT
- OVERLOAD

## Technologies

- Python
- pytest
- pandas
- NumPy
- Matplotlib
- PyYAML
- PyVISA
- CSV-based test reporting

## Project Structure

```text
PCB_Fault_Test_System/
├── config/
│   └── limits.yaml
├── src/
│   ├── pcb_model.py
│   ├── instrument_sim.py
│   ├── measurements.py
│   ├── fault_analysis.py
│   ├── data_logger.py
│   ├── plot_results.py
│   └── config_loader.py
├── tests/
├── data/
├── reports/
├── main.py
├── requirements.txt
├── pytest.ini
└── README.md
```

## How to Run

Create and activate a virtual environment, then install dependencies:

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Run the simulated PCB tests:

```powershell
python main.py
```

Generate the result graphs:

```powershell
python -m src.plot_results
```

Run the automated regression tests:

```powershell
python -m pytest -v
```

## Generated Outputs

- `data/test_results.csv`
- `data/rail_test_results.csv`
- `data/test_summary.csv`
- `reports/pcb_test_results.png`

## Scope and Limitations

This project currently uses simulated PCB measurements and virtual instruments. It demonstrates software-based testing, fault classification, configurable limits, result logging, and visualization. It does not establish physical PCB testing or hardware-in-the-loop validation.

## Future Improvements

- Connect real instruments through supported VISA interfaces
- Add hardware safety checks before energizing a physical DUT
- Implement configurable acceptance limits and expanded test coverage
- Add report generation and test-run identification
- Validate the workflow against real PCB measurements

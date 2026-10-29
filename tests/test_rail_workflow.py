
from src.config_loader import load_limits
from src.data_logger import save_rail_test_result
from src.instrument_sim import VirtualMultimeter
from src.measurements import evaluate_pcb_rails
from src.pcb_model import VirtualPCB


def test_normal_pcb_workflow_saves_pass_result(tmp_path, monkeypatch):
    # Load real project configuration before patching Path.resolve().
    limits = load_limits()

    import src.data_logger as data_logger

    monkeypatch.setattr(
        data_logger.Path,
        "resolve",
        lambda self: tmp_path / "src" / "data_logger.py",
    )

    pcb = VirtualPCB(fault="NORMAL")
    dmm = VirtualMultimeter()

    result = evaluate_pcb_rails(pcb, dmm, limits)
    save_rail_test_result(result)

    csv_file = tmp_path / "data" / "rail_test_results.csv"

    assert csv_file.exists()
    assert result["overall"] == "PASS"


def test_faulty_pcb_workflow_saves_fail_result(tmp_path, monkeypatch):
    # Load real project configuration before patching Path.resolve().
    limits = load_limits()

    import src.data_logger as data_logger

    monkeypatch.setattr(
        data_logger.Path,
        "resolve",
        lambda self: tmp_path / "src" / "data_logger.py",
    )

    pcb = VirtualPCB(fault="3V3_LOW")
    dmm = VirtualMultimeter()

    result = evaluate_pcb_rails(pcb, dmm, limits)
    save_rail_test_result(result)

    csv_file = tmp_path / "data" / "rail_test_results.csv"

    assert csv_file.exists()
    assert result["overall"] == "FAIL"
    assert result["results"]["rail_3v3"] == "FAIL"

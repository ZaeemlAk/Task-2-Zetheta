from app.services.drift_service import classify_psi, get_drift_summary


def test_psi_classification():
    assert classify_psi(0.05) == "Stable"
    assert classify_psi(0.12) == "Minor drift"
    assert classify_psi(0.21) == "Moderate drift"
    assert classify_psi(0.30) == "Severe drift"


def test_drift_summary_not_empty():
    rows = get_drift_summary()
    assert isinstance(rows, list)
    assert len(rows) > 0

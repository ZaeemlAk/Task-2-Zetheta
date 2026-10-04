from app.services.performance_service import compute_business_impact, get_performance_summary


def test_performance_summary_consistent():
    summary = get_performance_summary()
    assert "precision" in summary
    assert "recall" in summary
    assert summary["precision"] >= 0.5
    assert summary["recall"] >= 0.4


def test_business_impact_is_positive():
    impact = compute_business_impact()
    assert impact["estimated_exposure_inr"] > 0
    assert impact["total_business_impact_inr"] > impact["estimated_exposure_inr"] * 0.5

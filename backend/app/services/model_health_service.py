from __future__ import annotations

from app.services.alert_service import evaluate_alerts
from app.services.drift_service import get_drift_summary
from app.services.performance_service import compute_business_impact, get_performance_summary


def get_model_health() -> dict:
    performance = get_performance_summary()
    drift_rows = get_drift_summary()
    business = compute_business_impact()
    alerts = evaluate_alerts(performance, drift_rows, business)
    drift_score = 100 - min(100, sum(15 for row in drift_rows if row["classification"] in {"Moderate drift", "Severe drift"}) * 10)
    performance_score = min(100, max(0, (performance["precision"] * 50 + performance["recall"] * 50) * 100))
    quality_score = max(0, 100 - sum(8 for row in drift_rows if row["null_percentage"] > 0.05) * 5)
    business_score = max(0, 100 - (business["total_business_impact_inr"] / 6000000) * 100)
    overall = round((performance_score * 0.35 + drift_score * 0.30 + quality_score * 0.20 + business_score * 0.15))
    return {
        "overall_score": overall,
        "components": {
            "performance": round(performance_score),
            "drift": round(drift_score),
            "data_quality": round(quality_score),
            "business_impact": round(business_score),
        },
        "alerts": alerts,
        "status": "RED" if overall < 50 else "AMBER" if overall < 75 else "GREEN",
    }

from __future__ import annotations

from typing import Dict, List


def evaluate_alerts(performance: Dict, drift_rows: List[Dict], business: Dict) -> List[Dict]:
    alerts = []
    severe_drift_count = sum(1 for row in drift_rows if row["classification"] in {"Moderate drift", "Severe drift"})
    if performance["precision"] < 0.8:
        alerts.append({"level": "RED", "title": "Precision collapse", "message": "Precision has fallen below the intervention threshold."})
    if performance["recall"] < 0.65:
        alerts.append({"level": "RED", "title": "Recall collapse", "message": "Recall is materially below the expected performance envelope."})
    if severe_drift_count >= 5:
        alerts.append({"level": "ORANGE", "title": "Multi-feature drift", "message": "Several critical features show material distributional change."})
    if business["estimated_exposure_inr"] > 1_000_000:
        alerts.append({"level": "AMBER", "title": "Financial exposure above threshold", "message": "Fraud exposure and customer impact have risen materially."})
    if not alerts:
        alerts.append({"level": "GREEN", "title": "Stable", "message": "No significant drift or performance anomaly is present at this time."})
    return alerts

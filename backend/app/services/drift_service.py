from __future__ import annotations

from typing import Dict, List

import pandas as pd

from app.config import DATA_DIR

FEATURES = [
    "F01 transaction_amount",
    "F02 transaction_frequency_24h",
    "F03 merchant_category_code",
    "F04 geographic_distance",
    "F05 device_fingerprint_match",
    "F06 time_since_last_transaction",
    "F07 customer_account_age",
    "F08 average_monthly_balance",
    "F09 channel_type",
    "F10 ip_reputation_score",
    "F11 session_duration",
    "F12 failed_login_attempts",
    "F13 beneficiary_account_age",
    "F14 transaction_velocity_7d",
    "F15 cross_border_indicator",
]


def load_feature_distributions() -> pd.DataFrame:
    path = DATA_DIR / "feature_distributions.csv"
    return pd.read_csv(path)


def classify_psi(value: float) -> str:
    if value < 0.10:
        return "Stable"
    if value < 0.20:
        return "Minor drift"
    if value < 0.25:
        return "Moderate drift"
    return "Severe drift"


def get_drift_summary() -> List[Dict]:
    df = load_feature_distributions()
    summary = []
    for feature_name, group in df.groupby("feature_name"):
        latest = group.sort_values("week_id").iloc[-1]
        summary.append(
            {
                "feature": feature_name,
                "latest_psi": float(latest["psi_vs_baseline"]),
                "classification": classify_psi(float(latest["psi_vs_baseline"])),
                "ks_statistic": float(latest["ks_statistic"]),
                "ks_p_value": float(latest["ks_p_value"]),
                "js_divergence": float(latest["js_divergence"]),
                "null_percentage": float(latest["null_percentage"]),
                "drift_flag": bool(latest["drift_flag"]),
                "trend": "increasing" if float(latest["psi_vs_baseline"]) > group["psi_vs_baseline"].median() else "stable",
            }
        )
    return sorted(summary, key=lambda x: x["latest_psi"], reverse=True)


def get_feature_detail(feature_name: str) -> Dict:
    df = load_feature_distributions()
    feature_df = df[df["feature_name"] == feature_name].sort_values("week_id")
    if feature_df.empty:
        raise ValueError(f"Feature not found: {feature_name}")
    return {
        "feature": feature_name,
        "history": feature_df.to_dict(orient="records"),
        "latest": feature_df.iloc[-1].to_dict(),
        "severity": classify_psi(float(feature_df.iloc[-1]["psi_vs_baseline"])),
    }

from __future__ import annotations

from typing import Dict, List

import pandas as pd

from app.config import DATA_DIR


def load_performance() -> pd.DataFrame:
    return pd.read_csv(DATA_DIR / "performance_log.csv")


def get_performance_summary() -> Dict:
    df = load_performance()
    latest = df.iloc[-1]
    start = df.iloc[0]
    return {
        "week_id": int(latest["week_id"]),
        "precision": float(latest["precision"]),
        "recall": float(latest["recall"]),
        "f1_score": float(latest["f1_score"]),
        "auc_roc": float(latest["auc_roc"]),
        "avg_inference_latency_ms": float(latest["avg_inference_latency_ms"]),
        "alert_triggered": bool(latest["alert_triggered"]),
        "initial_precision": float(start["precision"]),
        "initial_recall": float(start["recall"]),
        "degradation_start_week": int(df.loc[df["precision"] < 0.85, "week_id"].min() or df.iloc[0]["week_id"]),
        "total_transactions": int(df["total_transactions"].sum()),
    }


def get_performance_timeline() -> List[Dict]:
    return load_performance().to_dict(orient="records")


def compute_business_impact() -> Dict:
    df = load_performance()
    estimated_loss = float(df["total_fraud_confirmed"].sum() * 0.85 * 150000)
    false_positive_cost = float(df["false_positives"].sum() * 2500)
    missed_fraud_cost = float(df["false_negatives"].sum() * 180000)
    return {
        "estimated_loss_inr": round(estimated_loss, 2),
        "false_positive_cost_inr": round(false_positive_cost, 2),
        "missed_fraud_cost_inr": round(missed_fraud_cost, 2),
        "total_business_impact_inr": round(estimated_loss + false_positive_cost + missed_fraud_cost, 2),
        "estimated_exposure_inr": 150000000.0,
    }

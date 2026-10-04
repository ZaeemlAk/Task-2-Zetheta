from __future__ import annotations

import json
from pathlib import Path

import numpy as np
import pandas as pd

DATA_DIR = Path(__file__).resolve().parent

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


def generate_performance_log() -> pd.DataFrame:
    weeks = list(range(1, 53))
    records = []
    base_transactions = 16000
    for week in weeks:
        seasonal = 1 + 0.18 * np.sin((week / 52) * 2 * np.pi)
        drift_phase = max(0.0, (week - 18) / 30)
        total_transactions = int(base_transactions * seasonal * (1 + 0.22 * drift_phase))
        fraud_prevalence = 0.015 + 0.013 * drift_phase + 0.003 * np.sin(week / 4)
        total_fraud_confirmed = max(80, int(total_transactions * fraud_prevalence))
        precision = 0.942 - 0.0033 * week
        precision = max(0.67, min(0.942, precision))
        recall = 0.917 - 0.005 * week
        recall = max(0.55, min(0.917, recall))
        f1 = 2 * precision * recall / (precision + recall)
        tp = int(total_fraud_confirmed * recall)
        fn = max(0, total_fraud_confirmed - tp)
        fp = int((tp * (1 - precision)) / max(precision, 1e-6))
        total_fraud_flagged = tp + fp
        tn = max(0, total_transactions - total_fraud_confirmed - fp - fn)
        auc_roc = max(0.72, 0.94 - 0.002 * week + 0.05 * (1 / (1 + np.exp(-(week - 18)))))
        latency = 45 + 10 * (1 + drift_phase) + np.random.default_rng(week).uniform(-4, 8)
        alert_triggered = precision < 0.80 or recall < 0.70
        records.append(
            {
                "week_id": week,
                "week_start_date": f"2024-W{week:02d}",
                "total_transactions": total_transactions,
                "total_fraud_flagged": total_fraud_flagged,
                "total_fraud_confirmed": total_fraud_confirmed,
                "true_positives": tp,
                "false_positives": fp,
                "false_negatives": fn,
                "true_negatives": tn,
                "precision": round(float(precision), 4),
                "recall": round(float(recall), 4),
                "f1_score": round(float(f1), 4),
                "auc_roc": round(float(auc_roc), 4),
                "avg_inference_latency_ms": round(float(latency), 2),
                "alert_triggered": bool(alert_triggered),
            }
        )
    return pd.DataFrame(records)


def generate_feature_distributions() -> pd.DataFrame:
    rows = []
    rng = np.random.default_rng(42)
    feature_configs = {
        "F01 transaction_amount": {"mean": 3200, "std": 2200, "drift": 0.9},
        "F02 transaction_frequency_24h": {"mean": 2.6, "std": 1.4, "drift": 0.7},
        "F03 merchant_category_code": {"mean": 0.5, "std": 0.2, "drift": 0.5},
        "F04 geographic_distance": {"mean": 210, "std": 160, "drift": 0.8},
        "F05 device_fingerprint_match": {"mean": 0.82, "std": 0.2, "drift": 0.4},
        "F06 time_since_last_transaction": {"mean": 6.5, "std": 4.1, "drift": 0.6},
        "F07 customer_account_age": {"mean": 950, "std": 620, "drift": 0.2},
        "F08 average_monthly_balance": {"mean": 62000, "std": 26000, "drift": 0.4},
        "F09 channel_type": {"mean": 0.6, "std": 0.18, "drift": 0.3},
        "F10 ip_reputation_score": {"mean": 0.75, "std": 0.22, "drift": 0.85},
        "F11 session_duration": {"mean": 250, "std": 110, "drift": 0.7},
        "F12 failed_login_attempts": {"mean": 0.85, "std": 1.0, "drift": 0.55},
        "F13 beneficiary_account_age": {"mean": 248, "std": 165, "drift": 0.2},
        "F14 transaction_velocity_7d": {"mean": 8.5, "std": 5.9, "drift": 0.95},
        "F15 cross_border_indicator": {"mean": 0.12, "std": 0.1, "drift": 0.9},
    }
    for week in range(1, 53):
        drift_stage = max(0.0, (week - 18) / 24)
        for feature_name, conf in feature_configs.items():
            shift = conf["drift"] * drift_stage
            mean = conf["mean"] * (1 + shift)
            std = conf["std"] * (1 + 0.45 * shift)
            base_vals = rng.normal(mean, std, 6000)
            current_vals = base_vals + rng.normal(0, std * 0.33, 6000)
            psi = min(0.45, 0.03 + 0.12 * drift_stage + abs(mean - conf["mean"]) / max(conf["mean"], 1))
            ks_stat = min(1.0, 0.06 + 0.41 * drift_stage + rng.random() * 0.12)
            pval = max(0.0, 0.04 - 0.02 * drift_stage + rng.random() * 0.05)
            js_div = min(0.5, 0.02 + 0.18 * drift_stage)
            null_pct = max(0.0, 0.005 + 0.015 * drift_stage + rng.random() * 0.02)
            rows.append(
                {
                    "week_id": week,
                    "feature_name": feature_name,
                    "mean": round(float(np.mean(current_vals)), 4),
                    "std_dev": round(float(np.std(current_vals)), 4),
                    "median": round(float(np.median(current_vals)), 4),
                    "percentile_5": round(float(np.percentile(current_vals, 5)), 4),
                    "percentile_25": round(float(np.percentile(current_vals, 25)), 4),
                    "percentile_75": round(float(np.percentile(current_vals, 75)), 4),
                    "percentile_95": round(float(np.percentile(current_vals, 95)), 4),
                    "skewness": round(float(np.mean((current_vals - np.mean(current_vals)) ** 3) / (np.std(current_vals) ** 3 + 1e-8)), 4),
                    "kurtosis": round(float(np.mean((current_vals - np.mean(current_vals)) ** 4) / (np.std(current_vals) ** 4 + 1e-8) - 3), 4),
                    "psi_vs_baseline": round(float(psi), 4),
                    "ks_statistic": round(float(ks_stat), 4),
                    "ks_p_value": round(float(pval), 4),
                    "js_divergence": round(float(js_div), 4),
                    "null_percentage": round(float(null_pct), 4),
                    "drift_flag": bool(psi > 0.1 or pval < 0.05),
                }
            )
    return pd.DataFrame(rows)


def generate_predictions() -> pd.DataFrame:
    months = list(range(1, 13))
    rows = []
    rng = np.random.default_rng(7)
    prediction_id = 1
    for month in months:
        for _ in range(10000):
            drift = max(0.0, (month - 4) / 9)
            base = 0.06 + 0.015 * drift + rng.random() * 0.02
            label = 1 if rng.random() < base else 0
            logit = np.log(base / max(0.05, 1 - base)) + rng.normal(0, 0.8)
            prob = 1 / (1 + np.exp(-logit))
            prob = min(0.99, max(0.01, prob))
            predicted_label = 1 if prob >= 0.65 else 0
            actual_label = label
            label_confidence = round(float(np.clip(0.5 + (prob - 0.5) * 2.0, 0.0, 1.0)), 4)
            feature_values = {
                "transaction_amount": round(float(rng.uniform(50, 25000)), 2),
                "transaction_frequency_24h": round(float(rng.uniform(1, 12)), 2),
                "merchant_category_code": int(rng.integers(1, 15)),
                "geographic_distance": round(float(rng.uniform(10, 5000)), 2),
                "device_fingerprint_match": round(float(rng.choice([0, 1], p=[0.25, 0.75])), 4),
                "time_since_last_transaction": round(float(rng.uniform(0.1, 36)), 2),
                "customer_account_age": round(float(rng.uniform(30, 4000)), 2),
                "average_monthly_balance": round(float(rng.uniform(5000, 200000)), 2),
                "channel_type": int(rng.integers(1, 4)),
                "ip_reputation_score": round(float(rng.uniform(0, 100)), 2),
                "session_duration": round(float(rng.uniform(30, 1200)), 2),
                "failed_login_attempts": round(float(rng.uniform(0, 10)), 2),
                "beneficiary_account_age": round(float(rng.uniform(1, 1800)), 2),
                "transaction_velocity_7d": round(float(rng.uniform(1, 35)), 2),
                "cross_border_indicator": int(rng.choice([0, 1], p=[0.9, 0.1])),
            }
            rows.append(
                {
                    "prediction_id": prediction_id,
                    "month": month,
                    "fraud_probability": round(float(prob), 6),
                    "predicted_label": predicted_label,
                    "actual_label": actual_label,
                    "label_confidence": label_confidence,
                    "feature_values_json": json.dumps(feature_values),
                }
            )
            prediction_id += 1
    return pd.DataFrame(rows)


def generate_events() -> pd.DataFrame:
    events = [
        ("2024-01-15", "UPI adoption", "Aggressive UPI adoption and campaign expanded small-ticket digital transactions.", "High", "F01,F02,F09,F14"),
        ("2024-03-01", "IP reputation", "Third-party IP reputation feed updated and several low-risk IP ranges were reclassified.", "High", "F10,F05,F11"),
        ("2024-04-10", "Device spoofing", "Device fingerprint spoofing campaign targeted mobile user sessions.", "Critical", "F05,F11,F12"),
        ("2024-05-18", "Mobile app redesign", "Mobile app redesign changed session and channel telemetry capture behavior.", "Medium", "F09,F11,F06"),
        ("2024-06-22", "Fraud-labeling process", "Fraud review queue delay created labeling lag and stale supervisory labels.", "Critical", "F03,F12,F15"),
        ("2024-07-12", "RBI UPI limit changes", "Higher UPI transaction limits increased high-value transfer patterns.", "High", "F01,F14,F15"),
        ("2024-08-03", "Inflation", "Inflation elevated transaction sizes and risk asymmetry.", "Medium", "F01,F08,F07"),
        ("2024-09-17", "Cross-border fraud", "Cross-border mule activity increased and bypassed geo heuristics.", "Critical", "F04,F15,F10"),
        ("2024-10-20", "XGBoost library update", "Model library update introduced threshold-shift behaviour in the production pipeline.", "Medium", "F10,F15,F01"),
        ("2024-11-05", "Feedback loop", "Missed fraud cases were later treated as legitimate labels and reintroduced to retraining.", "Critical", "F03,F12,F15"),
    ]
    return pd.DataFrame(events, columns=["event_date", "category", "description", "severity", "affected_features"])


def main() -> None:
    performance = generate_performance_log()
    performance.to_csv(DATA_DIR / "performance_log.csv", index=False)

    feature_dist = generate_feature_distributions()
    feature_dist.to_csv(DATA_DIR / "feature_distributions.csv", index=False)

    predictions = generate_predictions()
    predictions.to_csv(DATA_DIR / "sample_predictions.csv", index=False)

    events = generate_events()
    events.to_csv(DATA_DIR / "external_events.csv", index=False)

    print("Generated datasets:")
    print(performance.head().to_string(index=False))
    print(feature_dist.head().to_string(index=False))
    print(predictions.head().to_string(index=False))
    print(events.head().to_string(index=False))


if __name__ == "__main__":
    main()

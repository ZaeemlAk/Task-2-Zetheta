from __future__ import annotations

from typing import Dict, List

from app.services.drift_service import get_drift_summary
from app.services.performance_service import compute_business_impact, load_performance


def get_events() -> List[Dict]:
    return [
        {"event_date": "2024-01-15", "category": "UPI adoption", "description": "Aggressive UPI adoption and campaign expanded small-ticket digital transactions.", "severity": "High", "affected_features": "F01,F02,F09,F14"},
        {"event_date": "2024-03-01", "category": "IP reputation", "description": "Third-party IP reputation feed updated and several low-risk IP ranges were reclassified.", "severity": "High", "affected_features": "F10,F05,F11"},
        {"event_date": "2024-04-10", "category": "Device spoofing", "description": "Device fingerprint spoofing campaign targeted mobile user sessions.", "severity": "Critical", "affected_features": "F05,F11,F12"},
        {"event_date": "2024-05-18", "category": "App redesign", "description": "Mobile app redesign changed session and channel telemetry capture behavior.", "severity": "Medium", "affected_features": "F09,F11,F06"},
        {"event_date": "2024-06-22", "category": "Labeling process", "description": "Fraud review queue delay created labeling lag and stale supervisory labels.", "severity": "Critical", "affected_features": "F03,F12,F15"},
        {"event_date": "2024-07-12", "category": "RBI UPI limits", "description": "Higher UPI transaction limits increased high-value transfer patterns.", "severity": "High", "affected_features": "F01,F14,F15"},
        {"event_date": "2024-08-03", "category": "Inflation", "description": "Inflation elevated transaction sizes and risk asymmetry.", "severity": "Medium", "affected_features": "F01,F08,F07"},
        {"event_date": "2024-09-17", "category": "Cross-border fraud", "description": "Cross-border mule activity increased and bypassed geo heuristics.", "severity": "Critical", "affected_features": "F04,F15,F10"},
        {"event_date": "2024-10-20", "category": "XGBoost library update", "description": "Model library update introduced threshold-shift behaviour in the production pipeline.", "severity": "Medium", "affected_features": "F10,F15,F01"},
        {"event_date": "2024-11-05", "category": "Feedback loop", "description": "Missed fraud cases were later treated as legitimate labels and reintroduced to retraining.", "severity": "Critical", "affected_features": "F03,F12,F15"},
    ]


def get_root_cause() -> Dict:
    performance_df = load_performance()
    latest = performance_df.iloc[-1]
    drift = get_drift_summary()
    top_drifts = sorted(drift, key=lambda x: x["latest_psi"], reverse=True)[:5]
    fishbone = {
        "Data": ["Label lag due to review queue", "Third-party IP feed update", "Missing device telemetry after app redesign"],
        "Model": ["Threshold sensitivity after deployment and stale feature relationships", "Feature importance shift toward value and velocity features"],
        "Process": ["Delayed fraud investigation workflow", "Retry policy and lack of champion-challenger monitoring"],
        "People": ["Manual review backlog and inconsistent label adjudication", "Insufficient escalation for high-risk segments"],
        "Technology": ["Monitoring gap for upstream schema and freshness", "XGBoost library update without shadow validation"],
        "Environment": ["UPI campaign, inflation, and cross-border fraud pattern change"],
    }
    five_whys = [
        {
            "question": f"Why did precision fall to {float(latest['precision']):.2f}?",
            "answer": "The model began to misclassify high-volume, low-velocity fraud patterns as legitimate transactions after feature shifts in UPI and cross-border activity.",
            "depth": 1,
        },
        {
            "question": "Why did the feature shifts matter?",
            "answer": "The model learned from historical fraud patterns that did not match new channel and device behavior.",
            "depth": 2,
        },
        {
            "question": "Why were the shifts not detected earlier?",
            "answer": "Monitoring checked only aggregate statistics and missed threshold-specific and label-quality drift signals.",
            "depth": 3,
        },
        {
            "question": "Why did the feedback loop accelerate the problem?",
            "answer": "Missed fraud cases were eventually labeled as genuine, reducing the quality of retraining data and reinforcing the wrong decision boundary.",
            "depth": 4,
        },
        {
            "question": "Why is this systemic?",
            "answer": "The bank lacked continuous upstream validation, label freshness monitoring, and approved model rollback policies.",
            "depth": 5,
        },
    ]
    fault_tree = {
        "top_event": "SENTINEL-7 performance degradation",
        "branches": [
            {"name": "Data drift and label contamination", "logic": "AND", "children": ["feature drift on F01/F10/F14/F15", "delayed labels", "feedback loop"]},
            {"name": "Monitoring blind spots", "logic": "OR", "children": ["no feature-level alerting", "no upstream quality checks", "late alert escalation"]},
            {"name": "Environmental change", "logic": "OR", "children": ["UPI campaign", "device spoofing", "cross-border fraud"]},
        ],
    }
    return {
        "fishbone": fishbone,
        "five_whys": five_whys,
        "fault_tree": fault_tree,
        "top_drifts": top_drifts,
        "business_impact": compute_business_impact(),
    }


def get_timeline() -> List[Dict]:
    return [
        {"phase": "Month 0–2", "status": "Stable", "evidence": "Precision ~94.2% and recall ~91.7% with limited drift.", "inference": "Baseline drift is within acceptable monitoring limits.", "hypothesis": "No material degradation yet."},
        {"phase": "Month 3", "status": "Early drift", "evidence": "UPI campaign shifts transaction size and frequency distributions.", "inference": "Distributional changes begin to affect high-value transfer behavior.", "hypothesis": "Environment-driven shift is emerging."},
        {"phase": "Month 4–5", "status": "Widening feature drift", "evidence": "IP reputation and device spoofing metrics begin to drift materially.", "inference": "The model lacks resilience to malicious session manipulations.", "hypothesis": "Adversarial and upstream data changes are compounding."},
        {"phase": "Month 6", "status": "Label delay", "evidence": "Fraud labeling latency grows and review queue backlog emerges.", "inference": "Training data quality begins to deteriorate.", "hypothesis": "Stale labels are reducing the effective learning signal."},
        {"phase": "Month 7–8", "status": "Economic shift", "evidence": "UPI limits and inflation increase transaction magnitude and frequency volatility.", "inference": "The target fraud distribution is moving faster than the model can adapt.", "hypothesis": "Baseline drift is no longer well-represented by training data."},
        {"phase": "Month 9–10", "status": "Cross-border attack", "evidence": "Cross-border fraud creates a clear change in F04 and F15.", "inference": "Risk patterns shift away from historical domestic fraud behavior.", "hypothesis": "The model is failing to adapt to a new fraud archetype."},
        {"phase": "Month 11–12", "status": "Feedback loop driven degradation", "evidence": "Missed fraud cases are later treated as legitimate labels and reintroduced to retraining.", "inference": "The training signal becomes contaminated and the degradation accelerates.", "hypothesis": "A data feedback loop is amplifying the model loss."},
    ]

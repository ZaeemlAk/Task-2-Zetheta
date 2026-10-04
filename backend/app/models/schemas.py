from pydantic import BaseModel


class PerformanceRecord(BaseModel):
    week_id: int
    week_start_date: str
    total_transactions: int
    total_fraud_flagged: int
    total_fraud_confirmed: int
    true_positives: int
    false_positives: int
    false_negatives: int
    true_negatives: int
    precision: float
    recall: float
    f1_score: float
    auc_roc: float
    avg_inference_latency_ms: float
    alert_triggered: bool


class DriftFeatureRecord(BaseModel):
    week_id: int
    feature_name: str
    mean: float
    std_dev: float
    median: float
    percentile_5: float
    percentile_25: float
    percentile_75: float
    percentile_95: float
    skewness: float
    kurtosis: float
    psi_vs_baseline: float
    ks_statistic: float
    ks_p_value: float
    js_divergence: float
    null_percentage: float
    drift_flag: bool


class AlertConfig(BaseModel):
    psi_warning: float = 0.1
    psi_critical: float = 0.2
    precision_drop_warning: float = 0.03
    precision_drop_critical: float = 0.08
    recall_drop_warning: float = 0.05
    recall_drop_critical: float = 0.12
    quality_drift_warning: float = 0.2
    business_impact_warning: float = 1_000_000


class InvestigationRequest(BaseModel):
    force_recompute: bool = False


class EventRecord(BaseModel):
    event_date: str
    category: str
    description: str
    severity: str
    affected_features: str

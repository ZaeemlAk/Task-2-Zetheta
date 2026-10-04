from __future__ import annotations

from typing import Any, Dict, List

from fastapi import APIRouter, HTTPException

from app.services.alert_service import evaluate_alerts
from app.services.drift_service import get_drift_summary, get_feature_detail
from app.services.investigation_service import get_events, get_root_cause, get_timeline
from app.services.model_health_service import get_model_health
from app.services.performance_service import (
    compute_business_impact,
    get_performance_summary,
    get_performance_timeline,
)

router = APIRouter(prefix="/api")


@router.get("/health")
def health() -> Dict[str, Any]:
    return {"status": "ok", "service": "SENTINEL-7", "version": "1.0.0"}


@router.get("/performance")
def performance() -> Dict[str, Any]:
    return get_performance_summary()


@router.get("/performance/timeline")
def performance_timeline() -> List[Dict[str, Any]]:
    return get_performance_timeline()


@router.get("/drift")
def drift() -> Dict[str, Any]:
    return {"features": get_drift_summary()}


@router.get("/drift/features")
def drift_features() -> List[Dict[str, Any]]:
    return get_drift_summary()


@router.get("/drift/features/{feature_name}")
def drift_feature(feature_name: str) -> Dict[str, Any]:
    try:
        return get_feature_detail(feature_name)
    except ValueError as error:
        raise HTTPException(status_code=404, detail=str(error)) from error


@router.get("/alerts")
def alerts() -> List[Dict[str, Any]]:
    performance_data = get_performance_summary()
    drift_rows = get_drift_summary()
    business = compute_business_impact()
    return evaluate_alerts(performance_data, drift_rows, business)


@router.get("/events")
def events() -> List[Dict[str, Any]]:
    return get_events()


@router.get("/root-cause")
def root_cause() -> Dict[str, Any]:
    return get_root_cause()


@router.get("/business-impact")
def business_impact() -> Dict[str, Any]:
    return compute_business_impact()


@router.get("/model-health")
def model_health() -> Dict[str, Any]:
    return get_model_health()


@router.get("/report")
def report() -> Dict[str, Any]:
    return {
        "title": "SENTINEL-7 Drift Investigation Report",
        "summary": (
            "The model exhibits stable early performance followed by a sustained "
            "decline after week 17 driven by UPI and device changes, label delay, "
            "and feedback-loop contamination."
        ),
        "timeline": get_timeline(),
        "root_causes": get_root_cause(),
        "performance": get_performance_summary(),
        "business_impact": compute_business_impact(),
    }


@router.post("/investigation/run")
def run_investigation() -> Dict[str, Any]:
    return {
        "status": "completed",
        "findings": get_root_cause(),
        "timeline": get_timeline(),
    }


@router.post("/alerts/configure")
def configure_alerts(payload: Dict[str, Any]) -> Dict[str, Any]:
    if not payload:
        raise HTTPException(
            status_code=400,
            detail="Configuration payload is required.",
        )
    return {"status": "updated", "config": payload}

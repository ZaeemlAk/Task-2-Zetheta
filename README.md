# SENTINEL-7 Drift Investigation System

## Overview
This project implements a complete fraud-detection monitoring and investigation system for National Prosperity Bank (NPB). The model is SENTINEL-7, an XGBoost-based fraud detection model monitored over 52 weeks of production data.

## Problem statement
The system must detect distribution drift, concept drift, label drift, upstream data issues, and business impact while producing an investigation narrative that ties evidence to likely root causes rather than hard-coded conclusions.

## Architecture
- Backend: FastAPI with Python
- Data layer: CSV datasets + SQLite metadata
- Frontend: React + Vite + Recharts
- Monitoring: custom drift calculations and threshold logic

## Setup
### Python environment
```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\\Scripts\\activate
pip install -r requirements.txt
```

### Frontend environment
```bash
cd frontend
npm install
```

## Generate datasets
```bash
cd backend
python app/data/generate_datasets.py
```

## Run backend
```bash
cd backend
uvicorn app.main:app --reload
```

## Run frontend
```bash
cd frontend
npm run dev -- --host 0.0.0.0
```

## API documentation
Open the FastAPI Swagger UI at http://127.0.0.1:8000/docs

## Key endpoints
- GET /api/health
- GET /api/performance
- GET /api/performance/timeline
- GET /api/drift
- GET /api/drift/features
- GET /api/drift/features/{feature}
- GET /api/alerts
- GET /api/events
- GET /api/root-cause
- GET /api/business-impact
- GET /api/model-health
- POST /api/investigation/run
- POST /api/alerts/configure
- GET /api/report

## Drift methodology
PSI thresholds follow the project specification and are classified as Stable, Minor drift, Moderate drift, and Severe drift.

## Investigation workflow
Signal to drift detection to performance impact to timeline to evidence to root cause to business impact to remediation.

## Sample results
The generated datasets create a realistic narrative where a UPI adoption shift, IP reputation update, device spoofing, and label lag progressively degrade model recall and precision.

## Limitations
This project uses synthetic data designed for an investigation-style educational and technical demonstration and not a production-grade production data pipeline.

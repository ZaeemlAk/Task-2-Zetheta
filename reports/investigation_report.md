# SENTINEL-7 Investigation Report

## Executive Summary
The model shows an early stable operating envelope, then a sustained decline after week 17. The evidence indicates a combination of feature drift, label lag, and a feedback loop in retraining.

## Investigation Objective
Determine when degradation started, which features drifted, whether concept drift occurred, and which causes were operational versus statistical.

## Root Causes
- UPI adoption and transaction profile shift
- IP reputation feed change
- Device spoofing and app redesign telemetry change
- Labeling delay and feedback contamination
- Monitoring blind spots

## Business Impact
Estimated fraud exposure is approximately INR 15 Crore, with false-positive and missed-fraud cost compounding the business loss.

## Remediation Plan
1. Retrain on revised, high-quality labels.
2. Add champion-challenger evaluation.
3. Recalibrate threshold and guardrail alerting.
4. Repair upstream data and monitoring for feature freshness.
5. Prevent feedback-loop contamination by separating review outcomes from training labels.

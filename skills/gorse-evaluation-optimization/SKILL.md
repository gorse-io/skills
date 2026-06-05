---
name: gorse-evaluation-optimization
description: "Use when helping data, ML, or product teams evaluate Gorse recommendation quality, choose metrics, tune feedback signals, and improve online outcomes."
version: 1.0.0
author: Gorse
license: MIT
metadata:
  hermes:
    tags: [gorse, evaluation, optimization, metrics]
    related_skills: []
---

# Gorse Evaluation Optimization

## Overview

Move users from “Gorse works” to “Gorse improves product outcomes.” Focus on measurable goals, feedback definitions, offline sanity checks, online experiments, and iterative tuning.

## Define Product Goal

Identify whether the product wants clicks, likes, purchases, retention, dwell time, discovery, or diversity. Feedback types and metrics should match the goal.

## Offline Metrics

Use Hit Rate, Precision@K, Recall@K, and NDCG@K for regression checks. They are useful but do not replace online experiments.

## Online Metrics

Track CTR, CVR, purchase/favorite/star rate, retention, dwell time, and negative feedback rate. Use guardrails for latency, diversity, freshness, and complaint/hide rate.

## Optimization Levers

Improve event tracking, item metadata, read feedback, recommender mix, cache freshness, and ranker choice. Use FM or LLM rankers only when data volume and latency/cost justify them.

## Common Pitfalls

1. Optimizing clicks when satisfaction matters.
2. No baseline or holdout.
3. Ignoring cold start.
4. Overfitting offline metrics.
5. Not logging served recommendations.

## Verification Checklist

- [ ] The user's goal is mapped to users, items, feedback, configuration, or deployment state.
- [ ] Claims are grounded in the current Gorse docs/source or live API output.
- [ ] Examples use placeholders instead of secrets.
- [ ] The next action is clear and testable.

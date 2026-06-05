---
name: gorse-recommendation-pipeline
description: "Use when explaining how Gorse generates recommendations through retrieval, ranking, filtering, replacement, caching, and master-worker-server responsibilities."
version: 1.0.0
author: Gorse
license: MIT
metadata:
  hermes:
    tags: [gorse, pipeline, retrieval, ranking]
    related_skills: []
---

# Gorse Recommendation Pipeline

## Overview

Explain how Gorse turns users, items, and feedback into recommendations. The core model is retrieval plus ranking: multiple recommenders generate candidates, rankers and filters shape the final output.

## Architecture

1. Data source layer stores users, items, and feedback.
2. Retrieval layer generates candidates.
3. Ranking layer scores, filters, sorts, and returns candidates.

Node roles: master trains/manages tasks, workers generate offline recommendations, servers serve APIs.

## Retrieval Sources

- Latest items for freshness.
- Non-personalized popular/rule-ranked items.
- Item-to-item similar items.
- User-to-user similar users.
- Collaborative filtering latent recommendations.
- External custom recommenders.

## Ranking Options

- `none`: simple retrieval baseline.
- `fm`: factorization machine with structured signals.
- `llm`: text/context-aware ranking when latency and cost fit.

## Filtering and Cache

Gorse can remove hidden items, apply category filters, remove read items, apply replacement rules, and serve cached offline results. Empty results often mean retrieval produced no candidates or filters removed them all.

## Common Pitfalls

1. Confusing retrieval with ranking; ranking cannot fix zero candidates.
2. Configuring too few recommenders.
3. Ignoring asynchronous task/cache updates.
4. Applying strict categories with sparse data.

## Verification Checklist

- [ ] The user's goal is mapped to users, items, feedback, configuration, or deployment state.
- [ ] Claims are grounded in the current Gorse docs/source or live API output.
- [ ] Examples use placeholders instead of secrets.
- [ ] The next action is clear and testable.

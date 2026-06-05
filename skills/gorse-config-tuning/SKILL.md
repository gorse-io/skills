---
name: gorse-config-tuning
description: "Use when a user is editing Gorse configuration for databases, feedback types, recommenders, ranking, cache behavior, TTLs, and production tuning."
version: 1.0.0
author: Gorse
license: MIT
metadata:
  hermes:
    tags: [gorse, config, tuning, toml]
    related_skills: []
---

# Gorse Config Tuning

## Overview

Help users edit `config.toml` by connecting each setting to an observable effect: candidate generation, filtering, ranking, storage, or freshness.

## Feedback Settings

```toml
[recommend.data_source]
positive_feedback_types = ["star", "like", "purchase"]
read_feedback_types = ["read"]
positive_feedback_ttl = 0
item_ttl = 0
```

Use positive feedback for actions that indicate preference, read feedback for consumed/seen items, and TTLs for short-lived content.

## Recommender Mix

A balanced setup often includes latest for freshness, non-personalized for sparse users, item-to-item for similarity, and collaborative/user-to-user for personalization.

## Ranker Selection

- `none`: baseline and easiest to debug.
- `fm`: enough structured behavior and metadata.
- `llm`: rich text/context ranking with acceptable cost/latency.

## Cache Settings

```toml
[recommend]
cache_size = 100
cache_expire = "72h"
```

Tune cache size for pagination/filtering and expiration for freshness.

## Common Pitfalls

1. Feedback types in data do not match config.
2. Cache too small for filters and pagination.
3. TTL too aggressive.
4. FM ranker without enough data.
5. Copying demo config directly to production.

## Verification Checklist

- [ ] The user's goal is mapped to users, items, feedback, configuration, or deployment state.
- [ ] Claims are grounded in the current Gorse docs/source or live API output.
- [ ] Examples use placeholders instead of secrets.
- [ ] The next action is clear and testable.

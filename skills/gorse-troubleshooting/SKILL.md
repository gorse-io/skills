---
name: gorse-troubleshooting
description: "Use when diagnosing Gorse problems such as empty recommendations, stale results, failed tasks, data import issues, dashboard access, storage errors, and cluster connectivity."
version: 1.0.0
author: Gorse
license: MIT
metadata:
  hermes:
    tags: [gorse, troubleshooting, debugging]
    related_skills: []
---

# Gorse Troubleshooting

## Overview

Diagnose Gorse issues systematically. Start with the symptom, then check data, configuration, tasks, cache, filters, and deployment health.

## Empty Recommendations Checklist

1. Does the user exist?
2. Does the item catalog exist?
3. Does the user have positive feedback?
4. Do feedback types match `positive_feedback_types`?
5. Have recommendation tasks completed?
6. Are items hidden or expired by TTL?
7. Are category filters too strict?
8. Is cache populated and unexpired?
9. Is the selected recommender appropriate for the data volume?

## Stale Recommendations

Check task schedule, cache update time, feedback timestamps, worker health, and whether writes go to the same store the cluster reads.

## Dashboard/API Unreachable

Check process/container status, port mapping, firewall/reverse proxy, storage connection errors, and the endpoint being used.

## Common Pitfalls

1. Skipping task status.
2. Wrong feedback type.
3. Bad timestamp units/timezone.
4. Debugging only cold users.
5. Ignoring filters.

## Verification Checklist

- [ ] The user's goal is mapped to users, items, feedback, configuration, or deployment state.
- [ ] Claims are grounded in the current Gorse docs/source or live API output.
- [ ] Examples use placeholders instead of secrets.
- [ ] The next action is clear and testable.

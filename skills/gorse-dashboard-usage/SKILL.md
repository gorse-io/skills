---
name: gorse-dashboard-usage
description: "Use when a user needs help using the Gorse web dashboard for data management, recommendation pipeline editing, task progress, and system monitoring."
version: 1.0.0
author: Gorse
license: MIT
metadata:
  hermes:
    tags: [gorse, dashboard, ui, admin]
    related_skills: []
---

# Gorse Dashboard Usage

## Overview

Help users who prefer visual administration. The dashboard is useful for data inspection, task status, recommendation pipeline configuration, and system health.

## Common Workflows

- Open local dashboard at `http://localhost:8088`.
- Check task progress before expecting generated recommendations.
- Verify users, items, feedback, hidden flags, and feedback types.
- Inspect or edit recommendation pipeline settings.
- Monitor nodes and service health in distributed deployments.

## Troubleshooting in Dashboard

If recommendations are empty, inspect data first: target user exists, items exist, feedback exists, items are not hidden, tasks are successful, and filters are not too strict.

## Common Pitfalls

1. Changing pipeline settings but not waiting for tasks.
2. Checking items but not feedback.
3. Overlooking hidden items.
4. Misreading stale cache as poor model quality.
5. Not verifying behavior with the recommendation API.

## Verification Checklist

- [ ] The user's goal is mapped to users, items, feedback, configuration, or deployment state.
- [ ] Claims are grounded in the current Gorse docs/source or live API output.
- [ ] Examples use placeholders instead of secrets.
- [ ] The next action is clear and testable.

---
name: gorse-cli-usage
description: "Use when an administrator or developer wants to install and use gorse-cli to inspect nodes, tasks, data, configuration, or recommendation API state."
version: 1.0.0
author: Gorse
license: MIT
metadata:
  hermes:
    tags: [gorse, cli, administration]
    related_skills: []
---

# Gorse Cli Usage

## Overview

Use `gorse-cli` for operational and administrative workflows. Keep command descriptions concise and avoid redundant wording like “from Gorse admin API” because the CLI is already an admin tool.

## When to Use

- Inspect cluster status.
- Check nodes and task progress.
- Script Gorse administration.
- Debug API state without the dashboard.

## Command Categories

- Cluster inspection: nodes, health, membership.
- Task inspection: task list and progress.
- Data operations: users, items, feedback.
- Recommendation checks: fetch recommendations for test users.
- Context/configuration: endpoint, token, output format.

## Safety

Treat delete, purge, reset, and overwrite commands as destructive. Confirm endpoint and credentials before writes. Prefer read-only inspection first.

## Common Pitfalls

1. Wrong endpoint.
2. Missing production credentials.
3. Using write commands while debugging.
4. Checking only CLI output without cross-checking dashboard/API.

## Verification Checklist

- [ ] The user's goal is mapped to users, items, feedback, configuration, or deployment state.
- [ ] Claims are grounded in the current Gorse docs/source or live API output.
- [ ] Examples use placeholders instead of secrets.
- [ ] The next action is clear and testable.

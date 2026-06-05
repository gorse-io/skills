---
name: gorse-deployment
description: "Use when deploying Gorse with Docker, Docker Compose, or distributed master-worker-server topologies and choosing data/cache storage for production."
version: 1.0.0
author: Gorse
license: MIT
metadata:
  hermes:
    tags: [gorse, deployment, docker, operations]
    related_skills: []
---

# Gorse Deployment

## Overview

Guide deployment from local all-in-one to production distributed clusters. Cover topology, storage, ports, health checks, logs, upgrades, and rollback.

## Deployment Modes

All-in-one is best for demos and small installs:

```bash
docker run -p 8088:8088 zhenghaoz/gorse-in-one --playground
```

Distributed deployments separate master, worker, and server roles. Scale workers for offline generation throughput and servers for API traffic.

## Storage Planning

Use a durable data store for users/items/feedback and a cache store for recommendation outputs. Typical durable stores include PostgreSQL, MySQL/MariaDB, MongoDB, and ClickHouse. Redis is common for low-latency cache.

## Operational Checklist

- Keep credentials out of images and public repos.
- Expose only needed ports.
- Add health checks for API and stores.
- Collect logs per role.
- Monitor task progress and recommendation cache freshness.

## Common Pitfalls

1. Running multiple masters unintentionally.
2. Scaling servers but not workers.
3. Using ephemeral storage for durable feedback.
4. No task monitoring.
5. Exposing admin endpoints publicly without appropriate controls.

## Verification Checklist

- [ ] The user's goal is mapped to users, items, feedback, configuration, or deployment state.
- [ ] Claims are grounded in the current Gorse docs/source or live API output.
- [ ] Examples use placeholders instead of secrets.
- [ ] The next action is clear and testable.

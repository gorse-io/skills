---
name: gorse-contributor-development
description: "Use when helping contributors understand the Gorse codebase, development workflow, source layout, testing approach, and where to implement APIs, storage, recommenders, CLI commands, or docs."
version: 1.0.0
author: Gorse
license: MIT
metadata:
  hermes:
    tags: [gorse, contributors, development, go]
    related_skills: []
---

# Gorse Contributor Development

## Overview

Orient contributors by source area and workflow, then point to the smallest relevant tests and verification commands.

## Source Map

- `cmd/`: binaries and CLI entry points.
- `server/`: REST API serving and online recommendation behavior.
- `master/`: tasks, training, configuration, and cluster management.
- `worker/`: offline recommendation generation.
- `storage/`: data, cache, and vector store implementations.
- `logics/`: recommenders such as item-to-item, user-to-user, CF, external.
- `model/`: ML models and rankers.
- `dataset/`: dataset construction and indexing.
- `common/`: shared utilities, math, logging, parallel helpers.
- `protocol/`: generated protocol definitions.

## Development Workflow

Start from a clean branch, read the closest implementation and tests, add/update tests, run targeted package tests, then broader tests before pushing. Update docs/CLI help when user-facing behavior changes.

## Feature Placement

New REST endpoint: inspect `server/` or `master/`. New storage backend: implement interfaces under `storage/`. New recommender: inspect `logics/` and worker pipeline. New ranker/model: inspect `model/` and config wiring. New CLI command: inspect `cmd/gorse-cli/`.

## Common Pitfalls

1. Changing behavior without tests.
2. Testing only one storage backend.
3. Forgetting config defaults/parsing/docs.
4. Verbose CLI help wording.
5. Editing generated protocol files manually.

## Verification Checklist

- [ ] The user's goal is mapped to users, items, feedback, configuration, or deployment state.
- [ ] Claims are grounded in the current Gorse docs/source or live API output.
- [ ] Examples use placeholders instead of secrets.
- [ ] The next action is clear and testable.

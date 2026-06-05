---
name: gorse-sdk-integration
description: "Use when a developer wants to choose or use a Gorse SDK instead of raw REST calls, including integration patterns and language client guidance."
version: 1.0.0
author: Gorse
license: MIT
metadata:
  hermes:
    tags: [gorse, sdk, client, integration]
    related_skills: []
---

# Gorse Sdk Integration

## Overview

Help developers choose language-native clients or raw REST. Verify current SDK repositories/packages before giving exact installation commands.

## REST vs SDK

Use REST for small scripts, unavailable/outdated SDKs, or full API coverage. Use SDKs when typed models, errors, and shared retry handling improve production code.

## Integration Architecture

1. Product backend receives behavior events.
2. Backend writes feedback to Gorse.
3. Backend syncs catalog items.
4. Backend requests recommendations.
5. Backend applies final authorization/business rules.
6. Backend logs exposure and conversion outcomes.

Avoid calling Gorse directly from public frontend code when credentials are required.

## Common Operations

Create/update users and items, insert feedback in batches, get recommendations, get similar items/users if supported, handle API errors and retries.

## Common Pitfalls

1. Embedding secrets in frontend apps.
2. Treating SDK retries as durable event storage.
3. Sending one event per request at high volume.
4. Not version-pinning clients.
5. Ignoring API compatibility.

## Verification Checklist

- [ ] The user's goal is mapped to users, items, feedback, configuration, or deployment state.
- [ ] Claims are grounded in the current Gorse docs/source or live API output.
- [ ] Examples use placeholders instead of secrets.
- [ ] The next action is clear and testable.

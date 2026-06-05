---
name: gorse-api-integration
description: "Use when a developer wants to integrate an application backend with Gorse REST APIs for users, items, feedback, recommendations, and write-back behavior."
version: 1.0.0
author: Gorse
license: MIT
metadata:
  hermes:
    tags: [gorse, api, rest, integration]
    related_skills: []
---

# Gorse Api Integration

## Overview

Help application developers connect a backend service to Gorse. Prefer concrete HTTP examples, then point to SDKs when users want language-native clients.

## When to Use

- The user asks how to call Gorse from an app.
- The user needs examples for users, items, feedback, or recommendations.
- The user wants automatic read/write-back behavior.

## Base URL

Local all-in-one demo: `http://127.0.0.1:8088`. Production should use the deployed server endpoint and configured auth.

## Insert Feedback

```bash
curl -X POST 'http://127.0.0.1:8088/api/feedback' \
  -H 'Content-Type: application/json' \
  -d '[{"FeedbackType":"like","UserId":"u1","ItemId":"i1","Value":1,"Timestamp":"2026-01-01T00:00:00Z"}]'
```

## Fetch Recommendations

```bash
curl 'http://127.0.0.1:8088/api/recommend/u1?n=10'
```

## Automatic Read Feedback

```bash
curl 'http://127.0.0.1:8088/api/recommend/u1?write-back-type=read&n=10'
curl 'http://127.0.0.1:8088/api/recommend/u1?write-back-type=read&write-back-delay=10m&n=10'
```

## Common Pitfalls

1. Importing only items without feedback.
2. Calling recommendations before offline tasks finish.
3. Not recording reads, causing repeated consumed items.
4. Sending local timestamps without timezone; prefer UTC.
5. Leaking API keys in frontend code.

## Verification Checklist

- [ ] The user's goal is mapped to users, items, feedback, configuration, or deployment state.
- [ ] Claims are grounded in the current Gorse docs/source or live API output.
- [ ] Examples use placeholders instead of secrets.
- [ ] The next action is clear and testable.

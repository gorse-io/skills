---
name: gorse-data-modeling
description: "Use when a user needs to map business entities and events into Gorse users, items, feedback, labels, categories, timestamps, and feedback type configuration."
version: 1.0.0
author: Gorse
license: MIT
metadata:
  hermes:
    tags: [gorse, data-modeling, feedback, items]
    related_skills: []
---

# Gorse Data Modeling

## Overview

Translate business data into Gorse `User`, `Item`, and `Feedback` records. Good recommendation quality starts with stable IDs, meaningful positive feedback, useful item metadata, and correct read feedback.

## When to Use

- The user asks how to import their own data.
- The user asks what should be a user, item, or feedback.
- The user has empty or poor recommendations and may have modeled events incorrectly.

## Core Models

- `User`: recommendation subject. Use a stable `UserId`; optional labels describe region, role, plan, language, or interests.
- `Item`: recommendable object. Use a stable `ItemId`; `IsHidden` excludes items; `Categories` support filters; `Timestamp` supports freshness and TTL; `Labels` describe content.
- `Feedback`: interaction. `FeedbackType`, `UserId`, `ItemId`, `Value`, and `Timestamp` drive learning and filtering.

## Choosing Feedback Types

| Business event | Suggested type | Role |
| --- | --- | --- |
| Impression/view | `read` or `view` | Seen/read feedback |
| Click/open | `click` | Weak positive |
| Like/favorite/star | `like`, `star` | Strong positive |
| Purchase/subscribe | `purchase` | Very strong positive |
| Hide/dislike | `dislike`, `not_interested` | Negative/exclusion signal |

Example config:

```toml
[recommend.data_source]
positive_feedback_types = ["like", "star", "purchase"]
read_feedback_types = ["read"]
positive_feedback_ttl = 0
item_ttl = 0
```

## Common Pitfalls

1. Treating impressions as strong positive feedback.
2. Changing IDs and losing historical signal continuity.
3. Missing or malformed timestamps.
4. Overusing narrow categories until no candidates remain.
5. Hiding active items with `IsHidden`.

## Verification Checklist

- [ ] The user's goal is mapped to users, items, feedback, configuration, or deployment state.
- [ ] Claims are grounded in the current Gorse docs/source or live API output.
- [ ] Examples use placeholders instead of secrets.
- [ ] The next action is clear and testable.

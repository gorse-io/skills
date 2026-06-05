---
name: gorse-quickstart
description: "Use when a user is trying Gorse for the first time and needs to start a local instance, load sample feedback, open the dashboard, and fetch initial recommendations."
version: 1.0.0
author: Gorse
license: MIT
metadata:
  hermes:
    tags: [gorse, quickstart, docker, dashboard]
    related_skills: []
---

# Gorse Quickstart

## Overview

Guide first-time users from zero to a working local Gorse instance. Keep the path short: start the all-in-one image, open the dashboard, insert a small amount of feedback, wait for recommendation tasks, and query the recommendation API.

## When to Use

- The user asks how to try Gorse locally.
- The user wants a minimal demo before integrating their own data.
- The user asks why the dashboard or API does not show recommendations yet.

## Fast Path

```bash
docker run -p 8088:8088 zhenghaoz/gorse-in-one --playground
```

Open `http://localhost:8088`. The playground imports GitHub repository demo data. Wait until item-to-item or recommendation-generation tasks complete on the dashboard task page before expecting good recommendation results.

## Example Feedback and Recommendation

```bash
read -d '' JSON << 'EOF'
[
  { "FeedbackType": "star", "UserId": "bob", "ItemId": "ollama:ollama", "Value": 1.0, "Timestamp": "2022-02-24" },
  { "FeedbackType": "star", "UserId": "bob", "ItemId": "huggingface:transformers", "Value": 1.0, "Timestamp": "2022-02-25" },
  { "FeedbackType": "star", "UserId": "bob", "ItemId": "vllm-project:vllm", "Value": 1.0, "Timestamp": "2022-02-27" }
]
EOF

curl -X POST http://127.0.0.1:8088/api/feedback -H 'Content-Type: application/json' -d "$JSON"
curl 'http://127.0.0.1:8088/api/recommend/bob?n=10'
```

## Common Pitfalls

1. Expecting recommendations immediately before background tasks finish.
2. Testing with a user that has no positive feedback.
3. Using the wrong local port; the playground uses `8088`.
4. Forgetting hidden items, TTL, read feedback, or category filters can remove candidates.

## Verification Checklist

- [ ] The user's goal is mapped to users, items, feedback, configuration, or deployment state.
- [ ] Claims are grounded in the current Gorse docs/source or live API output.
- [ ] Examples use placeholders instead of secrets.
- [ ] The next action is clear and testable.

---
name: gorse-use-case-recipes
description: "Use when designing Gorse solutions for common scenarios such as e-commerce, news, video, music, developer platforms, learning platforms, jobs, and SaaS recommendations."
version: 1.0.0
author: Gorse
license: MIT
metadata:
  hermes:
    tags: [gorse, recipes, use-cases]
    related_skills: []
---

# Gorse Use Case Recipes

## Overview

Translate a product scenario into a concrete Gorse setup: users, items, feedback types, categories, freshness needs, and first API call.

## Recipe Template

1. Who is the user?
2. What is the item?
3. What events are positive feedback?
4. What events are read/seen feedback?
5. What categories or labels matter?
6. How fresh must results be?
7. What endpoint does the app call first?

## Examples

### E-commerce

User is shopper, item is SKU, positive feedback includes `favorite`, `add_to_cart`, `purchase`, read feedback is `view`, categories include department/brand/store.

### News or Content Feed

User is reader, item is article/post/video, positive feedback includes `click`, `read>=30`, `like`, `share`, read feedback is `impression` or `read`, freshness is high.

### Developer Repositories

User is developer, item is repository, positive feedback includes `star`, `fork`, `watch`, categories include language/topic/owner.

### Learning Platform

User is learner, item is course/lesson, positive feedback includes `complete`, `save`, `high_rating`, and categories include subject/difficulty/language.

## Common Pitfalls

1. Skipping read feedback in feeds.
2. Using purchase-only feedback for sparse catalogs.
3. No freshness strategy for time-sensitive content.
4. Leaking tenant/permission boundaries.
5. Copying a recipe without adapting product goals.

## Verification Checklist

- [ ] The user's goal is mapped to users, items, feedback, configuration, or deployment state.
- [ ] Claims are grounded in the current Gorse docs/source or live API output.
- [ ] Examples use placeholders instead of secrets.
- [ ] The next action is clear and testable.

---
name: gorse-recommendation-tuning
description: Use when configuring Gorse candidate retrieval, ranking, cold-start fallback, repeated recommendations, or recommendation-quality evaluation as an application operator.
---

# Gorse Recommendation Tuning

Help a Gorse user choose and validate a recommendation pipeline. This is an
application configuration workflow, not a guide to modifying Gorse source.

## Establish the objective and baseline

1. Identify the running Gorse version, effective configuration, dataset size,
   event definitions, update latency target, and resource budget. Check Dashboard
   RecFlow as well as the file: saved pipeline settings take precedence over file
   defaults. Use the matching release's documentation/template; do not paste an
   entire development config.
2. State the product goal: new-item discovery, personal relevance, repeat purchases,
   similar-item navigation, or a measurable engagement/conversion outcome.
3. Check that real user/item/feedback records have arrived and configured positive,
   read, and negative rules match those records. Do not tune models around missing
   events, fabricated exposure records, future timestamps, or empty labels.
4. Save the existing configuration and baseline results. Agree on a reversible
   rollout and evaluation window before changing production behavior.
5. Separate candidate availability, ranking quality, and serving filters. An item
   absent from every candidate source cannot be rescued by a more expensive ranker.

## Select candidate sources

| Available information / need | Candidate choice | Verify first |
| --- | --- | --- |
| New users or a fresh catalog | `latest` or a non-personalized rule | Item timestamps, eligibility, and enough candidates |
| Tags or externally generated embeddings | Item-to-item | Correct labels field and consistent value shape |
| Users with overlapping preferences | User-to-user | Profile labels or sufficient shared positive interactions |
| Enough real historical positive interactions | Collaborative filtering | Enabled training, usable dataset, model/task completion |
| Business-specific candidates from another service | External recommender | Endpoint trust, failure handling, and IDs present in Gorse |

- Non-personalized `score` is a numeric Expr expression; `filter` is boolean.
  Scores are ordered descending. Confirm the feedback types counted by the rule
  actually qualify as positive under the data-source configuration.
- For item-to-item, `embedding` and `tags` require a `column` such as
  `item.Labels.embedding` or `item.Labels.topics`; interaction-based `users` does
  not take that content column. Verify vector dimensions/model consistency before
  choosing embedding similarity. Do not promise a backend metric without checking
  the deployed release and vector-store capabilities.
- User-to-user supports content or interaction signals. Use the target template's
  `[[recommend.user-to-user]]` schema; do not transpose a legacy singular section
  from an older example without checking it.
- Configure collaborative filtering with `type = "mf"` only when appropriate data
  exists. More training epochs or hyperparameter trials consume resources; first
  confirm the model uses the intended events and has completed training.
- An external recommender's script returns item IDs; unknown IDs are ignored.
  Its documented HTTP `fetch` runs synchronously and is not browser Fetch. Review
  scripts and destination hosts before execution; do not embed production secrets.

## Wire sources into ranking and fallback

Defining a named source is not enough: select it in the ranker's candidate list.
Use the documented names `latest`, `collaborative`, `non-personalized/NAME`,
`item-to-item/NAME`, and `user-to-user/NAME` where supported by the target release.
Check external-source naming against that release rather than guessing a prefix.

This **configuration fragment**, not a complete deployment config, starts from
catalog tags and preserves a simple cold-start path. Replace the labels field and
name with values that exist in the application's data:

```toml
[[recommend.item-to-item]]
name = "catalog_tags"
type = "tags"
column = "item.Labels.topics"

[recommend.ranker]
type = "none"
recommenders = ["item-to-item/catalog_tags", "latest"]

[recommend.fallback]
recommenders = ["latest"]
```

- Start with `none` to inspect candidate behavior without an extra learned ranker;
  it is not a claim that this maximizes product quality.
- Consider `fm` once real positive/read/negative feedback supports learning. Inspect
  its own training status and metrics separately from collaborative filtering.
- For `llm`, supply query/document templates and configure the complete reranking
  endpoint under `[recommend.ranker.reranker_api]`, plus model and authentication.
  Confirm the documented Jina/Cohere-style text request and `results` response;
  an OpenAI-compatible chat endpoint is not automatically a reranking endpoint.
- Review which user history and item text leave the deployment before enabling a
  remote reranker. Budget for privacy, latency, rate limits, and provider costs.
- Fallback fills candidate shortages, especially cold starts. It does not train a
  personalized model. An empty recommendation configuration yields a latest-only
  baseline in the referenced docs, not evidence of personalization.

## Freshness and repetition

- Inspect master dataset/model tasks, worker generation, and server filtering as
  distinct stages. A successful data write does not mean every cache/model is current.
- Tune `[recommend]` cache size/expiry and model fitting periods against measured
  freshness, storage, CPU, and latency. Do not confuse recommendation cache expiry
  with the separate server response-cache setting.
- New users, active users, and inactive users may have different cache behavior.
  Observe task completion and timestamps rather than repeatedly restarting nodes.
- Enable `[recommend.replacement]` only when recommending already-consumed items
  again is intentional. Its positive/read decay settings alter repeat priorities;
  repetition is not a substitute for fixing incorrect read-feedback classification.
- Keep hidden items and requested categories in the verification set. Category
  filtering can exhaust a small catalog even when unfiltered recommendations work.

## Validate and iterate

1. In an authorized staging instance, compare a new user, an established user, a
   sparse-history user, and category-filtered requests. Inspect actual item IDs,
   hidden/read exclusion, result count, and meaningful catalog coverage.
2. Inspect individual candidate lists or neighbors using the documented APIs,
   Dashboard RecFlow, or the installed CLI's supported commands. Then compare the
   final served recommendations, not just one intermediate list.
3. Wait for required dataset, model, and worker tasks. Do not report old cached
   results as evidence that a new configuration is effective.
4. Review collaborative metrics (including NDCG@10) and FM metrics (including AUC)
   separately. Offline sampled evaluation is not proof of online business impact.
5. Use genuine exposure and outcome events for online positive-feedback rates.
   Compare cohorts or run a controlled experiment when available; avoid drawing
   conclusions from a changed event denominator or test-generated feedback.
6. Change one hypothesis at a time and record configuration/version, data window,
   task completion, quality/freshness/latency observations, and rollback decision.
   If quality falls, restore the approved baseline; do not purge data or retrain
   indiscriminately.

## Official sources

Prepared from docs revision `5cef16bd228c4095de6bbfa0f46832c198a305eb`; re-check
against the deployed release. These are source references, not API-version pins.

- [Pipeline and node responsibilities](https://github.com/gorse-io/docs/blob/main/src/docs/concepts/pipeline.md)
- [RecFlow effective configuration](https://github.com/gorse-io/docs/blob/main/src/docs/dashboard/recflow.md)
- [Configuration schema](https://github.com/gorse-io/docs/blob/main/src/docs/config.md)
- [Candidate recommenders](https://github.com/gorse-io/docs/tree/main/src/docs/concepts/recommenders)
- [Ranking and reranker protocol](https://github.com/gorse-io/docs/blob/main/src/docs/concepts/ranking.md)
- [Repeated-item replacement](https://github.com/gorse-io/docs/blob/main/src/docs/concepts/replacement.md)
- [Online and offline evaluation](https://github.com/gorse-io/docs/blob/main/src/docs/concepts/evaluation.md)

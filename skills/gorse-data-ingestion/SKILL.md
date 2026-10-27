---
name: gorse-data-ingestion
description: "Use when importing or streaming users, items, and real feedback into Gorse; map schemas, choose documented write semantics, and verify ingestion safely."
---

# Gorse Data Ingestion

Help application operators load their own data, not modify Gorse source code.

## Establish the contract and safety boundary

1. Identify the deployed Gorse version, application API endpoint, intended dataset, and whether this is an isolated staging deployment.
2. Check that deployment's `/apidocs` and version-matched documentation before choosing fields, SDK methods, or connector options. The sources below describe a documentation snapshot, not a promise that every deployed release supports it.
3. Obtain explicit approval for the target and scope before any batch write, feedback replay, connector deployment, or import. Do not run examples against a live service automatically.
4. Keep API keys in environment variables or a secret manager; use HTTPS for authenticated remote requests. Do not include secrets or personal data in logs or shared payload examples.
5. Distinguish the application REST key (`[server].api_key`, header `X-API-Key`) from the master admin key (`[master].admin_api_key`). Import/restore and CLI administration are not ordinary application reads.

## Map application data

Use stable application identifiers. `UserId` and `ItemId` must not contain `/`; do not silently rewrite identifiers and break feedback joins.

| Entity | Documented fields and meaning |
| --- | --- |
| User | `UserId` string; `Labels` JSON describing characteristics; `Comment` string for dashboard browsing. |
| Item | `ItemId` string; `IsHidden` boolean; `Categories` string array for recommendation filtering; `Timestamp` for item freshness; `Labels` JSON describing content; `Comment` string. |
| Feedback | `FeedbackType`, `UserId`, `ItemId`, numeric `Value`, and `Timestamp`. The unique key is `(UserId, ItemId, FeedbackType)`, not an event ID or timestamp. |

- Preserve structured JSON labels, such as objects containing topic arrays; do not turn them into comma-joined strings. Labels can be empty. Categories are a separate field, not inferred from a label named `category`.
- Human-supplied labels and embedding vectors can describe items. Do not prescribe a vector dimension or model without the deployment's recommender contract.
- Use actual source timestamps, preferably timezone-explicit RFC3339 values such as `2026-01-01T00:00:00Z`; do not stamp an old import with ingestion time and make old items look fresh.
- A future feedback timestamp delays when feedback takes effect; use it only for an intentional delayed-read policy, not as a timezone workaround.
- Set `Value` from real event strength (for example a rating); the data-source guide allows `0` when unavailable. Confirm feedback value support in the deployed release.
- The REST reference also lists feedback `Comment` and `Updated`; the Kafka page shows feedback `Labels`. Do not assume these are portable across REST, SDKs, and releases; verify the selected interface before forwarding extra fields.
- `IsHidden=true` removes an item from recommendations but permits training use. The guide says hiding is immediate; unhiding waits for recommendation refresh. Do not delete history merely to stop recommending unavailable items.

## Define event meaning before loading feedback

Map application behavior to `[recommend.data_source]` configuration, not to arbitrary event names that training will ignore.

```toml
[recommend.data_source]
positive_feedback_types = ["like", "rating>=4"]
read_feedback_types = ["read", "rating<4"]
negative_feedback_types = ["dislike"]
positive_feedback_ttl = 0
item_ttl = 0
```

This is an illustrative policy to adapt, not a command to apply. Positive and read expressions support `>`, `>=`, `<`, `<=`, and `==` after the feedback type. Store `FeedbackType="rating"` with a numeric value, not `FeedbackType="rating>=4"`.

- Positive feedback means a genuinely desired user action; read feedback means the user saw the item. Explicit dislike is different from a read without subsequent positive feedback.
- Reserve `negative_feedback_types` for genuine explicit rejection. The guide gives it highest priority; do not classify a routine skip or close as explicit dislike.
- `positive_feedback_ttl` and `item_ttl` are in days in the data-source guide; `0` means no expiration. Treat expiry as recommendation eligibility, not a guaranteed physical data deletion API.
- Never manufacture clicks, exposure/read events, likes, or negative examples to fill a sparse dataset or silence training warnings. Cold start has fallback recommenders.
- Record actual displays/actions. Fetching a recommendation does not prove it was displayed. Automatic recommendation writeback is a deliberate approximation, not observed exposure.

## Choose a documented ingestion path

### REST or an application SDK

- Singular inserts: `POST /api/user` and `POST /api/item` take one object.
- Batch inserts: `POST /api/users` and `POST /api/items` take JSON arrays.
- Feedback: `PUT /api/feedback` and `POST /api/feedback` take JSON arrays, but have different duplicate semantics (below).
- Existing entity modifications: `PATCH /api/user/{user-id}` and `PATCH /api/item/{item-id}`. Verify partial-update behavior in the deployment instead of assuming JSON merge semantics for labels.
- Write users/items with their metadata before feedback when possible. `[server].auto_insert_user` and `auto_insert_item` default to `true` in the cited config, but implicit insertion does not supply your catalog metadata. Inspect actual settings.
- Select a bounded batch size appropriate for the deployment; these docs do not establish a universal REST payload limit or transaction guarantee. Keep a source-to-batch manifest and record acknowledged/uncertain batches.
- With an SDK, check which HTTP operation its insertion method actually uses before enabling retries; method names alone do not establish duplicate handling.

### Binary import/restore

The quick start demonstrates `POST /api/restore` with a binary Gorse dump, not arbitrary CSV or JSON. The CLI documents `gorse-cli dump <file>` and `gorse-cli restore <file>`.

**Restore overwrites existing users, items, feedback, and cache data.** Do not execute it on a populated live deployment as a routine incremental import. Confirm approval, backup/recovery, binary compatibility, master/admin endpoint and authentication, and an isolated destination first. Do not invent CSV-import flags or treat a binary dump as a feedback batch.

The quick-start sample import restarts the master to reload imported data immediately. Coordinate any required reload with the operator; do not automatically restart production or assume ordinary REST writes require restarts.

### Kafka Connect streaming

The Kafka guide marks the connector under development. Match the connector artifact and options to its released version before configuring it.

- Install `io.gorse:gorse-kafka-connect` plus runtime dependencies under the worker's `plugin.path`; restart the worker after changing that plugin path.
- Connector class: `io.gorse.gorse4j.connect.GorseSinkConnector`.
- Documented options include `gorse.endpoint`, `gorse.api.key`, `gorse.entity`, `topic.<topic>.entity`, and `gorse.batch.size` (documented default `500`). Entity choices are `user`, `item`, and `feedback`.
- Topic names containing `user`, `item`, or `feedback` can be inferred; set the entity explicitly when inference is ambiguous.
- Record values can be JSON objects/arrays, maps, structs, or arrays/collections of records. Default mapping recognizes Gorse, lower-camel, and snake-case field names.
- Map nested fields with `field.<field>` or `topic.<topic>.field.<field>`, e.g. `topic.events.field.feedback_type=event.type`. Ensure each real event provides its type; do not synthesize a click default.
- The cited page documents label composition through `field.labels.<labelName>` and topic-level equivalents. Check that the installed connector actually supports this before use; older releases can differ.
- The page does not promise exactly-once delivery, a retry policy, or feedback overwrite/accumulation behavior. Establish these from the installed connector contract before replaying offsets; do not invent connector settings or infer semantics from Kafka alone.

## Handle duplicates and uncertain writes

- `PUT /api/feedback` overwrites feedback with the same unique key. Replaying a fixed desired value avoids additive duplication, but can overwrite newer concurrent feedback; preserve timestamps and coordinate replay ownership.
- `POST /api/feedback` accumulates `Value` for an existing key. Repeating a value of `1` can make it `2`; a timeout does not mean the first write failed. Do not blindly retry additive batches.
- Keep source-event deduplication/checkpoints outside Gorse when event-level accounting is required. The documented feedback key cannot retain every repeated event separately.
- After uncertain outcomes, read affected feedback and reconcile against source data before retrying. No idempotency-key header or all-or-nothing batch guarantee is established by these pages.
- Retry transient failures with bounded backoff only after establishing operation semantics. Fix authentication/schema failures instead of looping.

## Verify ingestion without inventing engagement

1. Reconcile source counts after applying the feedback unique key; raw event totals need not equal stored feedback totals. Check write responses (`RowAffected`) but do not use them as the sole proof of correct data.
2. Read back specific users/items and feedback pairs, comparing IDs, labels, categories, values, and timestamps.
3. Page through `GET /api/users`, `/api/items`, and `/api/feedback` with `n` and opaque `cursor`; responses contain `Cursor` and `Users`, `Items`, or `Feedback`. Follow the returned cursor according to the deployed contract; detect repeated cursors rather than looping indefinitely.
4. Inspect dashboard Tasks or, with separately configured admin access, `gorse-cli stats`, `gorse-cli ps`, and `gorse-cli get feedback -n 20`.
5. A successful write is not proof models/caches are refreshed. Check task progress before judging recommendations. FAQ: collaborative training needs positive feedback; click-through training needs read feedback without positive feedback. Correct real-event mapping, not fabricated events.
6. Preview recommendations without writeback. Confirm category membership and hidden-item handling, and report ingestion acceptance separately from recommendation readiness.

## Official sources

Documentation basis: `gorse-io/docs` snapshot `5cef16bd228c4095de6bbfa0f46832c198a305eb`; always recheck deployed-version compatibility.

- Data schema, feedback expressions and duplicate semantics: https://github.com/gorse-io/docs/blob/main/src/docs/concepts/data-source.md
- REST payloads, write responses and readback: https://github.com/gorse-io/docs/blob/main/src/docs/api/restful-api.md
- SDK catalog: https://github.com/gorse-io/docs/blob/main/src/docs/api/README.md
- Kafka options/mapping: https://github.com/gorse-io/docs/blob/main/src/docs/api/kafka-connect.md
- Binary sample import and task readiness: https://github.com/gorse-io/docs/blob/main/src/docs/quick-start.md
- Keys, auto-insertion and data-source settings: https://github.com/gorse-io/docs/blob/main/src/docs/config.md
- Training warnings and exposure tracking: https://github.com/gorse-io/docs/blob/main/src/docs/faq.md
- Admin inspection and restore warning: https://github.com/gorse-io/docs/blob/main/src/docs/gorse-cli.md

---
name: gorse-api-integration
description: "Use when consuming Gorse REST APIs or SDKs for recommendations, category filters, pagination, authentication, and truthful feedback writeback."
---

# Gorse API Integration

Integrate an application with a deployed Gorse service. Do not modify Gorse internals or invent missing client methods.

## Establish the deployed contract

1. Record the Gorse server version and SDK package version. Consult the deployment's `/apidocs`, then match the official documentation and SDK release to that deployment.
2. Use the actual application REST base URL. The quick start uses port `8087` for a cluster's server and `8088` for Gorse-in-one; master HTTP/admin normally uses `8088`. These are examples, not a reason to override operator-provided URLs.
3. Do not invent `/api/v1`, an API-version header, or a negotiation guarantee. The cited docs use `/api/...` and do not establish such versioning mechanisms. Pin client dependencies and recheck request and response contracts on upgrades.
4. The cited REST page shows `/api/recommend/{user-id}` returning string IDs, while score-bearing APIs show `{ "Id": ..., "Score": ... }` objects. SDK versions can expose different models. Inspect the deployed response and installed SDK types before choosing a decoder; do not assume every recommendation call returns the same shape.
5. Source SDK pages explicitly warn APIs can change. If examples and the installed package disagree, use the version's documented public signature; do not guess optional arguments or bypass private client internals.

## Authentication and secret handling

- Application authorization is enabled with `[server].api_key`; send it as `X-API-Key`. The REST guide says authorization is absent by default; absence of a key is not a production security policy.
- Use HTTPS for authenticated remote traffic. Keep the key server-side, outside browser bundles, URLs, logs, and committed examples. Do not use `curl -k` to bypass certificate errors.
- `[master].admin_api_key` and dashboard authentication are separate from the application REST key. The CLI targets master/admin APIs and supports `GORSE_ADMIN_ENDPOINT` and `GORSE_ADMIN_API_KEY`; do not give application clients admin credentials.
- The variables below are application/example inputs, not claimed Gorse configuration overrides. Set them from your approved environment/secret store. Never paste real secrets into shared commands.

## Read recommendations with curl

Read-only Bash template; set `GORSE_ENDPOINT` to an approved HTTPS base URL without a trailing slash, `GORSE_API_KEY` from a secret store, `GORSE_USER_ID_URLENCODED` to a percent-encoded path segment, and `GORSE_CATEGORY` to a real catalog category. User/item IDs cannot contain `/`; percent-encoding is not permission to use otherwise invalid identifiers.

```bash
: "${GORSE_ENDPOINT:?Set the approved application REST endpoint}"
: "${GORSE_API_KEY:?Load the application API key securely}"
: "${GORSE_USER_ID_URLENCODED:?Set a URL-encoded user ID}"
: "${GORSE_CATEGORY:?Set an existing category}"
curl --fail-with-body --silent --show-error --get \
  "${GORSE_ENDPOINT}/api/recommend/${GORSE_USER_ID_URLENCODED}" \
  --header "X-API-Key: ${GORSE_API_KEY}" \
  --header 'Accept: application/json' \
  --data-urlencode 'n=10' \
  --data-urlencode 'offset=0' \
  --data-urlencode "category=${GORSE_CATEGORY}"
```

No `write-back-type` is included, so previewing does not intentionally create read feedback. Inspect HTTP failures rather than parsing an error body as recommendations.

### Choose the endpoint by application need

| Endpoint | Purpose |
| --- | --- |
| `GET /api/recommend/{user-id}` | Personalized recommendation pipeline for a user. |
| `GET /api/latest` | Latest items. |
| `GET /api/non-personalized/{name}` | A configured named non-personalized recommender. |
| `GET /api/collaborative-filtering/{user-id}` | Collaborative filtering results for a user. |
| `GET /api/item-to-item/{name}/{item-id}` | A configured named item-to-item recommender. |
| `GET /api/user-to-user/{name}/{user-id}` | A configured named user-to-user recommender. |
| `POST /api/session/recommend` | Session recommendations from a JSON feedback array; consult the deployed schema before sending. |

The REST page also lists item/user neighbor endpoints. Do not assume a recommender name exists: obtain it from the operator's configuration. Resolve returned item IDs to application metadata or `GET /api/item/{item-id}`; recommendations are not full catalog objects and scores are not guaranteed probabilities.

## Categories and pagination

- Categories come from the item's `Categories`, not its label values. Use the `category` query parameter on the documented recommendation endpoint.
- `/api/recommend/{user-id}` documents multi-category filtering. For versions that support it, encode multiple values as repeated query keys (`category=...&category=...`), not as a comma-separated string or `category[0]`. Verify support/selection semantics in the deployed contract rather than assuming an AND/OR rule.
- Recommendation endpoints use `n` and `offset`; request the next offset as appropriate for the application. Results can change as feedback, caches, and catalog availability change; this is not a stable snapshot cursor or an unlimited inventory export.
- Catalog/feedback lists instead use `n` and `cursor`: `GET /api/users`, `/api/items`, `/api/feedback` return an object with `Cursor` and `Users`, `Items`, or `Feedback`. Treat cursors as opaque, URL-encode them, and follow the deployment's end-of-pagination rule. Detect repeated cursors and cap work to prevent infinite loops.
- Do not infer list continuation solely from receiving exactly `n` rows. Do not pass a recommendation offset as a list cursor.
- Some item recommendation endpoints document query `user-id` to remove read items for a user (for example latest and item-to-item). It is distinct from a path user ID; check the specific endpoint rather than adding it everywhere.

Read-only list-page template; initialize `GORSE_CURSOR` to an empty string for the first page and thereafter to the response's `Cursor`:

```bash
: "${GORSE_ENDPOINT:?Set the approved application REST endpoint}"
: "${GORSE_API_KEY:?Load the application API key securely}"
curl --fail-with-body --silent --show-error --get \
  "${GORSE_ENDPOINT}/api/items" \
  --header "X-API-Key: ${GORSE_API_KEY}" \
  --header 'Accept: application/json' \
  --data-urlencode 'n=100' \
  --data-urlencode "cursor=${GORSE_CURSOR-}"
```

## Consume an official SDK

Choose the language page below, pin a compatible package version, construct the client with endpoint/key from environment variables, and handle returned errors/exceptions. Keep the initial integration read-only; SDK tutorial insert calls are writes, not prerequisites for every recommendation request.

A minimal documented Python call shape (requires the approved package/environment and an existing user):

```python
import os
from gorse import Gorse

client = Gorse(os.environ["GORSE_ENDPOINT"], os.environ["GORSE_API_KEY"])
recommendations = client.get_recommend(os.environ["GORSE_USER_ID"], n=10)
# Decode according to the installed SDK's return type; do not assume string IDs.
```

The Python page also documents `AsyncGorse` with awaited `get_recommend`. Match blocking/async clients to the application. Check version-specific public options for category, offset, and writeback; do not copy parameters from another language. The TypeScript example uses `getRecommend({ userId, cursorOptions: { n: 10 } })`; that SDK option name does not change REST recommendation pagination into cursor pagination.

## Feedback and writeback are side effects

- By default, keep automatic writeback off during previews, health checks, retries, and prefetching.
- For accurate exposure, report actual displayed/read items from the application. Record positive feedback only for observed actions; never fabricate clicks/reads to improve apparent coverage or silence training warnings.
- `/api/recommend/{user-id}` accepts `write-back-type` and `write-back-delay` (duration format such as `10m`, documented as `0h0m0s`). Enabling them writes feedback even though the request is `GET`.
- Automatic writeback is a convenience approximation: a returned item may never render. Delayed timestamps defer when the read takes effect; they do not confirm the user saw it or cancel an abandoned prefetch.
- Agree on the feedback policy and explicit write scope before enabling writeback. A genuine read type must match `[recommend.data_source].read_feedback_types`; a click is positive only if the application's configured semantics say so.
- Direct feedback arrays use `PUT /api/feedback` to overwrite by `(UserId, ItemId, FeedbackType)` or `POST /api/feedback` to accumulate values. Retrying POST can double-count. A timeout leaves an uncertain outcome; reconcile stored feedback before replaying.
- Keep event-level deduplication/checkpoints in the application when required. Do not invent an idempotency-key header. Batch/import/restore operations require explicit approval; restore overwrites existing data and is not part of a normal read integration.

## Verify and troubleshoot as a consumer

1. With operator approval, perform a read without writeback for a known user and inspect the actual JSON type, IDs, and category membership. Do not run any live writes merely to validate this skill.
2. Check `GET /api/health/ready` and inspect readiness/store status; liveness alone (`GET /api/health/live`) does not prove recommendation availability.
3. Treat `n` as the requested size, not guaranteed cardinality. Empty results can reflect cold start, exhausted/read items, category mismatches, hidden items, or unfinished recommendation tasks; inspect data and task state before changing APIs.
4. The quick start waits for recommendation generation. Use dashboard Tasks or separately authorized CLI `gorse-cli ps`/`stats` to inspect progress; accepted data is not proof recommendations have refreshed.
5. For safe reads, use bounded retries/backoff and explicit client timeouts. For writeback GETs or feedback writes, first account for side effects; do not apply a blanket retry policy to every request.
6. Report the server/SDK versions, endpoint family, sanitized status/error, response shape, and whether writeback was enabled. Do not log keys, personal identifiers, or feedback payloads unnecessarily.

## Official sources

Documentation basis: `gorse-io/docs` snapshot `5cef16bd228c4095de6bbfa0f46832c198a305eb`; recheck deployed-version compatibility.

- API catalog: https://github.com/gorse-io/docs/blob/main/src/docs/api/README.md
- REST contract and auth: https://github.com/gorse-io/docs/blob/main/src/docs/api/restful-api.md
- Python: https://github.com/gorse-io/docs/blob/main/src/docs/api/python-sdk.md
- Go: https://github.com/gorse-io/docs/blob/main/src/docs/api/go-sdk.md
- TypeScript: https://github.com/gorse-io/docs/blob/main/src/docs/api/typescript-sdk.md
- Java: https://github.com/gorse-io/docs/blob/main/src/docs/api/java-sdk.md
- Rust: https://github.com/gorse-io/docs/blob/main/src/docs/api/rust-sdk.md
- PHP: https://github.com/gorse-io/docs/blob/main/src/docs/api/php-sdk.md
- Ruby: https://github.com/gorse-io/docs/blob/main/src/docs/api/ruby-sdk.md
- .NET: https://github.com/gorse-io/docs/blob/main/src/docs/api/dotnet-sdk.md
- Feedback semantics/writeback: https://github.com/gorse-io/docs/blob/main/src/docs/concepts/data-source.md
- Endpoint/task examples: https://github.com/gorse-io/docs/blob/main/src/docs/quick-start.md
- Config/keys: https://github.com/gorse-io/docs/blob/main/src/docs/config.md
- Read tracking and cold start: https://github.com/gorse-io/docs/blob/main/src/docs/faq.md
- Separate admin/CLI workflows: https://github.com/gorse-io/docs/blob/main/src/docs/gorse-cli.md

---
name: gorse-core-development
description: "Use when changing Gorse core configuration, recommendation pipelines, master/server/worker lifecycle, protobuf transport, or authentication boundaries."
---

# Gorse Core Development

## Establish the target

1. Confirm the checkout remote, requested branch or revision, and working-tree state:
   ```sh
   git remote -v
   git status --short --branch
   git rev-parse HEAD
   ```
2. Read repository instructions, `go.mod`, relevant build targets, implementation, and existing tests **at that exact revision** before applying any pattern below. File names and symbols are navigation hints, not guarantees of current APIs.
3. Identify the behavior to preserve and the smallest regression that demonstrates the requested change. Do not combine adjacent architectural migrations without authorization.
4. Respect the requested verification and publication boundaries. Do not commit, push, start services, or modify unrelated files without appropriate scope.

## Map the behavior before editing

Typical areas to inspect, when present:

| Area | Starting points | Follow through to |
| --- | --- | --- |
| Configuration | `config/`, embedded TOML, defaults and validation | environment bindings, hashes, metadata, reload |
| Recommendations | `logics/`, `model/`, master tasks | worker cache generation, server APIs, neighbors |
| Lifecycle | `master/`, `server/`, `worker/`, `cmd/` | synchronization, HTTP/gRPC, owned storage clients |
| Transport | `protocol/`, storage proxy implementations | generated code, conversions, dump/restore |
| Authentication | master/server route registration and guards | API keys, dashboard sessions, OIDC, raw handlers |

For backend contracts and integration coverage, use `gorse-storage-development` if installed; this skill remains usable without it.

## Configuration changes

- Trace a setting through the struct and tags, defaults, embedded examples, parsing, validation, environment bindings, serialization, and tests. Update every applicable source of defaults together.
- Test omitted, explicit zero, and explicit nonzero values according to the intended contract; do not assume zero always means disabled or default.
- Include behavior-affecting settings in recommender hashes/digests where those control cache or model invalidation.
- If configuration loading uses global Viper state, test successive loads for stale values. Preserve the target's loader design rather than introducing an unrelated global-to-instance refactor.
- Define the reload boundary explicitly. If database clients are restart-only, retain their active configuration in exported metadata as well as runtime state; do not advertise new settings while retaining old clients.
- Do not introduce dynamic proxy getters or runtime database replacement merely to implement ordinary configuration reload.
- Copy mutable configuration slices/maps before handing snapshots to asynchronous work; coordinate live reads and writes with the target's locking scheme.

## Recommendation and model changes

1. Trace data ingestion, training, serialization, worker generation, cache materialization, and online serving separately. Do not assume all recommenders use the same path.
2. Preserve the established boundary: an offline collaborative-cache change must not silently introduce online vector queries. An embedding item-to-item change must not migrate unrelated recommender types.
3. Preserve hidden-item exclusion, category filters, self/exclusion sets, context limits, score direction, result limits, and fallback behavior in both recommendation and neighbor endpoints.
4. For vector writers, use actual trained/observed dimensions, batch writes, flush before deleting stale records, and propagate write failures. Coordinate concurrent pushes and collection initialization.
5. Preserve digest/update-time and garbage-collection behavior when changing where intermediate results live.
6. Keep config/model type names distinct from persisted blob names and headers. Unknown serialized formats must not be silently decoded as another model; service-level fallback is a separate policy.
7. Inspect normal and alternate build-tag implementations when changing models. Regression-test deserialize-then-predict, not only freshly initialized models, especially optional embedding inputs.
8. Keep per-sample context features aligned with users, items, targets, and timestamps. If deduplicating feedback, carry labels from the same winning record as its timestamp.
9. For agent-style recommenders, validate templates before remote calls, bound tool iterations and concurrency, and test default/custom limits without contacting a live model provider.

## Master, server, and worker lifecycle

- Inventory resources actually opened by each node: direct stores, proxy clients, master connections, task loops, timers, and observability resources. Establish ownership; do not infer it from field names.
- Stop new work, cancel/unblock producers, and join owned loops and in-flight requests before closing the resources they use. Account for gRPC graceful-stop waiting on active RPCs.
- Prevent sync/reload from installing or reopening clients during shutdown. Protect stopping state and replaceable cancellation functions consistently; register wait-group work before launching goroutines.
- For deliberate client replacement, open the replacement first, synchronize publication with readers, and release the retired client only after its users finish. Keep the old client usable when opening the replacement fails.
- Attempt independent cleanup even after one close fails; preserve useful errors. Make repeated stop/shutdown behavior explicit.
- Inspect each interface before calling `Close`; not every store abstraction has a common close contract. Proxy and direct-store ownership can differ.
- Distinguish local filesystem stores from URI-dispatched stores; never pass an arbitrary remote URI into a filesystem-only server constructor.

## Protobuf and proxy boundaries

- For an interface change, enumerate concrete implementations, sentinels, proxy client/server, callers, tests, and protocol messages.
- Preserve backend behavior through forwarding; do not replace a remote search/query operation with client-side stream scanning.
- Update conversions in both directions, including timestamps, optional fields, labels, scores, categories, and hidden flags. Search manual protocol constructors and dump/restore paths for dropped fields.
- Inspect wire compatibility requirements before editing field numbers or message shapes. Renumbering/reusing fields is not a harmless Go refactor; coordinate intentional breaking changes explicitly.
- Use the target's generator command and tool versions. Regenerate affected message and service outputs as applicable; never hand-edit generated code to substitute for generation.
- Verify initialization/reconciliation RPCs as well as the query RPC that depends on them.

## Authentication boundaries

- Trace each affected route from registration to its actual guard. Raw container handlers may bypass dashboard WebService filters; middleware elsewhere does not prove protection.
- Keep ordinary API keys, administrative API keys, password sessions, and OIDC sessions distinct unless the verified contract deliberately accepts multiple modes.
- Test the configured-auth/empty-admin-key combination: an empty key must not accidentally bypass another configured authentication mode. Preserve intentionally unauthenticated mode only if that is the target contract.
- Reuse the existing guard that implements the required policy after reading it; do not prescribe a helper name across revisions.
- Verify unauthorized access has no side effects on destructive handlers. Cover legitimate key/cookie access, invalid credentials, and streaming responses where applicable.
- Preserve session-cookie set/clear behavior. Password-login response changes do not imply removing browser OIDC authorize/callback redirects.
- Never expose secrets in logs, config endpoints, fixtures, or reports. Preserve non-secret example values when unrelated to the change.

## Verification and review

Read [the verification checklist](references/verification.md) for test selection and boundary checks.

- Use two Go import groups: standard library, then all non-standard imports (third-party and project imports together). Avoid unnecessary aliases; use one only for a real collision or ambiguity. Run `gofmt` on touched Go files.
- Run targeted behavioral tests first, then affected consumer packages and appropriate build-tag variants. Prove the chosen selector actually ran tests.
- Run `git diff --check` and inspect the full scoped diff, including new/untracked files. Do not treat compile-only checks as behavioral coverage.
- Report actual commands, passes/failures/skips, unavailable services/toolchains, changed files, and unverified boundaries. Do not claim broader CI or runtime success from a narrow test run.

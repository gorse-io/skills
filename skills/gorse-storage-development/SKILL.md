---
name: gorse-storage-development
description: "Use when changing Gorse storage contracts, shared backend tests, SQL persistence, search indexes, vector semantics, or storage gRPC proxies."
---

# Gorse Storage Development

## Inspect the target first

1. Confirm remote, branch/revision, and existing changes with `git remote -v`, `git status --short --branch`, and `git rev-parse HEAD`.
2. Read repository instructions, `go.mod`, current interfaces, concrete backends, shared tests, and test-service configuration **at that revision**. Historical recipes are prompts for inspection, not unconditional API or backend-support claims.
3. Inspect the affected subsystem independently: `storage/data`, `storage/cache`, `storage/vectors`, or other storage packages present in the target. Similar method names do not establish identical contracts.
4. Identify persisted-format and wire-compatibility requirements before implementation. Preserve unrelated defaults, service versions, and example configuration.

## Change the contract as one unit

Build an implementation matrix before changing an interface:

| Surface | Required review |
| --- | --- |
| Shared model/interface | method semantics, context, errors, optional values |
| Every concrete backend | schema, write/read paths, initialization and cleanup |
| `NoDatabase` or equivalent | actual subsystem and method-specific behavior |
| Proxy client/server | symmetric conversions, forwarding, lifecycle |
| Protocol | request/response and service definitions, generated outputs |
| Shared tests | reusable contract plus capability-specific coverage |
| Consumers | master, worker, REST, recommendation, export/restore |

- Do not prescribe universal `NoDatabase` success or failure. Read its implementation and tests in each subsystem: lifecycle, query, and mutation methods may intentionally differ, and revisions may change the policy. Preserve or deliberately change that policy with focused tests.
- Do not run the persistence suite against a tolerant no-op sentinel that cannot retain data. Add focused sentinel tests and interface conformance checks instead.
- Keep storage types in storage packages, not master/server packages. Avoid redefining upstream contracts in adapters.
- Keep input/API quota validation at its established boundary; a persistence field addition must not silently change shared validation policy.

## Shared tests before backend patches

1. Add a regression to the shared suite when it describes behavior all implementing backends should satisfy. Confirm affected backend suites actually embed/run it.
2. Use backend-specific tests for real capability differences; do not weaken the common contract to accommodate an accidental fallback.
3. Cover insert/read/update/delete and overwrite/non-overwrite behavior when changing persisted fields. Exercise streams, pagination, and proxies if those carry the field.
4. Make metadata assertions meaningful. When storage owns a timestamp, assert it is nonzero, then clear it before comparing business fields; do not copy actual values into expected fixtures to conceal differences.
5. Isolate fixture data and namespaces. Avoid wall-clock sleeps, unordered-map assumptions, and assertions that mistake requested result limits for guaranteed cardinality.
6. Use two Go import groups: standard library, then all non-standard imports together. Avoid unnecessary aliases; qualify types normally unless a real naming collision requires an alias.

## SQL and document persistence

- Trace fields through schemas/migrations, selected columns, row decoding, inserts/upserts, merge columns, and document update/read paths. Include aggregate/helper tables and materialized views where present.
- Preserve omitted-field compatibility for optional metadata; inspect older insertion paths before introducing non-null constraints or new defaults.
- Check JSON/BSON round-trip representations, nil versus empty values, timestamp precision, and conversion errors rather than assuming in-memory equality.
- Bind user values. Identifier handling needs separate validation/quoting and namespace-isolation checks; value parameters cannot safely stand in for table or column names.
- Verify latest-state behavior for append/version-based engines in normal reads, not only after test-only optimization. Inspect whether helper tables have real readers and correct backfill/upgrade paths.
- Keep dependency changes narrow. Inspect declared module paths and existing `replace` directives before updating a driver fork; avoid replacing a module identity with its repository name by guesswork.

## Search and index reconciliation

- Establish the public query grammar at the target revision: plain text versus backend query syntax, any-term versus all-term, limits, result wrapper, and score direction.
- If the contract is plain-text any-term matching, test records that match different individual terms; a fixture matching both terms cannot distinguish OR from AND.
- Preserve native tokenizer/stop-word differences unless explicitly normalizing them. Shared result-set semantics do not imply identical scores or ordering across engines.
- Parameter binding prevents SQL injection, not interpretation by a full-text query language. Escape/quote tokens for the chosen grammar; never pass raw terms to an operator-aware parser and call them plain text.
- Make reconciliation idempotent: copy and normalize configured fields, compare meaningful existing index metadata, and rebuild only when desired semantics differ. Do not mutate shared configuration slices while sorting.
- Cover reordered-equivalent fields, changed fields, subsequent writes, and actual search after reconciliation. Inspect FTS tables, triggers, generated columns, and index options as applicable.
- Trace initialization/reconciliation through proxies and master dataset tasks. A query RPC alone is insufficient if the index is never created.
- Treat CJK tokenization, multi-character queries, and optional semantic search as separate capabilities requiring real backend probes. Do not infer them from generic text-search support.

## Vector storage

- Inspect the current collection/vector types, distance metrics, score contract, query filters, supported dimensions/dtypes, and quantization options. Do not carry forward an old backend capability matrix.
- Define whether larger or smaller scores are better. If the public contract is larger-is-more-similar, convert native distances at the backend boundary while preserving native similarity scores; do not normalize every metric with the same formula.
- Test dot product with unequal norms and an ordering that differs from cosine when proving true inner-product semantics. Vector normalization or cosine reranking does not generally preserve matrix-factorization rankings.
- Use an exact small-data oracle for metric tests; ANN recall tests and exact score assertions have different purposes. Distinguish exact stored counts from index-build/progress counters.
- Preserve IDs, categories, hidden flags, timestamps, scores, and payloads through write, query, fetch, and proxy conversions. Hidden items may be valid query sources but forbidden results according to the established contract.
- Validate schema dimensions and dtypes before writes/queries. For an index upgrade, update creation parameters, query parameters, metadata inspection, and fixtures together; verify pinned dependency support.
- Batch writes; flush successfully before timestamp-based stale deletion. Test failure paths so a partial rebuild does not silently erase valid records.
- Inspect direct versus master-proxied routing for embedded/local stores; do not assume workers may independently open the same files.
- Verify lifecycle methods against each backend. An optimization method may be a deliberate no-op in one implementation, not grounds for inventing the same behavior everywhere.

## Proxies and protobuf

- Forward operations to the backend instead of approximating search, counts, or vector queries by scanning streams on the client.
- Update interface, client, server, request/response messages, RPC definitions, generated files, and shared proxy tests together as applicable.
- Convert fields symmetrically and preserve optional/error/context behavior. Search manual constructors outside proxy files, including bulk and dump/restore paths.
- Inspect the required upgrade/compatibility policy before changing field types or numbers. Breaking message-shape changes require explicit coordination; do not invent compatibility machinery or remove it without a requirement.
- Use the target's generation commands and pinned tools, not hand-edited generated Go. Verify index setup RPCs as well as data RPCs.

## Integration and final review

See [backend verification](references/backend-verification.md) for a service-aware sequence.

- Start with local backend and sentinel tests, then proxy tests and real external backend suites. Test names and service requirements must be discovered, not assumed from old examples.
- For new external-service tests and benchmarks, require explicit service configuration and skip clearly when absent; do not silently connect to localhost/default credentials. Report skipped coverage separately from passes.
- Start only authorized disposable services, verify actual readiness, isolate run namespaces, and clean up resources you created. Never purge a shared deployment as test setup.
- Run `gofmt`, targeted tests, affected consumer compile/behavior checks, and `git diff --check`. Review new/untracked files as well as tracked diffs.
- Report commands, passing/failing/skipped backends, and remaining semantic or compatibility risks. Functional integration coverage is not performance validation.

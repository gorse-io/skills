---
name: gorse-sdk-development
description: "Use when developing Gorse client SDKs: verify REST contracts, preserve public compatibility, encode cross-language requests, and test against a real server."
---

# Gorse SDK Development

## Scope and source of truth

Use for REST wrappers, request/response models, public method signatures, examples,
and integration tests in Gorse client SDK repositories.

- Confirm the repository by its Git remote, default branch, and target revision.
  Inspect working-tree status before editing; do not overwrite unrelated changes.
- For organization-wide work, enumerate the current public SDK repositories. Do not
  assume a remembered repository name, language list, or default branch is current.
- Read the target Gorse server revision's REST route registration **and handler**.
  In `gorse-io/gorse`, start at `server/rest.go`; follow parsing helpers and tests.
  Route annotations alone can omit header-dependent response behavior.
- Compare that contract with the SDK's transport, exported models, tests, and README.
  An SDK-normalized object is not necessarily the server's JSON envelope.
- Treat examples below as discovery anchors, not a promise about every release.
  Record which server and SDK revisions the change supports.

## Establish the contract before coding

For each changed endpoint, record:

1. HTTP method, route, deprecation status, and path-segment encoding.
2. Authentication and API-version headers.
3. Query names, repeated values, defaults, omission versus explicit zero/empty values.
4. Request JSON fields and response envelope, pagination, timestamps, and errors.
5. Existing public SDK signatures and language-specific return conventions.

Useful contracts to re-check at the selected revision:

- Recommendation uses `/api/recommend/{user-id}` in the inspected implementation;
  the additional path-category route is deprecated there.
- Multiple categories are repeated keys: `category=Drama&category=Comedy`.
  Read `ReadCategories` and recommendation logic to establish filtering semantics.
- Check `n`, `offset`, `write-back-type`, and `write-back-delay` as well as categories.
- `X-API-Version` can change recommendation results from IDs to score objects.
  Match decoding and the SDK's headers; never silently switch public result types.
- Item search/list endpoints can return an iterator containing `Cursor` and `Items`,
  even when a particular response has no cursor. Do not substitute a raw item array
  or copy storage-internal types without verifying the wire response.

## Implement idiomatically and compatibly

- Reuse the existing transport and error handling; keep endpoint wrappers small.
- Encode free-form query values, cursor tokens, categories, and identifiers with
  appropriate URI builders. Path-segment escaping is not query escaping.
- Encode each value once. Cover spaces, Unicode, `+`, `&`, `/`, and reserved characters
  where the server contract allows them.
- Verify the language library's actual repeated-key serialization. An array can
  become `category[0]`, `category[]`, comma-separated text, or a JSON string; none is
  interchangeable with repeated `category` keys unless the server accepts it.
- For example, Go `url.Values.Add` and Python sequence-valued query parameters can
  express repeated values; confirm the resulting request for the selected library.
- Apply equivalent behavior to sync/async clients and overloads where they exist.
- Preserve public method names, parameter ordering, optional keywords, convenience
  overloads, and return models by default. Add options idiomatically without forcing
  a signature migration. Make breaking changes only when explicitly requested;
  then update every caller, test, and example within scope.
- Do not turn a narrow parameter fix into a repository-wide API modernization.

## Prefer existing real-server behavior tests

1. Read the SDK's current CI workflow, test configuration, dependency manifests,
   and setup scripts before selecting commands or starting services.
2. Derive server image/revision, configuration, environment variables, ports,
   credentials, readiness conditions, dataset, and test command from those files.
   A floating image tag or downloaded script may not match the intended revision.
3. Inspect downloaded setup scripts before execution. Use an isolated test workspace
   and test instance: restore/import operations can overwrite server data.
4. Reuse the existing real-server suite. Some SDK workflows use Gorse's
   `client/setup-test.sh` and MovieLens fixtures; confirm this on the target revision
   rather than copying historical Docker/configuration commands.
5. Preserve existing deterministic default/single-category recommendation tests.
   Add a separately named multi-category test with its own user/fixture data.
6. Assert non-empty results, fetch each returned item, and check that its categories
   intersect the requested set when that is the verified server semantics. An empty
   list must not make an `all`/loop assertion pass vacuously.
7. For search, require a known non-empty match. Requested `n` is generally a limit,
   not a guarantee of exactly that many matches.
8. Exercise write-back/offset behavior when changed, with isolated state and cleanup.
   Do not mutate shared fixtures so later tests depend on execution order.

Prefer these observable API tests over mocks, private-request-method patches, or
request-construction-only tests when the real fixture exists. A focused local HTTP
capture/decoding test can supplement integration coverage for escaping or errors,
but must not replace the real behavioral test or be reported as server coverage.

## Verification and handoff

- Run the language's formatter/linter and targeted tests, then the existing SDK
  suite against the configured real server when available.
- Check examples against exported signatures and run `git diff --check`.
- Report exact commands, server/SDK revisions, tests passed, skips, and blockers.
  A missing service, failed dataset download, or unready recommender is not a pass.
- Review the complete change set for unrelated changes. Commit or publish only
  when authorized; never infer that SDK work requires a release.

## Public discovery anchors

Resolve these paths on the task's selected branch/tag; paths and APIs can move.

- Gorse contract: https://github.com/gorse-io/gorse — `server/rest.go`, REST tests,
  `client/setup-test.sh`, and the configuration referenced by that script.
- Go SDK example: https://github.com/gorse-io/gorse-go — `client.go`, response model
  definitions, `client_test.go`, `README.md`, and `.github/workflows/ci.yml`.
- User-facing API/SDK docs: https://github.com/gorse-io/docs — `src/docs/api/` and
  `src/zh/docs/api/`; verify examples against implementation, not vice versa.

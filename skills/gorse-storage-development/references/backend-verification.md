# Backend verification

Inspect current test entry points, shared suite methods, environment-variable names, build tags, and Compose/CI service definitions before choosing commands. Backend availability and defaults change across revisions.

## Evidence sequence

1. Record a narrow failing regression for the behavior being changed.
2. Run the appropriate temporary local-store suite. Do not assume an embedded backend from an older branch still exists.
3. Run focused `NoDatabase` tests according to that subsystem's verified policy.
4. Run proxy coverage against an actual backend so initialization, conversion, query semantics, and errors cross the transport boundary.
5. Run each affected external backend with an explicit disposable URI, correct capabilities, and real readiness checks. Serialize memory-heavy services/suites when needed.
6. Compile and behavior-test affected consumers. A storage result-wrapper change may require REST adapters without changing the public JSON shape.
7. Run broader suites only with known prerequisites. Separate missing services, dependency/native-link failures, and behavioral regressions in the report.

Examples only after confirming those suites exist:

```sh
go test ./storage/data -run '^(TestNoDatabase|TestSQLite|TestProxy)$' -count=1
go test ./storage/vectors -run '^(TestNoDatabase|TestProxy)$' -count=1
go test ./protocol ./logics ./master ./server ./worker -run '^$'
git diff --check
```

Check verbose output or test discovery when needed to prove selectors execute the intended top-level tests and suite methods. A zero exit with no selected tests is not coverage. Compile-only `-run '^$'` does not validate semantics.

## Backend review questions

### SQL and documents

- Does every write/read path carry new fields, including streams and merge/upsert paths?
- Do schema upgrades work against an existing database, not just a freshly initialized one?
- Are optional-field omissions still valid? Are driver-owned timestamps asserted independently?
- For versioned append engines, do production readers select current state without relying on a test's forced compaction?

### Search

- Is the test contract about matching, tokenization, ranking, or index lifecycle? Avoid mixing them.
- Do unchanged/reordered fields preserve index identity while changed fields rebuild correctly?
- Does punctuation remain literal when plain-text semantics are promised?
- Are writes after reconciliation searchable, and does proxy setup reach the backend?
- If an engine requires a version/module feature, verify the actual running capability and update test infrastructure only within scope.

### Vectors

- Does a metric test distinguish the requested metric from a plausible fallback?
- Do direct and proxied queries enforce hidden/category filters and preserve score direction?
- Do dimension/dtype/quantization validation and describe/list metadata agree?
- Are count results exact stored-object counts rather than ANN progress estimates?
- Do partial batch failures avoid destructive stale cleanup?

## Integration safety and reporting

- Do not print URI credentials, overwrite production data, or infer that an open port means a service is ready.
- Use temporary directories and unique prefixes/collections; stop/remove only services and data created for this run.
- Keep external test and benchmark skip guards before connection setup. With URI variables absent, prove local tests still run and external suites explicitly skip.
- Record successful coverage per backend and operation. A skipped external suite does not establish driver compatibility.
- For performance claims, add representative scale/concurrency measurements, query-plan/index evidence, write amplification, and lifecycle costs. Passing shared CRUD tests alone proves none of those.

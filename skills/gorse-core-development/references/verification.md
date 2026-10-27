# Core verification checklist

Use only after inspecting the exact target revision. Select real test names and prerequisites from that checkout; these commands illustrate package-level starting points, not a guaranteed service-free suite.

## Select the evidence

| Change | Behavioral evidence | Consumers to inspect |
| --- | --- | --- |
| Config | omitted/zero/custom values, invalid inputs, successive loads | reload, metadata, digest invalidation |
| Recommendation | result IDs, filtering, ordering, fallbacks | online APIs, neighbors, offline worker |
| Models | registry creation and serialization round trip | master train/search, worker pull, alternate build tags |
| Lifecycle | cancellation, joined loops, ownership and close failures | command signal handlers, direct/proxy connections |
| Protocol | direct/proxy parity and field round trips | manual constructors, dump/restore, initialization |
| Auth | denied request plus authorized success | raw handlers, sessions, OIDC, stream path |

Examples after checking package/test availability:

```sh
go test ./config -count=1
go test ./logics ./model/cf ./model/ctr -count=1
go test ./master ./server ./worker -count=1
go test ./protocol ./master ./server ./worker -run '^$'
git diff --check
```

The `-run '^$'` command is a compile check, not a behavioral test. Package initialization and native linking can still have prerequisites. Prefer narrower selectors when existing suites need external services or large dependencies.

## Concurrency and teardown

- Test cancellation while work is active, not just shutdown of an idle struct.
- Cover replacement-open failure and a shutdown/sync overlap when changing client replacement.
- Verify no background producer can reopen stores after shutdown. Joining loops is stronger evidence than sleeping and retrying file deletion, especially on Windows.
- Inject one close failure and assert other owned resources are still released.
- Use the race detector on affected concurrency tests when supported. Package-global loggers/configuration and parallel tests may require isolation before meaningful race coverage is possible.

## Behavioral traps

- An embedding recommender unit test does not prove the REST neighbors endpoint uses the same new data path.
- Test hidden vectors through both direct and proxy paths; one missing conversion can expose hidden items.
- Use a serialize/deserialize round trip to test optional model state; an empty initialized index can conceal missing deserialized state.
- Test plain and streaming authentication paths separately if headers can be committed before authorization completes.
- For stochastic numerical failures, reproduce the exact test and inspect its inputs. Prefer deterministic values away from nondifferentiable boundaries; do not weaken tolerance merely to obtain a green run.

## Completion report

Separate behavioral tests, compile checks, formatting, and integration evidence. Record skipped/unavailable backend and build-tag coverage. A network timeout, unavailable native toolchain, or missing database service is a blocker to that evidence, not a fabricated pass or proof of a code regression.

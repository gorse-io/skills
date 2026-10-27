---
name: gorse-cli-development
description: Use when changing Gorse CLI commands, playground examples, native installers, or Node.js wrappers. Preserve command semantics and verify the actual distribution path.
---

# Gorse CLI Development

## Establish the current layout

Find the CLI repository and entrypoint from the current source. The CLI may be extracted from core; do not assume historical `cmd/gorse-cli` paths still apply. Read command definitions, release asset naming, installers, and existing integration setup before editing.

## Commands and clients

- Keep help text concise: prefer “Get cluster nodes” over phrases that repeat that this is a Gorse admin client.
- Preserve existing no-argument behavior when adding search. If a command accepts multiple search words, inspect Cobra argument rules and join the words into one query rather than silently using the first word.
- Keep reusable HTTP API clients separate from CLI formatting and sorting. Use the existing client API rather than duplicating transports.
- For a new SDK dependency, check whether its upstream change has merged. Pin the upstream revision rather than leaving a fork replacement after merge.
- Search all callers and integration tests after SDK return-type changes, not just the command package.
- Configure and reconcile search indexes in real-server fixtures before asserting search output.
- For admin-client integration tests, seed fixtures inside the tests that consume them. Check CI service ports before choosing fixture ports; avoid collisions with an already running dashboard.

## Playground examples

Use the unambiguous equals form for named datasets:

```sh
gorse-in-one --playground=ml-100k
```

A flag with a no-option default can treat the space-separated dataset as a positional argument. If changing imported dataset timestamps, trace both item and feedback timestamps through restore.

## Native installers

1. Inspect the release workflow for actual asset names, OS/architecture combinations, and version metadata.
2. Shell installers piped into `sh` must be POSIX-compatible; a Bash shebang is ignored in that invocation. Use `set -eu` rather than Bash-only `pipefail` when no pipelines require it.
3. Syntax-check with the supported shell, then exercise the piped invocation using a temporary mocked downloader/fixture. A syntax check alone does not verify installation.
4. PowerShell installation must make the binary discoverable in the intended shell/session. Test the installed command through PATH, not just an absolute path.
5. Never run privileged installation or alter the user's global PATH without permission. Use an isolated test destination locally when necessary; default-path CI tests need explicit disposable runners.
6. Exercise each claimed platform natively in CI where available. Cross-compilation is not proof of installer behavior.

## Node.js native wrappers

- Keep the main package binary-free; map runtime targets to platform-specific optional dependency packages.
- Inspect the package manager's workspace OS/CPU rules before placing target-restricted packages in one workspace. Validate the packed metadata, not only source `package.json` files.
- Launch the native process with asynchronous `spawn`, inherited stdio, and argument forwarding.
- Mirror the child's exit code and termination signal. Remove the wrapper's own signal handler before re-emitting that signal to itself.
- Test a nonzero exit code and genuine signal termination with an executable fixture.
- A local wrapper fixture does not verify release download, package publishing, or consumer installation; test those boundaries separately when in scope.

## Verification

Run focused command/client tests and `git diff --check`. For installers or packaging, inspect generated artifacts and perform a clean consumer smoke test. Report native platforms and distribution paths that were not exercised.

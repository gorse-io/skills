---
name: gorse-contribution-workflow
description: Use when preparing, reviewing, or publishing changes across Gorse repositories. Verify repository identity, isolate the change, and report local and remote checks separately.
---

# Gorse Contribution Workflow

## Discover before editing

1. Identify the repository by `git remote -v`, not by its directory name.
2. Read repository instructions and discover the default branch; do not assume `main` or `master`.
3. Check `git status --short --branch` and `git worktree list`. Preserve unrelated work.
4. For an existing PR, read its head repository, branch, SHA, and base. Reuse the matching clean worktree or create an isolated worktree. Update that PR rather than opening a replacement.
5. Start independent work from the freshly fetched base, not another feature branch.
6. Respect explicit boundaries: investigation-only means reproduce and explain without editing; no-commit means no commit; no-tests means do not launch additional tests or services.

## Keep changes focused

- Stage exact intended paths. Review the entire base-to-head diff, not just unstaged edits.
- Preserve example credentials and unrelated config comments. Never publish real credentials.
- Use the existing system Go toolchain before considering containers. Do not install or upgrade Go without authorization.
- For Go, use two import groups: standard library, then all non-standard imports including Gorse packages. Prefer declared package names; alias only for actual conflicts or path/name mismatches.
- Prefer small, idiomatic changes over one-use helpers, redundant wrappers, speculative compatibility layers, and unrelated refactors.
- Preserve compatibility unless the task explicitly authorizes a breaking migration. Do not add fallback/dual-write paths to an explicitly incompatible migration.

## Verify at the changed boundary

- Core changes: focused package/contract tests, then broader checks where feasible.
- Storage changes: local backends first, then explicitly configured external services. A skipped suite is not backend verification.
- SDK changes: current REST contract and existing real-server integration tests.
- Docs changes: actual package-manager build script and navigation/link checks.
- CLI changes: command/help output, parsing, installers or package wrappers as applicable.
- Always run `git diff --check` before publishing unless the user explicitly forbids all validation.
- Do not call a network timeout, unavailable database, or disk-full error a product regression. Inspect the failure and report the boundary actually exercised.

## Publish only within authorization

1. Check authenticated GitHub identity and repository permissions without printing secrets.
2. Follow the requested delivery mode: direct push when authorized, otherwise a topic branch and PR. Never merge just because a PR is green.
3. If upstream push is unavailable, verify a fork's parent before pushing there. Keep upstream and fork remotes distinct.
4. Use the contributor's configured/authorized author identity; preserve original authors on backports.
5. Before creating a PR, check whether one already exists for the head branch.
6. After pushing, read back the exact remote branch SHA and PR head SHA. Both must match the intended local commit.
7. When CI monitoring is requested, inspect failures and finish monitoring the pushed head. Separate workflow checks from external checks. An old green SHA does not verify a new commit.
8. For a narrow rebase request, verify head/base/check status promptly rather than silently waiting for the entire matrix.
9. Before any CI-fix push, re-read PR state: a fix pushed to an already merged head does not join the merge.

## Backports

- Read the actual merged commit and target branch. Preserve original authorship.
- Resolve conflicts against release capabilities: retain its dependency baseline and omit tests for APIs absent on that release.
- Avoid broad dependency cleanup during a narrow backport.
- Verify the complete target-base diff and create the PR against the release branch, not the default branch.

## Completion report

Report the changed surface, commit or PR, actual verification, and remaining blockers. Distinguish local tests, remote CI, and unexercised platforms. Never fabricate successful output or describe a queued check as passed.

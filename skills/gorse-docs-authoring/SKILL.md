---
name: gorse-docs-authoring
description: "Use when authoring Gorse VuePress documentation: ground examples in source, maintain bilingual navigation and indexes, preserve valid links, and verify builds."
---

# Gorse Docs Authoring

## Scope and initial inspection

Use for documentation pages, SDK/CLI examples, bilingual navigation, link repairs,
and narrowly scoped follow-ups in `gorse-io/docs`.

1. Confirm the repository by remote URL and inspect branch/working-tree status.
2. Identify the requested version, feature, locale scope, and placement. Read nearby
   pages and configuration before editing; do not assume paths remain unchanged.
3. For a follow-up, confirm the existing branch and review target. Keep the change
   on that branch unless instructed otherwise; do not create a duplicate review.
4. Review the complete base-to-head diff, not just the latest edit. Remove unrelated
   hunks introduced by your work without overwriting others' changes.

## Ground documentation in the correct source

- CLI syntax: inspect the relevant CLI implementation and actual `--help` output
  from the selected revision when executable tooling is available.
- REST behavior: read Gorse route registration, handlers, and parsing logic.
- SDK usage: inspect exported signatures, models, README examples, and tests in the
  relevant SDK revision. Do not invent imports, options types, or response shapes.
- Installation: inspect maintained installer scripts, release asset naming, and
  package-manager definitions rather than repeating remembered commands.
- Configuration: inspect the implementation and example configuration for the same
  supported version. Distinguish released behavior from development-branch changes.

Scope follows the request: an exact replacement list or review correction is not
permission to modernize surrounding examples. Preserve unaffected timestamps,
imports, commands, and prose; propose broader synchronization separately.

## Bilingual placement and discoverability

The inspected docs tree uses the following locations; re-check them before editing:

| Purpose | English | Chinese |
| --- | --- | --- |
| Documentation pages | `src/docs/` | `src/zh/docs/` |
| Sidebar configuration | `src/.vuepress/sidebar/en.ts` | `src/.vuepress/sidebar/zh.ts` |
| Documentation landing index | `src/docs/README.md` | `src/zh/docs/README.md` |

- Update both locales for new/shared content unless explicitly limited to one.
  Preserve technical meaning, commands, warnings, and feature availability.
- A page requested at the same level as Dashboard belongs at the corresponding
  top-level page/navigation layer, not inside `dashboard/`.
- Update **both sidebar files and both documentation README indexes** for new
  top-level pages. Sidebar-only placement leaves landing-page readers behind.
- For nested content, update the relevant parent index and sidebar group in each
  locale; inspect any affected root index entries as well.
- Match neighboring frontmatter, icons, heading levels, link style, and locale
  routes. Verify that links target actual pages and generated anchors.
- When moving/removing a page, audit inbound links, navigation, and redirect config.

## VuePress syntax and examples

Follow the installed VuePress/Theme Hope version and existing examples. Do not
assume arbitrary Markdown tab syntax works with the site's plugins.

The inspected quick-start uses `::: tabs`, `@tab:active Linux/macOS`, and
`@tab Windows`. Use `bash` and `powershell` as fence languages, not tab labels.
For code-only tabs, inspect an existing working `::: code-tabs` example first.

A safely fenced example of a tabs container:

````md
::: tabs

@tab:active Linux/macOS

```bash
printf '%s\n' 'example'
```

@tab Windows

```powershell
Write-Output 'example'
```

:::
````

- An outer fence demonstrating inner triple-backtick blocks must use four or more
  backticks (or a different valid delimiter). Never close an example accidentally
  by nesting identical triple-backtick fences.
- Keep containers balanced and use the site's admonition/frontmatter conventions.
- For platform support changes, inspect the whole affected workflow: downloads,
  decompression, binary uploads, JSON quoting, and recommendations may each differ.
  Leave truly identical commands shared.
- Test exact runnable snippets where practical; do not report a local HTTP capture
  or parser check as a live Gorse integration test or native Windows validation.
- Mark placeholders clearly; never include real credentials. Warn before destructive
  restore, overwrite, deletion, or reset examples.

## Link repairs without churn

- Corroborate a failure before changing a URL. A working 301/308 redirect is not a
  broken link and should remain unless redirect cleanup is explicitly requested.
- Fix confirmed missing files/routes, malformed URLs, 404/410 responses, or wrong
  semantic destinations. Distinguish bot protection, rate limits, and temporary
  network errors from actual breakage.
- Preserve excluded files and requested prose scope. Do not canonicalize providers
  or reformat working examples merely to satisfy a noisy link checker.

## Verify using the actual package scripts

1. Read `package.json`, the lockfile, CI workflow, and toolchain declarations. Select
   the repository's package manager and supported runtime, not remembered versions.
2. Install dependencies using the lockfile-compatible repository workflow. Do not
   upgrade dependencies or regenerate the lockfile as an incidental docs change.
3. Inspect available scripts before invoking them. The inspected `package.json`
   defines `docs:build` as `vuepress-vite build src`; with pnpm this is:

   ```bash
   pnpm docs:build
   git diff --check
   ```

   Reconfirm the script on the target revision. Do not invent a `test` or lint
   script. Run generation scripts only when relevant and inspect generated changes.
4. Require a successful exit status. Classify warnings from actual output; do not
   assume a remembered warning is harmless. Report build blockers plainly.
5. Inspect rendered output for changed tabs, locale navigation, commands, and links.
   A successful build does not prove interactive tabs or client-rendered diagrams
   work. Parse changed Mermaid fences with the installed version when applicable.
6. Search for stale page names/anchors after moves and validate repository-relative
   links. Exclude dependencies and build/cache output from source inventories.
7. Review staged, unstaged, and untracked changes. Report exact commands/results,
   modified pages/navigation, and any checks not run. Publish only when authorized.

## Public discovery anchors

- Documentation source: https://github.com/gorse-io/docs — `package.json`, CI,
  `src/.vuepress/`, both `src/docs/` and `src/zh/docs/`, and their README indexes.
- Working platform-tab example: `src/docs/quick-start.md` and its Chinese counterpart.
- Server/API implementation: https://github.com/gorse-io/gorse.
- Go SDK example source: https://github.com/gorse-io/gorse-go.

Resolve implementation links at the relevant revision. None of these anchors
establishes that a historical API or toolchain is still current.

---
name: gorse-cli
description: "Use when operating Gorse with gorse-cli: select an application, inspect or change data, follow cursor pages, edit the recommendation pipeline, and export or restore approved data."
---

# Gorse CLI Operations

Operate an existing Gorse service; do not modify Gorse source. Start read-only.
Get explicit approval before remote writes, imports, deletion, pipeline changes,
restore/reset, or sending data to paid/external providers. Examples are not
permission to run them against production.

## Establish version, target, and access

1. Identify the approved environment, master/admin endpoint, server version, and
   installed CLI version. Use HTTPS for authenticated remote deployments; loopback
   HTTP examples are only for an isolated local sandbox.
2. Inspect installed help before choosing commands:

   ```sh
   gorse-cli --version
   gorse-cli --help
   gorse-cli application --help
   gorse-cli user list --help
   gorse-cli pipeline ranker update --help
   ```

3. This skill describes the source revision linked in
   [commands and compatibility](references/commands.md), not a minimum released
   version. A published binary can lack main-branch features. If a command is
   missing, stop and obtain an approved compatible CLI; do not invent aliases,
   silently upgrade, or require a source checkout for routine operation.
4. Use the master/admin key, not the application REST key. Never request a key in
   chat, print it, or commit it. Prefer an interactive key prompt/system keyring,
   or environment variables populated by an approved secret store. Treat pipeline
   output, exports, and backups as sensitive data.

## Select and verify an application

For an approved local sandbox, saving a connection changes only local CLI state:

```sh
gorse-cli application add local --endpoint http://localhost:8088
gorse-cli application current
gorse-cli application list
```

`add` saves credentials in the system keyring and selects the application. It
prompts for the admin key when no flag/environment key was supplied. `application
use NAME` switches the saved selection; it does not deploy or create remote data.

**Check overrides before every write.** Endpoint and key are resolved separately:
nonempty explicit flag → environment (`GORSE_ADMIN_ENDPOINT`,
`GORSE_ADMIN_API_KEY`) → explicit `--application` → current saved application.
Thus `--application` does not override a nonempty environment value, and mixed
sources can accidentally pair one endpoint with another key. Inspect routing
without displaying secret values; resolve unintended overrides before proceeding.
Deleting a local application is not remote data deletion and can select another
saved application, so check `application current` again afterward.

## Inspect data and follow pages

```sh
gorse-cli stats
gorse-cli ps
gorse-cli user list -n 20
gorse-cli item list -n 20
gorse-cli feedback list --user USER_ID -n 20
gorse-cli item categories
gorse-cli pipeline get
```

- Read a specific record with `user get USER_ID` or `item get ITEM_ID`; use IDs
  obtained from the target, not guessed identifiers.
- For user/item lists, copy the printed **Next page** command. It retains page
  size and explicit application/endpoint flags; an explicit API key becomes a
  placeholder that must be supplied safely. Keep the cursor opaque and quoted.
  No hint means no next page; do not construct an offset or loop on a repeated
  cursor. The default page size is 10, including `-n 0`.
- `item list QUERY...` searches items. It has no cursor pagination; do not combine
  a search query with nonempty `--cursor`. `feedback list` also has no CLI cursor
  flag in the referenced revision; use targeted filters instead.
- For recommendation diagnosis, compare `recommend latest`, `recommend
  item-to-user USER_ID`, and a configured named recommender. Obtain names from
  the pipeline first. Never fabricate feedback to make a preview nonempty.

## Change records deliberately

Follow [data and transfer commands](references/commands.md#data-and-transfers).

1. Read the existing record and agree on IDs, fields, overwrite scope, and rollback.
2. Use `user update` / `item update` for partial field changes, not a replacement
   `add` built from an incomplete record. Omitted flags leave fields unchanged.
   Labels/categories replace the whole field rather than merge nested keys.
3. Pass explicit false or empty values when intended: `--is-hidden=false`,
   `--comment=`, `--category=`, or `--labels='{}'`. JSON `null` is not a labels
   clear operation. Quote expressions and JSON for the operator's shell.
4. `feedback add` records a **real observed event**. Its POST semantics are
   additive on an existing feedback key in the referenced SDK; do not blindly
   replay an uncertain write. Preserve the event's actual type/value/timestamp.
5. User/item/feedback deletion requires an explicitly true `--yes`. Obtain
   authorization first; never append it merely to bypass a refusal. Read back
   affected records after changes; `RowAffected` alone does not prove correctness.

## Edit the recommendation pipeline

Follow [pipeline commands](references/commands.md#pipeline-commands).

1. Inspect `pipeline get`, the relevant group's `get`, and actual installed help.
   Preserve a restricted-access baseline and record the intended change.
2. Use the smallest approved update. New settings commands overlay only explicitly
   changed fields onto the current full pipeline before submitting it; omitted
   settings are retained. Repeated list flags specify the complete ordered
   replacement list, not appends.
3. Defining a named recommender does not automatically select it in ranking or
   fallback. Update those references explicitly and verify them afterward.
4. Let the server validate expressions/types. A sole empty list flag requests a
   clear, but the server may reject it, including an empty ranker list. Do not
   claim success after an error or retry with broader destructive changes.
5. Reads/updates are not protected by compare-and-swap. Coordinate concurrent
   editors. Read back the effective settings, then inspect `ps`, task completion,
   and recommendation previews; an accepted update is not a trained model.
6. `pipeline reset` returns to file defaults, not the saved baseline. It requires
   separate approval and its normal confirmation. Do not invent an apply-file,
   edit, schema, or force flag that the installed CLI does not expose.

## Transfer, back up, and recover

- JSONL `user/item/feedback import [file]` and `export [file]` are resource
  transfers, not binary dumps. Omit the file or use `-` for stdin/stdout. The CLI
  forwards data without content validation or client-side batching; the server
  owns validation, replacement semantics, and partial commits.
- Review the entire import target and data contract before writing. Completed
  server batches are not rolled back on a later failure. Reconcile actual records
  before retrying; never assume an import is transactional or a dry run.
- A named export writes a sibling temporary file and replaces its destination
  after success; stdout export has no status banner. Shell `>` redirection can
  truncate a file before the CLI runs, so do not use it over a valuable backup.
- `dump FILE` is a binary data backup and may overwrite that path. Choose a new
  restricted filename, check exit status/nonempty output, and record a checksum
  and compatible versions. It is not a whole-infrastructure snapshot.
- Restore only to the explicitly approved target, with a pre-restore backup,
  compatible binary format, coordinated writers, and normal confirmation.
  `restore FILE` warns that users/items/feedback/cache will be overwritten.
- Read back representative data/counts and task readiness. Prove recovery in an
  isolated environment; do not claim a production restore was tested from help
  checks or an export alone.

## Sources and related workflows

Exact commands, flags, compatibility notes, and pinned official implementation
links: [command reference](references/commands.md).
Use the collection's data-ingestion, recommendation-tuning, and operations skills
for event policy, quality evaluation, and incident recovery; this skill focuses
on the CLI interaction boundary.

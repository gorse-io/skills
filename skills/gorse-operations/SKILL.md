---
name: gorse-operations
description: "Use when operating a deployed Gorse service: inspect health, tasks, logs, metrics and recommendations; use dashboard or CLI safely; plan backups, restores and incident recovery."
---

# Gorse Operations

Use read-only checks first. This is an end-user runbook, not a code-development
workflow. Do not restart services, import data, change pipelines, restore backups,
delete records, or purge storage without the user's explicit authorization.

## Identify the actual target

1. Record environment, endpoint, topology, affected users, symptom onset, and last
   deployment/config/data change. Confirm the target before every write.
2. Check the running version: Dashboard **Cluster** shows node versions; documented
   binary flags include `gorse-in-one --version` and split-role `--version`.
   For containers, record the actual image digest as well as its tag. Check CLI
   command support with `gorse-cli <command> --help`; do not assume CLI and server
   are compatible merely because they are installed together.
3. These instructions use official docs at
   `5cef16bd228c4095de6bbfa0f46832c198a305eb`. Validate against the deployed release,
   its config template, executable help and interactive `/apidocs` before acting.
   Current docs can describe features missing from an older deployment.
4. In a split cluster: API servers normally use HTTP `8087`, master dashboard/admin
   HTTP `8088` and master gRPC `8086`; worker monitoring HTTP is `8089`.
   Gorse-in-one uses HTTP `8088` for API/dashboard. Respect configured overrides.

## Health and readiness

[REST API docs][rest] document `GET /api/health/live` and
`GET /api/health/ready` on the server API. For an authorized local, unauthenticated
sandbox server:

```sh
curl -i http://127.0.0.1:8087/api/health/live
curl -i http://127.0.0.1:8087/api/health/ready
```

Use port `8088` for an all-in-one instance after confirming its release supports
these probes. For secured deployments use the configured TLS endpoint and auth
policy; do not disable certificate verification. Ordinary authenticated API calls
use `X-API-Key` with the server API key, not the admin API key.

- Liveness says the HTTP service has started; readiness says it can handle requests.
  Inspect HTTP status and the response's `Ready`, `DataStoreConnected`,
  `CacheStoreConnected`, `DataStoreError`, and `CacheStoreError` fields.
- Readiness is not proof that recommendations are populated or model quality is good.
- On DB errors, inspect effective DSNs (without printing secrets), environment
  overrides, credentials, TLS trust, network/DNS and backend availability. Correct
  the specific dependency failure before restarting unrelated nodes.
- These server routes are not a guarantee of identical master/worker probe routes.
  Confirm each role's supported probes before configuring orchestration checks.

## Dashboard and CLI: read-only diagnosis

[Dashboard Overview][dashboard] describes the master UI:

- **Overview:** user/item/feedback totals, collaborative NDCG/precision/recall,
  ranker AUC/precision/recall, and latest/non-personalized previews.
- **Tasks:** task state, start/end times and progress; compare failed or stalled
  tasks with logs for that time window. Dataset loading, neighbor generation and
  training must complete before their downstream results are expected.
- **Cluster:** expected servers/workers and versions; investigate missing or mixed
  nodes before scaling. Master loss can leave serving alive while updates stop.
- **Users / Items:** inspect a specific entity, its feedback and recommender previews;
  avoid delete controls. **Advance** import/purge controls are writes, not diagnosis.

For [Gorse CLI][cli], use a saved context to avoid putting secrets in command-line
arguments. The following loopback context is only for a local/private sandbox;
substitute the approved TLS-protected master endpoint for a remote deployment.

```sh
gorse-cli context add local --endpoint http://localhost:8088
gorse-cli context current
gorse-cli cluster-info
gorse-cli stats
gorse-cli ps
gorse-cli get users -n 20
gorse-cli get items -n 20
gorse-cli get feedback -n 20
gorse-cli get categories
gorse-cli pipeline get
gorse-cli pipeline schema
```

`context add` prompts for the admin API key and stores context credentials in the
system keyring. Check the selected context every time; context creation changes
local CLI state. Do not paste keys into chat or share unsanitized context/config
output. CLI administration uses the master endpoint and admin key; a server API
key is not a substitute. If a command is absent, consult that CLI version's help
rather than inventing an equivalent flag or endpoint.

## Logs, metrics, and workload freshness

[Docker Deployment][docker], [Binary Deployment][binary], and [Configuration][config]
document role logging and monitoring interfaces.

1. For a documented Linux service, run `systemctl status gorse`. Inspect the
   configured `--log-path` or the deployment platform's collected logs. Correlate
   task name, node/version and time; sanitize user data and secrets before sharing.
2. Check `--log-max-size`, `--log-max-age`, and `--log-max-backups` in that binary's
   help before changing retention. Use temporary `--debug` only with approval,
   resource limits and a plan to revert; do not enable it indefinitely by default.
3. Prometheus export is documented on master HTTP `8088`, server HTTP `8087`, and
   worker HTTP `8089`. The cited pages do **not** specify a scrape path or metric
   names. Verify them in release-specific official documentation or deployed route
   configuration before adding a scrape job; do not guess `/metrics` or counters.
4. Compare task completion and cache freshness with configured periods rather than
   declaring a running process healthy. Servers scale online traffic; workers scale
   offline generation. A worker cannot repair missing data or a bad pipeline.

## Empty, stale, or unexpected recommendations

Follow [FAQ][faq], [Pipeline][pipeline], [Data Source][data], and the actual pipeline:

1. Confirm the request reaches the intended API instance/port and existing user.
   Verify actual user/item/feedback counts and IDs with the dashboard or CLI.
2. Compare unfiltered latest items against the user result, replacing `USER_ID`
   below with a real ID; it is not shell syntax for an unknown identifier.

```sh
gorse-cli recommend latest -n 10
gorse-cli get feedback --user USER_ID
gorse-cli recommend item-to-user USER_ID -n 10
```

3. Remove optional category filters for a diagnostic comparison. Inspect category
   membership, `IsHidden`, item/feedback TTLs, timestamps and clock skew. Check the
   user's seen/read history: read filtering or exhaustion can legitimately empty a
   result. Do not clear feedback or unhide unavailable items to force a result.
4. For collaborative training reporting no feedback, compare stored feedback types
   with `recommend.data_source.positive_feedback_types`. For click-through training,
   the FAQ calls out missing negative examples from read events without positives.
   Also inspect explicit negative-feedback settings in releases that support them;
   do not conflate explicit dislikes with ordinary read events.
5. Inspect master dataset/neighbor/model tasks and worker generation. The quick-start
   waits for item-to-item generation before its recommendation check. Confirm the
   cache database is connected and generated results are fresh before tuning models.
6. Inspect the effective pipeline, not just file contents: saved RecFlow settings
   take precedence. An empty pipeline defaults to latest, not personalization.
   Compare configured candidate sources, ranker and fallback; cold-start fallback
   needs eligible items. Do not assume a recommender named `popular` or `similar`
   exists; obtain the configured name before requesting a named preview.
7. Repeated reads may be intentional when the application never records impressions.
   FAQ documents explicit read feedback and automatic write-back parameters. A GET
   with write-back is a **data write**, so keep it out of read-only smoke tests.

## Backups, restores, and configuration changes

[CLI][cli] documents binary data backup/restore; [Dashboard][dashboard] offers JSON
lines export/import separately. Do not interchange these formats.

1. Confirm the current master context, authorized data scope, release, and a new
   output filename that will not overwrite an existing backup. Export contains
   application data: restrict access and retention. For an approved backup:

```sh
gorse-cli context current
gorse-cli dump backup.bin
```

2. Check exit status, file existence/nonzero size, and record release/config plus
   a checksum with an available local tool. Store config/secret references and
   relevant database, cache, model/blob and persistent-volume recovery procedures
   separately. A CLI dump is not a documented whole-infrastructure snapshot or
   point-in-time consistency guarantee. Prove recoverability in an isolated target.
3. **Restore requires explicit authorization of the target and overwrite scope.**
   The CLI warns it replaces users, items, feedback and cache data. First take an
   approved pre-restore backup, coordinate writers/downtime and verify format/release
   compatibility. Only then run `gorse-cli restore backup.bin`, retaining its normal
   confirmation. Never add an invented force/skip-confirmation flag.
4. After restore, read back entity counts and representative records; check readiness,
   task progress and recommendation previews. Quick-start restarts the Compose
   `master` after sample import; apply that only to a matching authorized deployment,
   not as a universal restore requirement.
5. Before a pipeline change, preserve `pipeline get` output and inspect `pipeline
   schema`. CLI patch/reset and RecFlow Save/Clear change live behavior. RecFlow
   Clear and CLI reset return to file defaults; request approval and compare the
   effective pipeline afterwards. Do not promise hot reload of unrelated settings.
6. Dashboard user/item deletion and **Purge Database** require explicit authorization.
   Purge is irreversible. Never use purge, volume deletion, or Helm redeployment as
   a routine health fix, credential rotation, or rollback strategy.

## Official sources (pinned docs revision)

[rest]: https://github.com/gorse-io/docs/blob/5cef16bd228c4095de6bbfa0f46832c198a305eb/src/docs/api/restful-api.md
[cli]: https://github.com/gorse-io/docs/blob/5cef16bd228c4095de6bbfa0f46832c198a305eb/src/docs/gorse-cli.md
[dashboard]: https://github.com/gorse-io/docs/blob/5cef16bd228c4095de6bbfa0f46832c198a305eb/src/docs/dashboard/overview.md
[RecFlow precedence and Save/Clear](https://github.com/gorse-io/docs/blob/5cef16bd228c4095de6bbfa0f46832c198a305eb/src/docs/dashboard/recflow.md).
[faq]: https://github.com/gorse-io/docs/blob/5cef16bd228c4095de6bbfa0f46832c198a305eb/src/docs/faq.md
[config]: https://github.com/gorse-io/docs/blob/5cef16bd228c4095de6bbfa0f46832c198a305eb/src/docs/config.md
[docker]: https://github.com/gorse-io/docs/blob/5cef16bd228c4095de6bbfa0f46832c198a305eb/src/docs/deploy/docker.md
[binary]: https://github.com/gorse-io/docs/blob/5cef16bd228c4095de6bbfa0f46832c198a305eb/src/docs/deploy/binary.md
[pipeline]: https://github.com/gorse-io/docs/blob/5cef16bd228c4095de6bbfa0f46832c198a305eb/src/docs/concepts/pipeline.md
[data]: https://github.com/gorse-io/docs/blob/5cef16bd228c4095de6bbfa0f46832c198a305eb/src/docs/concepts/data-source.md
[Quick-start import/task example](https://github.com/gorse-io/docs/blob/5cef16bd228c4095de6bbfa0f46832c198a305eb/src/docs/quick-start.md).

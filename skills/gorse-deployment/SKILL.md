---
name: gorse-deployment
description: "Use when deploying Gorse for end users: choose demo or production topology, configure storage and security, and launch documented Docker, binary, or Kubernetes deployments."
---

# Gorse Deployment

Deploy a recommender service, not a source-development environment. Use only the
installation method the user requests; do not install, start services, expose
ports, or alter databases without authorization.

## Establish the release and scope

1. Identify sandbox versus production, OS/CPU, existing infrastructure, traffic,
   database ownership, persistence needs, and allowed downtime.
2. Record the actual Gorse version, container tag/digest or binary artifact, chart
   version if applicable, and effective configuration (redact secrets). For binaries,
   run `gorse-in-one --version` and `gorse-in-one --help`; split-role binaries also
   document `--version` and `--help`. Dashboard Cluster lists node versions.
3. The sources below are current-branch docs at revision
   `5cef16bd228c4095de6bbfa0f46832c198a305eb`, **not a release compatibility promise**.
   Obtain config and deployment examples for the chosen release. Do not mix a
   `master` config, `release-0.4` Compose example, and an unrelated image.
4. Pin a reviewed release/image digest for production. `latest` is mutable;
   `nightly` follows development. Check the deployed executable's help before
   applying flags: these docs disagree about some cache-path flags.

## Choose topology and network boundaries

[Quick Start][quick] and [Pipeline][pipeline] distinguish these roles:

| Topology/role | Responsibility | Documented default interface |
| --- | --- | --- |
| Playground | Disposable all-in-one trial | HTTP `8088` |
| Gorse-in-one | Single-node service | HTTP API/dashboard `8088`; master gRPC `8086` |
| One master per cluster | Dataset loading, neighbors, models, coordination | gRPC `8086`; dashboard/metrics HTTP `8088` |
| Servers | Online API, filtering and fallback | HTTP `8087` |
| Workers | Offline retrieval/ranking and cache generation | Monitoring HTTP `8089` |

- Scale servers for request throughput, workers for offline throughput. Do not
  propose multiple active masters as an undocumented HA arrangement.
- Keep gRPC, databases, worker monitoring, and dashboard on trusted networks.
  Public application traffic belongs on the server API, not worker `8089`.
- Server/worker CLI HTTP binding defaults to `127.0.0.1`; container examples use
  `--http-host 0.0.0.0`. Master config defaults bind to `0.0.0.0`. Review actual
  port mappings/firewalls rather than assuming either default is safe.

## Configure storage, credentials, and persistence first

Use a release-matched `config.toml` template; [Configuration][config] describes keys.

1. Set both `[database].data_store` and `cache_store`. The deployment docs list
   MySQL/PostgreSQL/MongoDB for data, and those plus Redis for cache. Redis is not
   a documented data-store choice here. Check compatibility against the deployed
   release; old minimum versions and sample image versions are not security advice.
2. `GORSE_DATA_STORE` and `GORSE_CACHE_STORE` override those file settings. Review
   `table_prefix`, `data_table_prefix`, and `cache_table_prefix` for namespace
   isolation. Do not point a new instance at a shared production namespace by default.
3. Provision authorized database accounts and validate network/TLS access. Preserve
   documented DSN syntax, e.g. MySQL uses `mysql://...@tcp(host:3306)/database`;
   PostgreSQL supports `postgres://...` and `sslmode=verify-full`. Never copy sample
   passwords or `sslmode=disable` into production. Supply secrets through an approved
   secret mechanism, not committed config, shell history, or pasted diagnostics.
4. Set dashboard credentials using `[master].dashboard_user_name` and
   `dashboard_password`, or configure `[oidc]` for a supported release. The default
   dashboard is unauthenticated. Set `[master].admin_api_key` separately from
   `[server].api_key`; environment mappings include `GORSE_ADMIN_API_KEY` and
   `GORSE_SERVER_API_KEY`. API keys require protected TLS transport; keys alone do
   not encrypt HTTP. Configure documented gRPC SSL fields if required by the topology.
5. Persist database volumes, role-specific cache files, logs, and trained-model
   blobs. `[blob].uri` defaults to local storage; mount its actual resolved location
   or configure supported object storage. A database volume alone does not preserve
   every Gorse artifact. Ensure runtime accounts can write only required locations.
6. Set real feedback definitions and an appropriate recommendation pipeline before
   expecting personalization. An empty recommendation section defaults to latest
   items; more worker replicas do not create missing feedback or a missing pipeline.

## Docker: trial or persistent deployment

### Disposable trial only

The quick-start command, with host binding restricted to loopback:

```sh
docker run -p 127.0.0.1:8088:8088 zhenghaoz/gorse-in-one --playground
```

This unpinned command is for an authorized isolated trial, not a production rollout
or durable backup. Do not import the sample dataset into an existing instance.

### Persistent single node or cluster

1. Obtain the official Compose file and config for the chosen release, following
   [Docker Deployment][docker] or [Quick Start][quick]. Inspect them before use.
   For a split cluster, use one master plus server and worker services; a single
   node can use the official `zhenghaoz/gorse-in-one` image.
2. Pin all images; replace sample credentials; remove unnecessary published database,
   gRPC, and monitoring ports. Match config mount paths to the file you actually
   created: Docker examples use both `./config.toml` and `./config/config.toml`.
3. Add durable mounts for the artifacts above. The single-node example mounts config
   but does not persist every Gorse-local file. Do not reuse its defaults unchanged.
4. Start the reviewed stack in its own directory only after approval:

```sh
docker compose up -d
```

5. Verify database connectivity, dashboard node registration, and API readiness.
   Compose dependency ordering is not evidence that databases are ready. Never use
   volume deletion as a normal restart or troubleshooting step.

## Binary: single-node deployment

[Binary Deployment][binary] recommends the all-in-one executable, not a manually
managed multi-node binary cluster. Select the release artifact for the real OS/CPU,
verify its provenance, and install it under the user's approved policy. Prepare
external data/cache databases and a release-matched config first.

```sh
gorse-in-one --version
gorse-in-one --help
gorse-in-one -c config.toml
```

For a managed service, use writable persistent locations and the executable's
verified log/cache flags. The binary flag table lists `--master-cache-path` and
`--worker-cache-path`, while its systemd example uses `--cache-path`; do not copy
that discrepancy into a unit without checking the selected release's help. Review
service identity and permissions before installing/enabling a service.

## Kubernetes: inspect the selected chart before installing

[Kubernetes Deployment][kubernetes] documents Helm, PV provisioning, and a bundled
MongoDB dependency; it explicitly warns that chart parameters can change. Confirm
actual cluster/chart compatibility, images, resource settings, network exposure,
secret handling, and PV lifecycle with the chosen chart's parameter reference.
Do not assume historical minimum Kubernetes/Helm versions are current guidance.

The documented setup and values-file installation are:

```sh
helm repo add bitnami https://charts.bitnami.com/bitnami
helm repo add gorse-io https://charts.gorse.io
helm install gorse -f values.yaml gorse-io/gorse
helm list
```

Prepare and review `values.yaml` first, including `gorse.dashboard.username`,
`gorse.dashboard.password`, and `gorse.api.key` as supported by that chart. Use the
selected chart's supported version-pinning mechanism after checking Helm help;
these unversioned examples are not a production pin. Docs warn that Helm credential
changes may not update persisted application credentials. **Do not delete PVs to
rotate credentials.** Investigate the deployed chart and obtain an approved,
backed-up migration plan. Uninstall and storage deletion need separate authorization.

## Acceptance and handoff

- Verify the actual node versions, expected roles, DB access, durable mounts, and
  TLS/auth boundaries; test the application API on `8087` (cluster) or `8088`
  (all-in-one), adjusted for configured ports.
- Use the release's documented readiness probe; check task completion before a
  recommendation smoke test with an existing user. No ready models/data is different
  from a failed deployment. Check persistence across an approved restart, not deletion.
- Report what actually ran, endpoints, pinned versions, backup ownership, and any
  unverified compatibility. Never include secrets in the handoff.

## Official sources (pinned docs revision)

[quick]: https://github.com/gorse-io/docs/blob/5cef16bd228c4095de6bbfa0f46832c198a305eb/src/docs/quick-start.md
[docker]: https://github.com/gorse-io/docs/blob/5cef16bd228c4095de6bbfa0f46832c198a305eb/src/docs/deploy/docker.md
[binary]: https://github.com/gorse-io/docs/blob/5cef16bd228c4095de6bbfa0f46832c198a305eb/src/docs/deploy/binary.md
[kubernetes]: https://github.com/gorse-io/docs/blob/5cef16bd228c4095de6bbfa0f46832c198a305eb/src/docs/deploy/kubernetes.md
[config]: https://github.com/gorse-io/docs/blob/5cef16bd228c4095de6bbfa0f46832c198a305eb/src/docs/config.md
[pipeline]: https://github.com/gorse-io/docs/blob/5cef16bd228c4095de6bbfa0f46832c198a305eb/src/docs/concepts/pipeline.md

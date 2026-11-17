# Gorse CLI command reference

## Compatibility and installation

These examples were checked against official `gorse-io/cli` source revision
`1213e9dada2be39b8b4906541bd67f26133426dd`. Source coverage is not a claim that
an installed or latest released binary contains all commands. Run `--version`
and each relevant `--help`, and verify server compatibility before use.
Do not silently translate newer commands into legacy `context` / `get users`
syntax or assume `pipeline schema` / `cluster-info` exists in this revision.

Use an approved installation method from the [official CLI README][readme] or
[official releases][releases]. Installing/upgrading changes the local machine;
ask before doing it. Do not install a compiler or build from source just to run
an operator workflow. Installed help is the final check on command availability.
Examples below use POSIX shell quoting; adapt quoting for PowerShell or cmd.exe.

## Connection and read-only inspection

```sh
gorse-cli application add local --endpoint http://localhost:8088
gorse-cli application use local
gorse-cli application current
gorse-cli application list
gorse-cli stats
gorse-cli ps
gorse-cli user list -n 20
gorse-cli item list -n 20
gorse-cli user get USER_ID
gorse-cli item get ITEM_ID
gorse-cli feedback list --type like --user USER_ID --item ITEM_ID -n 20
gorse-cli item categories
```

The first two commands change local keyring/selection state, not remote data.
`application delete NAME` removes a local saved connection, not a remote service.
Use an approved HTTPS admin endpoint instead of the loopback sandbox address for
remote deployments. Per-field precedence is nonempty flag, environment, explicit
application, current application. Avoid mixing unrelated endpoint/key overrides.

User/item lists accept `--cursor`. Prefer the actual printed next-page command;
this is an illustrative shape, not a token to execute:

```text
Next page: gorse-cli user list -n 20 --cursor '<server-returned-cursor>'
```

The printed command quotes values for POSIX shells. It never echoes an explicitly
supplied key; replace `<api-key>` safely if present. Do not decode/re-encode a
cursor. No CLI cursor is exposed for feedback lists or item searches here.

Recommendation previews (substitute real IDs and configured recommender names):

```sh
gorse-cli recommend latest -n 10
gorse-cli recommend item-to-user USER_ID -n 10
gorse-cli recommend non-personalized NAME --user-id USER_ID -n 10
gorse-cli recommend item-to-item NAME ITEM_ID -n 10
gorse-cli recommend user-to-user NAME USER_ID -n 10
```

`latest` is global; user recommendations can exclude seen/read items. Previewing
items is not proof of genuine exposure and is not permission to create feedback.

## Data and transfers

All writes below require prior approval of the target and record scope. IDs,
labels, categories, and timestamps are illustrative and must come from the real
application contract. Never run a block wholesale as a production migration.

```sh
gorse-cli user add user-42 --labels='{"role":"reader"}' --comment='Profile'
gorse-cli user update user-42 --comment='Updated profile'
gorse-cli item add item-42 --category=books --labels='{"topics":["science"]}'
gorse-cli item update item-42 --is-hidden=false --category=books --category=science
gorse-cli item update item-42 --category= --comment=
gorse-cli user update user-42 --labels='{}'
```

- `add` can replace existing data; do not use it as a partial update. `update`
  changes only supplied fields, but labels/categories replace the complete field.
- `--category=` clears all categories; do not mix it with nonempty categories.
  `--labels='{}'` or `'[]'` explicitly clears/replaces labels; `null` is rejected.
- For observed events only: `feedback add TYPE USER_ID ITEM_ID --value=1
  --timestamp=RFC3339`. The default value is 1 and an omitted timestamp is current
  time. Historical replays need actual event timestamps. In the pinned SDK this
  uses additive POST feedback semantics; reconcile uncertain writes before retry.
- `user delete USER_ID --yes`, `item delete ITEM_ID --yes`, and `feedback delete
  TYPE USER_ID ITEM_ID --yes` are destructive. Approval must precede adding `--yes`;
  `--yes=false` is not confirmation.

Approved JSONL transfers:

```sh
gorse-cli user export users.jsonl
gorse-cli item export items.jsonl
gorse-cli feedback export feedback.jsonl
gorse-cli user import users.jsonl
gorse-cli item import items.jsonl
gorse-cli feedback import feedback.jsonl
cat users.jsonl | gorse-cli user import -
```

Each record is a JSON object on a line, not an array of records or a binary dump.
Exports contain sensitive application data. A named export replaces an existing
file only after successful completion; select a new path unless overwrite was
approved. File omission or `-` selects stdin/stdout; stdout has no status banner.
The CLI does not validate content, re-encode records, or split imports itself.
The bulk API replaces same-key records and completed server batches are not rolled
back on later error. Check exit status, response, and representative readback.
An older server can lack feedback-label preservation even with a newer client;
verify the server's metadata fidelity before a large feedback migration.

`dump backup.bin` / `restore backup.bin` use a **different binary format**. Choose
a new restricted backup path because dump can truncate an existing file. Restore
is an authorized overwrite of users/items/feedback/cache and retains its normal
interactive confirmation; no force flag is documented here. Capture config and
storage/blob recovery procedures separately, and verify restoration in isolation.

## Pipeline commands

Read the current full pipeline and the specific group before changing it:

```sh
gorse-cli pipeline get
gorse-cli pipeline item-to-item list
gorse-cli pipeline user-to-user list
gorse-cli pipeline non-personalized list
gorse-cli pipeline external list
gorse-cli pipeline collaborative get
gorse-cli pipeline data-source get
gorse-cli pipeline search get
gorse-cli pipeline ranker get
gorse-cli pipeline fallback get
gorse-cli pipeline replacement get
```

Named groups `item-to-item`, `user-to-user`, `non-personalized`, and `external`
provide `list`, `get NAME`, `add NAME`, `update NAME`, and `delete NAME`. Inspect
that exact action's help and existing names first. Item-to-item content types use
`--type` / `--column`; non-personalized rules use `--score` / `--filter`; external
scripts use `--script` or `--script-file`, not both. Deleting a named recommender
is a live pipeline write, and has no entity-deletion `--yes` gate. Remove or
repoint explicit ranker/fallback references deliberately; do not silently rewire
them. External scripts can contact other services: review destinations and data
exposure before enabling them.

The following settings updates overlay only changed flags onto the current full
pipeline. They are not an atomic compare-and-swap operation. Obtain approval and
coordinate other editors, preserve a baseline, and read back the result.

| Command | Settings flags |
| --- | --- |
| `pipeline update` | `--cache-size`, `--cache-expire`, `--context-size`, `--active-user-ttl` |
| `pipeline data-source update` | repeated `--positive-feedback-type`, `--negative-feedback-type`, `--read-feedback-type`; `--positive-feedback-ttl`, `--item-ttl` |
| `pipeline search update` | repeated `--column` |
| `pipeline ranker update` | `--type`, repeated `--recommender`, `--cache-expire`, `--fit-period`, `--fit-epoch`, `--optimize-period`, `--optimize-trials`, `--early-stopping-patience` |
| `pipeline ranker update` provider flags | `--reranker-url`, `--reranker-model`, `--reranker-auth-token`, `--reranker-query-template`, `--reranker-document-template`; `--decision-url`, `--decision-model`, `--decision-auth-token`, `--decision-state-template`, `--decision-instructions-template` |
| `pipeline fallback update` | repeated `--recommender` |
| `pipeline replacement update` | `--enable-replacement`, `--positive-replacement-decay`, `--read-replacement-decay` |

TTL flags above are in days; duration flags accept values such as `24h` or `1h30m`.
Zero disables TTL expiration and model optimization where documented by that
flag's help; it is not universally valid for cache size, cache expiration, or
training parameters. Explicit false/zero/empty strings are not omission. Repeated
list flags replace the complete ordered list. A sole `--column=` / feedback-type
empty flag / `--recommender=` requests a clear; Master can reject it, including
an empty ranker list. Do not retry a rejected configuration as a broad reset.

Approved examples (the example labels field and recommender name must exist):

```sh
gorse-cli pipeline update --cache-size=200 --cache-expire=48h
gorse-cli pipeline data-source update --positive-feedback-type=like --read-feedback-type=read
gorse-cli pipeline search update --column=item.Labels.title
gorse-cli pipeline item-to-item add catalog_tags --type=tags --column=item.Labels.topics
gorse-cli pipeline ranker update --type=none --recommender=item-to-item/catalog_tags --recommender=latest
gorse-cli pipeline fallback update --recommender=latest
gorse-cli pipeline replacement update --enable-replacement=false
```

Adding a source does not select it in ranker/fallback automatically. Current
ranker types are `none`, `fm`, `reranker`, and `decision`; do not copy a historical
`llm` value into this CLI without checking the server. Remote provider settings
can expose user/item data and incur costs. Configure trusted endpoint/model and
compatible templates with approval before selecting a remote ranker. Provider
token flags expose values to process arguments: use the operator's approved
secret-handling procedure, not literal secrets in shared shell history.

`pipeline collaborative update` supports `--type`, `--fit-period`, `--fit-epoch`,
`--optimize-period`, and `--optimize-trials`. Its available flags differ from the
ranker's; do not infer early-stopping support from a field name in server config.
`pipeline reset` prompts before returning to file defaults; it is not restoration
of an exported YAML baseline. There is no apply-file/edit command in this source
revision. Read back settings and check `ps`/previews after any approved change.

## Official sources

Command examples above follow the pinned official CLI source, not private notes:

- [CLI registration, global flags and version][main]
- [Application selection, keyring and per-field credential precedence][application]
- [User CRUD, lists and resource transfer][user]
- [Item CRUD, search, lists and resource transfer][item]
- [Feedback commands and filters][feedback]
- [Pipeline command and flag definitions][pipeline]
- [Read-only inspection, JSONL adapters, cursor hints and binary backups][misc]
- [The pinned SDK's additive feedback insertion][sdk]

[readme]: https://github.com/gorse-io/cli/blob/1213e9dada2be39b8b4906541bd67f26133426dd/README.md
[releases]: https://github.com/gorse-io/cli/releases
[main]: https://github.com/gorse-io/cli/blob/1213e9dada2be39b8b4906541bd67f26133426dd/main.go
[application]: https://github.com/gorse-io/cli/blob/1213e9dada2be39b8b4906541bd67f26133426dd/internal/application.go
[user]: https://github.com/gorse-io/cli/blob/1213e9dada2be39b8b4906541bd67f26133426dd/internal/user.go
[item]: https://github.com/gorse-io/cli/blob/1213e9dada2be39b8b4906541bd67f26133426dd/internal/item.go
[feedback]: https://github.com/gorse-io/cli/blob/1213e9dada2be39b8b4906541bd67f26133426dd/internal/feedback.go
[pipeline]: https://github.com/gorse-io/cli/blob/1213e9dada2be39b8b4906541bd67f26133426dd/internal/pipeline.go
[misc]: https://github.com/gorse-io/cli/blob/1213e9dada2be39b8b4906541bd67f26133426dd/internal/misc.go
[sdk]: https://github.com/gorse-io/gorse-go/blob/062d740c10a2/client.go

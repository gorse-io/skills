# Gorse Skills

Reusable agent skills for **using, operating, and contributing to** the Gorse
recommender system. User skills turn the [official documentation](https://github.com/gorse-io/docs)
into task-oriented procedures; contributor skills support source changes.

## User skills

Start here to build a recommendation service without modifying Gorse source.

| Skill | Use it for |
| --- | --- |
| [gorse-deployment](skills/gorse-deployment/SKILL.md) | Run a demo, choose a production topology, configure storage, and verify deployment |
| [gorse-data-ingestion](skills/gorse-data-ingestion/SKILL.md) | Model and import users, items, and genuine feedback; validate event semantics |
| [gorse-api-integration](skills/gorse-api-integration/SKILL.md) | Connect an application through REST/SDKs, retrieve recommendations, and handle feedback |
| [gorse-recommendation-tuning](skills/gorse-recommendation-tuning/SKILL.md) | Select candidates, configure ranking/fallback, handle cold starts, and evaluate quality |
| [gorse-operations](skills/gorse-operations/SKILL.md) | Inspect health/tasks, diagnose empty or stale results, and plan safe backup/restore |

Suggested path: deployment → data ingestion → API integration → recommendation
tuning. Use operations whenever a running service needs inspection or recovery.
Each skill links to the relevant official docs. Match the documentation and
configuration to the deployed Gorse release; development-branch docs can differ.

## Contributor skills

Use these when the task is to change Gorse source, SDKs, installers, or docs—not
merely configure or consume a running recommendation service.

| Skill | Use it for |
| --- | --- |
| [gorse-contribution-workflow](skills/gorse-contribution-workflow/SKILL.md) | Repository discovery, focused changes, PRs, CI verification, and backports |
| [gorse-core-development](skills/gorse-core-development/SKILL.md) | Configuration, recommenders, service lifecycle, and API/auth boundaries |
| [gorse-storage-development](skills/gorse-storage-development/SKILL.md) | Data/cache/vector contracts, search, proxies, and backend verification |
| [gorse-cli-development](skills/gorse-cli-development/SKILL.md) | Commands, playground examples, installers, and native package wrappers |
| [gorse-sdk-development](skills/gorse-sdk-development/SKILL.md) | REST wrappers, cross-language API parity, and integration tests |
| [gorse-docs-authoring](skills/gorse-docs-authoring/SKILL.md) | Bilingual documentation, navigation, examples, and build checks |

## Usage

Each directory under `skills/` is independently usable and contains a `SKILL.md`
with `name` and `description` frontmatter. Copy the selected **whole directory**,
including any references, into the skill directory supported by your agent.
No skill requires installing the entire collection.

For user tasks, identify the running version, target environment, permissions, and
existing data before making changes. Begin with read-only inspection. Obtain
approval before production deployment, writes, import/restore, destructive actions,
or paid external services. Do not use a live production instance for examples.

For contributor tasks, read repository instructions and inspect the requested
revision. Discover branch names, package scripts, API contracts, and test prerequisites
from the checkout. Pair `gorse-contribution-workflow` with a specialized skill for
end-to-end contribution work. Historical patterns are inspection prompts, not
commands to apply blindly. Publish only within the user's authorization.

## Scope

Included: public Gorse user workflows grounded in official documentation, and
reusable contributor practices distilled from core, CLI, SDK, docs, and storage work.
These skills are not copies of chat histories or a replacement for release-specific
documentation, repository instructions, or effective runtime configuration.

Excluded: private Cloud project details, credentials, personal author identities,
machine-specific paths, transient failures, session transcripts, and raw task logs.
Standalone vector database development and unrelated infrastructure workflows are
outside this collection.

## Contributing

- Keep each skill focused and its trigger description specific about the audience.
- Ground user-facing flags, config fields, ports, and API examples in official docs;
  include source links and distinguish documented behavior from operational advice.
- Prefer concise procedures over copies of past patches or discussions.
- Put longer implementation checklists in that skill's `references/` directory.
- Keep references relative and self-contained; never depend on a private local skill.
- Preserve explicit user scope and distinguish verified results from assumptions.
- Avoid prescribing a historical API or dependency version as universally current.
- Run the repository validator and its tests before submitting changes:

```sh
python3 scripts/validate_skills.py
python3 -m unittest discover -s scripts -p 'test_*.py' -v
```

The validator checks structure, frontmatter, local links, and accidental private
machine/session references. It does not execute a live Gorse deployment or prove
that all configuration/API examples match every supported release.

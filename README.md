# Gorse Skills

Reusable agent skills for **using and operating** the Gorse recommender system.
These skills turn the [official documentation](https://github.com/gorse-io/docs)
into task-oriented procedures for application users and operators.

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

## Usage

Each directory under `skills/` is independently usable and contains a `SKILL.md`
with `name` and `description` frontmatter. Copy the selected **whole directory**,
including any references, into the skill directory supported by your agent.
No skill requires installing the entire collection.

For user tasks, identify the running version, target environment, permissions, and
existing data before making changes. Begin with read-only inspection. Obtain
approval before production deployment, writes, import/restore, destructive actions,
or paid external services. Do not use a live production instance for examples.

## Scope

Included: public Gorse user workflows for deployment, data ingestion, application
API/SDK integration, recommendation tuning, and operations, grounded in official
documentation.
These skills are not copies of chat histories or a replacement for release-specific
documentation, repository instructions, or effective runtime configuration.

Excluded: private Cloud project details, credentials, personal author identities,
machine-specific paths, transient failures, session transcripts, and raw task logs.
Source-development workflows, standalone vector database development, and unrelated
infrastructure workflows are outside this collection.

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

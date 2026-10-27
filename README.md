# Gorse Skills

Reusable agent skills for contributing to the Gorse recommender-system ecosystem.
These are curated workflows, not an export of chat histories or a replacement for
repository instructions and the source code at the revision being changed.

## Skills

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
Use `gorse-contribution-workflow` alongside a specialized skill for end-to-end
contribution work. Paths in a skill are relative to the repository being changed
unless explicitly described otherwise.

Read the target repository's instructions first. Discover branch names, package
scripts, API contracts, and test prerequisites from the current checkout. Historical
implementation patterns are prompts to inspect code, not commands to apply blindly.
Only commit, push, merge, deploy, or install tools within the user's authorization.

## Scope

Included: reusable public Gorse development practices distilled from core, CLI,
SDK, documentation, and storage work.

Excluded: private Cloud project details, credentials, personal author identities,
machine-specific paths, transient failures, session transcripts, and raw task logs.
Standalone vector database development and unrelated infrastructure workflows are
outside this initial collection.

## Contributing

- Keep each skill focused and its trigger description specific.
- Prefer concise procedures over copies of past patches or discussions.
- Put longer implementation checklists in that skill's `references/` directory.
- Keep references relative and self-contained; never depend on a private local skill.
- Preserve explicit user scope and distinguish verified results from assumptions.
- Avoid prescribing a historical API or dependency version as universally current.
- Run the repository validator before submitting changes:

```sh
python3 scripts/validate_skills.py
```

The validator checks structure, frontmatter, local links, and accidental private
machine/session references. It does not execute the target Gorse repositories'
builds or prove their current APIs match every example.

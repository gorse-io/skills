# Gorse Skills

Reusable skills for helping users adopt, integrate, operate, evaluate, and contribute to [Gorse](https://github.com/gorse-io/gorse), an open-source recommender system.

These skills are organized around user jobs rather than source-code directories. They are intended for AI assistants, documentation agents, support bots, and human contributors who need consistent, task-oriented guidance.

## Skill Index

| Skill | Audience | Use when |
| --- | --- | --- |
| `gorse-quickstart` | First-time users | Starting Gorse locally and getting first recommendations |
| `gorse-data-modeling` | Application developers | Mapping business data to users, items, and feedback |
| `gorse-api-integration` | Backend/full-stack developers | Integrating with REST APIs or SDKs |
| `gorse-recommendation-pipeline` | Developers/operators | Explaining retrieval, ranking, filtering, and caching |
| `gorse-config-tuning` | Engineers tuning behavior | Editing `config.toml` and recommender/ranker settings |
| `gorse-deployment` | Operators/platform engineers | Deploying single-node or distributed Gorse |
| `gorse-dashboard-usage` | Admins/product users | Using the web dashboard for data, tasks, and monitoring |
| `gorse-troubleshooting` | All users | Diagnosing empty recommendations, task, data, and deployment issues |
| `gorse-evaluation-optimization` | Data/ML/product teams | Evaluating recommendation quality and improving outcomes |
| `gorse-cli-usage` | Admins/operators | Using `gorse-cli` for administration and debugging |
| `gorse-sdk-integration` | App developers | Choosing REST vs SDK and integrating language clients |
| `gorse-use-case-recipes` | Solution designers | Designing Gorse setups for common business scenarios |
| `gorse-contributor-development` | Contributors | Understanding the codebase and making changes |

## Layout

Each skill lives at:

```text
skills/gorse/<skill-name>/SKILL.md
```

Each file uses YAML frontmatter followed by actionable Markdown guidance.

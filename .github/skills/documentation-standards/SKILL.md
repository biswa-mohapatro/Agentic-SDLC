---
name: documentation-standards
description: "Standards and templates for technical documentation. Use when: writing README files, API documentation, migration guides, architecture overviews, configuration references, changelog entries. Loaded by Docs Engineer agent."
---

# Documentation Standards — Skill

This skill defines the templates, tone, and quality standards for all project documentation.

---

## Document Types & Templates

### README.md

Structure:
```markdown
# Project Name

One-sentence description of what this project does.

## Features
- Feature 1 — brief description
- Feature 2 — brief description

## Quick Start

### Prerequisites
- Requirement 1
- Requirement 2

### Installation
\`\`\`bash
command to install
\`\`\`

### Configuration
Copy `.env.example` to `.env` and fill in your values:
\`\`\`bash
cp .env.example .env
\`\`\`

| Variable | Required | Default | Description |
|----------|----------|---------|-------------|
| `DB_TYPE` | Yes | — | Database backend |

### Running
\`\`\`bash
command to run
\`\`\`

## Architecture

\`\`\`
User → API → Pipeline → Adapter → Database
                 ↓
            LLM Service
\`\`\`

## Development

### Running Tests
\`\`\`bash
pytest tests/
\`\`\`

### Project Structure
\`\`\`
src/
├── adapters/    # Database adapters
├── core/        # Business logic
└── api/         # API endpoints
\`\`\`

## License
```

### MIGRATION.md

Structure:
```markdown
# Migration Guide: [version or change]

## What Changed
Brief summary of the breaking changes.

## Who Is Affected
- Users doing X need to update Y
- Users doing Z are NOT affected

## Step-by-Step Migration

### Step 1: Update configuration
Before:
\`\`\`
OLD_VAR=value
\`\`\`
After:
\`\`\`
NEW_VAR=value
\`\`\`

### Step 2: Update imports
Before:
\`\`\`python
from old.module import OldClass
\`\`\`
After:
\`\`\`python
from new.module import NewClass
\`\`\`

## Troubleshooting
| Symptom | Cause | Fix |
|---------|-------|-----|
| ImportError | Old import path | Update to new path |
```

### .env.example

```bash
# ─────────────────────────────────────────────
# Core Settings (always required)
# ─────────────────────────────────────────────
VARIABLE_NAME=placeholder-value

# ─────────────────────────────────────────────
# Feature Group (when FEATURE_ENABLED=true)
# ─────────────────────────────────────────────
FEATURE_SETTING=placeholder
```

Rules:
- **Every** env variable used by the project must be listed
- Group by feature/module with comment headers
- Use `placeholder-value`, `your-api-key`, `your-host.example.com` — never real values
- Include the comment for each variable explaining what it does

---

## Writing Style

### Tone
- Technical but accessible
- Present tense: "The adapter **returns**..." not "will return"
- Active voice: "Run the command" not "The command should be run"
- Second person for instructions: "Set your API key" not "Users should set their API key"

### Formatting
- Code in backticks: `DB_TYPE`, `execute_async()`
- File paths in backticks: `config/settings.py`
- Commands in code blocks with `bash` language tag
- Configuration in code blocks with appropriate language tag

### Tables Over Prose

Bad:
> The DB_TYPE variable controls which database backend is used. It can be set to "databricks" for Databricks, "postgresql" for PostgreSQL, or "duckdb" for DuckDB.

Good:
| `DB_TYPE` | Backend | Install Command |
|-----------|---------|-----------------|
| `databricks` | Databricks | `pip install .[databricks]` |
| `postgresql` | PostgreSQL | `pip install .[postgresql]` |
| `duckdb` | DuckDB | `pip install .[duckdb]` |

---

## Quality Checklist

Before completing documentation:

- [ ] All code examples reference actual files/functions in the project
- [ ] All commands are copy-pasteable (no placeholder paths)
- [ ] No real credentials, tokens, or internal URLs
- [ ] Links use relative paths within the project
- [ ] Every env variable in `.env.example` has a comment
- [ ] The Quick Start section works end-to-end for a new developer
- [ ] Configuration table has all required variables with types and defaults

---

## Inline Documentation (Docstrings)

Only add docstrings to **new public APIs** created during this cycle. Don't add docstrings to existing code.

### Python — Google Style
```python
def execute_async(self, sql_text: str, fetch_all: bool = True) -> dict[str, Any]:
    """Execute a SQL query and return normalised results.

    Args:
        sql_text: The SQL query to execute.
        fetch_all: Whether to fetch all rows. When False, returns status only.

    Returns:
        Dict with "columns" (list of str) and "rows" (list of tuple).

    Raises:
        RuntimeError: If the database connection fails.
    """
```

### TypeScript — JSDoc
```typescript
/**
 * Execute a query and return normalised results.
 * @param sql - The SQL query to execute
 * @returns Object with columns and rows arrays
 * @throws {ConnectionError} If the database is unreachable
 */
```

Match the existing docstring style in the project. Don't introduce a new format.

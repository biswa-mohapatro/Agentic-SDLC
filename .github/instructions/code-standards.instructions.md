---
description: 'Code quality standards for all implementation work. Enforces naming conventions, function design, error handling, import organization, and anti-patterns. Distilled from the code-quality skill for automatic application.'
applyTo: '**/*.py, **/*.ts, **/*.js, **/*.jsx, **/*.tsx'
---

# Code Standards

## Principles

1. **Readability over cleverness.** Code is read 10x more than written.
2. **Consistency over perfection.** Match the existing codebase style.
3. **Explicit over implicit.** Type hints, clear names, no magic.
4. **Fail fast, fail loud.** Validate early, raise exceptions, don't return None for errors.

## Naming

- **Discover first**: Read 5-10 existing files before naming anything. Match what exists.
- Names describe **what**, not **how**: `get_active_users()` not `query_database_for_users_where_active()`
- Booleans: `is_`, `has_`, `can_`, `should_`
- Collections: plural (`users`, `results`)
- No abbreviations except universals: `id`, `url`, `sql`

## Functions

- **Single responsibility**: One sentence description without "and"
- **0-3 params** ideal; 4-5 use a data class; 6+ refactor
- **Consistent return type**: Don't return `str | None | dict` from the same function
- Prefer raising exceptions over returning error codes or None

## Error Handling

- **At system boundaries**: Catch specific exceptions, log with context, re-raise as application errors with `raise ... from exc`
- **Inside business logic**: Don't catch exceptions — let them propagate
- **Never**: `except Exception: pass`, bare `except:`, return None to indicate failure, hide errors behind defaults

## Imports

1. Standard library
2. Third-party
3. Local project

Groups separated by blank lines. Alphabetical within each group.

## Anti-Patterns to Fix on Sight

| Anti-Pattern | Fix |
|-------------|-----|
| God class doing everything | Split into focused classes |
| Shotgun surgery across files | Consolidate related logic |
| Dead code / unused imports | Delete them |
| Magic numbers (`if status == 3`) | Named constants |
| String typing (`if role == "admin"`) | Enums |

## Module Structure

- Target < 300 lines per file; split if > 500
- `__init__.py` exports public API only
- One class per file for major abstractions

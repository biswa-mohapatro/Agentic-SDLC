---
name: code-quality
description: "Shared engineering standards for writing clean, maintainable code. Use when: implementing features, reviewing code, refactoring, enforcing naming conventions, structuring modules, error handling patterns. Loaded by Developer and Reviewer agents."
---

# Code Quality — Shared Skill

This skill defines the universal code quality standards that apply to all implementation and review work, regardless of the specific project or language.

---

## Principles

1. **Readability over cleverness.** Code is read 10x more than it's written.
2. **Consistency over perfection.** Match the existing codebase style, even if you prefer a different one.
3. **Explicit over implicit.** Type hints, clear names, no magic.
4. **Fail fast, fail loud.** Validate inputs early, raise exceptions, don't return None for errors.

---

## Naming Conventions

### Discover First, Then Follow

Before naming anything, read 5-10 existing files in the project to learn:
- Are classes `PascalCase` or `snake_case`?
- Are constants `UPPER_SNAKE_CASE`?
- Are private methods prefixed with `_`?
- Are modules named as nouns (`adapter`) or verbs (`adapting`)?
- Are test files `test_foo.py` or `foo_test.py`?

**Match what exists.** Do not introduce a new convention.

### Universal Rules
- Names should describe **what**, not **how**: `get_active_users()` not `query_database_for_users_where_active()`
- Boolean names start with `is_`, `has_`, `can_`, `should_`
- Collection names are plural: `users`, `table_names`, `results`
- Avoid abbreviations unless they're universal: `id`, `url`, `sql` are fine; `tbl`, `usr`, `mgr` are not

---

## Function Design

### Single Responsibility
Each function should do one thing. If you can't describe it in one sentence without "and", split it.

### Parameter Limits
- 0-3 parameters: fine
- 4-5: consider a data class or dict
- 6+: refactor into smaller functions or use a config object

### Return Types
- Always return a consistent type. Don't return `str | None | dict` from the same function.
- Prefer raising exceptions over returning error codes or None.
- For functions that can fail: return the result or raise, never both.

---

## Error Handling

### At System Boundaries (entry points, APIs, adapters)
```
try:
    result = external_call()
except SpecificError as exc:
    logger.error("Context: %s", exc)
    raise AppError("User-friendly message") from exc
```

### Inside Business Logic
Don't catch exceptions. Let them propagate to the boundary handler.

### Never Do
- `except Exception: pass` — silently swallowing errors
- `except: ...` — catching BaseException including KeyboardInterrupt
- Return `None` to indicate failure — raise instead
- `try: ... except: return default_value` — hiding errors behind defaults

---

## Import Organization

Follow the project's existing order. If there's no convention, use:
1. Standard library imports
2. Third-party library imports
3. Local project imports

Each group separated by a blank line. Alphabetical within each group.

---

## Module Structure

### File Length
- Aim for < 300 lines per module
- If a file exceeds 500 lines, consider splitting by responsibility

### Package Organization
- `__init__.py` should export the public API only
- Internal helpers should not be in `__init__.py`
- One class per file for major abstractions; utility functions can share a file

---

## Logging

### Standards
- Use the project's logging framework (find it: search for `get_logger`, `logging.getLogger`, `console.log`)
- Log at appropriate levels:
  - `DEBUG`: internal state useful for debugging
  - `INFO`: significant events (startup, connection, request completed)
  - `WARNING`: something unexpected but recoverable
  - `ERROR`: something failed and needs attention
- Include context in log messages: `"SQL execution failed. sql=%s error=%s"` not `"Error occurred"`
- Never log credentials, tokens, or PII

---

## Anti-Patterns to Catch

| Anti-Pattern | Fix |
|-------------|-----|
| God class (class doing everything) | Split into focused classes |
| Shotgun surgery (change requires touching many files) | Consolidate related logic |
| Feature envy (function using another class's data more than its own) | Move the function to the data's class |
| Dead code (unreachable functions, unused imports) | Delete it |
| Magic numbers (`if status == 3`) | Use named constants |
| String typing (`if role == "admin"`) | Use enums |

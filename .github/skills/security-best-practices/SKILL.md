---
name: security-best-practices
description: "Shared security standards based on OWASP Top 10. Use when: implementing features that handle user input, database queries, authentication, API endpoints, file operations, dependency management. Loaded by Developer and Reviewer agents."
---

# Security Best Practices — Shared Skill

This skill encodes security engineering knowledge that applies to all implementation and review work.

---

## OWASP Top 10 Checklist

### 1. Injection (SQL, Command, LDAP)

**Rule**: Never concatenate user input into queries.

```python
# BAD — SQL injection vulnerable
cursor.execute(f"SELECT * FROM users WHERE name = '{user_input}'")

# GOOD — parameterized query
cursor.execute("SELECT * FROM users WHERE name = %s", (user_input,))
```

**For ORM queries**: Use ORM methods, never raw SQL with string concatenation.
**For shell commands**: Use `subprocess.run(["cmd", arg])` with a list, never `os.system(f"cmd {arg}")`.

### 2. Broken Authentication

- Never hardcode credentials, tokens, or API keys in source code
- Load all secrets from environment variables or secret managers
- Never log credentials — not even in debug mode
- Rotate default credentials before deployment

### 3. Sensitive Data Exposure

- Don't log PII (emails, names, IP addresses) at INFO level or above
- Don't include sensitive data in error messages returned to users
- Use `repr()` truncation for SQL in logs: `sql_text[:200]`
- Ensure `.env` files are in `.gitignore`

### 4. Broken Access Control

- Validate permissions at the API boundary, not in business logic
- Use allow-lists, not deny-lists for authorization
- Default to deny — require explicit permission grants

### 5. Security Misconfiguration

- Don't leave debug mode enabled in production configs
- Don't expose stack traces to end users
- Set secure defaults — SSL mode "require", not "disable"
- Review dependency versions for known vulnerabilities

### 6. Vulnerable Dependencies

- Pin dependency versions in `pyproject.toml` / `package.json`
- Don't use `*` or unpinned versions
- When adding a new dependency, verify it's actively maintained
- Prefer well-known packages over obscure alternatives

---

## Secrets Management

### Detection Pattern

Before committing, search for patterns that indicate leaked secrets:
```
# Patterns to flag:
(?i)(password|secret|token|api_key|access_key)\s*=\s*["'][^"']+["']
(?i)dapi[a-zA-Z0-9]{32,}      # Databricks PATs
(?i)sk-[a-zA-Z0-9]{32,}        # OpenAI keys
(?i)ghp_[a-zA-Z0-9]{36}        # GitHub PATs
```

### Correct Pattern

```python
# All secrets from environment, with clear error on missing
import os

API_KEY = os.environ.get("API_KEY")
if not API_KEY:
    raise EnvironmentError("API_KEY environment variable is required")
```

Or via Pydantic Settings (preferred for Python projects):
```python
class Settings(BaseSettings):
    api_key: str = Field(..., description="API key for external service")

    model_config = SettingsConfigDict(env_file=".env")
```

---

## Input Validation

### At System Boundaries

Validate all external input at the point of entry (API handler, CLI argument parser, file reader).

```python
def handle_request(table_name: str) -> dict:
    # Validate format before using
    if not re.match(r'^[a-zA-Z0-9_]+\.[a-zA-Z0-9_]+\.[a-zA-Z0-9_]+$', table_name):
        raise ValueError(f"Invalid table name format: {table_name!r}")
    # Now safe to use
```

### SQL Safety for Text-to-SQL Systems

When the project generates SQL from LLM output:
- Always validate generated SQL is read-only (SELECT only, no DML/DDL)
- Validate table references against an allow-list
- Set query timeouts to prevent runaway queries
- Limit result set sizes

---

## File Operations

- Never use `eval()` or `exec()` on file contents
- Validate file paths — prevent path traversal (`../../../etc/passwd`)
- Use `pathlib.Path` for path manipulation
- Set appropriate file permissions on created files (not world-readable)

---

## Dependency Safety

When adding dependencies:
1. Verify the package exists on the official registry (PyPI, npm, NuGet)
2. Check download count and last release date — avoid abandoned packages
3. Check for known vulnerabilities on Snyk, GitHub Advisory Database
4. Prefer stdlib solutions when the functionality is simple

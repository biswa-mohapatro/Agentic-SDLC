---
description: 'Security standards based on OWASP Top 10. Enforces input validation, parameterized queries, credential handling, and dependency safety. Distilled from the security-best-practices skill for automatic application.'
applyTo: '**/*.py, **/*.ts, **/*.js, **/*.jsx, **/*.tsx, **/*.yaml, **/*.yml, **/*.toml, **/*.json, **/*.env*'
---

# Security and OWASP Standards

## Injection Prevention

- **Never** concatenate user input into SQL, shell commands, or LDAP queries
- Use parameterized queries: `cursor.execute("SELECT * FROM t WHERE id = %s", (id,))`
- Use `subprocess.run(["cmd", arg])` with a list, never `os.system(f"cmd {arg}")`
- For ORMs: use ORM methods, never raw SQL with string concatenation

## Credential Safety

- **Never** hardcode credentials, tokens, API keys, or secrets in source code
- Load all secrets from environment variables or secret managers
- **Never** log credentials — not even in debug mode
- Ensure `.env` files are in `.gitignore`
- Detect patterns before committing: `password=`, `api_key=`, `sk-`, `ghp_`, `dapi`

## Input Validation

- Validate **all** external input at system boundaries (API handlers, CLI parsers, file readers)
- Use allow-lists for table names, file paths, and user roles
- Reject invalid input early with clear error messages
- Set query timeouts and result set limits for generated SQL

## Sensitive Data

- Don't log PII (emails, names, IPs) at INFO level or above
- Don't include sensitive data in error messages returned to users
- Truncate SQL in logs: `sql_text[:200]`

## Dependencies

- Pin versions in `pyproject.toml` / `package.json` — no `*` or unpinned
- Verify new dependencies are actively maintained
- Prefer well-known packages over obscure alternatives

## Forbidden Patterns

- `eval()`, `exec()`, `pickle.loads()` on untrusted data
- `chmod 777` or world-writable permissions
- Debug mode in production configs
- Stack traces exposed to end users
- `os.system()` with string interpolation

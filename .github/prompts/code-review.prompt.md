---
description: "Review code for quality, security, and correctness"
agent: "Reviewer"
---

Review the code or changes described by the user. Apply all four review lenses:

1. **Correctness** — Logic errors, edge cases, off-by-one, null/undefined handling
2. **Security** — OWASP Top 10, injection, credential exposure, input validation
3. **Code Quality** — Naming, function design, duplication, complexity
4. **Architecture** — Consistency with existing patterns, separation of concerns

If issues are found, classify by severity (critical/warning/nit), fix what you can, and report the rest.

{{input}}

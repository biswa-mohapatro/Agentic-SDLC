---
description: "Refactor code to improve quality without changing behavior"
agent: "Developer"
---

Refactor the code described by the user. Read the workspace context from `copilot-instructions.md`, then:

1. **Understand** — Read the target code, understand its purpose, inputs, outputs, and behavior.
2. **Identify** — Find what to improve: naming, function size, duplication, complexity, coupling.
3. **Refactor** — Make changes incrementally, one at a time, preserving external behavior.
4. **Validate** — Run existing tests after each change to confirm no regressions.

**Rules**:
- Do NOT add new features or change external behavior
- Do NOT refactor code outside the scope the user identified
- If no tests exist, write them BEFORE refactoring to establish a safety net

{{input}}

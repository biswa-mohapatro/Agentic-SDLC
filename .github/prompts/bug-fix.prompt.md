---
description: "Diagnose and fix a bug — streamlined SDLC (discovery → fix → test → review)"
agent: "Project Lead"
---

The user needs to fix a bug. Read the workspace context from `copilot-instructions.md`, then run a **streamlined SDLC**:

1. **Phase 0 — Discovery**: Understand the bug from the user's description, error messages, stack traces, or reproduction steps. If a Jira ticket key is provided, read it via MCP for context.
2. **Phase 3 — Implementation**: Delegate to Developer to diagnose root cause and implement the fix.
3. **Phase 4 — Testing**: Delegate to Test Engineer to add regression tests covering the bug.
4. **Phase 5 — Review**: Delegate to Reviewer to verify correctness and check for side effects.

**Skip** planning, architecture, and documentation phases unless the fix requires structural changes.

User input: {{input}}

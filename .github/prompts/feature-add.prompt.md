---
description: "Add a new feature — full SDLC minus architecture (unless needed)"
agent: "Project Lead"
---

The user wants to add a new feature. Read the workspace context from `copilot-instructions.md`, then run the SDLC pipeline:

1. **Phase 0 — Discovery & Scoping**: Clarify feature requirements. If a Jira ticket key is provided, read it via MCP.
2. **Phase 1 — Planning**: Delegate to Planner to break the feature into tasks.
3. **Phase 3 — Implementation**: Delegate to Developer to build the feature.
4. **Phase 4 — Testing**: Delegate to Test Engineer to write tests.
5. **Phase 5 — Review**: Delegate to Reviewer for quality and security review.
6. **Phase 6 — Documentation**: Delegate to Docs Engineer to update docs.

**Skip** architecture phase unless the feature introduces new patterns, services, or interfaces.

User input: {{input}}

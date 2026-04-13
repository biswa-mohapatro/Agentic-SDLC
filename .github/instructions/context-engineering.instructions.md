---
description: 'Context engineering standards for structuring AI-consumable project knowledge. Enforces layered context, progressive disclosure, freshness, and anti-patterns. Applied to project documentation and customization files.'
applyTo: '**/copilot-instructions.md, **/ARCHITECTURE.md, **/PRODUCT.md, **/CONTRIBUTING.md, **/AGENTS.md, **/*.agent.md, **/*.prompt.md, **/SKILL.md, **/*.instructions.md'
---

# Context Engineering Standards

## Principles

1. **Start small, iterate.** Begin with minimal context; add detail only when the agent makes repeated mistakes.
2. **Keep context fresh.** Audit project docs with every significant change. Stale context is worse than no context.
3. **Progressive disclosure.** High-level overview first, detail on demand. Don't front-load everything.
4. **Separate concerns.** Different activity types (planning, coding, testing, review) belong in different context sources — not one monolithic file.

## Context Layering

| Layer | File(s) | Scope | Update Cadence |
|-------|---------|-------|---------------|
| Project-wide | `copilot-instructions.md` | Every interaction | On arch / process change |
| Module-specific | `*.instructions.md` with `applyTo` globs | Matching files only | When conventions shift |
| Task-specific | `*.prompt.md`, plan files | Single task | Per feature / bug |
| Role-specific | `*.agent.md`, `SKILL.md` | Agent invocations | On workflow refinement |

## What Belongs in `copilot-instructions.md`

- Project purpose (1–2 sentences)
- Links to supporting docs (`ARCHITECTURE.md`, `PRODUCT.md`, `CONTRIBUTING.md`)
- Key architectural decisions (patterns, frameworks, languages)
- Build / run / test commands
- MCP integration toggles (Jira, Confluence)

**Max target: 2 printed pages.** If it grows beyond that, extract detail into dedicated docs and link to them.

## What Does NOT Belong in Always-On Context

- Full API reference or schema dumps — move to linked docs
- Meeting notes, changelogs, or historical context — move to version control
- Verbose code examples — keep in skills or instructions files
- Personal preferences unrelated to the current project

## Writing Effective Context Docs

- Use **decision-making context**: information that changes what the agent would do, not encyclopaedic detail.
- Prefer **tables over prose** for configuration, enums, and mappings.
- Use **consistent terminology**: pick one term per concept and use it everywhere.
- Reference external standards (OWASP, INVEST) by name — agents know them.
- Include **anti-patterns** alongside preferred patterns so agents avoid known mistakes.

## Plan Documents

When producing implementation plans:

- Structure with a title, brief description, architecture notes, and a task checklist.
- Each task should be independently testable and map to a single commit.
- Note open questions (1–3) that block implementation.
- Save plans to a file (`<feature>-plan.md`) for large features; reference in chat for small ones.

## Handoff Context

When an agent hands off to the next phase:

- Summarise **what was done** (decisions made, files changed).
- State **what still needs doing** (next steps, known gaps).
- Note **any deviations** from the plan and why.

## Version and Review

- Track all context files in git — treat them as code.
- Review context docs during pull requests to catch staleness.
- Delete or archive context that no longer applies.

## Anti-Patterns

| Anti-Pattern | Fix |
|-------------|-----|
| Context dumping (walls of text in instructions) | Distill to decision-relevant bullets; link to full docs |
| Inconsistent guidance across files | Single source of truth per topic; cross-reference, don't duplicate |
| Neglecting validation | Spot-check agent outputs against context to catch misunderstanding |
| One-size-fits-all context | Use `applyTo` globs and role-specific agents to scope relevance |
| Never updating context after refactors | Add context review to the PR checklist |

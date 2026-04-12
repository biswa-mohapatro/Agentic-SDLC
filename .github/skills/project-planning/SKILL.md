---
name: project-planning
description: "Workflow for breaking requirements into implementation plans. Use when: parsing PRDs, creating task breakdowns, identifying dependencies between tasks, scoping work, estimating affected files. Loaded by Planner agent."
---

# Project Planning — Skill

This skill defines the methodology for breaking down product requirements into engineering implementation plans.

---

## Requirement Analysis Framework

### INVEST Criteria for Tasks

Every task in your plan should satisfy INVEST:
- **I**ndependent — can be implemented without waiting for other tasks (or specify the dependency)
- **N**egotiable — captures intent, not exact implementation details
- **V**aluable — delivers a meaningful unit of progress
- **E**stimable — scope is clear enough to estimate effort
- **S**mall — completable in a focused session (not a multi-day epic)
- **T**estable — has clear acceptance criteria

---

## Decomposition Strategy

### Top-Down Decomposition

```
PRD / Feature Request
  └── Epic 1: [major capability]
        ├── Task 1.1: [foundation change]
        ├── Task 1.2: [depends on 1.1]
        └── Task 1.3: [independent of 1.2]
  └── Epic 2: [another capability]
        ├── Task 2.1: [foundation]
        └── Task 2.2: [depends on 2.1]
```

### Ordering Rules

1. **Foundation first**: Abstract interfaces before concrete implementations
2. **Create before consume**: New modules before the code that imports them
3. **Core before edge**: Happy path before error handling
4. **Source before tests**: Implementation before test writing
5. **Configuration alongside code**: Settings changes in the same task as the feature

### Dependency Mapping

For each task, explicitly state:
- **Depends on**: which tasks must be done first
- **Blocks**: which tasks cannot start until this is done
- **Independent of**: which tasks can run in parallel

---

## File Impact Analysis

For each task, list:

```markdown
#### Task N: [title]
- **Files to CREATE**:
  - `path/to/new_file.py` — purpose
- **Files to MODIFY**:
  - `path/to/existing.py` — what changes and why
- **Files to DELETE** (rare):
  - `path/to/obsolete.py` — why it's no longer needed
```

### How to Identify Impacted Files

1. **Grep for imports**: If creating a new module, search for who imports the old one
2. **Trace the call graph**: Start from the entry point, follow function calls
3. **Check configuration**: Settings, env files, dependency manifests
4. **Check tests**: Existing test files that reference changed modules
5. **Check documentation**: README, docs that reference changed features

---

## Risk Assessment

For each plan, include:

```markdown
### Risk Areas
| Risk | Likelihood | Impact | Mitigation |
|------|-----------|--------|------------|
| Breaking backward compat | Medium | High | Keep old interface as alias |
| Import errors after rename | High | Low | Grep for all usages before renaming |
| Test failures | Medium | Medium | Run tests after each task |
```

---

## Out-of-Scope Declaration

Explicitly list what the plan does NOT cover:
- Features mentioned in the PRD but deferred
- Improvements noticed during planning but unrelated
- Technical debt found but not part of this work

This prevents scope creep and keeps sub-agents focused.

---

## Enhancement Workflow

When adding features to an existing codebase (not greenfield), follow this adapted workflow:

### Classify the Work Type

| Type | Definition | Planning Approach |
|------|-----------|-------------------|
| **Greenfield** | No existing code for this feature | Full decomposition from scratch |
| **Enhancement** | Adding capabilities on top of existing code | Delta-only — plan only what's new or changed |
| **Bug fix** | Existing code has wrong behaviour | Minimal — identify root cause, plan fix + regression test |
| **Refactoring** | Change structure without changing behaviour | Map all touchpoints, plan renames/moves, verify with tests |

### Delta Planning Rules

For enhancements:

1. **Never re-implement existing working code.** If `adapters/base.py` exists and works, do not include a "Create adapters/base.py" task.
2. **Reference existing code as context, not as tasks.** Instead of planning a task, write: "Depends on existing `adapters/base.py` (already implemented — no changes needed)."
3. **Plan only the gap.** If a file needs 2 new methods added to an existing class, the task is "Add methods X and Y to `Class` in `file.py`" — not "Implement `file.py`."
4. **State the regression baseline.** At the plan's top, note: "N existing tests must continue to pass. Existing files X, Y, Z must not have breaking changes."
5. **Flag integration points.** When new code must interact with existing code, explicitly state which existing functions/classes it calls and what contract (params, return types) it depends on.

### Enhancement Plan Template Additions

Add these sections to the standard plan template when the work is an enhancement:

```markdown
### Regression Baseline
- **Existing test count**: N tests passing
- **Files that must NOT break**: [list of files with stable contracts]
- **Existing APIs/interfaces consumed by new code**: [list]

### Completed Work (NOT in scope)
| Requirement | Status | Evidence |
|-------------|--------|----------|
| DatabaseAdapter ABC | ✅ Done | `adapters/base.py` exists with 4 abstract methods |
| Factory function | ✅ Done | `adapters/factory.py` dispatches by DB_TYPE |
```

---

## Plan Template

```markdown
## Implementation Plan

### Summary
[1-2 sentences: what this plan achieves]

### Prerequisites
- [things that must be true before starting]

### Affected Areas
| File | Action | Description |
|------|--------|-------------|
| `path/file.py` | MODIFY | ... |
| `path/new.py` | CREATE | ... |

### Tasks (ordered by dependency)

#### Task 1: [title]
- **Type**: CREATE | MODIFY | REFACTOR | DELETE
- **Files**: [list]
- **Description**: [what to do]
- **Depends on**: none
- **Acceptance**: [how to verify]

#### Task 2: [title]
...

### Risk Areas
(see template above)

### Out of Scope
- ...
```

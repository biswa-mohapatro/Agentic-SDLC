---
description: 'Testing conventions enforcing TDD workflow, test structure, naming, isolation, and coverage standards. Distilled from testing-strategy skill and VS Code TDD guide for automatic application to test files.'
applyTo: '**/test_*.py, **/*.test.ts, **/*.test.js, **/*.test.tsx, **/*.test.jsx, **/*.spec.ts, **/*.spec.js, **/tests/**, **/__tests__/**'
---

# Testing Conventions

## TDD Workflow

1. **Red**: Write a failing test that encodes the expected behaviour before writing implementation.
2. **Green**: Write the minimal code to make the test pass — nothing extra.
3. **Refactor**: Clean up while all tests remain green, then run the full suite to catch regressions.
4. **Repeat**: One new test per cycle. Small iterations prevent compounding errors.

## Test Structure — AAA Pattern

Every test follows **Arrange → Act → Assert**:

```
# Arrange — set up inputs and dependencies
# Act    — call the unit under test exactly once
# Assert — verify a single behaviour
```

One assertion concept per test. Multiple `assert` statements are acceptable only when verifying different facets of the same behaviour.

## Naming Convention

```
test_<unit>_<scenario>_<expected>
```

- Describe **what** is tested, the **condition**, and the **expected outcome**.
- Use `_` separators, not camelCase.
- Good: `test_register_user_duplicate_email_raises_conflict`
- Bad: `test_1`, `test_something`, `testUser`

## Test Isolation

- Each test must run independently and in any order.
- No shared mutable state across tests. Use fresh fixtures per test.
- Mock external dependencies (APIs, databases, file systems, clocks) at the adapter boundary.
- Never mock the code under test or standard-library pure functions.

## What to Mock vs. What Not to Mock

| Mock | Don't Mock |
|------|-----------|
| External services, databases, APIs | The code under test |
| Time-dependent operations | Simple data transformations |
| Random / non-deterministic ops | Standard library pure functions |
| Network / file-system I/O | In-memory business logic |

## Edge Cases — Always Cover

| Category | Examples |
|----------|---------|
| Empty input | `""`, `[]`, `{}`, `None` |
| Boundary values | 0, 1, -1, max size, empty string |
| Error paths | Missing credentials, timeout, bad config |
| Type mismatches | Wrong type passed to a typed parameter |

## Coverage Targets

- **Unit tests**: 80 %+ line coverage on business logic.
- **Integration tests**: Cover module boundaries and API contracts.
- **E2E tests**: Critical user journeys only — keep the count small.

Pyramid ratio: **80 % unit / 15 % integration / 5 % E2E.**

## Framework Hygiene

- **Detect first**: Search for the existing framework (`pytest`, `jest`, `xunit`, `mocha`) before writing anything. Match it.
- **Match existing directory structure**: `tests/`, `__tests__/`, `spec/`. Don't introduce a new layout.
- Re-use existing fixtures and helpers (`conftest.py`, `test_helpers`, `factories`) before creating new ones.

## Running Tests

- Run targeted tests immediately after each change.
- Run the full suite before considering a task complete.
- Report: total count, pass / fail counts, failure details.

## Anti-Patterns

| Anti-Pattern | Fix |
|-------------|-----|
| Tests that pass when implementation is wrong | Verify the test fails first (Red phase) |
| Testing implementation details | Assert observable behaviour, not internal state |
| Shared mutable fixtures | Create fresh fixtures per test |
| Swallowed errors in test setup | Let setup failures propagate — don't catch them |
| Giant test methods | Split into focused tests with descriptive names |
| Over-mocking everything | Mock at the boundary only |

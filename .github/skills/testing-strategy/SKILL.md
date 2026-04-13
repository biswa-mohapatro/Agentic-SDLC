---
name: testing-strategy
description: "Comprehensive testing patterns for unit, integration, and async tests. Use when: writing unit tests, creating test fixtures, mocking external dependencies, testing async code, TDD workflow, validating test coverage. Loaded by Test Engineer agent."
---

# Testing Strategy — Skill

This skill defines the testing methodology, patterns, and templates for writing production-grade tests.

---

## Testing Pyramid

```
         /  E2E  \          ← Few: critical user journeys only
        /----------\
       / Integration \      ← Some: module boundaries, API contracts
      /----------------\
     /    Unit Tests     \  ← Many: every function, every edge case
    /____________________\
```

Focus: **80% unit, 15% integration, 5% E2E.** Unit tests are the primary output.

---

## Framework Detection

Before writing any tests, determine:
1. What test framework exists? Search for `pytest`, `jest`, `xunit`, `mocha` in config files
2. What test directory structure exists? Check `tests/`, `__tests__/`, `spec/`
3. Are there existing fixtures/helpers? Check `conftest.py`, `test_helpers`, `factories`
4. Is there async test support? Check for `pytest-asyncio`, `@jest/globals`

**Match the existing pattern exactly.** Don't introduce a new framework.

---

## Unit Test Template — Python (pytest)

```python
"""Tests for module_name."""
import pytest
from unittest.mock import AsyncMock, MagicMock, patch

# If the entire module is async
pytestmark = pytest.mark.asyncio


class TestClassName:
    """Tests for ClassName."""

    def test_method_happy_path(self):
        """Method returns expected result with valid input."""
        # Arrange
        instance = ClassName(dependency=MagicMock())
        
        # Act
        result = instance.method(valid_input)
        
        # Assert
        assert result == expected_output

    def test_method_empty_input(self):
        """Method handles empty input gracefully."""
        instance = ClassName(dependency=MagicMock())
        result = instance.method("")
        assert result == default_value

    def test_method_raises_on_invalid(self):
        """Method raises ValueError for invalid input."""
        instance = ClassName(dependency=MagicMock())
        with pytest.raises(ValueError, match="expected message"):
            instance.method(invalid_input)
```

---

## Async Test Template — Python

```python
import pytest
from unittest.mock import AsyncMock

pytestmark = pytest.mark.asyncio


async def test_async_operation_returns_result(mock_dependency):
    """Async operation completes and returns normalised result."""
    mock_dependency.execute_async = AsyncMock(
        return_value={"columns": ["id"], "rows": [(1,)]}
    )
    
    result = await service.run(adapter=mock_dependency)
    
    assert result["status"] == "ok"
    mock_dependency.execute_async.assert_called_once()
```

---

## Mocking Strategy

### What to Mock
- External services (databases, APIs, LLMs, file systems)
- Time-dependent operations (`datetime.now`, sleep)
- Random/non-deterministic operations

### What NOT to Mock
- The code under test
- Simple data transformations
- Standard library pure functions

### Mock Scope
```
┌─────────────────────────────┐
│ Business Logic (test this)  │ ← DO NOT mock
│    calls ↓                  │
│ Adapter Interface (ABC)     │ ← MOCK HERE (the boundary)
│    implemented by ↓         │
│ Concrete Adapter            │ ← Not involved in unit tests
│    calls ↓                  │
│ External Service            │ ← Not involved in unit tests
└─────────────────────────────┘
```

### Mock Fixtures — Python

```python
# conftest.py — shared across test modules

@pytest.fixture
def mock_adapter():
    """In-memory test double that implements the adapter interface."""
    adapter = MagicMock()
    adapter.execute_async = AsyncMock(
        return_value={"columns": ["id", "name"], "rows": [(1, "test")]}
    )
    adapter.test_connection = AsyncMock(return_value=True)
    return adapter

@pytest.fixture
def failing_adapter():
    """Adapter that simulates connection failure."""
    adapter = MagicMock()
    adapter.execute_async = AsyncMock(
        side_effect=RuntimeError("Connection refused")
    )
    return adapter
```

---

## Test Naming Convention

```
test_<unit>_<scenario>_<expected>

Examples:
test_pipeline_valid_question_returns_analysis
test_adapter_missing_credentials_raises_connection_error
test_factory_unknown_db_type_raises_value_error
test_metadata_cache_hit_skips_database_query
```

---

## Edge Cases to Always Test

| Category | Examples |
|----------|---------|
| Empty input | `""`, `[]`, `{}`, `None` |
| Boundary values | 0, 1, -1, MAX_INT, empty string |
| Error recovery | Adapter throws, LLM returns empty, timeout |
| Concurrency | Async operations completing out of order |
| Type safety | Wrong type passed to typed parameter |
| Configuration | Missing env var, invalid config value |

---

## Running Tests

After writing tests, always run them:

```bash
# Python
pytest tests/unit/ --tb=short -q

# Node.js
npm test

# .NET
dotnet test --verbosity normal
```

Report:
- Total test count
- Pass count
- Fail count (with details for each failure)
- Warnings (if any)

---

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| `AsyncMock` not applied to async method | Use `new_callable=AsyncMock` in `@patch()` |
| Tests order-dependent | Each test must set up its own state |
| Mocking too deep (mocking internals) | Mock at the adapter boundary only |
| Test names like `test_1`, `test_a` | Use descriptive: `test_execute_empty_query_returns_empty_rows` |
| No assertion (test always passes) | Every test must have at least one `assert` |
| `import` caches settings after monkeypatch | Use `importlib.reload()` for settings module |

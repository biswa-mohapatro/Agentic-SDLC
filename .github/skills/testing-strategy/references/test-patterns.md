# Test Patterns Reference

Common test patterns with code examples. Use as a reference when writing tests.

---

## 1. Arrange-Act-Assert (AAA)

The standard unit test structure. Every test should have exactly these three sections.

```python
def test_calculate_discount_applies_percentage():
    # Arrange
    price = 100.0
    discount_pct = 15

    # Act
    result = calculate_discount(price, discount_pct)

    # Assert
    assert result == 85.0
```

---

## 2. Given-When-Then (BDD)

Equivalent to AAA but using BDD terminology. Useful for behavior-driven tests.

```python
def test_user_login_with_valid_credentials_returns_token():
    # Given a registered user
    user = create_test_user(email="test@example.com", password="secure123")

    # When they login with correct credentials
    response = login(email="test@example.com", password="secure123")

    # Then they receive a valid token
    assert response.status_code == 200
    assert "token" in response.json()
```

---

## 3. Test Doubles

| Double | Purpose | When to Use |
|--------|---------|-------------|
| **Stub** | Returns canned responses | Replace a dependency with predictable output |
| **Mock** | Verifies interactions | Assert that a method was called with expected args |
| **Fake** | Working implementation (simplified) | In-memory database, fake HTTP server |
| **Spy** | Records calls for later assertion | When you need both real behavior and call tracking |

```python
# Stub — returns a fixed value
def test_get_user_with_stubbed_db(mocker):
    mocker.patch("app.db.find_user", return_value={"id": 1, "name": "Alice"})
    user = get_user(1)
    assert user["name"] == "Alice"

# Mock — verifies the call happened
def test_send_email_on_signup(mocker):
    mock_send = mocker.patch("app.email.send_welcome_email")
    signup(email="new@example.com")
    mock_send.assert_called_once_with("new@example.com")

# Fake — in-memory implementation
class FakeUserRepository:
    def __init__(self):
        self._users = {}

    def save(self, user):
        self._users[user.id] = user

    def find(self, user_id):
        return self._users.get(user_id)
```

---

## 4. Parametrized Tests

Run the same test logic across multiple inputs.

```python
import pytest

@pytest.mark.parametrize("input_val, expected", [
    ("hello", "HELLO"),
    ("", ""),
    ("Hello World", "HELLO WORLD"),
    ("123abc", "123ABC"),
])
def test_to_uppercase(input_val, expected):
    assert to_uppercase(input_val) == expected
```

```typescript
// Jest equivalent
describe.each([
  ["hello", "HELLO"],
  ["", ""],
  ["Hello World", "HELLO WORLD"],
])("toUpperCase(%s)", (input, expected) => {
  it(`returns ${expected}`, () => {
    expect(toUpperCase(input)).toBe(expected);
  });
});
```

---

## 5. Exception / Error Testing

```python
import pytest

def test_divide_by_zero_raises_error():
    with pytest.raises(ZeroDivisionError):
        divide(10, 0)

def test_invalid_email_raises_validation_error():
    with pytest.raises(ValidationError, match="Invalid email"):
        validate_email("not-an-email")
```

```typescript
// Jest
it("throws on invalid input", () => {
  expect(() => parseConfig("")).toThrow("Config cannot be empty");
});

// Async
it("rejects on network failure", async () => {
  await expect(fetchData("bad-url")).rejects.toThrow("Network error");
});
```

---

## 6. Async Testing

```python
import pytest

@pytest.mark.asyncio
async def test_fetch_user_returns_data():
    user = await fetch_user(user_id=1)
    assert user["name"] == "Alice"

@pytest.mark.asyncio
async def test_concurrent_writes_are_safe():
    tasks = [write_record(i) for i in range(10)]
    results = await asyncio.gather(*tasks)
    assert all(r.success for r in results)
```

---

## 7. Fixture Patterns

```python
import pytest

@pytest.fixture
def db_session():
    """Create a test database session and roll back after test."""
    session = create_test_session()
    yield session
    session.rollback()
    session.close()

@pytest.fixture
def sample_user(db_session):
    """Create a sample user in the test database."""
    user = User(name="Test User", email="test@example.com")
    db_session.add(user)
    db_session.flush()
    return user

def test_user_can_update_name(db_session, sample_user):
    sample_user.name = "Updated"
    db_session.flush()
    refreshed = db_session.query(User).get(sample_user.id)
    assert refreshed.name == "Updated"
```

---

## 8. Edge Case Catalog

Always test these scenarios:

| Category | Cases |
|----------|-------|
| **Empty** | `""`, `[]`, `{}`, `None`, `0` |
| **Boundary** | Min value, max value, min ± 1, max ± 1 |
| **Type** | Wrong type, `None`/`null`/`undefined` |
| **Size** | 0 items, 1 item, very large input |
| **Encoding** | Unicode, emoji, special characters, RTL text |
| **Concurrency** | Race conditions, duplicate submissions |
| **Time** | Timezone boundaries, DST transitions, leap years |
| **Network** | Timeout, connection refused, partial response |
| **Auth** | No token, expired token, wrong role, valid token |

---

## 9. Test Naming Convention

```
test_<unit>_<scenario>_<expected>
```

Examples:
- `test_parse_config_missing_key_raises_error`
- `test_calculate_tax_zero_income_returns_zero`
- `test_login_expired_token_returns_401`
- `test_upload_file_exceeds_limit_rejects`

---

## 10. Testing Pyramid

```
         /  E2E  \          5% — Critical user journeys only
        /----------\
       / Integration \      15% — API contracts, DB queries
      /----------------\
     /    Unit Tests     \  80% — Pure logic, fast, isolated
    /____________________\
```

- **Unit**: No I/O, no network, no database. Mock external dependencies.
- **Integration**: Real database/API calls. Use test containers or fixtures.
- **E2E**: Full system with browser/HTTP client. Only for critical paths.

---

## 11. Data Quality Assertions

```python
import pandas as pd

def test_output_has_no_null_primary_keys(result_df):
    assert result_df["id"].notna().all(), "Null values in primary key"

def test_output_primary_key_is_unique(result_df):
    assert result_df["id"].is_unique, "Duplicate primary keys"

def test_amounts_within_valid_range(result_df):
    assert result_df["amount"].between(0, 1_000_000).all()

def test_schema_matches_contract(result_df):
    expected = {"id": "int64", "name": "object", "amount": "float64"}
    for col, dtype in expected.items():
        assert col in result_df.columns, f"Missing: {col}"
        assert str(result_df[col].dtype) == dtype, f"{col} dtype mismatch"
```

---

## 12. LLM / AI Response Testing

```python
from unittest.mock import MagicMock, AsyncMock

@pytest.fixture
def mock_llm():
    llm = MagicMock()
    llm.complete.return_value = '{"summary": "test", "confidence": 0.9}'
    return llm

def test_structured_response_has_required_fields(mock_llm):
    result = summarize(document="doc", llm=mock_llm)
    assert "summary" in result
    assert 0.0 <= result["confidence"] <= 1.0

def test_malformed_llm_response_raises(mock_llm):
    mock_llm.complete.return_value = "not json"
    with pytest.raises(LLMResponseError):
        summarize(document="doc", llm=mock_llm)

def test_retry_on_rate_limit(mock_llm):
    mock_llm.complete.side_effect = [RateLimitError("429"), '{"answer": "ok"}']
    result = call_with_retry(mock_llm, prompt="test", max_retries=2)
    assert result == {"answer": "ok"}
    assert mock_llm.complete.call_count == 2

def test_prompt_within_token_budget():
    prompt = build_prompt(context="x" * 10000, query="test")
    assert count_tokens(prompt) <= 8000
```

---
name: data-testing
description: "Testing patterns for data quality, schema validation, pipeline correctness, and transformation verification. Use when: testing ETL pipelines, data transformations, schema contracts, DataFrame operations, data integrity checks. Loaded by Test Engineer agent."
---

# Data Testing — Skill

Testing patterns for applications that process, transform, or store data.

---

## Data Quality Assertions

Every data-producing function should be tested for these properties:

| Property | What to Assert | Example |
|----------|---------------|---------|
| **Completeness** | Required columns are non-null above a threshold | `assert df["email"].notna().mean() >= 0.99` |
| **Uniqueness** | Primary key / business key has no duplicates | `assert df["id"].is_unique` |
| **Value range** | Numeric columns stay within expected bounds | `assert df["age"].between(0, 150).all()` |
| **Referential integrity** | Foreign keys exist in the parent table | `assert child_df["parent_id"].isin(parent_df["id"]).all()` |
| **Format conformance** | Strings match expected patterns | `assert df["email"].str.match(r".+@.+\..+").all()` |
| **Freshness** | Timestamps are within an expected window | `assert df["updated_at"].max() >= cutoff_date` |

---

## Schema Contract Testing

Test schemas explicitly — don't rely on runtime discovery.

```python
def test_output_schema_matches_contract():
    """Transformation output has the expected columns and types."""
    result = transform(input_df)

    expected_cols = {"id": "int64", "name": "object", "score": "float64"}
    for col, dtype in expected_cols.items():
        assert col in result.columns, f"Missing column: {col}"
        assert str(result[col].dtype) == dtype, f"{col} dtype mismatch"
```

### Schema Evolution Rules

- **Additive changes** (new columns) — existing tests must still pass.
- **Breaking changes** (renamed/removed columns, type changes) — update tests first (Red phase), then migrate.
- **Test both directions** when writing migrations: old → new and new → old (if rollback is supported).

---

## DataFrame Fixture Patterns

Keep fixtures small, deterministic, and representative.

```python
import pandas as pd
import pytest

@pytest.fixture
def sample_orders():
    """Minimal DataFrame covering happy path + edge cases."""
    return pd.DataFrame({
        "order_id": [1, 2, 3],
        "amount": [100.0, 0.0, -5.0],       # normal, zero, negative
        "status": ["shipped", "pending", None],  # valid, valid, null
        "created_at": pd.to_datetime(["2025-01-01", "2025-06-15", "2025-12-31"]),
    })

@pytest.fixture
def empty_orders():
    """Empty DataFrame with correct schema."""
    return pd.DataFrame(columns=["order_id", "amount", "status", "created_at"])
```

**Rules**:
- Always include at least one null / missing value
- Always include a zero and a boundary value
- Always include an empty-but-schema-correct fixture
- Keep row count under 10 for unit tests

---

## Transformation Testing

Test transformations as pure functions: input DataFrame → output DataFrame.

```python
def test_calculate_totals_sums_line_items(sample_orders):
    result = calculate_totals(sample_orders)

    assert "total" in result.columns
    assert result.loc[result["order_id"] == 1, "total"].iloc[0] == 100.0

def test_calculate_totals_empty_input(empty_orders):
    result = calculate_totals(empty_orders)

    assert len(result) == 0
    assert "total" in result.columns  # schema preserved even when empty
```

---

## Snapshot / Golden-File Testing

For complex transformations, compare output against a saved golden file.

```python
def test_pipeline_output_matches_golden(tmp_path, sample_input):
    result = run_pipeline(sample_input)
    golden = pd.read_parquet("tests/golden/expected_output.parquet")

    pd.testing.assert_frame_equal(result, golden, check_dtype=True)
```

**When to use**: Multi-step pipelines where hand-writing assertions per column is brittle.
**When to avoid**: Simple single-column transforms — use direct assertions instead.

---

## Pipeline Testing Patterns

### Idempotency

```python
def test_pipeline_is_idempotent(sample_input):
    first_run = run_pipeline(sample_input)
    second_run = run_pipeline(first_run)
    pd.testing.assert_frame_equal(first_run, second_run)
```

### Ordering Invariance

```python
def test_pipeline_ignores_input_order(sample_input):
    shuffled = sample_input.sample(frac=1, random_state=42)
    result_original = run_pipeline(sample_input).sort_values("id").reset_index(drop=True)
    result_shuffled = run_pipeline(shuffled).sort_values("id").reset_index(drop=True)
    pd.testing.assert_frame_equal(result_original, result_shuffled)
```

### Row Count Invariants

```python
def test_filter_reduces_rows(sample_input):
    result = filter_active(sample_input)
    assert len(result) <= len(sample_input)
    assert len(result) > 0  # at least one active row in fixture
```

---

## Edge Cases — Data Specific

| Category | Test Cases |
|----------|-----------|
| **Nulls** | All-null column, single null in PK, null in group-by key |
| **Duplicates** | Exact duplicates, duplicates on subset of columns |
| **Types** | Mixed types in a column, string numbers (`"123"`), date strings |
| **Encoding** | Unicode, emoji, null bytes, leading/trailing whitespace |
| **Scale** | Empty DataFrame, single row, boundary at partition size |
| **Dates** | Timezone-naive vs aware, DST boundaries, leap day, epoch zero |

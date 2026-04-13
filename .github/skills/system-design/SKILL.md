---
name: system-design
description: "Patterns and methodology for software architecture decisions. Use when: designing new modules, defining abstract interfaces, selecting design patterns, planning data flow, creating architecture decision records. Loaded by Architect agent."
---

# System Design — Skill

This skill codifies the design methodology and pattern library for architectural work.

---

## Design Process

### 1. Context Gathering

Before designing anything:
- Read `copilot-instructions.md` for project conventions
- Read existing abstractions (ABCs, Protocols, base classes)
- Read the module that will be most affected
- Count the consumers of the interface you're designing

### 2. Design Principles

Apply in order of priority:
1. **YAGNI** — Don't add it until you need it
2. **Single Responsibility** — Each class/module does one thing
3. **Dependency Inversion** — Depend on abstractions, not concretions
4. **Open/Closed** — Open for extension, closed for modification
5. **Liskov Substitution** — Subtypes must be substitutable for their base types

### 3. Choose the Simplest Pattern That Works

Don't reach for a complex pattern when a simple one will do.

---

## Pattern Library

### Abstract Base Class (ABC) — Python

Use when: you need to enforce a contract across multiple concrete implementations.

```python
import abc
from typing import Any, Dict, List

class ServiceAdapter(abc.ABC):
    """Contract that all service adapters must implement."""

    @abc.abstractmethod
    async def execute(self, request: Dict[str, Any]) -> Dict[str, Any]:
        """Execute a request and return normalised results."""

    @abc.abstractmethod
    async def health_check(self) -> bool:
        """Return True if the service is reachable."""
```

Rules:
- ABC goes in `base.py` inside the adapter package
- Concrete classes go in separate files: `concrete_a.py`, `concrete_b.py`
- Business logic imports only the ABC, never the concrete classes

### Factory Pattern

Use when: concrete class selection depends on configuration (env var, settings).

```python
def create_service() -> ServiceAdapter:
    service_type = settings.service_type.lower()
    match service_type:
        case "type_a":
            from .concrete_a import ConcreteA
            return ConcreteA()
        case "type_b":
            from .concrete_b import ConcreteB
            return ConcreteB()
        case _:
            raise ValueError(f"Unknown service type: {service_type}")
```

Rules:
- Imports inside match branches — only the selected backend needs to be installed
- Factory returns the ABC type, not the concrete type
- Only entry points call the factory; business logic receives the instance via DI

### Dependency Injection (DI)

Use when: passing abstract instances to business logic.

```python
class Pipeline:
    def __init__(self, db: DatabaseAdapter, cache: CacheAdapter):
        self._db = db
        self._cache = cache
```

Rules:
- Constructor parameters use the ABC type
- Entry points (API server, CLI, Streamlit app) create instances and inject
- Business logic never calls `create_service()` — it receives the service

### Strategy Pattern

Use when: you need interchangeable algorithms for the same operation.

```python
class QueryGenerator(abc.ABC):
    @abc.abstractmethod
    async def generate(self, question: str, context: dict) -> str: ...

class LLMQueryGenerator(QueryGenerator): ...
class TemplateQueryGenerator(QueryGenerator): ...
```

### Observer / Event Pattern

Use when: you need to notify multiple listeners of state changes (e.g., progress tracking).

```python
async def on_progress(event: dict) -> None: ...

await pipeline.run(question, on_progress=on_progress)
```

---

## Interface Design Checklist

For every new interface, verify:

- [ ] Every method has a clear docstring with Args, Returns, Raises
- [ ] Return types are consistent (always dict, never dict|None)
- [ ] The interface is **mockable** — can be replaced with AsyncMock in tests
- [ ] No method requires knowledge of implementation details to call
- [ ] String parameters that represent structured data (e.g., table names) have documented format requirements

---

## Architecture Decision Record (ADR) Template

```markdown
### ADR-N: [title]

**Status**: Proposed | Accepted | Deprecated
**Context**: Why this decision is needed
**Decision**: What we chose
**Alternatives Considered**:
  - Option A: pros / cons
  - Option B: pros / cons
**Consequences**:
  - Positive: ...
  - Negative: ...
  - Neutral: ...
```

---

## Data Flow Documentation

For complex operations, document the flow:

```
User Input
  → API Handler (validate, authenticate)
    → Pipeline (orchestrate)
      → Adapter.execute(sql) → Database
      → Analyzer.analyze(results) → LLM
    ← Return analysis + data
  ← WebSocket response
```

---

## Common Mistakes

| Mistake | Fix |
|---------|-----|
| Designing for hypothetical future features | Design for current requirements only |
| Multiple inheritance hierarchies | Use composition + ABC interfaces |
| Leaking adapter-specific types into business logic | Wrap in normalised return types |
| Config validation in business logic | Validate in adapter __init__ or settings validator |
| Circular imports | Reorganise into separate interface/implementation files |

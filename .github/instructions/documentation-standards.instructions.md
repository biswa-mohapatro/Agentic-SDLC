---
description: 'Documentation quality standards enforcing structure, writing style, formatting, and completeness checks. Distilled from the documentation-standards skill for automatic application to Markdown files.'
applyTo: '**/*.md'
---

# Documentation Standards

## Writing Style

- **Present tense, active voice**: "The adapter returns…" not "will return" or "is returned by".
- **Second person for instructions**: "Set your API key" not "Users should set their API key".
- **Technical but accessible**: Assume the reader knows the tech stack, not the project internals.
- **Concise**: One idea per sentence. Remove filler words.

## Formatting Rules

- Inline code for symbols, variables, commands, file paths: `DB_TYPE`, `execute_async()`, `config/settings.py`.
- Code blocks with a language tag (`bash`, `python`, `yaml`) — never bare fenced blocks.
- Tables over prose for configuration, enums, mappings, and comparisons.
- Headings follow a strict hierarchy: `#` → `##` → `###`. Never skip levels.

## README Structure

Every project README follows this order:

1. **Title + one-line description**
2. **Features** — bulleted, each with a brief description
3. **Quick Start** — Prerequisites, Installation, Configuration, Running
4. **Architecture** — high-level diagram or description
5. **Development** — running tests, project structure
6. **License**

The Quick Start section must work end-to-end for a new developer with copy-pasteable commands.

## Configuration Documentation

- Every environment variable used by the project must appear in `.env.example` with a placeholder value and a comment.
- Configuration tables include: Variable, Required (Yes/No), Default, Description.
- Never use real credentials, tokens, or internal URLs in examples.

## Migration Guides

When documenting breaking changes:

1. **What Changed** — brief summary
2. **Who Is Affected** — affected and unaffected users
3. **Step-by-Step Migration** — before/after code snippets
4. **Troubleshooting** — symptom / cause / fix table

## Inline Documentation (Docstrings)

- Add docstrings only to **new public APIs** created during the current work cycle.
- Don't retrofit docstrings onto existing unchanged code.
- Python: Google style. TypeScript/JS: JSDoc `@param` / `@returns` / `@throws`.
- One-liner for trivial functions; full docstring (summary, args, returns, raises) for complex ones.

## Diagrams

- Use ASCII art or Mermaid for architecture and flow diagrams within Markdown.
- Keep diagrams small — if a diagram exceeds 30 lines, split it into sub-diagrams.
- Label every arrow or connection.

## Quality Checklist

Before finalising documentation:

- [ ] Code examples reference actual files and functions in the project
- [ ] All commands are copy-pasteable with no placeholder paths
- [ ] No real credentials, tokens, or internal URLs
- [ ] Links use relative paths within the project
- [ ] Every env variable in `.env.example` has a comment
- [ ] Quick Start works end-to-end from a fresh clone
- [ ] Heading hierarchy is correct (no skipped levels)

## Anti-Patterns

| Anti-Pattern | Fix |
|-------------|-----|
| Prose where a table would be clearer | Convert to a table |
| Outdated screenshots or diagrams | Remove or regenerate from current state |
| Documenting implementation internals | Document behaviour and interfaces only |
| Bare code blocks without language tag | Add the correct language identifier |
| Copy-pasted external docs | Summarise and link to the source |

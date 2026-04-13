---
description: 'Standards for creating custom agent, skill, prompt, and instruction files. Enforces frontmatter syntax, tool aliases, naming conventions, and handoff patterns. Based on awesome-copilot best practices.'
applyTo: '**/*.agent.md, **/*.prompt.md, **/SKILL.md, **/*.instructions.md'
---

# Agent Authoring Standards

## Frontmatter Requirements

### Agent Files (`*.agent.md`)
```yaml
---
description: "Brief purpose and capabilities (50-150 chars). Use 'Use when:' pattern."
name: "Agent Display Name"
tools: [read, search, edit]       # Least-privilege — only what's needed
model: "Claude Sonnet 4.6"       # Always specify
user-invocable: false             # Set false for sub-agents
---
```

**Required**: `description` (single-quoted if contains colons)
**Strongly recommended**: `name`, `model`, `tools`
**Optional**: `user-invocable`, `handoffs`, `agents`

### Prompt Files (`*.prompt.md`)
```yaml
---
description: "What this prompt does"
name: "Prompt Display Name"
agent: "Target Agent Name"        # Routes to this agent
argument-hint: "What to type..."  # Placeholder text
tools: [read, search, edit]
---
```

### Skill Files (`SKILL.md`)
```yaml
---
name: skill-name                 # Lowercase with hyphens, matches folder name, max 64 chars
description: "Purpose and trigger phrases (10-1024 chars)"
---
```

### Instruction Files (`*.instructions.md`)
```yaml
---
description: "What standards this enforces"
applyTo: '**/*.py, **/*.ts'      # Glob patterns — be specific, avoid '**' alone
---
```

## Tool Aliases

| Alias | What It Does |
|-------|-------------|
| `read` | Read file contents |
| `edit` | Edit and modify files |
| `search` | Search for files or text |
| `execute` | Run shell commands |
| `agent` | Invoke sub-agents |
| `web` | Fetch web content |
| `todo` | Task list management |
| `atlassian/*` | Jira and Confluence operations |

## Naming Conventions

- **File names**: lowercase with hyphens (`my-agent.agent.md`)
- **Agent names**: Title case, descriptive (`"Code Review Specialist"`)
- **Skill folder names**: lowercase with hyphens, matching `name` field
- **Allowed chars**: `.`, `-`, `_`, `a-z`, `A-Z`, `0-9`

## Handoff Patterns

```yaml
handoffs:
  - label: "Start Implementation"    # Action-oriented label
    agent: "Developer"               # Target agent name
    prompt: "Implement the plan..."  # Context-aware prompt
    send: false                      # User reviews before sending
```

- Limit to 2-3 handoffs per agent
- Use action-oriented labels: "Start Implementation", not "Next"
- Reference completed work in the prompt text

## Common Pitfalls

- **Description is the discovery surface**: If trigger phrases aren't in `description`, the agent won't be found
- **YAML silent failures**: Unescaped colons, tabs instead of spaces, mismatched quotes
- **`applyTo: '**'` burns context**: Use specific globs unless the instruction truly applies to all files
- **Tools ceiling**: Sub-agents cannot access tools that aren't in the parent orchestrator's `tools` list

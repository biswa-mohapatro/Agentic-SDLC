# Agentic-SDLC

## Overview

This repository is a **generic Agentic SDLC Framework** for GitHub Copilot. It automates the software development lifecycle from PRD creation through deployment-ready code, using role-based AI agents that coordinate via an orchestrator pattern.

## Repository Structure

```
.
├── agents/                     # SDLC role-based agents
│   ├── project-lead.agent.md   # Orchestrator — coordinates all phases
│   ├── prd-generator.agent.md  # Creates PRDs via guided interview
│   ├── planner.agent.md        # Breaks PRDs into implementation plans
│   ├── architect.agent.md      # Designs system architecture
│   ├── developer.agent.md      # Implements code
│   ├── test-engineer.agent.md  # Writes and runs tests
│   ├── reviewer.agent.md       # Code review and security audit
│   └── docs-engineer.agent.md  # Documentation
├── prompts/                    # Entry points for users
│   ├── prd-to-mvp.prompt.md    # Full SDLC cycle from PRD
│   ├── create-prd.prompt.md    # Guided PRD creation
│   ├── bug-fix.prompt.md       # Streamlined bug-fix cycle
│   ├── feature-add.prompt.md   # Feature addition cycle
│   ├── code-review.prompt.md   # Direct code review
│   └── refactor.prompt.md      # Behavior-preserving refactoring
├── skills/                     # Reusable engineering knowledge
│   ├── code-quality/           # Naming, functions, error handling
│   ├── documentation-standards/# Templates and writing style
│   ├── project-planning/       # Decomposition and dependency mapping
│   ├── security-best-practices/# OWASP Top 10, secrets, input validation
│   │   └── references/owasp-checklist.md
│   ├── system-design/          # Architecture patterns and ADRs
│   └── testing-strategy/       # Test design, mocking, coverage
│       └── references/test-patterns.md
├── instructions/               # Auto-applied coding standards
│   ├── code-standards.instructions.md
│   ├── security-and-owasp.instructions.md
│   ├── agent-authoring.instructions.md
│   ├── testing-conventions.instructions.md
│   ├── context-engineering.instructions.md
│   └── documentation-standards.instructions.md
├── .github/
│   └── hooks/                  # Lifecycle hooks (PreToolUse, SessionStart, Stop)
│       ├── tool-guardian.json   # Blocks destructive terminal commands
│       ├── session-logger.json  # Audit trail for session start/stop
│       └── scripts/
│           ├── tool-guardian.py
│           └── session-logger.py
├── .vscode/
│   └── mcp.json                # Atlassian MCP server configuration
├── plugin.json                 # Plugin metadata for distribution
├── copilot-instructions.md     # Project context + MCP toggles (template)
└── AGENTS.md                   # This file
```

## How It Works

### Auto-Discovery

VS Code discovers every piece of this framework from the `.github/` directory structure — no manual registration needed:

| File Type | Pattern | Discovery Mechanism |
|-----------|---------|-------------------|
| **Agents** | `agents/*.agent.md` | Appear in the Copilot Chat agent picker |
| **Prompts** | `prompts/*.prompt.md` | Appear as `/slash-commands` in chat |
| **Skills** | `skills/*/SKILL.md` | Loaded on-demand when an agent's task matches the skill description |
| **Instructions** | `instructions/*.instructions.md` | Auto-injected when a file matching the `applyTo` glob is in scope |
| **Hooks** | `hooks/*.json` | Run at lifecycle events (before tool use, session start/stop) |

### What Fires When

```
You type in Copilot Chat
        │
        ├─ Always injected ──────────► copilot-instructions.md (project-wide context)
        │
        ├─ File is open/mentioned ───► instructions/*.instructions.md
        │                               (only those whose applyTo glob matches)
        │
        ├─ You pick an agent ────────► agents/*.agent.md
        │   or use a /prompt              │
        │                                 ├─ Agent loads skills on demand
        │                                 │   (when the task matches a skill description)
        │                                 │
        │                                 └─ Agent hands off to next agent
        │                                     (via handoffs: in frontmatter)
        │
        └─ Agent calls a tool ───────► hooks/*.json
                                        (PreToolUse → tool-guardian blocks danger)
```

### Walk-Through: `/PRD to MVP`

1. **`copilot-instructions.md`** is injected (always-on project context, MCP toggles)
2. **`prd-to-mvp.prompt.md`** fires — its `agent:` field routes to **Project Lead**
3. **`project-lead.agent.md`** takes over as orchestrator and delegates phase-by-phase:
   - **Planner** loads the `project-planning` skill for decomposition knowledge
   - **Architect** loads the `system-design` skill for patterns and ADRs
   - **Developer** loads `code-quality` + `security-best-practices` skills; editing a `.py` file auto-injects `code-standards` + `security-and-owasp` instructions
   - **Test Engineer** loads the `testing-strategy` skill; editing test files auto-injects `testing-conventions` instructions
   - **Reviewer** loads `code-quality` + `security-best-practices` skills
   - **Docs Engineer** loads the `documentation-standards` skill; editing `.md` files auto-injects `documentation-standards` instructions
4. Whenever any agent runs a terminal command, the **`tool-guardian`** hook intercepts and blocks destructive operations

### Three Layers of Context

```
┌─────────────────────────────────────────────────┐
│              Always-On Layer                     │
│  copilot-instructions.md (project context)       │
│  + instructions whose applyTo matches open files │
└──────────────────────┬──────────────────────────┘
                       │ injected into every interaction
                       ▼
┌─────────────────────────────────────────────────┐
│              Workflow Layer                       │
│  /prompt → agent → agent → agent (handoff chain) │
│  Each agent loads relevant skills on demand      │
└──────────────────────┬──────────────────────────┘
                       │ agents call tools
                       ▼
┌─────────────────────────────────────────────────┐
│              Safety Layer                        │
│  hooks intercept tool calls                      │
│  tool-guardian blocks destructive commands        │
│  session-logger records audit trail              │
└─────────────────────────────────────────────────┘
```

**Key insight**: Instructions and `copilot-instructions.md` are *invisible guardrails* — they shape every response without being explicitly invoked. Skills are *pulled* by agents. Prompts and agents are *pushed* by the user. Hooks are *safety interceptors* that wrap tool execution.

## SDLC Pipeline

```
PRD Generator → Project Lead (orchestrator)
                    │
                    ├── Phase 0: Discovery & Scoping (+ Jira read, Backlog → In Progress)
                    ├── Phase 1: Planning         → Planner
                    ├── Phase 2: Architecture      → Architect
                    ├── Phase 3: Implementation    → Developer (→ Jira: Test)
                    ├── Phase 4: Testing           → Test Engineer ↔ Developer (iteration loop)
                    ├── Phase 5: Review & Debug    → Reviewer ↔ Developer (iteration loop)
                    ├── Phase 6: Documentation     → Docs Engineer (+ Confluence, → Jira: Acceptance)
                    └── Phase 7: Close Out         → Acceptance gate + Jira: Done
```

### Handoff Chain (Manual Mode)

Each agent has `handoffs` enabling guided phase-by-phase transitions:

```
Planner → Architect → Developer ⇄ Test Engineer → Reviewer → Docs Engineer → Project Lead
                          ↑            │                │
                          └────────────┘                │
                          └─────────────────────────────┘
                          (backward handoffs for iteration)
```

Forward handoffs advance the pipeline. Backward handoffs (`Test Engineer → Developer`, `Reviewer → Developer`) handle iteration when issues are found that the downstream agent can't fix alone.

### Iteration Loops

The real SDLC isn't linear. These feedback loops are built into the agents:

| Loop | Trigger | Max Iterations | Escalation |
|------|---------|---------------|------------|
| Developer ↔ Test Engineer | Tests reveal source code bugs that Test Engineer can't fix | 2 | Project Lead asks user |
| Developer ↔ Reviewer | Review finds design-level issues requiring rework | 1 | Project Lead asks user |

In **orchestrated mode** (Project Lead driving), the Project Lead manages the iteration count. In **manual mode** (handoff buttons), the user decides when to stop iterating.

## Agent Roles

| Agent | Tools | MCP | Role |
|-------|-------|-----|------|
| **Project Lead** | read, search, agent, todo, web, atlassian/* | Yes | Orchestrates SDLC phases, delegates to sub-agents |
| **PRD Generator** | read, search, edit, web, atlassian/* | Yes | Creates PRDs via guided interview, reads Jira tickets |
| **Planner** | read, search, web, todo, atlassian/* | Yes | Breaks requirements into ordered task lists |
| **Architect** | read, search, web | No | Designs interfaces, patterns, data flow |
| **Developer** | read, search, edit, execute, atlassian/* | Yes | Implements code, transitions Jira tickets |
| **Test Engineer** | read, search, edit, execute | No | Writes and runs automated tests |
| **Reviewer** | read, search, edit, execute | No | Code review, security audit, bug fixes |
| **Docs Engineer** | read, search, edit, atlassian/* | Yes | Documentation, Confluence publishing |

## Skills

Skills are **on-demand engineering knowledge** loaded by agents when relevant. They are NOT auto-applied — agents explicitly load them.

| Skill | Used By | Purpose |
|-------|---------|---------|
| `code-quality` | Developer, Reviewer | Naming, function design, error handling, anti-patterns |
| `security-best-practices` | Developer, Reviewer | OWASP Top 10, secrets, input validation |
| `testing-strategy` | Test Engineer | Test design, mocking, coverage, AAA pattern |
| `project-planning` | Planner | INVEST criteria, decomposition, dependency mapping |
| `system-design` | Architect | Architecture patterns, ADRs, interface design |
| `documentation-standards` | Docs Engineer | README templates, writing style, docstring formats |

## Instructions (Auto-Applied)

Instructions automatically apply to matching files — no manual loading needed.

| Instruction | Applies To | Purpose |
|-------------|-----------|---------|
| `code-standards` | `*.py, *.ts, *.js, *.jsx, *.tsx` | Naming, functions, error handling, imports |
| `security-and-owasp` | All files | OWASP Top 10, credential safety, input validation |
| `agent-authoring` | `*.agent.md, *.prompt.md, SKILL.md, *.instructions.md` | Frontmatter syntax, tool aliases, handoff patterns |
| `testing-conventions` | `test_*.py, *.test.ts, *.test.js, tests/**, __tests__/**` | TDD workflow, AAA pattern, naming, isolation, coverage |
| `context-engineering` | `copilot-instructions.md, *.agent.md, *.prompt.md, SKILL.md` | Context layering, progressive disclosure, freshness, anti-patterns |
| `documentation-standards` | `*.md` | Writing style, formatting, README structure, quality checklist |

## MCP Integration

### Jira Workflow

The framework follows this Jira ticket lifecycle:

```
Backlog → TODO → In Progress → Test → Acceptance → Done
```

| Jira Status | Triggered By | SDLC Phase |
|-------------|-------------|------------|
| **Backlog** | Ticket created | — |
| **TODO** | User decides to work on it | — |
| **In Progress** | Project Lead (Phase 0) | Discovery & Scoping |
| **Test** | Project Lead (after Phase 3) | Implementation complete, testing begins |
| **Acceptance** | Project Lead (after Phase 5) | Review passed, Project Lead verifies all gates |
| **Done** | Project Lead (Phase 7) | All phases complete, acceptance gate passed |

Agents also post Jira comments at key moments (if `Post progress comments` is enabled):
- **Developer**: Implementation summary after Phase 3
- **Test Engineer**: Test results after Phase 4
- **Project Lead**: Final summary at Phase 7

### Setup

The Atlassian MCP server (`.vscode/mcp.json`) provides Jira and Confluence access. Configure these environment variables on your machine:

```bash
export JIRA_URL="https://your-domain.atlassian.net"
export JIRA_USERNAME="your-email@company.com"
export JIRA_API_TOKEN="your-jira-api-token"
export CONFLUENCE_URL="https://your-domain.atlassian.net/wiki"
export CONFLUENCE_USERNAME="your-email@company.com"
export CONFLUENCE_API_TOKEN="your-confluence-api-token"
```

### Per-Project Configuration

Toggle MCP features in each project's `copilot-instructions.md`:

```markdown
## MCP Integration Preferences
- Jira Integration: enabled
  - Auto-transition tickets: enabled
  - Post progress comments: disabled
  - Create sub-tasks from plan: disabled
- Confluence Integration: enabled
  - Auto-publish docs on completion: enabled
  - Read existing docs for context: enabled
```

Set any feature to `disabled` to turn it off for that project. Agents check these preferences before using MCP tools.

## Hooks

Hooks execute shell scripts at agent lifecycle points for safety and auditing.

| Hook | Event | Purpose |
|------|-------|---------|
| `tool-guardian` | PreToolUse | Blocks destructive commands (`rm -rf /`, `DROP TABLE`, `--force` push, etc.) and prompts for confirmation on risky operations (`git push`, `terraform apply`) |
| `session-logger` | SessionStart, Stop | Writes JSON-lines audit trail to `.copilot-logs/sessions.jsonl` |

Hook files live in `.github/hooks/` and are auto-discovered by VS Code. Scripts are cross-platform Python in `.github/hooks/scripts/`.

## Prompts (Entry Points)

| Prompt | Routes To | Use Case |
|--------|-----------|----------|
| `/PRD to MVP` | Project Lead | Full SDLC cycle from a PRD or requirements |
| `/Create PRD` | PRD Generator | Guided interview to produce a structured PRD |
| `/Bug Fix` | Project Lead | Streamlined discovery → fix → test → review |
| `/Feature Add` | Project Lead | Full SDLC minus architecture (unless needed) |
| `/Code Review` | Reviewer | Direct 4-lens review (correctness, security, quality, architecture) |
| `/Refactor` | Developer | Behavior-preserving quality improvements |

## How to Use

### Full SDLC from PRD
1. Use the `/PRD to MVP` prompt and paste your PRD or requirements
2. The Project Lead orchestrates all phases automatically

### Create a PRD First
1. Use the `/Create PRD` prompt with a product description or Jira ticket key
2. Review and iterate the PRD
3. Use the "Execute PRD" handoff button to start the SDLC

### Quick Actions
- **Fix a bug**: Use `/Bug Fix` with a description, error message, or Jira ticket key
- **Add a feature**: Use `/Feature Add` with requirements or a Jira ticket key
- **Review code**: Use `/Code Review` with a description of what to review
- **Refactor**: Use `/Refactor` with the target files or modules

### Manual Phase-by-Phase
1. Open any agent from the Copilot Chat agent picker
2. Complete the phase
3. Use the handoff button to advance to the next agent

### From a Jira Ticket
1. Use the `/PRD to MVP` prompt with a Jira ticket key (e.g., `PROJ-123`)
2. The Project Lead reads the ticket, transitions it to In Progress, and runs the SDLC

## Extending This Framework

### Adding a New Agent
Create `agents/your-agent.agent.md` with proper frontmatter. See `instructions/agent-authoring.instructions.md` for standards.

### Adding a New Skill
Create `skills/your-skill/SKILL.md` with `name` and `description` frontmatter. Reference it from agent files.

### Adding a New Instruction
Create `instructions/your-rule.instructions.md` with `description` and `applyTo` frontmatter.

### Adding a New Prompt
Create `prompts/your-prompt.prompt.md` with `agent` field routing to the target agent.

### Adding a New Hook
Create `.github/hooks/your-hook.json` with a `hooks` object mapping event names to command arrays. Scripts go in `.github/hooks/scripts/`. See `tool-guardian.json` for reference.

## Plugin Packaging

This framework can be installed as a VS Code agent plugin. Others can install it via:

```
Chat: Install Plugin From Source → paste the Git repository URL
```

The `plugin.json` at root provides metadata. VS Code auto-discovers agents, skills, prompts, hooks, and instructions from the standard directory structure.

## Remaining Roadmap

- **Agentic Workflows**: CI automation via GitHub Actions

## References:
- **GitHub Copilot Best Practices**: https://docs.github.com/en/copilot/get-started/best-practices
- **GitHub Copilot Guide**: https://github.com/github/awesome-copilot/tree/main
- **Test Driven Development Guide**: https://code.visualstudio.com/docs/copilot/guides/test-driven-development-guide
- **VSCode Context Engineering Guide**: https://code.visualstudio.com/docs/copilot/guides/context-engineering-guide

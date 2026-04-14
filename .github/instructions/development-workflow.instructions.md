---
description: 'Development workflow standards covering branching strategy, environment activation, pre-commit quality gates, and multi-language project setup. Auto-applied to all source files to enforce consistent development practices.'
applyTo: '**/*.py, **/*.ts, **/*.js, **/*.jsx, **/*.tsx, **/*.go, **/*.rs, **/*.cs, **/*.java, **/*.toml, **/*.json, **/*.yaml, **/*.yml'
---

# Development Workflow Standards

## Branching Strategy

### Greenfield Projects

Create long-lived branches from `main` before any implementation:

```
main
 ├── dev        ← daily development, all feature branches merge here
 └── test       ← release candidates, merged from dev when stable
```

Create these branches using the GitHub MCP `create_branch` tool (preferred) or `git switch -c <branch>`. Switch to `dev` before starting any coding work.

### Existing Projects

**Never work directly on `dev` or `main`.** Create a short-lived branch from `dev`:

| Work Type | Branch Pattern | Example |
|-----------|---------------|---------|
| Feature | `feature/<ticket-or-slug>` | `feature/PROJ-42-user-auth` |
| Bug fix | `bugfix/<ticket-or-slug>` | `bugfix/PROJ-99-null-crash` |
| Discovery / spike | `discovery/<slug>` | `discovery/llm-provider-eval` |
| Refactor | `refactor/<slug>` | `refactor/extract-adapter` |

Use the GitHub MCP `create_branch` tool when available. Include the Jira ticket key in the branch name when one exists.

### Before Coding — Branch Checklist

1. Confirm the current branch (`git branch --show-current`).
2. If on `main` or `dev`, create and switch to a work branch.
3. Pull latest: `git pull origin dev` (or `main` for greenfield setup).

## Environment Activation

**Always activate or use the project environment before running any terminal command.** Detect the stack and use the correct approach:

### Python (UV)

```bash
# Preferred — runs command inside the UV-managed environment
uv run <command>

# Setup if no environment exists
uv init                    # creates pyproject.toml
uv add <packages>          # adds dependencies
uv sync                    # installs from lockfile
```

- All commands: `uv run pytest`, `uv run python main.py`, `uv run ruff check .`
- Add packages: `uv add <package>` (never `pip install`)
- Dev dependencies: `uv add --dev <package>`

### Node.js / TypeScript

```bash
# Detect package manager from lockfile
# package-lock.json → npm | pnpm-lock.yaml → pnpm | yarn.lock → yarn

npm ci                     # install from lockfile (CI-safe)
npx <command>              # run project-local binaries

# Setup if no environment exists
npm init -y                # creates package.json
npm install <packages>     # adds dependencies
```

- All commands: `npx jest`, `npx eslint .`, `npx prettier --check .`
- Add packages: `npm install <package>` / `pnpm add <package>` / `yarn add <package>`
- Dev dependencies: `npm install --save-dev <package>`

### .NET

```bash
dotnet restore             # install from project file
dotnet run                 # run the project
dotnet test                # run tests
```

### Go

```bash
go mod tidy                # sync dependencies
go run .                   # run the project
go test ./...              # run tests
```

### Rust

```bash
cargo build                # compile and install dependencies
cargo run                  # run the project
cargo test                 # run tests
```

### Detection Rule

Before running any command, check for these files to identify the stack:

| File | Stack | Environment Command |
|------|-------|-------------------|
| `pyproject.toml` / `uv.lock` | Python (UV) | `uv run <cmd>` |
| `requirements.txt` | Python (pip) | Activate `.venv` first |
| `package.json` | Node.js | `npx <cmd>` or `npm run <script>` |
| `go.mod` | Go | Direct (`go <cmd>`) |
| `Cargo.toml` | Rust | Direct (`cargo <cmd>`) |
| `*.csproj` / `*.sln` | .NET | Direct (`dotnet <cmd>`) |

## Pre-Commit Quality Gates

Before any `git commit`, run the project's quality checks. If they fail, fix the issues before committing.

### Python (UV + Ruff)

```bash
uv run ruff check . --fix        # lint and auto-fix
uv run ruff format .             # format
uv run pytest tests/ -x -q       # tests (fail-fast)
uv run pip-audit                  # dependency vulnerability check (if installed)
```

### Node.js (ESLint + Prettier)

```bash
npx eslint . --fix               # lint and auto-fix
npx prettier --write .           # format
npx jest --bail                  # tests (fail-fast)
npm audit --audit-level=moderate # dependency vulnerability check
```

### .NET

```bash
dotnet format                    # format
dotnet build --warnaserror       # compile with warnings as errors
dotnet test                      # tests
```

### Go

```bash
go vet ./...                     # lint
gofmt -w .                       # format
go test ./...                    # tests
```

### Rust

```bash
cargo clippy -- -D warnings      # lint
cargo fmt                        # format
cargo test                       # tests
```

### Pre-Commit Execution Rule

1. **Detect the stack** using the file table above.
2. **Run lint → format → test** in that order.
3. If any step fails:
   - **Lint / format failures**: auto-fix and re-run.
   - **Test failures**: diagnose and fix the source code, then re-run.
4. Only proceed to `git commit` when all checks pass.
5. **Never** use `--no-verify` to skip pre-commit hooks.

## Project Initialisation — Multi-Stack

When setting up a new project, initialise the correct tooling:

| Stack | Init Command | Dev Dependencies to Add |
|-------|-------------|------------------------|
| Python | `uv init` | `uv add --dev ruff pytest` |
| Node.js | `npm init -y` | `npm i -D eslint prettier jest` |
| .NET | `dotnet new <template>` | Built-in formatting + xUnit |
| Go | `go mod init <module>` | `go vet` + `gofmt` are built-in |
| Rust | `cargo init` | `clippy` + `rustfmt` are built-in |

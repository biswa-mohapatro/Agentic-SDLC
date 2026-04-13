#!/usr/bin/env python3
"""Tool Guardian — PreToolUse hook that blocks destructive commands.

Reads JSON from stdin (VS Code hook input), checks terminal commands against
threat patterns, and outputs a permission decision via JSON to stdout.
"""
import json
import re
import sys

# Patterns that DENY execution (exit 0 with permissionDecision: deny)
DENY_PATTERNS = [
    (r"\brm\s+-rf\s+/", "Recursive delete from root"),
    (r"\bDROP\s+(TABLE|DATABASE|SCHEMA)\b", "Database DROP operation"),
    (r"\bTRUNCATE\s+TABLE\b", "Table truncation"),
    (r"\bgit\s+push\b.*--force", "Force push"),
    (r"\bgit\s+reset\s+--hard\b", "Hard reset"),
    (r"\bchmod\s+777\b", "World-writable permissions"),
    (r"\bFormat-Volume\b", "Volume format"),
    (r"\bRemove-Item\s+[^|]*-Recurse[^|]*-Force", "Forced recursive delete (PowerShell)"),
    (r"\b(del|rmdir)\s+/[sS]\b", "Recursive delete (Windows CMD)"),
    (r"\bcurl\b.*\|\s*(ba)?sh\b", "Pipe-to-shell execution"),
    (r"\bwget\b.*\|\s*(ba)?sh\b", "Pipe-to-shell execution"),
    (r"\beval\s*\(", "Dynamic code evaluation"),
    (r"\b--no-verify\b", "Bypassing verification hooks"),
    (r"\bsudo\s+rm\b", "Privileged file deletion"),
    (r"\bmkfs\b", "Filesystem format"),
    (r"\bdd\s+if=.*of=/dev/", "Raw disk write"),
    (r">\s*/etc/passwd\b", "Overwrite system file"),
    (r"\bDELETE\s+FROM\s+\S+\s*;?\s*$", "Unfiltered DELETE (no WHERE clause)"),
    (r"\bgit\s+branch\s+-[dD]\s+main\b", "Delete main branch"),
    (r"\bgit\s+branch\s+-[dD]\s+master\b", "Delete master branch"),
]

# Patterns that ASK for user confirmation (exit 0 with permissionDecision: ask)
ASK_PATTERNS = [
    (r"\bgit\s+push\b", "Git push — confirm target branch"),
    (r"\bnpm\s+publish\b", "Package publish to registry"),
    (r"\bdocker\s+rm\b", "Docker container removal"),
    (r"\bkubectl\s+delete\b", "Kubernetes resource deletion"),
    (r"\bterraform\s+destroy\b", "Infrastructure destruction"),
    (r"\bterraform\s+apply\b", "Infrastructure apply"),
    (r"\bcurl\b.*-X\s*(DELETE|PUT|POST)\b", "Mutating HTTP request"),
    (r"\bgit\s+checkout\s+--\s+\.", "Discard all local changes"),
    (r"\bgit\s+clean\s+-fd\b", "Remove untracked files"),
    (r"\bpip\s+install\b(?!.*-r\b)", "Package installation"),
    (r"\bnpm\s+install\b(?!.*package\.json)", "Package installation"),
]

# Tools that execute commands (check these for threat patterns)
TERMINAL_TOOLS = {
    "run_in_terminal",
    "run_command",
    "execute",
    "bash",
    "shell",
    "terminal",
}


def main():
    try:
        data = json.load(sys.stdin)
    except (json.JSONDecodeError, EOFError):
        sys.exit(0)  # Can't parse input — allow by default

    tool_name = data.get("tool_name", "")
    tool_input = data.get("tool_input", {})

    # Only inspect terminal/command execution tools
    if tool_name not in TERMINAL_TOOLS:
        sys.exit(0)

    # Extract command string from tool input
    command = (
        tool_input.get("command", "")
        or tool_input.get("input", "")
        or tool_input.get("cmd", "")
        or ""
    )
    if not command:
        sys.exit(0)

    # Check DENY patterns first (most restrictive)
    for pattern, reason in DENY_PATTERNS:
        if re.search(pattern, command, re.IGNORECASE):
            json.dump(
                {
                    "hookSpecificOutput": {
                        "hookEventName": "PreToolUse",
                        "permissionDecision": "deny",
                        "permissionDecisionReason": f"Blocked by tool-guardian: {reason}",
                    }
                },
                sys.stdout,
            )
            sys.exit(0)

    # Check ASK patterns (require user confirmation)
    for pattern, reason in ASK_PATTERNS:
        if re.search(pattern, command, re.IGNORECASE):
            json.dump(
                {
                    "hookSpecificOutput": {
                        "hookEventName": "PreToolUse",
                        "permissionDecision": "ask",
                        "permissionDecisionReason": f"Confirm: {reason}",
                    }
                },
                sys.stdout,
            )
            sys.exit(0)

    # Default: allow
    sys.exit(0)


if __name__ == "__main__":
    main()

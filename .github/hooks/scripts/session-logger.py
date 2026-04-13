#!/usr/bin/env python3
"""Session Logger — Logs agent session start/stop events for audit trails.

Writes JSON-lines to .copilot-logs/sessions.jsonl in the workspace root.
Each line records a session lifecycle event with timestamp and session ID.
"""
import json
import os
import sys
from datetime import datetime, timezone


def main():
    try:
        data = json.load(sys.stdin)
    except (json.JSONDecodeError, EOFError):
        sys.exit(0)

    cwd = data.get("cwd", os.getcwd())
    log_dir = os.path.join(cwd, ".copilot-logs")
    log_file = os.path.join(log_dir, "sessions.jsonl")

    entry = {
        "timestamp": data.get("timestamp", datetime.now(timezone.utc).isoformat()),
        "event": data.get("hookEventName", "unknown"),
        "sessionId": data.get("sessionId", "unknown"),
        "cwd": cwd,
    }

    try:
        os.makedirs(log_dir, exist_ok=True)
        with open(log_file, "a", encoding="utf-8") as f:
            f.write(json.dumps(entry) + "\n")
    except OSError:
        pass  # Logging failure should never block the agent

    sys.exit(0)


if __name__ == "__main__":
    main()

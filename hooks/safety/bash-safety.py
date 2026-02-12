#!/usr/bin/env python3
"""
Bash Safety Hook for Claude Code
Auto-allows safe bash commands (e.g. non-recursive rm) to reduce permission prompts.

Hook Type: PreToolUse (PermissionRequest matcher)
Matcher: Bash
Exit Codes:
  0 - Always (outputs decision JSON or nothing)

Usage in settings.json:
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Bash",
        "hooks": [{"type": "command", "command": "python3 hooks/safety/bash-safety.py"}]
      }
    ]
  }

How it works:
  - Intercepts Bash tool permission requests
  - Auto-allows `rm` commands that do not use recursive flags (-r, -R, -rf, -fr)
  - Recursive rm commands fall through to the normal permission prompt
  - All other Bash commands are unaffected (normal prompt shows)

CUSTOMISE: Add more auto-allow patterns for commands you trust.
"""
import json
import re
import sys

try:
    raw_input = sys.stdin.read()
    if not raw_input or not raw_input.strip():
        sys.exit(0)
    data = json.loads(raw_input)
except (json.JSONDecodeError, ValueError, EOFError):
    sys.exit(0)

command = data.get("tool_input", {}).get("command", "").strip()

# Only handle rm commands — everything else gets the normal prompt
if not re.match(r"^rm\s", command):
    sys.exit(0)

# Prompt for any recursive rm: -r, -R, -rf, -fr, -r -f, etc.
is_recursive = bool(re.search(r"-[a-zA-Z]*[rR]", command))

if not is_recursive:
    # Safe rm (single files, no recursion) — auto-allow
    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "PermissionRequest",
            "decision": {"behavior": "allow"}
        }
    }))

# Recursive rm: output nothing, normal permission prompt shows
sys.exit(0)

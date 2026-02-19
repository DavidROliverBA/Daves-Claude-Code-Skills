#!/usr/bin/env python3
"""PermissionRequest hook for Bash commands.

Auto-allows `rm` commands unless they include recursive flags (-r, -R, -rf, -fr).
All other non-allowed Bash commands fall through to the normal permission prompt.
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

# Only handle rm commands - everything else gets the normal prompt
if not re.match(r"^rm\s", command):
    sys.exit(0)

# Prompt for any recursive rm: -r, -R, -rf, -fr, -r -f, etc.
is_recursive = bool(re.search(r"-[a-zA-Z]*[rR]", command))

if not is_recursive:
    # Safe rm (single files, no recursion) - auto-allow
    print(json.dumps({
        "hookSpecificOutput": {
            "hookEventName": "PermissionRequest",
            "decision": {"behavior": "allow"}
        }
    }))

# Recursive rm: output nothing, normal permission prompt shows
sys.exit(0)

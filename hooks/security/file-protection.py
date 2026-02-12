#!/usr/bin/env python3
"""
File Protection Hook for Claude Code
Blocks edits to sensitive files like .env, lockfiles, private keys, and credentials.

Hook Type: PreToolUse
Matcher: Edit|Write
Exit Codes:
  0 - Success (file is safe to edit)
  2 - Block (file is protected)

Usage in settings.json:
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [{"type": "command", "command": "python3 hooks/security/file-protection.py"}]
      }
    ]
  }
"""

import json
import os
import re
import sys
from pathlib import Path

# Customise: patterns for files that should never be edited by AI
PROTECTED_PATTERNS = [
    r"\.env$",
    r"\.env\..*",
    r".*\.pem$",
    r".*\.key$",
    r".*\.p12$",
    r".*\.pfx$",
    r".*_rsa$",
    r".*_dsa$",
    r".*_ecdsa$",
    r".*_ed25519$",
    r"credentials\.json$",
    r"secrets\.json$",
    r"package-lock\.json$",
    r"yarn\.lock$",
    r"poetry\.lock$",
    r"Gemfile\.lock$",
    r"composer\.lock$",
    r"Cargo\.lock$",
    r"\.secrets\.baseline$",
    r"settings\.json$",
]

# Customise: directories that are safe to edit (relative to project root)
ALLOWED_DIRECTORIES = [
    "docs/",
    "tests/",
    ".claude/skills/",
    ".claude/hooks/",
    ".claude/scripts/",
]


def is_protected_file(file_path: str) -> bool:
    """Check if file matches protected patterns."""
    for pattern in PROTECTED_PATTERNS:
        if re.search(pattern, file_path):
            return True
    return False


def is_in_allowed_directory(file_path: str) -> bool:
    """Check if file is in an allowed directory."""
    for allowed_dir in ALLOWED_DIRECTORIES:
        if file_path.startswith(allowed_dir) or f"/{allowed_dir}" in file_path:
            return True
    return False


def main():
    try:
        raw_input = sys.stdin.read()
        if not raw_input or not raw_input.strip():
            sys.exit(0)
        input_data = json.loads(raw_input)
    except (json.JSONDecodeError, ValueError, EOFError):
        sys.exit(0)
    except Exception:
        sys.exit(0)

    tool_name = input_data.get("tool_name", "")
    tool_input = input_data.get("tool_input", {})

    if tool_name not in ("Edit", "Write"):
        sys.exit(0)

    file_path = tool_input.get("file_path", "")
    if not file_path:
        sys.exit(0)

    # Convert to relative path for checking
    file_path_rel = file_path.lstrip("/")

    # Allow files in explicitly allowed directories
    if is_in_allowed_directory(file_path_rel):
        sys.exit(0)

    # Block protected files
    if is_protected_file(file_path):
        reason_msg = (
            f"🔒 File protection: {file_path} is protected from AI edits.\n\n"
            f"This file contains sensitive configuration or lockfile data.\n"
            f"To edit this file, modify PROTECTED_PATTERNS in file-protection.py."
        )
        output = {
            "decision": "block",
            "reason": reason_msg
        }
        print(json.dumps(output))
        sys.exit(0)

    sys.exit(0)


if __name__ == "__main__":
    main()

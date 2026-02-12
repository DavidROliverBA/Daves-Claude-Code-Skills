#!/usr/bin/env python3
"""
Code Formatting Hook for Claude Code
Automatically formats files after editing based on file type.

Runs formatters (Prettier, Black, gofmt, rustfmt, shfmt) on files after
Claude edits them. Formatters must be installed separately.

Hook Type: PostToolUse
Matcher: Edit|Write
Exit Codes:
  0 - Always (non-blocking hook)

Usage in settings.json:
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [{"type": "command", "command": "python3 hooks/ux/code-formatter.py"}]
      }
    ]
  }
"""

import json
import subprocess
import sys
from pathlib import Path

FORMATTERS = {
    ".js": ["npx", "prettier", "--write"],
    ".jsx": ["npx", "prettier", "--write"],
    ".ts": ["npx", "prettier", "--write"],
    ".tsx": ["npx", "prettier", "--write"],
    ".json": ["npx", "prettier", "--write"],
    ".yaml": ["npx", "prettier", "--write"],
    ".yml": ["npx", "prettier", "--write"],
    ".css": ["npx", "prettier", "--write"],
    ".scss": ["npx", "prettier", "--write"],
    ".html": ["npx", "prettier", "--write"],
    ".py": ["black", "--quiet"],
    ".go": ["gofmt", "-w"],
    ".rs": ["rustfmt"],
    ".sh": ["shfmt", "-w"],
    ".bash": ["shfmt", "-w"],
}

SKIP_PATTERNS = [
    "node_modules/",
    ".git/",
    "dist/",
    "build/",
    ".next/",
    "__pycache__/",
    ".venv/",
    "venv/",
]

def find_project_root(file_path: str) -> str | None:
    path = Path(file_path).resolve()
    for parent in [path] + list(path.parents):
        if (parent / ".git").exists():
            return str(parent)
    return None

def should_skip(file_path: str) -> bool:
    for pattern in SKIP_PATTERNS:
        if pattern in file_path:
            return True
    return False

def format_file(file_path: str) -> str | None:
    if should_skip(file_path):
        return None
    path = Path(file_path)
    if not path.exists():
        return None
    ext = path.suffix.lower()
    if ext not in FORMATTERS:
        return None
    formatter_cmd = FORMATTERS[ext] + [file_path]
    try:
        result = subprocess.run(
            formatter_cmd,
            capture_output=True,
            text=True,
            timeout=8
        )
        if result.returncode == 0:
            return f"Formatted {path.name} with {formatter_cmd[0]}"
        else:
            if result.stderr:
                print(f"Format warning for {path.name}: {result.stderr[:100]}", file=sys.stderr)
            return None
    except FileNotFoundError:
        return None
    except subprocess.TimeoutExpired:
        print(f"Format timeout for {path.name}", file=sys.stderr)
        return None

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
    file_path = input_data.get("tool_input", {}).get("file_path", "")

    if tool_name not in ("Edit", "Write"):
        sys.exit(0)

    if not file_path:
        sys.exit(0)

    project_root = find_project_root(file_path)
    if not project_root:
        sys.exit(0)

    message = format_file(file_path)

    if message:
        output = {"additionalContext": message}
        print(json.dumps(output))

    sys.exit(0)

if __name__ == "__main__":
    main()

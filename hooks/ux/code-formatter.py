#!/usr/bin/env python3
"""
Code Formatting Hook for Claude Code
Automatically formats files after editing based on file type.

Hook Type: PostToolUse
Matcher: Edit|Write
Exit Codes:
  0 - Always (non-blocking hook)
"""

import json
import subprocess
import sys
from pathlib import Path

# Formatter configuration by file extension
# Each entry: extension -> [command, args...]
FORMATTERS = {
    # JavaScript/TypeScript (Prettier)
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

    # Python (Black)
    ".py": ["black", "--quiet"],

    # Go
    ".go": ["gofmt", "-w"],

    # Rust
    ".rs": ["rustfmt"],

    # Shell (shfmt)
    ".sh": ["shfmt", "-w"],
    ".bash": ["shfmt", "-w"],
}

# Files to skip (even if extension matches)
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


def should_skip(file_path: str) -> bool:
    """Check if file should be skipped."""
    for pattern in SKIP_PATTERNS:
        if pattern in file_path:
            return True
    return False


def format_file(file_path: str) -> str | None:
    """Format file based on extension. Returns message if formatted, None otherwise."""
    if should_skip(file_path):
        return None

    path = Path(file_path)

    # Check file exists
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
            timeout=8  # Must be less than hook timeout (10s)
        )
        if result.returncode == 0:
            return f"Formatted {path.name} with {formatter_cmd[0]}"
        else:
            # Formatter failed, but don't block - just log
            if result.stderr:
                print(f"Format warning for {path.name}: {result.stderr[:100]}", file=sys.stderr)
            return None
    except FileNotFoundError:
        # Formatter not installed, skip silently
        return None
    except subprocess.TimeoutExpired:
        print(f"Format timeout for {path.name}", file=sys.stderr)
        return None


def main():
    # Startup guard: exit gracefully if no valid input
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

    # Only run after Edit or Write
    if tool_name not in ("Edit", "Write"):
        sys.exit(0)

    if not file_path:
        sys.exit(0)

    # Only format files inside the Obsidian vault.
    # Hooks fire for ALL Edit/Write operations regardless of target repo.
    # When working cross-repo (e.g. /tmp/claude/), skip silently to avoid
    # running formatters on files that may have their own formatting config.
    VAULT_ROOT = "."
    if not file_path.startswith(VAULT_ROOT):
        sys.exit(0)

    message = format_file(file_path)

    # Output using additionalContext JSON format
    if message:
        output = {"additionalContext": message}
        print(json.dumps(output))

    # Always exit 0 - formatting is non-blocking
    sys.exit(0)


if __name__ == "__main__":
    main()

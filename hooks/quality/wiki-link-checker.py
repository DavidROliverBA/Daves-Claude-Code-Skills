#!/usr/bin/env python3
"""
Wiki-Link Checker Hook for Claude Code
Validates that [[wiki-links]] point to existing markdown files.

Hook Type: PostToolUse
Matcher: Edit|Write
Exit Codes:
  0 - Success (all links valid or file is not markdown)
  1 - Warning (broken links found but not blocking)

Usage in settings.json:
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [{"type": "command", "command": "python3 hooks/quality/wiki-link-checker.py"}]
      }
    ]
  }
"""

import json
import os
import re
import sys
from pathlib import Path

# Customise: note type prefixes to check
NOTE_PREFIXES = [
    "Project - ",
    "Meeting - ",
    "Task - ",
    "Reference - ",
    "_MOC - ",
]


def find_vault_root(start_path: str) -> Path | None:
    """Find vault root by looking for .obsidian directory."""
    current = Path(start_path).resolve()
    while current != current.parent:
        if (current / ".obsidian").exists():
            return current
        current = current.parent
    return None


def get_all_markdown_files(vault_root: Path) -> set[str]:
    """Get all markdown file basenames (without .md) in vault."""
    md_files = set()
    for md_file in vault_root.rglob("*.md"):
        basename = md_file.stem
        md_files.add(basename)
    return md_files


def extract_wiki_links(content: str) -> list[str]:
    """Extract [[wiki-links]] from content."""
    # Match [[link]] or [[link|alias]]
    pattern = r"\[\[([^\]\|]+)(?:\|[^\]]*)?\]\]"
    matches = re.findall(pattern, content)
    return matches


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
    if not file_path or not file_path.endswith(".md"):
        sys.exit(0)

    # Find vault root
    vault_root = find_vault_root(file_path)
    if not vault_root:
        sys.exit(0)

    # Get content
    content = ""
    if tool_name == "Write":
        content = tool_input.get("content", "")
    elif tool_name == "Edit":
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
        except Exception:
            sys.exit(0)

    if not content:
        sys.exit(0)

    # Extract wiki links
    wiki_links = extract_wiki_links(content)
    if not wiki_links:
        sys.exit(0)

    # Get all markdown files in vault
    md_files = get_all_markdown_files(vault_root)

    # Check for broken links
    broken_links = []
    for link in wiki_links:
        if link not in md_files:
            broken_links.append(link)

    if broken_links:
        output = {
            "decision": "allow",
            "message": f"⚠️ Broken wiki-links in {file_path}:\n" + "\n".join(f"  • [[{link}]]" for link in broken_links)
        }
        print(json.dumps(output))
        sys.exit(0)

    sys.exit(0)


if __name__ == "__main__":
    main()

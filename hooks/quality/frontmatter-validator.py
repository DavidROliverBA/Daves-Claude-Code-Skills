#!/usr/bin/env python3
"""
Frontmatter Validator Hook for Claude Code
Validates YAML frontmatter in markdown files against note type schemas.

Hook Type: PostToolUse
Matcher: Edit|Write
Exit Codes:
  0 - Success (frontmatter is valid or file is not markdown)
  1 - Warning (validation failed but not blocking)

Usage in settings.json:
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [{"type": "command", "command": "python3 hooks/quality/frontmatter-validator.py"}]
      }
    ]
  }
"""

import json
import os
import re
import sys
from pathlib import Path

# Customise: note types and their required fields
NOTE_SCHEMAS = {
    "Post": ["type", "title", "created", "tags"],
    "Project": ["type", "title", "created", "status", "tags"],
    "Meeting": ["type", "title", "date", "attendees", "tags"],
    "Person": ["type", "name", "created", "tags"],
    "Task": ["type", "title", "created", "status", "priority", "tags"],
    "Reference": ["type", "title", "created", "url", "tags"],
    "Daily": ["type", "date", "tags"],
    "MOC": ["type", "title", "created", "tags"],
}


def find_project_root(start_path: str) -> Path | None:
    """Find project root by looking for .obsidian or .git directory."""
    current = Path(start_path).resolve()
    while current != current.parent:
        if (current / ".obsidian").exists() or (current / ".git").exists():
            return current
        current = current.parent
    return None


def extract_frontmatter(content: str) -> dict | None:
    """Extract YAML frontmatter from markdown content."""
    if not content.startswith("---"):
        return None
    
    parts = content.split("---", 2)
    if len(parts) < 3:
        return None
    
    yaml_content = parts[1].strip()
    frontmatter = {}
    
    for line in yaml_content.split("\n"):
        line = line.strip()
        if ":" in line:
            key, value = line.split(":", 1)
            key = key.strip()
            value = value.strip()
            frontmatter[key] = value
    
    return frontmatter


def validate_frontmatter(frontmatter: dict, file_path: str) -> list[str]:
    """Validate frontmatter against note type schema."""
    errors = []
    
    note_type = frontmatter.get("type", "")
    if not note_type:
        errors.append("Missing required field: type")
        return errors
    
    schema = NOTE_SCHEMAS.get(note_type)
    if not schema:
        # Unknown type, skip validation
        return []
    
    for required_field in schema:
        if required_field not in frontmatter or not frontmatter[required_field]:
            errors.append(f"Missing required field for {note_type}: {required_field}")
    
    return errors


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

    # Get content
    content = ""
    if tool_name == "Write":
        content = tool_input.get("content", "")
    elif tool_name == "Edit":
        # For Edit, read the full file after edit
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
        except Exception:
            sys.exit(0)

    if not content:
        sys.exit(0)

    frontmatter = extract_frontmatter(content)
    if not frontmatter:
        # No frontmatter, skip validation
        sys.exit(0)

    errors = validate_frontmatter(frontmatter, file_path)
    
    if errors:
        output = {
            "decision": "allow",
            "message": f"⚠️ Frontmatter validation issues in {file_path}:\n" + "\n".join(f"  • {e}" for e in errors)
        }
        print(json.dumps(output))
        sys.exit(0)

    sys.exit(0)


if __name__ == "__main__":
    main()

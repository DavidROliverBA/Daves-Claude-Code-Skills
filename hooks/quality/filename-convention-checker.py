#!/usr/bin/env python3
"""
Filename Convention Checker Hook for Claude Code
Validates filenames against note type conventions.

Hook Type: PostToolUse
Matcher: Edit|Write
Exit Codes:
  0 - Success (filename is valid)
  1 - Warning (filename doesn't match conventions but not blocking)

Usage in settings.json:
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [{"type": "command", "command": "python3 hooks/quality/filename-convention-checker.py"}]
      }
    ]
  }
"""

import json
import os
import re
import sys
from pathlib import Path

# Customise: note types and their conventions
FILENAME_CONVENTIONS = {
    "Post": {
        "prefix": "Post - ",
        "location": "root",
    },
    "Project": {
        "prefix": "Project - ",
        "location": "Projects/",
    },
    "Meeting": {
        "prefix": "Meeting - ",
        "location": "Meetings/",
    },
    "Task": {
        "prefix": "Task - ",
        "location": "Tasks/",
    },
    "Daily": {
        "prefix": None,
        "location": "Daily/",
        "pattern": r"\d{4}-\d{2}-\d{2}\.md$",
    },
    "MOC": {
        "prefix": "_MOC - ",
        "location": "root",
    },
}


def find_project_root(start_path: str) -> Path | None:
    """Find project root by looking for .obsidian or .git directory."""
    current = Path(start_path).resolve()
    while current != current.parent:
        if (current / ".obsidian").exists() or (current / ".git").exists():
            return current
        current = current.parent
    return None


def extract_note_type_from_content(content: str) -> str | None:
    """Extract note type from YAML frontmatter."""
    if not content.startswith("---"):
        return None
    
    parts = content.split("---", 2)
    if len(parts) < 3:
        return None
    
    yaml_content = parts[1]
    
    # Match type line
    type_match = re.search(r"type:\s*([^\n]+)", yaml_content)
    if not type_match:
        return None
    
    return type_match.group(1).strip().strip('"').strip("'")


def validate_filename(file_path: str, note_type: str, project_root: Path) -> list[str]:
    """Validate filename against conventions."""
    errors = []
    
    conventions = FILENAME_CONVENTIONS.get(note_type)
    if not conventions:
        # Unknown type, skip validation
        return []
    
    file_name = Path(file_path).name
    file_rel_path = str(Path(file_path).relative_to(project_root))
    
    # Check prefix
    if conventions.get("prefix"):
        if not file_name.startswith(conventions["prefix"]):
            errors.append(f"Filename should start with '{conventions['prefix']}' for {note_type} notes.")
    
    # Check pattern (for Daily notes)
    if conventions.get("pattern"):
        if not re.search(conventions["pattern"], file_name):
            errors.append(f"Filename doesn't match expected pattern for {note_type} notes.")
    
    # Check location
    expected_location = conventions.get("location")
    if expected_location and expected_location != "root":
        if not file_rel_path.startswith(expected_location):
            errors.append(f"{note_type} notes should be in {expected_location} directory.")
    
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

    # Find project root
    project_root = find_project_root(file_path)
    if not project_root:
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

    # Extract note type
    note_type = extract_note_type_from_content(content)
    if not note_type:
        sys.exit(0)

    # Validate filename
    errors = validate_filename(file_path, note_type, project_root)
    
    if errors:
        output = {
            "decision": "allow",
            "message": f"⚠️ Filename convention issues in {file_path}:\n" + "\n".join(f"  • {e}" for e in errors)
        }
        print(json.dumps(output))
        sys.exit(0)

    sys.exit(0)


if __name__ == "__main__":
    main()

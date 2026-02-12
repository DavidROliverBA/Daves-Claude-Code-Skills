#!/usr/bin/env python3
"""
Tag Taxonomy Enforcer Hook for Claude Code
Enforces hierarchical tag taxonomy and prevents flat tags.

Hook Type: PostToolUse
Matcher: Edit|Write
Exit Codes:
  0 - Success (tags are valid or file is not markdown)
  1 - Warning (invalid tags found but not blocking)

Usage in settings.json:
  "hooks": {
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [{"type": "command", "command": "python3 hooks/quality/tag-taxonomy-enforcer.py"}]
      }
    ]
  }
"""

import json
import os
import re
import sys
from pathlib import Path

# Customise: hierarchical tag taxonomy
TAG_HIERARCHIES = {
    "area": ["engineering", "design", "marketing", "ops"],
    "project": ["example-app", "docs-site"],
    "technology": ["python", "javascript", "react", "docker", "aws"],
    "status": ["draft", "review", "published"],
    "type": ["guide", "reference", "tutorial", "api-docs"],
}

# Customise: approved flat tags (no hierarchy required)
APPROVED_FLAT_TAGS = ["pinned", "draft", "archive", "wip"]


def find_project_root(start_path: str) -> Path | None:
    """Find project root by looking for .obsidian or .git directory."""
    current = Path(start_path).resolve()
    while current != current.parent:
        if (current / ".obsidian").exists() or (current / ".git").exists():
            return current
        current = current.parent
    return None


def extract_tags_from_frontmatter(content: str) -> list[str]:
    """Extract tags from YAML frontmatter."""
    if not content.startswith("---"):
        return []
    
    parts = content.split("---", 2)
    if len(parts) < 3:
        return []
    
    yaml_content = parts[1]
    
    # Match tags line
    tags_match = re.search(r"tags:\s*\[([^\]]*)\]", yaml_content)
    if not tags_match:
        return []
    
    tags_str = tags_match.group(1)
    tags = [t.strip().strip('"').strip("'") for t in tags_str.split(",")]
    return [t for t in tags if t]


def validate_tags(tags: list[str]) -> list[str]:
    """Validate tags against taxonomy."""
    errors = []
    
    for tag in tags:
        # Remove # prefix if present
        tag = tag.lstrip("#")
        
        # Check if flat tag is approved
        if "/" not in tag:
            if tag not in APPROVED_FLAT_TAGS:
                errors.append(f"Flat tag '{tag}' not in approved list. Use hierarchical tags like 'area/engineering'.")
            continue
        
        # Check hierarchical tag
        parts = tag.split("/")
        if len(parts) < 2:
            continue
        
        category = parts[0]
        value = parts[1]
        
        if category in TAG_HIERARCHIES:
            if value not in TAG_HIERARCHIES[category]:
                errors.append(f"Tag '{tag}': value '{value}' not in taxonomy for category '{category}'.")
    
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
        try:
            with open(file_path, "r", encoding="utf-8") as f:
                content = f.read()
        except Exception:
            sys.exit(0)

    if not content:
        sys.exit(0)

    tags = extract_tags_from_frontmatter(content)
    if not tags:
        sys.exit(0)

    errors = validate_tags(tags)
    
    if errors:
        output = {
            "decision": "allow",
            "message": f"⚠️ Tag taxonomy issues in {file_path}:\n" + "\n".join(f"  • {e}" for e in errors)
        }
        print(json.dumps(output))
        sys.exit(0)

    sys.exit(0)


if __name__ == "__main__":
    main()

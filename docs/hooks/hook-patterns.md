# Hook Patterns

Common implementation patterns for Claude Code hooks.

## 1. Blocking Validation

**Use case:** Prevent dangerous operations (PreToolUse only)

**Pattern:**

```python
import json
import sys

def main():
    input_data = json.loads(sys.stdin.read())
    
    # Extract tool information
    tool_name = input_data.get("tool_name", "")
    tool_input = input_data.get("tool_input", {})
    
    # Validation logic
    if should_block(tool_input):
        output = {
            "decision": "block",
            "reason": "Operation not allowed"
        }
        print(json.dumps(output))
        sys.exit(2)  # MUST exit 2 to block
    
    sys.exit(0)  # Allow

if __name__ == "__main__":
    main()
```

**Exit code:** 2 (block)

**Examples:** file-protection.py, secret-file-scanner.py

---

## 2. Warning Notification

**Use case:** Alert user to issues without blocking (PostToolUse)

**Pattern:**

```python
import json
import sys

def main():
    input_data = json.loads(sys.stdin.read())
    
    # Check for issues
    issues = check_for_problems(input_data)
    
    if issues:
        output = {
            "decision": "allow",
            "message": f"⚠️ Issues found:
{format_issues(issues)}"
        }
        print(json.dumps(output))
        sys.exit(1)  # Exit 1 for warning
    
    sys.exit(0)

if __name__ == "__main__":
    main()
```

**Exit code:** 1 (warn)

**Examples:** frontmatter-validator.py, tag-taxonomy-enforcer.py

---

## 3. Context Injection

**Use case:** Add information to Claude's context (UserPromptSubmit)

**Pattern:**

```python
import json
import sys

def main():
    input_data = json.loads(sys.stdin.read())
    prompt = input_data.get("prompt", "")
    
    # Detect keywords and inject context
    context = None
    if "project" in prompt.lower():
        context = load_project_conventions()
    
    if context:
        output = {
            "decision": "allow",
            "context": context
        }
        print(json.dumps(output))
    
    sys.exit(0)

if __name__ == "__main__":
    main()
```

**Exit code:** 0

**Use:** Dynamically load context based on user intent

---

## 4. Auto-Allow Pattern

**Use case:** Hook always allows but processes data

**Pattern:**

```python
import json
import sys

def main():
    try:
        input_data = json.loads(sys.stdin.read())
        
        # Do processing (logging, stats, etc.)
        process_data(input_data)
        
    except Exception as e:
        # Log error but don't block
        sys.stderr.write(f"Hook error: {e}
")
    
    # Always exit 0 (allow)
    sys.exit(0)

if __name__ == "__main__":
    main()
```

**Exit code:** 0 (always)

**Examples:** backup-trigger.py, auto-commit-trigger.py

---

## 5. Notification Pattern

**Use case:** Inform user without blocking or warning

**Pattern:**

```python
import json
import sys

def main():
    input_data = json.loads(sys.stdin.read())
    
    # Gather information
    info = collect_info(input_data)
    
    # Show notification (exit 0 = no warning symbol)
    output = {
        "decision": "allow",
        "message": f"ℹ️ {info}"
    }
    print(json.dumps(output))
    sys.exit(0)

if __name__ == "__main__":
    main()
```

**Exit code:** 0 (informational)

**Difference from warning:** Exit 0 doesn't show ⚠️ symbol

---

## 6. Project Root Detection

**Use case:** Find vault/repo root for path-relative operations

**Pattern:**

```python
from pathlib import Path

def find_project_root(start_path: str) -> Path | None:
    """Find project root by looking for marker files."""
    current = Path(start_path).resolve()
    
    # Check for common markers
    markers = [".obsidian", ".git", "package.json", "pyproject.toml"]
    
    while current \!= current.parent:
        for marker in markers:
            if (current / marker).exists():
                return current
        current = current.parent
    
    return None

# Usage
file_path = tool_input.get("file_path", "")
project_root = find_project_root(file_path)
if not project_root:
    sys.exit(0)  # Skip if not in a project
```

**Use:** Path normalization, relative path checks, vault-wide operations

**Examples:** wiki-link-checker.py, filename-convention-checker.py

---

## 7. Startup Guard Pattern

**Use case:** Skip processing for non-relevant events/tools

**Pattern:**

```python
import json
import sys

def main():
    try:
        raw_input = sys.stdin.read()
        if not raw_input or not raw_input.strip():
            sys.exit(0)  # Empty input, skip
        
        input_data = json.loads(raw_input)
    except (json.JSONDecodeError, ValueError, EOFError):
        sys.exit(0)  # Invalid JSON, skip
    except Exception:
        sys.exit(0)  # Any error, skip
    
    # Check if this hook cares about this event
    tool_name = input_data.get("tool_name", "")
    if tool_name not in ("Edit", "Write"):
        sys.exit(0)  # Not our tool, skip
    
    # Check file type
    file_path = tool_input.get("file_path", "")
    if not file_path or not file_path.endswith(".md"):
        sys.exit(0)  # Not markdown, skip
    
    # Now do the real work
    process_file(input_data)
    sys.exit(0)

if __name__ == "__main__":
    main()
```

**Purpose:** Fail gracefully and exit early for irrelevant events

**Used in:** Nearly all hooks

---

## 8. Configurable Data Pattern

**Use case:** Make hook behaviour customisable without code changes

**Pattern:**

```python
# Customise: Add your patterns here
PROTECTED_PATTERNS = [
    r"\.env$",
    r".*\.key$",
    r"credentials\.json$",
]

# Customise: Add your allowed directories here
ALLOWED_DIRECTORIES = [
    "docs/",
    "tests/",
]

# Load from environment if available
import os
if os.getenv("PROTECTED_FILES"):
    PROTECTED_PATTERNS.extend(os.getenv("PROTECTED_FILES").split(","))
```

**Best practices:**
- Use `# Customise:` comments to mark configurable sections
- Provide sensible defaults
- Support environment variable overrides
- Document expected format

**Examples:** All security and quality hooks use this pattern

---

## Full Example: File Type Validator

Combines multiple patterns:

```python
#\!/usr/bin/env python3
"""
File Type Validator Hook
Blocks writing executable files to docs directory.

Hook Type: PreToolUse
Matcher: Write
"""

import json
import sys
from pathlib import Path

# Pattern 8: Configurable data
BLOCKED_EXTENSIONS = [".exe", ".sh", ".bat", ".cmd"]
PROTECTED_DIRS = ["docs/", "guides/"]

# Pattern 6: Project root detection
def find_project_root(start_path: str) -> Path | None:
    current = Path(start_path).resolve()
    while current \!= current.parent:
        if (current / ".git").exists():
            return current
        current = current.parent
    return None

def main():
    # Pattern 7: Startup guard
    try:
        raw_input = sys.stdin.read()
        if not raw_input:
            sys.exit(0)
        input_data = json.loads(raw_input)
    except Exception:
        sys.exit(0)
    
    tool_name = input_data.get("tool_name", "")
    if tool_name \!= "Write":
        sys.exit(0)
    
    tool_input = input_data.get("tool_input", {})
    file_path = tool_input.get("file_path", "")
    
    # Find project root
    project_root = find_project_root(file_path)
    if not project_root:
        sys.exit(0)
    
    # Check if in protected directory
    rel_path = Path(file_path).relative_to(project_root)
    in_protected = any(str(rel_path).startswith(d) for d in PROTECTED_DIRS)
    
    if not in_protected:
        sys.exit(0)
    
    # Pattern 1: Blocking validation
    file_ext = Path(file_path).suffix.lower()
    if file_ext in BLOCKED_EXTENSIONS:
        output = {
            "decision": "block",
            "reason": f"Cannot write {file_ext} files to docs directory"
        }
        print(json.dumps(output))
        sys.exit(2)
    
    sys.exit(0)

if __name__ == "__main__":
    main()
```

---

## Pattern Selection Guide

| Need | Pattern | Event | Exit Code |
|------|---------|-------|-----------|
| Block dangerous operation | Blocking | PreToolUse | 2 |
| Alert to issues | Warning | PostToolUse | 1 |
| Add context to prompt | Context Injection | UserPromptSubmit | 0 |
| Always process but allow | Auto-Allow | Any | 0 |
| Show info without warning | Notification | Any | 0 |
| Find vault/repo root | Project Root | Any | N/A |
| Skip irrelevant events | Startup Guard | Any | N/A |
| Make hook customisable | Configurable Data | Any | N/A |

## Further Reading

- [Hook Lifecycle](./hook-lifecycle.md) — Events and I/O schemas
- [README](./README.md) — Hook overview
- [Configuration](./configuration.md) — settings.json reference

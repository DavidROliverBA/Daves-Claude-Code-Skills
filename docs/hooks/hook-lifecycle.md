# Hook Lifecycle

Claude Code hooks execute at specific lifecycle events during conversations and tool usage.

## Hook Events

| Event | When It Fires | Common Use Cases |
|-------|--------------|------------------|
| **PreToolUse** | Before a tool executes | Validation, blocking dangerous operations |
| **PostToolUse** | After a tool executes | Formatting, quality checks, notifications |
| **UserPromptSubmit** | User submits a prompt | Context injection, logging |
| **Stop** | Conversation ends | Cleanup, final backups |
| **PermissionRequest** | Claude requests permission | Custom approval workflows |

### Additional Events

| Event | Description |
|-------|-------------|
| **Start** | Conversation begins |
| **ToolUseApproved** | User approves tool execution |
| **ToolUseDenied** | User denies tool execution |
| **ToolUsePartialFailure** | Some parallel tools failed |
| **AgentSpawn** | Subagent spawned |
| **AgentFinish** | Subagent completed |
| **Notification** | Claude sends notification |

## Event Flow

```
User submits prompt
  ↓
[UserPromptSubmit hooks]
  ↓
Claude generates response with tool calls
  ↓
[PreToolUse hooks] ← Can block here (exit 2)
  ↓
Tool executes (if not blocked)
  ↓
[PostToolUse hooks] ← Can warn here (exit 1)
  ↓
Response shown to user
```

## I/O Schema

### Input (stdin)

Hooks receive JSON via stdin:

```json
{
  "event": "PreToolUse",
  "tool_name": "Edit",
  "tool_input": {
    "file_path": "/path/to/file.md",
    "old_string": "original text",
    "new_string": "updated text"
  },
  "conversation_id": "abc123",
  "timestamp": "2026-02-12T10:30:00Z"
}
```

### Output (stdout)

Hooks output JSON to stdout:

```json
{
  "decision": "block",
  "reason": "File contains API keys",
  "message": "Additional context for user"
}
```

**Decision values:**
- `"allow"` — Continue normal operation
- `"block"` — Prevent tool execution (PreToolUse only)
- `"warn"` — Show warning but continue

**Exit codes must match decision:**
- Exit 0 → allow
- Exit 1 → warn
- Exit 2 → block

## PreToolUse Hooks

### Purpose
Validate tool inputs before execution. Can block dangerous operations.

### Input Schema

```json
{
  "event": "PreToolUse",
  "tool_name": "Write",
  "tool_input": {
    "file_path": "/path/to/.env",
    "content": "API_KEY=secret123"
  }
}
```

### Blocking Example

```python
import json
import sys

input_data = json.loads(sys.stdin.read())

if input_data["tool_input"]["file_path"].endswith(".env"):
    output = {
        "decision": "block",
        "reason": "Cannot edit .env files"
    }
    print(json.dumps(output))
    sys.exit(2)  # MUST exit 2 to block

sys.exit(0)
```

## PostToolUse Hooks

### Purpose
Process results after tool execution. Can warn but not block.

### Input Schema

```json
{
  "event": "PostToolUse",
  "tool_name": "Edit",
  "tool_input": {
    "file_path": "/path/to/note.md"
  },
  "tool_output": {
    "success": true
  }
}
```

### Warning Example

```python
import json
import sys

input_data = json.loads(sys.stdin.read())

# Check file after edit
with open(input_data["tool_input"]["file_path"]) as f:
    content = f.read()

if "TODO" in content:
    output = {
        "decision": "allow",
        "message": "⚠️ File contains TODO items"
    }
    print(json.dumps(output))
    sys.exit(1)  # Exit 1 for warning

sys.exit(0)
```

## UserPromptSubmit Hooks

### Purpose
Process user prompts before Claude responds. Can inject context.

### Input Schema

```json
{
  "event": "UserPromptSubmit",
  "prompt": "Create a new project note",
  "conversation_id": "abc123"
}
```

### Context Injection Example

```python
import json
import sys

input_data = json.loads(sys.stdin.read())

if "project" in input_data["prompt"].lower():
    output = {
        "decision": "allow",
        "context": "Use Project - prefix for project notes"
    }
    print(json.dumps(output))

sys.exit(0)
```

## Stop Hooks

### Purpose
Cleanup or final operations when conversation ends.

### Input Schema

```json
{
  "event": "Stop",
  "conversation_id": "abc123",
  "timestamp": "2026-02-12T11:00:00Z"
}
```

### Cleanup Example

```python
import json
import sys
import subprocess

# Final backup on conversation end
subprocess.run(["git", "add", "-A"])
subprocess.run(["git", "commit", "-m", "Session complete"])

sys.exit(0)
```

## Exit Code Behaviour

| Exit Code | Decision | PreToolUse | PostToolUse | Other Events |
|-----------|----------|------------|-------------|--------------|
| **0** | Allow | Tool executes | Continue | Continue |
| **1** | Warn | ⚠️ Not valid | Show warning | Show message |
| **2** | Block | Tool blocked | ⚠️ Not valid | ⚠️ Not valid |

**Critical rules:**
- PreToolUse: Use exit 2 to block
- PostToolUse: Use exit 1 to warn (cannot block)
- All events: Exit 0 for success

## Error Handling

If a hook crashes or outputs invalid JSON:
- Claude Code logs the error
- The tool continues as if hook returned exit 0
- User sees a notification about hook failure

**Best practice:** Always wrap hook logic in try/except and exit 0 on errors you want to ignore.

```python
try:
    # Hook logic here
    pass
except Exception as e:
    # Log error but don't block
    sys.stderr.write(f"Hook error: {e}
")
    sys.exit(0)
```

## Debugging Hooks

### Test hook with sample input

```bash
echo '{
  "event": "PreToolUse",
  "tool_name": "Write",
  "tool_input": {"file_path": "test.md", "content": "test"}
}' | python3 hooks/security/file-protection.py

echo "Exit code: 0"
```

### Check hook output

```bash
output=$(echo '{}' | python3 hooks/quality/frontmatter-validator.py)
echo "$output" | jq .
```

### Enable hook logging

Set environment variable:

```bash
export CLAUDE_HOOK_DEBUG=1
```

Hooks can check this and write to stderr for debugging.

## Performance Considerations

- Hooks run synchronously and block tool execution
- Keep hook execution time under 100ms for good UX
- For expensive operations (backups, analysis), use PostToolUse
- Consider caching (e.g., vault file list) to avoid repeated disk scans

## Further Reading

- [Hook Patterns](./hook-patterns.md) — Common implementation patterns
- [Configuration Reference](./configuration.md) — settings.json syntax
- [README](./README.md) — Hook overview and examples

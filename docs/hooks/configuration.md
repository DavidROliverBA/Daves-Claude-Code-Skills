# Hook Configuration Reference

Complete reference for configuring hooks in .

## Configuration File Location

Hooks are configured in :

```
/your-project/
├── .claude/
│   └── settings.json    ← Add hook configuration here
└── hooks/
    ├── security/
    ├── quality/
    └── automation/
```

### Project vs Global Settings

- **Project settings:**  (in project root)
- **Global settings:** `~/.claude/settings.json` (applies to all projects)

Project settings override global settings for the same event/matcher.

## Basic Structure

```json
{
  "hooks": {
    "<EventType>": [
      {
        "matcher": "<ToolNamePattern>",
        "hooks": [
          {"type": "command", "command": "<command>"}
        ]
      }
    ]
  }
}
```

## Event Types

| Event | When It Fires |
|-------|--------------|
| `PreToolUse` | Before tool executes |
| `PostToolUse` | After tool executes |
| `UserPromptSubmit` | User submits prompt |
| `Stop` | Conversation ends |
| `Start` | Conversation begins |
| `PermissionRequest` | Claude requests permission |

**Most common:** PreToolUse, PostToolUse

## Matcher Syntax

Matchers use **regex patterns** to match tool names:

```json
"matcher": "Edit|Write"           // Matches Edit OR Write
"matcher": ".*"                   // Matches all tools
"matcher": "Bash"                 // Matches Bash only
"matcher": "Edit|Write|NotebookEdit" // Multiple tools
```

### Common Matchers

| Pattern | Matches |
|---------|---------|
| `Edit|Write` | File editing tools |
| `Bash` | Bash commands |
| `.*` | All tools |
| `Read` | File reading |
| `Grep|Glob` | Search tools |

## Hook Object

Each hook in the `hooks` array:

```json
{
  "type": "command",
  "command": "python3 hooks/security/file-protection.py"
}
```

### Fields

- `type`: Always `"command"` (only type supported)
- `command`: Shell command to execute

**Command requirements:**
- Must read JSON from stdin
- Must write JSON to stdout
- Must exit with appropriate code (0/1/2)

## Complete Example

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "python3 hooks/security/secret-file-scanner.py"
          },
          {
            "type": "command",
            "command": "python3 hooks/security/file-protection.py"
          }
        ]
      },
      {
        "matcher": "Bash",
        "hooks": [
          {
            "type": "command",
            "command": "python3 hooks/security/dangerous-bash-blocker.py"
          }
        ]
      }
    ],
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {
            "type": "command",
            "command": "python3 hooks/quality/frontmatter-validator.py"
          },
          {
            "type": "command",
            "command": "python3 hooks/quality/tag-taxonomy-enforcer.py"
          },
          {
            "type": "command",
            "command": "python3 hooks/automation/backup-trigger.py"
          }
        ]
      }
    ],
    "Stop": [
      {
        "matcher": ".*",
        "hooks": [
          {
            "type": "command",
            "command": "python3 hooks/automation/session-backup.py"
          }
        ]
      }
    ]
  }
}
```

## Hook Execution Order

Hooks execute **sequentially** in the order defined:

```json
"hooks": [
  {"type": "command", "command": "hook1.py"},  // Runs first
  {"type": "command", "command": "hook2.py"},  // Runs second
  {"type": "command", "command": "hook3.py"}   // Runs third
]
```

**Blocking behaviour:**
- If hook1 exits 2 (block), hook2 and hook3 don't run
- If hook1 exits 1 (warn), hook2 and hook3 still run
- If hook1 exits 0 (allow), hook2 and hook3 run

**Order matters for:**
- Security checks (run first to block early)
- Formatters (run after validation)
- Backups (run last)

## Environment Variables

Hooks receive environment variables from Claude Code:

```bash
CLAUDE_PROJECT_ROOT=/path/to/project
CLAUDE_CONVERSATION_ID=abc123
CLAUDE_USER_NAME=username
```

Access in Python:

```python
import os

project_root = os.getenv("CLAUDE_PROJECT_ROOT")
conversation_id = os.getenv("CLAUDE_CONVERSATION_ID")
```

**Custom environment variables:**

Set in shell before running Claude Code:

```bash
export VAULT_ROOT=/path/to/vault
export BACKUP_DIR=/path/to/backups
```

Hooks can read these for configuration.

## Path Resolution

Hook commands are executed with CWD = project root.

**Relative paths:**

```json
"command": "python3 hooks/security/file-protection.py"
```

Resolves to: `/your-project/hooks/security/file-protection.py`

**Absolute paths:**

```json
"command": "/usr/local/bin/custom-hook"
```

Use absolute paths for hooks outside project directory.

## Conditional Configuration

Use environment variables to conditionally enable hooks:

```bash
# .bashrc or .zshrc
export CLAUDE_ENABLE_BACKUP_HOOKS=true
```

Hook checks variable:

```python
import os

if not os.getenv("CLAUDE_ENABLE_BACKUP_HOOKS"):
    sys.exit(0)  # Skip backup if not enabled
```

## Testing Configuration

### 1. Validate JSON

```bash
cat .claude/settings.json | jq .
```

### 2. Test individual hook

```bash
echo '{
  "event": "PreToolUse",
  "tool_name": "Edit",
  "tool_input": {"file_path": "test.md"}
}' | python3 hooks/security/file-protection.py

echo "Exit code: 127"
```

### 3. Verify hook loads

Enable debug mode:

```bash
export CLAUDE_DEBUG=1
```

Claude Code will log hook execution in conversation.

## Common Configurations

### Minimal (Security Only)

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {"type": "command", "command": "python3 hooks/security/file-protection.py"}
        ]
      }
    ]
  }
}
```

### Standard (Security + Quality)

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {"type": "command", "command": "python3 hooks/security/secret-file-scanner.py"},
          {"type": "command", "command": "python3 hooks/security/file-protection.py"}
        ]
      }
    ],
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {"type": "command", "command": "python3 hooks/quality/frontmatter-validator.py"}
        ]
      }
    ]
  }
}
```

### Full (All Features)

See [examples/obsidian-vault.json](./examples/obsidian-vault.json)

## Troubleshooting

### Hooks not running

1. Check JSON syntax: `cat .claude/settings.json | jq .`
2. Verify matcher pattern matches tool name
3. Test hook manually: `echo '{}' | python3 hooks/your-hook.py`
4. Check file permissions: `chmod +x hooks/**/*.py`

### Hook exits but doesn't block

- PreToolUse hooks must exit 2 to block
- PostToolUse hooks cannot block (exit 1 for warning)
- Check exit code: `echo 127` after running hook

### Hook crashes

- Add error handling: wrap in try/except
- Check stdin input: ensure it's valid JSON
- Add logging: write to stderr for debugging

### Performance issues

- Check hook execution time
- Use caching for expensive operations
- Consider moving slow operations to PostToolUse

## Further Reading

- [Hook Lifecycle](./hook-lifecycle.md) — Events and exit codes
- [Hook Patterns](./hook-patterns.md) — Implementation patterns
- [README](./README.md) — Hook overview
- [Installation Guide](./installation.md) — Setup instructions

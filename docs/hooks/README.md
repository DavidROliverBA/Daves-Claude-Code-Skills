# Claude Code Hooks Guide

Hooks allow you to customise and extend Claude Code's behaviour by running custom scripts at specific lifecycle events. This guide covers the 12 production-ready hooks in this repository.

## Quick Start

1. Copy hooks to your project: `cp -r hooks/ /your-project/`
2. Add hook configuration to `.claude/settings.json`
3. Test: `echo '{}' | python3 hooks/security/secret-detection.py`

See [installation.md](./installation.md) for detailed setup instructions.

## Available Hooks

### Security (3 hooks)

| Hook | Event | Purpose | Exit Code |
|------|-------|---------|-----------|
| [**secret-detection.py**](../../hooks/security/secret-detection.py) | UserPromptSubmit | Scans prompts for API keys, tokens, passwords (25 patterns) | 2 = block |
| [**secret-file-scanner.py**](../../hooks/security/secret-file-scanner.py) | PreToolUse (Edit\|Write) | Scans file content being written for embedded secrets | 2 = block |
| [**file-protection.py**](../../hooks/security/file-protection.py) | PreToolUse (Edit\|Write) | Blocks edits to .env, lockfiles, private keys, CI/CD configs | 2 = block |

### Quality (4 hooks)

| Hook | Event | Purpose | Exit Code |
|------|-------|---------|-----------|
| [**frontmatter-validator.py**](../../hooks/quality/frontmatter-validator.py) | PostToolUse (Edit\|Write) | Validates YAML frontmatter against configurable note schemas | 1 = warn |
| [**tag-taxonomy-enforcer.py**](../../hooks/quality/tag-taxonomy-enforcer.py) | PostToolUse (Edit\|Write) | Enforces hierarchical tag taxonomy (e.g. `area/engineering`) | 1 = warn |
| [**wiki-link-checker.py**](../../hooks/quality/wiki-link-checker.py) | PostToolUse (Edit\|Write) | Validates [[wiki-links]] point to existing files | 1 = warn |
| [**filename-convention-checker.py**](../../hooks/quality/filename-convention-checker.py) | PostToolUse (Edit\|Write) | Validates filenames match note type conventions | 1 = warn |

### UX (3 hooks)

| Hook | Event | Purpose | Exit Code |
|------|-------|---------|-----------|
| [**code-formatter.py**](../../hooks/ux/code-formatter.py) | PostToolUse (Edit\|Write) | Auto-formats with Prettier, Black, gofmt, rustfmt, or shfmt | 0 = success |
| [**context-loader.sh**](../../hooks/ux/context-loader.sh) | UserPromptSubmit | Auto-loads context files based on detected skill commands | 0 = success |
| [**search-hint.sh**](../../hooks/ux/search-hint.sh) | PreToolUse (Grep) | Suggests faster search alternatives for simple patterns | 0 = info |

### Safety (1 hook)

| Hook | Event | Purpose | Exit Code |
|------|-------|---------|-----------|
| [**bash-safety.py**](../../hooks/safety/bash-safety.py) | PermissionRequest (Bash) | Auto-allows safe read-only commands to reduce prompts | 0 = allow |

### Notification (1 hook)

| Hook | Event | Purpose | Exit Code |
|------|-------|---------|-----------|
| [**desktop-notify.sh**](../../hooks/notification/desktop-notify.sh) | Notification (Stop) | Desktop notification with sound when Claude finishes | 0 = success |

## Hook Types

| Event | When It Fires | Can Block? |
|-------|--------------|------------|
| **UserPromptSubmit** | User submits a prompt | Yes (exit 2) |
| **PreToolUse** | Before a tool executes | Yes (exit 2) |
| **PostToolUse** | After a tool executes | No (exit 1 = warn) |
| **PermissionRequest** | Claude requests tool permission | Yes (auto-allow) |
| **Notification** | Claude sends notification (Stop, idle, etc.) | No |

See [hook-lifecycle.md](./hook-lifecycle.md) for complete event reference.

## How Hooks Work

1. **Event occurs**: Claude Code triggers an event (e.g., user calls Edit tool)
2. **Matcher checks**: Event type and tool name are matched against hook configuration
3. **Hooks execute**: All matching hooks run in sequence
4. **Decision made**: Based on exit codes (0 = allow, 1 = warn, 2 = block)

### Exit Code Behaviour

| Exit Code | Meaning | Effect |
|-----------|---------|--------|
| **0** | Success | Continue normal operation |
| **1** | Warning | Show message but continue |
| **2** | Block | Prevent tool from executing |

## Configuration

Hooks are configured in `.claude/settings.json` or `.claude/settings.local.json`:

```json
{
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {"type": "command", "command": "python3 hooks/security/file-protection.py", "timeout": 5}
        ]
      }
    ],
    "PostToolUse": [
      {
        "matcher": "Edit|Write",
        "hooks": [
          {"type": "command", "command": "python3 hooks/quality/frontmatter-validator.py", "timeout": 10}
        ]
      }
    ]
  }
}
```

See [configuration.md](./configuration.md) for complete reference.

## Common Patterns

- **Blocking validation**: Use PreToolUse with exit code 2
- **Post-processing**: Use PostToolUse to format/validate after tool runs
- **Warning notifications**: Exit code 1 for non-blocking warnings
- **Auto-detection**: Hooks auto-detect project root via .obsidian/.git
- **Auto-allow**: PermissionRequest hooks with `behavior: allow` reduce prompts

See [hook-patterns.md](./hook-patterns.md) for detailed patterns.

## Customisation

All hooks include `# Customise:` comments marking configurable sections:

```python
# Customise: files to skip scanning
SKIP_PATTERNS = [
    r"\.pre-commit-config\.yaml$",
    r"secret-detection\.py$",
]
```

Common customisations:

| Hook | What to Customise |
|------|-------------------|
| file-protection.py | `PROTECTED_PATTERNS`, `ALLOWED_DIRECTORIES` |
| frontmatter-validator.py | `NOTE_SCHEMAS` — note types and required fields |
| tag-taxonomy-enforcer.py | `TAG_HIERARCHIES` — tag categories and values |
| filename-convention-checker.py | `CONVENTIONS` — filename patterns per type |
| secret-file-scanner.py | `SECRET_PATTERNS`, `SKIP_PATTERNS` |
| context-loader.sh | Skill command to context file mapping |
| bash-safety.py | `SAFE_COMMANDS` — commands to auto-allow |

## Example Configurations

| Configuration | Use Case | Hooks |
|---------------|----------|-------|
| [obsidian-vault.json](./examples/obsidian-vault.json) | Obsidian vault with all 12 hooks | All |
| [python-project.json](./examples/python-project.json) | Python project: security + formatting | 5 |
| [minimal.json](./examples/minimal.json) | Just secret detection + file protection | 2 |

## Further Reading

- [Hook Lifecycle](./hook-lifecycle.md) — Events, I/O schemas, exit codes
- [Hook Patterns](./hook-patterns.md) — Common implementation patterns
- [Configuration Reference](./configuration.md) — settings.json syntax
- [Installation Guide](./installation.md) — Setup and troubleshooting

## Licence

MIT Licence — see LICENCE file for details.
